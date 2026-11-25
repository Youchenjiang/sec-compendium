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

### 7. [PR Review Tool](pr_tool.py) (PR 審查、診斷與最終驗收工具)
- **路徑**：`security/tools/pr_tool.py`（搭配 `pr_audit.py`、`pr_verification.py`、`pr_reports.py`、`sonar_audit.py`、`gh_guard.py`、`process_guard.py`）
- **來源**：移植自 Clickra 倉庫的 `scripts/pr_tool.py`（Apache-2.0）；只保留審查與驗收功能。建立 PR 與 PR 說明檢查仍用 `pr_helper.py`，推送仍由人明確核准後手動執行。
- **原則**：除了 `resolve` 以外全部唯讀；`resolve` 一次只處理一個 thread，預設只預覽，需 `--execute --authorize <PR>:<thread>`；絕不發表或修改留言；不為了讓 PR 變綠而關掉還沒修好的問題。
- **子命令**：
  - `status` / `review`：PR 狀態、CI 彙總與所有未解決 review thread（DeepSource 留言只顯示標題）。
  - `audit [--json] [--sonar]`：逐頁讀取 inline 留言、一般留言與 review 摘要，不改變任何審查狀態。
  - `sonar [--json]`：列出 SonarCloud 該 PR 的 open/confirmed issues 與 quality gate。
  - `diagnose [--reports failed|all]`：讀取失敗 check 的 log、GitHub Check Run 摘要與 DeepSource 行內發現。
  - `verify`：唯讀最終驗收；確認 PR HEAD 等於遠端分支 SHA，盤點 review threads、SonarCloud issues 與必要 CI checks，任一未通過即回傳非 0。
  - `body --output <新檔>`：把既有 PR 說明匯出成新檔（不覆寫既有檔案）。
  - `resolve <PR> --thread <PRRT_...>`：預覽或在明確授權下解決單一已驗證修好的 thread。
- **SonarCloud 專案**：依序取 `SONAR_PROJECT_KEY`、`sonar-project.properties` 的 `sonar.projectKey`、`owner_repo`；私有專案設 `SONAR_TOKEN`。
- **必要 checks**（`pr_verification.REQUIRED`）：PR and commit policy、Documentation & Playbooks Quality Audit、TruffleHog Secrets Scan、DeepSource: Secrets、SonarCloud、SonarCloud Code Analysis；有 `.py` 變更時另需 DeepSource: Python。缺少或被略過的必要 check 一律視為未通過。

### 8. Dual-Profile Collab Bus (`collab_bus.py` / `collab_race.py` / `collab_watch.py` / `collab_protocol.py` / `collab_host_watch.py`)
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
  - **Secret boundary**：plaintext password/token/session secret/private key 不得進 tracked `.collab`，也不得進 `.collab/runtime/`。Race 可用 `secret_ref + secret_sha256 + secret_exact` 將 exact secret 標成 READY，但 event/board 只保存 redacted host-local reference 與 hash。
  - **Canonical naming / review linkage**：task=`Txxx_TYPE.md`、finding=`FINDING_Txxx.md`、review=`REVIEW_Txxx.md`；`REVIEW` task 必須以 `--review-target-finding FINDING_Txxx` 綁定既有 finding，且 review output 的 `對應 Finding` 必須完全一致。
  - **MCP bridge（`mcp` 子命令）**：以 `collab_bus.py mcp {list,tools,call}` 作為協作執行路徑的 MCP 入口；服務端清單、金鑰變數名與 runner 均登載於 `.agent/mcp/registry.json`，可由 session 直接呼叫（例：`semgrep` 掃碼、`cve-mcp-server` 查 CVE/EPSS/KEV）。實作見 `collab_mcp.py`。
  - **常駐 worker-host watcher（`collab_host_watch.py`）**：worker 主機不用逐 session 手動啟動。supervisor 自動掃描 task tree 中 `Session-H2-*`（可用 `--prefix` / `COLLAB_HOST_SESSION_PREFIX` 調整）的 assignee，對每個 session 維持一個 watcher pass，並週期性重新掃描，使主機一新派工的 `Session-H2-Foo` **無須重啟即被接收**；預設 `--transport file`，確保 ACK 與 handoff 不依賴 composer。`--worker-command` 會在每次新 handoff 寫出後自動呼叫 worker（封包路徑接在指令後），接上 agent CLI 即可自動產出 finding/review；未設定時僅排入 inbox 並提示。

---

#### Race profile (`collab_race.py`)

競賽 Race profile 沿用 governed task / hash / handoff，不另建第二套 transport。差別是 task 以 **Investigation Lane** 分工，一個 lane 可同時覆蓋多個 question；Worker 找到一題就把 append-only answer event 發到 `.collab/runtime/race/`，不等待 `DONE`。

核心規則：

