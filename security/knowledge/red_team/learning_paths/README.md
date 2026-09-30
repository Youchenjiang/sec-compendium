# 🧭 紅隊全領域深度學習路徑全景導航庫 (Red Team Learning Paths Directory)

> 💡 **核心精神**：本目錄為 [`../index.md`](../index.md) 中六大作戰階段、23 個攻擊核心領域量身打造的**「全流程深度自學與實戰突破指南」**（六大作戰區塊、22 篇深度原理手冊）。
>
> 徹底解決「只有技術手冊、不知道怎麼學、缺乏系統化底層架構」的信心焦慮，每個模組皆包含：**📍 你在哪裡去哪裡（狀態對比）、🧱 第零關前置基礎、🗺️ 整體學習地圖（四/五階段時長）、各階段底層機制/封包結構/指令實作、以及 ✅ 本路徑通過檢查表（Checklist）**。
>
> 🚀 **實戰修課主線**：想知道按部就班的推薦學習順序？請直接參閱 [【現代紅隊實戰通關課表與作戰主線 (Phase 1 ~ Phase 6)】](../career_curriculum.md)（含 Phase 1 ~ Phase 6 全景作戰鏈、40 項 Core 核心必修與能力分流）。
>
> 🎯 **實戰題庫對照表**：所有 110 篇原子手冊與免費線上靶場（PortSwigger、HTB、picoCTF、GOAD、SadServers、CloudGoat 等）的逐題對照，請參閱 [【紅隊全領域實戰滲透與可練習題庫總表】](../index.md)。

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

---

## ⚡ 區塊四：主機立足與本地提權 (Host Foothold & Privilege Escalation)
> 💡 **作戰任務**：突破作業系統邊界獲取 Root 或 SYSTEM 終極控制權。深入 Linux 核心狀態機與 Windows 存取權杖模型，掌握 SUID、Capabilities、Dirty Pipe、Potato 家族、UAC 繞過與 LSASS/DPAPI 憑據金庫提取。

- [**學習路徑 14：Linux 主機權限提升與核心安全機制深度自學路徑**](block_4_host_privesc/14_linux_privilege_escalation_internals.md)
  - **涵蓋領域**：R18 (SUID/SGID 權限位元、Sudoers 弱配置、Dirty Pipe 核心漏洞、POSIX Capabilities、Cron 通配符、NFS no_root_squash)
  - **核心技術**：行程身分模型 (RUID/EUID/SUID) 轉換、微特權 Capability 分割、Linux 管道環形緩衝區髒頁覆寫、Wildcard 命令列參數注入。
- [**學習路徑 15：Windows 主機權限提升：存取權杖、UAC 繞過與服務劫持深度學習路徑**](block_4_host_privesc/15_windows_privilege_escalation_tokens_uac.md)
  - **涵蓋領域**：R19.1 ~ R19.5 (未加引號服務路徑、Potato 權杖模擬、AlwaysInstallElevated、UAC Bypass、DLL 搜尋順序劫持)
  - **核心技術**：Windows Token 模擬機制、DCOM 命名管道欺騙、Auto-Elevate 程式白名單、Mock Folders 空格目錄偽造、SafeDllSearchMode 順序劫持。
- [**學習路徑 16：Windows 憑證存取機制：SAM、LSASS 記憶體與 DPAPI 深度學習路徑**](block_4_host_privesc/16_windows_credential_access_lsass_dpapi.md)
  - **涵蓋領域**：R19.6 ~ R19.8 (SAM/SYSTEM 登錄檔轉儲、LSASS 記憶體憑據提取、RunAsPPL 核心防護對抗、DPAPI 主金鑰解密)
  - **核心技術**：離線 Syskey 解密本機 NTLM Hash、LSA 安全子系統記憶體佈局、BYOVD 易受害驅動抹除 PPL 旗標、網域備份金鑰 (Domain Backup Key) 跨主機解密。

---

## 🌪️ 區塊五：內網橫向移動、穿透代理與 C2 基礎設施 (Pivoting & C2 Infrastructure)
> 💡 **作戰任務**：建立隱蔽、強韌、具備動態流量可塑性的多層通訊鏈路。化解企業嚴苛邊界防火牆，將整個內網直接映射至本機路由，並透過 WMI/WinRM 原生無檔案機制進行跳板橫向移動。

