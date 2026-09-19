# 方案 C：配套靶場實體資產與挑戰題目擴充（Labs & Challenges Expansion）實施計畫

本計畫旨在將現有的 **107 本藍隊防禦與護網營運手冊** 以及 **全真模擬考試庫**，從「文字標準作業程序 (SOP)」全面升級為**「具備實體環境、真實跡證、可親手揮刀與 Flag 檢定的交鑰匙靶場系統（Turnkey Cyber Range）」**。

---

## 1. 核心實施目標與價值主張

1. **破除紙上談兵**：提供即開即用（Turnkey）的 `docker-compose.yml` 部署套件，讀者不需要手動裝配繁雜的底層相依性，一行指令即可拉起攻防演練環境。
2. **輕量化離線分析（雙軌支援）**：針對電腦規格有限無法跑大型 VM 的使用者，建立 `challenges/evidence/` 實體鑑識標本包（真實 PCAP 封包、EVTX 事件紀錄、進程記憶體 dump），直接支援 Wireshark、tshark、Hayabusa、Chainsaw 分析。
3. **測驗題庫（Mock Exam B）100% 實體化**：將 `mock_exam_b_lab_questions.md` 中的情境題與實體跡證檔案深度錨定，提供客觀的 `FLAG{...}` 驗證機制。
4. **與現有資產無縫接軌**：完整相容 `career_curriculum.md` 課綱、90 Runs 訓練地圖與 `validate_playbooks.py` CI/CD 檢查管道，不造成既有知識庫任何破壞。

---

## 2. 目錄架構拓撲規劃

```
ctfd-kit/security/
├── labs/                               # [新增] 實體靶場環境專屬目錄
│   ├── README.md                       # 靶場架構概覽、最低硬體需求與快速啟動指南
│   ├── OPTION_C_EXPANSION_PLAN.md      # 本實施計畫文檔（專案永久存檔）
│   ├── 01_atomic_purple_range/         # 【對接 27.1 / 27.2】紫隊自動化對抗模擬靶場
│   │   ├── docker-compose.yml          # Caldera Server + Linux Target + Sysmon Agent
│   │   ├── configs/                    # Caldera 預設設定、Sysmon 偵測規則配置
│   │   ├── scripts/                    # run_atomic_test.sh 一鍵注入攻擊技術 (T1059, T1003 等)
│   │   └── README.md                   # 部署指引、紅隊發動與藍隊告警捕獲演練教學
│   ├── 02_splunk_bots_range/           # 【對接 28.2】Splunk / Elastic BOTS 威脅獵捕環境
│   │   ├── docker-compose.yml          # 輕量 OpenSearch / Elastic SIEM + Logstash 容器
│   │   ├── datasets/                   # BOTS 經典情境縮小版精選真實 Attack Log
│   │   ├── queries/                    # 28.2 手冊對應之 SPL / EQL 查詢與 hunting 語法庫
│   │   └── README.md                   # 啟動步驟與 15 題威脅獵捕挑戰演練
│   └── 03_apt_cross_domain_ctf/        # 【對接 28.1】APT 全鏈條橫向移動奪旗靶場
│       ├── docker-compose.yml          # DMZ (Web漏洞) -> 內網跳板 -> DB/旗標伺服器隔離網路
│       ├── web_vuln/                   # 包含實際 RCE 漏洞之 Web 應用程式源碼
│       ├── internal_pivot/             # 模擬內網橫向移動目標機 (SSH/Samba)
│       ├── flags/                      # Flag 配發與驗證機制
│       └── README.md                   # 紅藍對抗全流程演練指引
├── challenges/
│   ├── evidence/                       # [新增] 離線鑑識標本資料集（免開 Docker 也能揮刀）
│   │   ├── pcap/                       # Cobalt Strike Beacon、DNS Tunneling、WebShell 傳輸封包
│   │   ├── evtx/                       # Windows Event Logs (4624, 4688, Sysmon EID 1, 3, 10)
│   │   ├── memory/                     # 惡意程式注入記憶體 minidump / LiME 測試標本
│   │   └── README.md                   # 標本檔案 SHA-256 清單、分析目標與使用指引
│   └── lab_progress_tracker.md         # [更新] 新增實體靶場通關進度追蹤欄位
└── exams/
    ├── mock_exam_b_lab_questions.md    # [更新] 將題目與 evidence/labs 建立 Flag 格式關聯
    └── mock_exam_b_lab_solutions.md    # [更新] 補充真實命令列執行結果與 Flag 金鑰對照表
```

---

## 3. 五大實施階段詳細規劃 (Work Breakdown Structure)

### 階段一：離線攻防跡證資料集與生成工具（Phase 1: Evidence Datasets）
* **產出成果**：`security/exams/evidence/`
* **核心內容**：
  1. **PCAP 流量包**：
     - `c2_beaconing.pcap`：模擬 Cobalt Strike HTTP/HTTPS 心跳與 Jitter 抖動。
     - `dns_data_exfiltration.pcap`：Base64/Hex 編碼之 DNS 隱寫外帶資料。
     - `webshell_traffic.pcap`：中國蟻劍 / 冰蠍加密通訊流量。
  2. **EVTX 事件日誌**：
     - `sysmon_credential_access.evtx`：包含 Mimikatz 讀取 LSASS 記憶體（Sysmon Event ID 10）。
     - `lateral_movement_psexec.evtx`：包含服務安裝（EID 7045）與網路登入（EID 4624 Type 3）。
     - `powershell_obfuscated_exec.evtx`：包含編碼混淆 PowerShell 執行（EID 4104 / 4688）。
  3. **自動化生成腳本**：
     - 提供 `tools/generate_synthetic_evidence.py`，確保資料包透明可重現，並附帶 SHA256 校驗碼。

