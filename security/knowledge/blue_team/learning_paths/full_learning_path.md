# 🎯 北極星雙目標：全國賽奪牌 → DEVCORE 實習

> **目標 1：全國賽**（數位鑑識 + 安全強化 + CTF I/II + AD 內網攻防）
> **目標 2：DEVCORE 實習**（PortSwigger 全套 + 網頁開發 + 伺服器建置 + Binary/Reverse）
>
> 學習節奏：**每兩天一個循環**
> - 🟢 Day 1（Input）：啃教材 / 筆記 / Lab
> - 🔴 Day 2（Output）：解題 / 實作 / 寫 writeup

---

> [!NOTE]
> **內部離線教材索引說明**：本文檔中標註之「本地資料」、「本地資源」（如 `01_Web安全/`、`06_網路安全與數位取證/` 等）均為實驗室內部離線教材庫目錄，完整 25 個題源與 394 個子模組對照清單請參見 👉 [【資料來源總索引 (sources_index.md)】](../../../../tracks/lab/90_runs/sources_index.md)。

## 技能地圖：全國賽 × DEVCORE 重疊分析

| 技能模組 | 全國賽 | DEVCORE | 本地離線資料（詳見 [sources_index.md](../../../../tracks/lab/90_runs/sources_index.md)） |
|----------|--------|---------|----------|
| Web 漏洞（SQLi/XSS/SSRF/RCE） | CTF I Day2 AM | Research/Red Team 必要 | ✅ `01_Web安全/` |
| PortSwigger 全部 Lab | — | Red Team 硬性門檻 | ❌ 需線上完成 |
| Binary / PWN（BOF/ROP） | CTF I Day2 AM | Binary/Research 必要 | ✅ `02_二進制/` |
| Reverse（Ghidra/IDA） | CTF I Day2 AM | Research 必要 | ✅ `02_二進制/03` |
| 數位鑑識（pcap/mem/disk） | Day1 AM 整份卷 | Forensics 技能 | ✅ `06_取證/` |
| AD 攻防（Kerberoasting/DPAPI） | CTF II Day2 PM | Red Team 加分 | ✅ `04_系統內網/07` |
| 安全強化 Hardening | Day1 PM 整份卷 | Red Team 概念 | ✅ `07_藍隊/` |
| 網頁開發建站（Flask/PHP） | — | Red Team 必要 | ❌ 最大缺口 |
| 伺服器建置（Nginx/AD） | — | Red Team 必要 | ❌ 最大缺口 |
| JVM heap dump / Java profiling | CTF I Day2 AM | — | ❌ 需補充 |
| 內網 pivoting（DMZ→內網） | CTF II Day2 PM | — | ✅ `04_系統內網/06` |

---

## 第 1 個月：全局速通（15-Run Global Blitz）

> 目標：先把所有技術領域過一遍，建立全局視野，不要有盲區。
> 每 Run = 2 天。共 30 天 15 Run。

---

### Run 1（Day 1–2）HTTP 抓包 / Burp Suite 基礎

**目標：** CTF I Web、DEVCORE 必備工具熟悉
**Day 2 任務：** Burp 改 Header 繞過登入，抓 JWT / Cookie

**本地資源：**
- `01_Web安全/11_Web漏洞自動化掃描/試聽課福利_BurpSuite`
- `01_Web安全/11_Web漏洞自動化掃描/教主Kali與Python_BurpSuite滲透`
- `01_Web安全/02_HTTP網路協定與抓包/暗月Web紅隊_HTTP協定詳解`
- `01_Web安全/11_Web漏洞自動化掃描/CTF常見題型解析_BurpSuite`
- `01_Web安全/11_Web漏洞自動化掃描/HackTools_burpsuite`

**線上資源：**
- PortSwigger Burp Suite 官方教學：https://portswigger.net/burp/documentation/desktop
- TryHackMe：Burp Suite 模組

---

### Run 2（Day 3–4）SQLi 全套 + 盲注腳本

