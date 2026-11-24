#!/usr/bin/env python3
r"""vmrun_guest.py - VMware Guest Operations 包裝工具（免 SSH／免開埠）

透過 VMware Tools 通道（VMCI）在客體作業系統內執行命令與傳檔，
不需要客體開放任何 TCP 埠、不需要 SSH/WinRM、不需要調整客體防火牆。

為什麼需要包裝：
  1. `vmrun` 在帳密錯誤或缺少時會**無限等待認證**，因此所有呼叫都必須強制逾時。
  2. `runProgramInGuest` / `runScriptInGuest` **不回傳 stdout**，
     故一律採用「客體內重導到檔案 -> CopyFileFromGuestToHost 拉回 -> 讀取」流程。

憑證來源（兩種，任選）：
  1. 環境變數（適合臨時使用，但密碼會進入 shell 歷史與命令列）：
        export VM_GU='<guest 使用者>'
        export VM_GP='<guest 密碼>'
        export VM_VMX='C:/path/to/vm.vmx'   # 可省略，預設為本機 Windows 10 x64 這台
  2. 憑證檔（**建議**，密碼不會出現在命令列或對話記錄中）：
        repo 根目錄 `secrets.env`（必須被 Git ignore）或其他 repo 外檔案，內容格式：
            VM_GU=<guest 使用者>
            VM_GP=<guest 密碼>
        使用方式：python vmrun_guest.py --creds-file secrets.env ps
     ※ repo 內憑證檔只有在 `git check-ignore` 明確確認已忽略時才允許讀取；
       未被 ignore 的 repo 內檔案仍會拒絕，避免機敏資訊被誤 commit。

用法:
    python vmrun_guest.py tools
    python vmrun_guest.py ps
    python vmrun_guest.py exec "whoami /all"
    python vmrun_guest.py powershell "Get-Service | Select-Object -First 5"
    python vmrun_guest.py ls "C:\\\\Users"
    python vmrun_guest.py exists "C:\\\\Windows\\\\System32\\\\cmd.exe"
    python vmrun_guest.py put <host_path> <guest_path>
    python vmrun_guest.py get <guest_path> <host_path>
    python vmrun_guest.py kill 4092 1648        # 用 PID 清理殘留行程
    python vmrun_guest.py kill cmd.exe          # 用名稱清理（會先列出行程再殺）

為何需要 kill：
    vmrun 逾時只中止「本機端」的 vmrun.exe，**不會殺掉客體行程**。
    被遗留下來的 `cmd.exe` 會繼續持有輸出檔（`_vmrun_out.txt`）與 payload 檔，
    於是下一次呼叫的重導會建立失敗（cmd 回傳 exit 1），而包裝工具會拉到
    **上一次的舊輸出**——看起來像「指令跑了但沒反應」，實際上根本沒執行。
    遇到這種情況先 `kill cmd.exe powershell.exe` 再重跑。
"""
import argparse
import os
import subprocess
import sys
import tempfile

from safe_paths import resolve_cli_path

DEFAULT_VMRUN = r"C:\MyAPP\VMware Workstation\vmrun.exe"
# No machine-specific default: pass --vmx or set VM_VMX (see secrets.env.example).
DEFAULT_VMX = None
GUEST_CMD = r"C:\Windows\System32\cmd.exe"
GUEST_PS = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
# Path inside the guest VM (written by the guest, never opened on this host).
GUEST_OUT = r"C:\Windows\Temp\_vmrun_out.txt"  # NOSONAR
DEFAULT_TIMEOUT = 90
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_CREDS_FILE = os.path.join(REPO_ROOT, "secrets.env")


class VMError(Exception):
    pass


