# 🛡️ 隊員 A 一頁紙秒選速查表（Web ✕ Android ✕ 通識）

> **用途**：10/16 最後掃讀＋考場臨場「看特徵 → 秒選」對照。單選題不扣分、靠辨識特徵拿分，看到左欄關鍵字直接對右欄答案。
> **範圍**：Web 應用安全（主責）＋ Android/Java 逆向（主責）＋ Misc/網路通識 1/3（Linux 權限、Port、雲端責任、隱寫、手算）。
> **配套**：錯題卷 [`exams/final_mock_25q.md`](exams/final_mock_25q.md) ｜ 單元一卷 [`exams/unit_1_exam_25q.md`](exams/unit_1_exam_25q.md)

---

## 🔴 單元一：Web 伺服器端注入（SQLi / 命令注入 / SSTI）

| 題幹特徵關鍵字 | 秒選判斷 |
| :--- | :--- |
| 欄位回顯網頁、要對齊欄位數 | **UNION-based**；先 `ORDER BY n` 猜欄位數 |
| `updatexml` / `extractvalue` / 報錯字串吐資料 | **Error-based 報錯注入**（XPATH 解析異常） |
| 回應只有「存在/不存在」兩種、無報錯 | **Boolean 盲注**；二分法每字元約 **7 次**請求（log₂128） |
| 完全無回顯無報錯、回應長度一致 | **Time-based 時間盲注** |
| 強迫 DB 向外部 DNS 解析、資料拼在子網域 | **OOB 帶外外洩** |
| MySQL 延遲 | `SLEEP()` / `BENCHMARK()` |
| MSSQL 延遲 | `WAITFOR DELAY '0:0:5'` |
| PostgreSQL 延遲 | `pg_sleep(5)` |
| Oracle 延遲 | `dbms_pipe.receive_message()` |
| `id=1 OR 1=1` 無引號就成功、過濾單引號無效 | **整數型注入**（numeric context，不需閉合引號） |
| GBK 編碼 + `%df'` 逃逸 `addslashes` | **寬字節注入**（0xDF+0x5C 併成漢字，單引號脫逸） |
| `ORDER BY $col`、預編譯 `?` 拋語法錯 | 欄位/表名**不能參數化** → 必須**白名單映射** |
| 防 SQLi 唯一正解 | **參數化查詢 / PreparedStatement**（非 WAF、非過濾） |
| `;`、`|`、`&&`、`$(...)`、反引號接系統指令 | **OS 命令注入** |
| 命令注入防護 | 用**參數化 API**（如 `execve` 陣列傳參）、白名單；非跳脫 |
| `{{7*7}}`→`49`、`${...}`、`#{...}` | **SSTI 模板注入**；回傳 49 即確認 |
| Jinja2/Twig `{{}}`、FreeMarker `${}`、Thymeleaf `__${}__` | SSTI 各引擎語法 |

---

## 🟠 單元二：Web 前端與跨站信任邊界（XSS / CSRF / CORS / Cookie）

| 題幹特徵關鍵字 | 秒選判斷 |
| :--- | :--- |
| 參數值即時反射進頁面、非持久 | **Reflected XSS** |
| 留言/暱稱存進 DB 後每個訪客都中 | **Stored XSS**（危害最大） |
| `document.location`/`innerHTML`/`#fragment`、純前端 | **DOM-based XSS**（payload 不經後端） |
| XSS 防護 | 輸出編碼（context-aware escaping）＋ **CSP**；HttpOnly 擋竊 Cookie |
| CSP `nonce` 放行規則 | 僅放行帶相同 nonce 的 `<script>`，擋 inline 注入 |
| 無 token、靠 Cookie 自動攜帶、誘導點擊送請求 | **CSRF** |
| CSRF 防護 | **CSRF Token**（不可預測）＋ `SameSite` Cookie；驗 Origin/Referer |
| `Access-Control-Allow-Origin: *` 搭 `Allow-Credentials: true` | **CORS 錯配**（規範禁止此組合，憑證洩漏） |
| ACAO 反射 Origin 且 ACAC true | 任意站可帶憑證讀回應 → 高危 CORS |
| `HttpOnly` | JS 讀不到 Cookie（擋 XSS 竊 session） |
| `Secure` | 僅 HTTPS 才送 Cookie |
| `SameSite=Strict/Lax` | 擋跨站自動攜帶（防 CSRF） |

