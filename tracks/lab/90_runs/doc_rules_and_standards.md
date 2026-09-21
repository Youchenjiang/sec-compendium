# 🛡️ 網路安全資料庫 - 專案整理規範與進度說明檔 (ORGANIZATION_RULES.md)

## 📌 §0 組織與命名最高鐵律 (Iron Rules)

1. **三層金字塔架構分層原則**：
   - **第一層 (Level-1)**：`01`~`09` **頂層技術領域 (Top Domains)**。
   - **第二層 (Level-2)**：從 `01_` 開始連續編號 **技術子域 (Technical Sub-domains)**。
   - **第三層 (Level-3)**：**攻防實戰作業步驟 (Workflow Steps)**。
2. **第三層步驟分類模型 (Workflow Steps Rule)**：
   - 第三層目錄**必須統一按實戰滲透與攻防作業步驟**劃分（避免按載體或雜亂名稱劃分）：
     - `01_語法原理與手動探測` (Recon & Concepts)
     - `02_漏洞利用與Payload構造` (Exploitation & Payloads)
     - `03_自動化工具與腳本` (Tools & Automation)
     - `04_防護繞過與高階利用` (Bypass & Advanced)
3. **命名格式規範**：`[來源縮寫]_[單一具體技術細項]`
   - 範例：`Web攻防實戰_SQL注入基礎`、`ctf_PWN棧溢出漏洞`、`HW_藍隊日誌`、`HackTools_sql`
4. **嚴禁載體/格式詞**：資料夾名稱中**絕對禁止出現**以下無意義載體詞：
   - ❌ `課程影片`、`電子書`、`源碼`、`講義`、`課件`、`工具`、`題庫`、`指南`、`經驗談`、`筆試題`、`表格`、`文件`、`包`、`試題`、`視頻`
5. **來源前綴絕對留存**：
   - 在目錄移動、升層/降層（1->2->3）過程中，原始資料夾名稱與來源前綴（`Web攻防實戰_`、`ctf_`、`HW_`、`Java代碼審計_`、`工具使用_`、`HackTools_`、`Z0FCourse_` 等）**100% 絕對禁止修改或刪除**！

---

## ⚖️ §0.1 6 大分類裁判鐵律 (Refining Rules for Intent & Domain Boundaries)

1. **規則 1：用途/攻擊目標導向，而非工具名稱導向**：
   - 工具前綴不決定分類，攻擊目標決定分類。如 `Metasploit_Web` 歸 `01`；`Metasploit_Android` 歸 `02`；`Metasploit_提權/C2` 歸 `04`；`Burp` 歸 `01`；`Hydra` 歸 `04`。
2. **規則 2：攻擊利用歸攻擊域 (01/04)，防禦加固歸藍隊域 (07)**：
   - 凡目的為取得控制權/漏洞利用 (Attack) ➔ 歸屬 `01` (Web) / `04` (系統內網)；凡目的為降低風險/日誌研判/加固 (Defense) ➔ 歸屬 `07`。
3. **規則 3：事前 vs. 事中 vs. 事後三分法**：
   - Web 黑箱滲透/利用 (事前/事中) ➔ `01`；系統/內網/C2/提權/DDoS發包 (事中) ➔ `04`；藍隊防守/加固 (事中) ➔ `07`；事後流量 PCAP/DFIR 數位取證 (事後) ➔ `06`。
4. **規則 4：通用環境、連線工具、數據庫管理、語言基礎優先歸 09**：
   - VMware、Kali Linux、phpStudy、XAMPP、Docker 環境、.NET/Java Runtime、PuTTY、Xshell、FTP、MySQL數據庫管理工具，一律歸屬 `09_基礎設施與運營環境`。
5. **規則 5：同名系列嚴禁跨域 ambiguity，必須在名稱中明確技術邊界**：
   - 同名系列若內容不同，必須在名稱中標明技術領域（如 `01/試聽課福利_Web漏洞Fuzz字典` vs `04/試聽課福利_爆破密碼字典`），嚴禁同名跨域混淆。
6. **規則 6：知識主體 (Primary Domain) 唯一原則與 IDS 裁判**：
   - 一份資料只能有一個主要知識領域，即使內容跨領域，也依核心學習目標分類；工具、語言、平台僅作為屬性。
   - **IDS/EDR/SIEM 裁判**：若偏部署配置、規則寫入與告警研判 ➔ 歸 `07`；若偏 PCAP 封包解析與底層協定分析 ➔ 歸 `06`。

---

## 🧭 9 大頂層 MECE 互斥分類收錄標準與邊界紀律

1. **`01_Web安全/`**：
   - **定位**：黑箱滲透測試、前端 Web 逆向 (JS逆向/API)、HTTP/HTTPS 請求層面漏洞利用 (Payload)、Web 滲透前置背景基礎與 **Web 崗位專屬面試考題**。
2. **`02_二進制與逆向/`**：
   - **定位**：二進制漏洞利用 (PWN)、逆向工程 (RE) 與底層彙編/硬體/移動端安全。
3. **`03_密碼學與隱寫/`**：
   - **定位**：純密碼學原理、演算法破譯、檔案頭/結構修復與 MISC 隱寫術。
4. **`04_系統與內網安全/` (紅隊攻擊面 - Red Team Attack)**：
   - **定位**：單機系統安全、提權、社交工程/釣魚、內網橫向、DDoS發包與 C2 控權技術。
5. **`05_代碼審計與安全開發/`**：
   - **定位**：白箱源碼審計 (Code Audit)、漏洞修補與安全開發生命週期 (SDL)。
6. **`06_網路安全與數位取證/` (事後調查與底層流量)**：
   - **定位**：底層網路協定分析、PCAP 流量分析、網路監控、DFIR 事後數位取證與 **網路協定專屬面試**。
7. **`07_藍隊防禦與護網營運/` (藍隊防守面 - Blue Team Defense)**：
   - **定位**：護網 (HW) 專案營運、防守方 (Blue Team) 策略、即時日誌告警研判、系統加固與 **護網藍隊專屬面試**。
8. **`08_通用學習與面試庫/`**：
   - **定位**：CTF 大賽 Writeup、賽制指南、CISP 認證、SRC 申領/提交流程與 **HR/跨領域通用面試題庫**。