**目標：** CTF I / DEVCORE OWASP Top 10
**Day 2 任務：** Python 寫時間盲注 Exp 拖庫

**本地資源：**
- `01_Web安全/06_SQL注入與命令執行/暗月Web紅隊_MySQL注入`
- `01_Web安全/06_SQL注入與命令執行/原書籍_SQL注入Sqlmap`
- `01_Web安全/06_SQL注入與命令執行/Web攻防實戰_SQL注入基礎`
- `01_Web安全/06_SQL注入與命令執行/Web攻防實戰_SQL注入WAF繞過`
- `01_Web安全/06_SQL注入與命令執行/暗月Web紅隊_DNSLog無回顯注入`
- `01_Web安全/CTF題型解析_SQL盲注`
- `01_Web安全/CTF常見題型解析_SQL注入`

**線上資源：**
- PortSwigger SQL Injection Labs（全部做完）
- SQLi-labs 靶機（GitHub）
- PicoCTF：SQL Injection 題目

---

### Run 3（Day 5–6）RCE + 檔案上傳繞過

**目標：** CTF I / DEVCORE
**Day 2 任務：** 繞過 upload-labs 前 10 關，無字母 RCE

**本地資源：**
- `01_Web安全/07_檔案上傳與包含漏洞/暗月Web紅隊_任意檔案上傳`
- `01_Web安全/07_檔案上傳與包含漏洞/Web攻防實戰_FileUpload任意檔案上傳`
- `01_Web安全/06_SQL注入與命令執行/Web攻防教程_RCE命令`
- `01_Web安全/CTF題型解析_檔案上傳繞過`
- `01_Web安全/CTF題型解析_RCE命令執行`
- `01_Web安全/51CTO奪旗賽_任意檔案上傳PUT漏洞`
- `01_Web安全/51CTO奪旗賽_RCE_命令執行`

**線上資源：**
- upload-labs：https://github.com/c0ny1/upload-labs
- PortSwigger File Upload Vulnerabilities Labs

---

### Run 4（Day 7–8）XSS / CSRF / SSRF + Gopher 打內網

**目標：** CTF I
**Day 2 任務：** SSRF Gopher 協議打內網 Redis 寫 WebShell

**本地資源：**
- `01_Web安全/08_客戶端與業務邏輯漏洞/Web攻防教程_XSS攻擊`
- `01_Web安全/08_客戶端與業務邏輯漏洞/Web攻防實戰_XSS`
- `01_Web安全/08_客戶端與業務邏輯漏洞/Web攻防實戰_SSRF漏洞`
- `01_Web安全/08_客戶端與業務邏輯漏洞/暗月Web紅隊_CSRF`
- `01_Web安全/CTF題型解析_SSRF服務端請求偽造`
- `01_Web安全/CTF題型解析_XXE`

**線上資源：**
- PortSwigger XSS / CSRF / SSRF Labs
- CyberChef：https://gchq.github.io/CyberChef/

---

### Run 5（Day 9–10）PHP / Java 反序列化

**目標：** CTF I
**Day 2 任務：** ysoserial 打 Shiro 拿 Shell

**本地資源：**
- `01_Web安全/09_反序列化與組件漏洞/暗月Web紅隊_PHP反序列化漏洞`
- `01_Web安全/09_反序列化與組件漏洞/試聽課福利_Java反序列化`
- `01_Web安全/09_反序列化與組件漏洞/試聽課福利_PHPGGC`
- `01_Web安全/09_反序列化與組件漏洞/CTF題型解析_PHP反序列化魔術方法`
- `01_Web安全/10_中間件與框架安全/試聽課福利_Shiro漏洞利用Exp`
- `01_Web安全/09_反序列化與組件漏洞/CTF題型解析_SSTI模板注入(Flask)`

**線上資源：**
- ysoserial：https://github.com/frohoff/ysoserial
- PHPGGC：https://github.com/ambionics/phpggc

---

### Run 6（Day 11–12）Nmap 掃描 + 未授權服務利用

