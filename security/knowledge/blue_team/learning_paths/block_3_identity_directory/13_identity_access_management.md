# 🆔 身分存取管理安全 (IAM) 深度學習路徑
> 對應藍隊防衛矩陣：**領域 13** (13.1 ~ 13.3)
> 預計總投入時間：**30 ~ 40 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
以為開了 2FA 就萬無一失  ──►    掌握 MFA 疲勞轟炸 (MFA Fatigue) 與反向代理釣魚
分不清 OAuth 與 SAML 差異 ──►    深入剖析 JWT 權杖竄改與重放攻擊 (Token Replay)
忽視服務帳號 (Service Account)──►能審計過期憑證、未輪換金鑰與工作階段劫持
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
OAuth2.0/SAML  JWT結構與篡改防範  MFA疲勞與繞過防衛  服務帳戶與零信任
(8h)           (10h)             (10h)             (8h)
```

---

## 🔑 階段一：OAuth 2.0 與 SAML 2.0 身分同盟（約 8 小時）

### 1.1 OAuth 2.0 授權碼模式 (Authorization Code Flow)

```
User (瀏覽器) ──► 授權伺服器 (IdP) ──► 取得授權碼 (Code) ──► 換取 Access Token
```

- **重定向 URI (Redirect URI) 寬鬆匹配漏洞**：若授權伺服器未嚴格校驗回呼網址，攻擊者可誘騙 Token 發送至惡意伺服器。

---

## 🛡️ 階段二：MFA 疲勞攻擊 (MFA Fatigue) 與 Passkey 防禦（約 10 小時）

### 2.1 攻擊與加固策略

1. **MFA 疲勞轟炸**：利用攻擊者腳本在深夜高頻發送 Push 通知，誘使疲憊的使用者誤點「允許」。
2. **防禦機制 (Number Matching)**：強制要求使用者在 Authenticator App 輸入螢幕上顯示的雙位數隨機數字，杜絕盲目確認。
3. **FIDO2 / WebAuthn (Passkey)**：基於公開金鑰密碼學與網域綁定，徹底杜絕反向代理 (如 Evilginx) 釣魚竊取 Session Cookie。

---

## 📋 自我評估檢查點

- [ ] 說出 OAuth 2.0 中 Access Token 與 Refresh Token 的用途與有效期限差異。
- [ ] 解釋數字匹配 (Number Matching) 如何終結 MFA 疲勞轟炸。
- [ ] 說明 FIDO2 / 實體安全金鑰 (YubiKey) 為什麼能徹底免疫中間人釣魚網站。
