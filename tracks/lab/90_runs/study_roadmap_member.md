# 🚀 資訊安全 6 個月攻防讀書會路線圖 (Member Study Group Edition)

> [!IMPORTANT]
> **當前版本**: `v5.8` (成員發布版)
> **發布日期**: 2026-08-08
> **核心架構與規則**: 
> 1. **時間軸**: 每 2 天為 1 個 Run（半年 180 天共 90 個 Run）。
> 2. **線上資源對接**: 每日課表對接 PortSwigger Academy、pwnable.kr、CryptoHack、Root-Me 等公開平台。
> 3. **前置需求**: 入會前須自備 Linux CLI 與 Docker 基本環境。
> 4. 🏆 **金盾獎專項衝刺 (9/10～10/10)**: 本學期參賽隊伍在初賽前一個月，可優先切換至專屬實戰衝刺課表 ➔ [`30days_sprint_roadmap.md`](../golden_shield_sprint/30days_sprint_roadmap.md)！

---

## 🤝 讀書會運作流程與成員公約 (Operating Rules & Conventions)

> [!TIP]
> **輕鬆學習、互相交流的日常運作默契**：

1. 🕒 **定時線上聚會 (每 Run 第一天 22:00)**：
   - 每兩天晚上 10 點線上聚會。會議開頭簡短聊聊上一 Run 的卡關經驗或有趣發現（短短幾分鐘輕鬆分享即可）。
2. 📝 **個人實操 Writeup 筆記**：
   - 將每日解題與實操過程寫成簡短 Markdown 筆記（Writeup），並整理提交至個人的筆記軟體（Obsidian, Notion, HackMD 等）。
3. ✍️ **會議紀要輪值（簡短回顧）**：
   - 每次聚會由成員輪流簡單列幾點重點紀錄，方便大家事後回顧討論回憶（輕鬆紀錄、無需壓力）。


## 🛠️ Day 0: 讀書會入會前置自備門檻 (Prerequisites)

- **作業系統環境**：Kali Linux / Ubuntu 虛擬機器或 Windows WSL2。
- **容器環境**：Docker Desktop 與 `docker-compose`。
- **必備命令列**：Linux 基本指令（`cd`, `ls`, `grep`, `chmod`, `curl`, `ssh`）。

---

## 🗓️ Month 1 (第 1 ~ 32 天 / Run 1 ~ Run 16): 攻防雙軌基礎與工具鏈入門

