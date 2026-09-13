# 🛡️ 資訊安全 6 個月密集主路線圖 (Master Leader Edition)

> [!IMPORTANT]
> **當前版本**: `v2.0` (組長掌控版 - 1 Run = 2 天 / 雙軌攻防實戰)
> **發布日期**: 2026-08-08
> **版本變更說明**: 
> 1. 本版本已將 **Linux CLI 命令行與 Docker 靶場搭設** 列為 **`Day 0 前置自備門檻`**。
> 2. 正式 **Run 1 ~ Run 15**（Month 1 / 共 30 天）全部升級為**純硬核攻防主題**，並對接本地資料庫資料夾與講義影片！

---

## 📌 版本變更履歷 (Changelog)

| 版本 (Version) | 發布日期 (Date) | 修訂重點 (Summary of Changes) | 適用對象 (Audience) |
|---|---|---|---|
| **v1.0** | 2026-08-07 | 初版主路線圖 (組長存檔版) | 組長內部參考 |
| **v2.0** | 2026-08-08 | **最新執行版**：對齊 1 Run = 2 天；Day 0 門檻；Runs 1~15 升級雙軌純攻防與本地資源對接 | **組長正式執行版** |

---

## 🛠️ Day 0: 讀書會入會前置自備門檻 (Prerequisites)

- **作業系統環境**：Kali Linux / Ubuntu 虛擬機或 Windows WSL2。
- **容器環境**：Docker Desktop 與 `docker-compose`。
- **必備命令行**：Linux 基本指令（`cd`, `ls`, `grep`, `chmod`, `curl`, `ssh`）。

---

## 🗓️ Month 1: 攻防雙軌與工具鏈早建 (第 1 ~ 30 天 / Run 1 ~ Run 15)

> **時間規則**: **1 個 Run = 2 天 (48小時)**。

### ⚔️ Month 1 詳細 Run 本地對照與練習清單

