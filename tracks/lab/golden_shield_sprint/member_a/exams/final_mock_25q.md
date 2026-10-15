# 🛡️ 金盾獎初賽收尾全真模擬卷：隊員 A 跨單元綜合卷（25 題）

> **考試科目**：隊員 A 全主責綜合 —— Web 應用安全 ✕ Android/Java 逆向 ✕ 通識 1/3（Linux 權限・Port・雲端責任・隱寫・手算）
> **試卷規模**：25 道全真單選情境題（滿分 100 分，每題 4 分）
> **建議作答時間**：18 ～ 22 分鐘（平均每題 45 秒，模擬初賽 90 分鐘臨場節奏）
> **合格門檻**：84 分（答對 21 題以上即達「秒殺級」）
> **配套**：速查表 [`../CHEATSHEET_1PAGE.md`](../CHEATSHEET_1PAGE.md) ｜ 單元一卷 [`unit_1_exam_25q.md`](unit_1_exam_25q.md)
> **用法**：先全部作答（答錯不扣分，務必每題都填），再對文末解析。錯題紅筆標記，補進錯題庫。

---

## 📑 試題卷（答案與解析位於文末）

### 第一部分：Web 注入與伺服器端（Q1 ~ Q7）

#### Q1.【SQLi 類型判讀】
某端點 `search.php?q=` 無論輸入任何值，頁面內容與長度皆完全一致、不噴報錯；但輸入 `' OR SLEEP(3)-- ` 時頁面延遲約 3 秒才回應。此為何種注入？
* (A) UNION-based 聯合查詢注入
* (B) Error-based 報錯注入
* (C) Boolean-based 布林盲注
* (D) Time-based 時間盲注

#### Q2.【延遲函數對應】
承上，若後端資料庫改為 **Microsoft SQL Server**，下列何者為正確的時間延遲驗證語法？
* (A) `' OR SLEEP(5)-- `
* (B) `' OR pg_sleep(5)-- `
* (C) `'; WAITFOR DELAY '0:0:5'-- `
* (D) `' OR dbms_pipe.receive_message('a',5)-- `

#### Q3.【防禦唯一正解】
關於防禦 SQL 注入，下列何者為**根本且最可靠**的做法？
* (A) 在前端以 JavaScript 過濾單引號與分號
* (B) 使用參數化查詢（Prepared Statement），將程式碼與資料嚴格分離
* (C) 部署 WAF 攔截含 `UNION`、`SELECT` 的請求
* (D) 對使用者輸入做 `addslashes` 跳脫所有引號

#### Q4.【OS 命令注入】
後端程式碼 `system("ping -c 4 " . $_GET['host']);`。攻擊者輸入 `host=8.8.8.8; cat /etc/passwd` 可讀取系統檔案。此漏洞類型與最佳防禦分別為？
* (A) SSTI；改用沙箱模板引擎
* (B) OS 命令注入；改用參數化執行 API（如陣列傳參 `execve`）並採白名單
* (C) 路徑穿越；過濾 `../`
* (D) SSRF；禁止存取內網

#### Q5.【SSTI 確認】
滲透測試時於留言欄輸入 `{{7*7}}`，頁面回顯 `49`。這代表後端最可能存在何種漏洞？其對應引擎語系？
* (A) XSS；純前端 JavaScript 執行
* (B) SSTI 伺服器端模板注入；`{{ }}` 常見於 Jinja2 / Twig
* (C) SQL 注入；`7*7` 觸發算術型回顯
* (D) 命令注入；`*` 觸發萬用字元展開

#### Q6.【寬字節注入】
PHP 舊系統以 `addslashes` 將 `'` 轉為 `\'`，資料庫連線編碼為 **GBK**。攻擊者送出 `%df'` 竟成功逃逸。底層原因為？
* (A) `0xDF` 與轉義斜線 `0x5C` 在 GBK 下被合併解碼為一個雙位元組漢字，使其後單引號脫逸生效
* (B) `%df` 在 URL 解碼後等於單引號本身
* (C) GBK 編碼會自動刪除所有反斜線
* (D) PHP 對 `%df` 觸發記憶體洩漏

