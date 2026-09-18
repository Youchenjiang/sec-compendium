# 🏁 HITCON 2026 Wargame 全面覆盤與技術檢討總結報告 (Post-Mortem & Retrospective)

> **競賽主題**：HITCON 2026 Wargame — PHP Vendor Under DocumentRoot Security Assessment  
> **結算結果**：4 Solves (owasp/phprbac x2, internations/http-mock, 等)  
> **整理日期**：2026-08-23  
> **核心目的**：深入剖析本輪自動化審計與協同作戰中的效率瓶頸、誤判根源、動靜態斷層，並沉澱出下一代高精準度代碼安全審計架構。

---

## 📑 目錄
1. [一、 戰局總覽與成果回顧](#一-戰局總覽與成果回顧)
2. [二、 核心痛點與效率低下之根本原因剖析 (Root Cause Analysis)](#二-核心痛點與效率低下之根本原因剖析)
3. [三、 關鍵漏洞原型與容器環境特性總結](#三-關鍵漏洞原型與容器環境特性總結)
4. [四、 成功靶標與失敗靶標深度對比](#四-成功靶標與失敗靶標深度對比)
5. [五、 未來自動化審計與協作體系重構藍圖](#五-未來自動化審計與協作體系重構藍圖)

---

## 一、 戰局總覽與成果回顧

本次 Wargame 的核心命題為：「**當開發者直接將 Composer vendor 安裝在 Web DocumentRoot (`/var/www/html/`) 下時所暴露的安全威脅**」。

- **成功解出靶標 (4 題 AC)**：
  1. `owasp/phprbac:2.0.0` (PHP 7.4.33) — `install.php` 頂層 Procedural 寫入後門。
  2. `owasp/phprbac:2.0.0` (PHP 8.4) — `install.php` 頂層 Procedural 寫入後門。
  3. `internations/http-mock:0.14.0` (PHP 7.4.33) — `public/index.php` 暴露路由 + SuperClosure 反序列化。
  4. 其他成功觸發之獨立 Procedural 端點。
- **遺憾未拿下的核心高分靶標**：
  - `oddvalue/laravel-drafts:3.2.0` (27 Solves)
  - `creolab/laravel-modules:0.5.6` (20 Solves)
  - `schickling/backup:0.6.0` (18 Solves)
  - `vrana/adminer:5.5.1` (高星數)

---

## 二、 核心痛點與效率低下之根本原因剖析

回顧整個協同作戰流程，造成效率低落與大量無效循環的核心原因可歸納為以下四大斷層：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            四大核心斷層剖析                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. 靜態正則與動態環境的「虛擬攻擊面斷層」                                   │
│    - 誤區：掃描到 class 內部有 eval/system 即判定可利用。                    │
│    - 真相：DocumentRoot 下無框架路由，class 檔直接訪問為 200 (0 bytes)。    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. Composer 發行包裁剪（--no-dev / export-ignore）認知延遲                  │
│    - 誤區：在完整 Git 源碼快取中審計 tests/ 與 examples/。                 │
│    - 真相：容器使用 --prefer-dist 安裝，多數 examples 在生產環境返回 404。   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. 缺乏即時本地 Docker 閉環驗證 (Validation Feedback Loop)                  │
│    - 誤區：依賴純文字對話與 Markdown 文件推演利用鏈。                      │
│    - 真相：未第一時間執行 `./run.sh` 進行動態 curl 驗收，導致死結被延遲暴露。│
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. 平台底層特徵解構不及時（readflag 與權限架構）                            │
│    - 誤區：過度推測 /readflag 包含 anti-bot 數學題，增加利用負擔。          │
│    - 真相：readflag.c 原始碼為直接 open(/flag2) 輸出，無需複雜管道。        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 三、 關鍵漏洞原型與容器環境特性總結

在本次最小化 Docker 容器（Apache + mod_php + 無全域框架引導）中，可利用的漏洞嚴格收斂為以下三種原型：

### 1. 原型 A：自包含獨立 Procedural 安裝/配置腳本
- **特徵**：`.php` 檔案未被封裝在 class 內，頂層直接讀取 `$_GET` / `$_POST` 並呼叫 `file_put_contents()` 或 `include`。
- **代表**：`owasp/phprbac` 的 `install.php`。
- **致命傷**：直接寫入未經轉義的變數到配置檔並立即 `require`。

### 2. 原型 B：自帶獨立 Web 路由與反序列化引擎
- **特徵**：套件內部包含自帶的 `public/index.php`，能夠在沒有外部框架的情況下自我啟動並解析 Request URI。
- **代表**：`internations/http-mock` 的 `public/index.php/_expectation`。
- **致命傷**：未授權端點直接呼叫 `@unserialize()` 且環境包含 SuperClosure。

### 3. 原型 C：配置覆寫與 Apache 屬性劫持 (.htaccess)
- **特徵**：容器 DocumentRoot 全數屬於 `www-data`，且 Apache 開啟 `AllowOverride All`。
- **利用點**：任何任意寫檔皆可寫入 `.htaccess` 設定 `php_value auto_prepend_file /flag1` 達成自動回顯。

---

## 四、 成功靶標與失敗靶標深度對比

| 套件名稱 | 預期利用路徑 | 實際受阻原因 / 成功關鍵 | 最終評判 |
| :--- | :--- | :--- | :---: |
| **`owasp/phprbac:2.0.0`** | `install.php` 代碼注入 | 頂層直通 Procedural，無任何前置阻礙 | ✅ **AC** |
| **`internations/http-mock:0.14.0`** | `public/index.php` 反序列化 | 自包含輕量路由 + SuperClosure eval | ✅ **AC** |
| **`vrana/adminer:5.5.1`** | SQLite 注入寫檔 | Adminer 要求密碼非空 vs SQLite 拒絕密碼之代碼死結 | ❌ **未解** |
| **`potsky/pimp-my-log:1.7.10`** | `configure.php` 註冊 log | `getlog` 正則表達式強制過濾非 log 行 | ⚠️ **PA 阻礙** |
| **`pingplusplus/pingpp-php:2.6.0`** | `charge/create.php` LFI | `require_once` 強制附加 `.php` 後綴阻斷直接讀 flag | ❌ **未解** |
| **`oddvalue/laravel-drafts:3.2.0`** | Rector / Draft 路由 | 框架依賴性強，缺少獨立啟動進入點 | ❌ **未解** |

---

## 五、 未來自動化審計與協作體系重構藍圖

為避免未來再次陷入「大量的虛擬漏洞報告 $\rightarrow$ 實測全部 404 $\rightarrow$ 浪費溝通成本」的惡性循環，下一代審計引擎必須建立以下三大鐵律：

### 1. 動態驗證先行 (Dynamic First Principle)
- **規則**：**嚴禁提交任何未經本地 Docker 實際發送 HTTP 請求驗證的分析結果**。
- **流程**：
  1. 啟動 `dist/run.sh` 建立真實 Challenge 容器。
  2. 自動發送探測請求至所有潛在端點。
  3. 唯有 HTTP 回傳狀態碼為 200 且輸出大小 $>0$（非純 class 定義）的端點，才啟動深層污點分析。

### 2. 生產環境發行包裁剪模擬 (Dist-Aware Filtering)
- **規則**：在審計前，自動檢查套件的 `.gitattributes` 與 `composer.json`。
- **過濾**：自動剔除標記為 `export-ignore` 的測試目錄與範例目錄，確保快取檔案與容器發行版 100% 同步。

### 3. 單一標準化 Task 數據協議
- **規範**：Agent 之間的通訊不再使用冗長的口語化描述，直接交付包含完整 `Method`、`URI`、`Headers`、`Body` 與 `Expected Grep String` 的 JSON TaskSpec，實現零歧義對接與自動驗收。

---

> 💡 **總結**：本次競賽雖僅拿下四題，但徹底摸清了「Vendor Under DocumentRoot」情境下的真實邊界與防禦機制，為後續代碼安全工具鏈的演進奠定了極為寶貴的實戰基石。