**目標：** CTF II
**Day 2 任務：** MSF 打未授權 Redis / Mongo 拿 Shell

**本地資源：**
- `06_網路安全與數位取證/02_端口掃描與Nmap工具/試聽課福利_Nmap網絡端口掃描`
- `06_網路安全與數位取證/02_端口掃描與Nmap工具/教主Kali與Python_Nmap網路掃描`
- `04_系統與內網安全/02_未授權服務與RCE利用/暗月Web紅隊_Redis未授權`
- `04_系統與內網安全/02_未授權服務與RCE利用/CTF題型解析_Redis未授權`
- `04_系統與內網安全/01_主機掃描與探測/Metasploit魔鬼訓練營_主機刺探`

**線上資源：**
- Metasploit Unleashed：https://www.metasploitunleashed.com/
- TryHackMe：Nmap 模組

---

### Run 7（Day 13–14）Linux / Windows 權限提升

**目標：** CTF II
**Day 2 任務：** SUID 提權 + MSF meterpreter getuid → system

**本地資源：**
- `04_系統與內網安全/03_權限提升/工具使用_Linux提權`
- `04_系統與內網安全/03_權限提升/工具使用_Windows提權`
- `04_系統與內網安全/03_權限提升/暗月Web紅隊_Linux_SUID提權`
- `04_系統與內網安全/03_權限提升/暗月Web紅隊_MOF提權`
- `04_系統與內網安全/03_權限提升/Metasploit魔鬼訓練營_系統權限提升`
- `04_系統與內網安全/03_權限提升/暗月Web紅隊_Windows溢出提權`

**線上資源：**
- GTFOBins（Linux 提權）：https://gtfobins.github.io/
- LOLBAS（Windows 提權）：https://lolbas-project.github.io/
- HackTricks 提權章節：https://book.hacktricks.xyz/

---

### Run 8（Day 15–16）密碼爆破 + 隧道穿透

**目標：** CTF II
**Day 2 任務：** Hydra 爆 SSH + Chisel 建 SOCKS5 隧道進內網

**本地資源：**
- `04_系統與內網安全/04_密碼爆破與字典/外校_Hydra密碼爆破`
- `04_系統與內網安全/04_密碼爆破與字典/暗月Web紅隊_Hydra服務爆破`
- `04_系統與內網安全/06_隧道與穿透/暗月Web紅隊_Socket內網隧道`
- `04_系統與內網安全/06_隧道與穿透/暗月Web紅隊_SSH內網穿透`
- `04_系統與內網安全/06_隧道與穿透/暗月Web紅隊_多層內網隧道穿透`

**線上資源：**
- Chisel：https://github.com/jpillora/chisel
- ligolo-ng（更現代的隧道工具）：https://github.com/nicocha30/ligolo-ng

---

### Run 9（Day 17–18）AD 域控入門（Kerberoasting / Pass-the-Hash）

**目標：** CTF II / DEVCORE
**Day 2 任務：** impacket GetUserSPNs → hashcat 破票 → 橫向

**本地資源：**
- `04_系統與內網安全/07_內網橫向與域控/暗月Web紅隊_內網橫向滲透`
- `04_系統與內網安全/07_內網橫向與域控/Metasploit魔鬼訓練營_HASH憑證`
- `04_系統與內網安全/07_內網橫向與域控/HW_域控`

**線上資源：**
- impacket 文檔：https://github.com/fortra/impacket
- TryHackMe：Active Directory Basics
- HackTricks AD 攻擊鏈：https://book.hacktricks.xyz/windows-hardening/active-directory-methodology

---

### Run 10（Day 19–20）x86/x64 彙編 + 棧溢出 BOF

**目標：** CTF I Bin / DEVCORE Binary 組
**Day 2 任務：** pwntools 寫 ret2win Exp，nc 連靶機拿 flag

