# 🌐 多 Agent Session 階層協同作戰手冊 (Hierarchical Multi-Agent Framework)

> **版本**：v2.3 (Governed Case Bus Edition)
> **適用場景**：HITCON Cyber Range / CTF 主機鑑識與應急響應  
> **核心設計**：以 **case-centric、single-writer、evidence-first** 為核心；`.collab/cases/` 是正式 task/evidence 的唯一權威總線。每個 case 只有一個 Lead Session，專項 Session 回傳 finding/review；另由一個 Global Coordinator 維護全域 scoreboard。`.collab/runtime/` 只承載可丟棄的事件與 handoff transport，不是第二套 evidence source of truth。

### Canonical source-of-truth precedence

遇到跨文件狀態不一致時，依下列權威順序判定，不以 `MEMORY.md` 或口頭紀錄覆蓋現行治理資料：

1. `CASE_STATE.md`：Case ownership、已接受的 evidence-backed facts 與 case 執行狀態。
2. `tasks/Txxx_TYPE.md`：發布後 immutable 的任務輸入、唯一 assignee 與 execution environment。
3. `.collab/runtime/events/`：task runtime lifecycle；只記協作執行狀態，不構成答案證據。
4. `findings/` / `reviews/`：Worker / Reviewer 的 governed evidence output。
5. `questions.md`：答案生命週期與人類平台提交結果。
6. `SCOREBOARD.md`：Global Coordinator 維護的跨 case 摘要；不得反向覆蓋 case source of truth。
7. `MEMORY.md`：歷史與操作經驗，不是現行 ownership、task、answer 或 runtime 狀態的權威來源。

---

## 1. 核心架構：一主多從的階層代理體系

無論是在單機多 Session 或跨實體主機執行，正式 task/evidence 都只透過 `cases/<CaseID>/tasks/`、`findings/`、`reviews/` 交換。`.collab/runtime/inbox/` 是 browser-free 的暫態 handoff transport，可刪除、可重建，不得視為第二套 task/evidence storage。

```mermaid
flowchart TD
    User["人類總指揮 / 最終提交員"] <==> Lead["Case Lead<br/>單一 case writer"]
    Lead -->|建立 immutable task| T["cases/Cxx/tasks/Txxx_TYPE.md"]
    T --> Worker["Triage / Reverse / Specialist"]
    Worker -->|只寫自己的成果| F["cases/Cxx/findings/FINDING_Txxx.md"]
    F --> Reviewer["Independent Reviewer"]
    Reviewer -->|需要時獨立審查| R["cases/Cxx/reviews/REVIEW_Txxx.md"]
    F --> Lead
    R --> Lead
    Lead --> S["CASE_STATE.md"]
    Lead --> Q["questions.md"]
    Lead --> Coordinator["Global Coordinator"]
    Coordinator --> B["SCOREBOARD.md"]
    Q -->|SUBMITTED / ACCEPTED / REJECTED 由人工回報平台結果| User
```

---

## 2. 角色分工矩陣 (Who Does What)

| 代理人角色 | 能力需求 | 核心職責 | 寫入邊界 |
| :--- | :--- | :--- | :--- |
| **Main Agent / Case Lead** | 全局推理、終端操作、工件整合 | 對被指派 case 拆題、建立 task、彙整 finding/review、維護答案生命週期 | 只寫自己 case 的 `CASE_STATE.md`、`questions.md`、`tasks/`；若兼任 Global Coordinator 才寫 `SCOREBOARD.md` |
| **Triage Hunter** | 長文本檢索、異常篩選、快速 evidence triage | DISCOVERY / TRIAGE / VERIFY 任務；允許指出題目候選集合之外的新線索 | 只寫自己對應的 `findings/` |
| **Reverse Engineer** | 程式碼推理、去混淆、二進位分析 | REVERSE 任務；還原邏輯並提供可重現證據 | 只寫自己對應的 `findings/` |
| **Independent Reviewer** | 獨立驗證、反例與 false-positive 排除 | REVIEW 任務；檢查證據、因果、格式與替代解釋 | 只寫自己對應的 `reviews/` |
| **人類選手** | 平台互動與最終裁決 | 實際提交答案，將平台 ACCEPTED / REJECTED 結果回報 Main | 不直接改協作狀態檔，避免多 writer |

### Reasoning Effort Policy（Canonical）

