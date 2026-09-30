# 01 — Attack Surface 與 Entry Routing

## 目的

取得授權 scope 後，下一步不是把所有工具都跑一遍，而是建立 attack-surface map，再選擇資訊價值高、影響低、可回復的 entry validation。這份手冊提供從已知 target 到第一個可驗證 foothold hypothesis 的 routing 方法。

---

## 1. 建立 Attack Surface Map

依「可互動介面」而不是工具名稱分類：

| Surface | 常見入口 | 先確認的 prerequisite |
| :--- | :--- | :--- |
| Network service | TCP/UDP service、VPN、remote admin | reachability、protocol、version/context |
| Web / API | HTTP endpoint、auth flow、upload、callback | host、route、role、session、rate limit |
| Identity | login、SSO、directory、service account | account state、auth method、lockout policy |
| File / share | SMB/NFS/object storage/repository | read/write permission、path、owner |
| Directory / trust | AD/LDAP/tenant trust | domain context、identity、delegation |
| Cloud control plane | IAM/API/metadata | tenant/account、role、region、scope |
| Local host | process/service/package/config | local access、OS/build、privilege |
| Source / CI/CD | repository、pipeline、artifact registry | repo role、branch protection、runner context |

同一 target 可能同時暴露多個 surface；routing 目標是先找最能縮小 attack-path 假說的那個，而不是先追求最深權限。

---

## 2. Discovery 與 Active Validation 分開

```text
Known target
   ↓
Passive / low-impact discovery
   ↓
Surface inventory
   ↓
Prerequisite check
   ↓
Minimal active validation
   ↓
Observed capability
```

Discovery 只建立「可能存在」；active validation 才能建立「可互動」或「可取得某 capability」。

---

## 3. Routing Score

每個候選 entry path 可以用四個維度排序：

| 維度 | 問題 |
| :--- | :--- |
| Information gain | 成功/失敗後能排除多少假說？ |
| Authorization clarity | 是否完全在 scope 與 ROE 內？ |
| Impact | 是否可能造成 lockout、crash、資料修改？ |
| Reversibility | 是否容易 cleanup / restore？ |

優先：高資訊、授權清楚、低 impact、高可回復。

不要因某 technique「成功率高」就跳過 scope 或 impact 評估。

---

## 4. Service Routing

服務探測後，先問：

```text
Service observed
   ↓
Is protocol identity confirmed?
   ├─ No → banner / handshake / documentation-level validation
   └─ Yes
       ↓
Is authentication required?
       ↓
Do we have an authorized test identity?
       ↓
Can a read-only request validate access?
```

版本字串本身不是漏洞證明；產品版本也可能被 proxy、backport、container image 或 vendor patch 改變。

---

## 5. Web / API Routing

先建立 application map：

- unauthenticated routes
- authenticated routes
- role boundaries
- object identifiers
- upload/download flows
- state-changing methods
- API version / schema
- callback / webhook

優先驗證：

1. 是否能重現正常 user flow。
2. 哪些 request 真的改變 server-side state。
3. 哪些 identifier 屬於 session、tenant、object、role。
4. 是否有可用 synthetic object 測試 authorization boundary。

先理解正常流程，才能判斷後續 deviation 是否真的突破 trust boundary。

---

## 6. Identity Routing

遇到帳號、token、session 時先分類：

| Identity material | 先驗證什麼 |
| :--- | :--- |
| Username only | account existence 是否允許測試 |
| Test password | auth 是否成功、role 是什麼 |
| Session cookie | target / expiry / scope |
| API token | audience、permission、tenant |
| Kerberos ticket | client、service、realm、lifetime |
| Cloud credential | account/role、region、policy |

「擁有 credential material」不等於「credential 有效」，更不等於「所有服務都能使用」。

---

## 7. Local Host Routing

已有 local access 時，entry routing 轉成 privilege-boundary routing：

```text
Current identity
  ↓
Effective privilege / groups
  ↓
Service / task / file / socket / secret exposure
  ↓
Candidate boundary
  ↓
Read-only or reversible validation
```

先建立 current capability，不要直接假設 shell 類型或 username 代表實際 privilege。

---

## 8. Cloud / Container Routing

Cloud 與 Kubernetes 容易因自動 discovery 跨 scope，需額外記錄：

- account / subscription / project / cluster
- namespace / resource group
- service account / role
- region
- external managed service ownership

如果 API 回傳另一個 account/tenant/resource reference，只記錄 finding，先做 scope drift check，再決定是否互動。

---

## 9. Entry Hypothesis Template

每個候選 entry path 用同一格式：

| 欄位 | 內容 |
| :--- | :--- |
| Surface | Web / service / identity / local / cloud... |
| Observation | 已知事實 |
| Hypothesis | 可能取得的 capability |
| Preconditions | 必須成立的條件 |
| Minimal validation | 最低 impact 驗證方式 |
| Success observable | target/protocol 上會看到什麼 |
| Failure meaning | 失敗能排除什麼 |
| Scope check | 是否完全在 scope |
| Next pivot | 成功或失敗後去哪裡 |

---

## 10. Routing Anti-Patterns

避免：

- 看到版本號就直接套 exploit。
- 看到 login 就先暴力破解。
- 看到 token 就在所有服務重放。
- 看到相鄰 subnet 就自動掃描。
- 看到 public PoC 就假設 target build 一定受影響。
- 看到 tool 回傳 success 就直接寫「已取得 foothold」。

這些做法都跳過 prerequisite 或 success validation。

---

## 11. Best Next Action

下一步應能回答一個具體 evidence gap，例如：

```text
Gap: service 是否真的允許 anonymous read？
Action: 執行 read-only listing
Observable: server 回傳 object list
Result: capability = anonymous read
```

而不是：

```text
Action: 跑更多 scanner
Reason: 看看會不會有東西
```

---

## 12. Stop / Pivot Conditions

Stop 當：

- 下一步需要跨 scope。
- prerequisite 已被明確否定。
- validation 會超過允許 impact。
- target state 不穩定或出現非預期影響。

Pivot 當：

- surface 可達，但缺 identity → identity path。
- identity 有效，但 privilege 不足 → privilege path。
- service version 不確定 → configuration / fingerprint validation。
- entry path 被 mitigation 阻擋 → 記錄 control effectiveness，選另一個已授權 surface。

---

## 13. Completion Checklist

- [ ] Attack surface 已按 interface 分類。
- [ ] 每個候選 entry path 都有 prerequisite。
- [ ] 已選最低 impact validation。
- [ ] Success observable 可由 target/protocol 驗證。
- [ ] Failure meaning 已定義。
- [ ] 新 asset 已做 scope drift check。
- [ ] 已知第一個 validated capability 或明確 stop reason。

取得第一個 capability 後，進入 `02_foothold_and_privilege_pivots.md`。
