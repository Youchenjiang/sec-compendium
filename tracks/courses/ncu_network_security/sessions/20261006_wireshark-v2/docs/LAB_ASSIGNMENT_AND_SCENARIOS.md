# Wireshark 實戰工作坊：課程情境設計與作業規劃指引

> **課程代號**：`WORKSHOP_202610_NET_Wireshark-Fundamentals-v2`  
> **授課對象**：大學部資管系學生（幾乎無 Wireshark 先備經驗）  
> **核心設計思維**：  
> 1. 拒絕死記按鈕與指令，每個操作背後都有明確的**「真實工作情境（Who / What / Why / Takeaway）」**。  
> 2. 拒絕無效折騰（如尋找已關閉的 HTTP 測試站、指令列切大檔）。  
> 3. 確保所有作業在 10~15 分鐘內**「做得出來、看得懂封包、拿得到成果」**。

---

## 📌 實作總覽架構

```
[實作一：本機連線診斷] ────────► [實作二：內網資安合規] ────────► [實作三 / 加分：遠端維護鑑識]
   ICMP Ping & Tracert             FTP 明文帳密側錄 (Root-Me 97)      Telnet 字元回彈鑑識 (Root-Me 99)
   • 驗證實體/網路層連通性          • CWE-319 明文傳輸風險             • 互動式終端通訊還原
   • 辨識 Type 8/0/11 差異          • Follow TCP Stream 串流重組       • 體會 Character Echo 特性
   • 了解 ICMP Tunneling 概念       • 掌握 Display Filter (ftp)        • 明白 SSH 替代必要性
```

---

## 🛠️ 實作一：本機網路連線診斷（ICMP Ping & Tracert 深度解剖）

### 1. 商業與工程情境
* **你的角色**：企業 IT 網管 / 系統運維工程師。
* **遭遇問題**：業務部同仁通報：「網頁打不開、系統連不上，公司是不是斷網了？」
* **核心排查思考**：
  * **故障隔離 (Fault Isolation)**：到底是真的實體斷網，還是只有特定網站故障，或是 DNS 解析伺服器當機？
  * 選擇 `8.8.8.8`（Google Public DNS）作為全球公認的外網基準點。
* **為什麼終端機不夠，必須開 Wireshark？**：
  * 終端機只會顯示 `Request timed out`（這句話掩蓋了 4 種截然不同的底層故障）。
  * Wireshark 能看見：封包到底有沒有出網卡？路上有沒有路由器主動回覆報錯？

### 2. 實戰步驟（三階段對比體驗）

#### ① 階段 A：正常通訊（一去一回）
* **終端指令**：`ping -n 2 8.8.8.8`
* **Wireshark 過濾式**：`icmp`
* **觀察現象**：
  * 看到兩組對稱的封包：
    1. `Echo (ping) request` (`Type: 8, Code: 0`)
    2. `Echo (ping) reply` (`Type: 0, Code: 0`)
  * 展開 IP Header，看見真實的 Source IP、Destination IP 以及當前網路跳數（TTL）。

#### ② 階段 B：異常排查（對比路由器報錯 Type 3 與靜默逾時 Timeout）
* **終端指令**：`ping -n 2 192.0.2.1`  
  *(註：`192.0.2.0/24` 為 RFC 5737 官方測試保留網段，全球公網無此路由)*
* **觀察現象（課堂依網路環境與頻率限制，會出現兩種現象）**：
  * **現象 A（收到節點主動報錯）**：
    * 終端機顯示：`Reply from [上游路由器 IP]: Destination net unreachable.`
    * Wireshark 顯示：上游骨幹路由器（如 TANet `203.72.x.x`）回傳 `Destination unreachable (Network unreachable)` (`Type: 3, Code: 0`)。
    * 意義：中途路由器查無路由條目，主動發送存證信函告知發送端。
  * **現象 B（靜默丟棄 / 逾時）**：
    * 終端機顯示：`Request timed out.`
    * Wireshark 顯示：只有 Request (`Type: 8`) 送出網卡，右側完全沒有任何回應（標記 `[no response found!]`）。
    * 意義：觸發路由器防禦機制（RFC 1812 ICMP Rate Limit 頻率限制）或防火牆丟棄，中途已讀不回。
* **技術結論**：單看終端機容易混淆，但透過 Wireshark 能一眼區分「中途節點主動報錯」與「封包遭丟棄已讀不回」。

