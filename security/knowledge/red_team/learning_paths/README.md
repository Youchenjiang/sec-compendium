# 🧭 紅隊全領域深度學習路徑全景導航庫 (Red Team Learning Paths Directory)

> 💡 **核心精神**：本目錄為 [`../index.md`](../index.md) 中三大作戰階段、17 個攻擊核心領域量身打造的**「全流程深度自學與實戰突破指南」**。
>
> 徹底解決「只有技術手冊、不知道怎麼學、缺乏系統化底層架構」的信心焦慮，每個模組皆包含：**📍 你在哪裡去哪裡（狀態對比）、🧱 第零關前置基礎、🗺️ 整體學習地圖（五階段時長）、各階段底層機制/封包結構/指令實作、以及 ✅ 本路徑通過檢查表（Checklist）**。
>
> 🚀 **實戰修課主線**：想知道按部就班的推薦學習順序？請直接參閱 [【現代紅隊實戰通關課表與作戰主線 (Phase 1 ~ Phase 6)】](../career_curriculum.md)（含 Phase 1 ~ Phase 6 全景作戰鏈、25 項 Core 核心必修與能力分流）。
>
> 🎯 **實戰題庫對照表**：所有 70 篇原子手冊與免費線上靶場（PortSwigger、HTB、picoCTF、GOAD）的逐題對照，請參閱 [【紅隊全領域實戰滲透與可練習題庫總表】](../index.md)。

---

## 🌐 區塊一：外部情報、網路空間測繪與資產暴露面 (Reconnaissance & Attack Surface)
> 💡 **作戰任務**：精確繪製目標組織的外網疆界，從法定法人實體、子網域命名空間、BGP 路由宣告，逐步收斂至可攻擊的對外暴露服務，絕不在未授權目標浪費彈藥。

- [**學習路徑 01：組織架構、人員情報與公開代碼倉庫洩漏深度學習路徑**](block_1_recon_surface/01_external_recon_osint.md)
  - **涵蓋領域**：R01 (組織實體架構、人員郵件枚舉)、R02 (搜尋引擎 Dorking、Git 歷史金鑰洩漏)
  - **核心技術**：SEC 10-K Exhibit 21 子公司穿透、Hunter.io 命名逆推、TruffleHog 資訊熵掃描、100% 被動模式保障。
- [**學習路徑 02：DNS 命名空間、憑證透明度與基礎設施測繪深度學習路徑**](block_1_recon_surface/02_dns_namespace_infrastructure.md)
  - **涵蓋領域**：R03 (RDAP/WHOIS、權威/被動 DNS、憑證透明度 CT Logs)、R04 (BGP/ASN 測繪、CDN 辨析)
  - **核心技術**：AXFR 區域傳送、crt.sh 萬用字元子網域採集、MassDNS 高速解析、SSL 憑證反查穿透 CDN 真實 IP。
- [**學習路徑 03：外部暴露面探測、服務指紋與無害驗證深度學習路徑**](block_1_recon_surface/03_external_attack_surface_validation.md)
  - **涵蓋領域**：R05 (全網測繪資料庫、主機存活性、通訊埠枚舉、服務指紋、VHost/目錄探測、無害驗證)
  - **核心技術**：Shodan/Censys 零流量定位、Nmap Half-Open SYN 狀態機解析、ffuf 虛擬主機碰撞、OOB 帶外無害驗證。

---

## 🎯 區塊二：邊界打點與 Web/API 突破 (Perimeter & Web Exploitation)
> 💡 **作戰任務**：獲取企業初始立足點 (Initial Foothold)。整合外部身分憑證猜解、各類語法直譯器注入、後端資源信任濫用、中介代理走私與業務邏輯破壞，撕開邊界防線進入目標系統。

- [**學習路徑 04：憑證秘密恢復、密碼噴灑與撞庫深度學習路徑**](block_2_perimeter_web/04_credential_attacks_spraying.md)
  - **涵蓋領域**：R06 (離線雜湊破解、線上服務猜解、低頻密碼噴灑、洩漏憑證撞庫)
  - **核心技術**：Hashcat GPU 規則突變、帳號鎖定閾值探針、OWA/Office 365 密碼噴灑、出口 IP 輪替規避 SOC。
- [**學習路徑 05：直譯器與語法樹注入深度學習路徑**](block_2_perimeter_web/05_web_interpreter_injections.md)
  - **涵蓋領域**：R10 (SQL 查詢結構注入、作業系統命令直譯器注入、SSTI 模板引擎注入)
  - **核心技術**：AST 抽象語法樹結構破壞、時間盲注與 DNS 外帶、無空白字元 Shell 混淆、Python Jinja2 MRO 沙盒逃逸。
