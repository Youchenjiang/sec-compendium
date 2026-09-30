# 05 — Scenario Lesson Promotion 與 Red-Team Knowledge Governance

## 目的

CTF、靶場、purple-team exercise、內部 assessment 與授權 penetration test 都會產生新的攻擊鏈經驗。本文件定義如何把「某一次 operation 中已被驗證的方法」去場景化，升級成共通 `operations/` 或 `playbooks/` 知識，而不把特定 target、credential、flag、IP、hash 或未證實假說寫進公共方法論。

---

## 1. Promote Method, Not Answer

可以升級：

- authorization / scope guardrail
- attack-surface routing pattern
- prerequisite discriminator
- capability validation pattern
- privilege / identity pivot rule
- tool / target compatibility caveat
- defensive-control observation
- failure classification
- stop / abort rule
- cleanup / restoration pattern

不應升級：

- flag
- 真實 credential / token / key
- 特定 target hostname / IP / tenant
- 特定 customer / employee / student identity
- 單一案件專屬 path / object ID
- 未授權環境細節
- 只在一次失敗中猜出的假說

---

## 2. Promotion Candidate 條件

一個 lesson 至少符合：

1. 在已授權 scenario 中實際驗證。
2. 有清楚 success/failure observable，而不是只靠工具提示。
3. 移除 scenario-specific 值後仍能成立。
4. 適用條件與 limitation 可以說清楚。
5. 未來另一個 lab/engagement 可以重播。
6. 不會鼓勵超出 scope 或增加不必要 impact。

「很常聽人這樣做」不算 promotion evidence。

---

## 3. Candidate Record

| 欄位 | 內容 |
| :--- | :--- |
| Lesson | 想升級的規則 |
| Source scenario | CTF / lab / exercise / engagement reference |
| Authorization context | 為何該 action 在來源 scenario 中合法 |
| Source path | 原始 operation note / writeup |
| Capability tested | 驗證了什麼能力 |
| Success / failure observable | 哪個 target-side result 支持 lesson |
| Preconditions | 必須成立的環境條件 |
| Generalized wording | 去除 scenario 值後的寫法 |
| Limitation | 何時不適用 |
| Cleanup lesson | 是否有 state / restoration 要點 |
| Target document | operations / atomic playbook |
| Validation count | 已在幾個獨立 scenario 重現 |

---

## 4. Promotion Level

| 狀態 | 條件 | 用途 |
| :--- | :--- | :--- |
| Candidate | 1 個 authorized scenario + observable | 等待 generalization review |
| Reusable | 已移除 scenario 值，prerequisite/limitation 完整 | 可進共通知識庫 |
| Stable | 至少 2 個不同 scenario 或 protocol/vendor docs 支持 | 可作推薦 workflow |

Validation count 是治理資訊，不是「成功率百分比」。

---

## 5. Operations vs Playbooks

升級前先選唯一 source of truth。

放 `operations/`：

- scope / ROE
- attack-path routing
- capability state
- identity/trust pivot
- retry/pivot/stop decision
- cleanup governance
- scenario promotion

放 `playbooks/`：

- 單一 technique 的 mechanics
- tool usage
- target discovery for that technique
- success validation specific to that technique
- telemetry footprint
- technique-specific cleanup
- defensive countermeasure

不要把完整 technique 同時複製兩份。

---

## 6. Generalization Procedure

```text
Scenario finding
      ↓
Confirm authorization + observable
      ↓
Remove target / credential / flag / IP / hash
      ↓
Extract prerequisite + capability transition
      ↓
State limitation + cleanup
      ↓
Choose operations or playbooks
      ↓
Review for answer leakage / scope drift
      ↓
Atomic documentation commit
```

---

## 7. 好的 Generalization

Scenario-specific：

```text
某 lab 的 10.10.x.x:8443 可以用某帳號登入，最後拿到 admin。
```

不應進共通知識庫。

可升級：

```text
當 identity material 被發現時，先驗 target/audience、expiry 與 role；
authentication accepted 只證明 authenticated capability，必須再驗 effective privilege，
且 credential reuse 僅限 ROE 明確允許的 target。
```

後者保留方法，沒有保存 scenario answer。

---

## 8. Tool Lesson Generalization

工具型 lesson 不能寫成：

```text
工具 X 顯示 SUCCESS，所以 technique 成功。
```

應寫成：

```text
工具 X 的成功訊息只算 operator-side observation；
需要 protocol response、target-side state 或第二 telemetry channel 才升級為 validated capability。
```

這種 lesson 才能跨版本與工具重用。

---

## 9. Defensive-Control Lesson

紅隊知識不只升級「怎麼成功」，也要升級「什麼控制有效」。

例如：

- prerequisite 成立但 ACL 阻擋
- identity 有效但 MFA 阻擋
- code path 可達但 application allowlisting 阻擋
- network reachable 但 segmentation 阻擋下一 hop

Generalization 應描述 control placement、observable 與 remaining capability，不以「想辦法繞過」作唯一結論。

---

## 10. Failure Promotion

Failed path 可升級的條件：

- root cause 已確認
- failure class 清楚
- stop condition 有價值
- 可避免未來重複低品質嘗試

例如「某技術需要 target feature X；若 feature 明確不存在，就 stop 而非換工具重試」是很好的 reusable lesson。

---

## 11. Cleanup Lesson

如果 operation 發現：

- 某工具會留下額外 process/file
- 某 workflow 的 rollback 順序很重要
- 某 validation 會建立 session/token/object

這些 cleanup 行為也應被升級成 atomic playbook requirement。

---

## 12. Promotion Review Checklist

- [ ] Source scenario 有明確授權背景。
- [ ] Lesson 由 target/protocol observable 驗證。
- [ ] 已移除 target、credential、flag、IP、hash 等 scenario 值。
- [ ] Preconditions 已寫出。
- [ ] Limitation 已寫出。
- [ ] Impact / cleanup 已寫出。
- [ ] 不會鼓勵 scope 自動擴張。
- [ ] 已選正確 knowledge layer。
- [ ] 沒有與既有規則建立第二份 source of truth。
- [ ] Commit 只包含同一個 lesson / 同一脈絡。

---

## 13. Atomic Commit Rule

好的 promotion：

```text
docs(knowledge): add token audience validation rule
```

不好的 promotion：

```text
docs: add all lessons from last CTF
```

Revert Test：如果 lesson A 可以獨立撤回而不影響 lesson B，它們就應拆開提交。

---

## 14. Maintenance Loop

每次 scenario 結束後：

1. 從 validated / blocked / failed paths 提取候選 lesson。
2. 檢查 authorization 與 observable 是否足夠。
3. 去除 scenario-specific values。
4. 搜尋現有 operations/playbooks 是否已有同類規則。
5. 選唯一 source of truth。
6. 用 atomic commit 升級。
7. 後續 scenario 重複驗證時補 limitation 或 stable status。

紅隊知識庫應隨實戰成長，但不應變成 target answer、credential 或 exploit success screenshot 的堆積區。