### 階段二：紫隊對抗自動化模擬靶場（Phase 2: Atomic Purple Range）
* **產出成果**：`security/labs/01_atomic_purple_range/`
* **核心內容**：
  1. 編寫 `docker-compose.yml`，包含：
     - `caldera-server`：MITRE Caldera C2 自動化對抗測試平台（Web UI: 8888）。
     - `linux-victim`：裝載 Sysmon for Linux 與 Auditd 的靶機容器，掛載 Caldera Agent。
  2. 提供 `scripts/run_atomic_attack.sh`：
     - 自動排程執行 MITRE ATT&CK T1059.004 (Bash 混淆)、T1003.008 (/etc/shadow 竊取)、T1021.004 (SSH 橫向連線)。
  3. 撰寫 `README.md`：指導學員如何登入 Caldera UI 觀測攻擊路徑，並在靶機日誌中驗證 Blue Team 規則命中。

### 階段三：Splunk / Elastic BOTS 威脅獵捕靶場（Phase 3: Splunk BOTS Range）
* **產出成果**：`security/labs/02_splunk_bots_range/`
* **核心內容**：
  1. 編寫 `docker-compose.yml`，配置輕量化 OpenSearch + OpenSearch Dashboards（記憶體控制在 1.5GB 以內，一般筆電可順暢運作）。
  2. 提供預載資料導入腳本 `import_bots_dataset.sh`，將 BOTS 經典攻擊案例（Web 掃描 -> RCE -> 後門植入 -> 提權）匯入索引。
  3. 整理 `queries/bots_hunting_playbook.md`，提供與手冊 `28.2` 嚴密對應的 15 道 Hunting 題目與 SPL/PPL 檢索句法。

### 階段四：APT 跨網段全鏈條奪旗靶場（Phase 4: APT Cross-Domain CTF）
* **產出成果**：`security/labs/03_apt_cross_domain_ctf/`
* **核心內容**：
  1. 編寫三層隔離網段之 `docker-compose.yml`：
     - `dmz-network`（172.20.0.0/24）：對外 Web 服務（含 Log4j / RCE 漏洞）。
     - `internal-network`（172.21.0.0/24）：內部檔案跳板機（含弱口令與 Sudo 提權漏洞）。
     - `vault-network`（172.22.0.0/24）：核心機密資料庫（存放終極 Flag，僅限跳板機連入）。
  2. 提供紅隊攻防走廊與藍隊監控儀表板，支援雙向演練。

### 階段五：全真考題 B 卷（Mock Exam B）打通與 Flag 閉環（Phase 5: Exam Lab Integration）
* **產出成果**：`security/exams/mock_exam_b_lab_questions.md` 與 `solutions`
* **核心內容**：
  1. 將考題中的每道題目，直接指定到 `challenges/evidence/` 中的具體檔案。
  2. 考生可以直接在命令列執行工具（例如 `tshark -r c2_beaconing.pcap -Y "http.request"` 或 `chainsaw hunt evtx/`），算出結果並得到 `FLAG{...}`。
  3. 建立標準解答與驗證腳本，形成「學習 -> 練習 -> 測驗 -> 評分」四位一體的完整體系。

---

## 4. 實施時程與交付檢驗標準

| 階段任務 | 預計產出檔案 | 交付檢核標準 |
| :--- | :--- | :--- |
| **Phase 1: 離線跡證標本庫** | `challenges/evidence/` (PCAP, EVTX, Logs) + SHA256 清單 | 免開容器直接可用 Wireshark / Chainsaw 正確解析 |
| **Phase 2: 紫隊模擬靶場** | `labs/01_atomic_purple_range/` (compose, scripts, doc) | `docker compose up -d` 成功運行，Caldera 順暢注入測試 |
| **Phase 3: BOTS 威脅獵捕** | `labs/02_splunk_bots_range/` (compose, dataset, queries) | OpenSearch 順暢匯入日誌，SPL/EQL 能精確查獲攻擊特徵 |
| **Phase 4: APT 全域奪旗** | `labs/03_apt_cross_domain_ctf/` (3-tier compose, web app) | 3 層隔離網段正常運作，漏洞利用與防禦追蹤完整閉環 |
| **Phase 5: 考題與 Flag 閉環** | `exams/mock_exam_b_lab_*` 更新 | 題目 100% 綁定實體資料集，Flag 驗證無誤 |

---

## 5. 安全與環境規範遵守

1. **零損害相容**：所有新增檔案均放置於 `labs/` 與 `challenges/evidence/`，不更動現有 107 本 Playbook 的內部結構，確保 `python tools/validate_playbooks.py` 持續 100% 通過。
2. **原子化 Git 規範**：每次階段交付遵循 `feat(labs): ...` 或 `docs(labs): ...` 規範，絕不產生巨型混雜 commit。
3. **輕量與資源控制**：所有 Docker 服務皆設有 `mem_limit` 與 `cpus` 限制，確保 8GB~16GB RAM 的一般學生筆電皆可輕鬆運作。
