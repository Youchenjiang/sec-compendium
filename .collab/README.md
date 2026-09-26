# 🌐 多 Agent Session 階層協同作戰手冊 (Hierarchical Multi-Agent Framework)

> **版本**：v2.2 (Governed Case Bus Edition)
> **適用場景**：HITCON Cyber Range / CTF 主機鑑識與應急響應  
> **核心設計**：以 **case-centric、single-writer、evidence-first** 為核心；`.collab/cases/` 是唯一協作總線。每個 case 只有一個 Lead Session，專項 Session 回傳 finding/review；另由一個 Global Coordinator 維護全域 scoreboard。

---

## 1. 核心架構：一主多從的階層代理體系

無論是在單機多 Session 或跨實體主機執行，協作都只透過 `cases/<CaseID>/tasks/`、`findings/`、`reviews/` 交換文字工件；不再維護第二套 inbox/outbox。

```mermaid
flowchart TD
    User["人類總指揮 / 最終提交員"] <==> Lead["Case Lead<br/>單一 case writer"]
    Lead -->|建立 immutable task| T["cases/Cxx/tasks/Txxx.md"]
    T --> Worker["Triage / Reverse / Specialist"]
    Worker -->|只寫自己的成果| F["cases/Cxx/findings/Fxxx.md"]
    F --> Reviewer["Independent Reviewer"]
    Reviewer -->|需要時獨立審查| R["cases/Cxx/reviews/Rxxx.md"]
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

---

## 3. 任務與答案生命週期

### Task Types
- `DISCOVERY`：開放式探索；不得限制 Worker 只能從預設候選中選答案。
- `TRIAGE`：快速縮小範圍並列出可疑標的與證據。
- `VERIFY`：驗證既有候選；可使用 A/B/C，但 Worker 必須能回報「皆非」。
- `REVERSE`：去混淆、逆向、解碼、結構還原。
- `REVIEW`：由獨立 Session 檢查 finding、替代解釋與反證。

### Task contract
1. Main 建立 `tasks/Txxx_<type>_<slug>.md` 後視為 **immutable**；Worker 不修改 task 狀態或內容。
2. Task 以 `target_role` 描述能力，以 `assignee_session` 指向**一個具體 Session**；不允許多 Session 同時把同一 task 視為自己的工作。
3. Worker 僅新增自己的 `findings/Fxxx_*.md`；Reviewer 僅新增自己的 `reviews/Rxxx_*.md`。
4. Case Lead 讀取成果後，唯一負責更新該 case 的 `CASE_STATE.md` 與 `questions.md`；Global Coordinator 根據各 Lead 回報唯一更新 `SCOREBOARD.md`。

### Answer lifecycle
`OPEN → CANDIDATE → VERIFIED → SUBMITTED → ACCEPTED | REJECTED`

- `OPEN`：尚無候選答案。
- `CANDIDATE`：已有答案，但 evidence contract 尚未滿足。
- `VERIFIED`：證據可重現、格式已檢查，Main 判定可提交；**不代表平台已接受**。
- `SUBMITTED`：人類已提交，等待平台結果。
- `ACCEPTED`：平台明確判定正確；只有此狀態計入 scoreboard 已解題數。
- `REJECTED`：平台明確判定錯誤；保留歷史 evidence，回到新一輪調查。

### Runtime communication lifecycle

正式 evidence 仍以 tracked `task / finding / review / questions` 為準；`.collab/runtime/` 只承載 Git-ignored、可跨同步目錄傳遞的 ephemeral event：

`DISPATCHED → ACK → START → DONE | ERROR`

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
  --question Q01 \
  --title "OpenVPN endpoint triage" \
  --objective "Find the exact remote OpenVPN IP:Port from the supplied evidence."

# Worker 啟動 watcher；看到新 task 時 watcher 自動回 ACK
python security/tools/collab_watch.py \
  --session Session-C01-Triage \
  --case C01_BottleOut

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

`DONE` 有三道硬門檻：task hash 不可自 DISPATCHED/ACK 後改變、governed output 必須存在、output contract 必須填完整。只建立空模板不能宣告 DONE。

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
4. **鐵律 4：Secrets 不進 Git**：
   - 真實密碼、token、session secret、private key 不得寫入 tracked `.collab` 檔案。
   - 需要跨 Session 暫存時只使用 Git 忽略的 `.collab/runtime/`，並在 tracked finding/questions 中以 `[REDACTED: runtime ref]` 指向。
   - CTF 公開 flag 或題目專用、賽後失效的 credential 是否公開，仍由人類選手決定；預設視為 secret。
5. **鐵律 5：以 watcher + bus CLI 取代口頭猜測**：
   - Session 以 `collab_watch.py --session <SessionName>` 收件；不要用「最新 task」猜測工作。
   - ACK / START / DONE / ERROR / QUESTION / REPLY / NOTE 一律透過 `collab_bus.py` 留下 immutable runtime event。
   - 若 watcher 通知漏掉，可用 `collab_bus.py events` 回看，不需要重新派 task。

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
