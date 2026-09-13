# 🛡️ 資訊安全讀書會 6 個月密集衝刺路線圖 (Member Edition)

> [!IMPORTANT]
> **當前版本**: `v2.0` (對齊版 - 1 Run = 2 天 / 雙軌攻防實戰)
> **發布日期**: 2026-08-08
> **版本變更說明**: 
> 1. 本版本已將 **Linux CLI 命令行與 Docker 靶場搭設** 列為 **`Day 0 前置自備門檻`**，不再佔用正式 2 天的 Run 名額！
> 2. 正式 **Run 1 ~ Run 15**（Month 1 / 共 30 天）全部升級為**純硬核攻防主題**，並提前引入 PWN、逆向、網路與密碼學工具鏈！

---

## 📌 版本變更履歷 (Changelog)

| 版本 (Version) | 發布日期 (Date) | 修訂重點 (Summary of Changes) | 狀態 (Status) |
|---|---|---|---|
| **v1.0** | 2026-08-07 | 初版成員路線圖（含有基礎預備排班） | 已發布 (舊版參照) |
| **v2.0** | 2026-08-08 | **最新執行版**：1 Run = 2 天；增設 Day 0 門檻；Runs 1~15 全面升級純硬核攻防與工具鏈早建 | **目前生效** |

---

## 🛠️ Day 0: 讀書會入會前置自備門檻 (Prerequisites)

> [!TIP]
> 請全體成員在 **Run 1 開始前自行準備並安裝完成**（不佔用讀書會正式聚會時間）：
> 1. **作業系統環境**：安裝 Kali Linux / Ubuntu 虛擬機或 Windows WSL2。
> 2. **容器環境**：安裝 Docker Desktop 與 `docker-compose`。
> 3. **必備命令行**：熟悉 Linux 基本指令（`cd`, `ls`, `grep`, `chmod`, `curl`, `ssh`）。

---

## 🗓️ Month 1: 攻防雙軌與工具鏈早建 (第 1 ~ 30 天 / Run 1 ~ Run 15)

> **時間規則**: **1 個 Run = 2 天 (48小時)**。每週進行 3~4 個 Run，月底進行階段總復盤。

### ⚔️ Month 1 詳細 Run 攻防主題與練習對照表

