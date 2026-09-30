# 🚀 現代紅隊實戰通關課表與作戰主線 (Red Team Career & Operational Curriculum)

> 💡 **核心精神**：本文件將紅隊 17 大領域與 70 項實戰 Playbook，由「扁平分散的技術手冊」昇華為**「以作戰鏈 (Cyber Kill Chain) 與企業滲透為核心的修課主線」**。  
> **徹底打破「平鋪流水號 (R01~R17)」帶來的結構割裂**，依照真實滲透作戰順序推進：從外網情報偵察、邊界打點突破，一路挺進至企業 Active Directory 網域統治。

---

## 🧭 紅隊修課階段 (Phase 1 ~ Phase 6) 全景流向

```mermaid
graph TD
    P1["Phase 1: Recon & Attack Surface<br>外部情報與資產暴露面 (R01~R05，19 篇)"] --> P2["Phase 2: Perimeter & Web Exploitation<br>邊界打點與 Web/API 突破 (R06, R09~R15，30 篇)"]
    P2 --> P3["Phase 3: Domain Dominance & Identity<br>企業身分與 AD 網域統治 (R07, R08, R16, R17，21 篇)"]
    P3 -.-> P4["Phase 4: Host Foothold & PrivEsc<br>主機立足與本地提權 (Linux / Windows 本機提權)"]
    P4 -.-> P5["Phase 5: Pivoting & Lateral Movement<br>內網橫向、隧道穿透與 C2 基礎設施"]
    P5 -.-> P6["Phase 6: Evasion & Specialized Targets<br>防禦規避、免殺繞過與雲原生 / K8s 逃逸"]
```

---

## 🎯 學習負擔消解：三層能力分類 (Core / Specialization / Advanced)

面對 70 篇原子手冊，**不需要死記硬背**！請依據三層分流逐步推進：

| 能力層級 | 包含篇數 | 核心定位與目標 | 適合對象 |
| :--- | :---: | :--- | :--- |
| **🎯 核心主幹 (Core Track)** | **25 篇** | 外網快速打點、注入漏洞利用、Kerberoasting/PtH/DCSync、BloodHound 圖譜分析之**絕對必修**。掌握此 25 篇即具備企業外網突破與內網橫向的主力作戰能力！ | 滲透測試員、競賽攻防手、紅隊新手 |
| **🔬 領域專精 (Specialization Track)** | **32 篇** | 請求走私 (Smuggling)、反序列化 (Deserialization)、AD CS 憑證範本濫用 (ESC1~ESC8)、進階 ACL 劫持。按滲透目標情境與隊伍分工專攻。 | 資深滲透顧問、AD 專案研究員、Web 安全專家 |
| **🚀 高階前沿 (Advanced Track)** | **13 篇** | 邊界架構拓撲推導、Golden/Silver Ticket 偽造、DCSync/DCShadow 底層注入、併發競態 (Race Condition) 深度利用。 | 紅隊技術負責人、APT 模擬專家、全真攻防推演主力 |

---

## 🌐 Phase 1: Reconnaissance & Attack Surface (外部情報與資產暴露面)

> 💡 **階段目標**：精確繪製目標組織的外網疆界，從法律實體、ASN、DNS 命名空間，逐步收斂至可攻擊的對外暴露服務，絕不在未授權目標浪費彈藥。

### 必修核心清單
1. **R01 企業法人與人員情資**：組織架構關聯推導 (`R01.1`)、公開人員與郵箱枚舉 (`R01.2`)。
2. **R02 公開數位足跡**：開放網路與搜尋引擎偵察 (`R02.1`)、公開代碼倉庫金鑰洩漏 (`R02.2`)。
3. **R03 域名命名空間**：WHOIS/RDAP 情資 (`R03.1`)、權威 DNS 枚舉 (`R03.2`)、憑證透明度 CT Logs (`R03.4`)、候選主機名發現 (`R03.5`)。
4. **R04 外部基礎設施歸屬**：IP/ASN/網段歸屬驗證 (`R04.1`)、CDN 與邊界歸屬邊界界定 (`R04.2`)。
5. **R05 外部暴露技術驗證**：網路掃描情資 (`R05.1`)、開放通訊埠探測 (`R05.3`)、服務指紋辨識 (`R05.4`)、虛擬主機枚舉 (`R05.5`)、Web 路徑探測 (`R05.6`)。