#### Q7.【ORDER BY 注入防禦】
排序功能 `... ORDER BY $col`，工程師改用預編譯佔位符 `?` 綁定 `$col` 卻拋出語法錯誤。正確理解為？
* (A) 資料庫驅動的 Bug，重啟即可
* (B) 欄位名/表名/排序關鍵字依 SQL 標準不可作為參數佔位符，須改用伺服器端**白名單映射**
* (C) 預編譯只支援數字欄位
* (D) 改用前端過濾特殊字元即可

---

### 第二部分：跨站與前端信任邊界（Q8 ~ Q12）

#### Q8.【XSS 類型】
論壇留言被存入資料庫後，每位瀏覽該貼文的使用者瀏覽器都會執行攻擊者植入的 `<script>`。此為何種 XSS？其危害特性？
* (A) Reflected XSS；需誘導受害者點擊特製連結
* (B) Stored XSS；持久化於伺服器，所有訪客自動觸發，危害最廣
* (C) DOM-based XSS；payload 不經伺服器
* (D) Self-XSS；僅受誘導自行貼入腳本者本人受影響、不跨使用者傳播

#### Q9.【Cookie 旗標】
欲讓 Session Cookie 在 XSS 發生時**無法被 JavaScript 讀取**以降低被竊風險，應設定下列哪個旗標？
* (A) `Secure`
* (B) `SameSite=Lax`
* (C) `HttpOnly`
* (D) `Domain=.example.com`

#### Q10.【CSRF 本質與防禦】
某轉帳功能僅憑瀏覽器自動攜帶的 Session Cookie 驗證身分、無任何不可預測 token。攻擊者誘導已登入使用者點擊惡意頁面即可觸發轉帳。此漏洞與最佳防禦為？
* (A) XSS；輸出編碼
* (B) CSRF；加入不可預測的 CSRF Token 並設定 `SameSite` Cookie
* (C) SSRF；禁止內網存取
* (D) 點擊劫持；設定 `X-Frame-Options`

#### Q11.【CORS 錯配】
某 API 回應標頭同時出現 `Access-Control-Allow-Origin: *` 與 `Access-Control-Allow-Credentials: true`。關於此配置，下列敘述何者正確？
* (A) 這是安全的最佳實務，允許所有來源共享資源
* (B) 瀏覽器會拒絕此組合——萬用字元 `*` 不得與憑證模式併用；真正高危的是「反射 Origin + credentials:true」
* (C) 此配置可防止 CSRF
* (D) 此配置僅影響同源請求

#### Q12.【DOM XSS 判讀】
某單頁應用以 `document.getElementById('out').innerHTML = location.hash.substring(1)` 將網址 `#` 後內容直接寫入頁面。此漏洞的關鍵特徵為？
* (A) payload 完全在前端處理、不經後端伺服器，屬 DOM-based XSS
* (B) 必定會被伺服器端 WAF 攔截
* (C) 屬於 Stored XSS，因資料存於 DOM
* (D) 僅在舊版 IE 可觸發

---

### 第三部分：架構、語意與供應鏈（Q13 ~ Q17）

#### Q13.【SSRF 打雲端 IMDS】
某圖片代理功能讓伺服器依使用者提供的 URL 抓取圖片。攻擊者填入 `http://169.254.169.254/latest/meta-data/iam/security-credentials/`。此攻擊鏈與目標為？
* (A) 路徑穿越；讀取本機 `/etc/passwd`
* (B) SSRF；存取雲端 Metadata 服務（IMDS）竊取臨時 IAM 憑證
* (C) XXE；外部實體解析
* (D) 快取污染；汙染 CDN
> 進階：最有效的防禦為？→ 啟用 **IMDSv2**（要求帶 token 的 PUT 請求，使單純 SSRF GET 失效）。

#### Q14.【JWT 演算法混淆】
某系統以 RS256（非對稱）簽發 JWT，但後端驗證時未鎖定演算法。攻擊者將標頭改為 `HS256`，並以**公開的 RSA 公鑰**作為 HMAC 金鑰重新簽名，竟驗證通過。此為何種弱點？
* (A) `alg:none` 繞過
* (B) 演算法混淆攻擊（RS256→HS256）：將公鑰當對稱金鑰偽造簽章
* (C) JWT 重放攻擊
* (D) Session Fixation

