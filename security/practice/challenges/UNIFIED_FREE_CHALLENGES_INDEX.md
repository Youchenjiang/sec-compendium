# 🌐 實戰題庫聚合中心 (Unified Free Challenges Hub & Master Index)

> 📌 **收錄原則**：
> 1. **100% 驗證完全免費 (Verified Non-Paywall / Non-VIP)**：所有收錄之關卡、主機與封包皆為免訂閱、免付費、免升級即可完整實作之官方題庫。
> 2. **雙軌對齊 (Purple Team Co-Evolution)**：橫跨「攻擊實施 (Red Team Penetration)」與「防守取證 (Blue Team DFIR)」八大主流實戰平台。
> 3. **結構化索引**：提供各平台原生目錄連結、CSV 原始清單，以及按「六大作戰實戰領域」跨平台聚合導引。

---

## 📊 八大平台免費題庫統計總覽 (Platform Overview)

| 平台名稱 (Platform) | 題庫定位與核心特色 | 驗證免費題數 (Free Tier) | 平台目錄導航 (Catalog) | 原始資料檔案 (Data / CSV) |
| :--- | :--- | :---: | :--- | :--- |
| **🛡️ CyberDefenders** | 藍隊實戰、端點鑑識 (DFIR)、記憶體與威脅情資 | **82 題** | [CyberDefenders 全目錄](platforms/cyberdefenders/cyberdefenders_all_challenges_catalog.md) | [`cyberdefenders_all_challenges_2026.csv`](platforms/cyberdefenders/cyberdefenders_all_challenges_2026.csv) |
| **📦 Hack The Box (HTB)** | 滲透測試主機攻堅 (Machines) 與藍隊調查 (Sherlocks) | **359 題** | [HackTheBox 全目錄](platforms/hackthebox/hackthebox_all_challenges_catalog.md) | [`hackthebox_all_challenges_2026.csv`](platforms/hackthebox/hackthebox_all_challenges_2026.csv) |
| **🦈 Malware-Traffic-Analysis (MTA)** | 真實惡意流量 PCAP、資安事件流量分析與攻擊溯源 | **113 套** | [MTA 流量分析目錄](platforms/mta/mta_all_exercises_catalog.md) | [`mta_all_exercises_2026.csv`](platforms/mta/mta_all_exercises_2026.csv) |
| **🌐 PortSwigger Web Academy** | Web 滲透深度實驗、漏洞利用與程式碼審計 | **274 題** | [PortSwigger 全目錄](platforms/portswigger/portswigger_all_labs_catalog.md)（[90 Runs 追蹤](../../../tracks/lab/90_runs/checklists/portswigger_90_runs.md)） | [`portswigger_all_labs_2026.csv`](platforms/portswigger/portswigger_all_labs_2026.csv) |
| **🚩 picoCTF / CyLab Academy** | CTF 競賽打底、基礎技能、二進位 PWN、逆向與密碼學 | **525 題** | [CyLab 全題目目錄](platforms/cylab_picoctf/cylab_all_challenges_catalog.md)（[學習路徑](platforms/cylab_picoctf/cylab_learning_paths_catalog.md)） | [`cylab_all_challenges_2026-08-08.csv`](platforms/cylab_picoctf/cylab_all_challenges_2026-08-08.csv) |
| **🔐 CryptoHack** | 現代密碼學（AES, RSA, ECC, Diffie-Hellman, Post-Quantum） | **308 題** | [CryptoHack 全目錄](platforms/cryptohack/cryptohack_all_challenges_catalog.md) | [`cryptohack_all_challenges_2026.csv`](platforms/cryptohack/cryptohack_all_challenges_2026.csv) |
| **🎯 TryHackMe (THM)** | 引導式學習與雲端 VM、Active Directory 內網、SOC 防禦全房間 | **992 間** | [TryHackMe 全量房間目錄](platforms/tryhackme/tryhackme_free_rooms_catalog.md) | [`tryhackme_all_rooms_2026.csv`](platforms/tryhackme/tryhackme_all_rooms_2026.csv) |
| **🚩 Root-Me** | 歐洲經典攻防靶場（官方 REST API 動態同步 11 大領域官方題庫） | **608 題** | [Root-Me 全分類目錄](platforms/rootme/rootme_all_challenges_catalog.md) | [`rootme_all_challenges_2026.csv`](platforms/rootme/rootme_all_challenges_2026.csv) |
| **總計 (Total Verified Free Tier)** | **橫跨紅隊滲透、藍隊防禦、CTF 競賽與密碼學之全自動即時同步題庫** | **3,261 題** | **8 大平台官方直連** | **全格式支援 CSV / Markdown** |


