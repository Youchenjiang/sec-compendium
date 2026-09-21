# 🗺️ 資訊安全全域知識領域演進地圖 (security_domains_map.md)

> [!IMPORTANT]
> **檔案定位**：本檔案依據資安核心九大技術領域（`01` 至 `09`）建立，為全體成員與組長提供**「資安各核心領域的內在構成邏輯、技術點演進關係與全景學習路徑」**。
> 幫助成員在進入各實戰章節或 90-Runs 課表前，清楚理解**「各技術領域在整體資安體系中的角色與前後依賴關係」**。

---

## 🧭 全景總覽：九大資安領域體系與全域技能樹

```mermaid
flowchart TD
    ROOT["🛡️ 資訊安全全域攻防體系"]
    
    ROOT --> D1["📁 01_Web安全<br>(Web 應用與 API 安全)"]
    ROOT --> D2["📁 02_二進位制與逆向<br>(底層彙編、逆向與 PWN)"]
    ROOT --> D3["📁 03_密碼學與隱寫<br>(加解密演算法與 Misc)"]
    ROOT --> D4["📁 04_系統與內網安全<br>(系統提權、內網滲透與 AD 域控)"]
    ROOT --> D5["📁 05_程式碼審計與安全開發<br>(白箱原始碼審計與 DevSecOps)"]
    ROOT --> D6["📁 06_網路安全與數位取證<br>(封包分析、取證與 IDS)"]
    ROOT --> D7["📁 07_藍隊防禦與護網營運<br>(系統加固、日誌研判與 SOC)"]
    ROOT --> D8["📁 08_通用學習與面試庫<br>(CTF Writeup、證照與面試)"]
    ROOT --> D9["📁 09_基礎設施與運營環境<br>(靶場、虛擬機器與開發環境)"]

    style ROOT fill:#1e293b,stroke:#3b82f6,stroke-width:3px,color:#ffffff
    style D1 fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#ffffff
    style D2 fill:#0f172a,stroke:#ef4444,stroke-width:2px,color:#ffffff
    style D3 fill:#0f172a,stroke:#ec4899,stroke-width:2px,color:#ffffff
    style D4 fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#ffffff
    style D5 fill:#0f172a,stroke:#f59e0b,stroke-width:2px,color:#ffffff
    style D6 fill:#0f172a,stroke:#8b5cf6,stroke-width:2px,color:#ffffff
    style D7 fill:#0f172a,stroke:#06b6d4,stroke-width:2px,color:#ffffff
    style D8 fill:#0f172a,stroke:#64748b,stroke-width:2px,color:#ffffff
    style D9 fill:#0f172a,stroke:#64748b,stroke-width:2px,color:#ffffff
```

---

## 📁 01_Web安全 (Web 應用與 API 安全)

Web 安全的核心本質是**「不可信任的使用者輸入突破邊界並被伺服器/瀏覽器解析執行」**。本模組目錄依序從通訊基礎、注入破壞到框架與實戰演練：

```mermaid
flowchart TD
    subgraph S1 ["【基礎層】語法、通訊與情報收集"]
        W1["01_前端語言與語法<br>03_後端語言與資料庫"]
        W2["02_HTTP協定與代理抓包<br>(Burp Suite / Headers / Cookies)"]
        W3["04_資產測繪與情報收集<br>05_滲透測試流程與基礎思路"]
    end

    subgraph S2 ["【漏洞核心層】服務端漏洞與使用者端安全"]
        W4["06_SQL隱碼攻擊漏洞專題<br>(Union / Error / Blind / SQLMap)"]
        W5["07_RCE命令與程式碼執行"]
        W6["08_檔案上傳與Webshell木馬權維<br>(蟻劍 / 冰蠍 / 哥斯拉)"]
        W7["09_XXE與XML實體注入"]
        W8["10_客戶端與業務邏輯漏洞<br>(XSS / CSRF / CORS / IDOR)<br>+ 03_API安全與GraphQL專題"]
    end

    subgraph S3 ["【進階與實戰層】元件中介軟體與綜合靶場"]
        W9["11_反序列化與元件漏洞"]
        W10["12_中介軟體與框架安全<br>(Apache / Nginx / IIS / Spring / Struts2)"]
        W11["13_漏洞自動化掃描<br>14_綜合靶場與VulnHub實戰演練<br>15_筆試與面試題庫"]
    end

    S1 --> S2
    S2 --> S3

    style S1 fill:#1e1e2e,stroke:#3b82f6,stroke-width:2px,color:#cdd6f4
    style S2 fill:#181825,stroke:#fab387,stroke-width:2px,color:#cdd6f4
    style S3 fill:#313244,stroke:#a6e3a1,stroke-width:2px,color:#cdd6f4
```

