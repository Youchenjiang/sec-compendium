# 🐧 Linux 主機權限提升與核心安全機制深度自學路徑 (Linux Privilege Escalation Internals)
> 對應紅隊作戰矩陣：**Phase 4 (R18)** (R18.1 ~ R18.6)  
> 預計總投入時間：**25 ~ 30 小時**（視 Linux 系統核心、行程憑據模型與 POSIX 規範基礎而定）

---

## 📍 你在哪裡、去哪裡

```text
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
只會盲目跑 LinPEAS 腳本      ──►     透徹理解 SUID/SGID 權限位元與行程 UID/EUID 切換機制
看到 sudo -l 就隨機亂試      ──►     精通 Sudoers 配置缺陷、env_keep 環境變數與野字符注入
不明白 Kernel 漏洞原理       ──►     理解 Linux Page Cache 與 Dirty Pipe 核心管線髒頁覆寫原理
不知道 NFS 為何能直接變 root ──►     掌握 NFS no_root_squash 跨主機 UID 信任邊界穿透
```

---

## 🧱 第零關：先確認你有這些基礎

| 核心先備概念 | 需要了解到的程度 | 快速補強公開資源 |
| :--- | :--- | :--- |
| Linux 行程身分模型 | 清楚區分 Real UID (RUID)、Effective UID (EUID)、Saved UID (SUID) | [Linux Kernel: Credentials Documentation](https://docs.kernel.org/security/credentials.html) |
| POSIX 文件存取權限 | 理解 File Mode Bits (12-bit)、rwx 以及 Octal 4000/2000 語意 | [GNU coreutils: File permissions](https://www.gnu.org/software/coreutils/manual/html_node/File-permissions.html) |
| Linux 系統調用與管道 | 理解 `setuid()`、`execve()` 與 Linux Pipe 緩衝區結構 | [man 2 setuid](https://man7.org/linux/man-pages/man2/setuid.2.html) ｜ [man 7 pipe](https://man7.org/linux/man-pages/man7/pipe.7.html) |
| Linux Capabilities | 理解線程能力模型（CAP_SETUID, CAP_DAC_OVERRIDE 等 41 種權限分割） | [man 7 capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html) |

---

## 🗺️ 整體學習地圖（四個階段）

```text
階段一 (6h) ──────► 階段二 (8h) ──────► 階段三 (8h) ──────► 階段四 (6h)
SUID/Capabilities   Sudoers配置缺陷     Kernel漏洞機制      Cron野字符/NFS
權限位元與能力分割    與安全環境變數      (Dirty Pipe覆寫)    與防禦加固稽核
```

---

## 🏛️ 階段一：SUID/SGID 機制與 Linux Capabilities 權限細粒度分割（約 6 小時）

### 1.1 SUID 運作本質與行程憑證（Process Credentials）
當執行具備 SUID (Octal 4000) 的可執行檔時，Linux 核心會將行程的 `EUID`（有效使用者 ID）設定為該二進位檔案的擁有者（Owner），而非執行者的 `RUID`（實際使用者 ID）。
- **GTFOBins 突破原理**：若具備 SUID 的程式支援執行外部命令（如 `find -exec`、`vim` 呼叫 Shell），且該程式未在呼叫 `execve()` 前主動 drop 權限，則啟動的子行程將繼承 EUID 0 (root)。
- **檢查指令**：
  ```bash
  find / -perm -4000 -type f -exec ls -la {} 2>/dev/null \;
  ```

### 1.2 Linux Capabilities 繞過全能 Root 限制
為避免賦予單一二進位程式完整的 Root 權限，Linux 引入 Capabilities 機制將 Root 的超級權限拆解為 41 種微特權：
- `cap_setuid+ep`：允許行程呼叫 `setuid()` 切換任意 UID。
- `cap_dac_override+ep`：忽略檔案讀寫執行的 DAC 存取控制權限。
- 檢測指令：
  ```bash
  getcap -r / 2>/dev/null
  ```

---

## 🥩 階段二：Sudoers 弱配置、安全環境變數與野字符劫持（約 8 小時）

### 2.1 `sudo -l` 與規則解析
`/etc/sudoers` 檔案中允許特定使用者以其他身分執行指定指令：
- **NOPASSWD 濫用**：若包含 `(ALL) NOPASSWD: /usr/bin/python3`，可直接藉由內建 `pty.spawn("/bin/bash")` 取得 root。
- **LD_PRELOAD / env_keep**：若配置包含 `Defaults env_keep += "LD_PRELOAD"`，執行 sudo 時會保留攻擊者指定的共享庫預載入路徑，導致動態鏈接器在程式啟動前優先載入自訂惡意 `.so`。

### 2.2 Cron 排程工作與 Wildcard（萬用字元）注入
當 root 的 Crontab 執行如 `tar czf backup.tar.gz *` 時：
- `tar` 會將目錄下以 `--checkpoint=1` 和 `--checkpoint-action=exec=sh exploit.sh` 命名的檔案視為命令列參數。
- 攻擊者透過 `touch -- '--checkpoint=1'` 製造參數注入，實現無特權檔案觸發 Root 程式碼執行。

---

## 🔬 階段三：Linux 核心漏洞機制深潛——以 Dirty Pipe (CVE-2022-0847) 為例（約 8 小時）

### 3.1 漏洞本質：Linux Page Cache 管道緩衝區標誌位未初始化
- Linux 管道（Pipe）底層透過 `pipe_buffer` 環狀陣列管理記憶體頁面。
- 5.8 核心引入 `PIPE_BUF_FLAG_CAN_MERGE` 旗標以加速資料拼接。
- `splice()` 系統調用允許直接將唯讀檔案的 Page Cache 頁面映射至管道環中，但在未清空 `PIPE_BUF_FLAG_CAN_MERGE` 的情況下，後續寫入管道的資料會直接污染該唯讀 Page Cache 記憶體頁！
- **利用結果**：無特權使用者可任意覆寫唯讀檔案（如 `/etc/passwd` 或具備 SUID 的二進位程式），達成即時本地提權。

---

## 🛡️ 階段四：防禦對策、稽核追蹤與實踐檢驗（約 6 小時）

### 4.1 防禦加固標準
1. **分割掛載點**：對 `/tmp`, `/dev/shm`, `/var/tmp` 設定 `noexec,nosuid,nodev` 掛載旗標。
2. **Auditd 系統調用審計**：監控敏感二進位檔案的執行與屬性變更（例如監控 `setuid`, `setgid`, `chmod`）。
3. **NFS 安全配置**：所有跨網路共享目錄嚴格啟用預設的 `root_squash`，禁止 `no_root_squash`。

---

## 📋 自我評估檢查點
- [ ] 能向他人清楚解釋 RUID、EUID 與 SUID 在作業系統核心中的轉換關係。
- [ ] 能在無自動化工具輔助下，純手動枚舉系統中異常 SUID 與 Capabilities 檔案。
- [ ] 能分析 Sudoers 設定檔中 `env_reset`、`secure_path` 與 `LD_PRELOAD` 的安全邊界。
- [ ] 能解釋 Tar Wildcard 注入時命令列解析器處理檔名的底層原理。
- [ ] 能說明 Page Cache 與 Pipe Buffer 互動時發生 Dirty Pipe 漏洞的根本成因。

---

## 🏆 推薦實戰靶場與題庫直達
1. **GTFOBins 官方權威參考庫**：精研各種 Unix 二進位檔案的 SUID/Sudo 提權利用語法。[GTFOBins](https://gtfobins.github.io/)
2. **SadServers 免費 Linux 排錯靶場**：在真實 Linux 終端練習權限排查與服務調試。[SadServers](https://sadservers.com/)
3. **Hack The Box Starting Point (Linux Track)**：循序練習從初始低權限訪問到 Linux Root 提權全流程。[HTB Starting Point](https://app.hackthebox.com/starting-point)
