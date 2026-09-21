# 📶 無線通訊安全機制與協定演進深度學習路徑 (Wireless Security WPA2/WPA3)
> 對應藍隊防衛矩陣：**領域 8** (8.1 ~ 8.2)
> 預計總投入時間：**25 ~ 35 小時**（金盾獎高頻客觀題）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
知道 Wi-Fi 要輸密碼      ──►    掌握 802.11 四向交握 (4-Way Handshake) 底層運作
聽過 WPA2 被破解過       ──►    能深入剖析 KRACK 金鑰重放與離線字典攻擊原理
分不清 WPA2 與 WPA3 差異 ──►    精通 WPA3 Dragonfly (SAE) 前向保密機制
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
WEP/WPA/WPA2演進  4-Way Handshake深度  KRACK與字典攻擊  WPA3 SAE前向保密
(6h)             (10h)                (8h)            (8h)
```

---

## 🏁 階段一：無線安全協定歷史演進與演算法對比（約 6 小時）

```
WEP (64/128-bit RC4, 24-bit IV 碰撞弱點，數分鐘即被破解)
  └──► WPA (過渡期標準: TKIP 暫時金鑰整合協定，增加金鑰混合函數)
        └──► WPA2 (802.11i 正式標準: 強制採用 AES-CCMP 加密)
              └──► WPA3 (最新標準: 採用 SAE 對等實體同步認證、CNSA 192-bit)
```

---

## 🤝 階段二：802.11 四向交握 (4-Way Handshake) 核心運作（約 10 小時）

### 2.1 金鑰階層架構 (Key Hierarchy)

1. **PMK (Pairwise Master Key)**：由使用者預先共享金鑰 (PSK) 透過 PBKDF2 演算法（4096 次 HMAC-SHA1）衍生產生。
2. **PTK (Pairwise Transient Key)**：真正用於單播通訊加密的臨時金鑰。
   - 計算公式：$	ext{PTK} = 	ext{PRF}(	ext{PMK} + 	ext{ANonce} + 	ext{SNonce} + 	ext{AP MAC} + 	ext{Station MAC})$

### 2.2 四向交握流程圖

```
Access Point (AP)                               Station (Client)
       │                                               │
       ├─── 1. 傳送 ANonce ───────────────────────────►│ (Client 產生 SNonce 並計算 PTK)
       │                                               │
       │◄── 2. 傳送 SNonce + MIC (訊息鑑別碼) ────────┤ (AP 驗證 MIC 並計算出相同 PTK)
       │                                               │
       ├─── 3. 傳送 GTK (群組廣播金鑰) + MIC ─────────►│ (Client 安裝 PTK/GTK)
       │                                               │
       │◄── 4. 傳送 ACK 確認 ─────────────────────────┤ (交握完成，開始加密通訊)
```

---

## 💥 階段三：WPA2 離線字典攻擊與 KRACK 重放攻擊（約 8 小時）

### 3.1 離線字典暴破 (Offline Dictionary Attack)

- 攻擊者不需連入網路，僅需側錄步驟 1 與步驟 2 封包（包含 ANonce、SNonce 與 MIC）。
- 在本機利用密碼字典反覆計算候選 PMK 並驗證 MIC 是否吻合。

### 3.2 KRACK (Key Reinstallation Attacks) 金鑰重裝反覆攻擊

- 利用客戶端在未收到步驟 4 ACK 時會重新發送步驟 3 的協定漏洞。
- 誘使客戶端**重新安裝已使用過之金鑰 (Reinstall Nonce)**，使 Nonce 重置為 0，進而破壞串流加密安全性，實現封包重放與解密。

---

## 🛡️ 階段四：WPA3 Dragonfly 協定與 SAE 防衛機制（約 8 小時）

### 4.1 SAE (Simultaneous Authentication of Equals)

- WPA3 捨棄 WPA2 PSK 四向交握，改用基於 RFC 7664 Dragonfly 握手協議的 **SAE**。
- **抗離線字典攻擊**：每次認證使用不同的密鑰交換，攻擊者無法僅透過側錄封包在離線端嘗試猜測密碼。
- **前向保密 (Forward Secrecy)**：即使未來的某一刻預先共享密碼外洩，攻擊者也無法解密過去側錄到的歷史通訊封包。

---

## 📋 自我評估檢查點

- [ ] 說出 PTK 計算時所需的五大輸入元素 (PMK, ANonce, SNonce, AP MAC, Client MAC)。
- [ ] 清楚說明攻擊者如何利用前兩次握手封包發動離線字典攻擊。
- [ ] 解釋 KRACK 攻擊的關鍵成因（金鑰與計數器重複安裝重置）。
- [ ] 闡述 WPA3 的 SAE 協定如何提供「抗離線字典攻擊」與「前向保密」兩大安全承諾。