---

## 🟡 單元三：Web 架構 / 語意 / 供應鏈（SSRF / 反序列化 / 走私 / JWT）

| 題幹特徵關鍵字 | 秒選判斷 |
| :--- | :--- |
| 伺服器幫你抓 URL、能打內網/`169.254.169.254` | **SSRF**；雲端打 IMDS 偷憑證 |
| SSRF 防護 | 白名單目的地、禁內網網段、**IMDSv2**（需 token） |
| `169.254.169.254/latest/meta-data/` | AWS **IMDS**（Metadata），SSRF 首要目標 |
| 反序列化不可信資料、`__wakeup`/`readObject`/`pickle` | **不安全反序列化** → RCE |
| Java `ObjectInputStream.readObject` / `ysoserial` | Java 反序列化利用鏈 |
| PHP `unserialize()` + POP 鏈 | PHP 物件注入 |
| 前後端對 `Content-Length` / `Transfer-Encoding` 解析不一致 | **HTTP 請求走私**（CL.TE / TE.CL） |
| 快取鍵未納入某 header、污染快取 | **Web 快取污染** |
| `Host` / `X-Forwarded-Host` 被信任做路由/產連結 | **Host 標頭注入**（密碼重置投毒） |
| JWT `alg: none` 被接受 | 偽造 token（未驗簽） |
| JWT 用公鑰當 HMAC 金鑰（RS256→HS256） | **演算法混淆**偽造 |
| `../../etc/passwd`、`%2e%2e` | **路徑穿越 / LFI** |
| `include($_GET['page'])` 引遠端 URL | **RFI**（遠端檔案引入） |
| XML `<!ENTITY xxe SYSTEM "file://...">` | **XXE**（外部實體，讀檔/SSRF） |
| 直接綁定全部請求欄位到物件、偷改 `isAdmin` | **Mass Assignment**（過度綁定） |
| 包名拼寫近似、內部套件被公開同名覆蓋 | **依賴混淆 / 供應鏈**（OWASP 2025 新增） |
| **OWASP 2025 兩大新增** | Software Supply Chain Failures、Mishandling of Exceptional Conditions |

---

## 🔵 單元四：Android / Java 逆向工程

| 題幹特徵關鍵字 | 秒選判斷 |
| :--- | :--- |
| APK 本質 | ZIP 壓縮檔，解壓看 `AndroidManifest.xml`、`classes.dex`、`resources.arsc`、`lib/` |
| 看權限、元件(Activity/Service/Receiver)、匯出旗標 | 讀 **AndroidManifest.xml** |
| 一鍵反編譯成近似 Java 原始碼、看邏輯 | **jadx**（首選讀程式碼） |
| 反編譯資源 + 改 Smali + 回打包 | **apktool**（改 flag/重打包） |
| 看 `.jar`/`.class` 的 Java 原始碼 | **jd-gui** |
| 執行期動態掛鉤、繞過 root/SSL pinning | **Frida**（動態插樁） |
| `.dex` 的組語 | **Smali** 語法 |
| `invoke-virtual` / `invoke-static` | Smali 呼叫方法 |
| `const-string v0, "flag"` | Smali 載入字串常數（flag 常藏這） |
| `if-eqz` / `if-nez` | Smali 條件跳轉（破解驗證邏輯關鍵） |
| `.method` / `.locals` / `return-void` | Smali 方法宣告 |
| Dalvik/ART、暫存器 `v0 v1 p0` | Android VM 與 Smali 暫存器 |

---

