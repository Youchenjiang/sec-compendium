# 🐧 Linux 系統基礎加固深度學習路徑 (Linux System Hardening)
> 對應藍隊防衛矩陣：**領域 1** (1.1 ~ 1.4)
> 預計總投入時間：**30 ~ 40 小時**（視 Linux 熟練度而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
會基本 cd/ls/cat 指令   ──►    能依照 CIS Benchmark 獨立加固伺服器
看到權限 777 不知其害  ──►    精通 SUID/SGID/Sticky 與 Linux 權限模型
依賴圖形介面查排程     ──►    精通 systemd timers/crontab 與自啟隱蔽項排查
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| Linux 目錄結構 (FHS) | 熟悉 `/etc`, `/var/log`, `/proc`, `/tmp`, `/bin` 用途 | [Linux Foundation: FHS Guide](https://refspecs.linuxfoundation.org/fhs.shtml) |
| 基本 Bash 命令操作 | 熟練使用 `grep`, `awk`, `sed`, `find`, `cut` 等文字過濾工具 | [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/) |
| 使用者與群組概念 | 知道 UID 0 的意義、`/etc/passwd` 與 `/etc/shadow` 格式 | [Debian Security Manual](https://www.debian.org/doc/manuals/securing-debian-manual/) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 → 階段二 → 階段三 → 階段四 → 階段五
權限模型  環境工具  日誌連線  認證硬化  排程與自啟
(6h)     (2h)     (8h)     (8h)     (10h)
```

---

## 🏁 階段一：底層權限模型與敏感檔案架構（約 6 小時）

### 1.1 Linux 權限三位元組與特殊權限剖析

標準檔案權限以 3 組 3 位元表示（Owner, Group, Others），而特殊權限位元組更常成為攻擊者提權跳板：

```
特殊權限位元 (Special Bits):
├── SUID (4000) : 以檔案擁有者身分執行 (如 /usr/bin/passwd)
├── SGID (2000) : 以檔案群組身分執行，或目錄下新檔案繼承群組
└── Sticky Bit (1000) : 僅擁有者與 root 可刪除該目錄檔案 (如 /tmp: 1777)
```

**🔍 全系統 SUID/SGID 檔案獵捕指令：**
```bash
# 找出所有包含 SUID 的可執行檔
find / -perm -4000 -type f -exec ls -ld {} \; 2>/dev/null

# 找出所有人皆可寫入的目錄 (World-Writable)
find / -type d -perm -0002 -ls 2>/dev/null
```

### 1.2 關鍵系統檔案結構與格式

- `/etc/passwd`：`username:x:UID:GID:Comment:HomeDir:Shell`（若第二欄不是 `x` 而是雜湊，代表存在影子檔案同步弱點）
- `/etc/shadow`：`username:$id$salt$hash:lastchange:min:max:warn:inact:expire`
  - `$1$` = MD5 (已廢棄)
  - `$5$` = SHA-256
  - `$6$` = SHA-512 (標準配置)
  - `$y$` = yescrypt (現代 Linux 預設)

---

## 🔧 階段二：審計工具與基線掃描環境建置（約 2 小時）

### 2.1 安裝自動化安全審計工具 Lynis

```bash
# 在 Ubuntu/Debian 上安裝 Lynis
sudo apt-get update && sudo apt-get install lynis -y

# 執行全系統加固審查並產出報告
sudo lynis audit system --quick
```

### 2.2 導入 CIS Benchmark 基準手冊

- 下載官方 [CIS Distribution-Independent Linux Benchmark](https://www.cisecurity.org/cis-benchmarks/)。
- 重點關注：第 1 節 Initial Setup、第 5 節 Access, Authentication and Authorization。

---

## 🔍 階段三：連線狀態、服務進程與通訊埠排查（約 8 小時）

### 3.1 核心連線排查指令與狀態分析

```bash
# 查看所有監聽中的 TCP/UDP 埠與對應進程名稱/PID
ss -antup | grep -i listen

# 追蹤特定對外連線的執行緒與檔案控制代碼
lsof -i :22
lsof -p <PID>
```

### 3.2 正常服務清單基準線排查

```bash
# 列出所有啟用中的 systemd 服務
systemctl list-unit-files --type=service --state=enabled

# 檢查隱匿的未登錄進程（排查 /proc/ 與 ps 差異）
ls -d /proc/[0-9]* | awk -F/ '{print $3}' | while read pid; do
    if ! ps -p $pid > /dev/null 2>&1; then
        echo "Suspicious Hidden PID: $pid"
    fi
done
```

---

## ⚔️ 階段四：帳號安全與 SSH 遠端存取硬化（約 8 小時）

### 4.1 `/etc/ssh/sshd_config` 加固實務

```ini
# 禁用 Root 直接密碼登入
PermitRootLogin prohibit-password

# 禁用密碼認證，強制採用公開金鑰
PasswordAuthentication no

# 限制最大登入嘗試次數防暴力破解
MaxAuthTries 3

# 啟用高強度密碼交換演算法
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group16-sha512
```

### 4.2 PAM (Pluggable Authentication Modules) 限制

在 `/etc/pam.d/common-auth` 設置帳號鎖定原則：
```ini
auth required pam_faillock.so preauth audit silent deny=5 unlock_time=900
```

---

## ⏰ 階段五：排程作業、自啟動項與持續性後門清剿（約 10 小時）

### 5.1 Crontab 與 Systemd Timers 排查

```bash
# 排查所有使用者與系統 Crontab
cat /etc/crontab
ls -la /etc/cron.*
for user in $(cut -f1 -d: /etc/passwd); do crontab -u $user -l 2>/dev/null; done

# 列出所有 systemd 定時器
systemctl list-timers --all
```

### 5.2 自啟動後門常見藏匿點

1. `/etc/rc.local` 與 `/etc/init.d/`
2. `~/.bashrc`, `~/.bash_profile`, `/etc/profile.d/*.sh`
3. `/etc/ld.so.preload`（惡意共享函式庫劫持）

---

## 📋 自我評估檢查點

- [ ] 能在無提示下寫出查詢全系統所有 SUID 檔案的 `find` 命令。
- [ ] 說出 `/etc/shadow` 中密碼雜湊欄位 `$6$` 與 `$y$` 的意義。
- [ ] 掌握 `ss -antup` 輸出中每一欄代表的連線狀態。
- [ ] 成功在測試主機完成 SSH 僅允許金鑰登入並停用 Root 登入配置。
- [ ] 知道如何清查 `/etc/ld.so.preload` 並解釋其後門劫持機制。

---

## 🏆 實戰推薦靶場

1. **OverTheWire: Bandit (Level 0~24)**：權限模型、文字過濾、SSH 金鑰加固。
2. **SadServers: "Saint John" & "Rosario"**：檔案權限故障排除、SSH 存取恢復實機。
3. **CIS Linux Benchmark 實作評估**：針對本機進行基準檢核修補。