#### Q15.【反序列化】
Java 應用對來自使用者的位元組流直接呼叫 `ObjectInputStream.readObject()`。攻擊者藉由 `ysoserial` 構造的 gadget chain 達成遠端程式碼執行。此漏洞根因為？
* (A) 緩衝區溢位
* (B) 不安全的反序列化：反序列化不可信資料時觸發利用鏈，應改用白名單/簽章驗證或避免原生序列化
* (C) 整數溢位
* (D) 競態條件

#### Q16.【HTTP 請求走私】
前端代理依 `Content-Length` 判斷請求邊界，後端伺服器卻依 `Transfer-Encoding: chunked` 判斷，兩者解析不一致導致請求被「夾帶」。此攻擊名稱與類型標記為？
* (A) 快取投毒；CP
* (B) HTTP 請求走私；CL.TE（前端用 CL、後端用 TE）
* (C) SSRF；內網穿透
* (D) Host 標頭注入

#### Q17.【OWASP 2025 新增項】
相較 OWASP Top 10 2021，2025 版新增了兩個類別。下列何者為其中之一，且常以「內部套件被外部同名惡意套件覆蓋」的依賴混淆呈現？
* (A) Broken Access Control
* (B) Software Supply Chain Failures（軟體供應鏈失效）
* (C) Cross-Site Scripting
* (D) Security Misconfiguration

---

### 第四部分：Android / Java 逆向（Q18 ~ Q21）

#### Q18.【APK 結構】
關於 Android APK 檔案，下列敘述何者正確？
* (A) APK 是加密容器，必須私鑰才能開啟
* (B) APK 本質是 ZIP 壓縮檔，可解壓取得 `AndroidManifest.xml`、`classes.dex`、`resources.arsc` 等
* (C) APK 內的程式邏輯以原始 Java `.java` 檔形式存放
* (D) APK 無法被反編譯

#### Q19.【工具分工】
分析者欲「將 APK 一鍵反編譯為近似 Java 原始碼以閱讀商業邏輯」，最適合的工具為？
* (A) apktool（主要用於資源反編譯與 Smali 層級重打包）
* (B) jadx（將 dex 反編譯為近似 Java 原始碼，適合讀邏輯）
* (C) Frida（執行期動態插樁）
* (D) Wireshark（封包分析）

#### Q20.【重打包場景】
分析者想修改 APK 內某驗證邏輯、改完後**重新打包成可安裝的 APK**，最合適的工具與產物層級為？
* (A) jadx；直接編輯其輸出的 `.java`
* (B) apktool；反編譯為 Smali、修改後以 `apktool b` 重新打包
* (C) jd-gui；編輯 `.class`
* (D) strings；直接改二進位

#### Q21.【Smali 語法】
在 Smali 程式碼中看到 `const-string v0, "S3cr3t_K3y"` 緊接著 `invoke-virtual {...}, ...equals(...)` 與 `if-eqz v0, :cond_0`。這段最可能的功能為？
* (A) 宣告一個網路 Socket
* (B) 載入字串常數並進行相等比對後條件跳轉——常是**硬編碼密鑰/flag 的驗證邏輯**
* (C) 進行浮點數運算
* (D) 配置 UI 版面

---

### 第五部分：通識 1/3（Q22 ~ Q25）

#### Q22.【Linux 權限手算】
某檔案權限為 `-rwsr-xr-x`，擁有者為 root。關於開頭的 `s`，下列敘述何者正確？
* (A) 這是 Sticky bit，僅能刪除自己的檔案
* (B) 這是 SUID 位元（八進位 4000），執行時以**檔案擁有者(root)身分**運行，是本機提權的重點目標
* (C) 這是 SGID 位元，以群組身分執行
* (D) `s` 僅表示符號連結

#### Q23.【找 SUID 提權點】
在取得低權限 shell 後，欲列舉系統上所有具 SUID 位元的可執行檔以尋找提權點，正確指令為？
* (A) `find / -perm 4000`（完全相等比對，易漏）
* (B) `find / -perm -4000 -type f 2>/dev/null`（含有 SUID 位元即列出）
* (C) `ls -laR /`
* (D) `chmod 4000 /bin/bash`

#### Q24.【雲端共同責任】
在 **SaaS** 模式下（如使用雲端 CRM），客戶端**仍須自行負責**的核心項目為？
* (A) 作業系統修補
* (B) 實體機房安全
* (C) 應用程式原始碼維護
* (D) 自身資料的分類保護與使用者身分存取管理（IAM）

