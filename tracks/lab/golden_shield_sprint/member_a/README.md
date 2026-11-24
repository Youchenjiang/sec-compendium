# 🛡️ 金盾獎初賽隊員 A（蔣）專屬準備手冊與全套教材庫

> **初賽時間**：民國 115 年 10 月 17 日（限時 90 分鐘，斷網閉卷，單選題，全隊共用 1 台電腦，附紙筆）  
> **成員定位**：隊員 A（蔣）  
> **核心主責**：**Web 應用安全** ＋ **Android / Java 逆向工程**  
> **通識分攤**：**Misc 與網路通識（1/3：Linux 權限、常用 Port、雲端共同責任模型、Misc 隱寫）**  
> **來源依據**：提取自 [`金盾獎初賽三人分工檢核表.md`](../金盾獎初賽三人分工檢核表.md) 與團隊實戰 Playbook 庫  
> 🔥 **本週個人衝刺戰略表**：👉 [`SPRINT_PLAN_7DAYS.md`](SPRINT_PLAN_7DAYS.md)（三位一體：檢核 ✕ Playbook ✕ PortSwigger 學院 7 天推進表）

---

## 📅 隊員 A 階段衝刺時程表

| 階段與日期 | 隊員 A 專屬核心任務 | 成果交付物 |
| :--- | :--- | :--- |
| **階段一<br>9/28 – 9/30** | • 完成報名表件、個資/肖像權同意書確認<br>• 獨立做一遍 2024 冰茶初賽回憶題中的 Web、Android、通識題<br>• 標記「答不出的主題」並加入下方檢核清單 | 初賽起點測驗盲點清單 |
| **階段二<br>10/1 – 10/7** | • **全面讀完主責教材**：Web 15 大項 ＋ Android 4 大項<br>• 熟記各漏洞特徵、常見 payload、防護機制與工具用途<br>• 整理出「隊員 A 一頁紙極速速查表 (Cheat Sheet)」 | 隊員 A 核心考點速查表 |
| **階段三<br>10/8 – 10/13** | • **交叉講解**：對隊員 B（葉）、隊員 C（李）進行 30 分鐘 Web & Android 考點精華分享<br>• **出題對戰**：出 15 題 Web/Android/通識單選題供小隊限時模擬交換作答<br>• 複習近一年重大資安事件與 CVE（尤其是 Web 與軟體供應鏈） | 15 題全真單選題 ＋ 交叉檢討筆記 |
| **階段四<br>10/14 – 10/16** | • 鎖定錯題庫與速查表做最後衝刺記憶<br>• 搭配紙筆手算進位轉換、hex 轉 ASCII、Base64 解碼<br>• 確認考場交通與身分證件 | 零死角應試狀態 |

---

## 📦 隊員 A 專屬 6 大核心作戰單元架構