#### **Run 1 (Day 1-2): HTTP 協定原理與 Burp Suite 代理抓包** `[Web 基礎]`
- **學習目標**: 理解 HTTP 請求/回應頭、狀態碼，掌握 Burp Suite Proxy / Repeater 截獲與改包。
- **研討主題**: 說明 GET 與 POST 的封包差異，以及 Header 欄位（Cookie, Referer, User-Agent）的作用。
- **指定練習關卡**:
  1. PortSwigger: [Unprotected Admin (GET路徑修改)](https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality)
  2. PortSwigger: [User Role Bypass (POST參數改寫)](https://portswigger.net/web-security/access-control/lab-user-role-can-be-bypassed-in-user-profile)

#### **Run 2 (Day 3-4): SQL Injection 基礎與萬能密碼登入繞過** `[Web 基礎]`
- **學習目標**: 理解 SQL 查詢語法、單引號 `'` 閉合原理，掌握 `' OR 1=1--` 萬能密碼成因。
- **研討主題**: 剖析登入驗證 SQL 語法漏洞，說明變數未過濾如何導致語法結構被破壞。
- **指定練習關卡**:
  1. PortSwigger: [SQLi 檢索隱藏數據 (Apprentice)](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data)
  2. PortSwigger: [SQLi 登入繞過 (Apprentice)](https://portswigger.net/web-security/sql-injection/lab-login-bypass)

#### **Run 3 (Day 5-6): 命令執行 (RCE) 與路徑遍歷 (Path Traversal)** `[Web 基礎]`
- **學習目標**: 理解 `system()` / `exec()` 命令拼接符（`;`, `&&`, `|`），掌握 `../` 讀取敏感檔案。
- **研討主題**: Linux / Windows 命令拼接符差異，以及如何過濾 `../` 與特徵字元。
- **指定練習關卡**:
  1. PortSwigger: [Command Injection 簡單命令](https://portswigger.net/web-security/os-command-injection/lab-simple)
  2. PortSwigger: [Path Traversal 讀取passwd](https://portswigger.net/web-security/file-path-traversal/lab-simple)

#### **Run 4 (Day 7-8): Wireshark 網路流量分析與協定防禦** `[Network / DFIR前置]`
- **學習目標**: 掌握 Wireshark 抓包過濾器（`ip.addr`, `http`, `tcp.port`），分析平文密碼與抓包追蹤。
- **研討主題**: HTTP vs HTTPS 流量差異，以及如何在 PCAP 流量包中還原傳輸檔案。
- **指定練習關卡**:
  1. Root-Me: [Network HTTP Headers](https://www.root-me.org/en/Challenges/Network/HTTP-headers)

#### **Run 5 (Day 9-10): 任意檔案上傳與 Webshell 木馬權維** `[Web 基礎]`
- **學習目標**: 理解副檔名繞過、MIME 類型偽造，掌握中國蟻劍 (AntSword) 連接 Webshell。
- **研討主題**: 剖析前端 JS 驗證 vs 後端黑白名單驗證，以及 Webshell 一句話木馬原理。
- **指定練習關卡**:
  1. PortSwigger: [Webshell 檔案上傳執行](https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload)

#### **Run 6 (Day 11-12): x86/x64 彙編基礎與 GDB / Pwntools 環境建立** `[PWN / Binary前置]`
- **學習目標**: 理解 CPU 暫存器 (EAX, ESP, EBP, EIP)、記憶體堆疊 (Stack) 結構，學會用 Pwntools 撰寫 Python Exp。
- **研討主題**: 畫出函數呼叫時 Stack Frame 的變化，說明 Push/Pop 與 Ret 指令。
- **指定練習關卡**:
  1. pwn.college: [Program Misuse 入門關卡](https://pwn.college/)
  2. Root-Me: [ELF x86 Stack Overflow basic 1](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-Stack-buffer-overflow-basic-1)

#### **Run 7 (Day 13-14): XSS 跨站腳本與 CSRF / SSRF 攻擊** `[Web 客戶端]`
- **學習目標**: 理解 Reflected XSS、Stored XSS、CSRF Token 繞過與 SSRF 內網探測。
- **研討主題**: XSS 同源策略 (SOP)、Cookie HttpOnly 屬性，以及 SSRF 偽造 `http://127.0.0.1` 請求。
- **指定練習關卡**:
  1. PortSwigger: [Reflected XSS 反射型](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)
  2. PortSwigger: [CSRF 無防禦攻擊](https://portswigger.net/web-security/csrf/lab-no-defenses)
  3. PortSwigger: [Basic SSRF 本地偽造](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost)

#### **Run 8 (Day 15-16): Ghidra / IDA Pro 靜態逆向工程基礎** `[Reverse 前置]`
- **學習目標**: 掌握 Ghidra / IDA Pro 反編譯 C 語言偽代碼、尋找 `main` 函數與關鍵字串。
- **研討主題**: 如何在逆向工程中尋找序列號 (Serial Check) 的判斷邏輯。
- **指定練習關卡**:
  1. Root-Me: [PE / ELF Reverse Engineering 基礎題](https://www.root-me.org/en/Challenges/Cracking/)

#### **Run 9 (Day 17-18): 越權漏洞 (IDOR) 與 Cookie/Session 會話劫持** `[Web 邏輯]`
- **學習目標**: 理解平行越權與垂直越權，掌握修改 `id=1001` 越權檢視他人資料。
- **研討主題**: 剖析 Session ID 隨機性不足與 URL 參數硬編碼存取控制缺陷。
- **指定練習關卡**:
  1. PortSwigger: [IDOR 越權讀取信件](https://portswigger.net/web-security/access-control/lab-insecure-direct-object-references)
  2. PortSwigger: [URL Access Control Bypass](https://portswigger.net/web-security/access-control/lab-url-based-access-control-can-be-bypassed)

#### **Run 10 (Day 19-20): Linux / Windows 本地權限提升 (PrivEsc)** `[Red Team 提權]`
- **學習目標**: 理解 SUID 提權、MySQL UDF 提權與 Windows 弱權限服務替換。
- **研討主題**: `find / -perm -4000` 尋找特權指令，以及高權限 SQL 注入轉提權。
- **指定練習關卡**:
  1. OverTheWire: [Bandit (Levels 0-10)](https://overthewire.org/wargames/bandit/)

#### **Run 11 (Day 21-22): SSTI 模板注入與 PHP/Java 反序列化** `[Web 進階]`
- **學習目標**: 理解 Flask Jinja2 SSTI `{{config}}` 洩露、PHP 魔術方法 `__wakeup()` 與 Java 反序列化。
- **研討主題**: 說明物件串行化/反序列化成因，以及 Template 引擎變數解析漏洞。
- **指定練習關卡**:
  1. PortSwigger: [XXE 檔案讀取](https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-retrieve-files)

#### **Run 12 (Day 23-24): PWN 堆疊溢出 (Stack Overflow) 緩衝區溢出** `[Binary / PWN]`
- **學習目標**: 掌握覆寫 EIP / RIP 暫存器、利用 Shellcode 或 `ret2text` 篡改程式執行流。
- **研討主題**: 說明 Buffer Overflow 的記憶體佈局，以及 NOP Sled 的作用。
- **指定練習關卡**:
  1. pwnable.kr: [bof / fd 經典題](http://pwnable.kr/)

#### **Run 13 (Day 25-26): CryptoHack 密碼學基礎 (RSA / AES 算法原理)** `[Cryptography]`
- **學習目標**: 理解 Base64、XOR 位元運算、RSA 公私鑰數學原理與 AES 對稱加密。
- **研討主題**: 說明公鑰加密與私鑰解密流程，以及大數分解 (p, q, n) 的安全基石。
- **指定練習關卡**:
  1. CryptoHack: [Introduction to Cryptohack](https://cryptohack.org/)

#### **Run 14 (Day 27-28): 內網滲透 (SOCKS5 隧道 / Pivoting / AD 域控攻防)** `[Red Team 內網]`
- **學習目標**: 掌握 MSF / Chisel 搭建 SOCKS5 代理隧道、內網 Port 掃描與 AD 域環境概念。
- **研討主題**: 說明雙網卡主機如何作為跳板 (Pivoting) 穿透內網防火牆。
- **指定練習關卡**:
  1. BlueTeamLabs Online: [Linux Hardening & Network](https://blueteamlabs.online/)

#### **Run 15 (Day 29-30): Month 1 階段總複盤與黑盒 VulnHub 靶機通關** `[Capstone 結業]`
- **學習目標**: 綜合運用 Runs 1~14 所學，獨立對黑盒 VulnHub 虛擬機進行完整滲透並產出 Writeup。
- **研討主題**: 進行 Month 1 復盤簡報，每人分享 VulnHub 靶機打法與筆記。
- **指定練習關卡**:
  1. 本地實體靶機: [Os-hackNos / VulnHub 離線靶機實戰演練](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/15_綜合靶場與VulnHub實戰演練/01_VulnHub與CTF實體靶機)

---

## 📈 成員學習成效評估標準 (Outputs)
1. **筆記產出 (Writeups)**: 每個 Run 結束後，需在個人 GitHub Repo 繳交一份 300 字以上的實操紀錄。
2. **靶場通關率**: 每個 Run 的指定線上關卡（PortSwigger / Root-Me / pwnable.kr）需達 100% 完成率。