#### ⚔️ **Run 1 (Day 1-2): HTTP 協定原理與 Burp Suite 代理抓包**
🌐 **線上專題**: [picoCTF: General Skills](https://learn.cylabacademy.org/learning-paths/14) ｜ [Beginner's Guide](https://learn.cylabacademy.org/learning-paths/18) ｜ [PortSwigger Access Control](https://portswigger.net/web-security/access-control)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 1** (08/07) | HTTP 請求與回應標頭分析 (GET/POST/Header/Status Code) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Insp3ct0r (ID: 367)](https://learn.cylabacademy.org/library?search=Insp3ct0r)<br>🌐 **PortSwigger**: • [Lab: Intercepting Web Requests via Burp](https://portswigger.net/burp)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [what's a net cat? (ID: 156)](https://learn.cylabacademy.org/library?search=what%27s%20a%20net%20cat%3F)<br>• [Super SSH (ID: 424)](https://learn.cylabacademy.org/library?search=Super%20SSH)<br>🌐 **PortSwigger**: • [Lab: Modifying Web Requests](https://portswigger.net/burp/proxy) |
| **Day 2** (08/08) | Burp Suite 代理截獲、Repeater 重放與 POST 欄位修改 | 同 Day 1 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 2 (Day 3-4): SQL Injection 基礎與萬能密碼登入繞過**
🌐 **線上專題**: [picoCTF: Irish Name Repo Series](https://learn.cylabacademy.org/learning-paths/7) ｜ [PortSwigger SQLi](https://portswigger.net/web-security/sql-injection)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 3** (08/09) | SQL 查詢語法剖析、單引號 `'` 閉合原理與注入點判斷 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Irish-Name-Repo 1 (ID: 548)](https://learn.cylabacademy.org/library?search=Irish-Name-Repo%201)<br>🌐 **PortSwigger**: • [Lab: Retrieval of hidden data](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Irish-Name-Repo 2 (ID: 550)](https://learn.cylabacademy.org/library?search=Irish-Name-Repo%202) & [Irish-Name-Repo 3 (ID: 552)](https://learn.cylabacademy.org/library?search=Irish-Name-Repo%203)<br>🌐 **PortSwigger**: • [Lab: Subverting login logic](https://portswigger.net/web-security/sql-injection/lab-login-bypass) |
| **Day 4** (08/10) | `' OR 1=1--` 萬能密碼成因與 POST 表單登入繞過原始碼分析 | 同 Day 3 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 3 (Day 5-6): 命令執行 (RCE) 與路徑遍歷 (Path Traversal)**
🌐 **線上專題**: [PortSwigger OS Command Injection](https://portswigger.net/web-security/os-command-injection) ｜ [PortSwigger File Path Traversal](https://portswigger.net/web-security/file-path-traversal)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 5** (08/11) | OS 命令注入原理與 Linux/Windows 命令拼接符 (` ; `, ` & `, ` && `, ` \| `, ` \|\| `) | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [ping-cmd (ID: 757)](https://learn.cylabacademy.org/library?search=ping-cmd)<br>🌐 **PortSwigger**: • [Lab: OS command injection, simple case](https://portswigger.net/web-security/os-command-injection/lab-simple)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: File path traversal, simple case](https://portswigger.net/web-security/file-path-traversal/lab-simple) |
| **Day 6** (08/12) | 路徑遍歷 (Path Traversal) 與 `../` 讀取 `/etc/passwd` | 同 Day 5 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 4 (Day 7-8): Wireshark 網路流量分析與協定防禦**
🌐 **線上專題**: [picoCTF: Forensics in CTF's](https://learn.cylabacademy.org/learning-paths/16) ｜ [Root-Me Network](https://www.root-me.org/en/Challenges/Network/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 7** (08/13) | Wireshark 基礎介面、網路介面選擇與網絡卡混雜模式捕獲<br>🎥 本地觀看：`1-WireShark简介.mp4` ~ `3-过滤器使用.mp4` ＋ `WireShark操作練習-2024.docx` | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Wireshark doo dooo do doo... (ID: 432)](https://learn.cylabacademy.org/library?search=Wireshark%20doo%20dooo%20do%20doo...)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Trivial Flag Transfer Protocol (ID: 434)](https://learn.cylabacademy.org/library?search=Trivial%20Flag%20Transfer%20Protocol) |
| **Day 8** (08/14) | Wireshark 顯示過濾語法 (`ip.addr`) 與 HTTP 追蹤流分析<br>🎥 本地觀看：`6-TCP协议.mp4` ~ `8-实战.mp4` ＋ 分析 `SQLInjection.pcapng` | 同 Day 7 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 5 (Day 9-10): 任意檔案上傳與 Webshell 木馬權維**
🌐 **線上專題**: [PortSwigger File Upload](https://portswigger.net/web-security/file-upload)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 9** (08/15) | 任意檔案上傳原理、前端 JS 驗證繞過與 Content-Type 偽造 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Remote code execution via web shell upload](https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload) |
| **Day 10** (08/16) | 一句話木馬編寫與中國蟻劍 (AntSword) 連線 Webshell | 同 Day 9 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 6 (Day 11-12): x86/x64 彙編基礎與 GDB / Pwntools 環境建立**
🌐 **線上專題**: [picoCTF: Low Level Binary Intro](https://learn.cylabacademy.org/learning-paths/2) ｜ [pwn.college: Computing 101](https://pwn.college/computing-101)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 11** (08/17) | x86/x64 彙編暫存器 (EAX, ESP, EBP, EIP) 與記憶體堆疊結構 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Bit-O-Asm-1 (ID: 125)](https://learn.cylabacademy.org/library?search=Bit-O-Asm-1) ~ [Bit-O-Asm-4 (ID: 138)](https://learn.cylabacademy.org/library?search=Bit-O-Asm-4)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [GDB baby step 1 (ID: 142)](https://learn.cylabacademy.org/library?search=GDB%20baby%20step%201) ~ [GDB baby step 4 (ID: 158)](https://learn.cylabacademy.org/library?search=GDB%20baby%20step%204) |
| **Day 12** (08/18) | Linux GDB 偵錯程式指令 (`gdb ./pwn`) 與 Pwntools 腳本撰寫 | 同 Day 11 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 7 (Day 13-14): HITCON 2026 Wargame 實戰演練與賽後 Writeup 覆盤 (Special Event)**
🌐 **賽事平台**: [HITCON CTF / Wargame](https://ctf.hitcon.org/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 13** (08/19) | HITCON 2026 Wargame 賽事實戰衝刺（Web / Pwn / Reverse / Crypto 題型突破） | 🎯 **實戰任務**:<br>🚩 **HITCON Wargame**: 全隊衝刺解題，即時記錄解題封包與卡關點 |
| **Day 14** (08/20) | 賽後 Writeup 整理、官方題解覆盤與全領域盲點歸納 | 🎯 **覆盤任務**:<br>📝 提交個人 Writeup 至筆記軟體並對照官方題解還原 Root Cause |

---

#### ⚔️ **Run 8 (Day 15-16): XSS 跨站腳本與 CSRF 身分偽造攻擊**
🌐 **線上專題**: [PortSwigger XSS](https://portswigger.net/web-security/cross-site-scripting) & [PortSwigger CSRF](https://portswigger.net/web-security/csrf)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 15** (08/21) | XSS 跨站腳本成因、Reflected / Stored / DOM XSS 與 Cookie 竊取 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Reflected XSS into HTML context](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Stored XSS into anchor href](https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded)<br>• [Lab: CORS with basic origin reflection](https://portswigger.net/web-security) |
| **Day 16** (08/22) | CSRF 跨站請求偽造原理、PoC 自動提交表單與 Token 防禦 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: CSRF vulnerability with no defenses](https://portswigger.net/web-security/csrf/lab-no-defenses) |

---

> [!NOTE]
> ☕ **階段自習與緩衝 (08/23 ~ 08/24)**: XSS / CSRF 與前階段漏洞自主實踐、Writeup 筆記整理與 PortSwigger 關卡補齊。

---

#### ⚔️ **Run 9 (Day 17-18): Ghidra / IDA Pro 靜態逆向工程基礎**
🌐 **線上專題**: [Root-Me Cracking](https://www.root-me.org/en/Challenges/Cracking/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 17** (08/25) | 逆向工程導論、靜態分析概念與 PE / ELF 可執行檔結構 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Safe Opener 1 (ID: 513)](https://learn.cylabacademy.org/library?search=Safe%20Opener%201) & [Safe Opener 2 (ID: 515)](https://learn.cylabacademy.org/library?search=Safe%20Opener%202)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [vault-door-training (ID: 472)](https://learn.cylabacademy.org/library?search=vault-door-training) |
| **Day 18** (08/26) | Ghidra / IDA Pro 反編譯 C 虛擬碼與 Serial 驗證邏輯逆向 | 同 Day 21 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 10 (Day 19-20): 越權漏洞 (IDOR) 與 Cookie/Session 會話劫持**
🌐 **線上專題**: [picoCTF: General Skills](https://learn.cylabacademy.org/learning-paths/14) ｜ [Beginner's Guide](https://learn.cylabacademy.org/learning-paths/18) ｜ [PortSwigger Access Control](https://portswigger.net/web-security/access-control)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 19** (08/27) | IDOR 越權原理與平行越權修改 `id=1001` 檢視他人信件 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Unprotected admin functionality](https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: User ID controlled bypass of access controls](https://portswigger.net/web-security)<br>• [Lab: Username enumeration via different responses](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses) |
| **Day 20** (08/28) | 垂直越權、URL 許可權控制繞過與 Session 劫持攻擊 | 同 Day 21 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 11 (Day 21-22): Linux / Windows 本地許可權提升 (PrivEsc)**
🌐 **線上專題**: [OverTheWire Bandit](https://overthewire.org/wargames/bandit/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 21** (08/29) | Linux SUID 提權原理與 `find / -perm -4000` 尋找特權 binary | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Magikarp Ground Mission (ID: 189)](https://learn.cylabacademy.org/library?search=Magikarp%20Ground%20Mission) / [First Find (ID: 320)](https://learn.cylabacademy.org/library?search=First%20Find)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Big Zip (ID: 322)](https://learn.cylabacademy.org/library?search=Big%20Zip) / [strings it (ID: 163)](https://learn.cylabacademy.org/library?search=strings%20it) / [plumbing (ID: 156)](https://learn.cylabacademy.org/library?search=plumbing) |
| **Day 22** (08/30) | MySQL UDF 提權原理與 Windows 服務路徑弱點提權實戰 | 同 Day 21 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 12 (Day 23-24): SSTI 模板注入與 PHP/Java 反序列化**
🌐 **線上專題**: [PortSwigger SSTI](https://portswigger.net/web-security/server-side-template-injection) ｜ [PortSwigger Deserialization](https://portswigger.net/web-security/deserialization)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 23** (08/31) | Flask Jinja2 SSTI 原理與 `{{config}}` / `__class__` 變數洩露 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Basic server-side template injection (ERB)](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Basic SSTI in Tornado](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic-tornado) |
| **Day 24** (09/01) | PHP 魔術方法 `__wakeup()` 觸發與 Java 物件反序列化 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Modifying serialized objects](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Modifying serialized data types](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types) |

---

#### ⚔️ **Run 13 (Day 25-26): PWN 堆疊溢位 (Stack Overflow) 緩衝區溢位**
🌐 **線上專題**: [pwnable.kr](http://pwnable.kr/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 25** (09/02) | PWN 堆疊溢位 (Stack Overflow) 記憶體佈局與 NOP Sled 原理 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [buffer overflow 0 (ID: 184)](https://learn.cylabacademy.org/library?search=buffer%20overflow%200) / [Local Target (ID: 188)](https://learn.cylabacademy.org/library?search=Local%20Target)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [buffer overflow 1 (ID: 192)](https://learn.cylabacademy.org/library?search=buffer%20overflow%201) / [Picker I (ID: 118)](https://learn.cylabacademy.org/library?search=Picker%20I) ~ [Picker IV (ID: 180)](https://learn.cylabacademy.org/library?search=Picker%20IV) |
| **Day 26** (09/03) | `ret2text` 篡改 EIP/RIP 執行流與 Pwntools 自動化 Exp 撰寫 | 同 Day 23 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 14 (Day 27-28): CryptoHack 密碼學基礎 (RSA / AES 演算法原理)**
🌐 **線上專題**: [picoCTF: Cryptography Intro](https://learn.cylabacademy.org/learning-paths/17) ｜ [Substitution Series](https://learn.cylabacademy.org/learning-paths/12) ｜ [CryptoHack](https://cryptohack.org/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 27** (09/04) | Base64、ASCII、XOR 位元運算與對稱加密基礎觀念 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [2warm (ID: 100)](https://learn.cylabacademy.org/library?search=2warm) / [Warmed Up (ID: 172)](https://learn.cylabacademy.org/library?search=Warmed%20Up) / [caesar (ID: 16)](https://learn.cylabacademy.org/library?search=caesar)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [interencdec (ID: 418)](https://learn.cylabacademy.org/library?search=interencdec)<br>• [Mind your Ps and Qs (ID: 27)](https://learn.cylabacademy.org/library?search=Mind%20your%20Ps%20and%20Qs) / [Mini RSA (ID: 18)](https://learn.cylabacademy.org/library?search=Mini%20RSA) / [rsa_oracle (ID: 29)](https://learn.cylabacademy.org/library?search=rsa_oracle) |
| **Day 28** (09/05) | RSA 公私鑰數學原理 (p, q, n, e, d) 與大數分解陷阱 | 同 Day 27 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 15 (Day 29-30): 內網滲透 (SOCKS5 隧道 / Pivoting / AD 域控攻防)**
🌐 **線上專題**: [TryHackMe Active Directory](https://tryhackme.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 29** (09/06) | MSF / Chisel 搭建 SOCKS5 代理隧道與 Pivoting 內網穿透 | 按專題課後練習進度 |
| **Day 30** (09/07) | Active Directory 域控基礎、Kerberos 驗證流程與黃金票據 | 按專題課後練習進度 |

---

#### ⚔️ **Run 16 (Day 31-32): Month 1 階段總複盤與黑盒 VulnHub 靶機通關**
🌐 **線上專題**: [VulnHub](https://www.vulnhub.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 31** (09/08) | 黑盒 VulnHub 靶機 (Os-hackNos) 資訊收集與 Nmap 服務掃描 | 按專題課後練習進度 |
| **Day 32** (09/09) | 靶機漏洞組合利用、獲取 Root 許可權與 Writeup 撰寫 | 按專題課後練習進度 |

---

## 🗓️ Month 2 (第 33 ~ 62 天 / Run 17 ~ Run 31): 核心漏洞深造與高級攻防

#### ⚔️ **Run 17 (Day 33-34): SQL Injection 盲注與 OOB DNSLog 帶外注入**
🌐 **線上專題**: [PortSwigger Blind SQLi](https://portswigger.net/web-security/sql-injection/blind)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 33** | 布林盲注與時間盲注 (`sleep(3)`, `ascii(substr())`) 原理與推算腳本 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Blind SQL injection with conditional responses](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Blind SQL injection with time delays](https://portswigger.net/web-security/sql-injection/blind/lab-time-delays)<br>• [Lab: Syntax injection in NoSQL](https://portswigger.net/web-security) |
| **Day 34** | DNSLog Out-of-band (OOB) 帶外注入與 `LOAD_FILE()` 資料外排 | 同 Day 31 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 18 (Day 35-36): SQL Injection WAF 繞過與拖庫實戰**
🌐 **線上專題**: [PortSwigger SQLi Filter Bypass](https://portswigger.net/web-security/sql-injection)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 35** | 大小寫混淆、雙寫繞過與 `/*!50000union*/` 行內註釋繞過 WAF | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: SQL injection UNION attack, determining column count](https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: SQL injection UNION attack, retrieving data](https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text) |
| **Day 36** | `mysqldump` 資料庫備份與 MySQL UDF (`sys_eval`) 特權執行 | 同 Day 33 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 19 (Day 37-38): Sqlmap 工具高階引數與 Tamper 腳本編寫**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 37** | Sqlmap `-r req.txt`, `--level 5 --risk 3`, `--os-shell` 抓包拖庫引數 | 按專題課後練習進度 |
| **Day 38** | 自訂 Sqlmap `tamper` 混淆腳本編寫與安全狗 (Safedog) 繞過 | 按專題課後練習進度 |

---

#### ⚔️ **Run 20 (Day 39-40): 任意檔案上傳高階繞過與解析漏洞**
🌐 **線上專題**: [PortSwigger File Upload](https://portswigger.net/web-security/file-upload)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 39** | 雙重副檔名 (`.php.jpg`)、`0x00` 截斷與 `.htaccess` 繞過 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Web shell upload via Content-Type restriction bypass](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Web shell upload via path traversal](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal) |
| **Day 40** | Apache / Nginx 解析漏洞 (`/1.php/1.jpg`) 與 PUT 寫入木馬 | 同 Day 37 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 21 (Day 41-42): LFI 本地檔案包含與 RFI 遠端檔案包含**
🌐 **線上專題**: [PortSwigger Path Traversal](https://portswigger.net/web-security/file-path-traversal)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 41** | LFI 配合 `php://filter` 讀取原始碼與 `php://input` 執行木馬 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: File path traversal, traversal sequences blocked with absolute path](https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: File path traversal, traversal sequences stripped non-recursively](https://portswigger.net/web-security/file-path-traversal/lab-sequences-stripped-non-recursively) |
| **Day 42** | Session 檔案包含與 Log 日誌注入 (`/var/log/apache2/access.log`) GETSHELL | 同 Day 39 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 22 (Day 43-44): DOM-based XSS 與 JS 加密解密逆向**
🌐 **線上專題**: [PortSwigger DOM XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 43** | DOM XSS Source & Sink (`location.search`, `document.write`) 剖析 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [vault-door-1 (ID: 474)](https://learn.cylabacademy.org/library?search=vault-door-1) ~ [vault-door-4 (ID: 480)](https://learn.cylabacademy.org/library?search=vault-door-4)<br>🌐 **PortSwigger**: • [Lab: DOM XSS using web message](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [vault-door-5 (ID: 481)](https://learn.cylabacademy.org/library?search=vault-door-5) ~ [vault-door-8 (ID: 487)](https://learn.cylabacademy.org/library?search=vault-door-8)<br>🌐 **PortSwigger**: • [Lab: Client-side prototype pollution via DOM XSS](https://portswigger.net/web-security) |
| **Day 44** | 前端 JS 混淆程式碼逆向與 Chrome DevTools 中斷點除錯解密 | 同 Day 41 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 23 (Day 45-46): SSRF 高階利用與 127.0.0.1 內網探測**
🌐 **線上專題**: [PortSwigger SSRF](https://portswigger.net/web-security/ssrf)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 45** | SSRF 配合 `gopher://` 與 `dict://` 協定攻擊內網 Redis | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Basic SSRF against the local server](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Host header SSRF](https://portswigger.net/web-security/host-header/exploiting/lab-host-header-ssrf-via-flawed-request-parsing) |
| **Day 46** | SSRF 繞過 127.0.0.1 過濾 (DNS Rebinding, 十六進位 IP 表示) | 同 Day 43 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 24 (Day 47-48): 業務邏輯漏洞 (支付篡改、驗證碼繞過、JSON 劫持)**
🌐 **線上專題**: [PortSwigger Logic Flaws](https://portswigger.net/web-security/logic-flaws)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 47** | 支付金額篡改、負數下單與驗證碼可預測/未失效漏洞 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Excessive trust in client-side controls](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Limit overrun race condition](https://portswigger.net/web-security/race-conditions/lab-race-conditions-limit-overrun)<br>• [Lab: Authentication bypass via OAuth implicit flow](https://portswigger.net/web-security/oauth/lab-oauth-authentication-bypass-via-oauth-implicit-flow) |
| **Day 48** | JSONP 跨域資料劫持與 CORS 跨域資源共享配置缺陷利用 | 同 Day 45 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 25 (Day 49-50): Linux 許可權提升進階 (Kernel Exploit, Dirty COW, Sudo)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 49** | Linux 核心溢位漏洞利用 (Dirty COW 臟牛, PTRACE_TRACEME) | 按專題課後練習進度 |
| **Day 50** | Sudo 許可權配置漏洞 (`sudo -l`) 與 Linux Cron Jobs 定時任務提權 | 按專題課後練習進度 |

---

#### ⚔️ **Run 26 (Day 51-52): Windows 許可權提升進階 (Bypass UAC, Token Impersonation)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 51** | Windows Server 2008R2 溢位提權與 LPK 劫持提權 | 按專題課後練習進度 |
| **Day 52** | Token 冒充 (JuicyPotato, RoguePotato) 與 Zend 反彈 Shell | 按專題課後練習進度 |

---

#### ⚔️ **Run 27 (Day 53-54): PHP 反序列化 POP 鏈與 PHPGGC 實戰**
🌐 **線上專題**: [PortSwigger Deserialization](https://portswigger.net/web-security/deserialization)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 53** | PHP POP 鏈 (Property-Oriented Programming) 魔術方法構造 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Modifying serialized objects](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Modifying serialized data types](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types) |
| **Day 54** | PHPGGC 自動化 Payload 生成器與 Phar 反序列化利用 | 同 Day 51 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 28 (Day 55-56): Java 反序列化 (ysoserial, Shiro, Fastjson)**
🌐 **線上專題**: [PortSwigger Java Deserialization](https://portswigger.net/web-security/deserialization)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 55** | Java `readObject()` 漏洞成因、ysoserial 工具與 CC 鏈分析 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Exploiting Java deserialization with Apache Commons](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-java-deserialization-with-apache-commons) |
| **Day 56** | Apache Shiro RememberMe 金鑰硬編碼與 Fastjson autoType 繞過 Exp | 同 Day 53 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 29 (Day 57-58): 中介軟體與框架安全 (Apache, Nginx, Tomcat, Spring)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 57** | Tomcat 弱口令 Manager 部署 WAR 包 GetShell 與 CVE-2017-12615 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: JWT authentication bypass via unverified signature](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Web cache poisoning with unkeyed header](https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-header) |
| **Day 58** | Spring Core RCE (Spring4Shell) 與 ThinkPHP5 5.0.23 RCE 漏洞剖析 | 同 Day 55 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 30 (Day 59-60): AWVS & Xray 自動化漏洞聯動掃描**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 59** | AWVS 14 漏洞自動化掃描器配置與黑盒主動掃描 | 按專題課後練習進度 |
| **Day 60** | Burp Suite + Xray 被動式掃描器代理聯動挖掘 | 按專題課後練習進度 |

---

#### ⚔️ **Run 31 (Day 61-62): Month 2 階段復盤與黑盒 CMS 靶場實戰 (YXCMS / WordPress)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 61** | YXCMS 1.4.7 離線靶場部署與黑盒滲透測試 | 按專題課後練習進度 |
| **Day 62** | WordPress 綜合檢測與 Month 2 階段 Writeup 總結 | 按專題課後練習進度 |

---

## 🗓️ Month 3 (第 61 ~ 90 天 / Run 31 ~ Run 45): 二進位制 PWN、逆向工程與紅隊內網滲透#### ⚔️ **Run 32 (Day 63-64): Linux GDB 除錯與 Pwntools 自動化控制**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 63** | Linux GDB 偵錯程式高階指令 (`gdb ./pwn`, `x/20wx $esp`) 記憶體剖析 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Ready Gladiator 0 (ID: 577)](https://learn.cylabacademy.org/library?search=Ready%20Gladiator%200)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Ready Gladiator 1 (ID: 579)](https://learn.cylabacademy.org/library?search=Ready%20Gladiator%201) & [Ready Gladiator 2 (ID: 581)](https://learn.cylabacademy.org/library?search=Ready%20Gladiator%202) |
| **Day 64** | Pwntools Python 庫 (`process()`, `remote()`) 自動化 Exp 腳本撰寫 | 同 Day 61 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 33 (Day 65-66): PWN ROP 鏈 (Return-Oriented Programming) 實戰**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 65** | Linux NX 記憶體保護與 ROPgadget 搜尋 `pop rdi; ret` Gadget | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Guessing Game 1 (ID: 568)](https://learn.cylabacademy.org/library?search=Guessing%20Game%201)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Guessing Game 2 (ID: 570)](https://learn.cylabacademy.org/library?search=Guessing%20Game%202) |
| **Day 66** | 64 位元 ROP 鏈構造與 `ret2libc` 洩露 libc 位址 | 同 Day 63 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 34 (Day 67-68): PWN 格式化字串漏洞與任意記憶體讀寫**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 67** | 格式化字串漏洞 (`printf`) 記憶體洩露原理 | 按專題課後練習進度 |
| **Day 68** | 利用 `%n` 任意寫入與 GOT 表改寫 | 按專題課後練習進度 |

---

#### ⚔️ **Run 35 (Day 69-70): Ghidra / IDA Pro 逆向工程與 C/C++ 反編譯分析**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 69** | Ghidra 靜態分析 C/C++ 結構體與指標排列微觀剖析 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Investigative Reversing 0 (ID: 524)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%200) ~ [Investigative Reversing 2 (ID: 528)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%202)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Investigative Reversing 3 (ID: 530)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%203) & [Investigative Reversing 4 (ID: 532)](https://learn.cylabacademy.org/library?search=Investigative%20Reversing%204) |
| **Day 70** | 控制流圖 (CFG) 導覽與 Binary Patch 修改跳過註冊驗證 | 同 Day 67 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 36 (Day 71-72): Android APK 逆向與 Smali 程式碼動態除錯**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 71** | Android APK 結構解析、`apktool` 解包與 Smali 閱讀 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [droids0 (ID: 588)](https://learn.cylabacademy.org/library?search=droids0) / [droids1 (ID: 590)](https://learn.cylabacademy.org/library?search=droids1) / [droids2 (ID: 592)](https://learn.cylabacademy.org/library?search=droids2)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [droids3 (ID: 594)](https://learn.cylabacademy.org/library?search=droids3) / [droids4 (ID: 596)](https://learn.cylabacademy.org/library?search=droids4) |
| **Day 72** | JADX-GUI 動態除錯 Android APK 與 驗證邏輯 Patch | 同 Day 69 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 37 (Day 73-74): 內網資產探測 (Nmap, Masscan, fscan)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 73** | Nmap 內網 C 段主機存活探測 (`nmap -sn`) 與服務識別 | 按專題課後練習進度 |
| **Day 74** | fscan 自動化內網掃描與弱口令爆破 (SSH, RDP, MySQL) | 按專題課後練習進度 |

---

#### ⚔️ **Run 38 (Day 75-76): 橫向移動 (Pass-the-Hash, WMI, PsExec)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 75** | Pass-the-Hash (雜湊傳遞) 攻擊與 Mimikatz 抓取 NTLM Hash | 按專題課後練習進度 |
| **Day 76** | 利用 WMI (`wmiexec.py`) 與 PsExec 實現無檔案橫向執行 | 按專題課後練習進度 |

---

#### ⚔️ **Run 39 (Day 77-78): Cobalt Strike C2 部署與 Listener / Stager 控權**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 77** | Cobalt Strike Teamserver 搭建與 Client 連線 | 按專題課後練習進度 |
| **Day 78** | CS Listener 設定、生成 Beacon Stager 與許可權維持 | 按專題課後練習進度 |

---

#### ⚔️ **Run 40 (Day 79-80): Active Directory 域控攻擊 (Kerberoasting, AS-REP Roasting)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 79** | Active Directory 域控架構與 Kerberos 認證流程 | 按專題課後練習進度 |
| **Day 80** | Kerberoasting 攻擊與 AS-REP Roasting 離線爆破 Hash | 按專題課後練習進度 |

---

#### ⚔️ **Run 41 (Day 81-82): Golden Ticket & Silver Ticket 域控接管**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 81** | Golden Ticket (黃金票據) 偽造與 `krbtgt` Hash 控制域控 | 按專題課後練習進度 |
| **Day 82** | Silver Ticket (白銀票據) 偽造與 MSSQL / CIFS 服務切入 | 按專題課後練習進度 |

---

#### ⚔️ **Run 42 (Day 83-84): 免殺與 Shellcode 載入器 (Bypass AV)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 83** | 免殺技術：Shellcode Loader 異或 / AES 特徵加密解密 | 按專題課後練習進度 |
| **Day 84** | 利用 Windows API (`VirtualAlloc`, `RtlMoveMemory`) 繞過記憶體掃描 | 按專題課後練習進度 |

---

#### ⚔️ **Run 43 (Day 85-86): Linux / Windows 許可權維持與後門 (Persistence)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 85** | Linux 許可權維持：SSH 公鑰寫入、Crontab 定時任務與 SUID 後門 | 按專題課後練習進度 |
| **Day 86** | Windows 許可權維持：機碼自啟動、排程工作與服務後門 | 按專題課後練習進度 |

---

#### ⚔️ **Run 44 (Day 87-88): Metasploit (MSF) 高階模組與 Exp 開發**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 87** | MSF `msfvenom` 生成 Payload 與 Handler 監聽設定 | 按專題課後練習進度 |
| **Day 88** | MSF 自訂 Ruby 漏洞利用模組 (Exp) 寫作規範與 API 對接 | 按專題課後練習進度 |

---

#### ⚔️ **Run 45 (Day 89-90): 內網縱深防禦與痕跡清理**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 89** | 攻擊痕跡清理：Linux 命令歷史 (`history -c`) 與 Windows 事件日誌 | 按專題課後練習進度 |
| **Day 90** | 內網網路隔離 (VLAN, ACL, Zero Trust) 策略評估與紅隊復盤 | 按專題課後練習進度 |

---

#### ⚔️ **Run 46 (Day 91-92): Month 3 階段總復盤與內網 AD 域控攻防靶場通關**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 91** | 內網 AD 靶場：Web 入口點突破 ➔ SOCKS5 代理穿透進入內網 | 按專題課後練習進度 |
| **Day 92** | 橫向移動至域控 (DC) 獲取 Domain Admin 與 Writeup 撰寫 | 按專題課後練習進度 |

---

## 🗓️ Month 4 (第 91 ~ 120 天 / Run 46 ~ Run 60): 程式碼審計、安全開發與藍隊防禦#### ⚔️ **Run 47 (Day 93-94): PHP 程式碼審計 (危險函式追蹤 ＋ AST/CFG 語意分析 ＋ Source-to-Sink 污點追蹤)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 93** | PHP 程式碼審計基礎：危險函式 (`eval`, `exec`) 定位與 Seay 工具 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [PortSwigger Code Audit Walkthroughs](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [AST/CFG Code Semantics Analysis](https://portswigger.net/web-security) |
| **Day 94** | PHP 變數追蹤法 (Sinks to Sources) 與 SQLi / XSS 白箱發現 | 同 Day 91 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 48 (Day 95-96): Java 程式碼審計 (Spring/Servlet 審計 ＋ 語意分析 ＋ 資料流分析 Data-flow Analysis)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 95** | Java Web 架構 (Filter, Servlet, Spring MVC) 與 Controller 入口 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [PortSwigger Java Vulnerability Analysis](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Source-to-Sink Data-flow Taint Analysis](https://portswigger.net/web-security) |
| **Day 96** | Java SQL 拼接 (MyBatis `${}` vs `#{}`) 與 `Runtime.exec()` RCE | 同 Day 93 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 49 (Day 97-98): 開源 CMS 程式碼審計專案實戰 (YXCMS 白箱審計 ＋ 複雜資料流與淨化函式過濾驗證)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 97** | YXCMS 1.4.7 解包、路由解析與 SQL 查詢構造器白箱分析 | 按專題課後練習進度 |
| **Day 98** | YXCMS 前臺 SQL 注入與後臺寫入 GetShell 驗證與 0day 挖掘 | 按專題課後練習進度 |

---

#### ⚔️ **Run 50 (Day 99-100): Python 安全開發 (自動化掃描工具開發)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 99** | Python Requests 模組：Session 維持、代理設定與自訂 Header | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [PW Crack 1 (ID: 245)](https://learn.cylabacademy.org/library?search=PW%20Crack%201) ~ [PW Crack 3 (ID: 247)](https://learn.cylabacademy.org/library?search=PW%20Crack%203)<br>• [fixme1.py (ID: 240)](https://learn.cylabacademy.org/library?search=fixme1.py)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [PW Crack 4 (ID: 248)](https://learn.cylabacademy.org/library?search=PW%20Crack%204) & [PW Crack 5 (ID: 611)](https://learn.cylabacademy.org/library?search=PW%20Crack%205)<br>• [fixme2.py (ID: 241)](https://learn.cylabacademy.org/library?search=fixme2.py) |
| **Day 100** | Python `threading` 多執行緒目錄 Fuzz 與漏洞掃描器編寫 | 同 Day 97 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 51 (Day 101-102): 藍隊防禦與護網日誌分析 (Web 攻擊日誌 ＋ 統計特徵選擇 Statistical Feature Selection)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 101** | Apache / Nginx Access Log 剖析與 Web 攻擊特徵日誌搜尋 | 按專題課後練習進度 |
| **Day 102** | 利用 Linux `grep`, `awk`, `uniq -c` 極速統計可疑 IP 紀錄 | 按專題課後練習進度 |

---

#### ⚔️ **Run 52 (Day 103-104): SIEM 與 ELK 集中日誌過濾 (巨量日誌過濾 ＋ CatBoost 機器學習流量分類)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 103** | SIEM 概念與 ELK (Elasticsearch, Logstash, Kibana) 集中日誌 | 按專題課後練習進度 |
| **Day 104** | 撰寫 Kibana KQL 告警查詢語法與 Web 爆破實時告警 | 按專題課後練習進度 |

---

#### ⚔️ **Run 53 (Day 105-106): Sysmon 與 Windows 日誌分析 (特徵工程 ＋ SHAP 可解釋性分析依賴圖視覺化)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 105** | Windows 事件檢視器關鍵 Event ID (4624, 4625, 4672) 判讀 | 按專題課後練習進度 |
| **Day 106** | Sysmon 配置檔編寫、程序建立與網路連線告警捕捉 | 按專題課後練習進度 |

---

#### ⚔️ **Run 54 (Day 107-108): 記憶體取證 (Volatility 分析 Dump 檔案)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 107** | 記憶體取證導論、Volatility 2.6/3 安裝與 Profile 選取 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Sleuthkit Intro (ID: 504)](https://learn.cylabacademy.org/library?search=Sleuthkit%20Intro) / [information (ID: 89)](https://learn.cylabacademy.org/library?search=information) / [Verify (ID: 54)](https://learn.cylabacademy.org/library?search=Verify)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Sleuthkit Apprentice (ID: 506)](https://learn.cylabacademy.org/library?search=Sleuthkit%20Apprentice)<br>• [Disk, disk, sleuth! (ID: 416)](https://learn.cylabacademy.org/library?search=Disk%2C%20disk%2C%20sleuth%21) & [Disk, disk, sleuth! II (ID: 418)](https://learn.cylabacademy.org/library?search=Disk%2C%20disk%2C%20sleuth%21%20II)<br>• [Glory of the Garden (ID: 409)](https://learn.cylabacademy.org/library?search=Glory%20of%20the%20Garden) / [Scan Surprise (ID: 444)](https://learn.cylabacademy.org/library?search=Scan%20Surprise) |
| **Day 108** | Volatility 實戰：`pslist`, `netscan`, `dumpfiles` 還原木馬 | 同 Day 105 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 55 (Day 109-110): 勒索軟體與木馬應變處置 (IR Incident Response)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 109** | 藍隊資安事件應變處置 (IR) 標準流程 (準備 ➔ 檢測 ➔ 根除) | 按專題課後練習進度 |
| **Day 110** | 惡意程序與後門排查工具 (Process Hacker, TCPView, Autoruns) | 按專題課後練習進度 |

---

#### ⚔️ **Run 56 (Day 111-112): 密碼學進階 (ECC, Diffie-Hellman, SHA-256)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 111** | ECC 橢圓曲線加密與 Diffie-Hellman 金鑰交換數學原理 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [PowerAnalysis: Warmup (ID: 36)](https://learn.cylabacademy.org/library?search=PowerAnalysis%3A%20Warmup)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [PowerAnalysis: Part 1 (ID: 38)](https://learn.cylabacademy.org/library?search=PowerAnalysis%3A%20Part%201)<br>• [corrupt-key-2 (ID: 287)](https://learn.cylabacademy.org/library?search=corrupt-key-2) |
| **Day 112** | SHA-256 / MD5 雜湊長度擴充套件攻擊與 HashPump 工具實操 | 同 Day 109 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 57 (Day 113-114): 隱寫術 (Steganography: Stegsolve, OutGuess)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 113** | 隱寫術導論、Stegsolve 工具使用、圖片 LSB 最低有效位提取 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [St3g0 (ID: 425)](https://learn.cylabacademy.org/library?search=St3g0) / [What Lies Within (ID: 427)](https://learn.cylabacademy.org/library?search=What%20Lies%20Within)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [m00nwalk (ID: 539)](https://learn.cylabacademy.org/library?search=m00nwalk) & [m00nwalk2 (ID: 541)](https://learn.cylabacademy.org/library?search=m00nwalk2) / [investigation_encoded_1 (ID: 559)](https://learn.cylabacademy.org/library?search=investigation_encoded_1) |
| **Day 114** | 音訊隱寫 (Audacity 頻譜圖) 與 OutGuess / Steghide 密碼破解 | 同 Day 111 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 58 (Day 115-116): 網頁安全防禦加固與 WAF 規則撰寫**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 115** | ModSecurity WAF 安裝配置與 OWASP CRS 部署調校 | 🎯 **必解關卡**:<br>🌐 **PortSwigger**: • [Lab: Obfuscating WAF bypass techniques](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-most-tags-and-attributes-blocked) |
| **Day 116** | 撰寫自訂 SecRule 規則防禦 SQLi, XSS 與 RCE 命令執行 | 同 Day 113 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 59 (Day 117-118): 資安筆試題庫解析 (觀念題/協議題/防禦題)**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 117** | TCP/IP 三向交握、TLS 1.3 握手流程、HTTP 狀態碼筆試題 | 按專題課後練習進度 |
| **Day 118** | 同源策略 (SOP)、CORS、Cookie 屬性 (`SameSite`) 筆試真題 | 按專題課後練習進度 |

---

#### ⚔️ **Run 60 (Day 119-120): 資安面試真題與履歷包裝**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 119** | 滲透測試專案經歷 STAR 原則描述與漏洞復盤表達 | 按專題課後練習進度 |
| **Day 120** | 資安工程師履歷包裝、GitHub 專案展示與 HR 常見問答 | 按專題課後練習進度 |

---

#### ⚔️ **Run 61 (Day 121-122): Month 4 階段總復盤與藍隊防禦報告產出**

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 121** | 從程式碼審計 ➔ 部署 WAF SecRule 擋截 ➔ SIEM 日誌告警 | 按專題課後練習進度 |
| **Day 122** | 產出藍隊防禦加固報告、程式碼修補建議書與 Writeup 總結 | 按專題課後練習進度 |

---

## 🗓️ Month 5 (第 121 ~ 150 天 / Run 61 ~ Run 75): 企業級紅隊綜合攻防與 AWD 對抗演練#### ⚔️ **Run 62 (Day 123-124): DMZ 邊界突破與 Web 許可權獲取**
🌐 **線上實戰**: [TryHackMe Enterprise Network](https://tryhackme.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 123** | DMZ 邊界網路探測、Nmap 服務指紋識別與入口點掃描 | 按專題課後練習進度 |
| **Day 124** | Web 漏洞組合利用 (SQLi/Upload) 獲取 DMZ Web 殼許可權 | 按專題課後練習進度 |

---

#### ⚔️ **Run 63 (Day 125-126): SOCKS5 代理與二階內網 Pivoting 穿透**
🌐 **線上實戰**: [TryHackMe Pivoting](https://tryhackme.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 125** | Chisel / MSF 搭建 SOCKS5 代理與二階內網隧道穿透 | 按專題課後練習進度 |
| **Day 126** | 內網 C 段主機存活探測、fscan 自動化掃描與服務爆破 | 按專題課後練習進度 |

---

#### ⚔️ **Run 64 (Day 127-128): 內網橫向移動與記憶體 Hash 抓取**
🌐 **工具庫**: [Impacket Tools](https://github.com/fortra/impacket)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 127** | Pass-the-Hash (雜湊傳遞) 橫向移動至內網成員伺服器 | 按專題課後練習進度 |
| **Day 128** | Mimikatz 抓取內網記憶體 NTLM Hash 與 LSA Secrets 洩露 | 按專題課後練習進度 |

---

#### ⚔️ **Run 65 (Day 129-130): Kerberoasting 與 Golden Ticket 域控接管**
🌐 **線上實戰**: [TryHackMe Attacktive Directory](https://tryhackme.com/room/attacktivedirectory)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 129** | Kerberoasting 攻擊與 SPN 服務帳號離線 Hash 爆破 | 按專題課後練習進度 |
| **Day 130** | 偽造 Golden Ticket (黃金票據) 完全接管 AD 域控制器 | 按專題課後練習進度 |

---

#### ⚔️ **Run 66 (Day 131-132): 企業紅隊攻擊拓撲與評估報告產出**
🌐 **報告範本**: [Cybersecurity Red Team Report Guide](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 131** | 企業紅隊攻防成果整理、戰果日誌與攻擊路徑拓撲圖繪製 | 按專題課後練習進度 |
| **Day 132** | 產出企業級紅隊滲透測試與資產風險評估報告 | 按專題課後練習進度 |

---

#### ⚔️ **Run 67 (Day 133-134): AWD 賽事初始化、原始碼修補與 WAF 部署**
🌐 **開源平台**: [AWD-Predator Platform](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 133** | AWD 戰前準備：SSH 密碼修改、GameBox 原始碼備份與許可權檢查 | 按專題課後練習進度 |
| **Day 134** | Web 原始碼漏洞修補：SQL 注入與 RCE 危險函式快速過濾 | 按專題課後練習進度 |

---

#### ⚔️ **Run 68 (Day 135-136): AWD 流量 WAF 部署與對手 Exp 分析**
🌐 **開源平台**: [AWD Defense WAF](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 135** | 部署 AWD 流量監控被動式 WAF 腳本與全網抓包日誌記錄 | 按專題課後練習進度 |
| **Day 136** | 分析對手攻擊流量標頭、還原對手漏洞利用二進位制 Payload | 按專題課後練習進度 |

---

#### ⚔️ **Run 69 (Day 137-138): AWD 自動化 Batch 批次提交 Flag 腳本**
🌐 **開源平台**: [AWD Auto Submit Tools](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 137** | 開發 Python AWD 批次抓 Flag 腳本與 API 自動提交 | 按專題課後練習進度 |
| **Day 138** | 部署 Cron 自動定時任務全網多目標輪流抓取 Flag 提交 | 按專題課後練習進度 |

---

#### ⚔️ **Run 70 (Day 139-140): AWD 高階繞過與後門徹底排查**
🌐 **開源平台**: [AWD Advanced Payload Guide](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 139** | 應對對手修補：撰寫二階 POP 鏈與混淆繞過 Exp 攻破對手 | 按專題課後練習進度 |
| **Day 140** | GameBox 徹底清查：隱藏 Webshell、Cron 後門與不死馬清除 | 按專題課後練習進度 |

---

#### ⚔️ **Run 71 (Day 141-142): 擬真 AWD 實體攻防賽與戰報總結**
🌐 **線上平台**: [AWD Online Arena](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 141** | 參加 2 小時實時模擬 AWD 攻防對抗賽（攻防實時交鋒） | 按專題課後練習進度 |
| **Day 142** | AWD 對抗賽戰報總結、得分與失分攻擊路徑復盤分析 | 按專題課後練習進度 |

---

#### ⚔️ **Run 72 (Day 143-144): 高階 CVE 漏洞重現 (Log4Shell & Spring4Shell)**
🌐 **線上環境**: [Vulhub Vulnerability Environment](https://vulhub.org/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 143** | Log4Shell (CVE-2021-44228) JNDI 注入與 RCE 白箱原理 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Live Art (ID: 293)](https://learn.cylabacademy.org/library?search=Live%20Art)<br>🌐 **PortSwigger**: • [Lab: Exploiting XXE to retrieve files](https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-retrieve-files)<br>🚀 **延伸挑戰**:<br>🌐 **PortSwigger**: • [Lab: Exploiting XXE to perform SSRF attacks](https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-perform-ssrf) |
| **Day 144** | Spring4Shell (CVE-2022-22965) 屬性繫結 RCE 漏洞重現 | 同 Day 141 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 73 (Day 145-146): 高階 CVE 漏洞重現 (Shiro & ThinkPHP)**
🌐 **線上環境**: [Vulhub Vulnerability Repository](https://vulhub.org/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 145** | Apache Shiro (CVE-2016-4437) RememberMe 反序列化重現 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Clouds (ID: 288)](https://learn.cylabacademy.org/library?search=Clouds)<br>🌐 **PortSwigger**: • [Lab: HTTP request smuggling, basic CL.TE vulnerability](https://portswigger.net/web-security/request-smuggling/lab-basic-cl-te)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [SaaS (ID: 312)](https://learn.cylabacademy.org/library?search=SaaS) / [zero_to_hero (ID: 323)](https://learn.cylabacademy.org/library?search=zero_to_hero)<br>🌐 **PortSwigger**: • [Lab: HTTP request smuggling, basic TE.CL vulnerability](https://portswigger.net/web-security/request-smuggling/lab-basic-te-cl) |
| **Day 146** | ThinkPHP 5.0.23 5.1.x 容器注入 RCE 漏洞分析與驗證 | 同 Day 143 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 74 (Day 147-148): 自訂 Python CVE 檢測工具與 Exp 開發**
🌐 **官方文件**: [Python Security Scripting Guide](https://docs.python.org/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 147** | 撰寫獨立 Python CVE 自動化檢測 PoC 工具腳本 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [Trust But Verify (ID: 783)](https://learn.cylabacademy.org/library?search=Trust%20But%20Verify) / [Neuron Meet 0 (ID: 771)](https://learn.cylabacademy.org/library?search=Neuron%20Meet%200)<br>🌐 **PortSwigger**: • [Lab: Exploiting LLM APIs with indirect prompt injection](https://portswigger.net/web-security)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Perceptron Train XOR (ID: 782)](https://learn.cylabacademy.org/library?search=Perceptron%20Train%20XOR) / [Perceptron Train XNOR (ID: 781)](https://learn.cylabacademy.org/library?search=Perceptron%20Train%20XNOR) |
| **Day 148** | 撰寫獨立 Python 漏洞利用 Exp 腳本並加入命令執行介面 | 同 Day 145 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 75 (Day 149-150): MSF Ruby Exp 獨立模組開發與封裝**
🌐 **官方教學**: [Metasploit Module Development](https://www.offsec.com/metasploit-unleashed/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 149** | MSF 模組結構解析：後設資料定義、Target 設定與 Payload 對接 | 🎯 **必解關卡**:<br>🚩 **picoCTF**: • [riscy business (ID: 305)](https://learn.cylabacademy.org/library?search=riscy%20business)<br>🚀 **延伸挑戰**:<br>🚩 **picoCTF**: • [Checkpass (ID: 307)](https://learn.cylabacademy.org/library?search=Checkpass) |
| **Day 150** | 將新發現 CVE 開發為標準 MSF Ruby 攻擊模組並載入測試 | 同 Day 147 關卡（延續實操與延伸挑戰） |

---

#### ⚔️ **Run 76 (Day 151-152): Month 5 階段考核總結與防禦建議產出**
🌐 **復盤報告**: [Cybersecurity Assessment Summary](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 151** | 漏洞重現 Writeup 整理、PoC/Exp 程式碼庫維護與驗證 | 按專題課後練習進度 |
| **Day 152** | Month 5 階段考核總結、CVE 防禦修補建議書產出 | 按專題課後練習進度 |

---

## 🗓️ Month 6 (第 151 ~ 180 天 / Run 76 ~ Run 90): 企業級藍隊 SOC 營運、應變處置與畢業專案#### ⚔️ **Run 77 (Day 153-154): 藍隊 SOC 資安事件應變 (IR) 啟動與封包儲存 (結合 CatBoost 惡意封包過濾)**
🌐 **CISA 指南**: [CISA Incident Handling Guide](https://www.cisa.gov/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 153** | 藍隊 SOC 資安事件應變 (IR) 啟動：受害主機隔離與封包儲存 | 按專題課後練習進度 |
| **Day 154** | 勒索軟體加密副檔名與勒索信樣式排查，識別攻擊家族 | 按專題課後練習進度 |

---

#### ⚔️ **Run 78 (Day 155-156): 記憶體 Dump 分析與 C2 流量分析 (結合 SHAP 特徵依賴視覺化解析 C2 行為)**
🌐 **線上平台**: [Root-Me Memory Forensics](https://www.root-me.org/en/Challenges/Forensic/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 155** | 利用 Volatility 分析受害主機記憶體 Dump，還原惡意程序 | 按專題課後練習進度 |
| **Day 156** | Wireshark 分析勒索軟體 C2 通訊流量與可疑外聯 IP | 按專題課後練習進度 |

---

#### ⚔️ **Run 79 (Day 157-158): 惡意後門排查、根除與防護補強**
🌐 **工具文件**: [Microsoft Autoruns Docs](https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 157** | 排查受害主機後門（Autoruns 機碼、排程工作與服務） | 按專題課後練習進度 |
| **Day 158** | 根除木馬後門、更新防毒特徵碼與修補漏洞防護 | 按專題課後練習進度 |

---

#### ⚔️ **Run 80 (Day 159-160): 系統災難復原與 SIEM/WAF 規則調校**
🌐 **官方指南**: [OWASP Incident Response Recovery](https://owasp.org/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 159** | 從離線快照與安全備份中還原資料庫與系統服務 | 按專題課後練習進度 |
| **Day 160** | 調校 SIEM / WAF 防禦告警規則，防止同類漏洞再次引爆 | 按專題課後練習進度 |

---

#### ⚔️ **Run 81 (Day 161-162): 藍隊 SOC 資安事件處置 (IR) 報告寫作**
🌐 **報告範本**: [SANS IR Report Template](https://www.sans.org/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 161** | 撰寫 SOC 藍隊事件應變處置與鑑識報告 (IR Report) | 按專題課後練習進度 |
| **Day 162** | 藍隊資安事件復盤會議報告與防禦改善政策評估 | 按專題課後練習進度 |

---

#### ⚔️ **Run 82 (Day 163-164): 畢業 Capstone（紅隊）：黑盒掃描與入口突破**
🌐 **線上靶場**: [VulnHub Official Site](https://www.vulnhub.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 163** | 終極考核（紅隊）：VulnHub 離線靶機黑盒資訊收集與服務掃描 | 按專題課後練習進度 |
| **Day 164** | 終極考核（紅隊）：Web 入口點漏洞利用與許可權獲取 | 按專題課後練習進度 |

---

#### ⚔️ **Run 83 (Day 165-166): 畢業 Capstone（紅隊）：提權 Root 與 Writeup**
🌐 **線上靶場**: [VulnHub Offsec Machines](https://www.vulnhub.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 165** | 終極考核（紅隊）：Linux SUID / Kernel 提權獲取 Root 許可權 | 按專題課後練習進度 |
| **Day 166** | 終極考核（紅隊）：撰寫完整滲透測試 Writeup 與漏洞評估 | 按專題課後練習進度 |

---

#### ⚔️ **Run 84 (Day 167-168): 畢業 Capstone（藍隊）：程式碼修補與 WAF 防禦**
🌐 **官方專案**: [OWASP ModSecurity CRS](https://coreruleset.org/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 167** | 終極考核（藍隊）：程式碼白箱審計與漏洞原始碼修補 | 按專題課後練習進度 |
| **Day 168** | 終極考核（藍隊）：部署 ModSecurity WAF 自訂 SecRule 防禦 | 按專題課後練習進度 |

---

#### ⚔️ **Run 85 (Day 169-170): 畢業 Capstone（藍隊）：系統加固與報告產出**
🌐 **防禦指南**: [CIS Benchmarks Guide](https://www.cisecurity.org/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 169** | 終極考核（藍隊）：Windows/Linux 系統安全加固與帳號審查 | 按專題課後練習進度 |
| **Day 170** | 終極考核（藍隊）：撰寫藍隊安全加固與修補建議報告 | 按專題課後練習進度 |

---

#### ⚔️ **Run 86 (Day 171-172): 畢業 Capstone：紅藍互審與成績核算**
🌐 **審查指南**: [Peer Review Security Evaluation](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 171** | 紅藍攻防結果對比、同儕互審與攻防路徑復盤 | 按專題課後練習進度 |
| **Day 172** | 終極考核成績核算、成果評分與專案結算 | 按專題課後練習進度 |

---

#### ⚔️ **Run 87 (Day 173-174): 結業作品集整理與 GitHub Portfolio**
🌐 **作品集參考**: [GitHub Cybersecurity Portfolio](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 173** | 整理 6 個月 Writeup 專案庫與 Markdown 整理編排 | 按專題課後練習進度 |
| **Day 174** | 打造 GitHub 資安專題展示庫 (Cybersecurity Portfolio) | 按專題課後練習進度 |

---

#### ⚔️ **Run 88 (Day 175-176): 履歷包裝與技術面試演練**
🌐 **面試指南**: [Cybersecurity Interview Prep](https://github.com/swisskyrepo/PayloadsAllTheThings)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 175** | 資安工程師履歷撰寫與專案經歷 STAR 原則包裝 | 按專題課後練習進度 |
| **Day 176** | 資安面試技術題（Web, 內網, 防禦, 協議）模擬問答演練 | 按專題課後練習進度 |

---

#### ⚔️ **Run 89 (Day 177-178): HR 面試演練與成果簡報製作**
🌐 **面試指南**: [HR Behavioral Interview Guide](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 177** | 資安面試 HR 綜合面試題與團隊協作問答演練 | 按專題課後練習進度 |
| **Day 178** | 讀書會結業專題成果發表簡報 (Slides) 製作 | 按專題課後練習進度 |

---

#### ⚔️ **Run 90 (Day 179-180): 結業 Live Demo 與擬真技術口試**
🌐 **展示指南**: [Cybersecurity Project Demo Guide](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 179** | 讀書會結業專題成果實機演示 (Live Demo) 預演 | 按專題課後練習進度 |
| **Day 180** | 模擬資安工程師技術口試 (Mock Technical Interview) | 按專題課後練習進度 |

---

#### ⚔️ **Run 91 (Day 181-182): 6 個月讀書會圓滿結業與就業啟航**
🌐 **畢業總結**: [Cybersecurity Career Roadmap](https://github.com/)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習關卡 (Lab / Challenge) |
| :--- | :--- | :--- |
| **Day 181** | 6 個月讀書會成長復盤與頒發結業證書 | 按專題課後練習進度 |
| **Day 182** | 圓滿結業與資安求職正式啟航 | 按專題課後練習進度 |