- `Execution Profile: race` 必須同時有 `Lane ID: LNN`；舊 task 缺欄位視為 `governed`。
- `REVIEW` 不能是 race lane；時間敏感的衝突驗證用 `VERIFY` lane。
- auto READY = high confidence + 至少 2 個 evidence reference + 無 semantic/review risk；否則 CANDIDATE。
- secret-valued答案使用 `--secret-ref --secret-sha256 --secret-exact`，不得用 `--answer` 把 plaintext 帶進 runtime。
- 相同 actor/task/question 的完全相同 answer/evidence/state 重複發布為 idempotent no-op。
- 不同 lane 的不同答案自動 `CONFLICT`；`review-queue` 只列需要額外確認者。
- Lead-only submission state machine：`READY → SUBMITTED → ACCEPTED | REJECTED`。
- `SUBMITTED/ACCEPTED` 鎖定；`REJECTED` 可由新 evidence 重開。
- `SESSION_CLOSED` 是硬 publication barrier；close 後答案不可再改 benchmark score。
- 外部 lane 超過 worker START SLO 時用 `watchdog --assist-overdue`；Lead 代打前必須先有 `LANE_ASSISTED`，answer 會記錄精確 `assist_event_id`。Lead 自己持有的 lane 則在 dispatch 時自動 ACK→START。
- task `ACK/START/DONE` 仍保留完整 audit trail；Race 只讓答案熱路徑不再等待 terminal lifecycle。
- `board --at <elapsed>` 可重建 cutoff；`metrics` 直接報 first READY、50%/80%/100% milestone、15m/30m readiness 與 worker START SLO breach。
- `race doctor` 驗 lane/task SHA-256、assignee、question scope、answer evidence、temporal Lead-assist provenance、preflight 與 close barrier。

~~~bash
python security/tools/collab_race.py preflight --case C01_BottleOut --lead-session Session-Antigravity --image <E01> --dfir-python <pinned-python>
python security/tools/collab_race.py open --case C01_BottleOut --lead-session Session-Antigravity --budget-minutes 30 --worker-start-slo-seconds 60 --require-dfir-preflight
python security/tools/collab_race.py lane --case C01_BottleOut --lead-session Session-Antigravity --lane-id L01 --task-id T101 --type TRIAGE --target-role ROLE_01_TRIAGE_HUNTER --assignee-session Session-C01-Triage --execution-environment portable_text_any --questions Q01,Q03,Q06 --domain execution-registry --objective "Resolve execution questions."
python security/tools/collab_race.py answer --case C01_BottleOut --task-id T101 --session Session-C01-Triage --question Q03 --answer "example.exe" --confidence high --evidence "Prefetch: EXAMPLE.EXE-...pf" --evidence "UserAssist: example.exe"
python security/tools/collab_race.py watchdog --case C01_BottleOut --lead-session Session-Antigravity --assist-overdue
python security/tools/collab_race.py board --case C01_BottleOut
python security/tools/collab_race.py board --case C01_BottleOut --at 15m
python security/tools/collab_race.py review-queue --case C01_BottleOut
python security/tools/collab_race.py metrics --case C01_BottleOut
python security/tools/collab_race.py close --case C01_BottleOut --lead-session Session-Antigravity
python security/tools/collab_race.py doctor --case C01_BottleOut
~~~

預設效能目標是 30 秒完成 routing、60 秒內外部 lane 真正 START、3 分鐘內第一個 candidate、一般小題 5 分鐘內 READY、15 分鐘 70–80% ready。這套 hot path 已用真實 blind benchmark 驗證：C01 修正前 baseline 為 **4/10 READY @ 30m**；修正後 C05 PaperGhost raw triage 為 **9/9 READY @ 671.470s、close @ 693.997s**，50%/80% 分別為 482.791s / 608.219s，doctor PASS。C05 仍有兩條外部 lane 超過 60s START SLO，所以 watchdog/Lead fallback 不能移除。跨主機 answer latency 只有在主機時鐘同步時才可視為精確執行秒數。

### 9. Race DFIR Query / Preflight (`dfir_query.py` / `ese_query.py`)

- **定位**：把 E01 / Windows triage bundle 的 parser readiness 移到 Race 計時前；比賽中不再臨時找 `fls/icat`、安裝 parser 或摸索 EWF loader。
- **已驗證 pinned Windows/Python 3.14 stack**：`dissect.target==3.20`、`dissect.esedb==3.18`、`colorama==0.4.6`，清單在 `requirements-dfir-race.txt`。
- **E01 fast path**：EWF logical stream 若 offset 0 已是 NTFS OEM ID，直接用 `NtfsFilesystem`；否則才做 volume-system discovery。
- **查詢能力**：directory/list/stat/extract、raw `$MFT` filename search、deleted MFT recovery、Registry、EVTX、SQLite、bounded pagefile/artifact search。
- **ESE**：`ese_query.py` 提供 bounded read-only tables/schema/records；preflight 一旦看到 `SRUDB.dat` 或 `Windows.edb` 而 ESE backend 不可用/版本不符，直接 fail closed。
- **安全性**：extract/recover 不覆寫既有 output；secret plaintext 不應由 query helper 寫進 repo/runtime。