- [**學習路徑 06：伺服端資源信任、SSRF 內網穿透與檔案包含深度學習路徑**](block_2_perimeter_web/06_server_resource_trust_ssrf_lfi.md)
  - **涵蓋領域**：R11 (SSRF 伺服端請求偽造、任意檔案讀取、本機/遠端檔案包含 LFI/RFI)
  - **核心技術**：DNS Rebinding 與 IP 進制編碼繞過、AWS/GCP IMDSv1/v2 憑證竊取、PHP Wrappers 濾鏡讀取、日誌投毒 GetShell。
- [**學習路徑 07：物件反序列化 Gadget 鏈與 XXE 實體解析深度學習路徑**](block_2_perimeter_web/07_deserialization_xxe_object_binding.md)
  - **涵蓋領域**：R12 (不安全反序列化、XML 外部實體解析 XXE、物件自動綁定 Mass Assignment)
  - **核心技術**：Java 序列化二進位流特徵、CommonsCollections 反射利用鏈、PHP 魔術方法 POP 鏈、外部 DTD 盲注 XXE、API 參數溢出。
- [**學習路徑 08：HTTP 請求走私、中介代理語意與快取投毒深度學習路徑**](block_2_perimeter_web/08_http_smuggling_cache_poisoning.md)
  - **涵蓋領域**：R13 (HTTP 請求走私 CL.TE/TE.CL、Web 快取投毒、Host/Forwarded 標頭劫持)
  - **核心技術**：長度邊界歧義解析、緩衝區殘留請求拼接、未加密鍵 (Unkeyed Header) 探測、快取投毒覆蓋全網靜態資源、密碼重設鏈接偽造。
- [**學習路徑 09：瀏覽器同源策略信任與業務併發競態深度學習路徑**](block_2_perimeter_web/09_browser_trust_and_business_logic.md)
  - **涵蓋領域**：R09 (Session 偽造、BOLA/BFLA 越權)、R14 (XSS/CSRF/CORS 濫用)、R15 (狀態機繞過、併發競態)
  - **核心技術**：DOM XSS 污點資料流追蹤、CORS 憑證外洩 PoC、水平/垂直越權、業務狀態機跳步、Turbo Intruder 單連線 HTTP/2 競態溢出。

---

## 👑 區塊三：企業身分與 AD 網域統治 (Domain Dominance & Identity)
> 💡 **作戰任務**：全面掌控企業 Active Directory 基礎設施。將 Kerberos/NTLM 身分協定、目錄授權 ACL、DRSUAPI 複製原語與企業憑證服務 (AD CS) 融會貫通，取得企業網域至高無上的控制權。

- [**學習路徑 10：Kerberos 協定本質、票據攻擊與偽造深度學習路徑**](block_3_domain_dominance/10_kerberos_protocol_ticket_attacks.md)
  - **涵蓋領域**：R07 (AS-REP Roasting、Kerberoasting、Pass-the-Hash、Pass-the-Ticket、Golden/Silver Ticket)
  - **核心技術**：三向交換時序與 PAC 驗證、無預認證帳號離線破解、SPN 服務票證提取、`krbtgt` 雜湊偽造黃金票據、白銀票據免 KDC 隱蔽打擊。
- [**學習路徑 11：Active Directory 圖論路徑、DACL 委派濫用與 GPO 劫持深度學習路徑**](block_3_domain_dominance/11_ad_graph_acl_delegation_abuse.md)
  - **涵蓋領域**：R08 (BloodHound 圖譜收集分析、操作員群組濫用、DACL 委派濫用、GPO 控制權濫用)
  - **核心技術**：BloodHound/SharpHound 採集、Cypher 最短路徑解算、Backup Operators 登錄檔讀取、GenericAll/WriteDacl 提權、SharpGPOAbuse 排程工作注入。
- [**學習路徑 12：DRSUAPI 目錄複製原語、DCSync 與 DCShadow 注入深度學習路徑**](block_3_domain_dominance/12_directory_replication_dcsync_dcshadow.md)
  - **涵蓋領域**：R16 (DCSync 全域認證複製、DCShadow 惡意目錄狀態注入)
  - **核心技術**：MS-DRSR 協定 RPC 呼叫、`DS-Replication-Get-Changes-All` 延伸特權、secretsdump 遠端全域 Hash 導出、DCShadow 暫態 DC「零日誌」特權寫入。
- [**學習路徑 13：企業憑證服務 (AD CS) 核心原理與 ESC1~ESC8 攻擊鏈深度學習路徑**](block_3_domain_dominance/13_adcs_certificate_template_abuse.md)
  - **涵蓋領域**：R17 (ESC1~ESC4 範本濫用、ESC6 CA 全域 SAN 策略濫用、ESC7 管理特權、憑證信任錨點篡改)
  - **核心技術**：PKINIT 數位憑證換取 TGT 票證、ESC1 指定任意 SAN 偽造管理員憑證、ESC3 註冊代理代表申請、Certipy 工具鏈實戰、CA 私鑰外洩「黃金憑證」持久化。
