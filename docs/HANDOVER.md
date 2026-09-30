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

---

## 📊 三、 自動化品質驗證現狀 (100% 通過)

執行指令：
```bash
python security/tools/validate_red_team_playbooks.py
```

當前全量測試統計結果：
* `phase_1_recon_surface`         : 19 篇 | 總行數:  3,233 行 (平均: 170 行/篇)
* `phase_2_perimeter_web`         : 30 篇 | 總行數:  5,459 行 (平均: 181 行/篇)
* `phase_3_domain_dominance`      : 21 篇 | 總行數:  3,531 行 (平均: 168 行/篇)
* `phase_4_host_privesc`          : 14 篇 | 總行數:  2,378 行 (平均: 169 行/篇)
* `phase_5_pivoting_c2`           : 13 篇 | 總行數:  2,190 行 (平均: 168 行/篇)
* `phase_6_evasion_cloud`         : 13 篇 | 總行數:  2,322 行 (平均: 178 行/篇)
* ----------------------------------------------------------------------
* 🏁 **全庫總計**：**110 篇特戰手冊** | **總行數: 19,113 行** (平均: 173 行/篇)
* ✅ **合規狀態**：100% 通過（0 Errors），所有程式碼圍欄閉合、關鍵字章節全數齊備、篇幅嚴格落於 160 ~ 190 行高密度黃金區間。

---

## 🔮 四、 下一階段展望與建議行動

1. **遠端倉庫同步 (Push to Remote)**：
   - 目前所有原子化 Commits 皆安全保存在本地 `feature/red-team-curriculum` 分支。
   - 經用戶確認後，可執行 `git push origin feature/red-team-curriculum` 或發起 Pull Request 合併進主幹。
2. **學習路徑 Phase 4~6 專題延伸 (可選)**：
   - 若未來需進一步拓展理論教材，可於 `learning_paths/` 依據相同架構建立 `block_4_privesc/`、`block_5_pivoting_c2/` 與 `block_6_evasion_cloud/`。
