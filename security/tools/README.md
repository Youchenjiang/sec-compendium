# 🛠️ 資安作戰與自動化工具庫 (Security Tools)

本目錄收錄專案通用之資安作戰工具、白箱原始碼審計引擎與自動化品質檢驗腳本。

---

## 🧰 工具清單

### 1. [Code Auditor](code_auditor/README.md) (自動化白箱原始碼審計與 PoC 驗證引擎)
- **路徑**：`security/tools/code_auditor/`
- **定位**：全功能 PHP / 開源供應鏈安全審計與動態驗證引擎。
- **能力**：
  - 🔍 **SAST 靜態分析**：AST 語法樹追蹤與 38 條核心危險 Sink 偵測（RCE, SQLi, SSTI, Unserialize, 任意讀寫）。
  - ⚡ **PoC 產生器**：自動根據 Sinks 與資料流合成漏洞利用代碼。
  - 🐳 **Docker 沙箱驗證**：在乾淨的隔離容器中即時動態驗證 Exploit 是否有效。
  - 🔌 **模組化平台介面**：支援本機離線審計與 CTF/Wargame 遠端競賽自動化。
  - 📐 **方法論指導**：👉 [全方位安全審計與攻防方法論 (audit_methodology.md)](code_auditor/audit_methodology.md)

### 2. [Unified Playbook Validator](validate_playbooks.py) (攻防手冊雙軌全能檢驗工具)
- **路徑**：`security/tools/validate_playbooks.py`
- **定位**：一鍵整合執行藍隊 (107 篇) 與紅隊 (110 篇) 實戰手冊規範稽核，並對全專案所有 Markdown 文檔執行跨模組超連結防護稽核。
- **參數支援**：`--all` (預設), `--blue`, `--red`, `--links-only`。

### 3. [Blue Team Playbook Validator](validate_blue_team_playbooks.py) (藍隊原子實戰手冊檢驗工具)
- **路徑**：`security/tools/validate_blue_team_playbooks.py`
- **定位**：自動化檢查 `blue_team/playbooks` 107 篇實戰手冊之七大黃金規格關鍵字（案發現場破題、第一動~第五動、靶場實戰、過關驗收）、行數門檻 (>=200 行) 與藍隊內部連結。

### 4. [Red Team Playbook Validator](validate_red_team_playbooks.py) (紅隊特戰手冊檢驗工具)
- **路徑**：`security/tools/validate_red_team_playbooks.py`
- **定位**：自動化檢查 `red_team/playbooks` 110 篇特戰手冊之五動戰術結構、速查規範篇幅 (150~210 行) 與紅隊內部連結。

### 5. [Commit Policy & Atomic Linter](lint_commits.py) (提交規範與四權分立稽核工具)
- **路徑**：`security/tools/lint_commits.py`
- **定位**：本機端 Conventional Commits 與「四權分立（目的/功能/脈絡/治理）」原子化稽核工具，對齊 CI 政策守門標準。
### 6. [PR Helper & Validator](pr_helper.py) (PR 自動生成、結構驗證與安全提交工具)
- **路徑**：`security/tools/pr_helper.py`
- **定位**：自動解析 Conventional Commits 產出合規 PR 說明文檔，本機端先跑完 CI 守門員再使用 `--body-file` 提交，徹底避免 Windows PowerShell 跳脫截斷與標籤時間差紅燈。
- **子命令**：
  - `generate`：自動分析分支 Commit 產出符合 `.github/pull_request_template.md` 規範之 PR Markdown。
  - `lint`：校驗 PR Body 三大章節、標題長度與 Conventional Commits。
  - `create`：本地全套驗證通過後，一鍵建立帶有標籤之 GitHub Pull Request。