為落實「輸入驗證 ➔ 跨站邊界 ➔ 系統架構 ➔ 行動逆向 ➔ 通識手算 ➔ 工具閉環」的清晰複習路徑，隊員 A 全科目切分為 **6 大作戰單元**：

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   🛡️ 隊員 A 專屬 6 大作戰單元架構                                │
├───────────────────────────────────┬──────────────────────────────────┬───────────────────────────┤
│ 【單元一】Web 伺服器端核心注入    │ 【單元二】Web 前端與跨站信任邊界 │ 【單元三】Web 架構/語意/供應鏈│
│ (SQLi / 命令注入 / SSTI)          │ (XSS / CSRF / CORS / Cookie)     │ (SSRF / 反序列化 / 走私)  │
├───────────────────────────────────┼──────────────────────────────────┼───────────────────────────┤
│ 【單元四】Android / Java 逆向工程 │ 【單元五】隊員 A 專屬通識 1/3    │ 【單元六】工具總表與真題閉環│
│ (APK結構 / Smali語法 / 四大工具)  │ (Linux權限 / Ports / 雲端責任)   │ (防誘答陷阱 / 15題出題對戰)│
└───────────────────────────────────┴──────────────────────────────────┴───────────────────────────┘
```

| 單元編號與名稱 | 核心覆蓋範圍 | 關鍵秒殺題眼與考點 | 核心對應 Playbooks |
| :--- | :--- | :--- | :--- |
| **【單元一】<br>Web 伺服器端核心注入** | • SQL 注入全景（五大維度、四大延遲函數、寬字節、ORDER BY 注入、二階注入）<br>• OS 命令注入（管道符、`${IFS}` 空白繞過）<br>• SSTI 模板注入（Jinja2 / Twig 語法） | • 根本防禦必選「參數化查詢 (Prepared Statements)」<br>• `ORDER BY` 無法參數化，需靠伺服器白名單<br>• 看到 `%df'` 秒選寬字節<br>• 延遲函數對應 DB 廠牌（MySQL/MSSQL/PG/Oracle） | [`web/R10.1`](web/R10.1_sql_query_injection.md)<br>[`web/R10.2`](web/R10.2_os_command_shell_injection.md)<br>[`web/R10.3`](web/R10.3_server_side_template_injection.md)<br>👉 [**單元一 25 題檢定卷**](exams/unit_1_exam_25q.md) |
| **【單元二】<br>Web 前端與跨站信任邊界** | • XSS 三大類型（Reflected, Stored, DOM-based）與 CSP nonce<br>• CSRF 防禦與 Cookie 旗標（SameSite Strict/Lax/None, HttpOnly, Secure）<br>• CORS 設定錯誤（反射 Origin ＋ `Allow-Credentials: true`）<br>• 狀態碼 (401 vs 403) 與郵件驗證 (SPF/DKIM/DMARC) | • `HttpOnly` 防 XSS 偷 Cookie，**無法防 CSRF**<br>• CSRF 防護：SameSite Cookie、Anti-CSRF Token、驗證碼<br>• 401（未驗證身分）vs 403（已驗證但無權限）<br>• SPF 屬 TXT 記錄，DMARC 定處置原則 | [`web/R14.1~14.5`](web/R14.1_reflected_cross_site_scripting.md) |
| **【單元三】<br>Web 架構、語意與深層利用** | • SSRF（偽協定 `gopher://`, 雲端 IMDS `169.254.169.254`, DNS Rebinding）<br>• 檔案包含 LFI/RFI 與 PHP 偽協定（`php://filter` 讀源碼）<br>• 反序列化（PHP `__destruct`/`__wakeup`, Java readObject, Log4Shell JNDI）<br>• XXE 外部實體宣告 (`SYSTEM`)<br>• JWT 攻擊（`alg: none`, RS256 轉 HS256 演算法混淆）<br>• HTTP 請求走私 (CL.TE / TE.CL)<br>• OWASP Top 10:2025（A03 軟體供應鏈安全） | • 雲端元數據 IP 必背 `169.254.169.254`<br>• XXE 根本防禦為禁用外部 DTD 解析<br>• JWT 演算法混淆：拿公鑰當對稱密鑰簽名<br>• HTTP 走私：前後端對 `Content-Length` 與 `Transfer-Encoding` 長度判定不一致 | [`web/R11.1~11.4`](web/R11.1_server_side_request_forgery.md)<br>[`web/R12.1~12.3`](web/R12.1_unsafe_deserialization_object_injection.md)<br>[`web/R13.1`](web/R13.1_http_request_smuggling_desynchronization.md)<br>[`web/R09.1`](web/R09.1_application_session_state_forgery_validation_bypass.md)<br>[`web/04.1`](web/04.1_supply_chain_dependency_confusion.md) |
| **【單元四】<br>Android / Java 逆向工程** | • APK 解剖結構（`AndroidManifest.xml` 四大元件, `classes.dex`, `resources.arsc`, `lib/` 各架構 `.so`）<br>• Smali 組合語言語法速讀（暫存器 `v`/`p`, `invoke-virtual`, `if-eqz`, 型態符號）<br>• 四大工具鏈分工（jadx, apktool, Frida, ProGuard）<br>• Java 混淆防護（ProGuard 類別方法轉 a, b, c） | • 初賽不考寫 Frida 腳本，考讀懂 Smali 與認工具<br>• `jadx` 輸出高階 `.java` 源碼；`apktool` 拆解出 `smali/` 組合代碼<br>• 動態 Hook 函式、繞過 Pinning 首選 `Frida`<br>• 四大元件：Activity, Service, Broadcast Receiver, Content Provider | [`android/26.1`](android/26.1_android_apk_malware_static_decompilation.md)<br>[`android/26.2`](android/26.2_android_runtime_logs_sqlite_forensics.md) |
| **【單元五】<br>隊員 A 專屬通識 1/3** | • Linux 權限模型（chmod 八進位換算 `r=4, w=2, x=1`；SUID `4000`, SGID `2000`, Sticky bit `1000`）<br>• 14 大核心通訊埠 Ports (21, 22, 23, 25, 53, 80, 110, 143, 161, 389, 443, 445, 3306, 3389)<br>• 雲端計算共同責任模型（IaaS vs PaaS vs SaaS 邊界劃分）<br>• Misc 檔案隱寫（ZIP 偽加密 `00 00` ➔ `09 00`；PNG `IHDR` 高度竄改與 CRC32 校驗） | • Linux 看到 `rwsr-xr-x` 秒選 SUID（數值 4000，GTFOBins 提權）<br>• DNS 預設 UDP 53，區域傳送 AXFR 為 TCP 53<br>• IaaS 客戶管 OS/Patch/Firewall；PaaS 客戶管 App 與設定；SaaS 客戶管帳號與資料<br>• 隱寫工具：`binwalk` (檔案雕刻), `steghide` (圖音密碼隱寫), `zsteg` (LSB) | [`misc_cloud/05.1`](misc_cloud/05.1_cloud_shared_responsibility_matrix.md)<br>[`misc_cloud/R18.1`](misc_cloud/R18.1_linux_suid_sgid_binary_abuse.md) |
| **【單元六】<br>工具總表辨識與全真出題對抗** | • 跨領域工具總表辨識（Web, 逆向, 封包, 鑑識, 隱寫）<br>• 誘答選項防陷阱（`gflags` 是 Windows 除錯工具，**不是**掃描器！）<br>• 產出隊員 A 一頁紙極速速查表 (Cheat Sheet)<br>• 親自編寫 15 道全真單選模擬題（含解析），小隊交叉模擬測驗 | • 題目問「下列何者不是 Web 漏洞掃描工具？」出現 `gflags` 或 `Wireshark` 秒剔除<br>• 10/11 交付 15 道高品質全真模擬題與速查表供小隊對抗驗收 | 詳見下方工具總表與真題手冊 |

