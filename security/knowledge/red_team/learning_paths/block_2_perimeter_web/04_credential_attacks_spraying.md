# 🔑 憑證秘密恢復、密碼噴灑與撞庫深度學習路徑 (Credential Attacks & Spraying)
> 對應紅隊作戰矩陣：**Phase 2 (R06)** (R06.1 ~ R06.4)  
> 預計總投入時間：**25 ~ 30 小時**（視密碼學雜湊、身分認證協定與自動化工具基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
用 Hydra 暴力破解常觸發帳號鎖定 ──►  精通低頻密碼噴灑 (Password Spraying) 規避閾值
只會用簡單字典跑 Hashcat        ──►  精通 Rule-based 規則突變與自定義掩碼攻擊
拿到洩漏帳密只會逐一手工嘗試   ──►  精通撞庫 (Credential Stuffing) 與 MFA 繞過邏輯
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| 雜湊演算法 (Hash Algorithms) | 理解 MD5, NTLM, SHA-256, bcrypt, PBKDF2 的加鹽與計算成本 | [Hashcat 官方演算法支援列表](https://hashcat.net/wiki/doku.php?id=example_hashes) |
| Active Directory 鎖定策略 | 理解 `lockoutThreshold`、`lockoutDuration` 與觀察窗口機制 | [Microsoft Learn: 帳戶鎖定原則](https://learn.microsoft.com/windows/security/) |
| HTTP 身分驗證機制 | 熟悉 Basic Auth, Digest, Bearer Token 與 Form 認證 | [MDN: HTTP 驗證指南](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
離線雜湊破解   服務猜解/鎖定  外網密碼噴灑   洩漏憑證撞庫   防禦規避日誌
(6h)           (5h)           (8h)           (6h)           (5h)
```

---

## ⚡ 階段一：離線密碼雜湊破解與規則攻擊（約 6 小時）

### 1.1 Hashcat GPU 高速破解與演算法模式
在拿到離線雜湊後，必須選擇正確的 Hashcat 模式（Mode）：
- `mode 1000`: NTLM Hash（速度極快，單卡百億級/秒）
- `mode 3200`: bcrypt `$2a$`（計算耗時，加鹽防彩虹表）
- `mode 13100`: Kerberoasting TGS-REP（五階段 RC4 雜湊）

```bash
# 使用 rockyou 字典搭配 Best64 規則變形破解 NTLM
hashcat -m 1000 -a 0 ntlm_hashes.txt rockyou.txt -r rules/best64.rule -O

# 使用自定義掩碼實施高精準組合爆破（如：年份 + 特殊字元）
hashcat -m 1000 -a 3 ntlm_hashes.txt -1 ?l?d ?u?1?1?1?1?1?1?d?s
```

---

## 🛡️ 階段二：線上服務密碼猜解與帳號鎖定機制探測（約 5 小時）

### 2.1 帳號鎖定閾值 (Account Lockout Threshold) 探針
在對企業發起線上攻擊前，必須確認其是否啟用了防爆破鎖定（例如：失敗 5 次鎖定 30 分鐘）。
- 探測策略：使用 1 個已知的無效測試帳號，發送連續 3 次錯誤密碼，觀察 HTTP 回應狀態碼或回應時間是否發生突變（如從 `401 Unauthorized` 變成 `423 Locked` 或回應延遲增加）。

---

## 🎯 階段三：外網低頻密碼噴灑攻擊實施 (Password Spraying)（約 8 小時）

### 3.1 密碼噴灑核心作戰邏輯
傳統暴力破解是「一個帳號嘗試一千個密碼」（必觸發鎖定）；密碼噴灑則是**「一千個帳號只嘗試一個密碼」**（如 `Company2026!` 或季節密碼 `Spring2026!`）：
```
[外部噴灑工具]
      │
      ├── (輪次 1: 09:00) ──► 全員嘗試 "Spring2026!" ──► (若失敗，休眠 45 分鐘)
      │
      └── (輪次 2: 09:45) ──► 全員嘗試 "Welcome123!" ──► (命中數名員工！)
```

### 3.2 工具鏈操作實戰 (MailSniper / SprayingToolkit)
```bash
# 針對 O365 / OWA 發起單一密碼噴灑，設定每帳號間隔延遲
python3 spray.py -u users.txt -p 'Welcome2026!' -a https://mail.target.com/autodiscover/autodiscover.xml --delay 5
```

---

## 🔄 階段四：已知洩漏憑證重用與撞庫攻擊 (Credential Stuffing)（約 6 小時）

### 4.1 歷史數據洩漏資料庫比對
利用 Have I Been Pwned API 或開源洩漏庫（Comb.txt）篩選出目標企業員工曾在外網（如 LinkedIn、Adobe）洩漏之歷史密碼。
- **密碼重用心理學**：多數人在收到強制換密碼通知時，僅修改密碼末尾數字或符號（如 `Passw0rd1!` ➔ `Passw0rd2!`）。

---

## 🥷 階段五：隱匿作戰與藍隊日誌特徵反制（約 5 小時）

### 5.1 規避 SOC 偵測的關鍵防護指標
- **日誌特徵**：Windows Event ID 4625 (登入失敗)、4624 (登入成功)。
- **反制手法**：
  1. **出口 IP 輪替**：利用 AWS API Gateway 或 Tor 代理池分散連線來源 IP，防止 SOC 以 IP 聚合計數觸發異常警報。
  2. **UA 與 Client 指紋偽裝**：模擬企業常見的 Outlook Mobile 或 Teams 官方客戶端 User-Agent。

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 精通 Hashcat 規則語法與常見哈希類型的破解指令。
- [ ] 能在實戰前精確探測目標服務的帳號鎖定閾值與鎖定時間。
- [ ] 能使用 MailSniper 或自編腳本針對 OWA 執行安全低頻密碼噴灑。
- [ ] 掌握撞庫數據清洗與末尾字元突變猜解思維。
- [ ] 能說明 Windows 4625 日誌的產生特徵與多出口 IP 規避原理。