---

## 🎯 五大作戰實戰領域跨平台聚合導引 (Cross-Platform Domain Mapping)

### 1. Web 滲透攻堅與流量鑑識 (Web Exploitation & Investigation)
> **紅隊攻擊**：SQL 注入、命令注入、檔案上傳、SSRF、反序列化、認證繞過。  
> **藍隊防禦**：Web 日誌還原、Webshell 捕獲、WAF 阻斷規則、流量取證分析。

- 🌐 **PortSwigger Academy**:
  - [SQL Injection (SQLi) 18 關實戰](https://portswigger.net/web-security/sql-injection)（[追蹤清單](../../../tracks/lab/90_runs/checklists/portswigger_90_runs.md#m2-w1伺服器端基礎)）
  - [OS Command Injection 5 關實戰](https://portswigger.net/web-security/os-command-injection)
  - [File Upload 任意檔案上傳繞過](https://portswigger.net/web-security/file-upload)
  - [SSRF 伺服器端請求偽造](https://portswigger.net/web-security/ssrf)
- 📦 **Hack The Box (Free Machines)**:
  - [Meow](https://app.hackthebox.com/machines/Meow) (Linux / Telnet 服務探針)
  - [Fawn](https://app.hackthebox.com/machines/Fawn) (Linux / FTP 匿名存取)
  - [Appointment](https://app.hackthebox.com/machines/Appointment) (Linux / SQLi 登入繞過)
  - [Responder](https://app.hackthebox.com/machines/Responder) (Windows / LFI & NTLM 雜湊捕捉)
  - [Unified](https://app.hackthebox.com/machines/Unified) (Linux / Log4j CVE-2021-44228 漏洞利用)
- 🛡️ **CyberDefenders (Free Labs)**:
  - [Web Investigation](https://cyberdefenders.org/blueteam-ctf-challenges/web-investigation/) (Easy / SQL 注入與 Webshell 流量鑑識)
  - [Tomcat Takeover](https://cyberdefenders.org/blueteam-ctf-challenges/tomcat-takeover/) (Easy / Web 伺服器管理後台突破鑑識)
  - [OpenWire](https://cyberdefenders.org/blueteam-ctf-challenges/openwire/) (Medium / ActiveMQ Java 反序列化 RCE 鑑識)
- 🚩 **picoCTF / CyLab Academy**:
  - [Insp3ct0r (ID: 367)](https://learn.cylabacademy.org/library?search=Insp3ct0r) (Web 源碼審查)
  - [Irish-Name-Repo 1~3](https://learn.cylabacademy.org/learning-paths/7) (SQLi 萬能密碼系列)
  - [Web Gauntlet (ID: 88)](https://learn.cylabacademy.org/library?search=Web%20Gauntlet) (SQLi 過濾繞過)

---

### 2. 網路封包分析與威脅獵捕 (Network Traffic & PCAP Hunting)
> **紅隊攻擊**：C2 隱蔽通道、DNS Tunneling、橫向 SMB 遠端呼叫、ARP 欺騙。  
> **藍隊防禦**：Wireshark / Zeek 封包剖析、Suricata 簽名撰寫、異常連線頻率統計。

- 🦈 **Malware-Traffic-Analysis (MTA)**:
  - [2026-09-11: Kongtuke rebuke!](https://www.malware-traffic-analysis.net/2026/09/11/index.html) (最新惡意流量分析)
  - [2024-11-26: Traffic Analysis Exercise](https://www.malware-traffic-analysis.net/2024/11/26/index.html) (企業感染鏈封包)
  - 完整 113 套年份封包挑戰索引請見 [MTA 全量目錄](platforms/mta/mta_all_exercises_catalog.md)。
- 🛡️ **CyberDefenders (Free Labs)**:
  - [Lockdown](https://cyberdefenders.org/blueteam-ctf-challenges/lockdown/) (Easy / 多階段網路入侵與記憶體關聯)
  - [XLM-Rat](https://cyberdefenders.org/blueteam-ctf-challenges/xlmrat/) (Easy / 惡意交付流量與反混淆)
  - [DanaBot](https://cyberdefenders.org/blueteam-ctf-challenges/danabot/) (Easy / 初始滲透與惡意 JavaScript 流量)
  - [PsExec Hunt](https://cyberdefenders.org/blueteam-ctf-challenges/psexec-hunt/) (Easy / SMB 流量鑑識與管理員共享獵捕)
  - [HawkEye](https://cyberdefenders.org/blueteam-ctf-challenges/hawkeye/) (Medium / 鍵盤側錄器流量外洩還原)
- 📦 **Hack The Box (Free Sherlocks)**:
  - [Brutus](https://app.hackthebox.com/sherlocks/Brutus) (Very Easy / 網路認證與日誌調查)
  - [Baggage](https://app.hackthebox.com/sherlocks/Baggage) (Very Easy / 網路封包取證)
- 🚩 **picoCTF**:
  - [Wireshark doo dooo do doo... (ID: 432)](https://learn.cylabacademy.org/library?search=Wireshark%20doo%20dooo%20do%20doo...)
  - [Trivial Flag Transfer Protocol (ID: 434)](https://learn.cylabacademy.org/library?search=Trivial%20Flag%20Transfer%20Protocol)

---

### 3. 主機權限提升與端點取證 (Host PrivEsc & Endpoint Forensics)
> **紅隊攻擊**：Linux SUID/Sudo 提權、Windows 權杖模擬 (Token Impersonation)、排程後門。  
> **藍隊防禦**：Windows 事件檢視器 (Event Logs)、MFT/Prefetch 時間線還原、Linux Bash 歷史鑑識。

- 📦 **Hack The Box (Free Machines)**:
  - [Three](https://app.hackthebox.com/machines/Three) (Linux / AWS S3 未授權與 PHP 權限)
  - [Vaccine](https://app.hackthebox.com/machines/Vaccine) (Linux / Sudo 提權)
  - [Archetype](https://app.hackthebox.com/machines/Archetype) (Windows / MSSQL xp_cmdshell & 登錄檔提權)
  - [Oopsie](https://app.hackthebox.com/machines/Oopsie) (Linux / SUID 二進位提權)
- 🛡️ **CyberDefenders (Free Labs)**:
  - [Insider](https://cyberdefenders.org/blueteam-ctf-challenges/insider/) (Easy / Linux 磁碟映像、日誌與 Bash 歷史調查)
  - [KrakenKeylogger](https://cyberdefenders.org/blueteam-ctf-challenges/krakenkeylogger/) (Medium / Windows 10 LNK、通知與應用日誌)
  - [AzurePot](https://cyberdefenders.org/blueteam-ctf-challenges/azurepot/) (Medium / Linux CVE-2021-41773 入侵與端點持久化)
  - [Sysinternals](https://cyberdefenders.org/blueteam-ctf-challenges/sysinternals/) (Medium / 磁碟映像、登錄檔鑑識與惡意程式檢測)
  - [Hacked](https://cyberdefenders.org/blueteam-ctf-challenges/hacked/) (Medium / Linux 伺服器入侵還原、持久化排查與密碼破解)
- 🚩 **picoCTF**:
  - [Magikarp Ground Mission (ID: 189)](https://learn.cylabacademy.org/library?search=Magikarp%20Ground%20Mission) (Linux 系統目錄與權限)
  - [First Find (ID: 320)](https://learn.cylabacademy.org/library?search=First%20Find) (檔案系統搜尋)

---

### 4. 記憶體鑑識與惡意程式逆向 (Memory DFIR & Malware Analysis)
> **紅隊攻擊**：Shellcode 載入器、反除錯 (Anti-debugging)、程式碼混淆、進程注入。  
> **藍隊防禦**：Volatility 3 記憶體轉儲分析、VAD 樹注入識別、PE 結構靜態分析。

- 🛡️ **CyberDefenders (Free Labs)**:
  - [Reveal](https://cyberdefenders.org/blueteam-ctf-challenges/reveal/) (Easy / Windows 記憶體轉儲、惡意進程與命令列分析)
  - [Ramnit](https://cyberdefenders.org/blueteam-ctf-challenges/ramnit/) (Easy / Volatility 記憶體惡意進程定位與雜湊提取)
  - [RedLine](https://cyberdefenders.org/blueteam-ctf-challenges/redline/) (Easy / 記憶體保護屬性、C2 架構與注入分析)
  - [BlackEnergy](https://cyberdefenders.org/blueteam-ctf-challenges/blackenergy/) (Medium / Windows 程式碼注入與未授權 DLL 載入)
  - [Seized](https://cyberdefenders.org/blueteam-ctf-challenges/seized/) (Medium / Linux 記憶體取證、Rootkit 與反彈 Shell 排查)
  - [MrRobot](https://cyberdefenders.org/blueteam-ctf-challenges/mrrobot/) (Medium / 記憶體鑑識、憑證竊取與橫向移動鏈分析)
  - [FakeGPT](https://cyberdefenders.org/blueteam-ctf-challenges/fakegpt/) (Easy / 惡意瀏覽器外掛逆向分析)
  - [XWorm](https://cyberdefenders.org/blueteam-ctf-challenges/xworm/) (Medium / 惡意程式持久化、規避與 C2 設定提取)
  - [GetPDF](https://cyberdefenders.org/blueteam-ctf-challenges/getpdf/) (Medium / 惡意 PDF 結構、JavaScript 反混淆與 Shellcode 模擬)
  - [Obfuscated](https://cyberdefenders.org/blueteam-ctf-challenges/obfuscated/) (Medium / 多階段 Office VBA 巨集與 JS 反混淆)
- 📦 **Hack The Box (Free Sherlocks)**:
  - [PhantomRing](https://app.hackthebox.com/sherlocks/PhantomRing) (Very Easy / 惡意程式分析)
- 🚩 **picoCTF (Binary & Reverse)**:
  - [Safe Opener 1~2](https://learn.cylabacademy.org/learning-paths/10) (靜態逆向)
  - [Bit-O-Asm 1~4](https://learn.cylabacademy.org/learning-paths/2) (x86/x64 彙編閱讀)
  - [buffer overflow 0~1](https://learn.cylabacademy.org/learning-paths/2) (堆疊溢位控制)

---

### 5. Active Directory 域控滲透與威脅情資 (AD Exploits & CTI)
> **紅隊攻擊**：Kerberoasting、AS-REP Roasting、Golden/Silver Ticket、DCSync、BloodHound 攻擊路徑。  
> **藍隊防禦**：Kerberos 票據異常監控、NTDS 提取告警、威脅情資 IOC 關聯與 ATT&CK 映射。

- 🛡️ **CyberDefenders (Free Labs - Threat Intel)**:
  - [Tusk Infostealer](https://cyberdefenders.org/blueteam-ctf-challenges/tusk-infostealer/) (Easy / CTI 情資分析與 IOC 提取)
  - [Red Stealer](https://cyberdefenders.org/blueteam-ctf-challenges/red-stealer/) (Easy / VirusTotal & MalwareBazaar 威脅研判)
  - [3CX Supply Chain](https://cyberdefenders.org/blueteam-ctf-challenges/3cx-supply-chain/) (Easy / 軟體供應鏈攻擊 TTP 溯源歸因)
  - [IcedID](https://cyberdefenders.org/blueteam-ctf-challenges/icedid/) (Easy / 惡意程式家族情資與威脅組織歸因)
  - [GrabThePhisher](https://cyberdefenders.org/blueteam-ctf-challenges/grabthephisher/) (Easy / 釣魚套裝攻擊情資與 Telegram API 外洩追蹤)
  - [BRabbit](https://cyberdefenders.org/blueteam-ctf-challenges/brabbit/) (Medium / Bad Rabbit 勒索病毒攻擊鏈與 ATT&CK 映射)
  - [PhishStrike](https://cyberdefenders.org/blueteam-ctf-challenges/phishstrike/) (Medium / 電子郵件標頭分析與 C2 通道識別)
- 📦 **Hack The Box (Free Sherlocks & Machines)**:
  - [Dream Job-1](https://app.hackthebox.com/sherlocks/Dream%20Job-1) (Very Easy / 威脅情資調查)
  - [Phishing_Email](https://app.hackthebox.com/sherlocks/Phishing_Email) (Very Easy / SOC 釣魚郵件研判)
  - [Dancing](https://app.hackthebox.com/machines/Dancing) (Windows / SMB 共享資源枚舉)
- 🎯 **TryHackMe (Free Rooms - AD & Defense)**:
  - [Attacktive Directory](https://tryhackme.com/room/attacktivedirectory) (Medium / Kerbrute, AS-REP Roasting, DCSync)
  - [AD Basic Enumeration](https://tryhackme.com/room/adbasicenumeration) (Easy / AD 核心架構、DC、LDAP)
  - [Windows Event Logs](https://tryhackme.com/room/windowseventlogs) (Easy / Security Event ID 4624/4625 鑑識)
  - [Windows Logging for SOC](https://tryhackme.com/room/windowsloggingforsoc) (Medium / 行程建立與網路連線日誌偵測)
  - [VulnNet: Active](https://tryhackme.com/room/vulnnetactive) (Hard / 企業多層網域橫向滲透)

---

### 6. 現代密碼學與演算法安全 (Cryptography & Algorithm Security)
> **密碼攻擊**：Padding Oracle、RSA Wiener 攻擊、小指數廣播攻擊、離散對數、雜湊長度擴展、ECC 弱參數。  
> **演算法防禦**：AES-GCM 認證加密、恆定時間比較、密鑰衍生函式 (KDF)、零知識證明 (ZKP) 與後量子密碼 (PQC)。

- 🔐 **CryptoHack (100% Free Challenges)**:
  - [Introduction & General](platforms/cryptohack/cryptohack_all_challenges_catalog.md#📌-introduction3-challenges) (ASCII, Hex, XOR 基礎運算)
  - [Block Ciphers (AES)](platforms/cryptohack/cryptohack_all_challenges_catalog.md#📌-block-ciphers-aes27-challenges) (ECB, CBC, CTR 模式弱點與 Padding Oracle)
  - [RSA Public Key](platforms/cryptohack/cryptohack_all_challenges_catalog.md#📌-rsa29-challenges) (費馬分解、Wiener 攻擊、低指數 Coppersmith)
  - [Diffie-Hellman](platforms/cryptohack/cryptohack_all_challenges_catalog.md#📌-diffie-hellman14-challenges) (離散對數問題、參數注入中間人攻擊)
  - [Elliptic Curves (ECC)](platforms/cryptohack/cryptohack_all_challenges_catalog.md#📌-elliptic-curves23-challenges) (ECDSA 簽章重用隨機數、無效曲線攻擊)
  - [Post-Quantum & Isogenies](platforms/cryptohack/cryptohack_all_challenges_catalog.md#📌-post-quantum18-challenges) (格密碼學基礎、SIDH 密鑰交換)
- 🚩 **Root-Me (Cryptography Track)**:
  - [RSA - Factorisation](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Factorisation) (RSA 模數分解)
  - [RSA - Continued fractions](https://www.root-me.org/en/Challenges/Cryptanalysis/RSA-Continued-fractions) (Wiener 脆弱私鑰連分數攻擊)
  - [Hash - Message Digest 5](https://www.root-me.org/en/Challenges/Cryptanalysis/Hash-Message-Digest-5) (彩虹表與字典破解)
- 🚩 **picoCTF**:
  - [Mod 26 (ID: 144)](https://learn.cylabacademy.org/library?search=Mod%2026) (ROT13 對稱置換)
  - [13 (ID: 63)](https://learn.cylabacademy.org/library?search=13) (凱薩位移)


---

## 🔗 與本專案學習主幹之關聯連結

- 📚 **藍隊 31 大學習路徑導航庫**：[security/knowledge/blue_team/learning_paths/README.md](../../knowledge/blue_team/learning_paths/README.md)
- 🧭 **藍隊實戰通關課表 (Phase 0 ~ Phase 6)**：[security/knowledge/blue_team/career_curriculum.md](../../knowledge/blue_team/career_curriculum.md)
- ⚔️ **紅隊 16 大滲透矩陣與題目表**：[security/knowledge/red_team/index.md](../../knowledge/red_team/index.md)
- 🏫 **社團週五讀書會雙軌演習大綱**：[tracks/club/friday_study_group/curriculum_14weeks.md](../../../tracks/club/friday_study_group/curriculum_14weeks.md)
