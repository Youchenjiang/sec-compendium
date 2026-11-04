# Wireshark 網路封包分析實作作業講義 (Student Handout)

> **課程名稱**：電腦網路與資訊安全實務  
> **作業名稱**：Wireshark 封包追蹤與未加密通訊鑑識實作  
> **繳交期限**：請依課程平臺 (ee-class) 公告為準  
> **繳交格式**：請將本講義所要求之**【步驟截圖】**與**【情境技術分析】**整理為 PDF 檔案繳交。

---

## 🎯 實作一：辦公室連線診斷 ── ICMP Ping & Tracert 解剖 (40%)

### 1. 商業與工程情境
你是企業 IT 維運工程師。業務同仁通報：「網頁打不開、系統連不上，公司是不是斷網了？」  
你的任務是進行**故障隔離 (Fault Isolation)**，利用外網通訊基準點 `8.8.8.8`（Google DNS）確認本機至外部網路的實體與網路層是否暢通。

### 2. 操作步驟
1. 開啟 Wireshark，雙擊你目前正在連網的介面（例如：`Wi-Fi` 或 `乙太網路`，可觀察介面清單右側即時流量波形判斷）開始側錄。
2. 在頂部顯示過濾列 (Display Filter) 輸入：`icmp` 並按 Enter。
3. 開啟終端機（Windows 請開 CMD 或 PowerShell，Mac 請開 Terminal），進行以下兩組對比測試：
   * **測試 A（正常連通）**：輸入 `ping -n 2 8.8.8.8`，觀察一去一回的 `Echo request (Type 8)` 與 `Echo reply (Type 0)`。
   * **測試 B（異常分析）**：輸入 `ping -n 2 192.0.2.1`（RFC 5737 測試保留網段），觀察終端機與 Wireshark 封包變化：
     * 是否收到上游路由器回傳之 `Destination unreachable (Type 3)`？
     * 或是否因觸發頻率限制/防火牆阻擋而顯示 `Request timed out`（Wireshark 標記 `no response found`）？
4. （進階對照）在終端機輸入：
   ```cmd
   tracert -d -h 1 8.8.8.8
   ```
   觀察 Wireshark 中是否有第一跳路由器回傳之 `Time-to-live exceeded (Type 11)` 封包。

### 3. 作業繳交要求
* **【截圖 1】**：包含 Wireshark 介面的截圖，需清楚呈現過濾條件 `icmp`、正常 ping 的 `Type 8 / Type 0` 封包，以及測試異常 (`192.0.2.1`) 或 tracert 時捕捉到之特殊封包（如 `Type 3`、`Type 11` 或 `no response`）。
* **【簡答題 1】**：
  1. 為什麼在終端機執行 ping 已經看到回傳了，工程師還需要打開 Wireshark 看 ICMP 封包？
  2. 當你 ping 測試網段 `192.0.2.1` 時，你的終端機與 Wireshark 各自出現了什麼現象？請說明這代表封包在網路中遭遇了何種處置（是中途節點主動回報，還是路徑上遭丟棄無人回應）？

---

## 🎯 實作二：內網資安合規稽核 ── FTP 明文密碼側錄 (40%)

### 1. 商業與工程情境
你是資安稽核員。公司明令禁止使用未加密協定，但入侵偵測系統（IDS）告警，指出有同仁私自架設老舊 FTP 伺服器傳送業務報表。網管人員辯稱：「我們 FTP 登入都有設密碼，不知道密碼的人進不來，很安全！」  
你的任務是分析交換機側錄檔 `ch1.pcap`，向管理層提出技術證據，證明明文傳輸（CWE-319）的危險性。

### 2. 操作步驟
1. 下載作業附件中的 `ch1.pcap`（亦可至 [Root-Me 題目頁面: FTP - authentication](https://www.root-me.org/en/Challenges/Network/FTP-authentication) 下載）。
2. 在 Wireshark 中開啟 `ch1.pcap` 檔案。
3. **嘗試以下兩種分析方法**：
   * **方法 A（語法過濾）**：在過濾列輸入 `ftp`，觀察封包清單中的 `USER` 與 `PASS` 指令。
   * **方法 B（串流還原）**：在任一封包上按右鍵 ➔ 選擇 `Follow` ➔ `TCP Stream`，觀察彈出的對話視窗。
4. 找出該員登入時使用的**帳號 (Username)** 與 **密碼 (Password)**。

### 3. 作業繳交要求
* **【截圖 2】**：截出 `Follow TCP Stream` 視窗（或封包清單），清楚標示出找到帳號與密碼的位置。
* **【簡答題 2】**：
  1. 請寫出從封包中還原出的 FTP 帳號與密碼。
  2. 請向管理層提出兩點具體的資安改善處置（例如應改用何種加密協定與連接埠）。

---

## 🌟 實作三（加分題）：遠端管理憑證鑑識 ── Telnet 終端回彈分析 (20%)

### 1. 商業與工程情境
數位鑑識團隊接獲通報，機房核心設備疑遭連線竄改。調閱之側錄檔 `ch2.pcap`（取自 [Root-Me: TELNET - authentication](https://www.root-me.org/en/Challenges/Network/TELNET-authentication)）記錄了一段遠端維護會話。請還原操作者的登入帳密。

### 2. 操作步驟與繳交要求
1. 用 Wireshark 開啟 `ch2.pcap`。
2. 過濾 `telnet`，右鍵使用 `Follow TCP Stream` 重組對話。
3. **【加分截圖】**：截出還原之 Telnet 連線對話視窗。
4. **【加分回答】**：寫出破解之帳密，並簡短說明為什麼 Telnet 在通訊時會出現「敲一個字母、回彈一個字母（Character Echo）」的現象。