子 Agent / Worker 的推理強度由 Case Lead 依任務性質指定；**不得把最高推理強度當作預設值**。預設配置如下：

| 角色 / 任務 | 預設 reasoning effort | 使用原則 |
| :--- | :--- | :--- |
| **Mechanical checker / metadata / 格式檢查** | `low` 或 `medium` | 規則明確、輸入輸出 deterministic；避免不必要的長推理。 |
| **Triage Hunter** | `medium` | 大量篩選、IOC 比對、候選縮小；優先速度與 evidence coverage。 |
| **Reverse Engineer** | `high` | 去混淆、程式邏輯、資料流、跨工件推理需要較深 reasoning。 |
| **Independent Reviewer** | `high` | 必須主動尋找反例、替代解釋與 evidence gap，不可只重述 finding。 |
| **Case Lead** | `high` | 負責拆題、跨 finding/review 整合與 `VERIFIED` gate。 |

升級規則：

1. `xhigh` **不是預設值**；只有在 `high` 已回報具體 blocker，且 blocker 明確屬於推理深度問題（例如複雜逆向、證據彼此矛盾、需要跨多條因果鏈消歧）時，才針對**單一 atomic task** 升級。
2. `max` / `ultra` **預設禁止自動使用**；只有人類明確要求，或 Case Lead 已有可稽核理由且人類同意時才啟用。
3. 不得因為 Worker「回答不合預期」就直接提高 reasoning effort；先判斷是 **evidence 缺失、task scope 不清、工具不可用、還是真的推理不足**。
4. 同一 task 若需重跑，必須記錄重跑原因；不得用不同強度反覆生成答案直到出現想要的結論。
5. Reasoning effort 只影響投入深度，**不能取代 evidence contract、review gate 或平台 ACCEPTED 結果**。

實務預設：`Triage=medium`、`Reverse=high`、`Reviewer=high`、`Case Lead=high`。若只是格式、metadata 或 deterministic validation，優先降到 `low/medium`。

### 節點能力契約 (Execution Capabilities)

`.collab` 只治理「這個 task 需要哪一類執行能力」，不保存實體主機名稱、VM 位址、工具路徑或 credential 位置。這些操作細節只有一份權威來源，避免協作規則與環境文件彼此漂移。

| Execution Environment | 能力契約 | 可執行節點 |
| :--- | :--- | :--- |
| `host_local_gateway` | 需要 Primary Analysis Gateway 才具備的本地標本、VM、特殊工具或高資源分析能力 | watcher 必須明確以 `primary` node class 執行 |
| `portable_text_any` | task 已被縮成可攜的文字、CSV、JSON、反編譯原始碼或其他不依賴 gateway 的輸入 | `primary` / `remote` 皆可 |

Watcher 的 `--node-class auto` 採 fail-closed：只有環境變數 `COLLAB_NODE_CLASS=primary` 明確宣告時才視為 Primary；未設定時一律當作 `remote`。具體主機、VM、工具、連線方式與 Pre-flight 規則以 tracked 的 [Holmes2026_雙機鑑識分工與作戰SOP.md](../tracks/lab/hitcon_range/playbooks/Holmes2026_雙機鑑識分工與作戰SOP.md) 為權威來源；本機若另有 Workspace Skill `hitcon-dfir-vm-ops`，可作操作輔助，但 `.collab` 不依賴它才能成立。


---

## 3. 任務與答案生命週期

### Task Types
- `DISCOVERY`：開放式探索；不得限制 Worker 只能從預設候選中選答案。
- `TRIAGE`：快速縮小範圍並列出可疑標的與證據。
- `VERIFY`：驗證既有候選；可使用 A/B/C，但 Worker 必須能回報「皆非」。
- `REVERSE`：去混淆、逆向、解碼、結構還原。
- `REVIEW`：由獨立 Session 檢查 finding、替代解釋與反證。

