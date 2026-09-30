# 04 — Execution Validation、Failure Paths 與 Stop Rules

## 目的

紅隊 operation 不能把「command 回傳 0」「工具印出 success」「session 有回應」直接當成 capability 成功。本文件定義 target-side validation、failure classification、retry/pivot 規則、stop condition 與 cleanup checkpoint，讓每個 action 都能被重播與審核。

---

## 1. Success 必須有 Observable

每個 action 在執行前先寫：

```text
Expected action
Expected target-side state change
Expected operator-visible result
Independent validation
Cleanup requirement
```

如果沒有預先定義 success observable，就很容易把工具自己的提示訊息誤當成功證據。

---

## 2. Success Validation Ladder

由低到高：

| Level | Validation | 意義 |
| :--- | :--- | :--- |
| 0 | Tool output only | 僅表示 client/tool 自己認為成功 |
| 1 | Protocol response | target/service 回傳符合預期 |
| 2 | Target-side state | target 上可觀察到受控 state change |
| 3 | Independent corroboration | 第二個 channel / telemetry 驗證同一 capability |

高影響 capability（privilege、remote admin、configuration change）優先要求 Level 2 以上。

---

## 3. Minimal Proof

Proof 應滿足：

- reversible
- synthetic
- low impact
- uniquely attributable to the test
- easy to clean
- enough to prove the capability

例如「可寫入」可用指定 marker object 證明，不需要改動真實業務資料。

---

## 4. Action Record

每次高價值 action 記錄：

| 欄位 | 內容 |
| :--- | :--- |
| Timestamp | 含 timezone |
| Operator | 執行者 |
| Target | host/app/service/object |
| Identity | 使用的 test identity / role |
| Technique | atomic playbook reference |
| Preconditions | 已驗證條件 |
| Action | command / GUI operation / API request |
| Expected observable | 成功應看到什麼 |
| Actual result | 實際看到什麼 |
| Validation level | 0–3 |
| Artifacts changed | files/process/config/session |
| Cleanup state | pending / complete / not required |

---

## 5. Failure Taxonomy

失敗至少分成：

### 5.1 Prerequisite Missing

必要條件根本不存在，例如 role、write permission、reachable service、compatible feature 不成立。

### 5.2 Authentication / Authorization Failure

Identity 不被接受，或已登入但權限不足。

### 5.3 Target Incompatibility

版本、architecture、configuration、protocol mode 與 technique 不相容。

### 5.4 Defensive Control Blocked

ACL、EDR、WAF、MFA、AppLocker、SELinux、IAM deny 等明確阻擋。

### 5.5 Tool / Operator Error

參數、parser、encoding、proxy、dependency、環境問題。

### 5.6 Hypothesis Wrong

原本對 target state 的假設不成立。

### 5.7 Scope / Safety Stop

技術上可能可行，但超出 ROE、impact ceiling 或 cleanup ability。

---

## 6. Retry Rule

只有在「同一 hypothesis 仍成立，且失敗原因可被具體修正」時 retry。

```text
Failure
  ↓
Root cause known?
  ├─ No → gather evidence, do not random retry
  └─ Yes
      ↓
Same hypothesis still valid?
      ├─ No → pivot
      └─ Yes → one controlled retry
```

不要透過輪流換五套工具來掩蓋 prerequisite 根本不存在。

---

## 7. Pivot Rule

Pivot 的理由應是 evidence gap 改變，例如：

- auth 成功、role 不足 → privilege path
- protocol reachability 成功、版本不符 → alternate authorized surface
- write capability 成功、execution 不成立 → execution prerequisite analysis
- mitigation 擋下 → control effectiveness finding + different scoped path

Pivot 不等於「換工具試試看」。

---

## 8. Defensive Telemetry Corroboration

Purple-team / lab 環境若能取得防守端 telemetry，可用來提高 validation quality：

- process creation
- authentication event
- network connection
- file/object create
- service/config change
- WAF/EDR alert

這些資料用於證明 operation observable 與 defensive coverage，不用來擴張 action scope。

---

## 9. False Positive / False Success

常見 false success：

- cached response
- client-side DOM/state change，但 server 未變更
- API 回 2xx，但 async job 失敗
- shell 顯示 username，但 effective token/role 不同
- remote tool 建立 transport，但 command 未執行
- marker 寫在 local temp，而不是 target

Success validation 應特別排除這些情況。

---

## 10. Partial Success

不是所有結果都只有 success/fail。

例如：

```text
Authentication: success
Authorization: read only
Write: denied
Execution: not tested
```

保留 capability matrix 比寫「成功登入」更有資訊價值。

---

## 11. Stop Conditions

立即停止當前 technique：

- 已達 objective，繼續只會增加 impact。
- root cause 顯示 prerequisite 不存在。
- target state 不穩定。
- 出現 unintended data modification / lockout / crash。
- 需要超出 ROE 的 bypass 才能繼續。
- cleanup 不能保證。
- operation window 已結束。

---

## 12. Abort / Emergency Stop

若出現非預期影響：

1. 停止新的 active actions。
2. 記錄最後 command、target、timestamp、identity。
3. 通知 stop authority / owner。
4. 依 ROE 決定是否執行已核准 cleanup。
5. 不自行擴張權限「修復」問題。

---

## 13. Cleanup Checkpoint

每次 state-changing action 後立即更新：

| Artifact | Created/modified | Restore action | Owner | Status |
| :--- | :--- | :--- | :--- | :--- |
| synthetic file | created | remove | operator | pending |
| test config | modified | restore baseline | app owner | complete |
| temporary session | created | terminate | operator | complete |

Cleanup 不應只存在 operator 記憶中。

---

## 14. Failed Path Record

每條 failed path 記：

```text
Hypothesis
Why it was reasonable
Preconditions checked
Action attempted
Observed failure
Failure class
What disproved or limited the path
Stop condition
Better pivot
Reusable lesson
```

---

## 15. Completion State

每條 technique 最終只能進入以下其中一種狀態：

- **Validated**：capability 已有 target/protocol proof。
- **Blocked**：控制措施明確阻擋。
- **Incompatible**：target 不符合 prerequisite。
- **Out of scope**：不可進一步驗證。
- **Aborted**：安全或 operation stop condition 觸發。
- **Unresolved**：目前 evidence 不足，且沒有合理低風險 action。

不要以「好像可以」「工具說成功」「之後再看」結束高價值 path。
