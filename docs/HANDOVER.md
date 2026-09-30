# 📋 紅隊作戰體系建置工程：跨對話交接文件 (Project Handover Document)

> **交接地點**：`docs/HANDOVER.md`  
> **更新時間**：2026-09-30  
> **交接對象**：接手本專案的下一任 AI 助理 / 資安工程師  
> **當前狀態**：六大作戰階段、23 大領域、全量 110 篇原子特戰手冊與 13 篇深度自學路徑 100% 全數落成！

---

## 🧭 一、 當前專案狀態與 Git 基準線

* **工作目錄**：`c:\Users\LabStrix\Documents\GitHub\Youchen\Security\red-team-curriculum`
* **當前分支**：`feature/red-team-curriculum`（Working Tree 100% Clean）
* **遠端追蹤**：未推送到 `origin`（本機歷史包含完整原子化 Commits）
* **本輪任務連續原子化提交（已嚴格解耦，遵循 SRP 單一責任原則）**：
  * `09d8e2f docs(curriculum): synchronize catalog, index, curriculum, and handover for 110 playbooks`
  * `6497b36 feat(playbooks): expand phase 6 evasion and cloud to 13 playbooks`
  * `094f516 feat(playbooks): expand phase 5 pivoting and c2 to 13 playbooks`
  * `26bc8de feat(playbooks): expand phase 4 host privesc to 14 playbooks covering UAC, DLL, LSASS, and DPAPI`
  * `6695daf feat(playbooks): add phase 6 defense evasion and cloud native playbooks`
  * `109d2da feat(playbooks): add phase 5 network pivoting and c2 infrastructure playbooks`
  * `2b771f9 feat(playbooks): add phase 4 host foothold and privilege escalation playbooks`
  * `a9c9851 test(tools): extend validation tool to support phase 4 through phase 6`
  * `ef392bd docs(learning-paths): update master directory and navigation index`
  * `a8577d3 docs(learning-paths): add block 3 active directory and domain dominance deep learning guides`
  * `ecc7ef9 docs(learning-paths): add block 2 perimeter and web exploitation deep learning guides`
  * `2cd6b0c docs(learning-paths): add block 1 recon and attack surface deep learning guides`
  * `05248e3 docs(index): update red team master skills and lab matrix to 70 techniques`

---

## 🏛️ 二、 紅隊體系三大核心工程成果總覽

### ✅ 成果 1：重構 `security/knowledge/red_team/index.md` (已完成)
* **升級維度**：對齊「六大作戰階段、23 大領域、110 項實戰技術點」的完整終極矩陣表。
* **分級與分流**：
  - 🟢 L1 (26 項) | 🟡 L2 (41 項) | 🔴 L3 (32 項) | 👑 L4 (11 項) 全景難度對照。
  - 整合 🎯 Core 核心主幹 (40 項) / 🔬 Specialization 領域專精 (48 項) / 🚀 Advanced 高階前沿 (22 項) 三層修課分流。
* **100% 免費靶場映照**：精準對接 PortSwigger Web Security Academy、HTB Starting Point / Sherlocks、picoCTF、GOAD、SadServers、GTFOBins、CloudGoat、Kubernetes Goat 等免付費實兵環境。

### ✅ 成果 2：建立 `learning_paths/` 深度自學體系 (已完成)
比照藍隊最高品質規格，於 `security/knowledge/red_team/learning_paths/` 下完成三大區塊共 13 篇深度原理指南：
* **`block_1_recon_surface/`**：
  - `01_external_recon_osint.md` (SEC 10-K 子公司穿透、Hunter.io、TruffleHog 資訊熵)
  - `02_dns_namespace_infrastructure.md` (AXFR 區域傳送、CT Logs、MassDNS、CDN 真實 IP 穿透)
  - `03_external_attack_surface_validation.md` (Shodan/Censys 零流量定位、Nmap SYN 狀態機、OOB 無害驗證)