### Task contract
1. Case Lead 透過 bus 建立 `tasks/Txxx_TYPE.md` 後視為 **immutable**；Worker 不修改 task 狀態或內容。
2. Task 以 `target_role` 描述能力，以 `assignee_session` 指向**一個具體 Session**。只有 `assignee_session == 當前 Session` 才能 ACK / START / 產出 governed output；角色相同不構成接單權限。
3. Worker 僅新增自己的 `findings/FINDING_Txxx.md`；Reviewer 僅新增自己的 `reviews/REVIEW_Txxx.md`。
4. Case Lead 讀取成果後，唯一負責更新該 case 的 `CASE_STATE.md` 與 `questions.md`；Global Coordinator 根據各 Lead 回報唯一更新 `SCOREBOARD.md`。
5. **執行環境契約（`execution_environment` / Markdown label: `Execution Environment`）**：
   - `host_local_gateway`：需要 Primary Analysis Gateway 專屬本地資源或工具的工作；只允許 node class 為 `primary` 的 watcher 接收。
   - `portable_text_any`：已抽取為純文字、CSV、JSON、反編譯原始碼之任務，**任何主機節點皆可接單處理**。
   - 新 task 的 `execution_environment` 是**強制治理欄位**：建立、驗證、watcher/handoff 與 `doctor` 必須拒絕缺漏或未知值。舊版 task 只有在存在唯一 `DISPATCHED` event、issuer 正確且目前 task hash 與該事件錨點完全一致時，才允許以 legacy 相容模式讀取；不得靠省略 `Protocol Contract` 自行降級。舊 task 不得原地補欄位，後續工作另發新 task。
6. **Review provenance**：`REVIEW` task 必須以 `Review Target Finding` 精確指向既有 `FINDING_Txxx`；review output 的 `對應 Finding` 必須完全相同，validator 才允許 `DONE`。

> **檔名契約**：CLI 建立的 task 使用 `Txxx_TYPE.md`；governed output 使用 `findings/FINDING_Txxx.md` 或 `reviews/REVIEW_Txxx.md`。檔案內容中的 `對應任務 / 對應 Task` 一律填精確 `Txxx`，不可填 `TASK_Txxx`。

### Answer lifecycle
`OPEN → CANDIDATE → VERIFIED → SUBMITTED → ACCEPTED | REJECTED`

- `OPEN`：尚無候選答案。
- `CANDIDATE`：已有答案，但 evidence contract 尚未滿足。
- `VERIFIED`：證據可重現、格式已檢查，Main 判定可提交；**不代表平台已接受**。
- `SUBMITTED`：人類已提交，等待平台結果。
- `ACCEPTED`：平台明確判定正確；只有此狀態計入 scoreboard 已解題數。
- `REJECTED`：平台明確判定錯誤；保留歷史 evidence，回到新一輪調查。

### Runtime communication lifecycle

正式 evidence 仍以 tracked `task / finding / review / questions` 為準；`.collab/runtime/` 只承載 Git-ignored、**仍會被目前 Google Drive 工作區同步到其他主機**的 ephemeral coordination data：

`DISPATCHED → ACK → START → DONE | ERROR`

Runtime lifecycle 必須按 protocol state machine 驗證；`DONE` / `ERROR` 都是 terminal state，不得再退回 `START`。若 `ERROR` 後仍需重做，Case Lead 另發新 task，保留原 failure provenance。跨主機不得以本機 wall-clock / `time_ns()` 直接推導因果順序；immutable task hash 只接受該 task 唯一的 `DISPATCHED` event 作基準，重複 dispatch 或 issuer mismatch 都是 protocol error。

`ACK` 只表示 exact-assignee watcher 已接受這筆 task delivery；**不代表 browser/CLI worker 已成功啟動**。只有 `START` 才代表 worker 已真正開始執行，因此 Lead 不得把停在 `ACK` 的 task 當作「分析已開工」。

若 worker 在 **ACK 前** 即因 orchestrator / browser / transport bootstrap 失敗，Case Lead 必須記錄 `DISPATCH_FAILED`，不可讓 task 永遠停留在模糊的 `DISPATCHED`：

```bash
python security/tools/collab_bus.py dispatch-failed \
  --case C03_MemoryDump --task-id T900 \
  --session Session-Antigravity \
  --message "Worker bootstrap failed before ACK"
```

`DISPATCH_FAILED` 只允許 Case Lead 在尚無任何 ACK 時寫入；已有 ACK 後的執行失敗應由 Worker 使用 `ERROR`。

另可在 Case Lead 與唯一 Assignee Session 間交換 `QUESTION / REPLY / NOTE`。Runtime event **不是答案證據，也不能直接把 question 升為 VERIFIED/ACCEPTED**。