---

## 📁 02_二進位制與逆向 (二進位制底層、逆向與 PWN)

二進位制安全絕非單一學科，而是遵循**「語法地基 ➡️ 閱讀理解 ➡️ 漏洞破壞 ➡️ 高階擴充套件」**的嚴格演進體系：

```mermaid
flowchart TD
    subgraph B1 ["第 1 步：01_組合語言與二進位制基礎 (Assembly)"]
        BA1["x86/x64 暫存器架構 (RAX, RSP, RBP, RIP)"]
        BA2["記憶體分段模型 (Text, Data, Heap, Stack LIFO)"]
        BA3["核心彙編指令 (MOV, LEA, PUSH, POP, CMP, JCC)"]
        BA4["GDB 動態除錯基礎 (下斷點, 暫存器與記憶體檢視)"]
    end

    subgraph B2 ["第 2 步：02_靜態反彙編與動態逆向 (Reverse Engineering)"]
        BB1["反編譯器工具 (Ghidra / IDA Pro / x64dbg)"]
        BB2["控制流分析 (CFG) 與 C 虛擬碼還原"]
        BB3["軟體保護分析 (脫殼, 去混淆, 反除錯)"]
        BB4["演算法逆向與二進位制協定分析"]
    end

    subgraph B3 ["第 3 步：03_PWN記憶體破壞漏洞利用 (Exploitation)"]
        BC1["堆疊溢位 (Stack Overflow) 覆蓋返回位址劫持 RIP"]
        BC2["Ret2text / Ret2shellcode / Ret2libc 漏洞利用"]
        BC3["ROP 鏈構造 (Return-Oriented Programming)"]
        BC4["格式化字串 (Format String) 任意讀寫"]
        BC5["堆漏洞利用 (Heap: UAF / Double Free)"]
        BC6["Python Pwntools 自動化 Exploit 腳本開發"]
    end

    subgraph B4 ["第 4 步：04_移動與物聯網 & 05_二進位制分析工具"]
        BD1["04_移動與物聯網 (Android / ARM 逆向 / IoT 韌體)"]
        BD2["05_二進位制分析工具 (C32Asm / DTDebug / pwn_tools)"]
    end

    B1 -->|具備看懂 CPU 指令能力| B2
    B2 -->|具備找出記憶體漏洞能力| B3
    B3 -->|擴充套件分析領域| B4

    style B1 fill:#1e1e2e,stroke:#3b82f6,stroke-width:2px,color:#cdd6f4
    style B2 fill:#181825,stroke:#89b4fa,stroke-width:2px,color:#cdd6f4
    style B3 fill:#11111b,stroke:#f38ba8,stroke-width:2px,color:#cdd6f4
    style B4 fill:#313244,stroke:#cba6f7,stroke-width:2px,color:#cdd6f4
```

---

## 📁 03_密碼學與隱寫 (密碼學演算法與 Misc)

```mermaid
flowchart TD
    subgraph C1 ["01_密碼學與演算法"]
        CA1["古典密碼學 (凱撒, 維吉尼亞, 頻率分析)"]
        CA2["現代對稱加密 (AES, DES - ECB/CBC 模式, Padding Oracle)"]
        CA3["現代非對稱加密 (RSA 質數分解, 共模攻擊, 小指數攻擊, ECC)"]
        CA4["雜湊演算法與數位簽章 (MD5, SHA-256, 長度擴充套件攻擊)"]
    end

    subgraph C2 ["02_雜項隱寫術 & 03_加解密工具腳本"]
        CB1["02_雜項隱寫術 (圖片 LSB 隱寫, 音訊隱寫, 壓縮包偽加密, 流量隱寫)"]
        CB2["03_加解密工具腳本 (CyberChef, Python Crypto 庫, Hashcat)"]
    end

    C1 --> C2

    style C1 fill:#1e1e2e,stroke:#ec4899,stroke-width:2px,color:#cdd6f4
    style C2 fill:#181825,stroke:#f5c2e7,stroke-width:2px,color:#cdd6f4
```

---

## 📁 04_系統與內網安全 (系統提權、內網滲透與 AD 域控)

內網滲透的核心本質是**「邊界突破後的資訊收集、特權提升、內網穿透、橫向移動與 AD 域控完全接管」**：

