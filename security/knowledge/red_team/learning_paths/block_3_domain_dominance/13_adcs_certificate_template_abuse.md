# 📜 企業憑證服務 (AD CS) 核心原理與 ESC1~ESC8 攻擊鏈深度學習路徑 (AD CS Exploitation)
> 對應紅隊作戰矩陣：**Phase 3 (R17)** (R17.1 ~ R17.7)  
> 預計總投入時間：**35 ~ 40 小時**（視 PKI 公鑰基礎設施、X.509 憑證擴充與 Active Directory Kerberos PKINIT 基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
不知道什麼是 AD CS 憑證服務  ──►     精通 PKI 基礎架構、憑證範本與 PKINIT 網域身分對齊
看懂 ESC1 但不知道其他代號   ──►     通盤掌握 ESC1 到 ESC8 的所有脆弱性配置利用鏈
拿到憑證不知如何換成管理員Hash ──►   精通 Certipy 工具鏈直接以憑證換取 TGT 與 NTLM Hash
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| X.509 憑證與擴充屬性 (Extensions) | 熟悉 SAN (主體別名)、EKU (增強金鑰用法) 與 CA 信任鏈 | [RFC 5280: X.509 PKI 規範](https://datatracker.ietf.org/doc/html/rfc5280) |
| Kerberos PKINIT 協定擴展 | 理解使用 X.509 數位憑證向 KDC 進行非對稱預驗證並換取 TGT | [RFC 4556: PKINIT in Kerberos](https://datatracker.ietf.org/doc/html/rfc4556) |
| Active Directory PKI 物件容器 | 熟悉 `CN=Public Key Services,CN=Services,CN=Configuration` | [SpecterOps: Certified Pre-Owned 白皮書](https://posts.specterops.io/certified-pre-owned-d95910965cd2) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
ADCS架構PKINIT ESC1任意身分申請 ESC2/ESC3代理鏈 ESC4/ESC6策略改 憑證換取TGT/Hash
(8h)           (10h)          (8h)           (8h)           (6h)
```

---

## 🏛️ 階段一：AD CS 憑證服務架構與 PKINIT 認證機制（約 8 小時）

### 1.1 企業憑證授權單位 (Enterprise CA) 的身分信任
在 Active Directory 中，AD CS 發行的憑證可用於**「身分驗證」**。
- 若憑證的 EKU 包含 `Client Authentication` (OID: `1.3.6.1.5.5.7.3.2`) 或 `Smart Card Logon` (OID: `1.3.6.1.4.1.311.20.2.2`)。
- 客戶端可將此憑證提交給 KDC，透過 **Kerberos PKINIT** 機制，直接獲取對應使用者的 Kerberos TGT 票證！

---

## 🎯 階段二：ESC1 申請者指定主體別名憑證頒發濫用（約 10 小時）

### 2.1 ESC1 的致命四條件 (Four Lethal Flags)
一個憑證範本 (Certificate Template) 同時滿足以下四個條件即構成 ESC1：
1. **頒發 CA 授權**：Enterprise CA 發行此範本。
2. **註冊權限過寬**：低特權使用者（如 `Domain Users` 或 `Authenticated Users`）具備註冊權限 (Enroll)。
3. **允許申請者指定 SAN**：設定了 `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` 標記（允許客戶端自行填寫憑證的 Subject Alternative Name）。
4. **具備身分驗證用途**：EKU 包含客戶端身分驗證。

### 2.2 Certipy 實戰武器化打擊
```bash
# 1. 掃描網域內所有脆弱憑證範本
certipy find -u low_user@domain.local -p password -dc-ip 192.168.1.10 -vulnerable

# 2. 偽造 Domain Admin (Administrator) 申請憑證
certipy req -u low_user@domain.local -p password -ca CORP-CA -template VulnerableTemplate -upn administrator@domain.local -dc-ip 192.168.1.10

# 3. 憑 pfx 憑證透過 PKINIT 換取 TGT 並導出 Administrator 的 NTLM Hash！
certipy auth -pfx administrator.pfx -dc-ip 192.168.1.10
```

---

## 🔄 階段三：ESC2、ESC3 與註冊代理濫用（約 8 小時）

### 3.1 ESC2 (Any Purpose EKU)
憑證範本定義了 `Any Purpose` 或無 EKU，代表該憑證可用於任何目的，包括代表他人申請或直接認證。

### 3.2 ESC3 (Certificate Request Agent)
範本包含「憑證註冊代理」EKU。攻擊者申請到註冊代理憑證後，可**代表 (On-Behalf-Of) 網域內任何高特權使用者向 CA 申請正式的驗證憑證**！

---

## 🛠️ 階段四：ESC4 (模板 ACL 可寫) 與 ESC6 (全域 SAN 開啟)（約 8 小時）

### 4.1 ESC4：動態修改範本
若攻擊者對某個憑證範本擁有 Write 權限：
1. 將範本動態修改為 ESC1 狀態（開啟 Enrollee Supplies Subject）。
2. 為自己頒發管理員憑證。
3. 立即復原範本配置，完成神不知鬼不覺的提權。

### 4.2 ESC6：CA 全域標誌漏洞
CA 伺服器全域開啟了 `EDITF_ATTRIBUTESUBJECTALTNAME2`：任何範本（即使未勾選指定 SAN），只要在申請時透過自定義屬性夾帶 SAN，CA 一律照單全收！

---

## 👑 階段五：憑證信任錨點覆寫與全域持久化 (Golden Certificate)（約 6 小時）

### 5.1 導出 CA 私鑰 (ESC7 / Backup)
若攻擊者掌握了 CA 伺服器的備份金鑰或具有管理員權限：
- 導出 CA 的私鑰 (`.pfx`)。
- 攻擊者可在**完全離線**狀態下，自行簽發任何網域使用者的智慧卡登入憑證！
- 即使目標企業更換了全域網域管理員密碼、更換了 `krbtgt` 金鑰，只要根 CA 證書未被吊銷，此「黃金憑證」永遠有效！

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 深刻理解 Kerberos PKINIT 如何以 X.509 憑證向 KDC 換取 TGT 票證。
- [ ] 能清楚背誦構成 ESC1 漏洞的四個核心標記。
- [ ] 熟練使用 Certipy 工具鏈完成掃描、憑證申請與身分驗證全流程。
- [ ] 掌握 ESC3 註冊代理代表他人申請憑證的兩階段利用鏈。
- [ ] 能清楚說明 CA 私鑰遭外洩後偽造「黃金憑證」達成持久化控制的原理。