```text
Case Lead       Worker / Reviewer
   |  DISPATCHED      |
   |----------------->|
   |       ACK        |
   |<-----------------|
   |      START       |
   |<-----------------|
   |  QUESTION/REPLY  |
   |<---------------->|
   |       DONE       |
   |<-----------------|
```

統一使用：

```bash
# Case Lead 建立 immutable task（actor 必須等於 CASE_STATE 的 Lead Session）
python security/tools/collab_bus.py new-task \
  --case C01_BottleOut \
  --actor-session Session-Antigravity \
  --task-id T001 \
  --type TRIAGE \
  --target-role ROLE_01_TRIAGE_HUNTER \
  --assignee-session Session-C01-Triage \
  --execution-environment portable_text_any \
  --question Q01 \
  --title "OpenVPN endpoint triage" \
  --objective "Find the exact remote OpenVPN IP:Port from the supplied evidence."

# Worker 啟動 watcher；看到新 task 時 watcher 自動回 ACK
python security/tools/collab_watch.py \
  --session Session-C01-Triage \
  --case C01_BottleOut

# 只有已確認具備 Primary Analysis Gateway 能力的節點才明確宣告 primary
python security/tools/collab_watch.py \
  --session Session-Gateway-Triage \
  --case C01_BottleOut \
  --node-class primary

# Worker 正式開始
python security/tools/collab_bus.py start \
  --case C01_BottleOut --task-id T001 --session Session-C01-Triage

# 需要澄清時，走 task-scoped QUESTION / REPLY
python security/tools/collab_bus.py send \
  --case C01_BottleOut --task-id T001 \
  --from-session Session-C01-Triage --to-session Session-Antigravity \
  --kind QUESTION --message "Should the answer include protocol prefix?"

# 建立正確 finding/review 骨架，填完後再送 DONE
python security/tools/collab_bus.py init-output \
  --case C01_BottleOut --task-id T001 --session Session-C01-Triage

python security/tools/collab_bus.py done \
  --case C01_BottleOut --task-id T001 --session Session-C01-Triage \
  --message "Finding ready for Lead review"

# Lead / Worker 隨時回看狀態與 event history
python security/tools/collab_bus.py status --case C01_BottleOut
python security/tools/collab_bus.py events --session Session-Antigravity --case C01_BottleOut
python security/tools/collab_bus.py doctor
```

`DONE` 有三道硬門檻：task hash 必須與唯一 `DISPATCHED` event 錨定值一致、governed output 必須存在、output contract 必須填完整。只建立空模板不能宣告 DONE。

### Browser-free handoff transport

Watcher 偵測 exact-assignee task 後會 ACK，並確保 `.collab/runtime/inbox/<Session>/<CaseID>/<TaskID>.json` 存在可重放 handoff；若 handoff 寫入失敗，watcher 下次循環會從 `ACK` 狀態重試。這個 inbox 只是 transport fallback：

- `--transport auto`：有 `--exec-program` 時嘗試互動式 agent，失敗或逾時仍保留 file handoff。
- `--transport agent`：要求互動式 agent 路徑；若不可用仍以 file handoff 保底。
- `--transport file`：完全不啟動互動式 agent，只產生 CLI handoff。
- `collab_bus.py inbox --session <Session> --show`：查看仍可執行的 handoff。
- task 進入 terminal state 後，對應 handoff 必須被消費或從預設 inbox 隱藏，避免 stale replay。

---

## 4. 協作安全與證據鐵律

1. **鐵律 1：大檔留在本機 SSD，雲端硬碟只同步「純文字情報」**：
   - 10GB+ 的原始 E01、Memory Dump 放在本地硬碟，**嚴禁**搬進 `.collab/`。
   - `.collab/` 只放 Markdown、CSV、JSON，檔案幾十 KB，雲端硬碟秒級同步，絕不卡頻寬。
2. **鐵律 2：每個檔案只有一個 Writer**：
   - Case Lead only：自己 case 的 `CASE_STATE.md`、`questions.md`、`tasks/`。
   - Global Coordinator only：`SCOREBOARD.md`。
   - Worker only：自己被指派 task 對應的 `findings/`。
   - Reviewer only：自己被指派 review 對應的 `reviews/`。
   - 任務一旦發布即不可由 Worker 原地改狀態，避免同步衝突與 provenance 被覆寫。
3. **鐵律 3：Evidence before confidence**：
   - 每個候選答案至少要記錄 artifact/source、取得方法、直接 observation、重現步驟與已知限制。
   - `confidence` 只能摘要證據強度，不可取代 evidence；「模型覺得很像」不是證據。
