# 🛡️ 資訊安全 6 個月主路線圖 (Master Leader Instructor Edition - v5.0)

> [!IMPORTANT]
> **當前版本**: `v5.0` (組長帶練與教學總綱)
> **發布日期**: 2026-08-08
> **執行規範 (依據 `ORGANIZATION_RULES.md`)**: 
> 1. **4 欄帶練架構**: 天數 ｜ 🎯 當日教學重點 ｜ 📁 本地影片/檔案與 🌐 線上資源 ｜ 🧪 指定練習與帶練講義/PoC 腳本
> 2. **組長帶練職責**: 為常規學員提供關卡解題思路、PoC 腳本模板（TODO 填空）、帶練提示與 AWD/Capstone 評分。
> 3. **全 180 天 (Day 1 ~ Day 180 / Run 1 ~ Run 90) 100% 逐日獨立對齊**。

## 📌 版本變更履歷 (Changelog)

| 版本 (Version) | 發布日期 (Date) | 修訂重點 (Summary of Changes) | 適用對象 (Audience) |
|---|---|---|---|
| **v1.0** | 2026-08-07 | 舊版 1 Run = 1 天主路線圖 | 歷史歸檔 |
| **v2.0** | 2026-08-08 | 1 Run = 2 天；初步對齊版 | 歷史歸檔 |
| **v5.0** | 2026-08-08 | 導入雙軌必解/延伸關卡對照、AI (CatBoost/SHAP) 與代碼語意分析 (Code Semantics) | **組長正式執行版** |

---

## 🛠️ Day 0: 讀書會入會前置自備門檻 (Prerequisites)

- **作業系統環境**：Kali Linux / Ubuntu 虛擬機或 Windows WSL2。
- **容器環境**：Docker Desktop 與 `docker-compose`。
- **必備命令行**：Linux 基本指令（`cd`, `ls`, `grep`, `chmod`, `curl`, `ssh`）。

---

## 🗓️ Month 1 (第 1 ~ 30 天 / Run 1 ~ Run 15): 攻防雙軌基礎與工具鏈入門

