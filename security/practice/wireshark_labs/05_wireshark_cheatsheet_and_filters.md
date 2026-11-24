# ⚡ 模組 05：Wireshark 高階過濾語法與 Tshark 指令速查

> **用途**：供解題時快速複製貼上高頻 Display Filters 與 Tshark 萃取命令。

---

## 🔍 第一部分：Wireshark 常用顯示過濾器 (Display Filters)

### 1. TCP 狀態機與異常排查
```text
# 找出半開連線 (SYN Flood 或連接埠掃描特徵)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# 找出連線被主動重設 (RST 阻斷或 Port Closed)
tcp.flags.reset == 1

# 找出包含特定字串的 TCP 流量 (如 flag{)
tcp contains "flag{"

# 找出特定重傳與視窗滿載警告
tcp.analysis.retransmission || tcp.analysis.zero_window
```

### 2. HTTP Web 攻擊分析
```text
# 篩選所有 HTTP POST 請求
http.request.method == "POST"

# 篩選 HTTP 回應代碼為 404 (目錄爆破特徵)
http.response.code == 404

# 篩選 HTTP 請求內容包含密碼或特定參數
http contains "password" || http contains "admin"

# 篩選出攜帶檔案上傳 (multipart/form-data) 的請求
http.content_type contains "multipart"
```

### 3. DNS 查詢與隱蔽通道 (DNS Tunneling)
```text
# 僅顯示所有 DNS 查詢請求 (排除回應)
dns.flags.response == 0

# 顯示特定網域名稱查詢
dns.qry.name contains "malware" || dns.qry.name contains "sync-cdn"

# 顯示所有查詢不存在的域名 (NXDOMAIN 錯誤，常用於 DGA 惡意軟體)
dns.flags.rcode == 3

# 顯示 TXT 記錄查詢 (常用於隱蔽資料傳輸)
dns.qry.type == 16
```

### 4. 身份認證與明文協定
```text
# FTP 認證命令
ftp.request.command == "USER" || ftp.request.command == "PASS"

# Telnet 資料流
telnet

# ICMP 請求與非標準負載
icmp.type == 8 && data.len > 64

# ARP 衝突與欺騙
arp.duplicate-address-detected || arp.opcode == 2
```

---

## 💻 第二部分：Tshark 命令列高效提取指令集

### 1. 快速提取 DNS 查詢列表並去重統計
```bash
tshark -r capture.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name | sort | uniq -c | sort -nr | head -n 30
```

### 2. 提取所有 HTTP 請求來源 IP、Host 與 URI
```bash
tshark -r capture.pcap -Y 'http.request' -T fields -e ip.src -e http.host -e http.request.uri
```

### 3. 自動將 PCAP 中的所有 HTTP 傳輸檔案導出至資料夾
```bash
tshark -r capture.pcap --export-objects "http,./extracted_files"
```

### 4. 統計所有 IP 通訊會話（Conversations）
```bash
tshark -r capture.pcap -q -z conv,ip
```

### 5. 提取 TLS SNI 伺服器名稱（識別訪問之 HTTPS 網站）
```bash
tshark -r capture.pcap -Y 'tls.handshake.extension.type == 0' -T fields -e ip.dst -e tls.handshake.extensions_server_name | sort -u
```
