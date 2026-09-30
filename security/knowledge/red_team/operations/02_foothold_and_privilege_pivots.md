# 02 — Foothold、Capability 與 Privilege Pivot

## 目的

取得第一個 foothold 後，紅隊最容易犯的錯是把「有 shell / 有 session / command 成功」直接等同「已取得高權限」。本手冊把 foothold 拆成可驗證 capability，並用 privilege boundary、可回復性與 impact 來選下一個 pivot。

---

## 1. Foothold 不是二元狀態

建議把 capability 分層：

| Capability | 可驗證的 proof |
| :--- | :--- |
| Reachability | protocol handshake / service response |
| Authenticated access | server-side session / authenticated response |
| Read capability | 可讀指定 synthetic object |
| Write capability | 可建立可清理的 marker |
| Code execution | target-side controlled process / marker output |
| Local privilege | effective identity / protected resource access |
| Service control | 可查詢／變更明確授權的 lab service |
| Administrative capability | 特定 privileged action 成功 |

每個 operation finding 應寫「取得哪個 capability」，而不是只寫「拿到 shell」。

---

## 2. 建立 Current State

```text
Current identity
Current host / container / app context
Effective privilege
Accessible resources
Network reachability
Available credentials/tokens
Writable locations
Security controls observed
```

這些欄位是後續 privilege pivot 的輸入。

---

## 3. Privilege Boundary Map

常見 boundary：

- anonymous → authenticated user
- user → privileged application role
- local user → local administrator/root
- service account → higher-privilege service identity
- workstation → server administration
- domain user → delegated directory privilege
- namespace/pod → cluster-scoped capability
- cloud role → broader IAM role

對每個 boundary 記錄：

| 欄位 | 內容 |
| :--- | :--- |
| Current capability | 目前已驗證狀態 |
| Target capability | 想證明的下一層權限 |
| Trust mechanism | ACL / token / service / sudo / IAM / delegation |
| Prerequisite | 必須成立的條件 |
| Minimal proof | 最低 impact 的成功證明 |
| Cleanup | 需要回復什麼 |

---

## 4. Enumerate Before Escalate

先用 read-only enumeration 建立 privilege model：

- current identity / groups / effective token
- service ownership / permissions
- sudo / delegated command policy
- file / directory permissions
- scheduled task / service configuration
- environment / secret references
- local admin / role membership
- cloud IAM bindings
- container capabilities / mounts

目標是找到「可解釋的 privilege path」，不是蒐集越多輸出越好。

---

## 5. Candidate Pivot 評分

優先選：

1. prerequisite 已被 evidence 支持。
2. 可用 synthetic/reversible proof 驗證。
3. cleanup path 明確。
4. 不需要取得超出 operation 目的的資料。
5. 成功/失敗都能提供明確資訊。

避免先選不可逆、會中斷服務或改變大量 state 的方法。

---

## 6. Success Validation

Privilege escalation 成功不以工具訊息判斷，而以 target-side state 判斷。

```text
Action executed
   ↓
Effective identity changed?
   ↓
Protected action now allowed?
   ↓
State verified independently?
```

例如：

- effective UID / token changed
- previously denied synthetic object becomes readable
- privileged API returns authorized response
- lab-only administrative action succeeds

成功 proof 應最小化，不必為了證明 admin 去 dump 大量 secrets。

---

## 7. Credential / Secret 發現後

遇到 credential material 時先記：

- type
- source
- target/audience
- expiry
- scope/role
- whether reuse is explicitly allowed

下一步先做 identity validation，不要自動向其他系統重放。

---

## 8. Local → Remote Pivot

本機高權限不自動代表能 lateral move。

先確認：

```text
Identity material available?
        ↓
Remote service reachable?
        ↓
Identity accepted by that service?
        ↓
Remote privilege / role?
```

這個流程交給 `03_identity_and_lateral_movement_paths.md` 做完整編排。

---

## 9. Mitigation as Result

如果 prerequisite 成立但 technique 被控制措施阻擋，這也是有效 finding。

記錄：

| 欄位 | 內容 |
| :--- | :--- |
| Expected capability | 原本想驗證什麼 |
| Control observed | EDR、ACL、UAC、AppArmor、SELinux、IAM deny 等 |
| Observable | block / deny / alert / rollback |
| State after block | target 是否保持原狀 |
| Next action | stop / alternate authorized route |

不要為了「一定要成功」而自動轉向更具破壞性的 bypass。

---

## 10. Failure Classification

失敗至少分成：

- prerequisite missing
- privilege insufficient
- target/version incompatible
- security control blocked
- scope/authorization prevents validation
- tool/parser/operator error
- hypothesis wrong
- target unstable

分類後才能決定 retry 還是 pivot。

---

## 11. Cleanup Contract

若 privilege validation 產生變更，立刻記錄：

- created file/object
- modified permission/config
- started/stopped service
- temporary account/key/token
- process/session
- scheduled artifact

每項都要有 owner 與 restore method。

---

## 12. Stop Conditions

Stop 當：

- 下一步只剩超出 ROE 的 high-impact technique。
- target 已出現非預期不穩定。
- privilege proof 已足夠滿足 objective。
- cleanup 無法保證。
- 需要使用真實敏感資料才能繼續。
- prerequisite 已明確不存在。

已證明 capability 後，不為了「更漂亮的截圖」重複執行同一 privilege action。

---

## 13. Pivot Output

完成本階段時，輸出：

```text
Validated capability
Effective identity
Target boundary crossed
Proof / observable
Security controls encountered
Artifacts changed
Cleanup state
Reachable next surfaces
Known identity material
```

如果下一步涉及新的 host/service/account trust，進入 `03_identity_and_lateral_movement_paths.md`。