#### Q25.【Magic Bytes / 隱寫手算】
鑑識時發現一個副檔名為 `.jpg` 的檔案，但以十六進位檢視其開頭為 `89 50 4E 47 0D 0A 1A 0A`。關於此檔案，正確判讀為？
* (A) 它是正常的 JPEG 檔（JPG 開頭為 `89 50`）
* (B) 開頭 `89 50 4E 47` 是 PNG 的 Magic Bytes，副檔名被竄改，真實類型為 **PNG**
* (C) 這是加密檔，無法判讀
* (D) 開頭不影響檔案類型，純看副檔名

---
---

## ✅ 答案與詳解

| 題號 | 答案 | 題號 | 答案 | 題號 | 答案 | 題號 | 答案 | 題號 | 答案 |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Q1 | **D** | Q6 | **A** | Q11 | **B** | Q16 | **B** | Q21 | **B** |
| Q2 | **C** | Q7 | **B** | Q12 | **A** | Q17 | **B** | Q22 | **B** |
| Q3 | **B** | Q8 | **B** | Q13 | **B** | Q18 | **B** | Q23 | **B** |
| Q4 | **B** | Q9 | **C** | Q14 | **B** | Q19 | **B** | Q24 | **D** |
| Q5 | **B** | Q10 | **B** | Q15 | **B** | Q20 | **B** | Q25 | **B** |

---

### 詳解

**Q1 ─ D**：回應內容/長度一致（排除 Boolean）、無報錯（排除 Error）、無回顯欄位（排除 UNION），但 `SLEEP(3)` 造成可觀測延遲 → **時間盲注**。
> 誘答：C 布林盲注需要「兩種不同回應」，此處回應完全一致，故不成立。

**Q2 ─ C**：MSSQL 用 `WAITFOR DELAY`；`SLEEP` 是 MySQL、`pg_sleep` 是 PostgreSQL、`dbms_pipe.receive_message` 是 Oracle。**四大 DB 延遲函數務必背熟**。

**Q3 ─ B**：防 SQLi 的根本是**程式碼與資料分離**（參數化查詢）。A/C/D 皆為可繞過的輔助手段，是經典誘答——WAF 可繞、`addslashes` 有寬字節問題、前端過濾形同虛設。

**Q4 ─ B**：`;` 串接系統指令 = **OS 命令注入**。最佳防禦是**參數化執行**（陣列傳參避免 shell 解析）＋白名單，而非黑名單跳脫。

**Q5 ─ B**：`{{7*7}}` 回傳 `49` 是 **SSTI** 的教科書確認特徵（算式被伺服器端模板引擎求值）。`{{ }}` 語法對應 Jinja2/Twig。若是 XSS，`7*7` 不會被求值成 49。

**Q6 ─ A**：寬字節注入。`addslashes` 把 `'` 變 `\'`（即 `0x5C 0x27`）；送 `%df`（`0xDF`）後變成 `0xDF 0x5C 0x27`，GBK 把 `0xDF5C` 當一個漢字吃掉，`0x27`（`'`）就脫逸出來。

**Q7 ─ B**：SQL 標準中**識別字（欄位/表名）與關鍵字不能參數化**，只有「值」能綁定。排序欄位必須用**白名單映射**（如 `{'price':'price','date':'created_at'}`）。

**Q8 ─ B**：存入 DB、所有訪客觸發 = **Stored XSS**，持久且影響面最大。A（反射）需誘點連結、C（DOM）不經伺服器。

**Q9 ─ C**：`HttpOnly` 讓 `document.cookie` 讀不到該 Cookie，降低 XSS 竊 session 風險。`Secure` 管傳輸加密、`SameSite` 管跨站攜帶，皆非此題目的。

**Q10 ─ B**：僅憑自動攜帶的 Cookie、無不可預測 token、誘導點擊觸發 = **CSRF**。防禦雙保險：**CSRF Token + SameSite**。

**Q11 ─ B**：規範明訂 `ACAO: *` **不得**搭配 `ACAC: true`，瀏覽器會拒絕帶憑證的跨源讀取。真正可利用的高危配置是「**反射任意 Origin + credentials:true**」。A 是典型誘答。

