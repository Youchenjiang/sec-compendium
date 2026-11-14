# 專用環境與特定網路閘道 WAF Tarpit（靜默丟包）分析報告

> **文件性質**：特定實驗室 / 校園網路環境的例外現象技術分析（Technical Exception Report）  
> **測試時間**：2026-11-13  
> **測試標的**：`*.cylabacademy.net` 系列靶機特定環境  

---

## 1. 現象描述 (Symptom)

在特定校園或實驗室網路環境下，透過瀏覽器或命令列對 Web 靶機送出包含 SQL 注入特徵之請求時：
* **正常請求**（如純英數字、普通單引號、一般帳密）：伺服器秒回（`HTTP 200 OK`，延遲約 0.3 秒）。
* **含特定 SQL 運算子請求**（如 `' OR 1=1`、`' AND 1=1`）：
  * 瀏覽器呈現**持續轉圈圈（Loading）**。
  * 經過 10~15 秒後，連線逾時中斷（`ERR_CONNECTION_TIMED_OUT` 或 `curl: (28) Operation timed out with 0 bytes received`）。
  * 伺服器端**未回傳 HTTP 403 Forbidden 或任何錯誤訊息**。

---

## 2. 終端機封包與特徵測試數據 (Empirical Data)

針對 `http://xebec.cylabacademy.net:13078/login.php` 進行最小特徵拆解測試：

| 測試 Payload | 測試指令 | 結果 | 反應時間 | 狀態碼 |
| :--- | :--- | :--- | :--- | :--- |
| `username=admin` | 正常字串 | ✅ 正常秒回 | 0.4s | `HTTP 200 OK` |
| `username=test'` | 單引號探針 | ✅ 正常秒回 | 0.3s | `HTTP 200 OK` |
| `username=1=1` | 純等號 | ✅ 正常秒回 | 0.3s | `HTTP 200 OK` |
| `username=1 and 1` / `1 or a` | 獨立關鍵字 | ✅ 正常秒回 | 0.3s | `HTTP 200 OK` |
| **`username=1 or 1=1`** | **OR + 比較式** | ❌ **卡死斷線** | **15s 逾時** | **0 bytes received** |
| **`username=1 or 3=4`** | **OR + 任意等式** | ❌ **卡死斷線** | **15s 逾時** | **0 bytes received** |
| **`username=1 or 1 like 1`** | **OR + LIKE 語法** | ❌ **卡死斷線** | **15s 逾時** | **0 bytes received** |
| **`username=1 and 1=1`** | **AND + 等式** | ❌ **卡死斷線** | **15s 逾時** | **0 bytes received** |

---

## 3. 機制分析 (Root Cause Analysis)

從 TCP 握手與 HTTP 傳輸過程分析：
1. **TCP 連線已建立**：`curl` 顯示 `Established connection to ... port ...`，三方握手成功。
2. **應用層靜默丟包 (Silent Drop / Tarpit)**：
   * 網路路徑上的中介設備（如反向代理、IPS 或網路閘道型 WAF）解析 HTTP 內容。
   * 匹配正則特徵：`/(or|and)\s+.*(=|like)/i`。
   * **阻斷策略不是 REJECT（不送 TCP RST，亦不發 HTTP 403），而是直接將後續 TCP ACK / HTTP Data 靜默丟棄（Drop）**。
3. **客戶端反應**：
   * 客戶端以為伺服器正在處理大型查詢，維持 Socket 連線等待。
   * 直到達到 TCP 逾時限制，宣告逾時斷線。

---

## 4. 繞過技術驗證 (Evasion Techniques)

此機制為粗糙的正則字元匹配，可透過以下方式避開特徵判定：

### 手法 A：空白置換 (Whitespace Replacement)
以 SQL 多行註解 `/**/` 取代空格：
* `1'/**/or/**/true--` $\rightarrow$ 避開 `\s+` 匹配，順利通關。

### 手法 B：前置編碼 (Pre-encoding / Transformation)
若後端應用層本身有解碼行為（例如 `Irish-Name-Repo 3` 的 ROT13）：
* 原本的 `' or 1=1-- ` 經 ROT13 轉為 `' be 1=1-- `。
* 傳輸過程中特徵為 `be`，完全不吻合 `or/and` 關鍵字，直接穿透該閘道設備，並在後端正確執行。
