# 🏰 Active Directory 網域攻防與防護深度學習路徑 (Active Directory Defense)
> 對應藍隊防衛矩陣：**領域 12** (12.1 ~ 12.5)
> 預計總投入時間：**40 ~ 55 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
知道 AD 是微軟網域管理服務──►    掌握 Kerberos 票據認證全流程與 TGT/ST 加密
聽過 Golden Ticket 攻擊   ──►    精通 AS-REP / Kerberoasting / DCSync 偵測
依賴 GUI 使用者帳號介面   ──►    能使用 BloodHound 審查最短特權路徑與 ACL 漏洞
```

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 → 階段二 → 階段三 → 階段四 → 階段五
Kerberos三步驗證 AS-REP/Kerberoasting 偽造票據防護 DCSync與NTDS 存取控制ACL
(10h)           (10h)                (10h)        (10h)         (10h)
```

---

## 🏁 階段一：Kerberos 協定與票據認證架構（約 10 小時）

```
Client (使用者端)            KDC / Domain Controller (網域控制器)
   │                                     │
   ├─── 1. AS-REQ (身分認證請求) ────────►│
   │◄── 2. AS-REP (核發 TGT 認證票據) ──┤ (以 krbtgt NTLM Hash 加密)
   │                                     │
   ├─── 3. TGS-REQ (請求服務票據 ST) ───►│ (提交 TGT)
   │◄── 4. TGS-REP (核發服務票據 ST) ───┤ (以服務帳號 SPN Hash 加密)
   │                                     │
   └─── 5. AP-REQ ──► 目標服務 (提供 ST 存取資源)
```

---

## 🎯 階段二：AS-REP Roasting 與 Kerberoasting 偵測（約 10 小時）

### 2.1 AS-REP Roasting (預驗證停用帳戶)
- 若帳號設定了 `DONT_REQ_PREAUTH`（不需 Kerberos 預先認證），任何人皆可直接向 KDC 索取該帳號加密的 TGT 進行離線字典爆破。
- **偵測 Event ID**：`4768` (Kerberos TGT 請求)，查看預驗證類型是否為 `0x0` (無預認證)。

### 2.2 Kerberoasting (SPN 服務票據提取)
- 任何網域合法使用者皆可向 KDC 請求已註冊 SPN 之服務票據 (TGS)。
- **偵測 Event ID**：`4769` (服務票據請求)，重點關注弱加密類型 `0x17` (RC4-HMAC)。

---

## 🎫 階段三：黃金票據 (Golden) 與白銀票據 (Silver) 辨析（約 10 小時）

| 特性 | 黃金票據 (Golden Ticket) | 白銀票據 (Silver Ticket) |
| :--- | :--- | :--- |
| **偽造標的** | TGT (全域票據發放憑單) | ST (特定服務票據) |
| **所需金鑰** | 網域核心 **`krbtgt`** NTLM Hash | 特定服務帳號 (如 MSSQL) NTLM Hash |
| **通訊對象** | 不需與 KDC 溝通，可通行全網域 | 直接與目標服務對話，**KDC 完全無日誌！** |
| **防衛處置** | **必須在短時間內輪換兩次 `krbtgt` 密碼** | 重設該受害服務帳號密碼 |

---

## 📋 自我評估檢查點

- [ ] 清楚默畫出 Kerberos AS-REQ 到 AP-REQ 的完整五步交握流程。
- [ ] 說出 Event ID 4768 與 4769 在 Kerberos 攻防日誌中的關鍵欄位與差異。
- [ ] 解釋為什麼清理黃金票據必須連續兩次變更 `krbtgt` 帳號密碼（因為保留舊版金鑰歷史）。
