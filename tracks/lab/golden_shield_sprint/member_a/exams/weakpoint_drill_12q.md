# 🎯 隊員 A 弱點強化變化題（12 題）

> **用途**：針對 [`final_mock_25q.md`](final_mock_25q.md) 錯題（Q5 SSTI、Q6 寬字節、Q9 Cookie 旗標、Q20 工具分工、Q25 Magic Bytes）各出變化題，把特徵打到反射。
> **用法**：限時 8 分鐘作答，對完答案把仍錯的再抄一次。目標：這 12 題全對。

---

## 🔴 弱點一：SSTI vs XSS 辨識（對應原 Q5）

#### D1.
測試者在搜尋框輸入 `${7*7}`，頁面回顯 `49`。最可能的漏洞與模板引擎為？
* (A) XSS；前端 JavaScript
* (B) SSTI；`${ }` 常見於 FreeMarker / Thymeleaf
* (C) SQL 注入；算術回顯
* (D) 命令注入

#### D2.
下列哪一組輸入與回應，**無法**作為 SSTI 的確認依據？
* (A) 輸入 `{{7*7}}`，回顯 `49`
* (B) 輸入 `{{7*'7'}}`，回顯 `7777777`（Jinja2 字串乘法）
* (C) 輸入 `<script>alert(1)</script>`，彈出警示框
* (D) 輸入 `${{<%[%'"}}%\`，回傳模板引擎的語法錯誤堆疊

#### D3.
某頁面輸入 `{{7*7}}` 原樣顯示 `{{7*7}}`（未變 49），但輸入 `<b>x</b>` 卻以粗體渲染。此最可能為？
* (A) SSTI 成立
* (B) 非 SSTI，而是 XSS / HTML 注入（模板未求值，但 HTML 被渲染）
* (C) SQL 注入
* (D) 寬字節注入

---

## 🟠 弱點二：寬字節注入機制（對應原 Q6）

#### D4.
寬字節注入（GBK + `%df'`）能逃逸 `addslashes` 的根本原因是？
* (A) `%df` 解碼後的位元組等同於單引號 `'`
* (B) `0xDF` 與 `addslashes` 補上的反斜線 `0x5C` 在 GBK 下被合併為一個雙位元組漢字，使反斜線被「吃掉」，其後單引號脫逸
* (C) GBK 會自動移除所有單引號
* (D) PHP 對高位元組停止轉義

#### D5.
下列哪個條件**不是**寬字節注入成立的必要前提？
* (A) 後端對單引號做了 `addslashes` / `magic_quotes`（補反斜線）
* (B) 資料庫連線使用 GBK 等寬字元編碼
* (C) 伺服器開啟了遠端 root 登入
* (D) 注入點位於字串情境需閉合引號

#### D6.
防禦寬字節注入，下列何者最根本？
* (A) 將連線編碼統一設為 `utf8mb4` 並使用參數化查詢
* (B) 再加一層 `addslashes`
* (C) 過濾 `%df`
* (D) 關閉資料庫報錯

---

## 🟡 弱點三：Cookie 三旗標分工（對應原 Q9）

#### D7.
`SameSite=Strict` 的 Cookie 主要防禦哪種攻擊？
* (A) XSS 竊取 Cookie
* (B) CSRF（阻止 Cookie 在跨站請求中被自動攜帶）
* (C) SQL 注入
* (D) 中間人竊聽

#### D8.
某網站僅對 Session Cookie 設定 `Secure` 旗標。這代表？
* (A) JavaScript 無法讀取此 Cookie
* (B) 此 Cookie 僅在 HTTPS 連線中傳送，但 JS 仍可透過 `document.cookie` 讀取
* (C) 此 Cookie 可防止 CSRF
* (D) 此 Cookie 永不過期

#### D9.
欲**同時**降低「XSS 竊 session」與「CSRF」兩種風險，Session Cookie 應至少設定？
* (A) 只設 `Secure`
* (B) `HttpOnly`（防 JS 讀取）＋ `SameSite`（防跨站攜帶），並建議加 `Secure`
* (C) 只設 `Domain`
* (D) 只設 `Path=/`

---

## 🔵 弱點四：Android 工具分工 + Magic Bytes（對應原 Q20、Q25）