**本地資源：**
- `02_二進制與逆向/01_彙編語言與二進制基礎/Z0FCourse_Assembly彙編語言`
- `02_二進制與逆向/02_PWN記憶體破壞漏洞利用/ctf_PWN棧溢出漏洞`
- `02_二進制與逆向/02_PWN記憶體破壞漏洞利用/ctf_PWN解題基礎入門`
- `02_二進制與逆向/02_PWN記憶體破壞漏洞利用/ctf_PWNExploit編寫教程`
- `02_二進制與逆向/02_PWN記憶體破壞漏洞利用/ctf_PWN教材`

**線上資源：**
- pwn.college：https://pwn.college/
- OverTheWire Narnia：https://overthewire.org/wargames/narnia/
- pwntools 文檔：https://docs.pwntools.com/

---

### Run 11（Day 21–22）ROP chain + PIE / ASLR 繞過

**目標：** CTF I Bin / DEVCORE
**Day 2 任務：** ROPgadget 找 gadget，自動化 pwntools 腳本打遠端

**本地資源：**
- `02_二進制與逆向/02_PWN記憶體破壞漏洞利用/ctf_PWN使用者態與ROP利用`
- `02_二進制與逆向/02_PWN記憶體破壞漏洞利用/ctf_PWN格式化字串漏洞`
- `02_二進制與逆向/02_PWN記憶體破壞漏洞利用/ctf_PWN高級利用`
- `02_二進制與逆向/HackTools_pwn`
- `02_二進制與逆向/HackTools_pwn_tools`

**線上資源：**
- ROPgadget：https://github.com/JonathanSalwan/ROPgadget
- pwnable.kr：http://pwnable.kr/（Run 11 開始刷）

---

### Run 12（Day 23–24）IDA Pro / Ghidra 靜態逆向

**目標：** CTF I Reverse / DEVCORE
**Day 2 任務：** Crackme 逆向找正確序號 / 演算法

**本地資源：**
- `02_二進制與逆向/03_靜態反彙編與動態逆向/Z0FCourse_逆向工程全套講義`
- `02_二進制與逆向/03_靜態反彙編與動態逆向/Z0FCourse_逆向分析工具`
- `02_二進制與逆向/ctf_逆向工程`
- `02_二進制與逆向/ctf_逆向工程賽題`
- `02_二進制與逆向/ctf_Crackme賽題`
- `02_二進制與逆向/ctf_PWN二進制專題_逆向工程RE`

**線上資源：**
- Ghidra（免費）：https://ghidra-sre.org/
- crackmes.one：https://crackmes.one/
- Reverse Engineering 教學：https://0xinfection.github.io/reversing/

---

### Run 13（Day 25–26）RSA / AES 密碼弱點 + 隱寫

**目標：** CTF I Crypto / Misc
**Day 2 任務：** Python 解 RSA 弱點 + 圖片 LSB 隱寫提取 flag

**本地資源：**
- `03_密碼學與隱寫/01_密碼學與演算法/ctf_競賽通用_密碼學RSA分析`
- `03_密碼學與隱寫/01_密碼學與演算法/CTF常見題型解析_密碼學入門`
- `03_密碼學與隱寫/02_雜項隱寫術/ctf_隱寫術`
- `03_密碼學與隱寫/02_雜項隱寫術/ctf_隱寫術解題技巧`
- `03_密碼學與隱寫/03_加解密工具腳本/ctf_常用密碼學與隱寫腳本`
- `03_密碼學與隱寫/ctf_AES密碼學動畫演示`

**線上資源：**
- CryptoHack：https://cryptohack.org/（RSA/AES/ECC 漸進式解題）
- CyberChef：https://gchq.github.io/CyberChef/
- RsaCtfTool：https://github.com/RsaCtfTool/RsaCtfTool

---

### Run 14（Day 27–28）Wireshark PCAP + Volatility 記憶體鑑識

**目標：** 全國賽 Day1 AM
**Day 2 任務：** 分析 pcap 還原 SQLi 攻擊鏈 + Volatility 重建 Timeline