class Guest:
    def __init__(self, vmx, user, password, vmrun, timeout, guest_out=GUEST_OUT):
        self.vmx = vmx
        self.vmrun = vmrun
        self.timeout = timeout
        self.guest_out = guest_out
        # payload 檔：實際命令寫在這裡，避免把命令内嵌成 vmrun 參數
        self.guest_payload = os.path.dirname(guest_out).replace('/', '\\') + '\\_vmrun_payload.cmd'
        self.auth = []
        if user:
            self.auth = ["-gu", user]
            # password 為 None 表示「未提供」→ 省略 -gp；
            # 空字串則代表「明知是空密碼」→ 必須明確傳 -gp ""，
            # 否則 vmrun 會誤認為未提供而卡住等認證。
            if password is not None:
                self.auth += ["-gp", password]

    def _run(self, args, timeout=None):
        cmd = [self.vmrun, "-T", "ws"] + self.auth + args
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=timeout or self.timeout, errors="replace")
        except subprocess.TimeoutExpired:
            raise VMError(
                f"vmrun 逾時 ({timeout or self.timeout}s) 而中止 —— "
                f"最常見原因是憑證錯誤或缺少 -gu/-gp；請確認 VM_GU / VM_GP"
            )
        return proc.returncode, (proc.stdout or "").strip(), (proc.stderr or "").strip()

    def _require_auth(self):
        if not self.auth:
            raise VMError("此操作需要客體憑證，請設定環境變數 VM_GU 與 VM_GP")

    def info(self):
        code1, out1, _ = self._run(["checkToolsState", self.vmx], timeout=30)
        code2, out2, err2 = self._run(["getGuestIPAddress", self.vmx], timeout=30)
        return {"tools_state": out1 or "(無回應)", "guest_ip": out2 or "(無回應)"}

    def ps(self):
        self._require_auth()
        code, out, err = self._run(["listProcessesInGuest", self.vmx])
        if code != 0:
            raise VMError(f"listProcessesInGuest 失敗 (exit {code}): {err}")
        return out

    def ls(self, guest_dir):
        self._require_auth()
        code, out, err = self._run(["listDirectoryInGuest", self.vmx, guest_dir])
        if code != 0:
            raise VMError(f"listDirectoryInGuest 失敗 (exit {code}): {err}")
        return out

    def exists(self, guest_path):
        self._require_auth()
        code, out, err = self._run(["fileExistsInGuest", self.vmx, guest_path])
        return code == 0, f"{out} {err}".strip()

    def put(self, host_path, guest_path):
        self._require_auth()
        code, _out, err = self._run(["CopyFileFromHostToGuest", self.vmx, host_path, guest_path])
        if code != 0:
            raise VMError(f"CopyFileFromHostToGuest 失敗: {err}")

    def get(self, guest_path, host_path):
        self._require_auth()
        code, _out, err = self._run(["CopyFileFromGuestToHost", self.vmx, guest_path, host_path])
        if code != 0:
            raise VMError(f"CopyFileFromGuestToHost 失敗: {err}")

    def kill(self, pid):
        """終止客體中指定 PID 的行程（vmrun 逾時不會代勞）。"""
        self._require_auth()
        code, out, err = self._run(["killProcessInGuest", self.vmx, str(pid)])
        return code == 0, f"{out} {err}".strip()

    def kill_matching(self, name):
        """依行程名稱片段清理客體行程；回傳 (殺掉的 pid 清單, 找不到的訊息)。"""
        self._require_auth()
        listing = self.ps()
        targets = []
        for line in listing.splitlines():
            if "pid=" not in line:
                continue
            head, _, cmd = line.partition("cmd=")
            if name.lower() not in cmd.lower():
                continue
            for part in head.split(","):
                part = part.strip()
                if part.startswith("pid="):
                    try:
                        targets.append(int(part[4:]))
                    except ValueError:
                        pass
        killed, failures = [], []
        for pid in targets:
            ok, msg = self.kill(pid)
            (killed if ok else failures).append(pid if ok else f"{pid}({msg})")
        return killed, failures

    def run(self, program, arguments="", interactive=False, local_timeout=None, check=True):
        """在客體執行單一程式（不回傳 stdout，需自行重導）。"""
        self._require_auth()
        args = ["runProgramInGuest", self.vmx]
        if interactive:
            args.append("-interactive")
        args += [program, arguments]
        code, out, err = self._run(args, timeout=local_timeout)
        if code != 0 and check:
            raise VMError(f"runProgramInGuest 失敗 (exit {code}): {out} {err}")
        return code, out, err

    def _write_local_cmd(self, content):
        fd, path = tempfile.mkstemp(suffix=".cmd")
        os.close(fd)
        with open(path, "w", newline="\r\n", encoding="ascii", errors="replace") as fh:
            fh.write("@echo off\n")
            fh.write(content + "\n")
        return path

    def _run_payload(self, command_line, local_timeout=None):
        """把命令寫成客體 payload.cmd，執行它，再把輸出拉回本機。

        runProgramInGuest 不回傳 stdout，所以「重導到檔再拉回來」是唯一路徑。
        即使客體程式以非零狀態碼結束仍會拉回輸出，錯誤訊息就在裡面。

        為何把命令寫成 payload .cmd 檔，而不是直接丢給 vmrun：
          vmrun 轉交 argv 給客體時沒保證引用完整，嵌套雙引號會被 cmd
          重新斷詞，殘骸丢給 PowerShell 就變成
          “參數被绑到一格空白”或 PositionalParameterNotFound。
          改成檔案後，PowerShell 語法由 cmd 自己解析，不再經 vmrun argv。

        兩個已踩過並修正的陷阱（両者症狀都是 vmrun 卡死到逾時）：
          1. 不可在 payload 前面再前綴 cmd.exe：payload 本身就由 cmd
             執行，内容變成 `cmd.exe <非開關參數>` 時，cmd 會進入互動模歷
             印出橫幅後永遠等 stdin。payload 第一行就是命令本身。
          2. 不可讓 payload 去執行它自己（會變成 cmd 自我遞迴）。
        """
        self._require_auth()
        if " " in self.guest_out:
            raise VMError(f"guest-out 路徑不可含空白: {self.guest_out}")
        # 外圈括號是必要的：cmd 的重導只绑到「它跟隨的那一個」命令，
        # 所以 `dir & echo hi & tool > out` 會讓前面幾個命令的輸出直接掉在 console。
        local_payload = self._write_local_cmd(f'( {command_line} ) > {self.guest_out} 2>&1')
        try:
            self.put(local_payload, self.guest_payload)
            code, _out, _err = self.run(GUEST_CMD, f'/c {self.guest_payload}',
                                        local_timeout=local_timeout, check=False)
        finally:
            os.remove(local_payload)
        local_out = os.path.join(tempfile.gettempdir(), "_vmrun_out.txt")
        if os.path.exists(local_out):
            os.remove(local_out)
        self.get(self.guest_out, local_out)
        if not os.path.exists(local_out):
            raise VMError(f"客體輸出檔未能取回（runProgramInGuest exit {code}）")
        with open(local_out, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        if code != 0:
            text += f"\n[exit code: {code}]\n"
        return text

    def run_line(self, guest_command, local_timeout=None):
        """執行一整行客體命令（可含引號；引號只存在於 payload 檔，不經 vmrun argv）。"""
        return self._run_payload(guest_command, local_timeout)


def load_creds_file(path, repo_root):
    """從憑證檔讀取 VM_GU / VM_GP。

    repo 內檔案僅在 Git 明確判定為 ignored 時允許使用；這讓本機 lab
    可以保留可重用認證，同時避免未受保護的 secret 被誤加入版控。
    """
    real = str(resolve_cli_path(path))
    inside_repo = False
    if repo_root:
        root = os.path.realpath(repo_root)
        inside_repo = real == root or real.startswith(root + os.sep)
    if inside_repo:
        rel = os.path.relpath(real, root)
        try:
            check = subprocess.run(
                ["git", "-C", root, "check-ignore", "--quiet", "--", rel],
                capture_output=True,
                text=True,
                timeout=10,
                errors="replace",
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise VMError(f"無法確認 repo 內憑證檔是否被 Git ignore: {exc}")
        if check.returncode != 0:
            raise VMError(f"拒絕使用未被 Git ignore 的 repo 內憑證檔: {path}")
    creds = {}
    with open(real, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip().upper()
            if key in ("VM_GU", "VM_GP"):
                creds[key] = value.strip()
    return creds


def main():
    parser = argparse.ArgumentParser(description="VMware Guest Operations 包裝工具")
    parser.add_argument("--vmx", default=os.environ.get("VM_VMX", DEFAULT_VMX))
    parser.add_argument("--vmrun", default=os.environ.get("VM_VMRUN", DEFAULT_VMRUN))
    default_creds = os.environ.get("VM_CREDS_FILE")
    if not default_creds and os.path.isfile(DEFAULT_CREDS_FILE):
        default_creds = DEFAULT_CREDS_FILE
    parser.add_argument("--creds-file", default=default_creds,
                        help="憑證檔路徑（內容為 VM_GU= / VM_GP= 兩行；優先於環境變數）")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--guest-out", default=GUEST_OUT,  # NOSONAR - guest-side path
                        help="客體輸出暫存檔路徑（預設 C:\\Windows\\Temp\\_vmrun_out.txt；UAC 受限時可改使用者暫存目錄）")
    parser.add_argument("--interactive", action="store_true", help="在互動 session 執行（GUI 程式用）")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("tools", help="檢查 VMware Tools 狀態與客體 IP（不需憑證）")
    sub.add_parser("ps", help="列出客體行程")
    sp = sub.add_parser("kill", help="終止客體行程：參數為數字視為 PID，否則視為行程名稱片段")
    sp.add_argument("target", nargs="+")
    sp.add_argument("-n", "--dry-run", action="store_true", help="只列出符合的行程，不實際終止")
    for name in ("exec", "powershell"):
        sp = sub.add_parser(name, help="在客體執行 CMD 指令並取回輸出"
                                 if name == "exec" else "在客體執行 PowerShell 指令並取回輸出")
        sp.add_argument("script", nargs=argparse.REMAINDER,
                        help="客體命令；可直接拆成多個詞（會自動接回一整行）。"
                             " 注意：--timeout 等選項必須寫在命令之前")
    sp = sub.add_parser("ls")
    sp.add_argument("guest_dir")
    sp = sub.add_parser("exists")
    sp.add_argument("guest_path")
    sp = sub.add_parser("put")
    sp.add_argument("host_path")
    sp.add_argument("guest_path")
    sp = sub.add_parser("get")
    sp.add_argument("guest_path")
    sp.add_argument("host_path")
    args = parser.parse_args()
    if not args.vmx:
        parser.error("--vmx is required (or set VM_VMX)")

    user = os.environ.get("VM_GU")
    password = os.environ.get("VM_GP")
    repo_root = REPO_ROOT
    try:
        if args.creds_file:
            creds = load_creds_file(args.creds_file, repo_root)
            user = creds.get("VM_GU", user)
            password = creds.get("VM_GP", password)
        guest = Guest(args.vmx, user, password, args.vmrun, args.timeout, args.guest_out)
        if args.command == "tools":
            info = guest.info()
            print(f"VMware Tools: {info['tools_state']}")
            print(f"客體 IP     : {info['guest_ip']}")
        elif args.command == "ps":
            print(guest.ps())
        elif args.command == "kill":
            for t in args.target:
                if t.isdigit():
                    if args.dry_run:
                        print(f"[dry-run] 會終止 PID {t}")
                        continue
                    ok, msg = guest.kill(int(t))
                    print(f"PID {t}: {'已終止' if ok else '失敗 ' + msg}")
                else:
                    if args.dry_run:
                        listing = guest.ps()
                        hits = [ln for ln in listing.splitlines() if t.lower() in ln.lower()]
                        print(f"[dry-run] 符合 '{t}' 的行程 {len(hits)} 個:")
                        for h in hits:
                            print("   " + h)
                        continue
                    killed, failures = guest.kill_matching(t)
                    print(f"'{t}': 已終止 {killed or '（無）'}　失敗 {failures or '（無）'}")
        elif args.command == "ls":
            print(guest.ls(args.guest_dir))
        elif args.command == "exists":
            ok, msg = guest.exists(args.guest_path)
            print(f"{'存在' if ok else '不存在'}: {msg}")
            sys.exit(0 if ok else 1)
        elif args.command == "put":
            guest.put(args.host_path, args.guest_path)
            print(f"已上傳: {args.host_path} -> {args.guest_path}")
        elif args.command == "get":
            guest.get(args.guest_path, args.host_path)
            print(f"已下載: {args.guest_path} -> {args.host_path}")
        elif args.command == "exec":
            print(guest.run_line(' '.join(args.script), args.timeout))
        elif args.command == "powershell":
            script = args.script if isinstance(args.script, str) else ' '.join(args.script)
            print(guest.run_line(f'{GUEST_PS} -NoProfile -Command "{script}"', args.timeout))
    except VMError as exc:
        print(f"錯誤: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
