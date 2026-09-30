# 🟣 紫隊攻防矩陣與導航圖層技術規範 (Purple Team Technical Specification)

> 本規範定義本專案紫隊（Purple Team）對抗矩陣的建構標準、TTP 映射法則、成熟度評分模型（Scoring Rubric）與 MITRE ATT&CK Navigator 圖層編譯工作流程。

---

## 1. 核心設計架構與目標

紫隊的核心價值在於**打破攻防孤島**，將紅隊的實戰攻擊技術（Offensive TTPs）與藍隊的防禦檢測/數位取證（Detection & Forensics）進行雙向對齊與閉環驗證。

```mermaid
flowchart LR
    subgraph Red[紅隊作戰 (Red Team)]
        RPlaybook["實戰武器化 Playbooks<br/>(110 篇)"]
        RSim["攻擊技術模擬 (Emulation)"]
    end

    subgraph Blue[藍隊聯防 (Blue Team)]
        BPlaybook["偵測與取證 Playbooks<br/>(107 篇)"]
        BTelemetry["端點/網路日誌遙測 (Telemetry)"]
    end

    subgraph Purple[紫隊中樞 (Purple Team Central)]
        Matrix["雙軌對抗矩陣<br/>(attack_defense_matrix.md)"]
        Generator["圖層產生器<br/>(purple_layer_generator.py)"]
        Heatmap["Navigator 全景熱圖<br/>(enterprise_attack_defense_layer.json)"]
    end

    RPlaybook --> Matrix
    BPlaybook --> Matrix
    Matrix --> Generator --> Heatmap
```

---

## 2. TTP 映射準則 (TTP Mapping Criteria)

所有收錄於 `attack_defense_matrix.md` 的技術項目，必須符合以下四項硬性準則：

### 2.1 標準化編碼 (Standardized Identification)
- 必須遵循 **MITRE ATT&CK Enterprise Matrix** 最新定義（v14+）。
- 支援技術主編號（如 `T1055`）與子技術編號（如 `T1059.001`）。
- 必須明確歸屬所屬戰術（Tactic，如 Initial Access, Execution, Persistence 等）。

### 2.2 雙向實體關聯 (Bilateral Concrete Linkage)
- **紅隊實戰連結**：必須指向具體的紅隊手冊（例如 `../../red_team/module_19_cloud_enterprise/R19.2_Azure_AD_Pass_through_Abuse.md`）。
- **藍隊防禦連結**：必須指向具體的藍隊手冊（例如 `../../blue_team/09_Cloud_Security_Incident_Response/09.1_AWS_GuardDuty_Compromise.md`）。
- **零死鏈要求**：手冊之相對路徑必須 100% 存在，並通過 `validate_playbooks.py` 與 `purple_layer_generator.py` 嚴格校驗。

### 2.3 核心遙測資料源 (Telemetry Data Sources)
必須清晰定義檢測該技術所依賴的具體日誌與指標，包括但不限於：
- **Windows / Sysmon**：如 Event ID 1 (Process Create), 3 (Network Connect), 10 (ProcessAccess), 4624/4625 (Logon), 4688。
- **Linux 審計**：Auditd (`audit.log`)、Syslog、`ebpf` 事件流。
- **雲端審計**：AWS CloudTrail, Azure Activity Log, GCP Cloud Audit Logs。
- **網路流量**：Zeek conn.log/http.log/dns.log, Suricata EVE JSON。

### 2.4 主動對抗與緩解處置 (Active Defense & Mitigation)
必須指明具備可操作性的處置工程：
- 檢測規則（Detection Rules）：Sigma 規則、Snort/Suricata 簽章、YARA 規則。
- 系統加固（System Hardening）：攻擊面縮減（ASR）、群組原則（GPO）、權限最小化配置。

---

## 3. 成熟度評定標準 (Maturity & Scoring Rubric)

在編譯產出 MITRE ATT&CK Navigator 圖層時，每個收錄之 TTP 依據其驗證閉環程度給予 0 至 4 分之權重評級：

| 評級 | 分數 | 狀態名稱 | 定義與判定標準 | 視覺色彩 |
|:---:|:---:|:---|:---|:---:|
| **L0** | `0` | **未納入對抗 (Unverified)** | 僅具備理論概念，尚未具備紅隊武器庫腳本或藍隊檢測手冊。 | `#ffffff` (白色) |
| **L1** | `1` | **單軌驗證 (Single Track)** | 僅具備紅隊攻擊 POC，或僅具備靜態防禦建議，未經實體對抗驗證。 | `#e0b0ff` (淺紫) |
| **L2** | `2` | **遙測具備 (Telemetry Ingested)** | 攻擊能成功觸發，且底層作業系統/雲端能記錄原始日誌，但缺乏自動化告警規則。 | `#ba55d3` (中紫) |
| **L3** | `3` | **雙軌閉環 (Purple Validated)** | **【本專案標準】** 紅隊攻擊路徑明確、藍隊具備可即時觸發的 Detection Logic、且雙向手冊皆完成對齊驗證。 | `#800080` (深紫) |
| **L4** | `4` | **持續對抗 (Continuous BAS)** | 已納入自動化入侵模擬（BAS）平台或 CI/CD 安全管線進行回歸測試。 | `#4a0e4e` (暗紫) |

---

## 4. Navigator 圖層編譯工作流 (Compilation Workflow)

### 4.1 自動化生成腳本
專案配備獨立編譯器：[purple_layer_generator.py](file:///c:/Users/LabStrix/Documents/GitHub/Youchen/Security/red-team-curriculum/security/knowledge/purple_team/purple_layer_generator.py)。

執行命令：
```powershell
python security/knowledge/purple_team/purple_layer_generator.py
```

### 4.2 編譯處理流程
1. **解析 Markdown**：以正規表示式抓取 `attack_defense_matrix.md` 中所有 Markdown 表格列。
2. **路徑實體驗證**：走訪每一組紅藍隊手冊相對路徑，確認硬碟上檔案 100% 存在；若有任何死鏈直接拋出錯誤並終止。
3. **元資料組裝**：將 TTP、紅隊手冊清單、藍隊手冊清單、遙測資料源與對抗處置封裝為 Navigator 注解（`comment`）與元資料（`metadata`）。
4. **輸出 JSON**：產出至 `layers/enterprise_attack_defense_layer.json`。

### 4.3 全域整合校驗
全域校驗工具 `security/tools/validate_playbooks.py` 已將紫隊手冊及產生器納入整體測試鏈：
```powershell
# 執行包含紅隊、藍隊、紫隊及全域超連結之整體檢驗
python security/tools/validate_playbooks.py --all
```