**本地資源：**
- `06_網路安全與數位取證/03_流量分析PCAP/原書籍_Wireshark流量分析`
- `06_網路安全與數位取證/工具使用_Wireshark流量監聽`
- `06_網路安全與數位取證/03_流量分析PCAP/試聽課福利_Wireshark流量分析`
- `06_網路安全與數位取證/03_流量分析PCAP/ctf_流量分析`
- `06_網路安全與數位取證/03_流量分析PCAP/CTF常見題型解析_流量`
- `06_網路安全與數位取證/03_流量分析PCAP/ctf_流量分析賽題`
- `06_網路安全與數位取證/06_流量與日誌腳本/ctf_常用流量與日誌分析腳本`

**線上資源：**
- Volatility 3 文檔：https://volatility3.readthedocs.io/
- PicoCTF Forensics 題目
- CTF-Wiki Forensics：https://ctf-wiki.org/forensics/

---

### Run 15（Day 29–30）Autopsy 磁碟鑑識 + Linux 加固

**目標：** 全國賽 Day1 AM / Day1 PM
**Day 2 任務：** Autopsy 掛載 ext4 image 寫鑑識報告 + 基礎 Linux 加固 checklist

**本地資源：**
- `06_網路安全與數位取證/04_數位取證DFIR/教主Kali與Python_回收站數位取證`
- `06_網路安全與數位取證/04_數位取證DFIR/教主Kali與Python_PDF元數據數位取證`
- `07_藍隊防禦與護網營運/02_系統與資料庫加固/系統加固_Linux系統安全加固`
- `07_藍隊防禦與護網營運/02_系統與資料庫加固/系統加固_漏洞加固`
- `07_藍隊防禦與護網營運/04_日誌與告警研判/暗月Web紅隊_Web日誌分析與逃逸檢測`

**線上資源：**
- Autopsy：https://www.autopsy.com/
- DFIR.training 資源庫：https://www.dfir.training/

---

## 第 2 個月：Web 深挖 × DEVCORE 紅隊門檻

### Week 1–2：PortSwigger 全套衝刺

**目標：** DEVCORE Red Team 必要（全部 Lab 做完）

**PortSwigger 優先順序：**
1. SQL Injection（所有 Lab）
2. Cross-site Scripting（所有 Lab）
3. CSRF、Clickjacking
4. SSRF、XXE
5. Authentication、Access Control
6. Path Traversal、File Upload
7. OS Command Injection
8. Business Logic、Information Disclosure
9. WebSockets、GraphQL、Prototype Pollution（進階）

**本地補充資源：**
- `01_Web安全/06_SQL注入與命令執行/Web攻防實戰_SQL注入WAF繞過`
- `01_Web安全/08_客戶端與業務邏輯漏洞/Web攻防實戰_業務邏輯安全`
- `01_Web安全/Web攻防實戰_訪問控制`
- `01_Web安全/Web攻防實戰_認證會話`
- `01_Web安全/13_Web安全筆試與面試考題`（每週核對一次）

**其他線上資源：**
- OWASP Testing Guide：https://owasp.org/www-project-web-security-testing-guide/
- HackTricks Web Attacks：https://book.hacktricks.xyz/

---

### Week 3：網頁開發建站（補 DEVCORE 最大缺口）

**任務：** 用 Python Flask 或 PHP 手刻含登入 + CRUD 的小型網站，刻意埋入漏洞

**刻意埋入的漏洞：** SQLi、弱 JWT、XSS、IDOR、任意檔案上傳

**本地補充資源：**
- `01_Web安全/03_後端語言與數據庫語法`（PHP / MySQL 語法參考）
- `01_Web安全/Web攻防實戰_WebApp開發`
- `09_基礎設施與運營環境/02_程式語言運行時/國科CTF_JAVA環境`
- `09_基礎設施與運營環境/02_程式語言運行時/國科CTF_Python環境`

**線上資源：**
- Flask 官方文檔：https://flask.palletsprojects.com/
- DVWA（含漏洞靶機範本）：https://github.com/digininja/DVWA

---

### Week 4：伺服器架設（補 DEVCORE 第二缺口）

**任務：** Docker 架設 Nginx + Apache + Tomcat，設定 vhost / TLS / log

