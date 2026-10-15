# 🚩 模組 01：picoCTF / CMU CyLab 官方精選實戰題

> **資料來源**：[`cylab_all_challenges_catalog.md`](../challenges/platforms/cylab_picoctf/cylab_all_challenges_catalog.md)  
> **難度分佈**：Easy ~ Hard（共 9 道關卡）

---

### 1. Packets Primer (CyLab ID: 286)
- **平台與年份**：picoCTF 2022 ｜ Forensics ｜ Medium (100 pts)
- **官方傳送門**：[前往 CyLab 題目庫](https://learn.cylabacademy.org/library?search=Packets%20Primer)
- **實戰情境**：在未加密的區域網路中側錄了一段 TCP 流量 `packets.pcap`。
- **解題核心觀念**：
  - 傳統網路協定（如 HTTP、FTP、Telnet）以純文字傳輸，攻擊者監聽即可截獲全部內容。
  - **Wireshark 核心操作**：
    1. 開啟 PCAP，在任意 TCP 封包上點擊右鍵。
    2. 選擇 `Follow` ➔ `TCP Stream`。
    3. 在彈出的追蹤串流對話框中直接讀取明文傳輸的 `picoCTF{...}`。

---

### 2. shark on wire 1 (CyLab ID: 30)
- **平台與年份**：picoCTF 2019 ｜ Forensics ｜ Medium (150 pts)
- **官方傳送門**：[前往 CyLab 題目庫](https://learn.cylabacademy.org/library?search=shark%20on%20wire%201)
- **實戰情境**：包含數百個 UDP 封包的流量側錄檔 `capture.pcap`，內含大量干擾串流。
- **解題核心觀念**：
  - 真實網路環境充滿背景雜訊與虛假字串，需要學會逐一分離與過濾傳輸會話。
  - **Wireshark 核心操作**：
    1. 使用顯示過濾器 `udp` 過濾所有 UDP 封包。
    2. 點擊 `Follow` ➔ `UDP Stream`。
    3. 在視窗右下角依序切換串流編號（`Stream 0`, `Stream 1`, `Stream 2` ...），在特定串流中過濾掉假 Flag 並找到真實 Flag。

---

### 3. Wireshark doo dooo do doo... (CyLab ID: 115)
- **平台與年份**：picoCTF 2021 ｜ Forensics ｜ Medium (50 pts)
- **官方傳送門**：[前往 CyLab 題目庫](https://learn.cylabacademy.org/library?search=Wireshark%20doo%20dooo%20do%20doo...)
- **實戰情境**：邊界 IDS 側錄到可疑通訊 `shark.pcap`，流量中包含經編碼傳輸的文字。
- **解題核心觀念**：
  - 攻擊者經常在通訊時使用簡易混淆手段逃避特徵檢測。
  - **Wireshark 核心操作**：
    1. 使用顯示過濾器 `http` 或 `tcp contains "cvpb"`（預先計算 Flag 前綴經 ROT13 的特徵）。
    2. 追蹤該 TCP 串流，發現內容為一段似懂非懂的文字 `cvpbPGS{...}`。
    3. 將字串透過 CyberChef 或 Python 執行 **ROT13** 解碼還原 `picoCTF{...}`。

---

### 4. Wireshark twoo twooo two twoo... (CyLab ID: 110)
- **平台與年份**：picoCTF 2021 ｜ Forensics ｜ Medium (100 pts)
- **官方傳送門**：[前往 CyLab 題目庫](https://learn.cylabacademy.org/library?search=Wireshark%20twoo%20twooo%20two%20twoo...)
- **實戰情境**：流量中出現大量異常的 DNS 查詢請求。
- **解題核心觀念**：
  - 惡意程式利用 DNS 協議攜帶外洩資料（DNS Tunneling）。
  - **Wireshark 核心操作**：
    1. 輸入過濾器 `dns && dns.flags.response == 0` 查看所有發出的 DNS 查詢。
    2. 發現大量子域名格式呈現為 Base64 字串（如 `xxx.redshrimp.com`）。
    3. 依序提取所有子域名片斷，拼接後進行 Base64 解碼得到 Flag。

---

### 5. shark on wire 2 (CyLab ID: 84)
- **平台與年份**：picoCTF 2019 ｜ Forensics ｜ Medium (300 pts)
- **官方傳送門**：[前往 CyLab 題目庫](https://learn.cylabacademy.org/library?search=shark%20on%20wire%202)
- **實戰情境**：極端隱蔽的資料外洩流量 `capture.pcap`。
- **解題核心觀念**：
  - 隱蔽通道（Covert Channel）不使用 Payload 夾帶資料，而是利用通訊協定標頭欄位（如通訊埠號）。
  - **Wireshark 核心操作**：
    1. 觀察 UDP 封包的目的通訊埠（Destination Port），發現有一系列封包目的埠落在 `5000` 以上且持續微幅跳動（例如 5065, 5073, 5066...）。
    2. 扣除基底 `5000` 後得到數字 `65, 73, 66...`，恰好對應 ASCII 碼的字元 `'A', 'I', 'B'...`。
    3. 使用 Python `scapy` 撰寫自動化腳本提取端口並轉換：
       ```python
       from scapy.all import rdpcap, UDP
       packets = rdpcap("capture.pcap")
       flag = "".join(chr(p[UDP].dport - 5000) for p in packets if p.haslayer(UDP) and 5000 < p[UDP].dport < 5255)
       print(flag)
       ```

---

### 6. WebNet0 (CyLab ID: 32)
- **平台與年份**：picoCTF 2019 ｜ Forensics ｜ Hard (350 pts)
- **官方傳送門**：[前往 CyLab 題目庫](https://learn.cylabacademy.org/library?search=WebNet0)
- **實戰情境**：提供一個 TLS 加密的 PCAP 檔案與伺服器私鑰 `picoca.key`。
- **解題核心觀念**：
  - 掌握 Wireshark 載入 RSA 私鑰解密 HTTPS 流量的標準流程。
  - **Wireshark 核心操作**：
    1. 進入 `Edit` ➔ `Preferences` ➔ `Protocols` ➔ `TLS`。
    2. 在 `RSA keys list` 點擊 `Edit...`。
    3. 新增條目：IP 位址填伺服器 IP，Port 填 `443`，Protocol 填 `http`，Key File 選取 `picoca.key`。
    4. 確定後原本加密的 TLS 流量將即時解密為明文 HTTP。
    5. 過濾 `http` 請求，在 HTTP Response Header 中找到 Flag。

---

### 7. WebNet1 (CyLab ID: 42)
- **平台與年份**：picoCTF 2019 ｜ Forensics ｜ Hard (450 pts)
- **官方傳送門**：[前往 CyLab 題目庫](https://learn.cylabacademy.org/library?search=WebNet1)
- **實戰情境**：同 WebNet0，但 Flag 沒有直接顯示於 HTTP 標頭，而是藏於傳輸的附檔與圖片中。
- **解題核心觀念**：
  - HTTPS 密文解密後的深層物件提取（Export Objects）與圖片隱寫。
  - **Wireshark 核心操作**：
    1. 載入私鑰解密 TLS 流量。
    2. 點擊 `File` ➔ `Export Objects` ➔ `HTTP`。
    3. 將所有網頁物件導出至硬碟。
    4. 使用 `strings` 或十六進位檢視器分析導出的圖片檔案（如 `vulture.jpg`），提取藏於其中的 Flag。

---

### 8. PcapPoisoning (CyLab ID: 362)
- **平台與年份**：picoCTF 2023 ｜ Forensics ｜ Medium (100 pts)
- **官方傳送門**：[前往 CyLab 題目庫](https://learn.cylabacademy.org/library?search=PcapPoisoning)
- **實戰情境**：封包中塞入了大量混淆特徵的投毒數據。
- **解題核心觀念**：
  - 高效文字搜尋與封包結構驗證。
  - **Wireshark 核心操作**：
    1. 使用快捷鍵 `Ctrl + F` 開啟搜尋欄。
    2. 搜尋類型切換為 `String`，搜尋範圍選擇 `Packet bytes`。
    3. 輸入 `picoCTF` 進行全量匹配，迅速定位出唯一有效的真實封包。

---

### 9. Trivial Flag Transfer Protocol (CyLab ID: 434)
- **平台與年份**：picoCTF 2021 ｜ Forensics ｜ Medium (90 pts)
- **官方傳送門**：[前往 CyLab 題目庫](https://learn.cylabacademy.org/library?search=Trivial%20Flag%20Transfer%20Protocol)
- **實戰情境**：網路中進行了一連串 TFTP（輕量型檔案傳輸協定）通訊。
- **解題核心觀念**：
  - UDP 69 埠 TFTP 協定剖析與傳輸檔案組合分析。
  - **Wireshark 核心操作**：
    1. 點擊 `File` ➔ `Export Objects` ➔ `TFTP`。
    2. 導出所有傳輸檔案（包含 `instructions.txt`, `plan`, `program.deb`, `picture1.bmp` 等）。
    3. 閱讀指示文本進行古典密碼解密，並分析導出的 BMP 圖片取得 Flag。