```mermaid
flowchart TD
    subgraph N1 ["【偵察與突破】主機探測與初始存取"]
        NA1["01_主機掃描與探測 (Nmap / 埠服務辨識)"]
        NA2["02_未授權服務與RCE利用 (Redis / MongoDB / Memcached)"]
        NA3["03_密碼爆破與字典 (Hydra / 弱密碼字典)"]
        NA4["04_社交工程與釣魚 (社工釣魚郵件 / 惡意巨集)"]
    end

    subgraph N2 ["【特權提升】取得本機最高許可權"]
        NB1["05_許可權提升"]
        NB2["Linux 提權 (SUID / Sudo 配置 / 核心溢位)"]
        NB3["Windows 提權 (未加引號服務路徑 / Token 竊取)"]
    end

    subgraph N3 ["【內網穿透與橫向】打通隧道與擴大戰果"]
        NC1["06_隧道與穿透 (FRP / Neo-reGeorg / SOCKS5 代理鏈)"]
        NC2["07_內網橫向與域控 (PsExec / WMI / 雜湊傳遞 PtH)"]
        NC3["09_區域網欺騙與DDoS攻擊 (ARP 欺騙 / 中間人攻擊)"]
    end

    subgraph N4 ["【域控接管與 C2】企業級特權完全控制"]
        ND1["07_Active Directory 域控攻擊 (Kerberoasting / 黃金票據 / DCSync)"]
        ND2["08_C2與控權 (Cobalt Strike / 許可權維持 / 通訊隱蔽)"]
    end

    subgraph N5 ["【紅隊現代進階】免殺、雲安全與無線近源"]
        NE1["10_免殺技術與EDR繞過 (AMSI / Syscalls / Loader)"]
        NE2["11_雲端安全與容器逃逸 (AWS/Azure / Docker / K8s)"]
        NE3["12_無線安全與物理滲透 (WiFi WPA2/3 / BadUSB / RFID)"]
    end

    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5

    style N1 fill:#1e1e2e,stroke:#3b82f6,stroke-width:2px,color:#cdd6f4
    style N2 fill:#181825,stroke:#f9e2af,stroke-width:2px,color:#cdd6f4
    style N3 fill:#11111b,stroke:#89dceb,stroke-width:2px,color:#cdd6f4
    style N4 fill:#313244,stroke:#f38ba8,stroke-width:2px,color:#cdd6f4
    style N5 fill:#181825,stroke:#cba6f7,stroke-width:2px,color:#cdd6f4
```

---

## 📁 05_程式碼審計與安全開發 (白箱原始碼審計與 DevSecOps)

原始碼審計的核心是**「白箱視角：從資料輸入源 (Source) 追蹤到危險執行函式 (Sink) 的污點分析」**：

```mermaid
flowchart TD
    subgraph A1 ["【語法與基礎】01_Java審計核心與語法"]
        AA1["Java 後端架構、反射機制、類載入器"]
        AA2["典型 MVC 框架工作流 (Spring Boot / MyBatis)"]
    end

    subgraph A2 ["【漏洞分析】02_白箱漏洞審計"]
        AB1["污點追蹤分析 (Source ➡️ Sanitizer ➡️ Sink)"]
        AB2["常見漏洞審計 (SQLi / RCE / SSRF / 檔案操作)"]
    end

    subgraph A3 ["【實戰與進階】03_審計專案實戰"]
        AC1["Java 反序列化利用鏈 (CC 鏈 / Fastjson / Jackson)"]
        AC2["Spring 記憶體馬 (Memory Webshell) 注入與排查"]
        AC3["企業級開源專案 (CMS / OA 系統) 全原始碼實戰審計"]
    end

    subgraph A4 ["【工具與體系】04_白箱審計工具 & 05_SDL與安全開發"]
        AD1["04_白箱審計工具 (Fortify / Semgrep / CodeQL 規則)"]
        AD2["05_SDL與安全開發 (SSDLC / 軟體供應鏈安全 / 安全規範)"]
    end

    A1 --> A2
    A2 --> A3
    A3 --> A4

    style A1 fill:#1e1e2e,stroke:#3b82f6,stroke-width:2px,color:#cdd6f4
    style A2 fill:#181825,stroke:#cba6f7,stroke-width:2px,color:#cdd6f4
    style A3 fill:#11111b,stroke:#f38ba8,stroke-width:2px,color:#cdd6f4
    style A4 fill:#313244,stroke:#a6e3a1,stroke-width:2px,color:#cdd6f4
```

---

## 📁 06_網路安全與數位取證 (封包分析、取證與 IDS)