**本地補充資源：**
- `01_Web安全/10_中間件與框架安全/Web攻防實戰_Nginx伺服器安全`
- `01_Web安全/10_中間件與框架安全/Web攻防實戰_Apache伺服器安全`
- `01_Web安全/10_中間件與框架安全/Web攻防實戰_Tomcat伺服器安全`
- `07_藍隊防禦與護網營運/03_存取控制與防火牆/外校_Linux存取控制與防火牆`
- `09_基礎設施與運營環境/03_Web與容器環境/工具使用_phpStudy`

**線上資源：**
- Docker 官方文檔：https://docs.docker.com/
- Nginx 設定指南：https://nginx.org/en/docs/

---

## 第 3 個月：AD 攻防深挖（全國賽 CTF II 核心）

### Week 1：AD 環境搭建

**線上資源：**
- GOAD（Game of Active Directory）：https://github.com/Orange-Cyberdefense/GOAD
- 手動搭建教學：https://www.youtube.com/c/TCMSecurityAcademy

**本地資源：**
- `09_基礎設施與運營環境/01_虛擬機與作業系統/工具使用_VMware`
- `09_基礎設施與運營環境/01_虛擬機與作業系統/工具使用_KaliLinux`

---

### Week 2：攻擊鏈演練（對標全國賽 CTF II）

| 攻擊技術 | 工具 | 對標考題 |
|----------|------|----------|
| Kerberoasting | impacket GetUserSPNs + hashcat | 全國賽 CTF II |
| AS-REP Roasting | impacket GetNPUsers | 延伸補充 |
| Golden Ticket | mimikatz / impacket | 全國賽 CTF II |
| DPAPI 憑證提取 | mimikatz dpapi | 全國賽 CTF II |
| Pass-the-Hash | impacket psexec / CrackMapExec | 全國賽 CTF II |
| SQL Server 提權至 SYSTEM | xp_cmdshell + impacket | 全國賽 CTF II |

**本地資源：**
- `04_系統與內網安全/07_內網橫向與域控/暗月Web紅隊_內網橫向滲透`
- `04_系統與內網安全/07_內網橫向與域控/Metasploit魔鬼訓練營_HASH憑證`
- `04_系統與內網安全/07_內網橫向與域控/HW_域控`
- `04_系統與內網安全/08_C2與控權/暗月Web紅隊_CobaltStrike控權`

**線上資源：**
- impacket：https://github.com/fortra/impacket
- CrackMapExec：https://github.com/byt3bl33d3r/CrackMapExec
- HackTricks AD 攻擊鏈：https://book.hacktricks.xyz/windows-hardening/active-directory-methodology
- TryHackMe：Attacking Active Directory

---

### Week 3：AD CS 漏洞（ESC1 / ESC15）

**線上資源：**
- Certipy：https://github.com/ly4k/Certipy
- AD CS 漏洞白皮書（Specter Ops）：https://posts.specterops.io/certified-pre-owned-d95910965cd2

---

### Week 4：AD Hardening（全國賽 Day1 PM）

**任務：** 每個設定做「攻擊前 vs 加固後」對比驗證

- LDAP signing / Channel binding
- SMB signing、SAM 防護、Print Spooler 限制
- PowerShell Script Block Logging + Constrained Language Mode
- dMSA 遷移、AD CS ESC1/ESC15 修補

**本地資源：**
- `07_藍隊防禦與護網營運/02_系統與資料庫加固/HW_加固`
- `07_藍隊防禦與護網營運/01_護網專案營運/HW_藍隊日誌`
- `07_藍隊防禦與護網營運/05_藍隊面試與培訓/HW_護網藍隊面試實戰培訓`

**線上資源：**
- Microsoft AD 安全最佳實踐：https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/best-practices-for-securing-active-directory
- PingCastle（AD 弱點掃描）：https://www.pingcastle.com/

---

## 第 4 個月：數位鑑識深度版（全國賽 Day1 AM）

### Week 1：PCAP 封包鑑識