---

## 🎯 模組一：Web 應用安全（核心主責，15 大檢核項）

> 💡 **作答核心直覺**：看到 Request Payload 或 Response 特徵，必須在 **5 秒內** 辨識出漏洞類型、影響成因與防護標頭。

| # | 核心考點與檢核項目 | 初賽高頻題眼 / 陷阱辨識 | 本地對應 Playbook 教學文檔 |
| :-: | :--- | :--- | :--- |
| **1** | **OWASP Top 10:2025** | • **2025 新增重點**：A03 Software Supply Chain Failures（供應鏈混淆）、A10 Mishandling of Exceptional Conditions（異常處理不當）<br>• 必須精確區分 2021 與 2025 的排名變化 | [`04.1_supply_chain_dependency_confusion.md`](web/04.1_supply_chain_dependency_confusion.md) |
| **2** | **SQL Injection 四大類型與延遲函數** | • **類型**：Error-based (`updatexml`, `extractvalue`)、Union-based (欄位數與型態對齊)、Boolean-blind (`length()`, `ascii()`, `substr()`)、Time-based<br>• **DB 延遲函數差異**：MySQL (`sleep(5)`)、MSSQL (`WAITFOR DELAY '0:0:5'`)、PostgreSQL (`pg_sleep(5)`)、Oracle (`dbms_pipe.receive_message`) | [`R10.1_sql_query_injection.md`](web/R10.1_sql_query_injection.md) |
| **3** | **寬字節注入 (Wide-Byte)** | • 發生在 GBK 等雙位元組編碼情境，利用 `%df` 與後端轉義斜線 `\` (`%5c`) 吃掉組合成中文字（`%df%5c` ➔ 運算為漢字 `運`），使單引號 `'` (`%27`) 逃逸 | [`R10.1_sql_query_injection.md`](web/R10.1_sql_query_injection.md) |
| **4** | **XSS 三大類型與 CSP 防護** | • **Reflected**（URL 參數即時反射）、**Stored**（入庫持久化）、**DOM-based**（前端 JS `sink` 如 `innerHTML`、`document.write`、`eval`）<br>• **CSP nonce**：`<script nonce="rAnd0m">` 必須一次性且不可預測，若無 `strict-dynamic` 且有 script gadget 則可被繞過 | [`R14.1_reflected_cross_site_scripting.md`](web/R14.1_reflected_cross_site_scripting.md)<br>[`R14.2_stored_cross_site_scripting.md`](web/R14.2_stored_cross_site_scripting.md)<br>[`R14.3_dom_based_cross_site_scripting.md`](web/R14.3_dom_based_cross_site_scripting.md) |
| **5** | **CSRF 與 Cookie 屬性** | • **SameSite 屬性**：`Strict`（完全禁止跨站攜帶）、`Lax`（預設，僅頂層導航 GET 攜帶）、`None`（必須搭配 `Secure`）<br>• **保護旗標**：`HttpOnly`（阻斷 JS `document.cookie` 讀取，防 XSS 偷 Token，但**無法**防 CSRF）、`Secure`（僅限 HTTPS 傳輸） | [`R14.4_cross_site_request_forgery.md`](web/R14.4_cross_site_request_forgery.md) |
| **6** | **CORS 設定錯誤** | • 誤配 `Access-Control-Allow-Origin: *` 時不可帶憑證；但若後端反射請求的 `Origin` 且宣告 `Access-Control-Allow-Credentials: true`，則導致跨站竊取機敏回應 | [`R14.5_cross_origin_resource_sharing_trust_abuse.md`](web/R14.5_cross_origin_resource_sharing_trust_abuse.md) |
| **7** | **SSRF 與雲端元數據濫用** | • **常用偽協定**：`gopher://`（可偽造任意 TCP 流量如 Redis/FastCGI）、`dict://`、`file://`<br>• **雲端 IMDS**：AWS/GCP `169.254.169.254`（IMDSv1 vs IMDSv2 Token 要求）<br>• **DNS Rebinding**：利用 TTL=0，第一次解析為外部 IP 繞過檢核，第二次解析為 `127.0.0.1` 達成攻擊 | [`R11.1_server_side_request_forgery.md`](web/R11.1_server_side_request_forgery.md)<br>[`05.4_s3_bucket_leak_imds_ssrf_defense.md`](web/05.4_s3_bucket_leak_imds_ssrf_defense.md) |
| **8** | **SSTI 模組注入** | • 各模板語法辨識：Jinja2 / Twig `{{7*'7'}}`（輸出 `7777777` 表 Jinja2，輸出 `49` 表 Twig）；Python 透過 `__mro__`、`__subclasses__()` 遍歷呼叫 `os.system` | [`R10.3_server_side_template_injection.md`](web/R10.3_server_side_template_injection.md) |
| **9** | **LFI / 檔案上傳 / 伺服器解析特性** | • **PHP 偽協定**：`php://filter/read=convert.base64-encode/resource=index.php` 讀源碼、`data://text/plain;base64,...`、`php://input`<br>• **伺服器解析漏洞**：Apache 換行解析 / 多副檔名（從右至左解析如 `shell.php.jpeg`）、Nginx `alias` 目錄穿越（缺少結尾 `/`） | [`R11.2_file_path_traversal.md`](web/R11.2_file_path_traversal.md)<br>[`R11.3_local_file_inclusion.md`](web/R11.3_local_file_inclusion.md)<br>[`R11.4_remote_file_inclusion.md`](web/R11.4_remote_file_inclusion.md) |
| **10** | **OS 命令注入空格繞過** | • 常用空格替換字元：`${IFS}`、`$IFS$9`、`<`、`<>`、`%09`（Tab）、`{cat,flag}`、`$'\x20'` | [`R10.2_os_command_shell_injection.md`](web/R10.2_os_command_shell_injection.md) |
| **11** | **JWT 安全攻擊** | • **弱點一**：簽名演算法被置換為 `alg: "none"`<br>• **弱點二**：演算法混淆（RS256 公私鑰驗證被改成 HS256，利用公開金鑰字串當作對稱金鑰簽名）<br>• **弱點三**：弱密鑰爆破（John / Hashcat） | [`R09.1_application_session_state_forgery_validation_bypass.md`](web/R09.1_application_session_state_forgery_validation_bypass.md) |
| **12** | **反序列化漏洞觸發點** | • **PHP**：魔術方法 `__destruct`、`__wakeup`、`__toString`、phar 偽協定反序列化<br>• **Python**：`pickle` 的 `__reduce__` 魔術方法<br>• **Java**：`readObject()`、Log4Shell（`${jndi:ldap://...}` JNDI 注入）、ysoserial CC 鏈 | [`R12.1_unsafe_deserialization_object_injection.md`](web/R12.1_unsafe_deserialization_object_injection.md)<br>[`20.1_java_memshell_filter_servlet_forensics.md`](web/20.1_java_memshell_filter_servlet_forensics.md) |
| **13** | **XXE (XML External Entity)** | • 外部實體宣告語法：`<!ENTITY xxe SYSTEM "file:///etc/passwd">` 或 `SYSTEM "http://..."`（可演變為 SSRF 或 OOB 外帶資料）<br>• 防禦核心：`disallow-doctype-decl`，禁用 DTD 外部實體解析 | [`R12.2_xml_external_entity_processing_abuse.md`](web/R12.2_xml_external_entity_processing_abuse.md) |
| **14** | **HTTP 狀態碼與安全標頭** | • **狀態碼區分**：`401 Unauthorized`（未認證，需提供有效憑證，通常帶 `WWW-Authenticate`）vs `403 Forbidden`（已認證但無權存取）<br>• **安全標頭**：`HSTS` (`Strict-Transport-Security`)、`X-Frame-Options` (DENY / SAMEORIGIN 防點擊劫持)、`X-Content-Type-Options: nosniff` | [`R13.1_http_request_smuggling_desynchronization.md`](web/R13.1_http_request_smuggling_desynchronization.md)<br>[`16.4_http_request_smuggling_defense.md`](web/16.4_http_request_smuggling_defense.md) |
| **15** | **電子郵件安全機制** | • **SPF**：DNS TXT 記錄（`v=spf1 ip4:1.2.3.4 -all`，`~all` 為軟失敗，`-all` 為硬失敗）<br>• **DKIM**：非對稱公私鑰數位簽章，DNS 存放公鑰<br>• **DMARC**：整合 SPF 與 DKIM，宣告驗證失敗後的處置原則（`p=none`、`p=quarantine`、`p=reject`） | （見下方通識精華） |