#### D10.
下列工具與用途配對，**錯誤**的是？
* (A) jadx → 將 dex 反編譯為近似 Java 原始碼，供閱讀邏輯
* (B) apktool → 反編譯資源與 Smali，修改後可 `apktool b` 重新打包
* (C) Frida → 執行期動態插樁，可繞過 root 偵測 / SSL pinning
* (D) jd-gui → 可編輯並重新編譯 APK 為可安裝檔

#### D11.
分析者只想「**靜態閱讀**」某 APK 的商業邏輯、不打算修改重打包，最有效率的首選工具為？
* (A) jadx
* (B) apktool（還要再手讀 Smali，較費時）
* (C) Frida
* (D) Wireshark

#### D12.
鑑識人員發現一個 `report.pdf`，十六進位開頭為 `50 4B 03 04`。正確判讀為？
* (A) 正常 PDF（PDF 開頭為 `50 4B`）
* (B) `50 4B 03 04` 是 ZIP 的 Magic Bytes，此檔真實為 ZIP 壓縮檔（docx/xlsx/jar 亦以此開頭），副檔名被偽裝
* (C) 這是加密檔
* (D) 開頭位元組與類型無關

---
---

## ✅ 答案與解析

| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **B** | **C** | **B** | **B** | **C** | **A** | **B** | **B** | **B** | **D** | **A** | **B** |

**D1 ─ B**：`${ }` 求值成 49 = SSTI；`${ }` 對應 FreeMarker/Thymeleaf，`{{ }}` 對應 Jinja2/Twig。
**D2 ─ C**：`<script>alert(1)</script>` 彈框是 **XSS** 的證據，不是 SSTI——SSTI 看的是「**算式被伺服器求值**」。A/B/D 都是 SSTI 的確認特徵。
**D3 ─ B**：`{{7*7}}` 未變 49（模板沒求值）但 `<b>` 被渲染 → 是 **XSS/HTML 注入**,不是 SSTI。這就是你原本 Q5 混淆的反向驗證。
**D4 ─ B**：核心是「**反斜線被吃掉**」，不是 `%df` 等於引號（這正是你原本 Q6 選錯的 B 選項陷阱，這裡反轉成正解讓你記牢機制）。
**D5 ─ C**：遠端 root 登入與寬字節注入無關。必要前提是「補反斜線 + 寬字元編碼 + 字串情境」。
**D6 ─ A**：根本防禦 = 統一 `utf8mb4` + 參數化查詢。再加 `addslashes` 反而是問題來源。
**D7 ─ B**：SameSite 管「跨站自動攜帶」→ 防 **CSRF**，不是防 XSS 竊取。
**D8 ─ B**：`Secure` 只保證走 HTTPS 才傳送，**JS 仍讀得到**（要擋讀取得靠 `HttpOnly`）。
**D9 ─ B**：防 XSS 竊 session 用 `HttpOnly`、防 CSRF 用 `SameSite`，兩者分工不同、要並用。
**D10 ─ D**：**錯誤配對**是 D——jd-gui 只能**檢視** `.class`/`.jar`，不能重新編譯 APK。重打包要用 apktool。
**D11 ─ A**：純靜態讀邏輯首選 **jadx**（一鍵 dex→Java）。
**D12 ─ B**：`50 4B 03 04`（`PK..`）是 **ZIP** 魔術位元組；docx/xlsx/apk/jar 本質都是 ZIP。副檔名 `.pdf` 不可信（PDF 應為 `25 50 44 46`）。

---

### 🧠 把這 5 句背起來就免疫

1. **`{{7*7}}`→49 = SSTI**；單純 `<script>` 彈框 = XSS;模板沒求值但 HTML 渲染 = XSS/HTML 注入。
2. **寬字節 = 反斜線被 GBK 吃掉**,不是 `%df` 等於引號。
3. **HttpOnly 防讀(XSS)、SameSite 防跨站(CSRF)、Secure 只走 HTTPS**。
4. **讀邏輯 jadx、重打包 apktool、動態 Frida、看 class jd-gui(不能回編)**。
5. **Magic Bytes**:PNG=`89504E47`、JPG=`FFD8FF`、PDF=`25504446`、ZIP/docx/apk=`504B0304`。