#### ⚔️ **Run 1 (Day 1-2): HTTP 協定原理與 Burp Suite 代理抓包**
📁 **本地對接**: [`01_Web安全/02_HTTP協定與代理抓包`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/02_HTTP協定與代理抓包) ｜ 🌐 **線上專題**: [PortSwigger Access Control](https://portswigger.net/web-security/access-control)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 1** | HTTP 請求與回應標頭分析 (GET/POST/Header/Status Code) | 📁 [`01_Web安全/02_HTTP協定與代理抓包`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/02_HTTP協定與代理抓包) <br>🎥 觀看抓包教學影片 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Insp3ct0r (ID: 367)](https://learn.cylabacademy.org/library?search=Insp3ct0r)<br>🌐 **PortSwigger**: • [Lab: Intercepting Web Requests via Burp](https://portswigger.net/burp)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [what's a net cat? (ID: 156)](https://learn.cylabacademy.org/library?search=what%27s%20a%20net%20cat%3F)<br>• [Super SSH (ID: 424)](https://learn.cylabacademy.org/library?search=Super%20SSH)<br>🌐 **PortSwigger**: • [Lab: Modifying Web Requests](https://portswigger.net/burp/proxy) |
| **Day 2** | Burp Suite 代理截獲、Repeater 重放與 POST 欄位修改 | 📁 [`01_Web安全/02_HTTP協定與代理抓包`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/02_HTTP協定與代理抓包) <br>🎥 觀看抓包教學影片 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Insp3ct0r (ID: 367)](https://learn.cylabacademy.org/library?search=Insp3ct0r)<br>🌐 **PortSwigger**: • [Lab: Intercepting Web Requests via Burp](https://portswigger.net/burp)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [what's a net cat? (ID: 156)](https://learn.cylabacademy.org/library?search=what%27s%20a%20net%20cat%3F)<br>• [Super SSH (ID: 424)](https://learn.cylabacademy.org/library?search=Super%20SSH)<br>🌐 **PortSwigger**: • [Lab: Modifying Web Requests](https://portswigger.net/burp/proxy) |

---
#### ⚔️ **Run 2 (Day 3-4): SQL Injection 基礎與萬能密碼登入繞過**
📁 **本地對接**: [`01_Web安全/06_SQL注入漏洞專題/02_SQL注入基礎與GET_POST`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題/02_SQL注入基礎與GET_POST) ｜ 🌐 **線上專題**: [PortSwigger SQLi](https://portswigger.net/web-security/sql-injection)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 3** | SQL 查詢語法剖析、單引號 `'` 閉合原理與注入點判斷 | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Irish-Name-Repo 1 (ID: 548)](https://learn.cylabacademy.org/library?search=Irish-Name-Repo%201)<br>🌐 **PortSwigger**: • [Lab: Retrieval of hidden data](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Irish-Name-Repo 2 (ID: 550)](https://learn.cylabacademy.org/library?search=Irish-Name-Repo%202) & [Irish-Name-Repo 3 (ID: 552)](https://learn.cylabacademy.org/library?search=Irish-Name-Repo%203)<br>🌐 **PortSwigger**: • [Lab: Subverting login logic](https://portswigger.net/web-security/sql-injection/lab-login-bypass) |
| **Day 4** | `' OR 1=1--` 萬能密碼成因與 POST 表單登入繞過源碼分析 | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Irish-Name-Repo 1 (ID: 548)](https://learn.cylabacademy.org/library?search=Irish-Name-Repo%201)<br>🌐 **PortSwigger**: • [Lab: Retrieval of hidden data](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Irish-Name-Repo 2 (ID: 550)](https://learn.cylabacademy.org/library?search=Irish-Name-Repo%202) & [Irish-Name-Repo 3 (ID: 552)](https://learn.cylabacademy.org/library?search=Irish-Name-Repo%203)<br>🌐 **PortSwigger**: • [Lab: Subverting login logic](https://portswigger.net/web-security/sql-injection/lab-login-bypass) |

---
#### ⚔️ **Run 3 (Day 5-6): 命令執行 (RCE) 與路徑遍歷 (Path Traversal)**
📁 **本地對接**: [`01_Web安全/07_RCE命令與代碼執行`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/07_RCE命令與代碼執行) ｜ 🌐 **線上專題**: [PortSwigger OS Command Injection](https://portswigger.net/web-security/os-command-injection) ｜ [PortSwigger File Path Traversal](https://portswigger.net/web-security/file-path-traversal)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 5** | OS 命令注入原理與 Linux/Windows 命令拼接符 (` ; `, ` & `, ` && `, ` \| `, ` \|\| `) | 📁 [`01_Web安全/07_RCE命令與代碼執行`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/07_RCE命令與代碼執行) | [PortSwigger: Command Injection Simple](https://portswigger.net/web-security/os-command-injection/lab-simple)<br>💡 **帶練指引**: 講解 Linux 命令拼接符 `; & && \| \|\|` 差異並提供 RCE 測試腳本 |
| **Day 6** | 路徑遍歷 (Path Traversal) 與 `../` 讀取 `/etc/passwd` | 📁 [`01_Web安全/07_RCE命令與代碼執行`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/07_RCE命令與代碼執行) | [PortSwigger: Path Traversal Simple](https://portswigger.net/web-security/file-path-traversal/lab-simple)<br>💡 **帶練指引**: 講解 Linux 命令拼接符 `; & && \| \|\|` 差異並提供 RCE 測試腳本 |

---
#### ⚔️ **Run 4 (Day 7-8): Wireshark 網路流量分析與協定防禦**
📁 **本地對接**: [`06_網路安全與數位取證/01_網路協定分析與Scapy`](file:///f:/OutClass/資訊應用/網路安全/06_網路安全與數位取證/01_網路協定分析與Scapy) ｜ 🌐 **線上專題**: [Root-Me Network](https://www.root-me.org/en/Challenges/Network/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 7** | Wireshark 基礎界面、網路介面選擇與網卡混雜模式捕獲 | 📁 分析本地封包 [`SQLInjection.pcapng`](file:///f:/OutClass/資訊應用/網路安全/06_網路安全與數位取證/01_網路協定分析與Scapy/網路指令/SQLInjection.pcapng) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Wireshark doo dooo do doo... (ID: 432)](https://learn.cylabacademy.org/library?search=Wireshark%20doo%20dooo%20do%20doo...)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Trivial Flag Transfer Protocol (ID: 434)](https://learn.cylabacademy.org/library?search=Trivial%20Flag%20Transfer%20Protocol) |
| **Day 8** | Wireshark 顯示過濾語法 (`ip.addr`) 與 HTTP 追蹤流分析 | 📁 [`01_Web安全/02_HTTP協定與代理抓包`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/02_HTTP協定與代理抓包) <br>🎥 觀看抓包教學影片 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Wireshark doo dooo do doo... (ID: 432)](https://learn.cylabacademy.org/library?search=Wireshark%20doo%20dooo%20do%20doo...)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Trivial Flag Transfer Protocol (ID: 434)](https://learn.cylabacademy.org/library?search=Trivial%20Flag%20Transfer%20Protocol) |

---
#### ⚔️ **Run 5 (Day 9-10): 任意檔案上傳與 Webshell 木馬權維**
📁 **本地對接**: [`01_Web安全/08_檔案上傳與包含漏洞`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/08_檔案上傳與包含漏洞) ｜ 🌐 **線上專題**: [PortSwigger File Upload](https://portswigger.net/web-security/file-upload)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 9** | 任意檔案上傳原理、前端 JS 驗證繞過與 Content-Type 偽造 | 📁 [`01_Web安全/08_檔案上傳與包含漏洞`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/08_檔案上傳與包含漏洞) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Remote code execution via web shell upload](https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload) |
| **Day 10** | 一句話木馬編寫與中國蟻劍 (AntSword) 連接 Webshell | 📁 [`01_Web安全/08_檔案上傳與包含漏洞`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/08_檔案上傳與包含漏洞) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Remote code execution via web shell upload](https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload) |

---
#### ⚔️ **Run 6 (Day 11-12): x86/x64 彙編基礎與 GDB / Pwntools 環境建立**
📁 **本地對接**: [`02_二進制與逆向/01_x86_x64彙編語言基礎`](file:///f:/OutClass/資訊應用/網路安全/02_二進制與逆向/01_x86_x64彙編語言基礎) ｜ 🌐 **線上專題**: [pwn.college Dojo](https://pwn.college/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 11** | x86/x64 彙編暫存器 (EAX, ESP, EBP, EIP) 與記憶體堆疊結構 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Bit-O-Asm-1 (ID: 125)](https://learn.cylabacademy.org/library?search=Bit-O-Asm-1) ~ [Bit-O-Asm-4 (ID: 138)](https://learn.cylabacademy.org/library?search=Bit-O-Asm-4)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [GDB baby step 1 (ID: 142)](https://learn.cylabacademy.org/library?search=GDB%20baby%20step%201) ~ [GDB baby step 4 (ID: 158)](https://learn.cylabacademy.org/library?search=GDB%20baby%20step%204) |
| **Day 12** | Linux GDB 調試器指令 (`gdb ./pwn`) 與 Pwntools 腳本撰寫 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Bit-O-Asm-1 (ID: 125)](https://learn.cylabacademy.org/library?search=Bit-O-Asm-1) ~ [Bit-O-Asm-4 (ID: 138)](https://learn.cylabacademy.org/library?search=Bit-O-Asm-4)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [GDB baby step 1 (ID: 142)](https://learn.cylabacademy.org/library?search=GDB%20baby%20step%201) ~ [GDB baby step 4 (ID: 158)](https://learn.cylabacademy.org/library?search=GDB%20baby%20step%204) |

---
#### ⚔️ **Run 7 (Day 13-14): XSS 跨站腳本與 CSRF / SSRF 攻擊**
📁 **本地對接**: [`01_Web安全/10_客戶端與業務邏輯漏洞`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/10_客戶端與業務邏輯漏洞) ｜ 🌐 **線上專題**: [PortSwigger XSS](https://portswigger.net/web-security/cross-site-scripting) & [SSRF](https://portswigger.net/web-security/ssrf)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 13** | XSS 跨站腳本成因、Reflected XSS 與 DOM-based XSS 彈窗 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Reflected XSS into HTML context](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Stored XSS into anchor href](https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded)<br>• [Lab: CORS with basic origin reflection](https://portswigger.net/web-security) |
| **Day 14** | CSRF 跨站請求偽造 PoC HTML 產生與 SSRF 內網探測 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Reflected XSS into HTML context](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Stored XSS into anchor href](https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded)<br>• [Lab: CORS with basic origin reflection](https://portswigger.net/web-security) |

---
#### ⚔️ **Run 8 (Day 15-16): Ghidra / IDA Pro 靜態逆向工程基礎**
📁 **本地對接**: [`02_二進制與逆向/02_逆向工程工具_Ghidra_IDA_Pro`](file:///f:/OutClass/資訊應用/網路安全/02_二進制與逆向/02_逆向工程工具_Ghidra_IDA_Pro) ｜ 🌐 **線上專題**: [Root-Me Cracking](https://www.root-me.org/en/Challenges/Cracking/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 15** | 逆向工程導論、靜態分析概念與 PE / ELF 可執行檔結構 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Safe Opener 1 (ID: 513)](https://learn.cylabacademy.org/library?search=Safe%20Opener%201) & [Safe Opener 2 (ID: 515)](https://learn.cylabacademy.org/library?search=Safe%20Opener%202)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [vault-door-training (ID: 472)](https://learn.cylabacademy.org/library?search=vault-door-training) |
| **Day 16** | Ghidra / IDA Pro 反編譯 C 偽代碼與 Serial 驗證邏輯逆向 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Safe Opener 1 (ID: 513)](https://learn.cylabacademy.org/library?search=Safe%20Opener%201) & [Safe Opener 2 (ID: 515)](https://learn.cylabacademy.org/library?search=Safe%20Opener%202)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [vault-door-training (ID: 472)](https://learn.cylabacademy.org/library?search=vault-door-training) |

---
#### ⚔️ **Run 9 (Day 17-18): 越權漏洞 (IDOR) 與 Cookie/Session 會話劫持**
📁 **本地對接**: [`01_Web安全/10_客戶端與業務邏輯漏洞/04_越權與未授權存取`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/10_客戶端與業務邏輯漏洞/04_越權與未授權存取) ｜ 🌐 **線上專題**: [PortSwigger Access Control](https://portswigger.net/web-security/access-control)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 17** | IDOR 越權原理與平行越權修改 `id=1001` 檢視他人信件 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Unprotected admin functionality](https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: User ID controlled bypass of access controls](https://portswigger.net/web-security)<br>• [Lab: Username enumeration via different responses](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses) |
| **Day 18** | 垂直越權、URL 權限控制繞過與 Session 劫持攻擊 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Unprotected admin functionality](https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: User ID controlled bypass of access controls](https://portswigger.net/web-security)<br>• [Lab: Username enumeration via different responses](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses) |

---
#### ⚔️ **Run 10 (Day 19-20): Linux / Windows 本地權限提升 (PrivEsc)**
📁 **本地對接**: [`04_系統與內網安全/03_權限提升`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/03_權限提升) ｜ 🌐 **線上專題**: [OverTheWire Bandit](https://overthewire.org/wargames/bandit/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 19** | Linux SUID 提權原理與 `find / -perm -4000` 尋找特權 binary | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Magikarp Ground Mission (ID: 189)](https://learn.cylabacademy.org/library?search=Magikarp%20Ground%20Mission) / [First Find (ID: 320)](https://learn.cylabacademy.org/library?search=First%20Find)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Big Zip (ID: 322)](https://learn.cylabacademy.org/library?search=Big%20Zip) / [strings it (ID: 163)](https://learn.cylabacademy.org/library?search=strings%20it) / [plumbing (ID: 156)](https://learn.cylabacademy.org/library?search=plumbing) |
| **Day 20** | MySQL UDF 提權原理與 Windows 服務路徑弱點提權實戰 | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Magikarp Ground Mission (ID: 189)](https://learn.cylabacademy.org/library?search=Magikarp%20Ground%20Mission) / [First Find (ID: 320)](https://learn.cylabacademy.org/library?search=First%20Find)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Big Zip (ID: 322)](https://learn.cylabacademy.org/library?search=Big%20Zip) / [strings it (ID: 163)](https://learn.cylabacademy.org/library?search=strings%20it) / [plumbing (ID: 156)](https://learn.cylabacademy.org/library?search=plumbing) |

---
#### ⚔️ **Run 11 (Day 21-22): SSTI 模板注入與 PHP/Java 反序列化**
📁 **本地對接**: [`01_Web安全/11_反序列化與組件漏洞`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/11_反序列化與組件漏洞) ｜ 🌐 **線上專題**: [PortSwigger SSTI](https://portswigger.net/web-security/server-side-template-injection)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 21** | Flask Jinja2 SSTI 原理與 `{{config}}` / `__class__` 變數洩露 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Basic server-side template injection (ERB)](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Basic SSTI in Tornado](https://portswigger.net/web-security) |
| **Day 22** | PHP 魔術方法 `__wakeup()` 觸發與 Java 物件反序列化 | 📁 測試本地工具 [`Java反序列化终极测试工具.jar`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/11_反序列化與組件漏洞/03_Java反序列化漏洞/Java反序列化终极测试工具.jar) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Basic server-side template injection (ERB)](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Basic SSTI in Tornado](https://portswigger.net/web-security) |

---
#### ⚔️ **Run 12 (Day 23-24): PWN 堆疊溢出 (Stack Overflow) 緩衝區溢出**
📁 **本地對接**: [`02_二進制與逆向/03_PWN堆疊溢出與ROP鏈構造`](file:///f:/OutClass/資訊應用/網路安全/02_二進制與逆向/03_PWN堆疊溢出與ROP鏈構造) ｜ 🌐 **線上專題**: [pwnable.kr](http://pwnable.kr/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 23** | PWN 堆疊溢出 (Stack Overflow) 記憶體佈局與 NOP Sled 原理 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [buffer overflow 0 (ID: 184)](https://learn.cylabacademy.org/library?search=buffer%20overflow%200) / [Local Target (ID: 188)](https://learn.cylabacademy.org/library?search=Local%20Target)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [buffer overflow 1 (ID: 192)](https://learn.cylabacademy.org/library?search=buffer%20overflow%201) / [Picker I (ID: 118)](https://learn.cylabacademy.org/library?search=Picker%20I) ~ [Picker IV (ID: 180)](https://learn.cylabacademy.org/library?search=Picker%20IV) |
| **Day 24** | `ret2text` 篡改 EIP/RIP 執行流與 Pwntools 自動化 Exp 撰寫 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [buffer overflow 0 (ID: 184)](https://learn.cylabacademy.org/library?search=buffer%20overflow%200) / [Local Target (ID: 188)](https://learn.cylabacademy.org/library?search=Local%20Target)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [buffer overflow 1 (ID: 192)](https://learn.cylabacademy.org/library?search=buffer%20overflow%201) / [Picker I (ID: 118)](https://learn.cylabacademy.org/library?search=Picker%20I) ~ [Picker IV (ID: 180)](https://learn.cylabacademy.org/library?search=Picker%20IV) |

---
#### ⚔️ **Run 13 (Day 25-26): CryptoHack 密碼學基礎 (RSA / AES 算法原理)**
📁 **本地對接**: [`03_密碼學與隱寫/01_古典密碼與對稱加密_AES_DES`](file:///f:/OutClass/資訊應用/網路安全/03_密碼學與隱寫/01_古典密碼與對稱加密_AES_DES) ｜ 🌐 **線上專題**: [CryptoHack](https://cryptohack.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 25** | Base64、ASCII、XOR 位元運算與對稱加密基礎觀念 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [2warm (ID: 100)](https://learn.cylabacademy.org/library?search=2warm) / [Warmed Up (ID: 172)](https://learn.cylabacademy.org/library?search=Warmed%20Up) / [caesar (ID: 16)](https://learn.cylabacademy.org/library?search=caesar)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [interencdec (ID: 418)](https://learn.cylabacademy.org/library?search=interencdec)<br>• [Mind your Ps and Qs (ID: 27)](https://learn.cylabacademy.org/library?search=Mind%20your%20Ps%20and%20Qs) / [Mini RSA (ID: 18)](https://learn.cylabacademy.org/library?search=Mini%20RSA) / [rsa_oracle (ID: 29)](https://learn.cylabacademy.org/library?search=rsa_oracle) |
| **Day 26** | RSA 公私鑰數學原理 (p, q, n, e, d) 與大數分解陷阱 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [2warm (ID: 100)](https://learn.cylabacademy.org/library?search=2warm) / [Warmed Up (ID: 172)](https://learn.cylabacademy.org/library?search=Warmed%20Up) / [caesar (ID: 16)](https://learn.cylabacademy.org/library?search=caesar)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [interencdec (ID: 418)](https://learn.cylabacademy.org/library?search=interencdec)<br>• [Mind your Ps and Qs (ID: 27)](https://learn.cylabacademy.org/library?search=Mind%20your%20Ps%20and%20Qs) / [Mini RSA (ID: 18)](https://learn.cylabacademy.org/library?search=Mini%20RSA) / [rsa_oracle (ID: 29)](https://learn.cylabacademy.org/library?search=rsa_oracle) |

---
#### ⚔️ **Run 14 (Day 27-28): 內網滲透 (SOCKS5 隧道 / Pivoting / AD 域控攻防)**
📁 **本地對接**: [`04_系統與內網安全/06_內網滲透與SOCKS5隧道`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/06_內網滲透與SOCKS5隧道) ｜ 🌐 **線上專題**: [TryHackMe Active Directory](https://tryhackme.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 27** | MSF / Chisel 搭建 SOCKS5 代理隧道與 Pivoting 內網穿透 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 28** | Active Directory 域控基礎、Kerberos 驗證流程與黃金票據 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 15 (Day 29-30): Month 1 階段總複盤與黑盒 VulnHub 靶機通關**
📁 **本地對接**: [`01_Web安全/15_綜合靶場與VulnHub實戰演練`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/15_綜合靶場與VulnHub實戰演練) ｜ 🌐 **線上專題**: [VulnHub](https://www.vulnhub.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 29** | 黑盒 VulnHub 靶機 (Os-hackNos) 資訊收集與 Nmap 服務掃描 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 30** | 靶機漏洞組合利用、獲取 Root 權限與 Writeup 撰寫 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---

## 🗓️ Month 2 (第 31 ~ 60 天 / Run 16 ~ Run 30): 核心漏洞深造與高級攻防
#### ⚔️ **Run 16 (Day 31-32): SQL Injection 盲注與 OOB DNSLog 帶外注入**
📁 **本地對接**: [`01_Web安全/06_SQL注入漏洞專題/04_SQL盲注與OOB_DNSLog`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題/04_SQL盲注與OOB_DNSLog) ｜ 🌐 **線上專題**: [PortSwigger Blind SQLi](https://portswigger.net/web-security/sql-injection/blind)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 31** | 布林盲注與時間盲注 (`sleep(3)`, `ascii(substr())`) 原理與推算腳本 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Blind SQL injection with conditional responses](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Blind SQL injection with time delays](https://portswigger.net/web-security/sql-injection/blind/lab-time-delays)<br>• [Lab: Syntax injection in NoSQL](https://portswigger.net/web-security) |
| **Day 32** | DNSLog Out-of-band (OOB) 帶外注入與 `LOAD_FILE()` 數據外排 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Blind SQL injection with conditional responses](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Blind SQL injection with time delays](https://portswigger.net/web-security/sql-injection/blind/lab-time-delays)<br>• [Lab: Syntax injection in NoSQL](https://portswigger.net/web-security) |

---
#### ⚔️ **Run 17 (Day 33-34): SQL Injection WAF 繞過與拖庫實戰**
📁 **本地對接**: [`01_Web安全/06_SQL注入漏洞專題/07_SQL注入WAF繞過與拖庫`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題/07_SQL注入WAF繞過與拖庫) ｜ 🌐 **線上專題**: [PortSwigger SQLi Filter Bypass](https://portswigger.net/web-security/sql-injection)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 33** | 大小寫混淆、雙寫繞過與 `/*!50000union*/` 行內註釋繞過 WAF | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: SQL injection UNION attack, determining column count](https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: SQL injection UNION attack, retrieving data](https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text) |
| **Day 34** | `mysqldump` 資料庫備份與 MySQL UDF (`sys_eval`) 特權執行 | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: SQL injection UNION attack, determining column count](https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: SQL injection UNION attack, retrieving data](https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text) |

---
#### ⚔️ **Run 18 (Day 35-36): Sqlmap 工具高級參數與 Tamper 腳本編寫**
📁 **本地對接**: [`01_Web安全/06_SQL注入漏洞專題/06_Sqlmap自動化注入專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題/06_Sqlmap自動化注入專題) ｜ 🌐 **工具文件**: [Sqlmap Usage Documentation](https://github.com/sqlmapproject/sqlmap/wiki/Usage)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 35** | Sqlmap `-r req.txt`, `--level 5 --risk 3`, `--os-shell` 抓包拖庫參數 | 🎥 觀看 [`10.8MYSQLUDF提权与命令执行.mp4`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題/07_SQL注入WAF繞過與拖庫/10.8MYSQLUDF提权与命令执行.mp4) | 按專題課後練習進度 |
| **Day 36** | 自訂 Sqlmap `tamper` 混淆腳本編寫與安全狗 (Safedog) 繞過 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 19 (Day 37-38): 任意檔案上傳高級繞過與解析漏洞**
📁 **本地對接**: [`01_Web安全/08_檔案上傳與包含漏洞/02_檔案上傳繞過技巧`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/08_檔案上傳與包含漏洞/02_檔案上傳繞過技巧) ｜ 🌐 **線上專題**: [PortSwigger File Upload](https://portswigger.net/web-security/file-upload)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 37** | 雙重副檔名 (`.php.jpg`)、`0x00` 截斷與 `.htaccess` 繞過 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Web shell upload via Content-Type restriction bypass](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Web shell upload via path traversal](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal) |
| **Day 38** | Apache / Nginx 解析漏洞 (`/1.php/1.jpg`) 與 PUT 寫入木馬 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Web shell upload via Content-Type restriction bypass](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Web shell upload via path traversal](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal) |

---
#### ⚔️ **Run 20 (Day 39-40): LFI 本地檔案包含與 RFI 遠端檔案包含**
📁 **本地對接**: [`01_Web安全/08_檔案上傳與包含漏洞/04_LFI本地與遠端檔案包含`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/08_檔案上傳與包含漏洞/04_LFI本地與遠端檔案包含) ｜ 🌐 **線上專題**: [PortSwigger Path Traversal](https://portswigger.net/web-security/file-path-traversal)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 39** | LFI 配合 `php://filter` 讀取源碼與 `php://input` 執行木馬 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: File path traversal, traversal sequences blocked with absolute path](https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: File path traversal, traversal sequences stripped non-recursively](https://portswigger.net/web-security/file-path-traversal/lab-sequences-stripped-non-recursively) |
| **Day 40** | Session 檔案包含與 Log 日誌注入 (`/var/log/apache2/access.log`) GETSHELL | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: File path traversal, traversal sequences blocked with absolute path](https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: File path traversal, traversal sequences stripped non-recursively](https://portswigger.net/web-security/file-path-traversal/lab-sequences-stripped-non-recursively) |

---
#### ⚔️ **Run 21 (Day 41-42): DOM-based XSS 與 JS 加密解密逆向**
📁 **本地對接**: [`01_Web安全/10_客戶端與業務邏輯漏洞/01_XSS跨站腳本挖掘與攻擊`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/10_客戶端與業務邏輯漏洞/01_XSS跨站腳本挖掘與攻擊) ｜ 🌐 **線上專題**: [PortSwigger DOM XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 41** | DOM XSS Source & Sink (`location.search`, `document.write`) 剖析 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [vault-door-1 (ID: 474)](https://learn.cylabacademy.org/library?search=vault-door-1) ~ [vault-door-4 (ID: 480)](https://learn.cylabacademy.org/library?search=vault-door-4)<br>🌐 **PortSwigger**: • [Lab: DOM XSS using web message](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [vault-door-5 (ID: 481)](https://learn.cylabacademy.org/library?search=vault-door-5) ~ [vault-door-8 (ID: 487)](https://learn.cylabacademy.org/library?search=vault-door-8)<br>🌐 **PortSwigger**: • [Lab: Client-side prototype pollution via DOM XSS](https://portswigger.net/web-security) |
| **Day 42** | 前端 JS 混淆代碼逆向與 Chrome DevTools 中斷點調試解密 | 📁 解析本地 HTML [`exam.html`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/01_前端語言與語法/05_JS加密解密與前端解題/exam.html) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [vault-door-1 (ID: 474)](https://learn.cylabacademy.org/library?search=vault-door-1) ~ [vault-door-4 (ID: 480)](https://learn.cylabacademy.org/library?search=vault-door-4)<br>🌐 **PortSwigger**: • [Lab: DOM XSS using web message](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [vault-door-5 (ID: 481)](https://learn.cylabacademy.org/library?search=vault-door-5) ~ [vault-door-8 (ID: 487)](https://learn.cylabacademy.org/library?search=vault-door-8)<br>🌐 **PortSwigger**: • [Lab: Client-side prototype pollution via DOM XSS](https://portswigger.net/web-security) |

---
#### ⚔️ **Run 22 (Day 43-44): SSRF 高級利用與 127.0.0.1 內網探測**
📁 **本地對接**: [`01_Web安全/10_客戶端與業務邏輯漏洞/03_SSRF服務端請求偽造`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/10_客戶端與業務邏輯漏洞/03_SSRF服務端請求偽造) ｜ 🌐 **線上專題**: [PortSwigger SSRF](https://portswigger.net/web-security/ssrf)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 43** | SSRF 配合 `gopher://` 與 `dict://` 協定攻擊內網 Redis | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Basic SSRF against the local server](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Host header SSRF](https://portswigger.net/web-security/host-header/exploiting/lab-host-header-ssrf-via-flawed-request-parsing) |
| **Day 44** | SSRF 繞過 127.0.0.1 過濾 (DNS Rebinding, 十六進位 IP 表示) | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Basic SSRF against the local server](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Host header SSRF](https://portswigger.net/web-security/host-header/exploiting/lab-host-header-ssrf-via-flawed-request-parsing) |

---
#### ⚔️ **Run 23 (Day 45-46): 業務邏輯漏洞 (支付篡改、驗證碼繞過、JSON 劫持)**
📁 **本地對接**: [`01_Web安全/10_客戶端與業務邏輯漏洞/06_業務邏輯漏洞與JSON劫持`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/10_客戶端與業務邏輯漏洞/06_業務邏輯漏洞與JSON劫持) ｜ 🌐 **線上專題**: [PortSwigger Logic Flaws](https://portswigger.net/web-security/logic-flaws)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 45** | 支付金額篡改、負數下單與驗證碼可預測/未失效漏洞 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Excessive trust in client-side controls](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Limit overrun race condition](https://portswigger.net/web-security/race-conditions/lab-race-conditions-limit-overrun)<br>• [Lab: Authentication bypass via OAuth implicit flow](https://portswigger.net/web-security/oauth/lab-oauth-authentication-bypass-via-oauth-implicit-flow) |
| **Day 46** | JSONP 跨域數據劫持與 CORS 跨域資源共享配置缺陷利用 | 📁 解析本地 HTML [`exam.html`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/01_前端語言與語法/05_JS加密解密與前端解題/exam.html) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Excessive trust in client-side controls](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Limit overrun race condition](https://portswigger.net/web-security/race-conditions/lab-race-conditions-limit-overrun)<br>• [Lab: Authentication bypass via OAuth implicit flow](https://portswigger.net/web-security/oauth/lab-oauth-authentication-bypass-via-oauth-implicit-flow) |

---
#### ⚔️ **Run 24 (Day 47-48): Linux 權限提升進階 (Kernel Exploit, Dirty COW, Sudo)**
📁 **本地對接**: [`04_系統與內網安全/03_權限提升/Linux內核提權`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/03_權限提升/Linux內核提權) ｜ 🌐 **工具網址**: [GTFOBins](https://gtfobins.github.io/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 47** | Linux 內核溢出漏洞利用 (Dirty COW 臟牛, PTRACE_TRACEME) | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 48** | Sudo 權限配置漏洞 (`sudo -l`) 與 Linux Cron Jobs 定時任務提權 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 25 (Day 49-50): Windows 權限提升進階 (Bypass UAC, Token Impersonation)**
📁 **本地對接**: [`04_系統與內網安全/03_權限提升/Windows溢出提權`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/03_權限提升/Windows溢出提權) ｜ 🌐 **知識庫**: [PayloadsAllTheThings Windows PrivEsc](https://github.com/swisskyrepo/PayloadsAllTheThings)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 49** | Windows Server 2008R2 溢出提權與 LPK 劫持提權 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 50** | Token 冒充 (JuicyPotato, RoguePotato) 與 Zend 反彈 Shell | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 26 (Day 51-52): PHP 反序列化 POP 鏈與 PHPGGC 實戰**
📁 **本地對接**: [`01_Web安全/11_反序列化與組件漏洞`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/11_反序列化與組件漏洞) ｜ 🌐 **線上專題**: [PortSwigger Deserialization](https://portswigger.net/web-security/deserialization)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 51** | PHP POP 鏈 (Property-Oriented Programming) 魔術方法構造 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Modifying serialized objects](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Modifying serialized data types](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types) |
| **Day 52** | PHPGGC 自動化 Payload 生成器與 Phar 反序列化利用 | 📁 測試本地工具 [`Java反序列化终极测试工具.jar`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/11_反序列化與組件漏洞/03_Java反序列化漏洞/Java反序列化终极测试工具.jar) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Modifying serialized objects](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Modifying serialized data types](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types) |

---
#### ⚔️ **Run 27 (Day 53-54): Java 反序列化 (ysoserial, Shiro, Fastjson)**
📁 **本地對接**: [`01_Web安全/11_反序列化與組件漏洞/03_Java反序列化漏洞`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/11_反序列化與組件漏洞/03_Java反序列化漏洞) ｜ 🌐 **線上專題**: [PortSwigger Java Deserialization](https://portswigger.net/web-security/deserialization)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 53** | Java `readObject()` 漏洞成因、ysoserial 工具與 CC 鏈分析 | 📁 測試本地工具 [`Java反序列化终极测试工具.jar`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/11_反序列化與組件漏洞/03_Java反序列化漏洞/Java反序列化终极测试工具.jar) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Exploiting Java deserialization with Apache Commons](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-java-deserialization-with-apache-commons) |
| **Day 54** | Apache Shiro RememberMe 金鑰硬編碼與 Fastjson autoType 繞過 Exp | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Exploiting Java deserialization with Apache Commons](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-java-deserialization-with-apache-commons) |

---
#### ⚔️ **Run 28 (Day 55-56): 中間件與框架安全 (Apache, Nginx, Tomcat, Spring)**
📁 **本地對接**: [`01_Web安全/12_中間件與框架安全`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/12_中間件與框架安全) ｜ 🌐 **線上環境**: [Vulhub Open Source Vulnerability Repository](https://vulhub.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 55** | Tomcat 弱口令 Manager 部署 WAR 包 GetShell 與 CVE-2017-12615 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: JWT authentication bypass via unverified signature](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Web cache poisoning with unkeyed header](https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-header) |
| **Day 56** | Spring Core RCE (Spring4Shell) 與 ThinkPHP5 5.0.23 RCE 漏洞剖析 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: JWT authentication bypass via unverified signature](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Web cache poisoning with unkeyed header](https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-header) |

---
#### ⚔️ **Run 29 (Day 57-58): AWVS & Xray 自動化漏洞聯動掃描**
📁 **本地對接**: [`01_Web安全/13_漏洞自動化掃描`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/13_漏洞自動化掃描) ｜ 🌐 **工具說明**: [Xray Vulnerability Scanner Doc](https://xray.cool/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 57** | AWVS 14 漏洞自動化掃描器配置與黑盒主動掃描 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 58** | Burp Suite + Xray 被動式掃描器代理聯動挖掘 | 📁 [`01_Web安全/02_HTTP協定與代理抓包`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/02_HTTP協定與代理抓包) <br>🎥 觀看抓包教學影片 | 按專題課後練習進度 |

---
#### ⚔️ **Run 30 (Day 59-60): Month 2 階段復盤與黑盒 CMS 靶場實戰 (YXCMS / WordPress)**
📁 **本地對接**: [`01_Web安全/15_綜合靶場與VulnHub實戰演練/02_CMS實務靶場環境`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/15_綜合靶場與VulnHub實戰演練/02_CMS實務靶場環境) ｜ 🌐 **離線靶場**: 本地 CMS 離線靶場

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 59** | YXCMS 1.4.7 離線靶場部署與黑盒滲透測試 | 📁 解壓本地靶場 [`YXCMS.zip`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/15_綜合靶場與VulnHub實戰演練/02_CMS實務靶場環境/YXCMS.zip) | 按專題課後練習進度 |
| **Day 60** | WordPress 綜合檢測與 Month 2 階段 Writeup 總結 | 📁 解壓本地靶場 [`YXCMS.zip`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/15_綜合靶場與VulnHub實戰演練/02_CMS實務靶場環境/YXCMS.zip) | 按專題課後練習進度 |

---

## 🗓️ Month 3 (第 61 ~ 90 天 / Run 31 ~ Run 45): 二進制 PWN、逆向工程與紅隊內網滲透
#### ⚔️ **Run 31 (Day 61-62): Linux GDB 調試與 Pwntools 自動化控制**
📁 **本地對接**: [`02_二進制與逆向/03_PWN堆疊溢出與ROP鏈構造`](file:///f:/OutClass/資訊應用/網路安全/02_二進制與逆向/03_PWN堆疊溢出與ROP鏈構造) ｜ 🌐 **線上平台**: [pwnable.kr](http://pwnable.kr/) & [pwn.college](https://pwn.college/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 61** | Linux GDB 調試器高級指令 (`gdb ./pwn`, `x/20wx $esp`) 記憶體剖析 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Ready Gladiator 0 (ID: 577)](https://learn.cylabacademy.org/library?search=Ready%20Gladiator%200)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Ready Gladiator 1 (ID: 579)](https://learn.cylabacademy.org/library?search=Ready%20Gladiator%201) & [Ready Gladiator 2 (ID: 581)](https://learn.cylabacademy.org/library?search=Ready%20Gladiator%202) |
| **Day 62** | Pwntools Python 庫 (`process()`, `remote()`) 自動化 Exp 腳本撰寫 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Ready Gladiator 0 (ID: 577)](https://learn.cylabacademy.org/library?search=Ready%20Gladiator%200)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Ready Gladiator 1 (ID: 579)](https://learn.cylabacademy.org/library?search=Ready%20Gladiator%201) & [Ready Gladiator 2 (ID: 581)](https://learn.cylabacademy.org/library?search=Ready%20Gladiator%202) |

---
#### ⚔️ **Run 32 (Day 63-64): PWN ROP 鏈 (Return-Oriented Programming) 實戰**
📁 **本地對接**: [`02_二進制與逆向/03_PWN堆疊溢出與ROP鏈構造`](file:///f:/OutClass/資訊應用/網路安全/02_二進制與逆向/03_PWN堆疊溢出與ROP鏈構造) ｜ 🌐 **線上平台**: [Root-Me Cracking](https://www.root-me.org/en/Challenges/Cracking/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 63** | Linux NX 記憶體保護與 ROPgadget 搜尋 `pop rdi; ret` Gadget | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Guessing Game 1 (ID: 568)](https://learn.cylabacademy.org/library?search=Guessing%20Game%201)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Guessing Game 2 (ID: 570)](https://learn.cylabacademy.org/library?search=Guessing%20Game%202) |
| **Day 64** | 64 位元 ROP 鏈構造與 `ret2libc` 洩露 libc 位址 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Guessing Game 1 (ID: 568)](https://learn.cylabacademy.org/library?search=Guessing%20Game%201)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Guessing Game 2 (ID: 570)](https://learn.cylabacademy.org/library?search=Guessing%20Game%202) |

---
#### ⚔️ **Run 33 (Day 65-66): PWN 格式化字串漏洞與任意記憶體讀寫**
📁 **本地對接**: [`02_二進制與逆向/03_PWN堆疊溢出與ROP鏈構造`](file:///f:/OutClass/資訊應用/網路安全/02_二進制與逆向/03_PWN堆疊溢出與ROP鏈構造) ｜ 🌐 **線上平台**: [Root-Me Cracking](https://www.root-me.org/en/Challenges/Cracking/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 65** | 格式化字串漏洞 (`printf`) 記憶體洩露原理 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 66** | 利用 `%n` 任意寫入與 GOT 表改寫 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 34 (Day 67-68): Ghidra / IDA Pro 逆向工程與 C/C++ 反編譯分析**
📁 **本地對接**: [`02_二進制與逆向/02_逆向工程工具_Ghidra_IDA_Pro`](file:///f:/OutClass/資訊應用/網路安全/02_二進制與逆向/02_逆向工程工具_Ghidra_IDA_Pro) ｜ 🌐 **線上平台**: [Root-Me Reversing](https://www.root-me.org/en/Challenges/Cracking/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 67** | Ghidra 靜態分析 C/C++ 結構體與指針排列微觀剖析 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Investigative Reversing 0 (ID: 524)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%200) ~ [Investigative Reversing 2 (ID: 528)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%202)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Investigative Reversing 3 (ID: 530)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%203) & [Investigative Reversing 4 (ID: 532)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%204) |
| **Day 68** | 控制流圖 (CFG) 導覽與 Binary Patch 修改跳過註冊驗證 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Investigative Reversing 0 (ID: 524)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%200) ~ [Investigative Reversing 2 (ID: 528)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%202)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Investigative Reversing 3 (ID: 530)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%203) & [Investigative Reversing 4 (ID: 532)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%204) |

---
#### ⚔️ **Run 35 (Day 69-70): Android APK 逆向與 Smali 代碼動態調試**
📁 **本地對接**: [`02_二進制與逆向/04_Android_APK逆向與Smali分析`](file:///f:/OutClass/資訊應用/網路安全/02_二進制與逆向/04_Android_APK逆向與Smali分析) ｜ 🌐 **線上平台**: [Root-Me Android Challenges](https://www.root-me.org/en/Challenges/Cracking/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 69** | Android APK 結構解析、`apktool` 解包與 Smali 閱讀 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [droids0 (ID: 588)](https://learn.cylabacademy.org/library?search=droids0) / [droids1 (ID: 590)](https://learn.cylabacademy.org/library?search=droids1) / [droids2 (ID: 592)](https://learn.cylabacademy.org/library?search=droids2)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [droids3 (ID: 594)](https://learn.cylabacademy.org/library?search=droids3) / [droids4 (ID: 596)](https://learn.cylabacademy.org/library?search=droids4) |
| **Day 70** | JADX-GUI 動態調試 Android APK 與 驗證邏輯 Patch | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [droids0 (ID: 588)](https://learn.cylabacademy.org/library?search=droids0) / [droids1 (ID: 590)](https://learn.cylabacademy.org/library?search=droids1) / [droids2 (ID: 592)](https://learn.cylabacademy.org/library?search=droids2)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [droids3 (ID: 594)](https://learn.cylabacademy.org/library?search=droids3) / [droids4 (ID: 596)](https://learn.cylabacademy.org/library?search=droids4) |

---
#### ⚔️ **Run 36 (Day 71-72): 內網資產探測 (Nmap, Masscan, fscan)**
📁 **本地對接**: [`04_系統與內網安全/06_內網滲透與SOCKS5隧道`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/06_內網滲透與SOCKS5隧道) ｜ 🌐 **官方文檔**: [Nmap Documentation](https://nmap.org/book/man.html)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 71** | Nmap 內網 C 段主機存活探測 (`nmap -sn`) 與服務識別 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 72** | fscan 自動化內網掃描與弱口令爆破 (SSH, RDP, MySQL) | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 按專題課後練習進度 |

---
#### ⚔️ **Run 37 (Day 73-74): 橫向移動 (Pass-the-Hash, WMI, PsExec)**
📁 **本地對接**: [`04_系統與內網安全/06_內網滲透與SOCKS5隧道`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/06_內網滲透與SOCKS5隧道) ｜ 🌐 **工具庫**: [Impacket Tools](https://github.com/fortra/impacket)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 73** | Pass-the-Hash (哈希傳遞) 攻擊與 Mimikatz 抓取 NTLM Hash | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 74** | 利用 WMI (`wmiexec.py`) 與 PsExec 實現無文件橫向執行 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 38 (Day 75-76): Cobalt Strike C2 部署與 Listener / Stager 控權**
📁 **本地對接**: [`04_系統與內網安全/08_C2與控權`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/08_C2與控權) ｜ 🌐 **參考手冊**: [Cobalt Strike User Guide](https://hacksysteam.github.io/CobaltStrike-Manual/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 75** | Cobalt Strike Teamserver 搭建與 Client 連線 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 76** | CS Listener 設定、生成 Beacon Stager 與權限維持 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 39 (Day 77-78): Active Directory 域控攻擊 (Kerberoasting, AS-REP Roasting)**
📁 **本地對接**: [`04_系統與內網安全/06_內網滲透與SOCKS5隧道`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/06_內網滲透與SOCKS5隧道) ｜ 🌐 **線上靶場**: [TryHackMe Attacktive Directory](https://tryhackme.com/room/attacktivedirectory)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 77** | Active Directory 域控架構與 Kerberos 認證流程 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 78** | Kerberoasting 攻擊與 AS-REP Roasting 離線爆破 Hash | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 40 (Day 79-80): Golden Ticket & Silver Ticket 域控接管**
📁 **本地對接**: [`04_系統與內網安全/06_內網滲透與SOCKS5隧道`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/06_內網滲透與SOCKS5隧道) ｜ 🌐 **知識庫**: [PayloadsAllTheThings AD](https://github.com/swisskyrepo/PayloadsAllTheThings)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 79** | Golden Ticket (黃金票據) 偽造與 `krbtgt` Hash 控制域控 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 80** | Silver Ticket (白銀票據) 偽造與 MSSQL / CIFS 服務切入 | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 按專題課後練習進度 |

---
#### ⚔️ **Run 41 (Day 81-82): 免殺與 Shellcode 載入器 (Bypass AV)**
📁 **本地對接**: [`04_系統與內網安全/08_C2與控權/紅隊軟體免殺技術`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/08_C2與控權/紅隊軟體免殺技術) ｜ 🌐 **知識庫**: [Bypass AV Loader](https://github.com/swisskyrepo/PayloadsAllTheThings)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 81** | 免殺技術：Shellcode Loader 異或 / AES 特徵加密解密 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 82** | 利用 Windows API (`VirtualAlloc`, `RtlMoveMemory`) 繞過記憶體掃描 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 42 (Day 83-84): Linux / Windows 權限維持與後門 (Persistence)**
📁 **本地對接**: [`04_系統與內網安全/08_C2與控權/後門`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/08_C2與控權/後門) ｜ 🌐 **MITRE ATT&CK**: [Persistence Tactics](https://attack.mitre.org/tactics/TA0003/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 83** | Linux 權限維持：SSH 公鑰寫入、Crontab 定時任務與 SUID 後門 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 84** | Windows 權限維持：機碼自啟動、排程工作與服務後門 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 43 (Day 85-86): Metasploit (MSF) 高級模組與 Exp 開發**
📁 **本地對接**: [`04_系統與內網安全/01_Metasploit框架與Exp實戰`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/01_Metasploit框架與Exp實戰) ｜ 🌐 **官方教學**: [Metasploit Unleashed Docs](https://www.offsec.com/metasploit-unleashed/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 85** | MSF `msfvenom` 生成 Payload 與 Handler 監聽設定 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 86** | MSF 自訂 Ruby 漏洞利用模組 (Exp) 寫作規範與 API 對接 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 44 (Day 87-88): 內網縱深防禦與痕跡清理**
📁 **本地對接**: [`04_系統與內網安全/06_內網滲透與SOCKS5隧道`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/06_內網滲透與SOCKS5隧道) ｜ 🌐 **MITRE ATT&CK**: [Defense Evasion](https://attack.mitre.org/tactics/TA0005/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 87** | 攻擊痕跡清理：Linux 命令歷史 (`history -c`) 與 Windows 事件日誌 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 88** | 內網網路隔離 (VLAN, ACL, Zero Trust) 策略評估與紅隊復盤 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 45 (Day 89-90): Month 3 階段總復盤與內網 AD 域控攻防靶場通關**
📁 **本地對接**: [`04_系統與內網安全`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全) ｜ 🌐 **線上靶場**: [TryHackMe Wreath Network](https://tryhackme.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 89** | 內網 AD 靶場：Web 入口點突破 ➔ SOCKS5 代理穿透進入內網 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 90** | 橫向移動至域控 (DC) 獲取 Domain Admin 與 Writeup 撰寫 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---

## 🗓️ Month 4 (第 91 ~ 120 天 / Run 46 ~ Run 60): 代碼審計、安全開發與藍隊防禦
#### ⚔️ **Run 46 (Day 91-92): PHP 代碼審計 (危險函數追蹤 ＋ AST/CFG 語意分析 ＋ Source-to-Sink 污點追蹤)**
📁 **本地對接**: [`05_代碼審計與安全開發/01_PHP代碼審計基礎`](file:///f:/OutClass/資訊應用/網路安全/05_代碼審計與安全開發/01_PHP代碼審計基礎) ｜ 🌐 **OWASP 參考**: [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 91** | PHP 代碼審計基礎：危險函數 (`eval`, `exec`) 定位與 Seay 工具 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [PortSwigger Code Audit Walkthroughs](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [AST/CFG Code Semantics Analysis](https://portswigger.net/web-security) |
| **Day 92** | PHP 變數追蹤法 (Sinks to Sources) 與 SQLi / XSS 白箱發現 | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [PortSwigger Code Audit Walkthroughs](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [AST/CFG Code Semantics Analysis](https://portswigger.net/web-security) |

---
#### ⚔️ **Run 47 (Day 93-94): Java 代碼審計 (Spring/Servlet 審計 ＋ 語意分析 ＋ 資料流分析 Data-flow Analysis)**
📁 **本地對接**: [`05_代碼審計與安全開發/02_Java代碼審計基礎`](file:///f:/OutClass/資訊應用/網路安全/05_代碼審計與安全開發/02_Java代碼審計基礎) ｜ 🌐 **OWASP 參考**: [OWASP Source Code Analysis](https://owasp.org/www-community/Source_Code_Analysis_Tools)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 93** | Java Web 架構 (Filter, Servlet, Spring MVC) 與 Controller 入口 | 📁 測試本地工具 [`Java反序列化终极测试工具.jar`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/11_反序列化與組件漏洞/03_Java反序列化漏洞/Java反序列化终极测试工具.jar) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [PortSwigger Java Vulnerability Analysis](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Source-to-Sink Data-flow Taint Analysis](https://portswigger.net/web-security) |
| **Day 94** | Java SQL 拼接 (MyBatis `${}` vs `#{}`) 與 `Runtime.exec()` RCE | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [PortSwigger Java Vulnerability Analysis](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Source-to-Sink Data-flow Taint Analysis](https://portswigger.net/web-security) |

---
#### ⚔️ **Run 48 (Day 95-96): 開源 CMS 代碼審計項目實戰 (YXCMS 白箱審計 ＋ 複雜資料流與淨化函數過濾驗證)**
📁 **本地對接**: [`05_代碼審計與安全開發/03_審計項目實戰`](file:///f:/OutClass/資訊應用/網路安全/05_代碼審計與安全開發/03_審計項目實戰) ｜ 🌐 **離線代碼**: 本地 YXCMS 開源專案

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 95** | YXCMS 1.4.7 解包、路由解析與 SQL 查詢構造器白箱分析 | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 按專題課後練習進度 |
| **Day 96** | YXCMS 前台 SQL 注入與後台寫入 GetShell 驗證與 0day 挖掘 | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 按專題課後練習進度 |

---
#### ⚔️ **Run 49 (Day 97-98): Python 安全開發 (自動化掃描工具開發)**
📁 **本地對接**: [`05_代碼審計與安全開發/04_Python安全工具開發`](file:///f:/OutClass/資訊應用/網路安全/05_代碼審計與安全開發/04_Python安全工具開發) ｜ 🌐 **官方文檔**: [Python Requests Docs](https://requests.readthedocs.io/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 97** | Python Requests 模組：Session 維持、代理設定與自訂 Header | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [PW Crack 1 (ID: 245)](https://learn.cylabacademy.org/library?search=PW%20Crack%201) ~ [PW Crack 3 (ID: 247)](https://learn.cylabacademy.org/library?search=PW%20Crack%203)<br>• [fixme1.py (ID: 240)](https://learn.cylabacademy.org/library?search=fixme1.py)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [PW Crack 4 (ID: 248)](https://learn.cylabacademy.org/library?search=PW%20Crack%204) & [PW Crack 5 (ID: 611)](https://learn.cylabacademy.org/library?search=PW%20Crack%205)<br>• [fixme2.py (ID: 241)](https://learn.cylabacademy.org/library?search=fixme2.py) |
| **Day 98** | Python `threading` 多執行緒目錄 Fuzz 與漏洞掃描器編寫 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [PW Crack 1 (ID: 245)](https://learn.cylabacademy.org/library?search=PW%20Crack%201) ~ [PW Crack 3 (ID: 247)](https://learn.cylabacademy.org/library?search=PW%20Crack%203)<br>• [fixme1.py (ID: 240)](https://learn.cylabacademy.org/library?search=fixme1.py)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [PW Crack 4 (ID: 248)](https://learn.cylabacademy.org/library?search=PW%20Crack%204) & [PW Crack 5 (ID: 611)](https://learn.cylabacademy.org/library?search=PW%20Crack%205)<br>• [fixme2.py (ID: 241)](https://learn.cylabacademy.org/library?search=fixme2.py) |

---
#### ⚔️ **Run 50 (Day 99-100): 藍隊防禦與護網日誌分析 (Web 攻擊日誌 ＋ 統計特徵選擇 Statistical Feature Selection)**
📁 **本地對接**: [`07_藍隊防禦與護網營運/01_護網專案營運`](file:///f:/OutClass/資訊應用/網路安全/07_藍隊防禦與護網營運/01_護網專案營運) ｜ 🌐 **OWASP 參考**: [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 99** | Apache / Nginx Access Log 剖析與 Web 攻擊特徵日誌搜尋 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 100** | 利用 Linux `grep`, `awk`, `uniq -c` 極速統計可疑 IP 紀錄 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 51 (Day 101-102): SIEM 與 ELK 集中日誌過濾 (巨量日誌過濾 ＋ CatBoost 機器學習流量分類)**
📁 **本地對接**: [`07_藍隊防禦與護網營運/02_藍隊日誌分析`](file:///f:/OutClass/資訊應用/網路安全/07_藍隊防禦與護網營運/02_藍隊日誌分析) ｜ 🌐 **官方文檔**: [Elastic Kibana KQL Guide](https://www.elastic.co/guide/en/kibana/current/kuery-query.html)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 101** | SIEM 概念與 ELK (Elasticsearch, Logstash, Kibana) 集中日誌 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 102** | 撰寫 Kibana KQL 告警查詢語法與 Web 爆破實時告警 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 52 (Day 103-104): Sysmon 與 Windows 日誌分析 (特徵工程 ＋ SHAP 可解釋性分析依賴圖視覺化)**
📁 **本地對接**: [`07_藍隊防禦與護網營運/02_藍隊日誌分析`](file:///f:/OutClass/資訊應用/網路安全/07_藍隊防禦與護網營運/02_藍隊日誌分析) ｜ 🌐 **官方文檔**: [Sysinternals Sysmon Docs](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 103** | Windows 事件檢視器關鍵 Event ID (4624, 4625, 4672) 判讀 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 104** | Sysmon 配置檔編寫、進程創建與網路連線告警捕捉 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 53 (Day 105-106): 記憶體取證 (Volatility 分析 Dump 檔案)**
📁 **本地對接**: [`06_網路安全與數位取證/03_記憶體取證與Volatility`](file:///f:/OutClass/資訊應用/網路安全/06_網路安全與數位取證/03_記憶體取證與Volatility) ｜ 🌐 **線上平台**: [Root-Me Memory Forensics](https://www.root-me.org/en/Challenges/Forensic/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 105** | 記憶體取證導論、Volatility 2.6/3 安裝與 Profile 選取 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Sleuthkit Intro (ID: 504)](https://learn.cylabacademy.org/library?search=Sleuthkit%20Intro) / [information (ID: 89)](https://learn.cylabacademy.org/library?search=information) / [Verify (ID: 54)](https://learn.cylabacademy.org/library?search=Verify)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Sleuthkit Apprentice (ID: 506)](https://learn.cylabacademy.org/library?search=Sleuthkit%20Apprentice)<br>• [Disk, disk, sleuth! (ID: 416)](https://learn.cylabacademy.org/library?search=Disk%2C%20disk%2C%20sleuth%21) & [Disk, disk, sleuth! II (ID: 418)](https://learn.cylabacademy.org/library?search=Disk%2C%20disk%2C%20sleuth%21%20II)<br>• [Glory of the Garden (ID: 409)](https://learn.cylabacademy.org/library?search=Glory%20of%20the%20Garden) / [Scan Surprise (ID: 444)](https://learn.cylabacademy.org/library?search=Scan%20Surprise) |
| **Day 106** | Volatility 實戰：`pslist`, `netscan`, `dumpfiles` 還原木馬 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Sleuthkit Intro (ID: 504)](https://learn.cylabacademy.org/library?search=Sleuthkit%20Intro) / [information (ID: 89)](https://learn.cylabacademy.org/library?search=information) / [Verify (ID: 54)](https://learn.cylabacademy.org/library?search=Verify)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Sleuthkit Apprentice (ID: 506)](https://learn.cylabacademy.org/library?search=Sleuthkit%20Apprentice)<br>• [Disk, disk, sleuth! (ID: 416)](https://learn.cylabacademy.org/library?search=Disk%2C%20disk%2C%20sleuth%21) & [Disk, disk, sleuth! II (ID: 418)](https://learn.cylabacademy.org/library?search=Disk%2C%20disk%2C%20sleuth%21%20II)<br>• [Glory of the Garden (ID: 409)](https://learn.cylabacademy.org/library?search=Glory%20of%20the%20Garden) / [Scan Surprise (ID: 444)](https://learn.cylabacademy.org/library?search=Scan%20Surprise) |

---
#### ⚔️ **Run 54 (Day 107-108): 勒索軟體與木馬應變處置 (IR Incident Response)**
📁 **本地對接**: [`06_網路安全與數位取證/04_數位取證與應變處置`](file:///f:/OutClass/資訊應用/網路安全/06_網路安全與數位取證/04_數位取證與應變處置) ｜ 🌐 **CISA 指南**: [CISA Incident Handling Guide](https://www.cisa.gov/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 107** | 藍隊資安事件應變處置 (IR) 標準流程 (準備 ➔ 檢測 ➔ 根除) | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 108** | 惡意進程與後門排查工具 (Process Hacker, TCPView, Autoruns) | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 55 (Day 109-110): 密碼學進階 (ECC, Diffie-Hellman, SHA-256)**
📁 **本地對接**: [`03_密碼學與隱寫/01_古典密碼與對稱加密_AES_DES`](file:///f:/OutClass/資訊應用/網路安全/03_密碼學與隱寫/01_古典密碼與對稱加密_AES_DES) ｜ 🌐 **線上平台**: [CryptoHack Advanced Cryptography](https://cryptohack.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 109** | ECC 橢圓曲線加密與 Diffie-Hellman 金鑰交換數學原理 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [PowerAnalysis: Warmup (ID: 36)](https://learn.cylabacademy.org/library?search=PowerAnalysis%3A%20Warmup)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [PowerAnalysis: Part 1 (ID: 38)](https://learn.cylabacademy.org/library?search=PowerAnalysis%3A%20Part%201)<br>• [corrupt-key-2 (ID: 287)](https://learn.cylabacademy.org/library?search=corrupt-key-2) |
| **Day 110** | SHA-256 / MD5 哈希長度擴展攻擊與 HashPump 工具實操 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [PowerAnalysis: Warmup (ID: 36)](https://learn.cylabacademy.org/library?search=PowerAnalysis%3A%20Warmup)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [PowerAnalysis: Part 1 (ID: 38)](https://learn.cylabacademy.org/library?search=PowerAnalysis%3A%20Part%201)<br>• [corrupt-key-2 (ID: 287)](https://learn.cylabacademy.org/library?search=corrupt-key-2) |

---
#### ⚔️ **Run 56 (Day 111-112): 隱寫術 (Steganography: Stegsolve, OutGuess)**
📁 **本地對接**: [`03_密碼學與隱寫/02_隱寫術與圖片音訊分析`](file:///f:/OutClass/資訊應用/網路安全/03_密碼學與隱寫/02_隱寫術與圖片音訊分析) ｜ 🌐 **線上平台**: [Root-Me Steganography](https://www.root-me.org/en/Challenges/Steganography/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 111** | 隱寫術導論、Stegsolve 工具使用、圖片 LSB 最低有效位提取 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [St3g0 (ID: 425)](https://learn.cylabacademy.org/library?search=St3g0) / [What Lies Within (ID: 427)](https://learn.cylabacademy.org/library?search=What%20Lies%20Within)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [m00nwalk (ID: 539)](https://learn.cylabacademy.org/library?search=m00nwalk) & [m00nwalk2 (ID: 541)](https://learn.cylabacademy.org/library?search=m00nwalk2) / [investigation_encoded_1 (ID: 559)](https://learn.cylabacademy.org/library?search=investigation_encoded_1) |
| **Day 112** | 音訊隱寫 (Audacity 頻譜圖) 與 OutGuess / Steghide 密碼破解 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [St3g0 (ID: 425)](https://learn.cylabacademy.org/library?search=St3g0) / [What Lies Within (ID: 427)](https://learn.cylabacademy.org/library?search=What%20Lies%20Within)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [m00nwalk (ID: 539)](https://learn.cylabacademy.org/library?search=m00nwalk) & [m00nwalk2 (ID: 541)](https://learn.cylabacademy.org/library?search=m00nwalk2) / [investigation_encoded_1 (ID: 559)](https://learn.cylabacademy.org/library?search=investigation_encoded_1) |

---
#### ⚔️ **Run 57 (Day 113-114): 網頁安全防禦加固與 WAF 規則撰寫**
📁 **本地對接**: [`07_藍隊防禦與護網營運`](file:///f:/OutClass/資訊應用/網路安全/07_藍隊防禦與護網營運) ｜ 🌐 **官方項目**: [OWASP ModSecurity Core Rule Set](https://coreruleset.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 113** | ModSecurity WAF 安裝配置與 OWASP CRS 部署調校 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Obfuscating WAF bypass techniques](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-most-tags-and-attributes-blocked) |
| **Day 114** | 撰寫自訂 SecRule 規則防禦 SQLi, XSS 與 RCE 命令執行 | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Obfuscating WAF bypass techniques](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-most-tags-and-attributes-blocked) |

---
#### ⚔️ **Run 58 (Day 115-116): 資安筆試題庫解析 (觀念題/協議題/防禦題)**
📁 **本地對接**: [`08_通用學習與面試庫/02_資安筆試題庫與題解`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫/02_資安筆試題庫與題解) ｜ 🌐 **OWASP 參考**: [OWASP Top 10 Security Risks](https://owasp.org/www-project-top-ten/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 115** | TCP/IP 三向交握、TLS 1.3 握手流程、HTTP 狀態碼筆試題 | 📁 [`01_Web安全/02_HTTP協定與代理抓包`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/02_HTTP協定與代理抓包) <br>🎥 觀看抓包教學影片 | 按專題課後練習進度 |
| **Day 116** | 同源策略 (SOP)、CORS、Cookie 屬性 (`SameSite`) 筆試真題 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 59 (Day 117-118): 資安面試真題與履歷包裝**
📁 **本地對接**: [`08_通用學習與面試庫/03_資安面試真題與履歷技巧`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫/03_資安面試真題與履歷技巧) ｜ 🌐 **面試指南**: [Cybersecurity Interview Prep](https://github.com/swisskyrepo/PayloadsAllTheThings)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 117** | 滲透測試項目經歷 STAR 原則描述與漏洞復盤表達 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 118** | 資安工程師履歷包裝、GitHub 專案展示與 HR 常見問答 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 60 (Day 119-120): Month 4 階段總復盤與藍隊防禦報告產出**
📁 **本地對接**: [`07_藍隊防禦與護網營運`](file:///f:/OutClass/資訊應用/網路安全/07_藍隊防禦與護網營運) ｜ 🌐 **OWASP 參考**: [OWASP Defensive Security](https://owasp.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 119** | 從代碼審計 ➔ 部署 WAF SecRule 擋截 ➔ SIEM 日誌告警 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 120** | 產出藍隊防禦加固報告、代碼修補建議書與 Writeup 總結 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---

## 🗓️ Month 5 (第 121 ~ 150 天 / Run 61 ~ Run 75): 企業級紅隊綜合攻防與 AWD 對抗演練
#### ⚔️ **Run 61 (Day 121-122): DMZ 邊界突破與 Web 權限獲取**
📁 **本地對接**: [`04_系統與內網安全/06_內網滲透與SOCKS5隧道`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/06_內網滲透與SOCKS5隧道) ｜ 🌐 **線上實戰**: [TryHackMe Enterprise Network](https://tryhackme.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 121** | DMZ 邊界網路探測、Nmap 服務指紋識別與入口點掃描 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 122** | Web 漏洞組合利用 (SQLi/Upload) 獲取 DMZ Web 殼權限 | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 按專題課後練習進度 |

---
#### ⚔️ **Run 62 (Day 123-124): SOCKS5 代理與二階內網 Pivoting 穿透**
📁 **本地對接**: [`04_系統與內網安全/06_內網滲透與SOCKS5隧道`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/06_內網滲透與SOCKS5隧道) ｜ 🌐 **線上實戰**: [TryHackMe Pivoting](https://tryhackme.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 123** | Chisel / MSF 搭建 SOCKS5 代理與二階內網隧道穿透 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 124** | 內網 C 段主機存活探測、fscan 自動化掃描與服務爆破 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 63 (Day 125-126): 內網橫向移動與記憶體 Hash 抓取**
📁 **本地對接**: [`04_系統與內網安全/06_內網滲透與SOCKS5隧道`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/06_內網滲透與SOCKS5隧道) ｜ 🌐 **工具庫**: [Impacket Tools](https://github.com/fortra/impacket)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 125** | Pass-the-Hash (哈希傳遞) 橫向移動至內網成員伺服器 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 126** | Mimikatz 抓取內網記憶體 NTLM Hash 與 LSA Secrets 洩露 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 64 (Day 127-128): Kerberoasting 與 Golden Ticket 域控接管**
📁 **本地對接**: [`04_系統與內網安全/06_內網滲透與SOCKS5隧道`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/06_內網滲透與SOCKS5隧道) ｜ 🌐 **線上實戰**: [TryHackMe Attacktive Directory](https://tryhackme.com/room/attacktivedirectory)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 127** | Kerberoasting 攻擊與 SPN 服務帳號離線 Hash 爆破 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 128** | 偽造 Golden Ticket (黃金票據) 完全接管 AD 域控制器 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 65 (Day 129-130): 企業紅隊攻擊拓撲與評估報告產出**
📁 **本地對接**: [`04_系統與內網安全`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全) ｜ 🌐 **報告範本**: [Cybersecurity Red Team Report Guide](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 129** | 企業紅隊攻防成果整理、戰果日誌與攻擊路徑拓撲圖繪製 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 130** | 產出企業級紅隊滲透測試與資產風險評估報告 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 66 (Day 131-132): AWD 賽事初始化、源碼修補與 WAF 部署**
📁 **本地對接**: [`08_通用學習與面試庫/01_CTF競賽Writeup與題解`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫/01_CTF競賽Writeup與題解) ｜ 🌐 **開源平台**: [AWD-Predator Platform](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 131** | AWD 戰前準備：SSH 密碼修改、GameBox 源碼備份與權限檢查 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 132** | Web 源碼漏洞修補：SQL 注入與 RCE 危險函數快速過濾 | 📁 [`01_Web安全/06_SQL注入漏洞專題`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/06_SQL注入漏洞專題) <br>🎥 觀看 SQL 注入基礎影片 | 按專題課後練習進度 |

---
#### ⚔️ **Run 67 (Day 133-134): AWD 流量 WAF 部署與對手 Exp 分析**
📁 **本地對接**: [`08_通用學習與面試庫/01_CTF競賽Writeup與題解`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫/01_CTF競賽Writeup與題解) ｜ 🌐 **開源平台**: [AWD Defense WAF](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 133** | 部署 AWD 流量監控被動式 WAF 腳本與全網抓包日誌記錄 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 134** | 分析對手攻擊流量標頭、還原對手漏洞利用二進制 Payload | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 68 (Day 135-136): AWD 自動化 Batch 批量提交 Flag 腳本**
📁 **本地對接**: [`08_通用學習與面試庫/01_CTF競賽Writeup與題解`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫/01_CTF競賽Writeup與題解) ｜ 🌐 **開源平台**: [AWD Auto Submit Tools](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 135** | 開發 Python AWD 批量抓 Flag 腳本與 API 自動提交 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 136** | 部署 Cron 自動定時任務全網多目標輪流抓取 Flag 提交 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 69 (Day 137-138): AWD 高級繞過與後門徹底排查**
📁 **本地對接**: [`08_通用學習與面試庫/01_CTF競賽Writeup與題解`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫/01_CTF競賽Writeup與題解) ｜ 🌐 **開源平台**: [AWD Advanced Payload Guide](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 137** | 應對對手修補：撰寫二階 POP 鏈與混淆繞過 Exp 攻破對手 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 138** | GameBox 徹底清查：隱藏 Webshell、Cron 後門與不死馬清除 | 📁 [`01_Web安全/08_檔案上傳與包含漏洞`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/08_檔案上傳與包含漏洞) | 按專題課後練習進度 |

---
#### ⚔️ **Run 70 (Day 139-140): 擬真 AWD 實體攻防賽與戰報總結**
📁 **本地對接**: [`08_通用學習與面試庫/01_CTF競賽Writeup與題解`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫/01_CTF競賽Writeup與題解) ｜ 🌐 **線上平台**: [AWD Online Arena](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 139** | 參加 2 小時實時模擬 AWD 攻防對抗賽（攻防實時交鋒） | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 140** | AWD 對抗賽戰報總結、得分與失分攻擊路徑復盤分析 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 71 (Day 141-142): 高階 CVE 漏洞重現 (Log4Shell & Spring4Shell)**
📁 **本地對接**: [`01_Web安全/12_中間件與框架安全`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/12_中間件與框架安全) ｜ 🌐 **線上環境**: [Vulhub Vulnerability Environment](https://vulhub.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 141** | Log4Shell (CVE-2021-44228) JNDI 注入與 RCE 白箱原理 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Live Art (ID: 293)](https://learn.cylabacademy.org/library?search=Live%20Art)<br>🌐 **PortSwigger**: • [Lab: Exploiting XXE to retrieve files](https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-retrieve-files)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Exploiting XXE to perform SSRF attacks](https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-perform-ssrf) |
| **Day 142** | Spring4Shell (CVE-2022-22965) 屬性綁定 RCE 漏洞重現 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Live Art (ID: 293)](https://learn.cylabacademy.org/library?search=Live%20Art)<br>🌐 **PortSwigger**: • [Lab: Exploiting XXE to retrieve files](https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-retrieve-files)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Exploiting XXE to perform SSRF attacks](https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-perform-ssrf) |

---
#### ⚔️ **Run 72 (Day 143-144): 高階 CVE 漏洞重現 (Shiro & ThinkPHP)**
📁 **本地對接**: [`01_Web安全/12_中間件與框架安全`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/12_中間件與框架安全) ｜ 🌐 **線上環境**: [Vulhub Vulnerability Repository](https://vulhub.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 143** | Apache Shiro (CVE-2016-4437) RememberMe 反序列化重現 | 📁 測試本地工具 [`Java反序列化终极测试工具.jar`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/11_反序列化與組件漏洞/03_Java反序列化漏洞/Java反序列化终极测试工具.jar) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Clouds (ID: 288)](https://learn.cylabacademy.org/library?search=Clouds)<br>🌐 **PortSwigger**: • [Lab: HTTP request smuggling, basic CL.TE vulnerability](https://portswigger.net/web-security/request-smuggling/lab-basic-cl-te)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [SaaS (ID: 312)](https://learn.cylabacademy.org/library?search=SaaS) / [zero_to_hero (ID: 323)](https://learn.cylabacademy.org/library?search=zero_to_hero)<br>🌐 **PortSwigger**: • [Lab: HTTP request smuggling, basic TE.CL vulnerability](https://portswigger.net/web-security/request-smuggling/lab-basic-te-cl) |
| **Day 144** | ThinkPHP 5.0.23 5.1.x 容器注入 RCE 漏洞分析與驗證 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Clouds (ID: 288)](https://learn.cylabacademy.org/library?search=Clouds)<br>🌐 **PortSwigger**: • [Lab: HTTP request smuggling, basic CL.TE vulnerability](https://portswigger.net/web-security/request-smuggling/lab-basic-cl-te)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [SaaS (ID: 312)](https://learn.cylabacademy.org/library?search=SaaS) / [zero_to_hero (ID: 323)](https://learn.cylabacademy.org/library?search=zero_to_hero)<br>🌐 **PortSwigger**: • [Lab: HTTP request smuggling, basic TE.CL vulnerability](https://portswigger.net/web-security/request-smuggling/lab-basic-te-cl) |

---
#### ⚔️ **Run 73 (Day 145-146): 自訂 Python CVE 檢測工具與 Exp 開發**
📁 **本地對接**: [`05_代碼審計與安全開發/04_Python安全工具開發`](file:///f:/OutClass/資訊應用/網路安全/05_代碼審計與安全開發/04_Python安全工具開發) ｜ 🌐 **官方文檔**: [Python Security Scripting Guide](https://docs.python.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 145** | 撰寫獨立 Python CVE 自動化檢測 PoC 工具腳本 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Trust But Verify (ID: 783)](https://learn.cylabacademy.org/library?search=Trust%20But%20Verify) / [Neuron Meet 0 (ID: 771)](https://learn.cylabacademy.org/library?search=Neuron%20Meet%200)<br>🌐 **PortSwigger**: • [Lab: Exploiting LLM APIs with indirect prompt injection](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Perceptron Train XOR (ID: 782)](https://learn.cylabacademy.org/library?search=Perceptron%20Train%20XOR) / [Perceptron Train XNOR (ID: 781)](https://learn.cylabacademy.org/library?search=Perceptron%20Train%20XNOR) |
| **Day 146** | 撰寫獨立 Python 漏洞利用 Exp 腳本並加入命令執行介面 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Trust But Verify (ID: 783)](https://learn.cylabacademy.org/library?search=Trust%20But%20Verify) / [Neuron Meet 0 (ID: 771)](https://learn.cylabacademy.org/library?search=Neuron%20Meet%200)<br>🌐 **PortSwigger**: • [Lab: Exploiting LLM APIs with indirect prompt injection](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Perceptron Train XOR (ID: 782)](https://learn.cylabacademy.org/library?search=Perceptron%20Train%20XOR) / [Perceptron Train XNOR (ID: 781)](https://learn.cylabacademy.org/library?search=Perceptron%20Train%20XNOR) |

---
#### ⚔️ **Run 74 (Day 147-148): MSF Ruby Exp 獨立模組開發與封裝**
📁 **本地對接**: [`04_系統與內網安全/01_Metasploit框架與Exp實戰`](file:///f:/OutClass/資訊應用/網路安全/04_系統與內網安全/01_Metasploit框架與Exp實戰) ｜ 🌐 **官方教學**: [Metasploit Module Development](https://www.offsec.com/metasploit-unleashed/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 147** | MSF 模組結構解析：元數據定義、Target 設置與 Payload 對接 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [riscy business (ID: 305)](https://learn.cylabacademy.org/library?search=riscy%20business)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Checkpass (ID: 307)](https://learn.cylabacademy.org/library?search=Checkpass) |
| **Day 148** | 將新發現 CVE 開發為標準 MSF Ruby 攻擊模組並載入測試 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [riscy business (ID: 305)](https://learn.cylabacademy.org/library?search=riscy%20business)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Checkpass (ID: 307)](https://learn.cylabacademy.org/library?search=Checkpass) |

---
#### ⚔️ **Run 75 (Day 149-150): Month 5 階段考核總結與防禦建議產出**
📁 **本地對接**: [`01_Web安全/12_中間件與框架安全`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/12_中間件與框架安全) ｜ 🌐 **復盤報告**: [Cybersecurity Assessment Summary](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 149** | 漏洞重現 Writeup 整理、PoC/Exp 代碼庫維護與驗證 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 150** | Month 5 階段考核總結、CVE 防禦修補建議書產出 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---

## 🗓️ Month 6 (第 151 ~ 180 天 / Run 76 ~ Run 90): 企業級藍隊 SOC 營運、應變處置與畢業專案
#### ⚔️ **Run 76 (Day 151-152): 藍隊 SOC 資安事件應變 (IR) 啟動與封包保存 (結合 CatBoost 惡意封包過濾)**
📁 **本地對接**: [`06_網路安全與數位取證/04_數位取證與應變處置`](file:///f:/OutClass/資訊應用/網路安全/06_網路安全與數位取證/04_數位取證與應變處置) ｜ 🌐 **CISA 指南**: [CISA Incident Handling Guide](https://www.cisa.gov/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 151** | 藍隊 SOC 資安事件應變 (IR) 啟動：受害主機隔離與封包保存 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 152** | 勒索軟體加密副檔名與勒索信樣式排查，識別攻擊家族 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 77 (Day 153-154): 記憶體 Dump 分析與 C2 流量分析 (結合 SHAP 特徵依賴視覺化解析 C2 行為)**
📁 **本地對接**: [`06_網路安全與數位取證/03_記憶體取證與Volatility`](file:///f:/OutClass/資訊應用/網路安全/06_網路安全與數位取證/03_記憶體取證與Volatility) ｜ 🌐 **線上平台**: [Root-Me Memory Forensics](https://www.root-me.org/en/Challenges/Forensic/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 153** | 利用 Volatility 分析受害主機記憶體 Dump，還原惡意進程 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 154** | Wireshark 分析勒索軟體 C2 通訊流量與可疑外聯 IP | 📁 分析本地封包 [`SQLInjection.pcapng`](file:///f:/OutClass/資訊應用/網路安全/06_網路安全與數位取證/01_網路協定分析與Scapy/網路指令/SQLInjection.pcapng) | 按專題課後練習進度 |

---
#### ⚔️ **Run 78 (Day 155-156): 惡意後門排查、根除與防護補強**
📁 **本地對接**: [`06_網路安全與數位取證/04_數位取證與應變處置`](file:///f:/OutClass/資訊應用/網路安全/06_網路安全與數位取證/04_數位取證與應變處置) ｜ 🌐 **工具文檔**: [Microsoft Autoruns Docs](https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 155** | 排查受害主機後門（Autoruns 機碼、排程工作與服務） | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 156** | 根除木馬後門、更新防毒特徵碼與修補漏洞防護 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 79 (Day 157-158): 系統災難復原與 SIEM/WAF 規則調校**
📁 **本地對接**: [`07_藍隊防禦與護網營運`](file:///f:/OutClass/資訊應用/網路安全/07_藍隊防禦與護網營運) ｜ 🌐 **官方指南**: [OWASP Incident Response Recovery](https://owasp.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 157** | 從離線快照與安全備份中還原資料庫與系統服務 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 158** | 調校 SIEM / WAF 防禦告警規則，防止同類漏洞再次引爆 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 80 (Day 159-160): 藍隊 SOC 資安事件處置 (IR) 報告寫作**
📁 **本地對接**: [`06_網路安全與數位取證/04_數位取證與應變處置`](file:///f:/OutClass/資訊應用/網路安全/06_網路安全與數位取證/04_數位取證與應變處置) ｜ 🌐 **報告範本**: [SANS IR Report Template](https://www.sans.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 159** | 撰寫 SOC 藍隊事件應變處置與鑑識報告 (IR Report) | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 160** | 藍隊資安事件復盤會議報告與防禦改善政策評估 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 81 (Day 161-162): 畢業 Capstone（紅隊）：黑盒掃描與入口突破**
📁 **本地對接**: [`01_Web安全/15_綜合靶場與VulnHub實戰演練`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/15_綜合靶場與VulnHub實戰演練) ｜ 🌐 **線上靶場**: [VulnHub Official Site](https://www.vulnhub.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 161** | 終極考核（紅隊）：VulnHub 離線靶機黑盒資訊收集與服務掃描 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 162** | 終極考核（紅隊）：Web 入口點漏洞利用與權限獲取 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 82 (Day 163-164): 畢業 Capstone（紅隊）：提權 Root 與 Writeup**
📁 **本地對接**: [`01_Web安全/15_綜合靶場與VulnHub實戰演練`](file:///f:/OutClass/資訊應用/網路安全/01_Web安全/15_綜合靶場與VulnHub實戰演練) ｜ 🌐 **線上靶場**: [VulnHub Offsec Machines](https://www.vulnhub.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 163** | 終極考核（紅隊）：Linux SUID / Kernel 提權獲取 Root 權限 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 164** | 終極考核（紅隊）：撰寫完整滲透測試 Writeup 與漏洞評估 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 83 (Day 165-166): 畢業 Capstone（藍隊）：代碼修補與 WAF 防禦**
📁 **本地對接**: [`07_藍隊防禦與護網營運`](file:///f:/OutClass/資訊應用/網路安全/07_藍隊防禦與護網營運) ｜ 🌐 **官方項目**: [OWASP ModSecurity CRS](https://coreruleset.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 165** | 終極考核（藍隊）：代碼白箱審計與漏洞源碼修補 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 166** | 終極考核（藍隊）：部署 ModSecurity WAF 自訂 SecRule 防禦 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 84 (Day 167-168): 畢業 Capstone（藍隊）：系統加固與報告產出**
📁 **本地對接**: [`07_藍隊防禦與護網營運`](file:///f:/OutClass/資訊應用/網路安全/07_藍隊防禦與護網營運) ｜ 🌐 **防禦指南**: [CIS Benchmarks Guide](https://www.cisecurity.org/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 167** | 終極考核（藍隊）：Windows/Linux 系統安全加固與帳號審查 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 168** | 終極考核（藍隊）：撰寫藍隊安全加固與修補建議報告 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 85 (Day 169-170): 畢業 Capstone：紅藍互審與成績核算**
📁 **本地對接**: [`08_通用學習與面試庫`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫) ｜ 🌐 **審查指南**: [Peer Review Security Evaluation](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 169** | 紅藍攻防結果對比、同儕互審與攻防路徑復盤 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 170** | 終極考核成績核算、成果評分與專案結算 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 86 (Day 171-172): 結業作品集整理與 GitHub Portfolio**
📁 **本地對接**: [`08_通用學習與面試庫/03_資安面試真題與履歷技巧`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫/03_資安面試真題與履歷技巧) ｜ 🌐 **作品集參考**: [GitHub Cybersecurity Portfolio](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 171** | 整理 6 個月 Writeup 專案庫與 Markdown 整理編排 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 172** | 打造 GitHub 資安專題展示庫 (Cybersecurity Portfolio) | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 87 (Day 173-174): 履歷包裝與技術面試演練**
📁 **本地對接**: [`08_通用學習與面試庫/03_資安面試真題與履歷技巧`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫/03_資安面試真題與履歷技巧) ｜ 🌐 **面試指南**: [Cybersecurity Interview Prep](https://github.com/swisskyrepo/PayloadsAllTheThings)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 173** | 資安工程師履歷撰寫與項目經歷 STAR 原則包裝 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 174** | 資安面試技術題（Web, 內網, 防禦, 協議）模擬問答演練 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 88 (Day 175-176): HR 面試演練與成果簡報製作**
📁 **本地對接**: [`08_通用學習與面試庫/05_HR與跨領域面試`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫/05_HR與跨領域面試) ｜ 🌐 **面試指南**: [HR Behavioral Interview Guide](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 175** | 資安面試 HR 綜合面試題與團隊協作問答演練 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 176** | 讀書會結業專題成果發表簡報 (Slides) 製作 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 89 (Day 177-178): 結業 Live Demo 與擬真技術口試**
📁 **本地對接**: [`08_通用學習與面試庫`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫) ｜ 🌐 **展示指南**: [Cybersecurity Project Demo Guide](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 177** | 讀書會結業專題成果實機演示 (Live Demo) 預演 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 178** | 模擬資安工程師技術口試 (Mock Technical Interview) | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |

---
#### ⚔️ **Run 90 (Day 179-180): 6 個月讀書會圓滿結業與就業啟航**
📁 **本地對接**: [`08_通用學習與面試庫`](file:///f:/OutClass/資訊應用/網路安全/08_通用學習與面試庫) ｜ 🌐 **畢業總結**: [Cybersecurity Career Roadmap](https://github.com/)

| 天數 (Day) | 🎯 當日教學重點 (Focus Task) | 📁 本地影片/檔案與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Instructor Walkthrough & Labs) |
| :--- | :--- | :--- | :--- |
| **Day 179** | 6 個月讀書會成長復盤與頒發結業證書 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |
| **Day 180** | 圓滿結業與資安求職正式啟航 | 📁 [`對應主題學習目錄`](file:///f:/OutClass/資訊應用/網路安全/) | 按專題課後練習進度 |