#### ③ 階段 C：節點報錯（看見路由器主動發送 ICMP Type 11）
* **終端指令**：`tracert -d -h 1 8.8.8.8`  
  *(參數：`-d` 不查網域名稱速度快，`-h 1` 限制封包生存跳數 TTL=1)*
* **觀察現象**：
  * 本機送出 `TTL=1` 的 Echo Request。
  * 抵達第一台路由器（系館/宿舍 Gateway）時 TTL 歸零被丟棄。
  * **路由器主動回傳黑底紅字/灰字封包**：`Time-to-live exceeded in transit (Type: 11, Code: 0)`。
  * **結論**：學生親眼理解 Traceroute 原理 ── 故意讓封包在中途死掉，逼各節點回報自身 IP。

#### ④ 階段 D（進階概念）：觀察 Payload 與隱蔽通道 (ICMP Tunneling)
* **終端指令**：`ping -l 64 -n 1 8.8.8.8`
* **觀察現象**：
  * 點選封包下方的 `Packet Bytes`，親眼看見 Windows 預設填充的 64 bytes 測試字母：  
    `abcdefghijklmnopqrstuvwabcdefghijklmnopqrstuvwabcdef...`
  * **資安觀念**：資料肚子裡是可以放自訂資料的；駭客若把竊取的密碼切碎藏在 ping 裡面外傳，就是典型的 **ICMP 隱蔽通道 (ICMP Tunneling)**。

---

## 🛠️ 實作二：內網資安合規稽核（FTP 明文帳密側錄）

### 1. 商業與工程情境
* **你的角色**：資安工程師 / 內部資安稽核員。
* **遭遇問題**：
  * 入侵偵測系統（IDS）發出告警，指出內網有人私自架設老舊 FTP 伺服器傳送業務報表。
  * 維運人員辯解：「我們 FTP 登入都有設密碼，外人不知道密碼進不來，很安全！」
* **你的任務**：
  * 調閱交換機側錄檔 `ch1.pcap`（取自 Root-Me 97 挑戰）。
  * 提出具體的技術證據，證明明文傳輸（CWE-319）的危險性。

### 2. 實戰步驟
1. **載入檔案**：直接用 Wireshark 打開 `ch1.pcap`。
2. **方法一（過濾語法）**：
   * 在上方過濾列輸入：`ftp`
   * 封包清單立刻篩出極少數關鍵控制封包，一眼看見：
     * `Request: USER [帳號名稱]`
     * `Request: PASS [真實密碼]`
3. **方法二（滑鼠串流還原）**：
   * 在任意 TCP 封包上點擊右鍵 ➔ `Follow` ➔ `TCP Stream`。
   * 紅色字體（客戶端送出）直接浮現出完整登入交談過程，密碼赤裸裸暴露。
4. **技術處置與結論**：
   * 證實通訊協定本身未經 TLS/SSL 保護，同網段或中繼節點側錄即可直視密碼。
   * **改善措施**：全面關閉 Port 21 (FTP)，改用具備 SSH 加密的 **SFTP (Port 22)** 或 **FTPS**。

---

## 🛠️ 實作三（加分題）：遠端管理憑證洩漏鑑識（Telnet 終端封包還原）

### 1. 商業與工程情境
* **你的角色**：數位鑑識與事件應變小組（DFIR）。
* **遭遇問題**：
  * 機房核心路由器設定遭異常改動，側錄檔顯示有一筆來自內網的遠端管理會話 `ch2.pcap`（取自 Root-Me 99 挑戰）。
  * 管理員宣稱是例行維護，但需要驗證當初登入使用的是何種身分憑證與指令。
* **核心排查思考**：
  * Telnet (Port 23) 與 FTP 雖然同為明文協定，但 Telnet 是「互動式虛擬終端（Interactive Terminal）」。
  * 每當使用者敲下鍵盤的一個字母，終端機伺服器會將該字元回彈給螢幕顯示（**Character Echo**）。

### 2. 實戰步驟
1. **載入檔案**：用 Wireshark 打開 `ch2.pcap`。
2. **過濾會話**：輸入過濾式 `telnet`，右鍵 ➔ `Follow` ➔ `TCP Stream`。
3. **字元拼裝與還原**：
   * 觀察 Telnet 登入畫面提示 `login:` 與 `Password:`。
   * 分析單一字元封包回彈序列，還原出操作者輸入的管理員密碼。
4. **技術處置與結論**：
   * Telnet 缺乏加密機制，且每次擊鍵都以明文傳輸。
   * **改善措施**：停用系統中的 `telnetd` 守護行程，強制升級至 **OpenSSH**。