~~~bash
# 完整 E01
python security/tools/dfir_query.py preflight --image <sample.E01>
python security/tools/dfir_query.py find-mft --image <sample.E01> --name Settings.sqlite
python security/tools/dfir_query.py search-file --image <sample.E01> --path /pagefile.sys --needle jailer

# KAPE / triage bundle
python security/tools/dfir_query.py preflight --evidence-root <TriageDir>
python security/tools/ese_query.py tables --database <SRUDB.dat>
python security/tools/ese_query.py records --database <Windows.edb> --table SystemIndex_PropertyStore --contains EXT-0419
~~~

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

# 10. MCP：呼叫單一工具（註冊表見 .agent/mcp/registry.json）
python security/tools/collab_bus.py mcp call --server cve-mcp-server \
  --tool lookup_cve --args '{"cve_id": "CVE-2021-44228"}'
python security/tools/collab_bus.py mcp call --server semgrep \
  --tool get_supported_languages

# 11. 常駐 worker-host watcher（主機二）：自動接收主機一派給 Session-H2-* 的工單
python security/tools/collab_host_watch.py --list-sessions
python security/tools/collab_host_watch.py --transport file --log .collab/runtime/host_watch.log
python security/tools/collab_host_watch.py --once   # 單次掃描（cron / Windows Task Scheduler）

# 12. 查看 PR 未解決的 review threads 與失敗 check 的原因 (唯讀)
python security/tools/pr_tool.py review 38
python security/tools/pr_tool.py diagnose 38

# 13. 合併前的唯讀最終驗收 (未通過時回傳非 0，並列出原因)
python security/tools/pr_tool.py verify 38

# 14. 預覽、再於明確授權後解決一個已驗證修好的 review thread (不留言)
python security/tools/pr_tool.py resolve 38 --thread PRRT_xxx
python security/tools/pr_tool.py resolve 38 --thread PRRT_xxx --execute --authorize 38:PRRT_xxx
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

---

## 🛰️ 常駐 Worker-Host Watcher（主機二）

跨機演練證明了「派工 → 接收 → 回報」可行，但前提是主機二**有人記得為每個 session 開 watcher**。`collab_host_watch.py` 把這件事變成常駐：它自己判斷該盯哪些 session，主機一只要把 task 指派給任一 `Session-H2-*` 名稱，主機二就會自動 ACK 並排入 handoff。

```bash
# [主機二] 前景常駐（Ctrl-C 停止）
python security/tools/collab_host_watch.py --transport file

# 先看目前會被盯上的 session（唯讀）
python security/tools/collab_host_watch.py --list-sessions

# 背景常駐：把輸出留在 log，供稍後查驗
python security/tools/collab_host_watch.py --transport file \
  --log .collab/runtime/host_watch.log

# 只用單次掃描：適合 cron / Windows Task Scheduler
python security/tools/collab_host_watch.py --once

# 接上 worker：每寫出一份新 handoff 就呼叫你的 agent CLI（路徑會附在指令後）
python security/tools/collab_host_watch.py --transport file \
  --worker-command <your-agent-cli> --worker-arg <agent-flag>
```

**行為**：
- **自動探索**：從 task tree 的 `Assignee Session`、既有 watcher state、以及 inbox 目錄聯集出所有 `Session-H2-*`；`--prefix`（或環境變數 `COLLAB_HOST_SESSION_PREFIX`）可改前綴。
- **無須重啟**：每 `--rescan-interval`（預設 15s）重新探索，新派工的 `Session-H2-Foo` 會自動被納入。
- **故障隔離**：單一 session 的任務不合規（例如 host-local gateway 任務落到遠端節點）只會被跳過並記 log，不會拖垮其他 session。
- **ACK 不依賴 browser**：預設 `--transport file`，先送 `ACK` 再寫持久化 handoff；互動式 composer 可用與否都不影響交付。
- **產生工件**：watcher 只負責收單、ACK、排入 inbox。真正的 finding/review 由 `--worker-command` 接上的 agent 產出；未設定時，人工或另一個 agent 用 `collab_bus.py inbox --session <S> --show` 消費即可。

> **單一 writer 提醒**：`watchers/<session>.json` 會跨機同步，因此**同一個 session 名稱只能在一台主機執行**。切勿在兩機同時開同名 watcher。

> **常駐方式**：Windows 可用 Task Scheduler 定期跑 `--once`；Linux/macOS 可 `nohup python ... &` 或 systemd service。