**Q12 ─ A**：資料從 `location.hash` 經 `innerHTML` 寫入、全程在瀏覽器端，後端從未接觸 payload → **DOM-based XSS**，伺服器端 WAF 往往看不到（因 `#` 後內容不送到伺服器）。

**Q13 ─ B**：`169.254.169.254` 是雲端 **IMDS**（Metadata）位址，透過 **SSRF** 可竊取臨時 IAM 憑證。防禦首推 **IMDSv2**（需 token 的 PUT，使單純 GET 的 SSRF 失效）。

**Q14 ─ B**：後端未鎖演算法 → 攻擊者把 RS256 改 HS256，用**公開的公鑰**當 HMAC 密鑰偽造簽章 = **演算法混淆**。防禦：伺服器端硬性指定允許的 `alg`。

**Q15 ─ B**：對不可信位元流呼叫 `readObject()` + gadget chain = **不安全反序列化** → RCE。防禦：避免原生序列化、白名單類別、簽章校驗。

**Q16 ─ B**：前端用 `Content-Length`、後端用 `Transfer-Encoding` → **CL.TE 請求走私**。（反過來前 TE 後 CL 為 TE.CL。）

**Q17 ─ B**：OWASP 2025 兩大新增 = **Software Supply Chain Failures** 與 Mishandling of Exceptional Conditions。依賴混淆/同名套件覆蓋屬供應鏈失效。A/C/D 皆為既有項目。

**Q18 ─ B**：APK = ZIP。可直接解壓檢視 `AndroidManifest.xml`、`classes.dex`、`resources.arsc`、`lib/`。程式以 dex 位元碼存放，非原始 `.java`。

**Q19 ─ B**：讀商業邏輯選 **jadx**（dex→近似 Java）。apktool 偏資源/Smali 重打包、Frida 偏動態。**「讀邏輯用 jadx、重打包用 apktool」是高頻分工考點**。

**Q20 ─ B**：要改驗證並**重新打包成可安裝 APK**，須走 **apktool**（反編譯 Smali → 改 → `apktool b` 回打包 → 重簽名）。jadx 的輸出僅供閱讀、無法回編譯。

**Q21 ─ B**：`const-string` 載入字串常數 + `equals` 比對 + `if-eqz` 條件跳轉 = 典型**硬編碼密鑰/flag 驗證**。CTF 逆向常直接在此讀出 flag 或改跳轉繞過。

**Q22 ─ B**：擁有者權限位的 `s` = **SUID（4000）**，執行時以檔案擁有者（此處 root）身分運行，是本機提權主戰場。Sticky bit 顯示在 other 的執行位（如 `/tmp` 的 `t`）。

**Q23 ─ B**：`-perm -4000` 的減號表示「**含有**該位元即符合」；`4000`（無減號）要求權限位**完全相等**，會漏掉 `4755` 等。這是經典指令陷阱。

**Q24 ─ D**：鐵律——**資料與身分存取（IAM）永遠是客戶責任**，不論 IaaS/PaaS/SaaS。SaaS 下 OS/實體/App 皆由雲商負責，故 A/B/C 錯。

**Q25 ─ B**：`89 50 4E 47` 是 **PNG** 的 Magic Bytes（`\x89PNG`）。副檔名 `.jpg` 不可信，真實類型為 PNG。JPG 應為 `FF D8 FF`。**鑑識看 Magic Bytes 不看副檔名**。

---

## 📊 成績對照

| 答對題數 | 評級 | 建議 |
| :--- | :--- | :--- |
| 24 ~ 25 | 🏆 秒殺級 | 穩定主責，可支援隊友通識題 |
| 21 ~ 23 | ✅ 合格 | 錯題精修即可上場 |
| 17 ~ 20 | ⚠️ 待加強 | 回速查表＋錯題重做一輪 |
| ≤ 16 | 🔴 急救 | 鎖定錯最多的單元，Day 2~3 重點補強 |

> **錯題回鎖**：Web 錯 → [`../web/`](../web/)；Android 錯 → [`../android/`](../android/)；通識錯 → [`../misc_cloud/`](../misc_cloud/) 與 [`../CHEATSHEET_1PAGE.md`](../CHEATSHEET_1PAGE.md)。