```mermaid
flowchart TD
    subgraph F1 ["【協定與掃描】01_網路協定分析 & 02_埠掃描"]
        FA1["01_網路協定分析與Scapy (TCP/IP 堆疊, 自定義構造封包)"]
        FA2["02_埠掃描與Nmap工具 (主機探測, NSE 腳本編寫)"]
    end

    subgraph F2 ["【流量分析與監控】03_流量分析PCAP & 05_IDS與網路監控"]
        FB1["03_流量分析PCAP (Wireshark 深度過濾, 惡意流量辨識)"]
        FB2["05_IDS與網路監控 (Suricata / Snort / Zeek 規則部署)"]
        FB3["06_流量與日誌腳本 (Python 自動化分析 PCAP)"]
    end

    subgraph F3 ["【數位取證與沙箱分析】04_數位取證DFIR & 07_惡意程式分析"]
        FC1["04_數位取證DFIR (Volatility 記憶體取證 / Autopsy 磁碟取證)"]
        FC2["07_惡意程式分析與沙箱 (Any.Run / Cuckoo / YARA 規則)"]
        FC3["應急響應 (抑制感染, 後門排查, 還原攻擊鏈 Root Cause)"]
    end

    F1 --> F2
    F2 --> F3

    style F1 fill:#1e1e2e,stroke:#3b82f6,stroke-width:2px,color:#cdd6f4
    style F2 fill:#181825,stroke:#89dceb,stroke-width:2px,color:#cdd6f4
    style F3 fill:#11111b,stroke:#f38ba8,stroke-width:2px,color:#cdd6f4
```

---

## 📁 07_藍隊防禦與護網營運 (系統加固、日誌研判與 SOC)

```mermaid
flowchart TD
    subgraph D_L1 ["【防禦加固】01_系統加固 & 02_存取控制"]
        DA1["01_系統與資料庫加固 (Linux / Windows / MySQL 安全基準)"]
        DA2["02_存取控制與防火牆 (Iptables / WAF / 安全群組配置)"]
    end

    subgraph D_L2 ["【營運監控】03_日誌與告警研判 & 04_護網專案營運"]
        DB1["03_日誌與告警研判 (SIEM 平台, Splunk SPL / ELK 查詢, 誤報排除)"]
        DB2["04_護網專案營運 (重保指揮體系, 威脅情報 IoC 阻斷, 溯源反制)"]
        DB3["05_藍隊面試與培訓 (防禦工程師技能與面試題庫)"]
    end

    D_L1 --> D_L2

    style D_L1 fill:#1e1e2e,stroke:#06b6d4,stroke-width:2px,color:#cdd6f4
    style D_L2 fill:#181825,stroke:#a6e3a1,stroke-width:2px,color:#cdd6f4
```

---

## 📁 08_通用學習與面試庫 ＆ 📁 09_基礎設施與運營環境

* **`08_通用學習與面試庫`**（職涯支援與賽事題解）：
  * `01_CTF競賽Writeup與題解` ｜ `02_CTF賽制介紹與平台指南` ｜ `03_SRC與認證` ｜ `04_通用基礎知識` ｜ `05_HR與跨領域面試`
* **`09_基礎設施與運營環境`**（實驗平台基石）：
  * `01_虛擬機與作業系統` (Kali, Ubuntu, Windows VM) ｜ `02_程式語言運行時` (Python, JDK, PHP) ｜ `03_Web與容器環境` (Docker, LAMP, Tomcat) ｜ `04_連線與傳輸工具` ｜ `05_綜合實驗環境`

---

## 📊 路線圖 (Month 1 ~ Month 6) 與倉庫目錄實體對照表

| 階段 (時程) | 🎯 核心學習主題 | 涵蓋之頂層目錄與核心子資料夾 |
| :--- | :--- | :--- |
| **Month 1** | **攻防雙軌基礎與工具鏈入門** | 📁 `01_Web安全` (01~05, 08) ＋ 📁 `02_二進制與逆向` (01, 05) ＋ 📁 `06_網路安全` (03) |
| **Month 2** | **服務端漏洞深入與二進位制破壞** | 📁 `01_Web安全` (06, 07, 09, 10) ＋ 📁 `02_二進制與逆向` (02) ＋ 📁 `04_系統與內網` (01~04) |
| **Month 3** | **企業內網滲透與框架漏洞實戰** | 📁 `04_系統與內網` (06~08 域控/C2) ＋ 📁 `01_Web安全` (11, 12 中介軟體/框架) ＋ 📁 `02_二進制` (ROP) |
| **Month 4** | **白箱原始碼審計與高階二進位制** | 📁 `05_代碼審計與安全開發` (01~04 Java/PHP 審計) ＋ 📁 `02_二進制` (Format String / Heap 堆漏洞) |
| **Month 5** | **企業藍隊防禦與數位取證** | 📁 `06_網路安全與數位取證` (04 取證) ＋ 📁 `07_藍隊防禦與護網` (01~04 加固/SIEM) ＋ 📁 `03_密碼學` |
| **Month 6** | **綜合實戰、靶場通關與職涯沖刺** | 📁 `01` (15 綜合靶場) ＋ 📁 `08_通用學習與面試庫` (01~05 題解/面試) ＋ 跨領域 AWD 攻防演練 |