**任務：** DNS 隧道偵測、HTTP 明文提取、SQLi 痕跡還原

**本地資源：**
- `06_網路安全與數位取證/03_流量分析PCAP/ctf_流量分析賽題`
- `06_網路安全與數位取證/03_流量分析PCAP/ctf_流量`
- `06_網路安全與數位取證/01_網路協定分析與Scapy/教主Kali與Python_Scapy協定分析`
- `06_網路安全與數位取證/HW_流量`

**線上資源：**
- Wireshark 過濾語法：https://wiki.wireshark.org/DisplayFilters
- malware-traffic-analysis.net（PCAP 練習集）：https://www.malware-traffic-analysis.net/

---

### Week 2：記憶體 Image 鑑識

**任務：** Volatility 3 完整流程，重建事件 Timeline

**本地資源：**
- `06_網路安全與數位取證/04_數位取證DFIR/`（全資料夾）

**線上資源：**
- Volatility 3：https://github.com/volatilityfoundation/volatility3
- MemLabs CTF 記憶體題庫：https://github.com/stuxnet999/MemLabs
- CTF-Wiki 記憶體鑑識：https://ctf-wiki.org/

---

### Week 3：磁碟 Image 鑑識

**任務：** Autopsy 掃 ext4，找帳號 / SSH key / cron 後門

**本地資源：**
- `06_網路安全與數位取證/04_數位取證DFIR/教主Kali與Python_回收站數位取證`

**線上資源：**
- Autopsy：https://www.autopsy.com/
- Sleuth Kit：https://www.sleuthkit.org/
- Eric Zimmerman 工具集：https://ericzimmerman.github.io/

---

### Week 4：JVM Heap Dump + JWT 分析

**任務：** jcmd 做 heap dump，VisualVM 讀取，提取 JWT key / 敏感資料

**本地資源：**
- `09_基礎設施與運營環境/02_程式語言運行時/國科CTF_JAVA環境`

**線上資源：**
- VisualVM：https://visualvm.github.io/
- Eclipse MAT（Memory Analyzer Tool）：https://www.eclipse.org/mat/
- jwt_tool：https://github.com/ticarpi/jwt_tool

---

## 第 5 個月：Binary 深挖（DEVCORE Binary 組 + 全國賽 CTF I Bin/Reverse）

### Week 1–2：進階記憶體漏洞（M1 沒涵蓋的缺口）

**任務：** Use-After-Free、Race Condition、Heap Exploitation

**本地資源：**
- `02_二進制與逆向/02_PWN記憶體破壞漏洞利用/ctf_PWN堆溢出漏洞`
- `02_二進制與逆向/02_PWN記憶體破壞漏洞利用/ctf_PWN_IOFILE漏洞`
- `02_二進制與逆向/02_PWN記憶體破壞漏洞利用/ctf_PWN高級利用`

**線上資源：**
- how2heap（CTF 堆利用教學）：https://github.com/shellphish/how2heap
- pwnable.tw（DEVCORE 加分平台）：https://pwnable.tw/
  - 推薦順序：Start → orw → calc → applestore

---

### Week 3：OS 底層概念（Virtual/Physical Address / Page Table）

**任務：** 理解虛擬記憶體映射，Page Fault 機制，對應 DEVCORE Binary 組要求

**線上資源：**
- OSDev Wiki：https://wiki.osdev.org/Paging
- CS:APP 第9章（虛擬記憶體）：免費章節 http://csapp.cs.cmu.edu/

---

### Week 4：全國賽 CTF I 特殊題型

**任務：**
1. GBA ROM 逆向（mGBA 模擬器 + Ghidra GBA plugin）
2. Java / JVM profiling（VisualVM 分析 heap）

**本地資源：**
- `02_二進制與逆向/03_靜態反彙編與動態逆向/Z0FCourse_逆向工程全套講義`
- `02_二進制與逆向/04_移動與物聯網/ctf_IoT智慧設備與路由器漏洞利用`
- `02_二進制與逆向/ctf_360勸退賽題_逆向工程`