### 7. Governed Collab Bus (`collab_bus.py` / `collab_watch.py` / `collab_protocol.py`)
- **定位**：HITCON / CTF 多 Session 協作通訊層；tracked Markdown 保存正式 task/evidence，Git-ignored `.collab/runtime/` 保存 ephemeral events/handoffs。runtime 目前仍由 Google Drive 跨機同步，因此它**不是 secret store**。
- **核心保證**：
  - task 只有 Case Lead 能建立，且只有一個 `Assignee Session`。
  - `Target Role` 只描述能力；只有 `Assignee Session` 精確相符的 Session 能 ACK / START / 產出 output。
  - 新 task 必須含 `execution_environment`（Markdown: `Execution Environment`），合法值只有 `host_local_gateway` / `portable_text_any`；缺漏或未知值必須視為不合法 task。
  - watcher 只接 exact-assignee task，收到後自動送 `ACK`；`ACK` 只代表 delivery 已被 watcher 接受，只有 `START` 才代表 worker 真正開始執行。
  - 支援 `START / DONE / ERROR / QUESTION / REPLY / NOTE` immutable events。
  - `DONE` 會驗 task hash 與 finding/review output contract，禁止空模板或被改寫 task 假結案。
  - `doctor` 可檢查 task metadata、duplicate ID、runtime ignore 與 immutable hash。
  - **傳輸 fallback（browser-free）**：watcher 於 ACK 後確保可重放 handoff 封包存在於 Git-ignored `.collab/runtime/inbox/<Session>/<CaseID>/<TaskID>.json`；若寫入失敗，下輪會從 `ACK` 狀態重試。`--transport {auto,agent,file}` 可選互動式 agent（預設）或純檔案/CLI，`--exec-timeout` 逾時即自動退回封包。
  - **跨機同步韌性**：runtime 目錄實際靠雲端硬碟跨機同步（Drive 不遵守 `.gitignore`）；讀取器以 `is_sync_artifact()` 忽略驅動器產生的衝突副本／暫存碎片，`doctor` 會將其列為 WARN，確保同步競態不會被誤讀成正式 event/handoff。
  - **Secret boundary**：plaintext password/token/session secret/private key 不得進 tracked `.collab`，也不得進 `.collab/runtime/`；只傳遞 `[REDACTED: local secret ref]` 類型的 host-local reference。
  - **Canonical naming / review linkage**：task=`Txxx_TYPE.md`、finding=`FINDING_Txxx.md`、review=`REVIEW_Txxx.md`；`REVIEW` task 必須以 `--review-target-finding FINDING_Txxx` 綁定既有 finding，且 review output 的 `對應 Finding` 必須完全一致。
  - **MCP bridge（`mcp` 子命令）**：以 `collab_bus.py mcp {list,launch,tools,call}` 作為協作執行路徑的 MCP 入口；服務端清單、金鑰變數名與 runner 均登載於 `.agent/mcp/registry.json`，可由 session 直接呼叫（例：`semgrep` 掃碼、`cve-mcp-server` 查 CVE/EPSS/KEV）。實作見 `collab_mcp.py`；`mcp launch` 為離線檢視（傳輸、argv、金鑰名稱，永不輸出值）。
  - **節點型傳輸**：`placement.holder_class` 決定連線方式（`kali`→ssh、`flare_vm`→vmrun Guest Operations、`container`→`docker run -i`），MCP 客戶端仍只說 stdio；規劃在 `mcp_transports.py`，橋接器在 `.agent/mcp/tools/`，規範見 `.agent/mcp/README.md` §12。

---

## 🚀 常用指令速查

