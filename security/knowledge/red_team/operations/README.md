# ⚔️ 紅隊作戰編排層 (Red Team Operation Orchestration)

## 定位

`operations/` 是紅隊的「案件／任務級」編排層。它不取代單一 technique playbook，而是回答一場**已授權** assessment、lab、purple-team exercise 或 CTF 中最常遇到的問題：

- 目前 scope 與 Rules of Engagement 允許做什麼？
- 已知 target / identity / service 能往哪些方向走？
- 哪一條 attack path 的資訊價值最高、風險最低？
- 一個 command 沒報錯，是否真的代表 capability 已取得？
- 什麼 observable 才能證明 foothold / privilege / lateral movement 成功？
- 失敗是 prerequisite 不足、mitigation 阻擋、工具不相容，還是假說錯誤？
- 何時必須停止、回復變更、或把下一步交回 defensive team？

`operations/` 與 `../playbooks/` 的分工：

```text
Operation orchestration
        ↓
選擇 technique / capability
        ↓
Atomic playbook
        ↓
Success validation
        ↓
回到 operation 決定下一個 pivot
```

---

## 使用邊界

本層只適用於：

- 自有環境與本機 lab。
- 明確取得授權的 penetration test / red-team engagement。
- Purple-team / detection engineering exercise。
- CTF、靶場、課堂或研究用 synthetic environment。

每次 operation 開始前都先記錄 scope、target、時間窗、允許 technique、禁止動作與 cleanup owner。若實際環境與授權文件不一致，以較嚴格者為準。

---

## 00–05 作戰流程

| 文件 | 主要問題 |
| :--- | :--- |
| `00_target_intake_and_scope.md` | 我們被授權測什麼？哪些資產／身分／時間與動作在界線內？ |
| `01_attack_surface_and_entry_routing.md` | 目前有哪些 attack surface？哪個 entry path 最值得先驗證？ |
| `02_foothold_and_privilege_pivots.md` | 已取得什麼 capability？下一個 privilege boundary 如何選？ |
| `03_identity_and_lateral_movement_paths.md` | Credential/token/session 如何映射到 identity、reachability 與 lateral path？ |
| `04_execution_validation_and_failure_paths.md` | 如何證明 action 真正成功？失敗後該 stop、retry 還是 pivot？ |
| `05_scenario_lesson_promotion.md` | 哪些 lesson 可以去場景化後升級成共通 operations/playbooks？ |

---

## Operation Workbook 最小欄位

一場 operation 至少維護：

| 欄位 | 內容 |
| :--- | :--- |
| Authorization reference | ROE / lab / ticket / exercise reference |
| In-scope assets | host、app、domain、tenant、CIDR、account |
| Out-of-scope | 明確禁止的資產、資料、動作 |
| Time window | 可執行時間與 maintenance restriction |
| Current capability | anonymous / user / local admin / domain user 等 |
| Known identities | account / token / session 與來源 |
| Reachable surfaces | service / host / API / trust boundary |
| Hypotheses | 可驗證的 attack-path 假說 |
| Validation result | 成功 observable、失敗分類、證據位置 |
| Cleanup state | 已建立／修改／上傳的 artifact 是否回復 |
| Next pivot | 下一個已授權且資訊價值最高的 action |

---

## 核心原則

1. **Authorization before action**：先確定 scope，再選技術。
2. **Capability, not command output**：command exit code 不等於取得 capability。
3. **Minimum necessary impact**：能用 read-only / synthetic / reversible proof 驗證，就不要先選高破壞方式。
4. **Validate state change**：每個成功結論都要有 target-side 或 protocol-level observable。
5. **Pivots are evidence-driven**：下一步依 prerequisite、identity、reachability 與 trust boundary，而不是因為某工具「常用」。
6. **Failure is structured data**：失敗要分類，避免用不同工具重複同一個錯誤假說。
7. **Cleanup is part of done**：operation 完成不只拿到 proof，也要完成 restore / artifact removal / handoff。
8. **Promote methods, not answers**：scenario-specific target、credential、flag、IP、hash 不進共通知識庫。

---

## 與 Blue Team 的對應

| Blue Team | Red Team |
| :--- | :--- |
| Evidence intake | Scope / target intake |
| Artifact routing | Attack-surface routing |
| Cross-artifact pivot | Attack-chain pivot |
| Evidence level | Success validation |
| Parser caveat | Tool / target compatibility |
| Stop condition | Failure / abort condition |
| Scenario lesson promotion | Operation lesson promotion |

兩邊共享同一個目標：讓「結論如何成立」與「下一步為何合理」都能被另一位分析者獨立重播。
