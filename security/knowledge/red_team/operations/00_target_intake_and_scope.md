# 00 — Target Intake、Authorization 與 Scope Baseline

## 目的

紅隊 operation 的第一個技術決策不是選工具，而是確認授權邊界。這份手冊把 Rules of Engagement、target inventory、時間窗、禁止動作與 cleanup 責任轉成可執行的 operation baseline，避免後續所有 technique 建立在錯誤 scope 上。

---

## 1. Authorization Record

開始前至少記錄：

| 欄位 | 內容 |
| :--- | :--- |
| Authorization reference | 合約、ticket、lab、課程或 exercise reference |
| Owner | 授權 owner / exercise lead |
| Operators | 可執行人員 |
| Start / end | operation 時間窗 |
| Emergency contact | 出現意外影響時的聯絡方式 |
| Stop authority | 誰可以立即終止 operation |
| Evidence/report owner | findings 與 operation log 的保管者 |

如果只知道「這台是靶機」但沒有可追溯的 authorization reference，先補齊 scope，不把口頭假設當作長期 operation baseline。

---

## 2. In-Scope Assets

Scope 應具體到可以判斷「這個 action 能不能做」。

```text
Environment
  ├─ Network / CIDR
  ├─ Host / VM / container
  ├─ Application / API
  ├─ Domain / tenant / subscription
  ├─ Identity / test account
  └─ Third-party dependency
```

建議表格：

| Asset | Identifier | Owner | In scope? | Allowed interaction | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Web app | hostname / URL | App team | Yes | authenticated test | synthetic data only |
| AD lab | domain | Lab owner | Yes | enumeration + approved techniques | no production trust |
| SaaS | tenant | Vendor | No / Conditional | metadata only | third-party restriction |

---

## 3. Out-of-Scope 必須寫出來

常見明確排除：

- Production database modification。
- Real customer / student / employee data extraction。
- Denial of Service、resource exhaustion、destructive testing。
- Social engineering / phishing，除非 ROE 明確納入。
- Third-party SaaS、CDN、MSSP、ISP infrastructure。
- Persistence beyond the exercise window。
- Credential reuse outside the designated lab/tenant。
- Any action requiring another team's explicit go-ahead。

「ROE 沒提到」不應自動解讀為允許。

---

## 4. Technique Allowlist / Denylist

把抽象條款轉成 technique 級條件：

| Technique family | Allowed? | Preconditions | Impact ceiling |
| :--- | :--- | :--- | :--- |
| Passive recon | Yes | public / lab data | no target change |
| Active scanning | Yes / Conditional | rate limit | no stress testing |
| Authentication testing | Conditional | test account | lockout-safe |
| Privilege escalation | Conditional | lab snapshot | reversible proof |
| Lateral movement | Conditional | named hosts | no unlisted subnet |
| Persistence | Usually No / Explicit only | cleanup plan | exercise-only artifact |
| Exfiltration simulation | Synthetic only | predefined marker file | no real data |

Technique allowlist 不是工具 allowlist；同一工具可執行多種不同 impact 的 action。

---

## 5. Data Handling Baseline

紅隊 findings 很容易碰到 secrets、tokens、documents、memory dumps。開始前先定義：

- 可以收集哪些資料類型？
- 是否只允許 synthetic marker？
- Credential material 是否可保存？保存多久？
- Screenshot 是否可能包含 PII？
- Report 中是否需要 redaction？
- Artifact 存放位置與 encryption requirement？
- operation 結束後誰負責刪除 temporary evidence？

只要「證明 access」就足夠時，不要把整批資料複製回來。

---

## 6. Time and Change Window

記錄：

```text
Operation timezone
Target timezone
Start/end window
Maintenance window
Known backup/snapshot time
Change freeze
Monitoring team awareness
```

這些時間資訊會影響：

- 掃描速率。
- account lockout risk。
- blue-team correlation。
- cleanup timing。
- rollback / snapshot availability。

---

## 7. Initial Capability State

Operation intake 時就標示目前真的擁有什麼，而不是假設「已登入」代表所有後續能力都成立。

常見 capability level：

| Capability | Example proof |
| :--- | :--- |
| Network reachability | TCP handshake / service banner |
| Anonymous read | 可讀指定 public/share object |
| Authenticated user | target-side session / authenticated response |
| Code execution | controlled marker / target-side process observable |
| Local privilege | effective identity / protected resource access |
| Remote administration | named host + verified session |
| Directory privilege | specific delegated action succeeds |

後續每個 pivot 都從「已驗證 capability」出發。

---

## 8. Safety Controls

operation 開始前建立最低安全控制：

1. Rate limit 與 concurrency 上限。
2. Test account / synthetic file / marker hostname。
3. Snapshot / backup / restore owner。
4. Cleanup checklist。
5. Emergency stop signal。
6. Operator log。
7. 禁止自動擴張 scope 的工具設定。

工具若會自動 follow redirect、recursive scan、discover adjacent subnet 或 reuse credentials，要先檢查是否可能跨出 scope。

---

## 9. Scope Drift Check

每次出現新的 host、identity、domain、tenant、bucket、repository 或 third-party service 時，先問：

```text
New asset discovered
      ↓
Is it explicitly in scope?
  ├─ Yes → continue under existing limits
  ├─ Conditional → record and obtain required approval
  └─ No/Unknown → stop active interaction; keep as finding only
```

「從 in-scope host 可以連到它」不代表新 target 自動變成 in-scope。

---

## 10. Stop Conditions

立即停止當前 action，至少包含：

- target identity / owner 與 scope 不一致。
- tool 正在對未授權地址或帳號執行 action。
- 產生非預期 service impact、lockout、crash 或資料修改。
- 遇到真實敏感資料但 ROE 只允許 synthetic proof。
- cleanup prerequisite 不存在。
- engagement window 已結束。
- stop authority 發出終止指示。

Stop 後保留 operator log 與最後已知 state，避免為了「清乾淨」而繼續做未授權變更。

---

## 11. Intake Completion Checklist

- [ ] Authorization reference 可追溯。
- [ ] In-scope / out-of-scope assets 已明確列出。
- [ ] Technique allow/deny 與 impact ceiling 已記錄。
- [ ] Data handling 規則已確認。
- [ ] Timezone / operation window / maintenance window 已確認。
- [ ] Initial capability state 已有 observable proof。
- [ ] Rate limit / stop / cleanup owner 已定義。
- [ ] New asset scope-drift 流程已建立。

完成以上項目後，才進入 `01_attack_surface_and_entry_routing.md`。