| 領域編號 | 涵蓋技術手冊路徑 | 核心重點 |
| :--- | :--- | :--- |
| **R01** | [`playbooks/phase_1_recon_surface/R01_organization_public_identity/`](playbooks/phase_1_recon_surface/R01_organization_public_identity/) | 企業架構、職能人員與社交工程目標候選 |
| **R02** | [`playbooks/phase_1_recon_surface/R02_public_digital_footprint/`](playbooks/phase_1_recon_surface/R02_public_digital_footprint/) | 開放原始碼洩漏、搜尋引擎 Dorking |
| **R03** | [`playbooks/phase_1_recon_surface/R03_domain_namespace_naming/`](playbooks/phase_1_recon_surface/R03_domain_namespace_naming/) | DNS 字典枚舉、子域名接管預警、CT 日誌 |
| **R04** | [`playbooks/phase_1_recon_surface/R04_external_infrastructure_ownership/`](playbooks/phase_1_recon_surface/R04_external_infrastructure_ownership/) | BGP 宣告、ASN 歸屬、CDN 真實 IP 穿透辨析 |
| **R05** | [`playbooks/phase_1_recon_surface/R05_external_technical_exposure/`](playbooks/phase_1_recon_surface/R05_external_technical_exposure/) | L4 埠掃描、L7 服務指紋、目錄與 VHost Fuzzing |

---

## 🎯 Phase 2: Perimeter & Web Exploitation (邊界打點與 Web/API 突破)

> 💡 **階段目標**：獲取企業初始立足點 (Initial Foothold)。整合外部認證猜解與應用程式層漏洞，撕開外網防線進入內網。

### 必修核心清單
1. **R06 憑證秘密恢復與猜解**：外部密碼噴灑 (`R06.3`)、撞庫攻擊 (`R06.4`)、離線 Hash 破解 (`R06.1`)。
2. **R09 身分驗證與狀態**：BOLA / 物件層級存取控制失效 (`R09.3`)、功能層級存取控制失效 BFLA (`R09.4`)。
3. **R10 語法解析與直譯器注入**：SQL 注入 (`R10.1`)、作業系統命令注入 (`R10.2`)、伺服端模板注入 SSTI (`R10.3`)。
4. **R11 伺服端資源與後端信任**：伺服端請求偽造 SSRF (`R11.1`)、任意檔案讀取 / 路徑穿越 (`R11.2`)、本機檔案包含 LFI (`R11.3`)。
5. **R12 物件反序列化與重構**：不安全反序列化 (`R12.1`)、XML 外部實體注入 XXE (`R12.2`)。
6. **R13 訊息封裝與中介代理**：HTTP 請求走私 Smuggling (`R13.1`)、Web 快取投毒 (`R13.2`)。
7. **R14 瀏覽器同源策略信任**：跨站腳本 XSS (`R14.1`~`R14.3`)、跨站請求偽造 CSRF (`R14.4`)、CORS 錯誤配置 (`R14.5`)。
8. **R15 業務工作流與邏輯漏洞**：狀態機繞過 (`R15.1`)、重放攻擊 (`R15.2`)、併發競態條件 Race Condition (`R15.3`)。

| 領域編號 | 涵蓋技術手冊路徑 | 核心重點 |
| :--- | :--- | :--- |
| **R06** | [`playbooks/phase_2_perimeter_web/R06_credential_secret_recovery_guessing_reuse/`](playbooks/phase_2_perimeter_web/R06_credential_secret_recovery_guessing_reuse/) | OWA / VPN 密碼噴灑、雜湊破解與秘密復原 |
| **R09** | [`playbooks/phase_2_perimeter_web/R09_application_authentication_session_authorization_state/`](playbooks/phase_2_perimeter_web/R09_application_authentication_session_authorization_state/) | 權限越權、Session 偽造與重放繞過 |
| **R10** | [`playbooks/phase_2_perimeter_web/R10_interpreter_query_expression_injection/`](playbooks/phase_2_perimeter_web/R10_interpreter_query_expression_injection/) | AST 語法樹破壞、RCE 命令執行 |
| **R11** | [`playbooks/phase_2_perimeter_web/R11_server_side_resource_backend_trust/`](playbooks/phase_2_perimeter_web/R11_server_side_resource_backend_trust/) | 突破內網隔離、雲端中繼資料獲取、敏感檔洩漏 |
| **R12** | [`playbooks/phase_2_perimeter_web/R12_serialization_object_binding_state_reconstruction/`](playbooks/phase_2_perimeter_web/R12_serialization_object_binding_state_reconstruction/) | 惡意 Gadget 構造、XML 實體解析濫用 |
| **R13** | [`playbooks/phase_2_perimeter_web/R13_application_message_framing_routing_intermediary_semantics/`](playbooks/phase_2_perimeter_web/R13_application_message_framing_routing_intermediary_semantics/) | 前後端長度邊界不一致利用、快取投毒 |
| **R14** | [`playbooks/phase_2_perimeter_web/R14_browser_cross_origin_trust/`](playbooks/phase_2_perimeter_web/R14_browser_cross_origin_trust/) | 客戶端憑證劫持、同源政策破壞 |
| **R15** | [`playbooks/phase_2_perimeter_web/R15_application_workflow_business_logic_integrity/`](playbooks/phase_2_perimeter_web/R15_application_workflow_business_logic_integrity/) | 業務邏輯邊界突破、高併發競態套利 |