#### **Run 1 (Day 1-2): HTTP 協定原理與 Burp Suite 代理抓包** `[Web 基礎]`
- **本地教材**: [`01_Web安全/02_HTTP協定與代理抓包/03_BurpSuite_代理抓包與Repeater`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/02_HTTP協定與代理抓包/03_BurpSuite_代理抓包與Repeater)
- **指定練習關卡**:
  1. PortSwigger: [Unprotected Admin (GET路徑修改)](https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality)
  2. PortSwigger: [User Role Bypass (POST參數改寫)](https://portswigger.net/web-security/access-control/lab-user-role-can-be-bypassed-in-user-profile)

#### **Run 2 (Day 3-4): SQL Injection 基礎與萬能密碼登入繞過** `[Web 基礎]`
- **本地教材**: [`01_Web安全/06_SQL注入漏洞專題/02_SQL注入基礎與GET_POST`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題/02_SQL注入基礎與GET_POST)
- **指定練習關卡**:
  1. PortSwigger: [SQLi 檢索隱藏數據 (Apprentice)](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data)
  2. PortSwigger: [SQLi 登入繞過 (Apprentice)](https://portswigger.net/web-security/sql-injection/lab-login-bypass)

#### **Run 3 (Day 5-6): 命令執行 (RCE) 與路徑遍歷 (Path Traversal)** `[Web 基礎]`
- **本地教材**: [`01_Web安全/07_RCE命令與代碼執行/01_教學影片`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/07_RCE命令與代碼執行/01_教學影片)
- **指定練習關卡**:
  1. PortSwigger: [Command Injection 簡單命令](https://portswigger.net/web-security/os-command-injection/lab-simple)
  2. PortSwigger: [Path Traversal 讀取passwd](https://portswigger.net/web-security/file-path-traversal/lab-simple)

#### **Run 4 (Day 7-8): Wireshark 網路流量分析與協定防禦** `[Network / DFIR前置]`
- **本地教材**: [`06_網路安全與數位取證/01_網路協定分析與Scapy`](file:///f:/OutClass/資訊應用/網路安全/06_網路安全與數位取證/01_網路協定分析與Scapy)
- **指定練習關卡**:
  1. Root-Me: [Network HTTP Headers](https://www.root-me.org/en/Challenges/Network/HTTP-headers)

#### **Run 5 (Day 9-10): 任意檔案上傳與 Webshell 木馬權維** `[Web 基礎]`
- **本地教材**: [`01_Web安全/08_檔案上傳與包含漏洞/01_任意檔案上傳原理`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/08_檔案上傳與包含漏洞/01_任意檔案上傳原理)
- **指定練習關卡**:
  1. PortSwigger: [Webshell 檔案上傳執行](https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload)

#### **Run 6 (Day 11-12): x86/x64 彙編基礎與 GDB / Pwntools 環境建立** `[PWN / Binary前置]`
- **本地教材**: [`02_二進制與逆向/01_x86_x64彙編語言基礎`](file:///f:/OutClass/資訊應用/網路安全/02_二進制與逆向/01_x86_x64彙編語言基礎)
- **指定練習關卡**:
  1. pwn.college: [Program Misuse 入門關卡](https://pwn.college/)
  2. Root-Me: [ELF x86 Stack Overflow basic 1](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-Stack-buffer-overflow-basic-1)

#### **Run 7 (Day 13-14): XSS 跨站腳本與 CSRF / SSRF 攻擊** `[Web 客戶端]`
- **本地教材**: [`01_Web安全/10_客戶端與業務邏輯漏洞/01_XSS跨站腳本挖掘與攻擊`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/10_客戶端與業務邏輯漏洞/01_XSS跨站腳本挖掘與攻擊)
- **指定練習關卡**:
  1. PortSwigger: [Reflected XSS 反射型](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)
  2. PortSwigger: [CSRF 無防禦攻擊](https://portswigger.net/web-security/csrf/lab-no-defenses)
  3. PortSwigger: [Basic SSRF 本地偽造](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost)

#### **Run 8 (Day 15-16): Ghidra / IDA Pro 靜態逆向工程基礎** `[Reverse 前置]`
- **本地教材**: [`02_二進制與逆向/03_Ghidra與IDA_Pro逆向工具`](file:///f:/OutClass/資訊應用/網路安全/02_二進制與逆向/03_Ghidra與IDA_Pro逆向工具)
- **指定練習關卡**:
  1. Root-Me: [PE / ELF Reverse Engineering 基礎題](https://www.root-me.org/en/Challenges/Cracking/)

#### **Run 9 (Day 17-18): 越權漏洞 (IDOR) 與 Cookie/Session 會話劫持** `[Web 邏輯]`
- **本地教材**: [`01_Web安全/10_客戶端與業務邏輯漏洞/04_越權與未授權存取`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/10_客戶端與業務邏輯漏洞/04_越權與未授權存取)
- **指定練習關卡**:
  1. PortSwigger: [IDOR 越權讀取信件](https://portswigger.net/web-security/access-control/lab-insecure-direct-object-references)
  2. PortSwigger: [URL Access Control Bypass](https://portswigger.net/web-security/access-control/lab-url-based-access-control-can-be-bypassed)

#### **Run 10 (Day 19-20): Linux / Windows 本地權限提升 (PrivEsc)** `[Red Team 提權]`
- **本地教材**: [`04_系統與內網安全/03_權限提升/Linux內核提權`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/03_權限提升/Linux內核提權)
- **指定練習關卡**:
  1. OverTheWire: [Bandit (Levels 0-10)](https://overthewire.org/wargames/bandit/)

#### **Run 11 (Day 21-22): SSTI 模板注入與 PHP/Java 反序列化** `[Web 進階]`
- **本地教材**: [`01_Web安全/11_反序列化與組件漏洞/04_SSTI模板注入(Flask_Jinja2)`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/11_反序列化與組件漏洞/04_SSTI模板注入(Flask_Jinja2))
- **指定練習關卡**:
  1. PortSwigger: [XXE 檔案讀取](https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-retrieve-files)

#### **Run 12 (Day 23-24): PWN 堆疊溢出 (Stack Overflow) 緩衝區溢出** `[Binary / PWN]`
- **本地教材**: [`02_二進制與逆向/02_PWN堆疊溢出與緩衝區溢出`](file:///f:/OutClass/資訊應用/網路安全/02_二進制與逆向/02_PWN堆疊溢出與緩衝區溢出)
- **指定練習關卡**:
  1. pwnable.kr: [bof / fd 經典題](http://pwnable.kr/)

#### **Run 13 (Day 25-26): CryptoHack 密碼學基礎 (RSA / AES 算法原理)** `[Cryptography]`
- **本地教材**: [`03_密碼學與隱寫/01_古典密碼與對稱加密_AES_DES`](file:///f:/OutClass/資訊應用/網路安全/03_密碼學與隱寫/01_古典密碼與對稱加密_AES_DES)
- **指定練習關卡**:
  1. CryptoHack: [Introduction to Cryptohack](https://cryptohack.org/)

#### **Run 14 (Day 27-28): 內網滲透 (SOCKS5 隧道 / Pivoting / AD 域控攻防)** `[Red Team 內網]`
- **本地教材**: [`04_系統與內網安全/06_內網滲透與SOCKS5隧道`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/06_內網滲透與SOCKS5隧道)
- **指定練習關卡**:
  1. BlueTeamLabs Online: [Linux Hardening & Network](https://blueteamlabs.online/)

#### **Run 15 (Day 29-30): Month 1 階段總複盤與黑盒 VulnHub 靶機通關** `[Capstone 結業]`
- **本地教材**: [`01_Web安全/15_綜合靶場與VulnHub實戰演練/01_VulnHub與CTF實體靶機`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/15_綜合靶場與VulnHub實戰演練/01_VulnHub與CTF實體靶機)
- **指定練習關卡**:
  1. 本地實體靶機: [Os-hackNos / VulnHub 離線靶機實戰演練](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/15_綜合靶場與VulnHub實戰演練/01_VulnHub與CTF實體靶機)