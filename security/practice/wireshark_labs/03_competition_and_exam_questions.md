# 🏆 模組 03：技能競賽真題與模擬考題精選

> **資料來源**：
> - 全國技能競賽/金盾獎實戰真題：[`tracks/lab/golden_shield_sprint/exam_analysis_manual.md`](../../tracks/lab/golden_shield_sprint/exam_analysis_manual.md)
> - 模擬考實戰 B 卷：[`security/practice/exams/mock_exam_b_lab_questions.md`](../exams/mock_exam_b_lab_questions.md)
> - 模擬考 A 卷：[`security/practice/exams/mock_exam_a_100q_questions.md`](../exams/mock_exam_a_100q_questions.md)
> - 藍隊實戰手冊 06.1：[`06.1_wireshark_tcp_handshake.md`](../../knowledge/blue_team/playbooks/phase_0_foundation/06.1_wireshark_tcp_handshake.md)

---

## 🎯 第一部分：全國技能競賽 / 金盾獎官方實戰真題

### 案例 A：DNS 隱蔽通道資料外洩 (DNS Exfiltration - `Topic1.pcap`)
- **題目背景**：某電商公司資安監控在深夜亮起紅燈：一台內部資料庫主機在離峰時段對外送出大量規律的 DNS 查詢。取得封包 `Topic1.pcap`。
- **原始流量拆解**：
  打開 PCAP 後，Wireshark 出現連續上百筆規律的 DNS 查詢：
  `s000.416c696365...sync-cdn.exfil-node.top` ➔ 子域名內嵌 Base32/Hex 資料。
- **真題題目與標準解答**：
  1. **【Q1】請分析出攻擊者用來外傳資料的域名？**
     - **標準答案**：`sync-cdn.exfil-node.top`
     - **Wireshark 語法**：`dns.flags.response == 0`，鎖定大量攜帶異常長子網域的查詢。
  2. **【Q2】這份被外洩的客戶名單一共有幾筆紀錄？**
     - **標準答案**：`29` 筆（從 id=1 到 id=29）。
  3. **【Q3】結合以上資訊，分析出駭客於攻擊中取得的特殊字串 FLAG？**
     - **標準答案**：`skill54{sl0w_l34k_thru_dns53}`
     - **解析**：29 筆客戶名單最後一欄的字元垂直排列拼出 Flag。

---

### 案例 B：電商網站 Web 攻擊鏈還原 (SQLi ➔ RCE - `traffic.pcap`)
- **題目背景**：某公司電商網站 TechMart 疑似遭入侵。對外閘道側錄了 HTTP 流量 `traffic.pcap`，混雜顧客瀏覽、爬蟲、掃描器目錄爆破與真實攻擊者滲透流程。
- **原始流量拆解**：
  - 掃描器噪音：`159.203.44.90` 大量發送 `/admin.php`、`/wp-admin.php`，全回 404。
  - 真實攻擊者：`82.45.112.207` 進行 SQL 注入、後台登入並透過診斷端點 RCE。
- **真題題目與標準解答**：
  1. **【Q4】成功取得 initial access 的攻擊者來源 IP？**
     - **標準答案**：`82.45.112.207`
  2. **【Q5】目錄爆破造成大量 404、但並未成功入侵的掃描器 IP 為？**
     - **標準答案**：`159.203.44.90`
     - **Wireshark 語法**：`http.response.code == 404` 統計 Top IP。
  3. **【Q6】成功利用 SQL injection 漏洞的 API 端點為？**
     - **標準答案**：`http://185.199.52.10/api/v1/products/query`
  4. **【Q7】透過 SQLi 洩漏並被拿去登入網站的管理者帳號與密碼？**
     - **標準答案**：`admin` / `S3cur3!TechM4rt#2026`
  5. **【Q8】登入網站後，攻擊者透過哪一個端點取得 RCE？**
     - **標準答案**：`http://185.199.52.10/api/v1/admin/diagnostics`
  6. **【Q9】攻擊者最終讀取到的 FLAG？**
     - **標準答案**：`skill54{s0urc3m4p_j50n_un10n_2_rc3}`

---

## 📝 第二部分：模擬試卷（Mock Exam）精選考題

### 1. 模擬試卷 B 卷（實戰鑑識題）
- **第 63 題**：若要在 Wireshark 中僅過濾顯示 `Topic1.pcap` 中所有的 DNS 查詢請求封包，應輸入何種顯示過濾表達式？  
  - **解答**：`dns.flags.response == 0`