---

## 👑 Phase 3: Domain Dominance & Identity (企業身分與 AD 網域統治)

> 💡 **階段目標**：全面掌控企業 Active Directory 基礎設施。將協定票據、存取控制 ACL、目錄複製 DRSUAPI 與企業憑證服務 (AD CS) 融會貫通。

### 必修核心清單
1. **R07 企業身分協定與票據**：AS-REP Roasting (`R07.1`)、Kerberoasting (`R07.2`)、NTLM Pass-the-Hash (`R07.3`)、TGT 重放 (`R07.4`)、黃金票據偽造 (`R07.6`)、白銀票據偽造 (`R07.7`)。
2. **R08 目錄授權與 ACL 提權路徑**：BloodHound 圖譜收集與分析 (`R08.1`, `R08.2`)、群組隸屬狀態確認 (`R08.3`)、DACL 授權濫用 GenericAll/WriteDacl (`R08.4`)、GPO 劫持 (`R08.5`)。
3. **R16 目錄複製與同步原語**：DCSync 網域憑證複製 (`R16.1`)、DCShadow 惡意目錄狀態注入 (`R16.2`)。
4. **R17 企業憑證服務 (AD CS) 濫用**：使用者指定 SAN 濫用 ESC1 (`R17.1`)、危險 EKU 濫用 ESC2 (`R17.2`)、註冊代理濫用 ESC3 (`R17.3`)、模板 ACL 濫用 ESC4 (`R17.4`)、CA 屬性濫用 ESC5~ESC8 (`R17.5`~`R17.7`)。

| 領域編號 | 涵蓋技術手冊路徑 | 核心重點 |
| :--- | :--- | :--- |
| **R07** | [`playbooks/phase_3_domain_dominance/R07_enterprise_authentication_protocol_ticket_semantics/`](playbooks/phase_3_domain_dominance/R07_enterprise_authentication_protocol_ticket_semantics/) | Kerberos/NTLM 票據生命週期與橫向鑑別 |
| **R08** | [`playbooks/phase_3_domain_dominance/R08_directory_authorization_delegation_privilege_paths/`](playbooks/phase_3_domain_dominance/R08_directory_authorization_delegation_privilege_paths/) | 圖論最短路徑計算、ACL 委派濫用、GPO 劫持 |
| **R16** | [`playbooks/phase_3_domain_dominance/R16_directory_replication_synchronization_semantics/`](playbooks/phase_3_domain_dominance/R16_directory_replication_synchronization_semantics/) | DRSUAPI 協定呼叫、全量 NTDS.dit 雜湊導出 |
| **R17** | [`playbooks/phase_3_domain_dominance/R17_enterprise_certificate_identity_enrollment_trust/`](playbooks/phase_3_domain_dominance/R17_enterprise_certificate_identity_enrollment_trust/) | AD CS 現代憑證攻擊全景 (ESC1~ESC8)、憑證鏈信任劫持 |

---

## 🔮 未來作戰擴充槽位 (Phase 4 ~ Phase 6)

| 規劃階段 | 核心任務 | 涵蓋技術方向 |
| :--- | :--- | :--- |
| **Phase 4: Host Foothold & PrivEsc** | 主機本地立足與提權 | Linux SUID / Sudo / 核心漏洞提權；Windows 服務配置、Token 模擬、SeImpersonate 濫用 |
| **Phase 5: Pivoting & Lateral Movement** | 跨網段穿透與 C2 基礎設施 | Chisel / Ligolo-ng 內網隧道、Sliver / Havoc C2 隱蔽通訊、可塑性 C2 Profile 配置 |
| **Phase 6: Evasion & Specialized Targets** | 防禦規避與前沿環境攻防 | EDR 鉤子繞過 (Direct Syscalls)、AMSI/ETW 記憶體修補、AWS/Azure 雲端提權、K8s 容器逃逸 |
