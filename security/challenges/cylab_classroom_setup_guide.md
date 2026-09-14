# 🏫 資訊安全 6 個月 CTF 教室創建與 90 個 Run 完整選題指南 (Run 1 ~ Run 90 Full Itemized Guide)

> [!IMPORTANT]
> **發布日期**: 2026-08-08
> **用途**: 供組長開立 CyLab / CTF 教室時，依序對照 **Run 1 至 Run 90** 將題目與 Learning Path 加入清單。
> **規則**: 全數 90 個 Run (180 天) **100% 完整收錄**，即使無對應 CyLab 關卡亦明確標註實戰項目與離線靶場！

---

## 🗓️ Month 1 (第 1 ~ 30 天 / Run 1 ~ Run 15): 攻防雙軌基礎與工具鏈入門

### ⚔️ **Run 1 (Day 1-2): HTTP 協定原理與 Burp Suite 代理抓包**
- 🔗 **CyLab / 線上專題**: [PortSwigger Access Control](https://portswigger.net/web-security/access-control)
- 📌 **每日實操與關卡細節**:
  - ****Day 1****: 🎯 HTTP 請求與回應標頭分析 (GET/POST/Header/Status Code)
    🧪 **指定練習/講義**: [PortSwigger: Unprotected Admin](https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality)  ｜ ＋ picoCTF: Insp3ct0r ｜ 💡 **帶練指引**: 指導學員配置 Burp 代理 127.0.0.1:8080 並示範 Repeater 抓包重放
  - ****Day 2****: 🎯 Burp Suite 代理截獲、Repeater 重放與 POST 欄位修改
    🧪 **指定練習/講義**: [PortSwigger: User Role Bypass](https://portswigger.net/web-security)  ｜ ＋ picoCTF: what's a net cat? / Super SSH ｜ 💡 **帶練指引**: 指導學員配置 Burp 代理 127.0.0.1:8080 並示範 Repeater 抓包重放

### ⚔️ **Run 2 (Day 3-4): SQL Injection 基礎與萬能密碼登入繞過**
- 🔗 **CyLab / 線上專題**: [PortSwigger SQLi](https://portswigger.net/web-security/sql-injection)
- 📌 **每日實操與關卡細節**:
  - ****Day 3****: 🎯 SQL 查詢語法剖析、單引號 `'` 閉合原理與注入點判斷
    🧪 **指定練習/講義**: [PortSwigger: SQLi Retrieving Hidden Data](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data)  ｜ ＋ picoCTF: Irish-Name-Repo 1 ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構
  - ****Day 4****: 🎯 `' OR 1=1--` 萬能密碼成因與 POST 表單登入繞過源碼分析
    🧪 **指定練習/講義**: [PortSwigger: SQLi Login Bypass](https://portswigger.net/web-security/sql-injection/lab-login-bypass)  ｜ ＋ picoCTF: Irish-Name-Repo 2 & 3 ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構

### ⚔️ **Run 3 (Day 5-6): 命令執行 (RCE) 與路徑遍歷 (Path Traversal)**
- 🔗 **CyLab / 線上專題**: [PortSwigger OS Command Injection](https://portswigger.net/web-security/os-command-injection) ｜ [PortSwigger File Path Traversal](https://portswigger.net/web-security/file-path-traversal)
- 📌 **每日實操與關卡細節**:
  - ****Day 5****: 🎯 OS 命令注入原理與 Linux/Windows 命令拼接符 (` ; `, ` & `, ` && `, ` \
    🧪 **指定練習/講義**: ` 差異並提供 RCE 測試腳本
  - ****Day 6****: 🎯 路徑遍歷 (Path Traversal) 與 `../` 讀取 `/etc/passwd`
    🧪 **指定練習/講義**: ` 差異並提供 RCE 測試腳本

### ⚔️ **Run 4 (Day 7-8): Wireshark 網路流量分析與協定防禦**
- 🔗 **CyLab / 線上專題**: [Root-Me Network](https://www.root-me.org/en/Challenges/Network/)
- 📌 **每日實操與關卡細節**:
  - ****Day 7****: 🎯 Wireshark 基礎界面、網路介面選擇與網卡混雜模式捕獲
    🧪 **指定練習/講義**: [Root-Me: Network HTTP Headers](https://www.root-me.org/en/Challenges/Network/HTTP-headers)  ｜ ＋ picoCTF: Wireshark doo dooo do doo... ｜ 💡 **帶練指引**: 演示 Wireshark `http.request.method==POST` 顯示過濾語法
  - ****Day 8****: 🎯 Wireshark 顯示過濾語法 (`ip.addr`) 與 HTTP 追蹤流分析
    🧪 **指定練習/講義**: 分析本地 [`SQLInjection.pcapng`](../../../06_網路安全與數位取證/03_流量分析PCAP/Wireshark專題_流量監聽與分析/02_帶練講義與PCAP實戰/SQLInjection.pcapng) 封包  ｜ ＋ picoCTF: Trivial Flag Transfer Protocol ｜ 💡 **帶練指引**: 指導學員配置 Burp 代理 127.0.0.1:8080 並示範 Repeater 抓包重放

### ⚔️ **Run 5 (Day 9-10): 任意檔案上傳與 Webshell 木馬權維**
- 🔗 **CyLab / 線上專題**: [PortSwigger File Upload](https://portswigger.net/web-security/file-upload)
- 📌 **每日實操與關卡細節**:
  - ****Day 9****: 🎯 任意檔案上傳原理、前端 JS 驗證繞過與 Content-Type 偽造
    🧪 **指定練習/講義**: [PortSwigger: File Upload Content-Type Bypass](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass) ｜ 💡 **帶練指引**: 發放 PHP 一句話木馬 `<?php @eval($_POST['cmd']);?>` 講義與中國蟻劍連線步驟
  - ****Day 10****: 🎯 一句話木馬編寫與中國蟻劍 (AntSword) 連接 Webshell
    🧪 **指定練習/講義**: [PortSwigger: Remote Code Execution via Webshell](https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload) ｜ 💡 **帶練指引**: 發放 PHP 一句話木馬 `<?php @eval($_POST['cmd']);?>` 講義與中國蟻劍連線步驟

### ⚔️ **Run 6 (Day 11-12): x86/x64 彙編基礎與 GDB / Pwntools 環境建立**
- 🔗 **CyLab / 線上專題**: [pwn.college Dojo](https://pwn.college/)
- 📌 **每日實操與關卡細節**:
  - ****Day 11****: 🎯 x86/x64 彙編暫存器 (EAX, ESP, EBP, EIP) 與記憶體堆疊結構
    🧪 **指定練習/講義**: [pwn.college: Program Misuse](https://pwn.college/)  ｜ ＋ picoCTF: Bit-O-Asm-1 ~ Bit-O-Asm-4 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 12****: 🎯 Linux GDB 調試器指令 (`gdb ./pwn`) 與 Pwntools 腳本撰寫
    🧪 **指定練習/講義**: [Root-Me: ELF x86 Stack Overflow basic 1](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-Stack-buffer-overflow-basic-1)  ｜ ＋ picoCTF: GDB baby step 1 ~ GDB baby step 4 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 7 (Day 13-14): XSS 跨站腳本與 CSRF / SSRF 攻擊**
- 🔗 **CyLab / 線上專題**: [PortSwigger XSS](https://portswigger.net/web-security/cross-site-scripting) & [SSRF](https://portswigger.net/web-security/ssrf)
- 📌 **每日實操與關卡細節**:
  - ****Day 13****: 🎯 XSS 跨站腳本成因、Reflected XSS 與 DOM-based XSS 彈窗
    🧪 **指定練習/講義**: [PortSwigger: Reflected XSS](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 14****: 🎯 CSRF 跨站請求偽造 PoC HTML 產生與 SSRF 內網探測
    🧪 **指定練習/講義**: [PortSwigger: SSRF Localhost](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 8 (Day 15-16): Ghidra / IDA Pro 靜態逆向工程基礎**
- 🔗 **CyLab / 線上專題**: [Root-Me Cracking](https://www.root-me.org/en/Challenges/Cracking/)
- 📌 **每日實操與關卡細節**:
  - ****Day 15****: 🎯 逆向工程導論、靜態分析概念與 PE / ELF 可執行檔結構
    🧪 **指定練習/講義**: PEbear 解析 PE 標頭  ｜ ＋ picoCTF: Safe Opener 1 & 2 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 16****: 🎯 Ghidra / IDA Pro 反編譯 C 偽代碼與 Serial 驗證邏輯逆向
    🧪 **指定練習/講義**: [Root-Me: ELF ARM Basic Keygen](https://www.root-me.org/en/Challenges/Cracking/)  ｜ ＋ picoCTF: vault-door-training ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 9 (Day 17-18): 越權漏洞 (IDOR) 與 Cookie/Session 會話劫持**
- 🔗 **CyLab / 線上專題**: [PortSwigger Access Control](https://portswigger.net/web-security/access-control)
- 📌 **每日實操與關卡細節**:
  - ****Day 17****: 🎯 IDOR 越權原理與平行越權修改 `id=1001` 檢視他人信件
    🧪 **指定練習/講義**: [PortSwigger: IDOR Lab](https://portswigger.net/web-security/access-control/lab-insecure-direct-object-references) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 18****: 🎯 垂直越權、URL 權限控制繞過與 Session 劫持攻擊
    🧪 **指定練習/講義**: [PortSwigger: URL Access Control Bypass](https://portswigger.net/web-security) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 10 (Day 19-20): Linux / Windows 本地權限提升 (PrivEsc)**
- 🔗 **CyLab / 線上專題**: [OverTheWire Bandit](https://overthewire.org/wargames/bandit/)
- 📌 **每日實操與關卡細節**:
  - ****Day 19****: 🎯 Linux SUID 提權原理與 `find / -perm -4000` 尋找特權 binary
    🧪 **指定練習/講義**: OverTheWire: Bandit (Levels 0-5)  ｜ ＋ picoCTF: Magikarp Ground Mission / First Find ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 20****: 🎯 MySQL UDF 提權原理與 Windows 服務路徑弱點提權實戰
    🧪 **指定練習/講義**: OverTheWire: Bandit (Levels 6-10)  ｜ ＋ picoCTF: Big Zip / strings it / plumbing ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構

### ⚔️ **Run 11 (Day 21-22): SSTI 模板注入與 PHP/Java 反序列化**
- 🔗 **CyLab / 線上專題**: [PortSwigger SSTI](https://portswigger.net/web-security/server-side-template-injection)
- 📌 **每日實操與關卡細節**:
  - ****Day 21****: 🎯 Flask Jinja2 SSTI 原理與 `{{config}}` / `__class__` 變數洩露
    🧪 **指定練習/講義**: PortSwigger: SSTI Basic Injection ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 22****: 🎯 PHP 魔術方法 `__wakeup()` 觸發與 Java 物件反序列化
    🧪 **指定練習/講義**: [PortSwigger: XXE File Retrieval](https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-retrieve-files) ｜ 💡 **帶練指引**: 演示 ysoserial 工具 CommonsCollections 鏈命令行生成 Exp

### ⚔️ **Run 12 (Day 23-24): PWN 堆疊溢出 (Stack Overflow) 緩衝區溢出**
- 🔗 **CyLab / 線上專題**: [pwnable.kr](http://pwnable.kr/)
- 📌 **每日實操與關卡細節**:
  - ****Day 23****: 🎯 PWN 堆疊溢出 (Stack Overflow) 記憶體佈局與 NOP Sled 原理
    🧪 **指定練習/講義**: pwnable.kr: `fd` 關卡（檔案描述符判讀）  ｜ ＋ picoCTF: buffer overflow 0 / Local Target ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 24****: 🎯 `ret2text` 篡改 EIP/RIP 執行流與 Pwntools 自動化 Exp 撰寫
    🧪 **指定練習/講義**: pwnable.kr: `bof` 關卡（緩衝區溢出覆寫）  ｜ ＋ picoCTF: buffer overflow 1 / Picker I ~ IV ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 13 (Day 25-26): CryptoHack 密碼學基礎 (RSA / AES 算法原理)**
- 🔗 **CyLab / 線上專題**: [CryptoHack](https://cryptohack.org/)
- 📌 **每日實操與關卡細節**:
  - ****Day 25****: 🎯 Base64、ASCII、XOR 位元運算與對稱加密基礎觀念
    🧪 **指定練習/講義**: CryptoHack: Introduction to Cryptography  ｜ ＋ picoCTF: 2warm / Warmed Up / caesar / interencdec ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 26****: 🎯 RSA 公私鑰數學原理 (p, q, n, e, d) 與大數分解陷阱
    🧪 **指定練習/講義**: CryptoHack: RSA Modular Math  ｜ ＋ picoCTF: Mind your Ps and Qs / Mini RSA / rsa_oracle ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 14 (Day 27-28): 內網滲透 (SOCKS5 隧道 / Pivoting / AD 域控攻防)**
- 🔗 **CyLab / 線上專題**: [TryHackMe Active Directory](https://tryhackme.com/)
- 📌 **每日實操與關卡細節**:
  - ****Day 27****: 🎯 MSF / Chisel 搭建 SOCKS5 代理隧道與 Pivoting 內網穿透
    🧪 **指定練習/講義**: TryHackMe: Wreath Network Pivoting ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 28****: 🎯 Active Directory 域控基礎、Kerberos 驗證流程與黃金票據
    🧪 **指定練習/講義**: TryHackMe: Attacktive Directory ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 15 (Day 29-30): Month 1 階段總複盤與黑盒 VulnHub 靶機通關**
- 🔗 **CyLab / 線上專題**: [VulnHub](https://www.vulnhub.com/)
- 📌 **每日實操與關卡細節**:
  - ****Day 29****: 🎯 黑盒 VulnHub 靶機 (Os-hackNos) 資訊收集與 Nmap 服務掃描
    🧪 **指定練習/講義**: Os-hackNos 靶機實戰 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 30****: 🎯 靶機漏洞組合利用、獲取 Root 權限與 Writeup 撰寫
    🧪 **指定練習/講義**: 撰寫 Month 1 結業 Writeup 報告 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義


---

## 🗓️ Month 2 (第 31 ~ 60 天 / Run 16 ~ Run 30): 核心漏洞深造與高級攻防

### ⚔️ **Run 16 (Day 31-32): SQL Injection 盲注與 OOB DNSLog 帶外注入**
- 🔗 **CyLab / 線上專題**: [PortSwigger Blind SQLi](https://portswigger.net/web-security/sql-injection/blind)
- 📌 **每日實操與關卡細節**:
  - ****Day 31****: 🎯 布林盲注與時間盲注 (`sleep(3)`, `ascii(substr())`) 原理與推算腳本
    🧪 **指定練習/講義**: [PortSwigger: Blind SQLi Time Delays](https://portswigger.net/web-security/sql-injection/blind/lab-time-delays) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 32****: 🎯 DNSLog Out-of-band (OOB) 帶外注入與 `LOAD_FILE()` 數據外排
    🧪 **指定練習/講義**: [PortSwigger: Blind SQLi OOB Interaction](https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 17 (Day 33-34): SQL Injection WAF 繞過與拖庫實戰**
- 🔗 **CyLab / 線上專題**: [PortSwigger SQLi Filter Bypass](https://portswigger.net/web-security/sql-injection)
- 📌 **每日實操與關卡細節**:
  - ****Day 33****: 🎯 大小寫混淆、雙寫繞過與 `/*!50000union*/` 行內註釋繞過 WAF
    🧪 **指定練習/講義**: PortSwigger: SQLi Filter Bypass ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 34****: 🎯 `mysqldump` 資料庫備份與 MySQL UDF (`sys_eval`) 特權執行
    🧪 **指定練習/講義**: 觀看 [`10.8MYSQLUDF提权与命令执行.mp4`](../../../01_Web安全/06_SQL注入漏洞專題/07_SQL注入WAF繞過與拖庫/10.8MYSQLUDF提权与命令执行.mp4) ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構

### ⚔️ **Run 18 (Day 35-36): Sqlmap 工具高級參數與 Tamper 腳本編寫**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 35****: 🎯 Sqlmap `-r req.txt`, `--level 5 --risk 3`, `--os-shell` 抓包拖庫參數
    🧪 **指定練習/講義**: 本地 Sqlmap 手冊演練 ｜ 💡 **帶練指引**: 提供 MySQL UDF `sys_eval` 提權 C 語言導出腳本模板
  - ****Day 36****: 🎯 自訂 Sqlmap `tamper` 混淆腳本編寫與安全狗 (Safedog) 繞過
    🧪 **指定練習/講義**: Python tamper 腳本寫作演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 19 (Day 37-38): 任意檔案上傳高級繞過與解析漏洞**
- 🔗 **CyLab / 線上專題**: [PortSwigger File Upload](https://portswigger.net/web-security/file-upload)
- 📌 **每日實操與關卡細節**:
  - ****Day 37****: 🎯 雙重副檔名 (`.php.jpg`)、`0x00` 截斷與 `.htaccess` 繞過
    🧪 **指定練習/講義**: [PortSwigger: File Upload Content-Type Bypass](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 38****: 🎯 Apache / Nginx 解析漏洞 (`/1.php/1.jpg`) 與 PUT 寫入木馬
    🧪 **指定練習/講義**: [PortSwigger: File Upload Extension Bypass](https://portswigger.net/web-security) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 20 (Day 39-40): LFI 本地檔案包含與 RFI 遠端檔案包含**
- 🔗 **CyLab / 線上專題**: [PortSwigger Path Traversal](https://portswigger.net/web-security/file-path-traversal)
- 📌 **每日實操與關卡細節**:
  - ****Day 39****: 🎯 LFI 配合 `php://filter` 讀取源碼與 `php://input` 執行木馬
    🧪 **指定練習/講義**: [PortSwigger: Path Traversal Absolute Path Bypass](https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 40****: 🎯 Session 檔案包含與 Log 日誌注入 (`/var/log/apache2/access.log`) GETSHELL
    🧪 **指定練習/講義**: 本地日誌包含 GETSHELL 實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 21 (Day 41-42): DOM-based XSS 與 JS 加密解密逆向**
- 🔗 **CyLab / 線上專題**: [PortSwigger DOM XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)
- 📌 **每日實操與關卡細節**:
  - ****Day 41****: 🎯 DOM XSS Source & Sink (`location.search`, `document.write`) 剖析
    🧪 **指定練習/講義**: [PortSwigger: DOM XSS document.write Sink](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink)  ｜ ＋ picoCTF: vault-door-1 ~ 4 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 42****: 🎯 前端 JS 混淆代碼逆向與 Chrome DevTools 中斷點調試解密
    🧪 **指定練習/講義**: 破解本地 [`exam.html`](../../../01_Web安全/01_前端語言與語法/05_JS加密解密與前端解題/exam.html) 前端加密  ｜ ＋ picoCTF: vault-door-5 ~ 8 ｜ 💡 **帶練指引**: 引導學員在 Chrome DevTools 設定 Event Listener Breakpoints

### ⚔️ **Run 22 (Day 43-44): SSRF 高級利用與 127.0.0.1 內網探測**
- 🔗 **CyLab / 線上專題**: [PortSwigger SSRF](https://portswigger.net/web-security/ssrf)
- 📌 **每日實操與關卡細節**:
  - ****Day 43****: 🎯 SSRF 配合 `gopher://` 與 `dict://` 協定攻擊內網 Redis
    🧪 **指定練習/講義**: [PortSwigger: SSRF Against Backend System](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 44****: 🎯 SSRF 繞過 127.0.0.1 過濾 (DNS Rebinding, 十六進位 IP 表示)
    🧪 **指定練習/講義**: [PortSwigger: SSRF Filter Bypass Open Redirection](https://portswigger.net/web-security/ssrf/lab-ssrf-filter-bypass-via-open-redirection) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 23 (Day 45-46): 業務邏輯漏洞 (支付篡改、驗證碼繞過、JSON 劫持)**
- 🔗 **CyLab / 線上專題**: [PortSwigger Logic Flaws](https://portswigger.net/web-security/logic-flaws)
- 📌 **每日實操與關卡細節**:
  - ****Day 45****: 🎯 支付金額篡改、負數下單與驗證碼可預測/未失效漏洞
    🧪 **指定練習/講義**: [PortSwigger: High-Level Logic Flaw](https://portswigger.net/web-security) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 46****: 🎯 JSONP 跨域數據劫持與 CORS 跨域資源共享配置缺陷利用
    🧪 **指定練習/講義**: [PortSwigger: CORS Trusted Insecure Origin](https://portswigger.net/web-security) ｜ 💡 **帶練指引**: 引導學員在 Chrome DevTools 設定 Event Listener Breakpoints

### ⚔️ **Run 24 (Day 47-48): Linux 權限提升進階 (Kernel Exploit, Dirty COW, Sudo)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 47****: 🎯 Linux 內核溢出漏洞利用 (Dirty COW 臟牛, PTRACE_TRACEME)
    🧪 **指定練習/講義**: 觀看 [`10.1WEB安全第六章提权篇LINUX内核漏洞提权.mp4`](../../../04_系統與內網安全/05_權限提升/Linux內核提權/10.1WEB安全第六章提权篇LINUX内核漏洞提权.mp4) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 48****: 🎯 Sudo 權限配置漏洞 (`sudo -l`) 與 Linux Cron Jobs 定時任務提權
    🧪 **指定練習/講義**: 觀看 [`10.5WEB安全第六章提权篇LINUXCRONJOBS提权.mp4`](../../../04_系統與內網安全/05_權限提升/Linux內核提權/10.5WEB安全第六章提权篇LINUXCRONJOBS提权.mp4) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 25 (Day 49-50): Windows 權限提升進階 (Bypass UAC, Token Impersonation)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 49****: 🎯 Windows Server 2008R2 溢出提權與 LPK 劫持提權
    🧪 **指定練習/講義**: 觀看 [`10.10WEB安全第六章提权篇winserver2008R2溢出提权.mp4`](../../../04_系統與內網安全/05_權限提升/Windows溢出提權/10.10WEB安全第六章提权篇winserver2008R2溢出提权.mp4) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 50****: 🎯 Token 冒充 (JuicyPotato, RoguePotato) 與 Zend 反彈 Shell
    🧪 **指定練習/講義**: 觀看 [`10.13WEB安全第六章提权篇zend反弹shell提权.mp4`](../../../04_系統與內網安全/05_權限提升/Windows溢出提權/10.13WEB安全第六章提权篇zend反弹shell提权.mp4) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 26 (Day 51-52): PHP 反序列化 POP 鏈與 PHPGGC 實戰**
- 🔗 **CyLab / 線上專題**: [PortSwigger Deserialization](https://portswigger.net/web-security/deserialization)
- 📌 **每日實操與關卡細節**:
  - ****Day 51****: 🎯 PHP POP 鏈 (Property-Oriented Programming) 魔術方法構造
    🧪 **指定練習/講義**: POP 鏈手寫演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 52****: 🎯 PHPGGC 自動化 Payload 生成器與 Phar 反序列化利用
    🧪 **指定練習/講義**: 本地 PHPGGC 工具庫演練 ｜ 💡 **帶練指引**: 演示 ysoserial 工具 CommonsCollections 鏈命令行生成 Exp

### ⚔️ **Run 27 (Day 53-54): Java 反序列化 (ysoserial, Shiro, Fastjson)**
- 🔗 **CyLab / 線上專題**: [PortSwigger Java Deserialization](https://portswigger.net/web-security/deserialization)
- 📌 **每日實操與關卡細節**:
  - ****Day 53****: 🎯 Java `readObject()` 漏洞成因、ysoserial 工具與 CC 鏈分析
    🧪 **指定練習/講義**: 測試本地 [`Java反序列化终极测试工具.jar`](../../../01_Web安全/11_反序列化與組件漏洞/03_Java反序列化漏洞/Java反序列化终极测试工具.jar) ｜ 💡 **帶練指引**: 演示 ysoserial 工具 CommonsCollections 鏈命令行生成 Exp
  - ****Day 54****: 🎯 Apache Shiro RememberMe 金鑰硬編碼與 Fastjson autoType 繞過 Exp
    🧪 **指定練習/講義**: Shiro / Fastjson Exp 測試 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 28 (Day 55-56): 中間件與框架安全 (Apache, Nginx, Tomcat, Spring)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 55****: 🎯 Tomcat 弱口令 Manager 部署 WAR 包 GetShell 與 CVE-2017-12615
    🧪 **指定練習/講義**: Tomcat WAR 上傳實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 56****: 🎯 Spring Core RCE (Spring4Shell) 與 ThinkPHP5 5.0.23 RCE 漏洞剖析
    🧪 **指定練習/講義**: ThinkPHP RCE 測試 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 29 (Day 57-58): AWVS & Xray 自動化漏洞聯動掃描**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 57****: 🎯 AWVS 14 漏洞自動化掃描器配置與黑盒主動掃描
    🧪 **指定練習/講義**: AWVS 掃描任務設定 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 58****: 🎯 Burp Suite + Xray 被動式掃描器代理聯動挖掘
    🧪 **指定練習/講義**: Burp + Xray 被動代理聯動 ｜ 💡 **帶練指引**: 指導學員配置 Burp 代理 127.0.0.1:8080 並示範 Repeater 抓包重放

### ⚔️ **Run 30 (Day 59-60): Month 2 階段復盤與黑盒 CMS 靶場實戰 (YXCMS / WordPress)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 59****: 🎯 YXCMS 1.4.7 離線靶場部署與黑盒滲透測試
    🧪 **指定練習/講義**: 解壓 [`YXCMS.zip`](../../../01_Web安全/14_綜合靶場與VulnHub實戰演練/02_CMS實務靶場環境/YXCMS.zip) 本地搭建測試 ｜ 💡 **帶練指引**: 協助學員在本地 phpStudy/Docker 部署 YXCMS 並引導黑盒測試
  - ****Day 60****: 🎯 WordPress 綜合檢測與 Month 2 階段 Writeup 總結
    🧪 **指定練習/講義**: 使用 [`Wordpress综合检测工具.exe`](../../../01_Web安全/14_綜合靶場與VulnHub實戰演練/02_CMS實務靶場環境/Wordpress综合检测工具.exe) 測試 ｜ 💡 **帶練指引**: 協助學員在本地 phpStudy/Docker 部署 YXCMS 並引導黑盒測試


---

## 🗓️ Month 3 (第 61 ~ 90 天 / Run 31 ~ Run 45): 二進制 PWN、逆向工程與紅隊內網滲透

### ⚔️ **Run 31 (Day 61-62): Linux GDB 調試與 Pwntools 自動化控制**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 61****: 🎯 Linux GDB 調試器高級指令 (`gdb ./pwn`, `x/20wx $esp`) 記憶體剖析
    🧪 **指定練習/講義**: pwnable.kr: `fd` 關卡（檔案描述符判讀） ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 62****: 🎯 Pwntools Python 庫 (`process()`, `remote()`) 自動化 Exp 腳本撰寫
    🧪 **指定練習/講義**: pwnable.kr: `bof` 關卡（緩衝區溢出覆寫） ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 32 (Day 63-64): PWN ROP 鏈 (Return-Oriented Programming) 實戰**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 63****: 🎯 Linux NX 記憶體保護與 ROPgadget 搜尋 `pop rdi; ret` Gadget
    🧪 **指定練習/講義**: [Root-Me: Stack Overflow 2](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-Stack-buffer-overflow-basic-2) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 64****: 🎯 64 位元 ROP 鏈構造與 `ret2libc` 洩露 libc 位址
    🧪 **指定練習/講義**: [pwn.college: Web Server Assembly](https://pwn.college/) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 33 (Day 65-66): PWN 格式化字串漏洞與任意記憶體讀寫**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 65****: 🎯 格式化字串漏洞 (`printf`) 記憶體洩露原理
    🧪 **指定練習/講義**: [Root-Me: Format String Basic 1](https://www.root-me.org/en/Challenges/Cracking/ELF-x86-Format-string-bug-basic-1) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 66****: 🎯 利用 `%n` 任意寫入與 GOT 表改寫
    🧪 **指定練習/講義**: pwnable.kr: `passcode` 關卡（GOT 表覆寫） ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 34 (Day 67-68): Ghidra / IDA Pro 逆向工程與 C/C++ 反編譯分析**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 67****: 🎯 Ghidra 靜態分析 C/C++ 結構體與指針排列微觀剖析
    🧪 **指定練習/講義**: [Root-Me: Keygen Challenge](https://www.root-me.org/en/Challenges/Cracking/)  ｜ ＋ picoCTF: Investigative Reversing 0 ~ 2 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 68****: 🎯 控制流圖 (CFG) 導覽與 Binary Patch 修改跳過註冊驗證
    🧪 **指定練習/講義**: PE Binary Patch 實操  ｜ ＋ picoCTF: Investigative Reversing 3 & 4 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 35 (Day 69-70): Android APK 逆向與 Smali 代碼動態調試**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 69****: 🎯 Android APK 結構解析、`apktool` 解包與 Smali 閱讀
    🧪 **指定練習/講義**: apktool 反編譯演練  ｜ ＋ picoCTF: droids0 / droids1 / droids2 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 70****: 🎯 JADX-GUI 動態調試 Android APK 與 驗證邏輯 Patch
    🧪 **指定練習/講義**: JADX 靜態追蹤演練  ｜ ＋ picoCTF: droids3 / droids4 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 36 (Day 71-72): 內網資產探測 (Nmap, Masscan, fscan)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 71****: 🎯 Nmap 內網 C 段主機存活探測 (`nmap -sn`) 與服務識別
    🧪 **指定練習/講義**: Nmap 內網掃描實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 72****: 🎯 fscan 自動化內網掃描與弱口令爆破 (SSH, RDP, MySQL)
    🧪 **指定練習/講義**: fscan 內網掃描演練 ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構

### ⚔️ **Run 37 (Day 73-74): 橫向移動 (Pass-the-Hash, WMI, PsExec)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 73****: 🎯 Pass-the-Hash (哈希傳遞) 攻擊與 Mimikatz 抓取 NTLM Hash
    🧪 **指定練習/講義**: Impacket `pth-toolkit` 演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 74****: 🎯 利用 WMI (`wmiexec.py`) 與 PsExec 實現無文件橫向執行
    🧪 **指定練習/講義**: Impacket `wmiexec.py` 演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 38 (Day 75-76): Cobalt Strike C2 部署與 Listener / Stager 控權**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 75****: 🎯 Cobalt Strike Teamserver 搭建與 Client 連線
    🧪 **指定練習/講義**: CS Teamserver 架設 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 76****: 🎯 CS Listener 設定、生成 Beacon Stager 與權限維持
    🧪 **指定練習/講義**: CS Beacon 控權演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 39 (Day 77-78): Active Directory 域控攻擊 (Kerberoasting, AS-REP Roasting)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 77****: 🎯 Active Directory 域控架構與 Kerberos 認證流程
    🧪 **指定練習/講義**: Kerberos 協定抓包判讀 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 78****: 🎯 Kerberoasting 攻擊與 AS-REP Roasting 離線爆破 Hash
    🧪 **指定練習/講義**: Impacket `GetUserSPNs.py` 演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 40 (Day 79-80): Golden Ticket & Silver Ticket 域控接管**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 79****: 🎯 Golden Ticket (黃金票據) 偽造與 `krbtgt` Hash 控制域控
    🧪 **指定練習/講義**: Mimikatz `kerberos::golden` 實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 80****: 🎯 Silver Ticket (白銀票據) 偽造與 MSSQL / CIFS 服務切入
    🧪 **指定練習/講義**: Mimikatz `kerberos::silver` 實操 ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構

### ⚔️ **Run 41 (Day 81-82): 免殺與 Shellcode 載入器 (Bypass AV)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 81****: 🎯 免殺技術：Shellcode Loader 異或 / AES 特徵加密解密
    🧪 **指定練習/講義**: 閱讀 [`紅隊軟體免殺技術`](../../../04_系統與內網安全/08_C2與控權/紅隊軟體免殺技術) 指南 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 82****: 🎯 利用 Windows API (`VirtualAlloc`, `RtlMoveMemory`) 繞過記憶體掃描
    🧪 **指定練習/講義**: 測試本地 [`木馬測試`](../../../04_系統與內網安全/08_C2與控權/木馬測試) 目錄 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 42 (Day 83-84): Linux / Windows 權限維持與後門 (Persistence)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 83****: 🎯 Linux 權限維持：SSH 公鑰寫入、Crontab 定時任務與 SUID 後門
    🧪 **指定練習/講義**: Linux 後門部署實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 84****: 🎯 Windows 權限維持：機碼自啟動、排程工作與服務後門
    🧪 **指定練習/講義**: Windows 機碼後門部署 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 43 (Day 85-86): Metasploit (MSF) 高級模組與 Exp 開發**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 85****: 🎯 MSF `msfvenom` 生成 Payload 與 Handler 監聽設定
    🧪 **指定練習/講義**: MSF Meterpreter 操練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 86****: 🎯 MSF 自訂 Ruby 漏洞利用模組 (Exp) 寫作規範與 API 對接
    🧪 **指定練習/講義**: 閱讀 [`漏洞利用Exp框架`](../../../04_系統與內網安全/08_C2與控權/漏洞利用Exp框架) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 44 (Day 87-88): 內網縱深防禦與痕跡清理**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 87****: 🎯 攻擊痕跡清理：Linux 命令歷史 (`history -c`) 與 Windows 事件日誌
    🧪 **指定練習/講義**: 日誌清理演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 88****: 🎯 內網網路隔離 (VLAN, ACL, Zero Trust) 策略評估與紅隊復盤
    🧪 **指定練習/講義**: 防禦建議書撰寫 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 45 (Day 89-90): Month 3 階段總復盤與內網 AD 域控攻防靶場通關**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 89****: 🎯 內網 AD 靶場：Web 入口點突破 ➔ SOCKS5 代理穿透進入內網
    🧪 **指定練習/講義**: 內網代理穿透實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 90****: 🎯 橫向移動至域控 (DC) 獲取 Domain Admin 與 Writeup 撰寫
    🧪 **指定練習/講義**: 撰寫 Month 3 結業報告 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義


---

## 🗓️ Month 4 (第 91 ~ 120 天 / Run 46 ~ Run 60): 代碼審計、安全開發與藍隊防禦

### ⚔️ **Run 46 (Day 91-92): PHP 代碼審計基礎與危險函數追蹤**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 91****: 🎯 PHP 代碼審計基礎：危險函數 (`eval`, `exec`) 定位與 Seay 工具
    🧪 **指定練習/講義**: Seay 工具白箱實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 92****: 🎯 PHP 變數追蹤法 (Sinks to Sources) 與 SQLi / XSS 白箱發現
    🧪 **指定練習/講義**: 白箱變數追蹤演練 ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構

### ⚔️ **Run 47 (Day 93-94): Java 代碼審計 (Spring / Servlet SQLi, RCE 審計)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 93****: 🎯 Java Web 架構 (Filter, Servlet, Spring MVC) 與 Controller 入口
    🧪 **指定練習/講義**: Java MVC 結構閱讀 ｜ 💡 **帶練指引**: 演示 ysoserial 工具 CommonsCollections 鏈命令行生成 Exp
  - ****Day 94****: 🎯 Java SQL 拼接 (MyBatis `${}` vs `#{}`) 與 `Runtime.exec()` RCE
    🧪 **指定練習/講義**: MyBatis SQLi 審計演練 ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構

### ⚔️ **Run 48 (Day 95-96): 開源 CMS 代碼審計項目實戰 (YXCMS 白箱審計)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 95****: 🎯 YXCMS 1.4.7 解包、路由解析與 SQL 查詢構造器白箱分析
    🧪 **指定練習/講義**: 本地 YXCMS 源碼閱讀 ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構
  - ****Day 96****: 🎯 YXCMS 前台 SQL 注入與後台寫入 GetShell 驗證與 0day 挖掘
    🧪 **指定練習/講義**: 撰寫 YXCMS 審計報告 ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構

### ⚔️ **Run 49 (Day 97-98): Python 安全開發 (自動化掃描工具開發)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 97****: 🎯 Python Requests 模組：Session 維持、代理設定與自訂 Header
    🧪 **指定練習/講義**: 撰寫 HTTP 請求腳本 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 98****: 🎯 Python `threading` 多執行緒目錄 Fuzz 與漏洞掃描器編寫
    🧪 **指定練習/講義**: 開發目錄爆破腳本 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 50 (Day 99-100): 藍隊防禦與護網日誌分析 (Web 攻擊日誌)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 99****: 🎯 Apache / Nginx Access Log 剖析與 Web 攻擊特徵日誌搜尋
    🧪 **指定練習/講義**: Linux 命令行日誌過濾 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 100****: 🎯 利用 Linux `grep`, `awk`, `uniq -c` 極速統計可疑 IP 紀錄
    🧪 **指定練習/講義**: Shell 腳本日誌過濾演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 51 (Day 101-102): SIEM 與 ELK 集中日誌過濾與告警**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 101****: 🎯 SIEM 概念與 ELK (Elasticsearch, Logstash, Kibana) 集中日誌
    🧪 **指定練習/講義**: Kibana 儀表板閱讀 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 102****: 🎯 撰寫 Kibana KQL 告警查詢語法與 Web 爆破實時告警
    🧪 **指定練習/講義**: KQL 告警語法演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 52 (Day 103-104): Windows 事件檢視器與 Sysmon 日誌分析**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 103****: 🎯 Windows 事件檢視器關鍵 Event ID (4624, 4625, 4672) 判讀
    🧪 **指定練習/講義**: Windows Event 追蹤 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 104****: 🎯 Sysmon 配置檔編寫、進程創建與網路連線告警捕捉
    🧪 **指定練習/講義**: Sysmon XML 配置實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 53 (Day 105-106): 記憶體取證 (Volatility 分析 Dump 檔案)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 105****: 🎯 記憶體取證導論、Volatility 2.6/3 安裝與 Profile 選取
    🧪 **指定練習/講義**: Volatility 命令演練  ｜ ＋ picoCTF: Sleuthkit Intro / Sleuthkit Apprentice ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 106****: 🎯 Volatility 實戰：`pslist`, `netscan`, `dumpfiles` 還原木馬
    🧪 **指定練習/講義**: [Root-Me: Memory Forensic](https://www.root-me.org/en/Challenges/Forensic/)  ｜ ＋ picoCTF: Disk, disk, sleuth! I & II ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 54 (Day 107-108): 勒索軟體與木馬應變處置 (IR Incident Response)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 107****: 🎯 藍隊資安事件應變處置 (IR) 標準流程 (準備 ➔ 檢測 ➔ 根除)
    🧪 **指定練習/講義**: IR 處置流程手冊閱讀 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 108****: 🎯 惡意進程與後門排查工具 (Process Hacker, TCPView, Autoruns)
    🧪 **指定練習/講義**: Autoruns 後門清除實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 55 (Day 109-110): 密碼學進階 (ECC, Diffie-Hellman, SHA-256)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 109****: 🎯 ECC 橢圓曲線加密與 Diffie-Hellman 金鑰交換數學原理
    🧪 **指定練習/講義**: [CryptoHack: Diffie-Hellman](https://cryptohack.org/) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 110****: 🎯 SHA-256 / MD5 哈希長度擴展攻擊與 HashPump 工具實操
    🧪 **指定練習/講義**: HashPump 攻擊演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 56 (Day 111-112): 隱寫術 (Steganography: Stegsolve, OutGuess)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 111****: 🎯 隱寫術導論、Stegsolve 工具使用、圖片 LSB 最低有效位提取
    🧪 **指定練習/講義**: Stegsolve 圖片分析實操  ｜ ＋ picoCTF: St3g0 / What Lies Within / Glory of the Garden ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 112****: 🎯 音訊隱寫 (Audacity 頻譜圖) 與 OutGuess / Steghide 密碼破解
    🧪 **指定練習/講義**: Audacity 音訊隱寫實操  ｜ ＋ picoCTF: m00nwalk 1 & m00nwalk 2 (SSTV 音訊隱寫) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 57 (Day 113-114): 網頁安全防禦加固與 WAF 規則撰寫**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 113****: 🎯 ModSecurity WAF 安裝配置與 OWASP CRS 部署調校
    🧪 **指定練習/講義**: ModSecurity 配置演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 114****: 🎯 撰寫自訂 SecRule 規則防禦 SQLi, XSS 與 RCE 命令執行
    🧪 **指定練習/講義**: WAF SecRule 編寫實操 ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構

### ⚔️ **Run 58 (Day 115-116): 資安筆試題庫解析 (觀念題/協議題/防禦題)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 115****: 🎯 TCP/IP 三向交握、TLS 1.3 握手流程、HTTP 狀態碼筆試題
    🧪 **指定練習/講義**: 本地筆試題庫刷題 ｜ 💡 **帶練指引**: 指導學員配置 Burp 代理 127.0.0.1:8080 並示範 Repeater 抓包重放
  - ****Day 116****: 🎯 同源策略 (SOP)、CORS、Cookie 屬性 (`SameSite`) 筆試真題
    🧪 **指定練習/講義**: 筆試真題模擬測試 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 59 (Day 117-118): 資安面試真題與履歷包裝**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 117****: 🎯 滲透測試項目經歷 STAR 原則描述與漏洞復盤表達
    🧪 **指定練習/講義**: 閱讀 [`技术面 分享.md`](../../../08_通用學習與面試庫/05_HR與跨領域面試/HR綜合面試與跨領域考題/技术面 分享.md) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 118****: 🎯 資安工程師履歷包裝、GitHub 專案展示與 HR 常見問答
    🧪 **指定練習/講義**: 閱讀 [`HR问题.md`](../../../08_通用學習與面試庫/05_HR與跨領域面試/HR綜合面試與跨領域考題/HR问题.md) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 60 (Day 119-120): Month 4 階段總復盤與藍隊防禦報告產出**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 119****: 🎯 從代碼審計 ➔ 部署 WAF SecRule 擋截 ➔ SIEM 日誌告警
    🧪 **指定練習/講義**: 攻防閉環演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 120****: 🎯 產出藍隊防禦加固報告、代碼修補建議書與 Writeup 總結
    🧪 **指定練習/講義**: 撰寫 Month 4 結業報告 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義


---

## 🗓️ Month 5 (第 121 ~ 150 天 / Run 61 ~ Run 75): 企業級紅隊綜合攻防與 AWD 對抗演練

### ⚔️ **Run 61 (Day 121-122): DMZ 邊界突破與 Web 權限獲取**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 121****: 🎯 DMZ 邊界網路探測、Nmap 服務指紋識別與入口點掃描
    🧪 **指定練習/講義**: TryHackMe Wreath DMZ Nmap 探測 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 122****: 🎯 Web 漏洞組合利用 (SQLi/Upload) 獲取 DMZ Web 殼權限
    🧪 **指定練習/講義**: TryHackMe Wreath Web 權限獲取 ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構

### ⚔️ **Run 62 (Day 123-124): SOCKS5 代理與二階內網 Pivoting 穿透**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 123****: 🎯 Chisel / MSF 搭建 SOCKS5 代理與二階內網隧道穿透
    🧪 **指定練習/講義**: TryHackMe Pivoting 代理建立 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 124****: 🎯 內網 C 段主機存活探測、fscan 自動化掃描與服務爆破
    🧪 **指定練習/講義**: fscan 內網二階掃描 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 63 (Day 125-126): 內網橫向移動與記憶體 Hash 抓取**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 125****: 🎯 Pass-the-Hash (哈希傳遞) 橫向移動至內網成員伺服器
    🧪 **指定練習/講義**: Impacket `pth-toolkit` 橫向移動 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 126****: 🎯 Mimikatz 抓取內網記憶體 NTLM Hash 與 LSA Secrets 洩露
    🧪 **指定練習/講義**: Mimikatz 記憶體憑據抓取 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 64 (Day 127-128): Kerberoasting 與 Golden Ticket 域控接管**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 127****: 🎯 Kerberoasting 攻擊與 SPN 服務帳號離線 Hash 爆破
    🧪 **指定練習/講義**: Impacket `GetUserSPNs.py` 演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 128****: 🎯 偽造 Golden Ticket (黃金票據) 完全接管 AD 域控制器
    🧪 **指定練習/講義**: Mimikatz `kerberos::golden` 實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 65 (Day 129-130): 企業紅隊攻擊拓撲與評估報告產出**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 129****: 🎯 企業紅隊攻防成果整理、戰果日誌與攻擊路徑拓撲圖繪製
    🧪 **指定練習/講義**: 繪製企業紅隊攻擊拓撲圖 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 130****: 🎯 產出企業級紅隊滲透測試與資產風險評估報告
    🧪 **指定練習/講義**: 撰寫完整紅隊評估報告 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 66 (Day 131-132): AWD 賽事初始化、源碼修補與 WAF 部署**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 131****: 🎯 AWD 戰前準備：SSH 密碼修改、GameBox 源碼備份與權限檢查
    🧪 **指定練習/講義**: AWD 賽前環境初始化 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 132****: 🎯 Web 源碼漏洞修補：SQL 注入與 RCE 危險函數快速過濾
    🧪 **指定練習/講義**: AWD Web 源碼修補實操 ｜ 💡 **帶練指引**: 引導學員推算單引號閉合 `' OR 1=1--` 並手繪 SQL 查詢結構

### ⚔️ **Run 67 (Day 133-134): AWD 流量 WAF 部署與對手 Exp 分析**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 133****: 🎯 部署 AWD 流量監控被動式 WAF 腳本與全網抓包日誌記錄
    🧪 **指定練習/講義**: AWD 通用防禦 WAF 部署 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 134****: 🎯 分析對手攻擊流量標頭、還原對手漏洞利用二進制 Payload
    🧪 **指定練習/講義**: 流量日誌分析與 Exp 還原 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 68 (Day 135-136): AWD 自動化 Batch 批量提交 Flag 腳本**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 135****: 🎯 開發 Python AWD 批量抓 Flag 腳本與 API 自動提交
    🧪 **指定練習/講義**: 撰寫 AWD 批量攻擊腳本 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 136****: 🎯 部署 Cron 自動定時任務全網多目標輪流抓取 Flag 提交
    🧪 **指定練習/講義**: 部署 AWD 全自動 Submit 任務 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 69 (Day 137-138): AWD 高級繞過與後門徹底排查**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 137****: 🎯 應對對手修補：撰寫二階 POP 鏈與混淆繞過 Exp 攻破對手
    🧪 **指定練習/講義**: 撰寫二階混淆繞過 Exp ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 138****: 🎯 GameBox 徹底清查：隱藏 Webshell、Cron 後門與不死馬清除
    🧪 **指定練習/講義**: AWD 不死馬與後門排查 ｜ 💡 **帶練指引**: 發放 PHP 一句話木馬 `<?php @eval($_POST['cmd']);?>` 講義與中國蟻劍連線步驟

### ⚔️ **Run 70 (Day 139-140): 擬真 AWD 實體攻防賽與戰報總結**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 139****: 🎯 參加 2 小時實時模擬 AWD 攻防對抗賽（攻防實時交鋒）
    🧪 **指定練習/講義**: AWD 實況對抗賽 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 140****: 🎯 AWD 對抗賽戰報總結、得分與失分攻擊路徑復盤分析
    🧪 **指定練習/講義**: 撰寫 AWD 賽事復盤報告 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 71 (Day 141-142): 高階 CVE 漏洞重現 (Log4Shell & Spring4Shell)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 141****: 🎯 Log4Shell (CVE-2021-44228) JNDI 注入與 RCE 白箱原理
    🧪 **指定練習/講義**: Vulhub Log4Shell 實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 142****: 🎯 Spring4Shell (CVE-2022-22965) 屬性綁定 RCE 漏洞重現
    🧪 **指定練習/講義**: Vulhub Spring4Shell 實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 72 (Day 143-144): 高階 CVE 漏洞重現 (Shiro & ThinkPHP)**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 143****: 🎯 Apache Shiro (CVE-2016-4437) RememberMe 反序列化重現
    🧪 **指定練習/講義**: Vulhub Shiro 實操 ｜ 💡 **帶練指引**: 演示 ysoserial 工具 CommonsCollections 鏈命令行生成 Exp
  - ****Day 144****: 🎯 ThinkPHP 5.0.23 5.1.x 容器注入 RCE 漏洞分析與驗證
    🧪 **指定練習/講義**: Vulhub ThinkPHP RCE 實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 73 (Day 145-146): 自訂 Python CVE 檢測工具與 Exp 開發**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 145****: 🎯 撰寫獨立 Python CVE 自動化檢測 PoC 工具腳本
    🧪 **指定練習/講義**: 開發 CVE 檢測 PoC  ｜ ＋ picoCTF: AI Foundations (Neuron Meet & 2D Expression) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 146****: 🎯 撰寫獨立 Python 漏洞利用 Exp 腳本並加入命令執行介面
    🧪 **指定練習/講義**: 開發 CVE Exp 利用腳本  ｜ ＋ picoCTF: AI Foundations (Perceptron Train XOR/XNOR) ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 74 (Day 147-148): MSF Ruby Exp 獨立模組開發與封裝**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 147****: 🎯 MSF 模組結構解析：元數據定義、Target 設置與 Payload 對接
    🧪 **指定練習/講義**: 閱讀 MSF Ruby 模組結構 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 148****: 🎯 將新發現 CVE 開發為標準 MSF Ruby 攻擊模組並載入測試
    🧪 **指定練習/講義**: 撰寫並載入 MSF 模組 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 75 (Day 149-150): Month 5 階段考核總結與防禦建議產出**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 149****: 🎯 漏洞重現 Writeup 整理、PoC/Exp 代碼庫維護與驗證
    🧪 **指定練習/講義**: 整理 CVE PoC 代碼庫 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 150****: 🎯 Month 5 階段考核總結、CVE 防禦修補建議書產出
    🧪 **指定練習/講義**: 撰寫 Month 5 總結報告 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義


---

## 🗓️ Month 6 (第 151 ~ 180 天 / Run 76 ~ Run 90): 企業級藍隊 SOC 營運與畢業 Capstone

### ⚔️ **Run 76 (Day 151-152): 藍隊 SOC 資安事件應變 (IR) 啟動與封包保存**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 151****: 🎯 藍隊 SOC 資安事件應變 (IR) 啟動：受害主機隔離與封包保存
    🧪 **指定練習/講義**: CISA IR 應變啟動演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 152****: 🎯 勒索軟體加密副檔名與勒索信樣式排查，識別攻擊家族
    🧪 **指定練習/講義**: 勒索軟體家族特徵分析 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 77 (Day 153-154): 記憶體 Dump 分析與 C2 流量分析**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 153****: 🎯 利用 Volatility 分析受害主機記憶體 Dump，還原惡意進程
    🧪 **指定練習/講義**: Volatility 記憶體還原實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 154****: 🎯 Wireshark 分析勒索軟體 C2 通訊流量與可疑外聯 IP
    🧪 **指定練習/講義**: Wireshark C2 流量解析 ｜ 💡 **帶練指引**: 演示 Wireshark `http.request.method==POST` 顯示過濾語法

### ⚔️ **Run 78 (Day 155-156): 惡意後門排查、根除與防護補強**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 155****: 🎯 排查受害主機後門（Autoruns 機碼、排程工作與服務）
    🧪 **指定練習/講義**: Autoruns 後門排查演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 156****: 🎯 根除木馬後門、更新防毒特徵碼與修補漏洞防護
    🧪 **指定練習/講義**: 惡意木馬根除實操 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 79 (Day 157-158): 系統災難復原與 SIEM/WAF 規則調校**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 157****: 🎯 從離線快照與安全備份中還原資料庫與系統服務
    🧪 **指定練習/講義**: 系統災難復原演練 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 158****: 🎯 調校 SIEM / WAF 防禦告警規則，防止同類漏洞再次引爆
    🧪 **指定練習/講義**: SIEM 告警規則加固 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 80 (Day 159-160): 藍隊 SOC 資安事件處置 (IR) 報告寫作**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 159****: 🎯 撰寫 SOC 藍隊事件應變處置與鑑識報告 (IR Report)
    🧪 **指定練習/講義**: 撰寫完整 IR 鑑識報告 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 160****: 🎯 藍隊資安事件復盤會議報告與防禦改善政策評估
    🧪 **指定練習/講義**: 產出資安復盤改善簡報 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 81 (Day 161-162): 畢業 Capstone（紅隊）：黑盒掃描與入口突破**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 161****: 🎯 終極考核（紅隊）：VulnHub 離線靶機黑盒資訊收集與服務掃描
    🧪 **指定練習/講義**: VulnHub 靶機黑盒 Nmap 掃描 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 162****: 🎯 終極考核（紅隊）：Web 入口點漏洞利用與權限獲取
    🧪 **指定練習/講義**: 獲取 VulnHub 靶機初始 Shell ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 82 (Day 163-164): 畢業 Capstone（紅隊）：提權 Root 與 Writeup**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 163****: 🎯 終極考核（紅隊）：Linux SUID / Kernel 提權獲取 Root 權限
    🧪 **指定練習/講義**: 成功獲取 Root Flag ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 164****: 🎯 終極考核（紅隊）：撰寫完整滲透測試 Writeup 與漏洞評估
    🧪 **指定練習/講義**: 撰寫畢業紅隊 Writeup ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 83 (Day 165-166): 畢業 Capstone（藍隊）：代碼修補與 WAF 防禦**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 165****: 🎯 終極考核（藍隊）：代碼白箱審計與漏洞源碼修補
    🧪 **指定練習/講義**: 白箱源碼漏洞修補 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 166****: 🎯 終極考核（藍隊）：部署 ModSecurity WAF 自訂 SecRule 防禦
    🧪 **指定練習/講義**: 部署 ModSecurity 防禦 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 84 (Day 167-168): 畢業 Capstone（藍隊）：系統加固與報告產出**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 167****: 🎯 終極考核（藍隊）：Windows/Linux 系統安全加固與帳號審查
    🧪 **指定練習/講義**: 執行 CIS 系統安全加固 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 168****: 🎯 終極考核（藍隊）：撰寫藍隊安全加固與修補建議報告
    🧪 **指定練習/講義**: 撰寫畢業藍隊加固報告 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 85 (Day 169-170): 畢業 Capstone：紅藍互審與成績核算**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 169****: 🎯 紅藍攻防結果對比、同儕互審與攻防路徑復盤
    🧪 **指定練習/講義**: 紅藍團隊互審復盤 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 170****: 🎯 終極考核成績核算、成果評分與專案結算
    🧪 **指定練習/講義**: Capstone 終極考核結算 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 86 (Day 171-172): 結業作品集整理與 GitHub Portfolio**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 171****: 🎯 整理 6 個月 Writeup 專案庫與 Markdown 整理編排
    🧪 **指定練習/講義**: 整理 Markdown 題解庫 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 172****: 🎯 打造 GitHub 資安專題展示庫 (Cybersecurity Portfolio)
    🧪 **指定練習/講義**: 建置 GitHub 個人資安作品集 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 87 (Day 173-174): 履歷包裝與技術面試演練**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 173****: 🎯 資安工程師履歷撰寫與項目經歷 STAR 原則包裝
    🧪 **指定練習/講義**: 完成資安工程師履歷初稿 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 174****: 🎯 資安面試技術題（Web, 內網, 防禦, 協議）模擬問答演練
    🧪 **指定練習/講義**: 資安技術面試模擬問答 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 88 (Day 175-176): HR 面試演練與成果簡報製作**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 175****: 🎯 資安面試 HR 綜合面試題與團隊協作問答演練
    🧪 **指定練習/講義**: HR 行為面試題模擬問答 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 176****: 🎯 讀書會結業專題成果發表簡報 (Slides) 製作
    🧪 **指定練習/講義**: 製作 6 個月結業簡報 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 89 (Day 177-178): 結業 Live Demo 與擬真技術口試**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 177****: 🎯 讀書會結業專題成果實機演示 (Live Demo) 預演
    🧪 **指定練習/講義**: 結業專題 Live Demo 預演 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 178****: 🎯 模擬資安工程師技術口試 (Mock Technical Interview)
    🧪 **指定練習/講義**: 接受資安專家模擬口試 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

### ⚔️ **Run 90 (Day 179-180): 6 個月讀書會圓滿結業與就業啟航**
- 🔗 **CyLab / 線上專題**: CyLab 綜合實戰 / 離線靶場對接
- 📌 **每日實操與關卡細節**:
  - ****Day 179****: 🎯 6 個月讀書會成長復盤與頒發結業證書
    🧪 **指定練習/講義**: 讀書會成長復盤與檢討 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義
  - ****Day 180****: 🎯 圓滿結業與資安求職正式啟航
    🧪 **指定練習/講義**: 6 個月讀書會圓滿結業 ｜ 💡 **帶練指引**: 講解關鍵技術原理並提供隨堂練習講義