- [**學習路徑 17：網路流量穿透、SOCKS5 代理與隱蔽隧道深度學習路徑**](block_5_pivoting_c2/17_network_traffic_tunneling_socks_proxies.md)
  - **涵蓋領域**：R20 (Chisel 反向 SOCKS5、Ligolo-ng TUN 代理、SSH 動態轉發、FRP 高性能穿透、DNS/ICMP 隱蔽隧道、PortProxy)
  - **核心技術**：SOCKS5 (RFC 1928) 握手語意、Ligolo-ng 虛擬 L3 網卡路由直連、DNS 遞迴解析外帶通道、ICMP Payload 數據封裝。
- [**學習路徑 18：現代 C2 架構體系、流量可塑性偽裝與記憶體隱蔽深度學習路徑**](block_5_pivoting_c2/18_c2_frameworks_architecture_traffic_malleability.md)
  - **涵蓋領域**：R21.1 ~ R21.4 (Sliver C2、Havoc C2 Demon Agent、Malleable 流量塑形、CDN/Domain Fronting、Sleep Mask 動態記憶體加密)
  - **核心技術**：分散式 Team Server 拓撲、HTTP 標頭流量可塑性偽裝、隨機 Jitter 破壞週期性分析、Sleep Mask (Ekko) 休眠記憶體 XOR 動態加密。
- [**學習路徑 19：內網橫向移動協定、無檔案遠端執行與會話劫持深度學習路徑**](block_5_pivoting_c2/19_lateral_movement_protocols_session_hijacking.md)
  - **涵蓋領域**：R21.5 ~ R21.6 (WMI/WinRM 無檔案遠端執行、PsExec 服務代價分析、RDP 會話劫持與影子桌面)
  - **核心技術**：DCE/RPC 端點映射、`Win32_Process.Create` 無二進位檔案落地執行、Evil-WinRM 雜湊傳遞登入、`tscon.exe` 遠端桌面免密搶奪。

---

## 🥷 區塊六：執行期防禦規避、雲端與容器滲透 (Defense Evasion, Cloud & Containers)
> 💡 **作戰任務**：與現代最頂級的安全防禦機制正面對抗。直擊 EDR/XDR 底層核心，穿透 User-Mode API Hooking、直接發出核心系統調用，並攻陷公有雲 IAM 身分邊界與 Kubernetes 容器編排叢集。

- [**學習路徑 20：終端防禦規避、直接系統調用與進程注入深度學習路徑**](block_6_evasion_cloud/20_edr_evasion_syscalls_unhooking_injection.md)
  - **涵蓋領域**：R22 (Direct/Indirect Syscalls、AMSI/ETW Patching、Process Hollowing、Early Bird APC 注入、Perun's Fart 磁碟脫鉤)
  - **核心技術**：EDR Inline Hook 機器碼覆寫本質、Indirect Syscalls 規避呼叫堆疊審查、記憶體讀取磁碟乾淨 `ntdll.dll` 脫鉤、APC 佇列早期注入。
- [**學習路徑 21：雲端環境滲透、實例元數據與 IAM 特權提升深度學習路徑**](block_6_evasion_cloud/21_cloud_identity_metadata_iam_abuse.md)
  - **涵蓋領域**：R23.1, R23.3 (IMDSv1 vs IMDSv2 元數據竊取、AWS/GCP IAM 策略漏洞與 21 種提權鏈、S3/GCS 儲存桶枚舉與接管)
  - **核心技術**：SSRF 穿透 Link-Local 取得 STS 臨時憑證、`iam:CreatePolicyVersion` 提權、`iam:PassRole` 結合 EC2 反彈 Shell、儲存桶未授權寫入投毒。
- [**學習路徑 22：容器逃逸機制、Kubernetes 叢集滲透與 RBAC 特權提升深度學習路徑**](block_6_evasion_cloud/22_container_escape_kubernetes_cluster_exploitation.md)
  - **涵蓋領域**：R23.2, R23.4, R23.5 (特權容器逃逸、Docker.sock 掛載逃逸、K8s ServiceAccount 憑據提取、RBAC 提權與 etcd 轉儲)
  - **核心技術**：Linux 命名空間與 Cgroups 邊界穿透、宿主機磁碟設備直接掛載逃逸、ServiceAccount JWT Token 存取 API Server、`pods/create` 結合 HostPath 接管節點。