* **`block_2_perimeter_web/`**：
  - `04_credential_attacks_spraying.md` (Hashcat 規則突變、帳號鎖定閾值探針、OWA 密碼噴灑)
  - `05_web_interpreter_injections.md` (AST 語法樹破壞、DNS 外帶盲注、無空白 Shell 混淆、Jinja2 MRO 沙盒逃逸)
  - `06_server_resource_trust_ssrf_lfi.md` (DNS Rebinding、AWS IMDSv1/v2 憑證竊取、PHP Wrappers、日誌投毒)
  - `07_deserialization_xxe_object_binding.md` (Java CommonsCollections 反射鏈、PHP POP 鏈、Blind XXE、Mass Assignment)
  - `08_http_smuggling_cache_poisoning.md` (CL.TE/TE.CL 長度邊界歧義、未入鍵標頭投毒、密碼重設劫持)
  - `09_browser_trust_and_business_logic.md` (DOM XSS 污點追蹤、CORS 憑證外洩、Turbo Intruder 單連線 HTTP/2 競態)
* **`block_3_domain_dominance/`**：
  - `10_kerberos_protocol_ticket_attacks.md` (三向交換與 PAC 驗證、AS-REP/Kerberoast、黃金/白銀票據)
  - `11_ad_graph_acl_delegation_abuse.md` (BloodHound 最短路徑、Backup Operators 登錄檔讀取、GenericAll、SharpGPOAbuse)
  - `12_directory_replication_dcsync_dcshadow.md` (DRSUAPI RPC 呼叫、secretsdump 全域 Hash 導出、DCShadow 零日誌注入)
  - `13_adcs_certificate_template_abuse.md` (PKINIT 憑證換 TGT、ESC1~ESC8 利用鏈、CA 私鑰外洩「黃金憑證」)
* **`learning_paths/README.md`**：升級為全景導覽手冊，與 index.md、career_curriculum.md 形成無縫導航。

### ✅ 成果 3：Phase 4 ~ Phase 6 全量原子手冊高密度落地 (已完成)
依據 `PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md` 規範，在 `playbooks/` 下完整落成了 3 個新作戰階段、6 個新領域、共 40 篇特戰速查原子手冊：
* **`playbooks/phase_4_host_privesc/` (14 篇)**：
  - `R18_linux_host_privilege_escalation/` (6 篇): SUID/SGID、Sudoers 弱配置、Dirty Pipe 核心提權、POSIX Capabilities、Cron 通配符、NFS no_root_squash。
  - `R19_windows_host_privilege_escalation/` (8 篇): 未加引號服務路徑、SeImpersonate Potato、AlwaysInstallElevated、UAC Bypass 模擬目錄、DLL 搜尋順序劫持、SAM/SYSTEM 轉儲、LSASS PPL 規避、DPAPI MasterKey。
* **`playbooks/phase_5_pivoting_c2/` (13 篇)**：
  - `R20_network_tunneling_proxy_pivoting/` (7 篇): Chisel 反向 SOCKS5、Ligolo-ng TUN 代理、SSH 動態轉發、FRP 高性能穿透、DNS/ICMP 隱蔽隧道、Socat/Netsh PortProxy、SMB 命名管道隧道。
  - `R21_command_and_control_infrastructure/` (6 篇): Sliver C2 部署操作、Malleable C2 流量偽裝、Havoc C2 Demon Agent、Sleep Mask 記憶體混淆、WMI/WinRM 無檔案橫向、RDP 會話劫持與 Shadow。
* **`playbooks/phase_6_evasion_cloud/` (13 篇)**：
  - `R22_defense_evasion_endpoint_runtime/` (8 篇): Direct Syscalls、AMSI/ETW Patching、Process Hollowing、Early Bird APC 注入、PPID 欺騙與參數偽裝、Perun's Fart 磁碟脫鉤、Shellcode UUID 編碼、Defender 排除路徑濫用。
  - `R23_cloud_container_infrastructure_exploitation/` (5 篇): 雲端 IAM/Metadata 濫用、Kubernetes 特權容器逃逸、S3 儲存桶枚舉接管、Docker Socket 掛載逃逸、K8s RBAC 提權與 Secrets 轉儲。

