# ⚡ 網路安全實務速查表 (Network Security Cheatsheet)

本速查表聚焦於**網路安全維運、流量分析、攻防測試與服務硬化**常用之指令與配置，強調實戰複製即用。

---

## 📋 目錄

1. [🛠️ 網路掃描與探測 (Nmap)](#️-網路掃描與探測-nmap)
2. [🦈 封包擷取與流量分析 (tcpdump & Wireshark)](#-封包擷取與流量分析-tcpdump--wireshark)
3. [🔒 SSL / TLS 憑證與連線排查 (OpenSSL)](#-ssl--tls-憑證與連線排查-openssl)
4. [🛡️ 防火牆與網路邊界硬化 (IPTables / UFW / Nginx)](#️-防火牆與網路邊界硬化-iptables--ufw--nginx)
5. [🔑 SSH 安全硬化與隧道 (SSH Security & Tunnels)](#-ssh-安全硬化與隧道-ssh-security--tunnels)
6. [🌐 Web 網路表頭與連線測試 (curl & Security Headers)](#-web-網路表頭與連線測試-curl--security-headers)

---

## 🛠️ 1. 網路掃描與探測 (Nmap)

### 常用組合指令

| 用途 | 指令 | 說明 |
| :--- | :--- | :--- |
| **快速主機存活確認** | `nmap -sn 192.168.1.0/24` | Ping Scan，不掃描 Port |
| **快速全 Port 探測** | `nmap -p- --min-rate 2000 10.10.10.1` | 加速掃描全 65535 Port |
| **標準服務與 OS 辨識** | `nmap -sCV -O 10.10.10.1` | `-sC` 預設腳本 + `-sV` 版本 + `-O` 作業系統 |
| **UDP 服務掃描** | `nmap -sU --top-ports 50 10.10.10.1` | 掃描前 50 個常用 UDP 埠 |
| **漏洞檢測腳本** | `nmap --script vuln 10.10.10.1` | 執行常見 CVE 漏洞檢測腳本 |

### 常用 NSE 腳本範例
```bash
# 檢查 SSL/TLS 支援的 Cipher Suite
nmap --script ssl-enum-ciphers -p 443 192.168.1.100

# 檢測 SMB 漏洞 (如 EternalBlue / MS17-010)
nmap -p 445 --script smb-vuln-ms17-010 192.168.1.0/24

# 檢測 HTTP 常用敏感目錄
nmap --script http-enum -p 80,443 192.168.1.100
```

---

## 🦈 2. 封包擷取與流量分析 (tcpdump & Wireshark)

### tcpdump 抓包速查

```bash
# 1. 抓取特定介面的流量並寫入 pcap 檔
tcpdump -i eth0 -w capture.pcap

# 2. 指定 IP 與 Port（過濾來自 192.168.1.50 的 80/443 流量）
tcpdump -i eth0 "host 192.168.1.50 and (port 80 or port 443)"

# 3. 抓取包含 SYN 標籤的封包 (觀察連線建立/掃描)
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'

# 4. 印出 ASCII 可讀內文 (適合排查明文 HTTP/DNS 流量)
tcpdump -i eth0 -A -s 0 'port 80'
```

### Wireshark 顯示過濾器 (Display Filters)

| 目的 | 過濾器語法 |
| :--- | :--- |
| **指定特定 IP** | `ip.addr == 192.168.1.1` 或 `ip.src == 10.0.0.1` |
| **指定 TCP/UDP Port** | `tcp.port == 443` 或 `udp.port == 53` |
| **HTTP 請求方法與狀態碼** | `http.request.method == "POST"` / `http.response.status_code == 404` |
| **TLS 握手與 Client Hello** | `tls.handshake.type == 1` |
| **DNS 查詢過濾** | `dns.qd.name contains "malicious"` |
| **TCP 重傳 / 異常封包** | `tcp.analysis.flags` 或 `tcp.analysis.retransmission` |

---

## 🔒 3. SSL / TLS 憑證與連線排查 (OpenSSL)

```bash
# 1. 測試與目標伺服器的 TLS 連線並列出完整憑證鏈
openssl s_client -connect example.com:443 -servername example.com

# 2. 檢查伺服器支援的 TLS 版本 (測試是否支援古老 TLS 1.0)
openssl s_client -connect example.com:443 -tls1_0

# 3. 檢查本地 .crt / .pem 憑證內容與有效期限
openssl x509 -in cert.crt -text -noout

# 4. 檢查 .csr (憑證簽署請求) 內容
openssl req -in request.csr -text -noout

# 5. 計算憑證與私鑰的 MD5 Hash (比對兩者是否匹配)
openssl x509 -noout -modulus -in cert.crt | openssl md5
openssl rsa -noout -modulus -in private.key | openssl md5
```

---

## 🛡️ 4. 防火牆與網路邊界硬化 (IPTables / UFW / Nginx)

### IPTables 防禦規則速查

```bash
# 封鎖指定可疑 IP
iptables -A INPUT -s 192.168.1.50 -j DROP

# 限制特定 Port 的連線速率 (防範 SSH 暴力破解)
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 -j DROP

# 儲存與復原 iptables 規則
iptables-save > /etc/iptables/rules.v4
iptables-restore < /etc/iptables/rules.v4
```

### UFW 防火牆常用指令

```bash
ufw enable                        # 啟動防火牆
ufw default deny incoming         # 預設阻擋所有進站
ufw default allow outgoing        # 預設允許所有出站
ufw allow 22/tcp                  # 開放 SSH 埠
ufw allow from 192.168.1.0/24 to any port 80  # 僅允許特定子網存取 80
ufw status verbose                # 檢視詳細狀態
```

### Nginx 安全 Header 配置 (`nginx.conf`)

```nginx
# 啟用基本資安標頭
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

---

## 🔑 5. SSH 安全硬化與隧道 (SSH Security & Tunnels)

### `/etc/ssh/sshd_config` 安全硬化必設項目

```ini
Port 2222                  # 更改預設 Port (降低盲目掃描風險)
PermitRootLogin no         # 禁用 Root 直接登入
PasswordAuthentication no  # 禁用密碼登入 (強制金鑰認證)
MaxAuthTries 3             # 降低單次連線嘗試次數
AllowUsers admin devuser   # 僅允許特定白名單帳號登入
```

### SSH 轉發與隧道指令

```bash
# 1. 本地 Port 轉發 (Local Port Forwarding)
# 將本地 8080 埠轉發至目標內網 192.168.1.10:80
ssh -L 8080:192.168.1.10:80 user@remote-jump-server -N

# 2. 動態 SOCKS 代理隧道 (Dynamic SOCKS Proxy)
# 本地 1080 Port 作為 SOCKS5 代理
ssh -D 1080 user@remote-jump-server -N
```

---

## 🌐 6. Web 網路表頭與連線測試 (curl & Security Headers)

### curl 網路測試與排錯指令

```bash
# 1. 檢視 HTTP 請求與回應詳細標頭 (不抓取 Body)
curl -I -v https://example.com

# 2. 測試追蹤重導向 (Follow Redirects)
curl -L -v http://example.com

# 3. 指定 Header 與 User-Agent 測試
curl -H "User-Agent: Mozilla/5.0" -H "X-Forwarded-For: 127.0.0.1" https://example.com

# 4. 測量 HTTP 響應時間詳細指標
curl -w "\nDNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTLS Handshake: %{time_appconnect}s\nTotal: %{time_total}s\n" -o /dev/null -s https://example.com
```

### 關鍵安全 Header 意義卡片

| Header 標頭 | 作用與防範漏洞 |
| :--- | :--- |
| **Strict-Transport-Security (HSTS)** | 強制瀏覽器使用 HTTPS，防止 SSL Strip 降級攻擊 |
| **Content-Security-Policy (CSP)** | 限制載入資源來源與腳本執行，核心防範 XSS 攻擊 |
| **X-Frame-Options** | 控制網頁是否可於 `<iframe` 內嵌，防範 Clickjacking (點擊劫持) |
| **X-Content-Type-Options** | 設為 `nosniff` 防止瀏覽器 MIME-sniffing 誤導弱點 |