**線上資源：**
- Ghidra GBA plugin：https://github.com/SiD3W4y/GhidraGBA
- mGBA 模擬器：https://mgba.io/

---

## 第 6 個月：模擬全國賽 + DEVCORE 實習衝刺

### Week 1–2：讀書會內部模擬全國賽

| 時段 | 科目 | 重點 |
|------|------|------|
| Day1 上午 | 數位鑑識模擬卷 | pcap + mem + disk + JVM |
| Day1 下午 | 安全強化模擬卷 | AD/Linux hardening 實作 |
| Day2 上午 | CTF I（Jeopardy） | Web + Bin + Reverse + Misc |
| Day2 下午 | CTF II（Attack-Defense） | DMZ → 內網 → AD → Domain Admin |

**本地資源：**
- `08_通用學習與面試庫/01_CTF競賽Writeup與題解/ctf_歷年競賽Writeup`
- `08_通用學習與面試庫/01_CTF競賽Writeup與題解/51CTO奪旗賽_綜合測試`
- `08_通用學習與面試庫/02_CTF賽制介紹與平台指南/國科CTF_賽前指導答疑`

---

### Week 3：CTFtime 實戰賽

**選賽標準：** CTFtime weight > 20，Jeopardy 賽制
**目標：** 每場至少解出各類別 1 題，賽後對照官方 writeup

**線上資源：**
- CTFtime：https://ctftime.org/event/list/upcoming
- HITCON CTF 歷屆題目：https://github.com/hitcon-ctf

---

### Week 4：DEVCORE 實習申請準備

**逐條核對，整理個人技能對照表：**

| DEVCORE 硬性條件 | 我完成的佐證（題目/專案/Lab） |
|------------------|-------------------------------|
| Python / Shell Script | |
| OWASP Top 10 | |
| PortSwigger 全部 Lab | |
| 網頁建站（Flask/PHP） | |
| Nginx/Apache 伺服器架設 | |
| GDB + ROP chain | |
| Ghidra 逆向 | |
| CTF 經驗 | |
| pwnable.tw 成績 | |

**本地資源：**
- `08_通用學習與面試庫/13_Web安全筆試與面試考題`
- `07_藍隊防禦與護網營運/05_藍隊面試與培訓/HW_護網藍隊面試實戰培訓`
- `08_通用學習與面試庫/05_HR與跨領域面試/HR綜合面試與跨領域考題`

---

## 常駐線上資源清單（全程使用）

| 平台 | 用途 | 網址 |
|------|------|------|
| PortSwigger Web Security Academy | M2 主力（DEVCORE 必做） | https://portswigger.net/web-security |
| CryptoHack | 密碼學漸進解題 | https://cryptohack.org/ |
| pwn.college | PWN 系統化教學 | https://pwn.college/ |
| pwnable.kr | PWN 解題（DEVCORE 加分） | http://pwnable.kr/ |
| pwnable.tw | PWN 解題（DEVCORE 加分指定） | https://pwnable.tw/ |
| HackTricks | 攻擊技術速查 | https://book.hacktricks.xyz/ |
| GTFOBins | Linux 提權速查 | https://gtfobins.github.io/ |
| LOLBAS | Windows 提權速查 | https://lolbas-project.github.io/ |
| CTFtime | 賽事行事曆 | https://ctftime.org/ |
| CTF-Wiki | 題型解析百科 | https://ctf-wiki.org/ |
| CyberChef | 編碼/解碼瑞士刀 | https://gchq.github.io/CyberChef/ |
| RevShells | Reverse Shell 產生器 | https://www.revshells.com/ |
| PicoCTF | 入門到中階 CTF 練習 | https://picoctf.org/ |
| OverTheWire | Linux 基礎 + Web 題目 | https://overthewire.org/ |
| GOAD | AD 實驗環境 | https://github.com/Orange-Cyberdefense/GOAD |
| Exploit-DB | CVE / Exploit 速查 | https://www.exploit-db.com/ |