9. **`09_基礎設施與運營環境/`**：
   - **定位**：作業系統、虛擬機、容器、伺服器環境、連線管理工具、資料庫管理工具與執行階段。

---

## 📂 專案全體目錄結構進度樹

```text
網路安全/
├── [x] 01_Web安全/
│   ├── [x] 01_網頁前端語言與語法/
│   │   ├── [x] Web攻防實戰_WebApp開發/
│   │   ├── [x] Web攻防實戰_Web前端基礎/
│   │   │   ├── [x] HTML&JavaScript/
│   │   │   └── [x] mysite/
│   │   ├── [x] ctf_JS加密解密賽題/
│   │   ├── [x] 暗月Web紅隊_CSS版面佈局/
│   │   └── [x] 暗月Web紅隊_HTML基礎語法/
│   ├── [x] 02_HTTP網路協定與抓包/
│   │   ├── [x] Web攻防實戰_HTTP協定基礎/
│   │   ├── [x] 教主Kali與Python_HTTPS加密攻擊/
│   │   └── [x] 暗月Web紅隊_HTTP協定詳解/
│   ├── [x] 03_後端語言與數據庫語法/
│   │   ├── [x] HackTools_php/
│   │   ├── [x] Web攻防實戰_JavaWeb安全基礎/
│   │   ├── [x] Web攻防實戰_PHP安全/
│   │   └── [x] ctf_PHP特性賽題/
│   ├── [x] 04_資產測繪與情報收集/
│   │   ├── [x] CTF常見題型解析_資訊洩露/
│   │   ├── [x] Web攻防教程_Shodan/
│   │   ├── [x] ctf_資訊洩露漏洞解題/
│   │   ├── [x] 國外全套滲透_網絡情報/
│   │   ├── [x] 工具使用_網絡情報刺探/
│   │   │   ├── [x] Debug/
│   │   │   ├── [x] Wscan Gui Beta6/
│   │   │   ├── [x] bin/
│   │   │   ├── [x] lib/
│   │   │   ├── [x] payloads/
│   │   │   ├── [x] plugin/
│   │   │   ├── [x] 导出数据/
│   │   │   └── [x] 工具图片/
│   │   ├── [x] 暗月Web紅隊_Web情報收集/
│   │   ├── [x] 暗月Web紅隊_Whois資產刺探/
│   │   ├── [x] 試聽課福利_JSFinder刺探/
│   │   │   └── [x] 御剑后台扫描工具/
│   │   └── [x] 試聽課福利_Layer資產刺探/
│   │   │   └── [x] 子域名挖掘机5.0最新版/
│   ├── [x] 05_Web滲透測試導論與靶場/
│   │   ├── [x] CTF常見題型解析_Web思路/
│   │   ├── [x] CTF題型解析_Python自動化漏洞挖掘腳本/
│   │   ├── [x] HW_Web滲透/
│   │   ├── [x] HackTools_javascript/
│   │   ├── [x] HackTools_web/
│   │   │   ├── [x] client-side/
│   │   │   ├── [x] img/
│   │   │   ├── [x] payload/
│   │   │   └── [x] server-side/
│   │   ├── [x] Metasploit魔鬼訓練營_Web/
│   │   ├── [x] SRC漏洞挖掘_JS逆向/
│   │   ├── [x] Web攻防實戰_Web滲透/
│   │   ├── [x] Web攻防實戰_滲透插件/
│   │   ├── [x] Web攻防實戰_訪問控制/
│   │   ├── [x] Web攻防實戰_認證會話/
│   │   ├── [x] ctf_Web解題基礎入門/
│   │   ├── [x] ctf_Web解題技巧/
│   │   ├── [x] ctf_Web解題賽題/
│   │   ├── [x] 原書籍_Web應用安全/
│   │   ├── [x] 國科CTF_Web/
│   │   ├── [x] 外校_Web配置/
│   │   ├── [x] 密碼破解訓練營_靶場CMS/
│   │   ├── [x] 工具使用_K8飛刀Webshell/
│   │   ├── [x] 工具使用_Webshell大馬小馬/
│   │   │   ├── [x] asp/
│   │   │   ├── [x] aspx/
│   │   │   ├── [x] jsp/
│   │   │   ├── [x] php/
│   │   │   └── [x] 大马/
│   │   ├── [x] 工具使用_WordPress綜合檢測/
│   │   │   └── [x] data/
│   │   ├── [x] 工具使用_YXCMS測試靶場/
│   │   ├── [x] 教主Kali與Python_Python網絡爬蟲/
│   │   ├── [x] 暗月Web紅隊_CTF靶機實戰測試/
│   │   ├── [x] 暗月Web紅隊_JSP注入/
│   │   ├── [x] 暗月Web紅隊_Web應用破解/
│   │   ├── [x] 暗月Web紅隊_位移注入/
│   │   └── [x] 試聽課福利_HackTools瀏覽器擴充套件/
│   ├── [x] 06_SQL注入與命令執行/
│   │   ├── [x] 51CTO奪旗賽_RCE_命令執行/
│   │   ├── [x] 51CTO奪旗賽_RCE_命令注入/
│   │   ├── [x] 51CTO奪旗賽_SQL注入_GETPOST/
│   │   ├── [x] 51CTO奪旗賽_SQL注入_Header頭注入/
│   │   ├── [x] 51CTO奪旗賽_SQL注入_SSL注入/
│   │   ├── [x] CTF常見題型解析_SQL注入/
│   │   ├── [x] CTF題型解析_RCE命令執行/
│   │   ├── [x] CTF題型解析_SQL盲注/
│   │   ├── [x] CTF題型解析_Sqlmap/
│   │   ├── [x] CTF題型解析_XML盲注/
│   │   ├── [x] CTF題型解析_XXE/
│   │   ├── [x] HackTools_sql/
│   │   ├── [x] Web攻防實戰_MySQL數據庫基礎/
│   │   ├── [x] Web攻防實戰_OOB注入/
│   │   │   └── [x] OOB注入靶场/
│   │   ├── [x] Web攻防實戰_SQL注入WAF繞過/
│   │   ├── [x] Web攻防實戰_SQL注入基礎/
│   │   ├── [x] Web攻防實戰_Sqlmap/
│   │   ├── [x] Web攻防教程_RCE命令/
│   │   ├── [x] Web攻防教程_SQL注入漏洞利用/
│   │   ├── [x] Web攻防教程_Sqlmap自動化注入/
│   │   ├── [x] Web攻防教程_XXE/
│   │   ├── [x] ctf_SQL注入漏洞解題/
│   │   ├── [x] 原書籍_SQL注入Sqlmap/
│   │   ├── [x] 國外全套滲透_SQL注入漏洞/
│   │   ├── [x] 國外全套滲透_命令執行/
│   │   ├── [x] 工具使用_Sqlmap注入掃描/
│   │   ├── [x] 教主Kali與Python_SQL注入漏洞利用/
│   │   ├── [x] 暗月Web紅隊_Access注入/
│   │   ├── [x] 暗月Web紅隊_DNSLog無回顯注入/
│   │   ├── [x] 暗月Web紅隊_MySQL數據庫語法基礎/
│   │   ├── [x] 暗月Web紅隊_MySQL注入/
│   │   ├── [x] 暗月Web紅隊_Oracle注入/
│   │   ├── [x] 暗月Web紅隊_RCE代碼執行/
│   │   ├── [x] 暗月Web紅隊_SQLServer注入/
│   │   ├── [x] 暗月Web紅隊_XPath注入漏洞/
│   │   ├── [x] 暗月Web紅隊_命令執行/
│   │   ├── [x] 暗月Web紅隊_數據庫拖庫/
│   │   └── [x] 試聽課福利_Sqlmap/
│   │   │   ├── [x] Bin/
│   │   │   ├── [x] doc/
│   │   │   ├── [x] extra/
│   │   │   ├── [x] lib/
│   │   │   ├── [x] plugins/
│   │   │   ├── [x] procs/
│   │   │   ├── [x] shell/
│   │   │   ├── [x] tamper/
│   │   │   ├── [x] thirdparty/
│   │   │   ├── [x] txt/
│   │   │   ├── [x] udf/
│   │   │   ├── [x] waf/
│   │   │   └── [x] xml/
│   ├── [x] 07_檔案上傳與包含漏洞/
│   │   ├── [x] 51CTO奪旗賽_任意檔案上傳PUT漏洞/
│   │   ├── [x] CTF題型解析_檔案上傳繞過/
│   │   ├── [x] CTF題型解析_檔案包含/
│   │   ├── [x] Web攻防實戰_FileUpload任意檔案上傳/
│   │   ├── [x] Web攻防教程_FileUpload任意檔案上傳/
│   │   ├── [x] 國外全套滲透_FileUpload任意檔案上傳/
│   │   ├── [x] 國外全套滲透_LFI/
│   │   ├── [x] 國科CTF_檔案上傳/
│   │   ├── [x] 暗月Web紅隊_LFI本地檔案包含/
│   │   ├── [x] 暗月Web紅隊_任意檔案上傳/
│   │   └── [x] 暗月Web紅隊_解析漏洞/
│   ├── [x] 08_客戶端與業務邏輯漏洞/
│   │   ├── [x] 51CTO奪旗賽_目錄遍歷/
│   │   ├── [x] 51CTO奪旗賽_路徑遍歷/
│   │   ├── [x] CTF常見題型解析_XSS跨站腳本攻擊/
│   │   ├── [x] CTF題型解析_SSRF服務端請求偽造/
│   │   ├── [x] CTF題型解析_Session/
│   │   ├── [x] Web攻防實戰_SSRF漏洞/
│   │   ├── [x] Web攻防實戰_XSS/
│   │   ├── [x] Web攻防實戰_業務邏輯安全/
│   │   ├── [x] Web攻防教程_CSRF/
│   │   ├── [x] Web攻防教程_SSRF服務端請求偽造/
│   │   ├── [x] Web攻防教程_XSS攻擊/
│   │   ├── [x] Web攻防教程_越權/
│   │   ├── [x] ctf_XSS跨站腳本攻擊解題/
│   │   ├── [x] 原書籍_XSS跨站腳本攻擊/
│   │   ├── [x] 國外全套滲透_CSRF跨站請求偽造/
│   │   ├── [x] 國外全套滲透_XSS跨站腳本攻擊/
│   │   ├── [x] 教主Kali與Python_CSRF跨站請求偽造/
│   │   ├── [x] 教主Kali與Python_XSS跨站腳本攻擊/
│   │   ├── [x] 暗月Web紅隊_CSRF/
│   │   ├── [x] 暗月Web紅隊_Cookie會話漏洞/
│   │   ├── [x] 暗月Web紅隊_JSON劫持漏洞/
│   │   ├── [x] 暗月Web紅隊_SSRF/
│   │   ├── [x] 暗月Web紅隊_XSS跨站腳本挖掘/
│   │   └── [x] 暗月Web紅隊_越權漏洞/
│   ├── [x] 09_反序列化與組件漏洞/
│   │   ├── [x] CTF題型解析_PHP反序列化魔術方法/
│   │   ├── [x] CTF題型解析_SSTI模板注入(Flask)/
│   │   ├── [x] Web攻防實戰_PHP反序列化/
│   │   ├── [x] 暗月Web紅隊_PHP反序列化漏洞/
│   │   ├── [x] 試聽課福利_Java反序列化/
│   │   └── [x] 試聽課福利_PHPGGC/
│   │   │   ├── [x] gadgetchains/
│   │   │   ├── [x] lib/
│   │   │   └── [x] templates/
│   ├── [x] 10_中間件與框架安全/
│   │   ├── [x] Web攻防實戰_Apache伺服器安全/
│   │   ├── [x] Web攻防實戰_Nginx伺服器安全/
│   │   ├── [x] Web攻防實戰_Spring框架安全/
│   │   ├── [x] Web攻防實戰_Tomcat伺服器安全/
│   │   ├── [x] 試聽課福利_Shiro漏洞利用Exp/
│   │   │   └── [x] config/
│   │   └── [x] 試聽課福利_ThinkPHP漏洞利用Exp/
│   ├── [x] 11_Web漏洞自動化掃描/
│   │   ├── [x] CTF常見題型解析_BurpSuite/
│   │   ├── [x] HackTools_burpsuite/
│   │   │   └── [x] img/
│   │   ├── [x] SRC漏洞挖掘_Fuzzing爆破技巧/
│   │   ├── [x] ctf_BurpSuite/
│   │   ├── [x] ctf_PWN二進制專題_Fuzzing分析/
│   │   ├── [x] ctf_Web漏洞掃描/
│   │   ├── [x] 密碼破解訓練營_BurpSuite/
│   │   ├── [x] 工具使用_AWVS漏洞掃描/
│   │   │   ├── [x] awvs14/
│   │   │   ├── [x] images/
│   │   │   ├── [x] 文档/
│   │   │   └── [x] 资料/
│   │   ├── [x] 工具使用_BurpSuite代理/
│   │   ├── [x] 工具使用_JSky漏洞掃描/
│   │   ├── [x] 工具使用_M7lrvCMS網站掃描/
│   │   │   ├── [x] Config/
│   │   │   ├── [x] Dictionary/
│   │   │   ├── [x] Engine/
│   │   │   ├── [x] Filter/
│   │   │   └── [x] ScanLog/
│   │   ├── [x] 工具使用_Pker極速後台掃描/
│   │   ├── [x] 工具使用_北極熊掃描/
│   │   ├── [x] 工具使用_天蠍座掃描/
│   │   ├── [x] 工具使用_網站掃描輔助元件/
│   │   ├── [x] 工具使用_超強網站掃描/
│   │   ├── [x] 教主Kali與Python_AppScan漏洞掃描/
│   │   ├── [x] 教主Kali與Python_BurpSuite滲透/
│   │   ├── [x] 暗月Web紅隊_Fiddler抓包/
│   │   ├── [x] 暗月Web紅隊_Python滲透Exp腳本編寫/
│   │   ├── [x] 暗月Web紅隊_W13scan漏洞掃描/
│   │   ├── [x] 暗月Web紅隊_Xray漏洞掃描/
│   │   ├── [x] 試聽課福利_AWVS/
│   │   ├── [x] 試聽課福利_BurpSuite/
│   │   ├── [x] 試聽課福利_Web漏洞Fuzz字典/
│   │   │   ├── [x] XXEDicts/
│   │   │   ├── [x] easyXssPayload/
│   │   │   ├── [x] fileuploadblacklist/
│   │   │   ├── [x] sqlDict/
│   │   │   └── [x] ssrfDicts/
│   │   ├── [x] 試聽課福利_Web漏洞掃描/
│   │   └── [x] 試聽課福利_Xray漏洞掃描/
│   ├── [x] 12_Webshell管理與權限維持/
│   │   ├── [x] 工具使用_CknifeWebshell/
│   │   │   └── [x] Customize/
│   │   ├── [x] 工具使用_Webshell一句話木馬/
│   │   ├── [x] 工具使用_中國菜刀Webshell管理/
│   │   │   ├── [x] CCC/
│   │   │   └── [x] Customize/
│   │   ├── [x] 工具使用_中國蟻劍Webshell管理/
│   │   │   ├── [x] database/
│   │   │   ├── [x] locales/
│   │   │   └── [x] resources/
│   │   ├── [x] 教主Kali與Python_WebShell木馬/
│   │   ├── [x] 暗月Web紅隊_主流CMS後台拿Webshell/
│   │   └── [x] 試聽課福利_Webshell木馬/
│   │   │   ├── [x] Customize/
│   │   │   ├── [x] GodzillaCache/
│   │   │   ├── [x] Script/
│   │   │   ├── [x] antData/
│   │   │   ├── [x] locales/
│   │   │   ├── [x] modules/
│   │   │   ├── [x] node_modules/
│   │   │   ├── [x] resources/
│   │   │   ├── [x] server/
│   │   │   ├── [x] source/
│   │   │   ├── [x] static/
│   │   │   ├── [x] swiftshader/
│   │   │   └── [x] views/
│   └── [x] 13_Web安全筆試與面試考題/
├── [x] 02_二進制與逆向/
│   ├── [x] 01_彙編語言與二進制基礎/
│   │   └── [x] Z0FCourse_Assembly彙編語言/
│   │   │   ├── [x] Chapter3_AssemblyPDF/
│   │   │   └── [x] assets/
│   ├── [x] 02_PWN記憶體破壞漏洞利用/
│   │   ├── [x] HackTools_pwn/
│   │   │   ├── [x] img/
│   │   │   └── [x] payload/
│   │   ├── [x] ctf_PWN/
│   │   ├── [x] ctf_PWNExploit編寫教程/
│   │   ├── [x] ctf_PWNIoT韌體安全/
│   │   ├── [x] ctf_PWNWindows漏洞/
│   │   ├── [x] ctf_PWN_IOFILE漏洞/
│   │   ├── [x] ctf_PWN_Linux/
│   │   ├── [x] ctf_PWN二進制專題_逆向工程RE/
│   │   ├── [x] ctf_PWN使用者態與ROP利用/
│   │   ├── [x] ctf_PWN內核漏洞/
│   │   ├── [x] ctf_PWN堆溢出漏洞/
│   │   ├── [x] ctf_PWN教材/
│   │   ├── [x] ctf_PWN格式化字串漏洞/
│   │   ├── [x] ctf_PWN棧溢出漏洞/
│   │   ├── [x] ctf_PWN解題基礎入門/
│   │   ├── [x] ctf_PWN零日漏洞與WebAssembly/
│   │   └── [x] ctf_PWN高級利用/
│   ├── [x] 03_靜態反彙編與動態逆向/
│   │   ├── [x] Z0FCourse_逆向工程全套講義/
│   │   │   ├── [x] Chapter 1 - Introduction/
│   │   │   ├── [x] Chapter 2 - BinaryBasics/
│   │   │   ├── [x] Chapter 3 - Assembly/
│   │   │   ├── [x] Chapter 4 - Tools/
│   │   │   ├── [x] Chapter 5 - BasicReversing/
│   │   │   ├── [x] Chapter 6 - DLL/
│   │   │   ├── [x] Chapter 7 - Windows/
│   │   │   ├── [x] Chapter 8 - Generic Table/
│   │   │   └── [x] FilesNeeded/
│   │   ├── [x] ctf_360勸退賽題_逆向工程/
│   │   │   ├── [x] Hello, CTF/
│   │   │   ├── [x] game/
│   │   │   ├── [x] jit-in-my-pants-3/
│   │   │   ├── [x] serial-150/
│   │   │   ├── [x] tt3441810/
│   │   │   └── [x] whats-the-hell-500/
│   │   ├── [x] ctf_Crackme賽題/
│   │   ├── [x] ctf_逆向工程/
│   │   ├── [x] ctf_逆向工程賽題/
│   │   │   └── [x] 逆向_4/
│   │   └── [x] 原書籍_逆向/
│   ├── [x] 04_移動與物聯網/
│   │   ├── [x] Metasploit魔鬼訓練營_Android/
│   │   ├── [x] ctf_360勸退賽題_移動端/
│   │   │   ├── [x] 1000Click/
│   │   │   ├── [x] Ransonware/
│   │   │   ├── [x] TryGetFlag/
│   │   │   ├── [x] Where/
│   │   │   ├── [x] libdroid-150/
│   │   │   └── [x] you-cant-see-me-150/
│   │   ├── [x] ctf_IoT智慧設備與路由器漏洞利用/
│   │   └── [x] 原書籍_Android移動端安全/
│   └── [x] 05_二進制分析工具/
│   │   ├── [x] HackTools_c/
│   │   ├── [x] HackTools_crypto/
│   │   ├── [x] HackTools_pwn_tools/
│   │   │   └── [x] gdb/
│   │   ├── [x] Z0FCourse_逆向分析工具/
│   │   │   ├── [x] Chapter4_ToolsPDF/
│   │   │   └── [x] assets/
│   │   ├── [x] 工具使用_C32Asm調試/
│   │   └── [x] 工具使用_DTDebug調試/
├── [x] 03_密碼學與隱寫/
│   ├── [x] 01_密碼學與演算法/
│   │   ├── [x] CTF常見題型解析_密碼學入門/
│   │   ├── [x] Web攻防實戰_加密演算法/
│   │   ├── [x] ctf_360勸退賽題_密碼學/
│   │   │   ├── [x] Meitantei-Konan/
│   │   │   ├── [x] crackme_c/
│   │   │   ├── [x] easychallenge/
│   │   │   ├── [x] flag_in_your_hand/
│   │   │   ├── [x] minesweeper-350/
│   │   │   ├── [x] safer-than-rot13/
│   │   │   ├── [x] x_xor_md5/
│   │   │   ├── [x] 告诉你个秘密/
│   │   │   ├── [x] 幂数加密/
│   │   │   ├── [x] 混合编码/
│   │   │   └── [x] 简单的rsa/
│   │   ├── [x] ctf_AES密碼學動畫演示/
│   │   ├── [x] ctf_密碼學加解密賽題/
│   │   │   └── [x] 加解密_6/
│   │   ├── [x] ctf_密碼學解題技巧/
│   │   ├── [x] ctf_競賽通用_密碼學RSA分析/
│   │   └── [x] 國科CTF_密碼學/
│   ├── [x] 02_雜項隱寫術/
│   │   ├── [x] CTF常見題型解析_MISC基礎/
│   │   ├── [x] ctf_360勸退賽題_MISC/
│   │   │   ├── [x] Pretty_Cat/
│   │   │   ├── [x] Zippy/
│   │   │   ├── [x] 再见李华/
│   │   │   └── [x] 就在其中/
│   │   ├── [x] ctf_MISC基礎/
│   │   ├── [x] ctf_MISC隱寫素材/
│   │   │   ├── [x] 3、压缩包/
│   │   │   ├── [x] 4、图片/
│   │   │   ├── [x] 5、音频/
│   │   │   └── [x] 8、Other/
│   │   ├── [x] ctf_MISC隱寫素材_流量包/
│   │   ├── [x] ctf_MISC隱寫術賽題/
│   │   ├── [x] ctf_競賽通用_MISC雜項基礎/
│   │   ├── [x] ctf_隱寫術/
│   │   ├── [x] ctf_隱寫術解題技巧/
│   │   └── [x] 國科CTF_MISC雜項解題/
│   └── [x] 03_加解密工具腳本/
│   │   └── [x] ctf_常用密碼學與隱寫腳本/
│   │   │   ├── [x] 26键盘密码-手机键盘密码/
│   │   │   ├── [x] Base/
│   │   │   ├── [x] CRC32校验爆破/
│   │   │   ├── [x] DES_Python-master/
│   │   │   ├── [x] Nihilist密码/
│   │   │   ├── [x] Python-Brainfuck-master/
│   │   │   ├── [x] RGB转图片/
│   │   │   ├── [x] RSA综合脚本利用/
│   │   │   ├── [x] TTL隐写/
│   │   │   ├── [x] emoji/
│   │   │   ├── [x] hex倒叙/
│   │   │   ├── [x] hex减位/
│   │   │   ├── [x] md5爆破/
│   │   │   ├── [x] python-Picke序列化/
│   │   │   ├── [x] reverse/
│   │   │   ├── [x] rot/
│   │   │   ├── [x] screentogif/
│   │   │   ├── [x] steghide爆破密码/
│   │   │   ├── [x] toy密码/
│   │   │   ├── [x] 一些比赛的脚本/
│   │   │   ├── [x] 二进制每8位倒序/
│   │   │   ├── [x] 十进制转字符/
│   │   │   ├── [x] 去重/
│   │   │   ├── [x] 双参数爆破脚本/
│   │   │   ├── [x] 变异凯撒/
│   │   │   ├── [x] 四方密码/
│   │   │   ├── [x] 图片爆破宽高/
│   │   │   ├── [x] 字符替换表/
│   │   │   ├── [x] 字符频率统计分析/
│   │   │   ├── [x] 字节转二维码/
│   │   │   ├── [x] 常用反解密脚本/
│   │   │   ├── [x] 批量修改文件名后缀/
│   │   │   ├── [x] 批量解压压缩包+带密码/
│   │   │   ├── [x] 数学题/
│   │   │   ├── [x] 文件异或/
│   │   │   ├── [x] 文本转gbk编码/
│   │   │   ├── [x] 曼彻斯特编码/
│   │   │   ├── [x] 替换脚本/
│   │   │   ├── [x] 流量数据提取脚本/
│   │   │   ├── [x] 红绿灯-二进制/
│   │   │   ├── [x] 维吉尼亚加密/
│   │   │   ├── [x] 谍报-替换普通话/
│   │   │   ├── [x] 进制互相转换/
│   │   │   ├── [x] 进制转化字符脚本/
│   │   │   ├── [x] 遍历读取压缩包文件判断1和0/
│   │   │   └── [x] 频域盲水印/
├── [x] 04_系統與內網安全/
│   ├── [x] 01_主機掃描與探測/
│   │   ├── [x] Metasploit魔鬼訓練營_主機刺探/
│   │   ├── [x] 原書籍_Python黑客編程/
│   │   ├── [x] 工具使用_NTscan網絡掃描/
│   │   ├── [x] 教主Kali與Python_Nexpose漏洞掃描/
│   │   └── [x] 試聽課福利_Nessus漏洞掃描/
│   ├── [x] 02_未授權服務與RCE利用/
│   │   ├── [x] 51CTO奪旗賽_FTP服務後門利用/
│   │   ├── [x] 51CTO奪旗賽_SMB服務資訊洩露/
│   │   ├── [x] 51CTO奪旗賽_SSH滲透/
│   │   ├── [x] CTF題型解析_Redis未授權/
│   │   ├── [x] 暗月Web紅隊_Redis主從RCE/
│   │   └── [x] 暗月Web紅隊_Redis未授權/
│   ├── [x] 03_權限提升/
│   │   ├── [x] HackTools_bash/
│   │   ├── [x] HackTools_linux/
│   │   │   └── [x] privesc/
│   │   ├── [x] Metasploit魔鬼訓練營_系統權限提升/
│   │   ├── [x] 工具使用_Linux提權/
│   │   ├── [x] 工具使用_Windows提權/
│   │   ├── [x] 暗月Web紅隊_Linux_SUID提權/
│   │   ├── [x] 暗月Web紅隊_Linux內核提權/
│   │   ├── [x] 暗月Web紅隊_MOF提權/
│   │   ├── [x] 暗月Web紅隊_Windows溢出提權/
│   │   ├── [x] 試聽課福利_Netcat提權/
│   │   └── [x] 試聽課福利_PSTools提權/
│   │   │   ├── [x] wmiexec/
│   │   │   ├── [x] 密码抓取/
│   │   │   └── [x] 开启3389/
│   ├── [x] 04_密碼爆破與字典/
│   │   ├── [x] 51CTO奪旗賽_Web密碼暴力破解/
│   │   ├── [x] Web攻防教程_Web密碼爆破/
│   │   ├── [x] 國外全套滲透_密碼爆破/
│   │   ├── [x] 外校_Hydra密碼爆破/
│   │   ├── [x] 密碼破解訓練營_WIFI密碼/
│   │   ├── [x] 密碼破解訓練營_Web網站帳號密碼暴力破解/
│   │   ├── [x] 密碼破解訓練營_Win密碼/
│   │   ├── [x] 密碼破解訓練營_字典/
│   │   ├── [x] 密碼破解訓練營_破解軟體/
│   │   ├── [x] 工具使用_Hydra密碼爆破/
│   │   ├── [x] 工具使用_密碼字典爆破/
│   │   ├── [x] 暗月Web紅隊_Hydra服務爆破/
│   │   ├── [x] 暗月Web紅隊_後台密碼爆破/
│   │   ├── [x] 試聽課福利_Hydra爆破/
│   │   │   ├── [x] config/
│   │   │   ├── [x] dic/
│   │   │   └── [x] logs/
│   │   ├── [x] 試聽課福利_SNETCracker爆破/
│   │   ├── [x] 試聽課福利_密碼字典/
│   │   └── [x] 試聽課福利_爆破密碼字典/
│   │   │   └── [x] fuzzDicts-master/
│   ├── [x] 05_社交工程與釣魚/
│   │   ├── [x] Metasploit魔鬼訓練營_Office/
│   │   ├── [x] Metasploit魔鬼訓練營_社交工程/
│   │   ├── [x] Metasploit魔鬼訓練營_郵件釣魚/
│   │   ├── [x] 工具使用_社會工程學釣魚/
│   │   ├── [x] 教主Kali與Python_社交工程攻擊/
│   │   ├── [x] 暗月Web紅隊_Office巨集釣魚/
│   │   ├── [x] 暗月Web紅隊_社工庫/
│   │   ├── [x] 暗月Web紅隊_郵件偽造/
│   │   └── [x] 暗月Web紅隊_魚叉郵件/
│   ├── [x] 06_隧道與穿透/
│   │   ├── [x] ctf_遠端連線/
│   │   ├── [x] 暗月Web紅隊_SSH內網穿透/
│   │   ├── [x] 暗月Web紅隊_Socket內網隧道/
│   │   └── [x] 暗月Web紅隊_多層內網隧道穿透/
│   ├── [x] 07_內網橫向與域控/
│   │   ├── [x] HW_內網滲透/
│   │   ├── [x] HW_域控/
│   │   ├── [x] HackTools_windows/
│   │   │   ├── [x] active-directory/
│   │   │   └── [x] privesc/
│   │   ├── [x] Metasploit魔鬼訓練營_HASH憑證/
│   │   └── [x] 暗月Web紅隊_內網橫向滲透/
│   ├── [x] 08_C2與控權/
│   │   ├── [x] HackTools_pentest/
│   │   ├── [x] Metasploit魔鬼訓練營_全套說明/
│   │   │   └── [x] 训练营环境镜像/
│   │   ├── [x] Metasploit魔鬼訓練營_後門/
│   │   ├── [x] Metasploit魔鬼訓練營_木馬加殼/
│   │   │   ├── [x] jiake_UPX/
│   │   │   ├── [x] jiake_aspack/
│   │   │   ├── [x] jiake_qita/
│   │   │   └── [x] pespin132/
│   │   ├── [x] Metasploit魔鬼訓練營_木馬測試/
│   │   ├── [x] 原書籍_Metasploit滲透測試/
│   │   ├── [x] 國外全套滲透_權限維持/
│   │   ├── [x] 工具使用_漏洞利用Exp框架/
│   │   ├── [x] 教主Kali與Python_Linux後門/
│   │   ├── [x] 教主Kali與Python_Metasploit漏洞攻擊/
│   │   ├── [x] 教主Kali與Python_Windows木馬/
│   │   ├── [x] 暗月Web紅隊_CobaltStrike控權/
│   │   ├── [x] 暗月Web紅隊_Empire框架後滲透/
│   │   └── [x] 暗月Web紅隊_紅隊軟體免殺技術/
│   └── [x] 09_局域網欺騙與DDoS攻擊/
│   │   ├── [x] HackTools_man_in_the_middle/
│   │   ├── [x] Web攻防實戰_DDoS拒絕服務攻擊/
│   │   ├── [x] 工具使用_DDoS壓力測試/
│   │   ├── [x] 教主Kali與Python_ARP欺騙攻擊/
│   │   ├── [x] 教主Kali與Python_DNS欺騙攻擊/
│   │   ├── [x] 教主Kali與Python_WPA/
│   │   ├── [x] 教主Kali與Python_局域網MAC/
│   │   └── [x] 試聽課福利_DDoS壓力測試/
├── [x] 05_代碼審計與安全開發/
│   ├── [x] 01_Java審計核心與語法/
│   │   ├── [x] Java代碼審計_HTTP請求/
│   │   ├── [x] Java代碼審計_Java審計/
│   │   ├── [x] Java代碼審計_Mybatis/
│   │   ├── [x] Java代碼審計_第三方框架/
│   │   ├── [x] Java代碼審計入門篇_Java反射/
│   │   │   └── [x] 4.5/
│   │   ├── [x] Java代碼審計入門篇_Java反序列化漏洞/
│   │   │   ├── [x] 5.6.2+5.6.3/
│   │   │   └── [x] 5.6.4/
│   │   ├── [x] Java代碼審計入門篇_RASP/
│   │   ├── [x] Java代碼審計入門篇_Spring/
│   │   │   ├── [x] 6.2.2/
│   │   │   ├── [x] 6.5.2/
│   │   │   ├── [x] 6.8.2/
│   │   │   ├── [x] 6.9.2/
│   │   │   ├── [x] 7.1.1/
│   │   │   ├── [x] 7.1.2/
│   │   │   └── [x] 7.1.3/
│   │   ├── [x] Java代碼審計入門篇_資源/
│   │   ├── [x] Java代碼審計自動站_JSP/
│   │   │   └── [x] Jsp-ServletJDBC/
│   │   └── [x] Java代碼審計自動站_Mybatis框架安全審計/
│   │   │   └── [x] bog-Mybitas/
│   ├── [x] 02_白箱漏洞審計/
│   │   ├── [x] Java代碼審計_CSRF跨站請求偽造/
│   │   ├── [x] Java代碼審計_SQL注入JDBC/
│   │   ├── [x] Java代碼審計_XSS跨站腳本攻擊/
│   │   ├── [x] Java代碼審計_任意檔案上傳/
│   │   ├── [x] Java代碼審計入門篇_RCE命令執行漏洞/
│   │   │   ├── [x] 5.5.2/
│   │   │   └── [x] 5.5.3/
│   │   ├── [x] Java代碼審計入門篇_SQL注入漏洞利用/
│   │   │   ├── [x] 5.1.2/
│   │   │   ├── [x] 5.1.3+5.1.4+5.1.5/
│   │   │   └── [x] 5.1.6/
│   │   ├── [x] Java代碼審計入門篇_SSRF/
│   │   │   ├── [x] 5.3.2/
│   │   │   └── [x] 5.4/
│   │   ├── [x] Java代碼審計入門篇_XSS跨站腳本攻擊/
│   │   │   └── [x] 5.2.2/
│   │   ├── [x] Java代碼審計入門篇_XXE/
│   │   │   ├── [x] 5.7.2/
│   │   │   ├── [x] 5.7.3/
│   │   │   └── [x] 5.7.4/
│   │   ├── [x] Java代碼審計入門篇_檔案上傳/
│   │   │   ├── [x] 5.10.2/
│   │   │   ├── [x] 5.8/
│   │   │   └── [x] 5.9.3/
│   │   └── [x] Java代碼審計自動站_檔案上傳/
│   │   │   └── [x] FileUploadAndDownLoad/
│   ├── [x] 03_審計項目實戰/
│   │   ├── [x] Java代碼審計_daimashenjiyuanma代碼審計源碼/
│   │   │   ├── [x] WebRoot/
│   │   │   └── [x] src/
│   │   └── [x] Jspxcms/
│   │   │   ├── [x] database/
│   │   │   ├── [x] src/
│   │   │   └── [x] target/
│   ├── [x] 04_白箱審計工具/
│   │   └── [x] 工具使用_白箱靜態代碼審計工具包/
│   └── [x] 05_SDL與安全開發/
│   │   ├── [x] Java代碼審計入門篇_OWASP/
│   │   ├── [x] Web攻防實戰_NodeJS安全開發/
│   │   ├── [x] Web攻防實戰_SDL安全開發/
│   │   ├── [x] Web攻防實戰_漏洞修補流程/
│   │   └── [x] 原書籍_PHP/
├── [x] 06_網路安全與數位取證/
│   ├── [x] 01_網路協定分析與Scapy/
│   │   ├── [x] 外校_OpenSSL/
│   │   ├── [x] 外校_網路指令/
│   │   ├── [x] 教主Kali與Python_Scapy協定分析/
│   │   └── [x] 面試_TCPIP網路協定考題/
│   ├── [x] 02_端口掃描與Nmap工具/
│   │   ├── [x] HackTools_network/
│   │   │   ├── [x] devices/
│   │   │   ├── [x] protocol/
│   │   │   └── [x] transport/
│   │   ├── [x] HackTools_network_tools/
│   │   ├── [x] 教主Kali與Python_Nmap網路掃描/
│   │   └── [x] 試聽課福利_Nmap網絡端口掃描/
│   │   │   ├── [x] licenses/
│   │   │   ├── [x] nselib/
│   │   │   └── [x] scripts/
│   ├── [x] 03_流量分析PCAP/
│   │   ├── [x] CTF常見題型解析_流量/
│   │   ├── [x] HW_流量/
│   │   ├── [x] ctf_360勸退賽題_流量分析/
│   │   │   ├── [x] 流量分析1/
│   │   │   └── [x] 流量分析2/
│   │   ├── [x] ctf_流量/
│   │   ├── [x] ctf_流量分析/
│   │   ├── [x] ctf_流量分析賽題/
│   │   │   ├── [x] ctf_wireshark/
│   │   │   └── [x] 取证_6/
│   │   ├── [x] 原書籍_Wireshark流量分析/
│   │   ├── [x] 國科CTF_流量取證/
│   │   ├── [x] 工具使用_Wireshark流量監聽/
│   │   │   └── [x] 课程资料/
│   │   └── [x] 試聽課福利_Wireshark流量分析/
│   ├── [x] 04_數位取證DFIR/
│   │   ├── [x] 教主Kali與Python_GPS/
│   │   ├── [x] 教主Kali與Python_PDF元數據數位取證/
│   │   └── [x] 教主Kali與Python_回收站數位取證/
│   ├── [x] 05_IDS與網路監控/
│   │   └── [x] 試聽課福利_IDS與主機網絡監控/
│   └── [x] 06_流量與日誌腳本/
│   │   └── [x] ctf_常用流量與日誌分析腳本/
├── [x] 07_藍隊防禦與護網營運/
│   ├── [x] 01_護網專案營運/
│   │   ├── [x] HW_自查/
│   │   ├── [x] HW_藍隊日誌/
│   │   └── [x] HW_資產梳理/
│   ├── [x] 02_系統與資料庫加固/
│   │   ├── [x] HW_加固/
│   │   ├── [x] 系統加固_Linux系統安全加固/
│   │   ├── [x] 系統加固_MySQL數據庫安全加固/
│   │   ├── [x] 系統加固_漏洞加固/
│   │   └── [x] 系統加固_移動端APP加固技術/
│   ├── [x] 03_存取控制與防火牆/
│   │   └── [x] 外校_Linux存取控制與防火牆/
│   ├── [x] 04_日誌與告警研判/
│   │   └── [x] 暗月Web紅隊_Web日誌分析與逃逸檢測/
│   └── [x] 05_藍隊面試與培訓/
│   │   └── [x] HW_護網藍隊面試實戰培訓/
├── [x] 08_通用學習與面試庫/
│   ├── [x] 01_CTF競賽Writeup與題解/
│   │   ├── [x] 51CTO奪旗賽_綜合測試/
│   │   ├── [x] ctf_CTF教材/
│   │   ├── [x] ctf_CTF競賽Writeup匯總/
│   │   ├── [x] ctf_Redrain安全簡報/
│   │   ├── [x] ctf_歷年競賽Writeup/
│   │   │   ├── [x] 2017/
│   │   │   ├── [x] 2018/
│   │   │   ├── [x] 2019/
│   │   │   ├── [x] AWD/
│   │   │   └── [x] template/
│   │   ├── [x] ctf_理論競賽考點彙總/
│   │   ├── [x] ctf_競賽通用_CTF技巧/
│   │   ├── [x] ctf_綜合解題資源/
│   │   └── [x] 靶场训练课程靶场资料/
│   │   │   ├── [x] FTP服务/
│   │   │   ├── [x] HTTP服务/
│   │   │   ├── [x] SMB服务/
│   │   │   ├── [x] SSH服务/
│   │   │   ├── [x] 综合漏洞/
│   │   │   └── [x] 靶场夺旗/
│   ├── [x] 02_CTF賽制介紹與平台指南/
│   │   ├── [x] 51CTO奪旗賽_賽制介紹/
│   │   ├── [x] 國科CTF_平台/
│   │   ├── [x] 國科CTF_賽制介紹/
│   │   └── [x] 國科CTF_賽前指導答疑/
│   ├── [x] 03_SRC與認證/
│   │   └── [x] SRC漏洞挖掘與安全獎勵規範/
│   ├── [x] 04_通用基礎知識/
│   │   └── [x] 通用基礎_Linux與網絡安全基礎/
│   ├── [x] 05_HR與跨領域面試/
│   │   └── [x] HR綜合面試與跨領域考題/
│   └── [x] 06_輔助工具與備份/
│   │   └── [x] 國科CTF_Notepad/
└── [x] 09_基礎設施與運營環境/
│   ├── [x] 01_虛擬機與作業系統/
│   │   ├── [x] VMware.Workstation.v12.0.0注册机/
│   │   ├── [x] 工具使用_KaliLinux/
│   │   └── [x] 工具使用_VMware/
│   ├── [x] 02_程式語言運行時/
│   │   ├── [x] 國科CTF_JAVA環境/
│   │   ├── [x] 國科CTF_Python環境/
│   │   └── [x] 工具使用_DOTNET環境/
│   │   │   ├── [x] AppInfo/
│   │   │   ├── [x] Mantra/
│   │   │   ├── [x] profile/
│   │   │   └── [x] settings/
│   ├── [x] 03_Web與容器環境/
│   │   ├── [x] 國科CTF_PHPstudy環境/
│   │   └── [x] 工具使用_phpStudy/
│   ├── [x] 04_連線與傳輸工具/
│   │   └── [x] 工具使用_Xshell/
│   └── [x] 05_綜合實驗環境/
│   │   ├── [x] HackTools_tools/
│   │   │   ├── [x] crack/
│   │   │   ├── [x] metasploit/
│   │   │   ├── [x] other/
│   │   │   └── [x] web/
│   │   ├── [x] 國外全套滲透_實驗環境/
│   │   ├── [x] 國科CTF_解題環境/
│   │   └── [x] 工具使用_實驗環境/
│   │   │   └── [x] 05-靶场/
```