- **第 64 題**：若使用 `tshark` 命令列工具直接提取所有 DNS 查詢的主機名稱並導出至文字檔，應下達何種指令？  
  - **解答**：`tshark -r Topic1.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name > dns_queries.txt`
- **第 67 題**：在 Wireshark 中，若要搜尋所有包含字串 `flag{` 的 TCP 數據流，應使用何種過濾語法？  
  - **解答**：`tcp contains "flag{"`
- **第 69 題**：在 SSL/TLS 封包解密中，若鑑識人員擁有伺服器的私鑰或瀏覽器導出的 `SSLKEYLOGFILE`，在 Wireshark 的哪一個設定選單中載入該金鑰檔案即可將 HTTPS 密文即時解密為明文 HTTP？  
  - **解答**：`Preferences` ➔ `Protocols` ➔ `TLS` ➔ `(Pre)-Master-Secret log filename`（或 `RSA keys list`）
- **第 78 題**：Wireshark 的「追蹤串流」（Follow Stream）功能中，TCP Stream 追蹤器通常以哪兩種顏色分別表示客戶端上傳流量與伺服器下行回顯？  
  - **解答**：**紅色** 代表客戶端上傳流量（Client to Server），**藍色** 代表伺服器下行回顯（Server to Client）。

### 2. 模擬試卷 A 卷（單選核心概念題）
- **第 41 題**：若鑑識人員想在 Wireshark 中過濾出「來源或目的 IP 為 192.168.1.100，且包含 HTTP POST 請求」的所有封包，應輸入何種 Display Filter？  
  - **解答**：`ip.addr == 192.168.1.100 && http.request.method == "POST"`
- **第 45 題**：在 Wireshark 分析封包時，若發現某一 TCP 連線中，發送端不斷發送負載極短的小封包，且 TCP 標誌中 PSH (Push) 旗標持續置位，隨後接收端立即回傳大量回顯字元，這種流量行為最符合下列哪一種應用程式？  
  - **解答**：互動式遠端連線終端（如 SSH 或 Telnet 會話）。

---

## 🧪 第三部分：手冊 06.1 經典演練題 (SYN Flood & RST 異常)

### 靶場任務：Wireshark Sample Captures (`synflood.pcap`)
1. **任務 1**：輸入過濾器 `tcp.flags.syn == 1 && tcp.flags.ack == 0`，計算半開連線封包佔總流量的比例。
2. **任務 2**：點開 `Statistics` ➔ `Conversations` ➔ `TCP` 分頁，觀察封包傳輸方向與 Byte 數的不對稱性。
3. **任務 3**：檢視 SYN 封包的 `TCP Options`，記錄是否攜帶 `MSS`、`SACK Permitted`，判定流量是真實作業系統還是工具（hping3 / Scapy）偽造。

### 核心 5 題情境測驗：
- **Q1**：Client 送出 `SYN` (Seq = 1000)，Server 回應的 `SYN, ACK` 封包中 `Seq` 與 `Ack` 值意義為何？  
  *答：`Seq` 為伺服器自訂的 ISN_s，`Ack` 嚴格等於 `Client_ISN + 1`（1001）。*
- **Q2**：為什麼 SYN Flood 攻擊即便頻寬只佔 20% 也能癱瘓高規格伺服器？  
  *答：攻擊耗盡了作業系統核心的半開連線佇列結構（SYN Backlog Queue）。*
- **Q3**：Nmap `-sS`（半開掃描）與 `-sT`（全連線掃描）在封包交握層面的差異？  
  *答：`-sS` 在收到 SYN-ACK 確認開埠後主動回彈 RST 中斷，不建立完整連線與應用層 Session；`-sT` 走完整三次交握。*
- **Q4**：啟用 Linux 核心 `tcp_syncookies = 1` 抵禦 SYN Flood 時會犧牲什麼 TCP 效能特性？  
  *答：犧牲了大型視窗縮放（Window Scale）、選擇性確認（SACK）等 TCP Options 協商優化。*
- **Q5**：Wireshark 中看到 `[RST, ACK]` 封包且序號在視窗內，但來源 MAC 是防火牆而非伺服器本身代表什麼？  
  *答：代表邊界入侵防禦系統（IPS/NGFW）觸發規則，主動發動了 TCP Reset 注入阻斷。*