---

## 📱 模組二：Android / Java 逆向工程（主責領域，4 大檢核項）

> 💡 **初賽考核重點**：考題偏向「觀念理解、工具對應、結構分析」，不需現場編寫逆向腳本，但必須能一眼認出檔案副檔名、工具角色與 smali 代碼語意。

| # | 核心考點 | 必背技術細節與考點特徵 | 本地對應 Playbook 教學文檔 |
| :-: | :--- | :--- | :--- |
| **1** | **APK 解剖結構** | • **`AndroidManifest.xml`**：全域配置（四大元件宣告、權限宣告、exported 屬性、debuggable 旗標）<br>• **`classes.dex`**：Dalvik Executable 位元組碼（可有多個如 classes2.dex）<br>• **`resources.arsc`**：預編譯二進位資源索引表<br>• **`lib/`**：各架構 Native 原生動態程式庫（`armeabi-v7a`、`arm64-v8a`、`x86` 之 `.so` 檔案）<br>• **`META-INF/`**：簽章資料（`CERT.RSA`、`CERT.SF`、`MANIFEST.MF`） | [`26.1_android_apk_malware_static_decompilation.md`](android/26.1_android_apk_malware_static_decompilation.md) |
| **2** | **Smali 語法與 DEX / .so 區別** | • **Smali 基本暫存器**：`v` 區域暫存器、`p` 參數暫存器（非靜態方法的 `p0` 為 `this`）<br>• **常見指令語法**：`const/4 v0, 0x1`、`invoke-virtual`、`invoke-static`、`move-result`、`if-eqz`、`return-void`<br>• **型態符號**：`Z`(boolean), `I`(int), `J`(long), `V`(void), `Ljava/lang/String;`(物件參考), `[I`(int 陣列) | [`26.1_android_apk_malware_static_decompilation.md`](android/26.1_android_apk_malware_static_decompilation.md) |
| **3** | **四大核心工具職責** | • **`jadx / jadx-gui`**：DEX 反編譯為高階 Java 原始碼，靜態程式碼審查主力<br>• **`apktool`**：解包 APK 資源並反組譯為 smali 組合語言（`apktool d app.apk`），修改後可重新打包（`apktool b`）<br>• **`Frida`**：動態程式碼插樁（Dynamic Instrumentation Hooking），在執行時期攔截函式、修改參數與返回值、繞過 SSL Pinning<br>• **`xposed`**：系統層級 Hook 框架 | [`26.1_android_apk_malware_static_decompilation.md`](android/26.1_android_apk_malware_static_decompilation.md)<br>[`26.2_android_runtime_logs_sqlite_forensics.md`](android/26.2_android_runtime_logs_sqlite_forensics.md) |
| **4** | **Java 反編譯與混淆防護** | • **ProGuard / R8**：程式碼壓縮、優化與混淆（將類別與變數名置換為 `a`, `b`, `c` 等無意義符號，破壞可讀性）<br>• **字串加密與加殼**：原生加殼（Native Packer 在 `.so` 載入時動態解密 DEX）、反除錯與 Root 偵測機制 | [`26.1_android_apk_malware_static_decompilation.md`](android/26.1_android_apk_malware_static_decompilation.md) |