## 🟢 單元五：通識 1/3（Linux 權限 / Port / 雲端責任 / 隱寫）

### Linux 權限（手算必考）
| 符號 / 數字 | 意義 |
| :--- | :--- |
| `rwx` = 4+2+1 = 7 | 讀=4 寫=2 執行=1 |
| `755` = `rwxr-xr-x` | owner 全權、group/other 讀執行 |
| `644` = `rw-r--r--` | 一般檔案常見 |
| `4755` 開頭 **4** | **SUID**（以檔案擁有者身分執行，提權關鍵） |
| `2755` 開頭 **2** | SGID |
| `1777` 開頭 **1** | Sticky bit（如 `/tmp`，只能刪自己的） |
| 找提權點 | `find / -perm -4000`（找 SUID binary）→ GTFOBins |

### 常用 Port（背到反射）
| Port | 服務 | Port | 服務 |
| :-- | :-- | :-- | :-- |
| 20/21 | FTP | 143 | IMAP |
| 22 | SSH | 161 | SNMP |
| 23 | Telnet | 389 | LDAP |
| 25 | SMTP | 443 | HTTPS |
| 53 | DNS | 445 | SMB |
| 80 | HTTP | 3306 | MySQL |
| 110 | POP3 | 3389 | RDP |
| 135/139 | NetBIOS/RPC | 5432 | PostgreSQL |
| 6379 | Redis | 27017 | MongoDB |

### 雲端共同責任模型
| 模式 | 雲商負責 | 客戶負責 |
| :--- | :--- | :--- |
| **IaaS** | 實體/網路/虛擬化 | OS 以上全部（含修補、App、資料） |
| **PaaS** | ＋OS/執行環境 | App 程式碼＋資料＋存取控制 |
| **SaaS** | ＋App | **僅資料與使用者存取管理** |
| 不變鐵律 | — | **資料與身分(IAM)永遠是客戶責任** |

### Misc / 隱寫 / 手算
| 特徵 | 工具 / 手法 |
| :--- | :--- |
| 圖片藏料、看 metadata | `exiftool`、`binwalk`（夾檔）、`strings` |
| 圖片 LSB 隱寫 / 密碼夾帶 | `steghide`、`zsteg`、`stegsolve` |
| 檔案真實類型（副檔名造假） | **Magic Bytes**：PNG=`89 50 4E 47`、JPG=`FF D8 FF`、PDF=`25 50 44 46`、ZIP=`50 4B 03 04` |
| Base64 特徵 | 大小寫數字 `+/`、`=` 補尾、長度 4 倍數 |
| Hex→ASCII | 每 2 碼 = 1 字元（`41`=A、`61`=a、`30`=0） |

### 紙筆手算速記
- **Hex↔Dec**：`A=10 B=11 C=12 D=13 E=14 F=15`；`0xFF=255`、`0x10=16`。
- **ASCII 錨點**：`A=65(0x41)`、`a=97(0x61)`、`0=48(0x30)`、空白=32。
- **Base64**：3 bytes(24bit) → 4 字元(每 6bit)；`=` 數量=補的 byte 數。
- **權限**：先寫 `rwxrwxrwx`，每組二進位轉八進位。

---

## ⚠️ 單元六:誘答陷阱紅旗(看到這些要警覺)

- 「防 SQLi 最佳解」選項出現 **WAF / 過濾單引號 / 前端 JS 驗證** → 全是誘答,**正解永遠是參數化查詢**。
- 「`alg:none` 不安全」是對的;但 JWT **只 Base64 不加密**,放機敏資料本身就錯。
- CORS `*` 搭 `credentials:true` 瀏覽器會**拒絕**,題目問「為何失敗」別選「成功」。
- SUID 找提權用 `-perm -4000` 不是 `-perm 4000`(後者要完全相等)。
- Android「反編譯看邏輯」選 jadx;「改了要重打包」才選 apktool,別混。
- 時間同分比速度 → **不確定的題先跳、全部要填**(不扣分)。