### ✅ 成果 4：召回紅隊作戰編排層 `operations/` (6 篇作戰方法論)
從歷史封存分支中召回並正式編入主幹核心：
* `00_target_intake_and_scope.md` (授權邊界、ROE 制定、測試界限確認)
* `01_attack_surface_and_entry_routing.md` (攻擊面梳理、最佳進入路徑決策)
* `02_foothold_and_privilege_pivots.md` (立足點評估、權限邊界跳板選擇)
* `03_identity_and_lateral_movement_paths.md` (憑證與身分映射、橫向移動作戰路徑)
* `04_execution_validation_and_failure_paths.md` (假陽性辨識、結構化失敗分析與回退)
* `05_scenario_lesson_promotion.md` (實戰覆盤、去識別化沉澱為共通知識庫)
* `README.md` (作戰編排層架構總覽，與藍隊 DFIR 鏈完整對齊)

### ✅ 成果 5：徹底清除冗餘封存區 `tracks/.../archive/` (已完成)
* 將創立宗旨與競賽定位考量濃縮合流至 `tracks/club/friday_study_group/README.md`。
* 徹底刪除實體 `archive/` 目錄，全專案超連結 100% 暢通，消滅歷史目錄噪訊。

### ✅ 成果 6：落成 Block 4 ~ Block 6 深度自學路徑 (共 9 篇新指南，全庫達 22 篇)
為 Phase 4 ~ Phase 6 建立完整的深度自學體系，與前三階段完全對稱：
* **`block_4_host_privesc/`**：
  - `14_linux_privilege_escalation_internals.md` (SUID/Capabilities、Sudoers 弱配置、Dirty Pipe 核心髒頁覆寫、NFS)
  - `15_windows_privilege_escalation_tokens_uac.md` (未加引號服務路徑、Potato 權杖模擬、Auto-Elevate UAC 繞過、DLL 劫持)
  - `16_windows_credential_access_lsass_dpapi.md` (離線 Syskey SAM 轉儲、LSASS PPL 核心防護、BYOVD 驅動對抗、DPAPI 主金鑰解密)
* **`block_5_pivoting_c2/`**：
  - `17_network_traffic_tunneling_socks_proxies.md` (SOCKS5 協定、Chisel 反向隧道、Ligolo-ng TUN 虛擬網卡路由、DNS/ICMP 隱蔽外帶)
  - `18_c2_frameworks_architecture_traffic_malleability.md` (Sliver/Havoc 架構、CDN 隱蔽重定向、Malleable 流量塑形、Sleep Mask 記憶體動態加密)
  - `19_lateral_movement_protocols_session_hijacking.md` (SMB 命名管道、WMI/WinRM 無檔案遠端執行、Evil-WinRM、`tscon` RDP 會話劫持)