```bash
# 1. 執行雙軌實戰手冊全能自動化品質稽核 (預設執行藍隊、紅隊與全專案超連結防護)
python security/tools/validate_playbooks.py

# 2. 單獨執行藍隊實戰手冊品質稽核
python security/tools/validate_blue_team_playbooks.py
# 或
python security/tools/validate_playbooks.py --blue

# 3. 單獨執行紅隊特戰手冊品質稽核
python security/tools/validate_red_team_playbooks.py
# 或
python security/tools/validate_playbooks.py --red

# 4. 僅執行全專案 Markdown 跨模組超連結稽核
python security/tools/validate_playbooks.py --links-only

# 5. 執行本地白箱代碼審計 (純靜態掃描)
python -m security.tools.code_auditor.main --local-dir /path/to/target --scan-only

# 6. 執行本地審計並生成 Exploit
python -m security.tools.code_auditor.main --local-dir /path/to/target

# 7. 執行本地 Commit 規範與四權分立稽核
python security/tools/lint_commits.py --base origin/main

# 8. 自動產出當前分支之合規 PR 說明檔 (避免 PowerShell 跳脫字元問題)
python security/tools/pr_helper.py generate --base origin/main -o PR_BODY.md

# 9. 本地全套驗證並一鍵安全提交 PR (附帶必備標籤)
python security/tools/pr_helper.py create --title "feat(tools): add pr helper and validator" --label "documentation"
# 4. Collab bus 自我檢查
python security/tools/collab_bus.py doctor
# 5. 查看指定 Session 的 task
python security/tools/collab_bus.py list --session Session-C01-Triage
# 6. 啟動指定 Session watcher
python security/tools/collab_watch.py --session Session-C01-Triage --case C01_BottleOut

# 7. 無 browser 環境：純檔案/CLI 派工並消費 handoff inbox
python security/tools/collab_watch.py --session Session-C01-Triage --case C01_BottleOut --transport file
python security/tools/collab_bus.py inbox --session Session-C01-Triage --show

# 8. MCP：列出已註冊伺服器（離線）
python security/tools/collab_bus.py mcp list

# 9. MCP：活體 session 列出伺服器真的暴露的工具
python security/tools/collab_bus.py mcp tools --server semgrep

# 10. MCP：離線檢視某顆伺服器會怎麼被拉起（傳輸、argv、金鑰名稱；不輸出值）
python security/tools/collab_bus.py mcp launch --server semgrep

# 11. MCP：呼叫單一工具（註冊表見 .agent/mcp/registry.json）
python security/tools/collab_bus.py mcp call --server cve-mcp-server \
  --tool lookup_cve --args '{"cve_id": "CVE-2021-44228"}'
python security/tools/collab_bus.py mcp call --server semgrep \
  --tool get_supported_languages
```

---

## 🌐 跨機對手演練 (Cross-Host Two-Way Rehearsal)

驗證「主機一（Lead）派工 → 主機二（worker）接收、ACK 並完成 → 主機一收到回報」雙向暢通。前提：兩機共享同一雲端同步工作區（Drive 不遵守 `.gitignore`，故 `.collab/runtime/` 會跨機）。

> 單機腳本無法代替此演練：派工必須由主機一發出，回程必須由主機一確認；切勿把同機 loopback 冒充為跨機驗證。

```bash
# [主機一 · Lead] 派工（actor 必須是該 case 的 Lead Session）
python security/tools/collab_bus.py new-task \
  --case C03_MemoryDump --actor-session Session-Antigravity \
  --task-id T901 --type TRIAGE --target-role ROLE_01_TRIAGE_HUNTER \
  --assignee-session Session-C03-Triage \
  --execution-environment portable_text_any \
  --title "Cross-host bus rehearsal" \
  --objective "Confirm host1->host2 dispatch syncs in and host2 ACKs+completes." \
  --context "Rehearsal only; do not touch Q01-Q10."

# [主機二 · worker] 等 Drive 同步後接收（file transport 確保 browser 無關）
python security/tools/collab_watch.py --session Session-C03-Triage --case C03_MemoryDump --transport file --once
python security/tools/collab_bus.py inbox --session Session-C03-Triage --show
python security/tools/collab_bus.py start     --case C03_MemoryDump --task-id T901 --session Session-C03-Triage
python security/tools/collab_bus.py init-output --case C03_MemoryDump --task-id T901 --session Session-C03-Triage
# …填完 FINDING_T901.md 後…
python security/tools/collab_bus.py done --case C03_MemoryDump --task-id T901 --session Session-C03-Triage --message "rehearsal done"

# [主機一] 等回程同步後驗證
python security/tools/collab_bus.py events --session Session-Antigravity --case C03_MemoryDump --task-id T901
python security/tools/collab_bus.py status --case C03_MemoryDump
```

**通過判準**：主機一在 `events` 中看到 `ACK → START → DONE`，且 `status` 顯示 `DONE`；三方 event 的 `task_sha256` 一致，證明 immutable task 跨機未被改寫。