4. **鐵律 4：Secrets 不進 Git，也不進 cloud-synced runtime**：
   - 真實密碼、token、session secret、private key 不得寫入 tracked `.collab` 檔案。
   - `.collab/runtime/` 雖被 Git ignore，但目前會由 Google Drive 跨機同步，因此**只能放非敏感 coordination data**，不得存放 plaintext secret。
   - 真實 secret 必須留在 **cloud-synced workspace 外**的 host-local secret store（例如作業系統憑證儲存，或由操作者從同步目錄外注入的環境變數）；tracked finding/questions 與 runtime event 只保存 `[REDACTED: local secret ref]` 類型的引用。
   - CTF 公開 flag 或題目專用、賽後失效的 credential 是否公開，仍由人類選手決定；預設視為 secret。
5. **鐵律 5：以 watcher + bus CLI 取代口頭猜測**：
   - Session 以 `collab_watch.py --session <SessionName>` 收件；只處理 `assignee_session` 精確等於自己的 task，不以角色或「最新 task」猜測工作。
   - ACK / START / DONE / ERROR / QUESTION / REPLY / NOTE 一律透過 `collab_bus.py` 留下 immutable runtime event。
   - 若 watcher 通知漏掉，可用 `collab_bus.py events` 回看，不需要重新派 task。
6. **鐵律 6：節點環境感知與特權邊界（Node Environment Awareness）**：
   - `host_local_gateway` task 只能由明確宣告為 `primary` 的節點執行；未宣告的 watcher 預設視為 `remote`。
   - `remote` 節點只執行 `portable_text_any`；若分析途中需要 gateway 專屬資源，使用 task-scoped `QUESTION` 請求 Lead / gateway 匯出可攜工件。
   - 主機、VM、工具、連線命令與 credential 配置不在 `.collab` 重複定義，一律以 tracked 作戰 SOP 為準；本機 Workspace Skill 只能作操作輔助。

---

## 5. 賽前啟動與角色認領 SOP (How to Bootstrap Roles)

在比賽開始或開啟各個 AI Session 時，按照以下極簡 SOP 快速完成角色載入與待命：

```mermaid
flowchart LR
    IDE0["【Session 0】Main Agent<br/>載入 ROLE_00_MAIN_ENGINE.md"]
    IDE1["【Session 1】Triage Hunter<br/>載入 ROLE_01_TRIAGE_HUNTER.md"]
    IDE2["【Session 2】Reverse Engineer<br/>載入 ROLE_02_REVERSE_ENGINEER.md"]
    IDE3["【Session 3，可選】Independent Reviewer<br/>載入 ROLE_03_DEVILS_ADVOCATE.md"]

    IDE0 -->|發布任務| BUS[".collab/cases/ 總線"]
    BUS -->|讀取任務| IDE1 & IDE2 & IDE3
```

### 具體操作步驟：
1. **Session 0 (Main Agent)**：
   - 傳送提示詞：`請閱讀 .collab/roles/ROLE_00_MAIN_ENGINE.md，擔任主引擎領航員，準備攻堅 C01 大題。`
   - 主引擎啟動，初始化環境並開始拆解任務。
2. **Session 1 (Triage Hunter)**：
   - 傳送提示詞：`請閱讀 .collab/roles/ROLE_01_TRIAGE_HUNTER.md，擔任初篩排查專家。回覆確認就緒。`
   - 子代理 1 回覆：「子代理 1 就緒，待命接單」，原地待命。
3. **Session 2 (Reverse Engineer)**：
   - 傳送提示詞：`請閱讀 .collab/roles/ROLE_02_REVERSE_ENGINEER.md，擔任代碼逆向專家。回覆確認就緒。`
   - 子代理 2 回覆：「子代理 2 就緒，待命接單」，原地待命。
4. **開跑作戰**：
   - 每個 Session 啟動自己的 watcher，例如：`python security/tools/collab_watch.py --session Session-C01-Triage --case C01_BottleOut`。
   - Case Lead 使用 `collab_bus.py new-task` 派工；watcher 偵測 exact assignee 後自動 ACK。
   - Session 只能處理 `assignee_session` 明確指向自己的 task；不要以「未認領」或「最新檔案」自行搶單，避免重複分析與同步競態。