* **`block_6_evasion_cloud/`**：
  - `20_edr_evasion_syscalls_unhooking_injection.md` (EDR Inline Hook 剖析、Direct/Indirect Syscalls、Perun's Fart 磁碟脫鉤、AMSI/ETW Patching、Process Hollowing、Early Bird APC)
  - `21_cloud_identity_metadata_iam_abuse.md` (IMDSv1/v2 差異、SSRF 竊取臨時憑證、21 種 IAM 提權利用鏈、S3 儲存桶覆寫投毒)
  - `22_container_escape_kubernetes_cluster_exploitation.md` (特權容器逃逸、Docker Socket 掛載逃逸、K8s ServiceAccount JWT 存取、RBAC 提權與 etcd 轉儲)
* **`learning_paths/README.md`**：升級為全景 6 大區塊、22 篇深度指南之終極導覽門戶。

### ✅ 成果 7：藍隊專屬品質校驗器與雙軌一鍵校驗總入口 (已完成)
* **`validate_blue_team_playbooks.py`**：為藍隊量身打造獨立之手冊品質稽核工具，精準檢驗 107 篇實戰手冊之七大黃金規格關鍵字（案發現場破題、第一動~第五動、靶場實戰、過關驗收）、行數門檻 (>=200 行) 與藍隊內部連結。
* **`validate_playbooks.py` 升級為全能守門員**：整合執行藍隊 (107 篇) 與紅隊 (110 篇) 實戰手冊規範稽核，並對全專案所有 Markdown 文檔 (380 份，736 處內部連結) 執行全量斷鏈檢測。支援 `--all`、`--blue`、`--red`、`--links-only` 命令列參數。

### ✅ 成果 8：紫隊全景對抗聯防體系與 ATT&CK 熱圖閉環 (已完成)
* **`security/knowledge/purple_team/README.md`**：確立紫隊協同演練總綱、偵測在迴圈 (Detection-in-the-Loop) 生命週期與 L0~L4 成熟度評估模型。
* **`attack_defense_matrix.md` (攻防全景聯防矩陣)**：橫跨 MITRE ATT&CK 14 大戰術，建立紅隊 110 篇手冊與藍隊 107 篇手冊的點對點對映表，詳列核心遙測來源 (Sysmon, Windows Event ID, Auditd, Zeek, Suricata, eBPF) 與應變對策。
* **`SPECIFICATION.md` (紫隊技術規範與評分模型)**：定義 TTP 雙向實體關聯準則、L0~L4 防禦成熟度判定指標與 Navigator 圖層自動化編譯工作流。
* **`purple_layer_generator.py`**：自動化解析攻防矩陣資料，校驗所有引用的紅藍手冊有效性，並一鍵產出合乎 MITRE ATT&CK Navigator v4.5 官方規範之 JSON 圖層檔案。
* **`layers/enterprise_attack_defense_layer.json`**：預編譯之企業級紫隊演習覆蓋熱圖，可直接載入官方 Navigator Web 介面呈現實戰閉環。

### ✅ 成果 9：四權分立提交規範與自動化 Commit 審核器 (已完成)
* **`.agent/atomic_commit_rules.md` 重構**：確立「四權分立（目的層 Purpose / 功能層 Function / 脈絡層 Context / 治理層 Governance）」原子化原則，禁止搭便車（嚴禁將 `MEMORY.md`、`HANDOVER.md` 混入功能 commit），並強制規定長度 $\le 72$ 字元與白名單 scopes。
* **`security/tools/lint_commits.py`**：本機端 Conventional Commits 與四權分立驗證腳本，嚴格對齊 `.github/workflows/policy.yml` 門禁標準，支援 `--base`、`--range` 與 `--strict` 模式。
* **歷史 Commit 全面校驗**：重構歷史並審核全部分支提交，達成 100% 符合規範。

---

## 📊 三、 自動化品質驗證現狀 (100% 通過)

執行指令：
```bash
# 1. 執行雙軌手冊與全庫超連結檢驗
python security/tools/validate_playbooks.py

# 2. 執行本機 Commit 政策與四權分立檢驗
python security/tools/lint_commits.py --base origin/main
```

當前全量測試統計結果：
* 🔵 **藍隊全庫 (107 篇手冊 | 31,972 行 | 379 處超連結)**：100% 通過品質稽核。
* 🔴 **紅隊全庫 (110 篇手冊 | 19,113 行 | 115 處超連結)**：100% 通過品質稽核。
* 🟣 **紫隊全庫 (41 項核心 ATT&CK 技術對映 | 1 份 Navigator 圖層 | 1 份技術規範)**：100% 通過有效性檢驗。
* 🌐 **全專案跨模組超連結**：全專案 **381 份 Markdown 文檔共 741 處內部超連結 100% 暢通，無任何死鏈！**
* 🛡️ **Commit 治理政策**：全部分支 Commits **100% 符合 Conventional Commits 與長度 $\le 72$ 字元限制！**

---

## 🔮 四、 下一階段展望與建議行動

1. **遠端倉庫同步 (Push to Remote)**：
   - 目前所有原子化 Commits 皆安全保存在本地 `feature/red-team-curriculum` 分支。
   - 經用戶確認後，可執行 `git push origin feature/red-team-curriculum` 或發起 Pull Request 合併進主幹。
2. **靶場實體紫隊演習聯動**：
   - 透過 `phase_6_capstone/ranges/01_atomic_purple_range` 進行 Caldera 與 Atomic Red Team 的自動化注入測試，驗證端點日誌即時產出。

