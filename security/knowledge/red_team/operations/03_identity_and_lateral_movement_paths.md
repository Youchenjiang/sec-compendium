# 03 — Identity、Trust 與 Lateral Movement Path

## 目的

橫向移動不是「能連到另一台主機」就算成功，而是 identity material、network reachability、service acceptance、authorization scope 與 remote privilege 同時成立。本手冊用 trust-boundary graph 管理這些條件，避免把 credential discovery、network reachability 與 remote control 混成同一個結論。

---

## 1. Identity Material 分類

| 類型 | 先確認 |
| :--- | :--- |
| Password / test secret | 所屬 identity、target、lockout policy |
| Session cookie | application、tenant、expiry、role |
| API token | audience、scope、expiry、issuer |
| Kerberos ticket | client、service、realm、lifetime |
| SSH key | account、host authorization、key restriction |
| Cloud credential | account、role、region、policy |
| Local token/session | host、logon context、effective privilege |

Material 被發現只代表「候選 identity path」，不是已驗證 remote capability。

---

## 2. Identity Validation

在 ROE 允許下，優先以最小作用的方式驗證：

```text
Identity material
      ↓
Target / audience match?
      ↓
Expired / revoked?
      ↓
Authentication accepted?
      ↓
Effective role / privilege?
```

每一步都可以停止；不要因為 material 存在就跨服務重放。

---

## 3. Trust-Boundary Graph

用 graph 表達 lateral path：

```text
[Identity]
   │
   ├── can authenticate to → [Service]
   │                         │
   │                         └── runs on → [Host]
   │
   └── has role/ACL on → [Resource / Directory Object]
```

Edge 只有在經過 validation 後才標成 confirmed；推測 edge 保持 hypothesis。

---

## 4. Reachability 與 Authorization 分開

```text
Port reachable
   ≠
Service authenticated
   ≠
Remote command capability
   ≠
Administrative privilege
```

Operation log 應分別記錄四個狀態，避免報告把「可連線」寫成「可橫向」。

---

## 5. Candidate Lateral Path

每條 candidate path 至少包含：

| 欄位 | 內容 |
| :--- | :--- |
| Source identity | 已驗證的 account/token/session |
| Source context | 哪台 host / app / tenant 取得 |
| Target service | SMB/WinRM/SSH/API/DB 等 |
| Target asset | 必須在 scope |
| Reachability | 是否已驗證 |
| Authentication method | password/key/ticket/token |
| Expected remote role | user/admin/service role |
| Minimal proof | 最低 impact capability validation |
| Cleanup | 是否產生 session/file/process |

---

## 6. Identity Reuse Guardrail

不要把「帳密相同」當作可以任意測試的理由。

Reuse 前確認：

- target 明確在 scope。
- credential reuse 在 ROE 允許範圍。
- 不會觸發 production lockout / MFA fatigue。
- test identity 不會影響真實 user。
- authentication protocol 與 target 相符。

---

## 7. Directory / AD Path

對 directory environment，將路徑拆成：

```text
Identity
  ↓
Group / delegated right / ACL
  ↓
Object / service / host
  ↓
Validated action
```

Graph 工具顯示的 edge 是候選 attack path；真正 operation finding 要驗證當前 directory state、權限 inheritance、disabled account、session availability 與 scope。

---

## 8. Remote Capability Validation

優先 proof：

- authenticated service query
- read-only host information
- synthetic marker under designated test path
- target-side process observable（若 ROE 允許 code execution）
- effective remote identity

不要用大規模 data collection 或 credential dumping 當成「只是證明 remote admin」。

---

## 9. Multi-Hop Path

多跳時每一 hop 都建立 checkpoint：

```text
Hop 1: identity A → service X → host B
  proof: ...
  cleanup: ...

Hop 2: identity B → service Y → host C
  proof: ...
  cleanup: ...
```

這能避免最後只知道「到了 C」，卻無法解釋每個 trust boundary 如何跨越。

---

## 10. Pivot Selection

優先選擇：

1. 已確認 identity + 已確認 reachability。
2. target 在 scope。
3. remote role 有明確 expected outcome。
4. proof 可 reversible。
5. 不需要跨出資料處理規則。

如果缺 identity，回到 foothold privilege path；如果缺 reachability，回到 attack-surface map。

---

## 11. Defensive Control as Outcome

若遠端 authentication 或 execution 被 MFA、network ACL、EDR、JEA、sudo policy、IAM deny 等控制措施阻擋，記錄：

- control location
- blocked action
- operator-visible response
- target-side telemetry（若 exercise 可取得）
- current capability 是否仍存在

成功的防禦控制也是 operation outcome，不需要為了繞過而擴大 impact。

---

## 12. Lateral Failure Classes

- unreachable service
- authentication rejected
- identity expired/revoked
- role insufficient
- protocol incompatible
- policy / MFA blocked
- target out of scope
- target state changed since enumeration
- tool/operator error

每種失敗對應不同 pivot，不要只換另一套 remote-exec 工具重試。

---

## 13. Scope Drift

如果 path graph 發現新的 host/domain/tenant/trust：

```text
New node
  ↓
Check original scope
  ├─ In scope → may validate
  └─ Unknown/out → passive record only
```

Trust relationship 不是 authorization relationship。

---

## 14. Cleanup

追蹤：

- remote sessions
- synthetic files
- created processes/services/tasks
- temporary keys/tokens
- modified ACL/config
- tunneling/proxy processes

每一 hop 完成後就更新 cleanup state，不等到 operation 最後才回想。

---

## 15. Completion Output

```text
Validated source identity
Validated target
Authentication mechanism
Reachability proof
Remote effective privilege
Trust boundary crossed
Control encountered
Artifacts changed
Cleanup status
Next authorized path
```

需要執行 technique 並判斷「到底成功還是失敗」時，進入 `04_execution_validation_and_failure_paths.md`。