---

## 🌐 模組三：Misc 與網路通識（隊員 A 分攤 1/3 領域）

> 💡 **舊學科題目特徵**：每年必出幾題「送分或秒殺題」，重點在數字換算、Port 號直覺、雲端邊界劃分。

### 1. Linux 權限模型與常用指令
- **數值換算**：`r=4`, `w=2`, `x=1`。例：`chmod 755` ➔ 擁有者 `rwx (7)`、群組 `r-x (5)`、其他人 `r-x (5)`。
- **特殊權限位（最高位）**：
  - **SUID (`4000`, 如 `rwsr-xr-x`)**：執行時具有檔案**擁有者**（通常為 root）的權限。考點：尋找 SUID 程式 `find / -perm -u=s -type f 2>/dev/null`，利用 [GTFOBins](https://gtfobins.github.io) 提權。
  - **SGID (`2000`, 如 `rwxr-sr-x`)**：執行時具有該**群組**的權限；若設於目錄上，新建檔案將自動繼承該目錄的群組。
  - **Sticky Bit (`1000`, 如 `rwxrwxrwt`)**：僅檔案擁有者或 root 能刪除其內的檔案（典型案例：`/tmp`）。
- **對應教學文檔**：[`R18.1_linux_suid_sgid_binary_abuse.md`](misc_cloud/R18.1_linux_suid_sgid_binary_abuse.md)

### 2. 核心通訊埠號（Common Ports 必背速查）
- `21`: **FTP**（控制連線，明文；20 為資料連線）
- `22`: **SSH** / SFTP（加密安全連線）
- `23`: **Telnet**（明文遠端終端機）
- `25`: **SMTP**（郵件發送傳遞）
- `53`: **DNS**（網域名稱解析，預設 UDP，區域傳輸 AXFR 時使用 TCP）
- `80`: **HTTP** / `443`: **HTTPS**
- `110`: **POP3** / `143`: **IMAP**（郵件接收）
- `161`: **SNMP**（網路管理協定，UDP）
- `389`: **LDAP** / `636`: **LDAPS**（目錄服務協定）
- `445`: **SMB** / Microsoft-DS（檔案共享，EternalBlue MS17-010 標靶）
- `3306`: **MySQL** / `1433`: **MSSQL** / `5432`: **PostgreSQL**
- `3389`: **RDP**（Windows 遠端桌面連線）

### 3. 雲端計算服務與共同責任模型 (Shared Responsibility)
- **IaaS (Infrastructure as a Service，如 AWS EC2, GCP GCE)**：
  - 雲端廠商負責：實體機房、硬體伺服器、虛擬化 Hypervisor、實體網路與供電。
  - **客戶負責**：作業系統 (OS) 更新與修補、防火牆安全群組 (Security Groups)、應用程式、使用者存取控管 (IAM)、資料加密。
- **PaaS (Platform as a Service，如 Google App Engine, AWS Elastic Beanstalk)**：
  - 雲端廠商負責：硬體、OS 維護、執行環境 runtime、資料庫引擎更新。
  - **客戶負責**：應用程式原始碼、應用設定與資料權限。
- **SaaS (Software as a Service，如 Microsoft 365, Google Workspace)**：
  - 雲端廠商負責：全部基礎設施、平台與軟體運作、高可用性。
  - **客戶負責**：帳號認證（MFA）、存取權限配置與使用者資料管理。
- **對應教學文檔**：[`05.1_cloud_shared_responsibility_matrix.md`](misc_cloud/05.1_cloud_shared_responsibility_matrix.md)

### 4. Misc 檔案隱寫與分析考點
- **ZIP 檔案偽加密**：修改壓縮源檔案目錄區的通用位元標記（將全域方式位標記第 1 位元組由 `00` 改為 `09` 或奇數即觸發密碼提示），使用十六進位編輯器改回 `00` 即可直接解鎖。
- **PNG 結構**：以 `89 50 4E 47 0D 0A 1A 0A` 開頭，第一個 Chunk 必為 `IHDR`（包含寬度 4 bytes、高度 4 bytes 與 CRC32 校驗）。常考**竄改圖片高度**隱藏下方 flag，解法為透過 CRC32 逆推正確高度並修正 hex。
- **隱寫工具辨別**：`binwalk`（分離檔案雕刻）、`steghide`（音訊/JPEG 密碼嵌入提取）、`zsteg`（PNG/BMP 的 LSB 隱寫）、`exiftool`（檢視中繼資料）。

---

## 🧰 隊員 A 必考工具辨識表（全隊混淆題防陷阱）

> ⚠️ **考題陷阱**：題目常給出四個工具名稱，問「下列何者不是 Web 漏洞掃描工具？」或「下列何者用於 Android 反編譯？」

| 工具名稱 | 主要功能分類 | 官方核心用途 | 考題常見混淆選項與陷阱備註 |
| :--- | :--- | :--- | :--- |
| **Burp Suite** | Web 滲透測試 | HTTP 封包攔截、重送（Repeater）、暴力測試（Intruder） | Web 必考神器 |
| **sqlmap** | Web 自動化攻擊 | 自動化偵測與利用 SQL 注入漏洞、提取資料庫資料 | 專攻 SQLi |
| **dirb / gobuster / dirsearch** | Web 目錄掃描 | 透過字典爆破網站隱藏路徑與目錄 | 常與除錯工具混雜出題 |
| **ffuf** | Web Fuzzing | 高性能快速目錄/參數/模糊測試工具 | 速度快，以 Go 開發 |
| **jadx / jadx-gui** | Android 逆向 | 將 Android DEX/APK 直接反編譯為 Java 原始碼 | 辨識其反編譯出的副檔名是 `.java` |
| **apktool** | Android 逆向 | 解包資源並反組譯為 Smali 組合代碼 | 辨識其輸出目錄包含 `smali/` |
| **Frida** | 動態 Hook 框架 | 基於 Python/JS 腳本動態插樁注入程式記憶體 | 攔截函式、繞過 Pinning 首選 |
| **gflags** | **Windows 系統除錯** | 設定全域或程序旗標（**不是**掃描工具！） | ⚠️ **2024 真題誘答陷阱選項** |
| **Hollow Hunter** | 惡意程式鑑識 | 偵測 Process Hollowing 程序掏空代碼注入 | 2024 真題出現 |
| **1768.py** | 記憶體鑑識 | 解析記憶體中的 Cobalt Strike Beacon 配置檔 | 2024 真題出現 |
| **CyberChef** | 萬用解碼分析 | GCHQ 開源之拖拉式多層編碼、雜湊、加解密處理平台 | CTF 與 Misc 必備 |
| **binwalk** | 檔案分析 | 根據二進位特徵碼辨識並提取嵌入的檔案 | 常用於韌體與多層打包 |

---

## 📚 本地專屬教材庫檔案索引（直達路徑）

本目錄已將所有隊員 A 衝刺所需的實戰 Playbook 歸整如下，可直接點擊閱讀：

### 📁 Web 應用教學文檔 (`./web/`)
1. [`R10.1_sql_query_injection.md`](web/R10.1_sql_query_injection.md) - SQL 注入四大類型、MySQL/MSSQL/PG 函數與寬字節
2. [`R10.2_os_command_shell_injection.md`](web/R10.2_os_command_shell_injection.md) - OS 指令注入與空白 `${IFS}` 繞過
3. [`R10.3_server_side_template_injection.md`](web/R10.3_server_side_template_injection.md) - Jinja2 / Twig 模板注入與沙盒逃逸
4. [`R11.1_server_side_request_forgery.md`](web/R11.1_server_side_request_forgery.md) - SSRF 原理、偽協定與 DNS Rebinding
5. [`R11.2_file_path_traversal.md`](web/R11.2_file_path_traversal.md) - 路徑穿越與目錄結構欺騙
6. [`R11.3_local_file_inclusion.md`](web/R11.3_local_file_inclusion.md) - 本地檔案包含 (LFI) 與 PHP 偽協定利用
7. [`R11.4_remote_file_inclusion.md`](web/R11.4_remote_file_inclusion.md) - 遠端檔案包含 (RFI) 條件與防禦
8. [`R12.1_unsafe_deserialization_object_injection.md`](web/R12.1_unsafe_deserialization_object_injection.md) - PHP 魔術方法與反序列化鏈
9. [`R12.2_xml_external_entity_processing_abuse.md`](web/R12.2_xml_external_entity_processing_abuse.md) - XXE 實體宣告與 OOB 外帶
10. [`R12.3_mass_assignment_unsafe_object_binding.md`](web/R12.3_mass_assignment_unsafe_object_binding.md) - 批量賦值與物件綁定漏洞
11. [`R13.1_http_request_smuggling_desynchronization.md`](web/R13.1_http_request_smuggling_desynchronization.md) - HTTP 請求走私 CL.TE / TE.CL
12. [`R13.2_web_cache_poisoning_cache_key_normalization_confusion.md`](web/R13.2_web_cache_poisoning_cache_key_normalization_confusion.md) - Web 快取投毒原理
13. [`R13.3_host_forwarded_header_routing_origin_selection_trust_abuse.md`](web/R13.3_host_forwarded_header_routing_origin_selection_trust_abuse.md) - 路由標頭偽造與信任濫用
14. [`R14.1_reflected_cross_site_scripting.md`](web/R14.1_reflected_cross_site_scripting.md) - 反射型 XSS 攻擊
15. [`R14.2_stored_cross_site_scripting.md`](web/R14.2_stored_cross_site_scripting.md) - 儲存型 XSS 攻擊
16. [`R14.3_dom_based_cross_site_scripting.md`](web/R14.3_dom_based_cross_site_scripting.md) - DOM 型 XSS Source 與 Sink 拆解
17. [`R14.4_cross_site_request_forgery.md`](web/R14.4_cross_site_request_forgery.md) - CSRF 與 SameSite / Token 防護
18. [`R14.5_cross_origin_resource_sharing_trust_abuse.md`](web/R14.5_cross_origin_resource_sharing_trust_abuse.md) - CORS 設定錯誤與憑證竊取
19. [`R15.1_workflow_state_transition_bypass.md`](web/R15.1_workflow_state_transition_bypass.md) - 業務邏輯與狀態流轉繞過
20. [`R15.2_business_action_replay_idempotency_abuse.md`](web/R15.2_business_action_replay_idempotency_abuse.md) - 重放與冪等性破壞
21. [`R15.3_application_race_condition_concurrency_abuse.md`](web/R15.3_application_race_condition_concurrency_abuse.md) - 競爭條件 (Race Condition) 與條件競爭
22. [`R09.1_application_session_state_forgery_validation_bypass.md`](web/R09.1_application_session_state_forgery_validation_bypass.md) - JWT 偽造與 Session 機制防禦
23. [`04.1_supply_chain_dependency_confusion.md`](web/04.1_supply_chain_dependency_confusion.md) - 軟體供應鏈安全（OWASP 2025 新主題）
24. [`05.4_s3_bucket_leak_imds_ssrf_defense.md`](web/05.4_s3_bucket_leak_imds_ssrf_defense.md) - IMDS 元數據濫用與 S3 防禦
25. [`16.4_http_request_smuggling_defense.md`](web/16.4_http_request_smuggling_defense.md) - 請求走私藍隊防禦手冊
26. [`20.1_java_memshell_filter_servlet_forensics.md`](web/20.1_java_memshell_filter_servlet_forensics.md) - Java 記憶體馬排查取證

### 📁 Android / Java 逆向教學文檔 (`./android/`)
1. [`26.1_android_apk_malware_static_decompilation.md`](android/26.1_android_apk_malware_static_decompilation.md) - APK 結構拆解、jadx/apktool、Smali 語法、ProGuard 混淆
2. [`26.2_android_runtime_logs_sqlite_forensics.md`](android/26.2_android_runtime_logs_sqlite_forensics.md) - Frida 動態注入、Runtime 日誌、SQLite 鑑識

### 📁 Misc 與雲端責任模型教學文檔 (`./misc_cloud/`)
1. [`05.1_cloud_shared_responsibility_matrix.md`](misc_cloud/05.1_cloud_shared_responsibility_matrix.md) - 雲端 IaaS / PaaS / SaaS 共同責任模型劃分全表
2. [`R18.1_linux_suid_sgid_binary_abuse.md`](misc_cloud/R18.1_linux_suid_sgid_binary_abuse.md) - Linux SUID/SGID 權限設定與提權防護

### 📁 速查表、模擬卷與考前整理
- [`CHEATSHEET_1PAGE.md`](CHEATSHEET_1PAGE.md) - 一頁紙秒選速查表（特徵 → 秒選對照）
- [`考前整理版.md`](考前整理版.md) - 考前 30 分鐘掃描版 ＋ 脈絡故事版（Web 到 App 滲透之旅）
- [`exams/FINAL_SPRINT_MASTER_60Q.md`](exams/FINAL_SPRINT_MASTER_60Q.md) - 60 題跨單元總衝刺大卷（實戰深度版）
- [`exams/MASTER_60Q_DEEPDIVE_NOTES.md`](exams/MASTER_60Q_DEEPDIVE_NOTES.md) - 大卷 Q1~Q15 逐題深度精講 ＋ 前端信任邊界概念釐清
- [`exams/REMAINING_Q16-Q60_DEEPDIVE.md`](exams/REMAINING_Q16-Q60_DEEPDIVE.md) - 大卷 Q16~Q60 逐題深度解析
- [`exams/unit_1_exam_25q.md`](exams/unit_1_exam_25q.md) - 單元一（Web 注入）25 題檢定卷
- [`exams/final_mock_25q.md`](exams/final_mock_25q.md) - 跨單元 25 題模擬卷
- [`exams/weakpoint_drill_12q.md`](exams/weakpoint_drill_12q.md) - 弱點強化 12 題變化卷
- [`exams/artifact_reading_10q.md`](exams/artifact_reading_10q.md) - 現場證據判讀 10 題（看 payload 反推漏洞）
