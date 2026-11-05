# 講師與助教指引手冊 (Instructor & TA Guide)

> **課程**：`WORKSHOP_202610_NET_Wireshark-v2`  
> **預計時間**：20 分鐘精華講解 ＋ 課堂/課後實作引導

---

## ⏱️ 20 分鐘精準節奏控制

| 時間區段 | 投影片頁數 | 教學重點與劇本 | 常見學生疑問與應對 |
| :---: | :---: | :--- | :--- |
| **00:00 - 04:00** | **P.1 - P.3** | **定位與介面**：以「使用者說網頁打不開」為例，說明 Application Log 與網卡封包差異，導覽三大核心顯示區。 | 學生問：「看伺服器 Log 不夠嗎？」<br>➔ 答：「若連線在 OS Kernel 掉了，Log 根本連一筆都不會寫入。」 |
| **04:00 - 08:00** | **P.4 - P.5** | **起手式與過濾**：教學生看右側「即時流量波形（Sparkline）」避開虛擬網卡選對網卡，講解 display filter 基本語法。 | 學生問：「有十幾張網卡選哪張？」<br>➔ 答：「看右側有折線起伏的實體網卡才是出入口！」 |
| **08:00 - 13:00** | **P.6 - P.9** | **實作一（連線診斷）**：實測正常 ping、Type 3 退信、Rate limit 逾時丟棄，以及 ping -i 1 逼出 Type 11。 | 學生問：「為什麼連續 ping 同一個 IP 結果會變？」<br>➔ 答：「第一筆上游報錯，第二筆觸發頻率限制丟棄。」 |
| **13:00 - 17:00** | **P.10 - P.12** | **實作二與三（明文鑑識）**：開啟 ch1.pcap 與 ch2.pcap，現場右鍵 Follow TCP Stream 看穿明文帳密與字元回顯。 | 學生會驚呼：「原來密碼真的直接顯示出來！」此時立刻點出使用 SSH/SFTP 的必要性。 |
| **17:00 - 20:00** | **P.13 - P.14** | **排錯流程與發布作業**：梳理四步驟，公告實作一、二、三的情境要求與評分標準。 | 提醒：「作業不准只交黑底終端機截圖，必須附上 Wireshark 對應封包。」 |

---

## 🙋‍♂️ 課堂必備問答（Q&A 破冰劇本）

### Q1：學生問「既然在 CMD 打 ping 就能看到回覆，為什麼還需要開 Wireshark？」
* **助教回答劇本**：
  > 「CMD 的 ping 只是應用程式的回報。當它顯示 `Request timed out` 時，你根本不知道是本機網卡壞了、外部主機當機、還是中間路由器擋了。在 Wireshark 裡，你能看見封包到底有沒有出網卡，甚至能看見中途路由器主動發送的報錯封包。」

### Q2：學生問「Follow TCP Stream 的紅字和藍字代表什麼？」
* **助教回答劇本**：
  > 「紅字代表客戶端發送（Client Request，例如你打的帳號密碼），藍字代表伺服器回傳（Server Response，例如 HTTP 200 OK 或 FTP 230 Login Successful）。」

### Q3：學生問「為什麼我 ping 192.0.2.1 時，終端機一下顯示 Destination net unreachable，一下顯示 Request timed out？」
* **助教回答劇本**：
  > 「這正是 Wireshark 存在的價值：
  > 1. 第一筆封包：學校/骨幹路由器（如 203.72.x.x）查無路由，主動回傳 ICMP Type 3 告知『網路不可達』。
  > 2. 第二筆封包：路由器啟動了防禦機制（RFC 1812 ICMP Rate Limit 頻率限制），直接靜默丟棄不回話，所以 Windows 只能乾等超時印出 Request timed out。
  > 差別就在於中途路由器有沒有把報錯封包丟回給你的網卡。」

---

## 🔑 作業參考解答與評分標準 (TA Rubric & Answer Key)

### 實作一：ICMP Ping & Tracert (配分 40%)
* **截圖檢查點**：
  1. Wireshark 畫面過濾條件顯示 `icmp`。
  2. 封包清單清楚出現 `Echo (ping) request` (`Type: 8`) 與 `Echo (ping) reply` (`Type: 0`)。
  3. 捕捉到異常或路由控制封包：
     - ping `192.0.2.1` 截圖到上游路由器回送的 `Destination unreachable (Type: 3)` 或逾時無回應 `[no response found!]`（任一者皆屬正確）。
     - 或執行 `tracert -d -h 1 8.8.8.8` 截圖到第一跳路由器的 `Time-to-live exceeded (Type 11)`。
* **文字結論要求**：
  * 能清楚說明：Wireshark 能一眼區分中途節點是主動回報錯誤（Type 3/11），還是路徑上遭靜默丟棄（Timeout 已讀不回），避免終端機模糊字眼的誤導。

### 實作二：Root-Me 97 · FTP authentication (配分 40%)
* **題目檔案**：`ch1.pcap`
* **標準答案**：
  * 帳號：`USER ...`（請依下載檔案實際內容為準，通常為明文字串）
  * 密碼：`PASS ...`
* **截圖檢查點**：
  * 截出 `Follow TCP Stream` 視窗，紅字部分清楚看見 `USER` 與 `PASS` 指令。
* **文字結論要求**：
  * 必須點出：「FTP 未加密（CWE-319），密碼明文傳輸極易遭側錄，應改用 SFTP (Port 22)。」

### 實作三（加分題）：Root-Me 99 · TELNET authentication (配分 20%)
* **題目檔案**：`ch2.pcap`
* **標準答案**：
  * 還原出登入帳號與密碼。
* **檢查點**：
  * 截出 Telnet 串流內容，說明字元回彈（Character Echo）現象。
