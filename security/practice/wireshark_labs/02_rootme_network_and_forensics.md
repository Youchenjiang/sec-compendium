# 🌐 模組 02：Root-Me 官方網路協定與封包取證挑戰目錄

> **資料來源**：[`rootme_all_challenges_catalog.md`](../challenges/platforms/rootme/rootme_all_challenges_catalog.md)  
> **官方入口**：[Root-Me Challenges](https://www.root-me.org/en/Challenges/)  
> **核心特色**：以真實 RFC 網路協定實作為背景，每道題目均提供標準 `.pcap` 檔案供 Wireshark 鑑識。

---

## 📌 第一部分：Network 分類（30 道核心協定分析關卡）

### 1. 明文與認證傳輸分析 (Authentication & Cleartext Protocols)
| ID | 題目名稱 | 官方連結 | 考察協定與 Wireshark 鑑識重點 |
| :---: | :--- | :--- | :--- |
| **97** | **FTP - authentication** | [傳送門](https://www.root-me.org/en/Challenges/Network/FTP-authentication) | 監聽 FTP 控制通道 (TCP 21)，過濾 `ftp` 追蹤明文 `USER` 與 `PASS`。 |
| **99** | **TELNET - authentication** | [傳送門](https://www.root-me.org/en/Challenges/Network/TELNET-authentication) | 追蹤 Telnet (TCP 23) 串流，拼接逐字元回顯（Echo）組裝登入密碼。 |
| **101** | **Twitter authentication** | [傳送門](https://www.root-me.org/en/Challenges/Network/Twitter-authentication) | 分析 HTTP 標頭 `Authorization: Basic <base64>` 並進行還原。 |
| **103** | **SIP - authentication** | [傳送門](https://www.root-me.org/en/Challenges/Network/SIP-authentication) | VoIP SIP 協定 Digest 認證計算（Realm, Nonce, Response Hash）。 |
| **197** | **XMPP - authentication** | [傳送門](https://www.root-me.org/en/Challenges/Network/XMPP-authentication) | 即時通訊 XMPP XML 串流中的 SASL PLAIN / DIGEST-MD5 認證結構。 |
| **346** | **LDAP - null bind** | [傳送門](https://www.root-me.org/en/Challenges/Network/LDAP-null-bind) | 剖析 LDAP (TCP 389) 匿名查詢與目錄樹屬性（`sAMAccountName` 等）。 |
| **361** | **CISCO - password** | [傳送門](https://www.root-me.org/en/Challenges/Network/CISCO-password) | 捕捉 Cisco 設備組態或連線流量，解密 Cisco Type 7 / Type 5 密碼。 |
| **424** | **SNMP - Authentification** | [傳送門](https://www.root-me.org/en/Challenges/Network/SNMP-Authentification) | 提取 UDP 161 SNMPv1/v2c 明文社群字串（Community String）。 |
| **2375**| **POP - APOP** | [傳送門](https://www.root-me.org/en/Challenges/Network/POP-APOP) | 郵件協定 APOP MD5 時間戳與密碼碰撞驗證。 |

---

### 2. 密碼學與加密通訊解構 (TLS / Cryptographic Exchanges)
| ID | 題目名稱 | 官方連結 | 考察協定與 Wireshark 鑑識重點 |
| :---: | :--- | :--- | :--- |
| **105** | **SSL - HTTP exchange** | [傳送門](https://www.root-me.org/en/Challenges/Network/SSL-HTTP-exchange) | 載入題目給予的私鑰檔案至 TLS 協定選單，解密 HTTPS 會話。 |
| **274** | **Wired Equivalent Privacy** | [傳送門](https://www.root-me.org/en/Challenges/Network/Wired-Equivalent-Privacy) | 802.11 無線網路 WEP RC4 脆弱 IV 收集與 Aircrack-ng / Wireshark 解密。 |
| **4667**| **WPA2 - Enterprise** | [傳送門](https://www.root-me.org/en/Challenges/Network/WPA2-Enterprise) | 802.1X RADIUS / EAP-PEAP 認證過程 MSCHAPv2 握手鑑識。 |
| **4668**| **WPA3 - SAE** | [傳送門](https://www.root-me.org/en/Challenges/Network/WPA3-SAE) | WPA3 Simultaneous Authentication of Equals (Dragonfly 握手) 封包分析。 |

---

### 3. 底層網路層與隱蔽通訊 (L2/L3 Protocols & Covert Channels)
| ID | 題目名稱 | 官方連結 | 考察協定與 Wireshark 鑑識重點 |
| :---: | :--- | :--- | :--- |
| **107** | **ICMP payload** | [傳送門](https://www.root-me.org/en/Challenges/Network/ICMP-payload) | 過濾 `icmp.type == 8`，提取 Echo Request Data 區塊中的隱寫位元組。 |
| **109** | **IP - Time To Live** | [傳送門](https://www.root-me.org/en/Challenges/Network/IP-Time-To-Live) | 觀察 IP 標頭 `ip.ttl` 數值變動，提取利用 TTL 編碼的二進位字串。 |
| **338** | **ETHERNET - frame** | [傳送門](https://www.root-me.org/en/Challenges/Network/ETHERNET-frame) | 分析底層乙太網訊框格式、Preamble、Type 欄位與 FCS 幀校驗。 |
| **348** | **ETHERNET - Patched transmission** | [傳送門](https://www.root-me.org/en/Challenges/Network/ETHERNET-Patched-transmission) | 識別被惡意改寫或損壞的訊框結構並重組。 |
| **340** | **DNS - zone transfert** | [傳送門](https://www.root-me.org/en/Challenges/Network/DNS-zone-transfert) | 提取 DNS AXFR (Type 252) 回應封包中完整洩漏的網域名稱記錄。 |
| **2348**| **HTTP - DNS Rebinding** | [傳送門](https://www.root-me.org/en/Challenges/Network/HTTP-DNS-Rebinding) | 分析 DNS TTL=0 造成的短時間 IP 跳轉（攻擊 127.0.0.1 內網）。 |
| **2362**| **RIPv1 - no authentication** | [傳送門](https://www.root-me.org/en/Challenges/Network/RIPv1-no-authentication) | 路由資訊協定 RIPv1 無認證缺陷與路由表廣播。 |
| **4260**| **ARP Spoofing - Active listening**| [傳送門](https://www.root-me.org/en/Challenges/Network/ARP-Spoofing-Active-listening) | 識別區域網路中 Gratuitous ARP 偽造與 IP-MAC 映射衝突。 |
| **4261**| **ARP Spoofing - The MITM** | [傳送門](https://www.root-me.org/en/Challenges/Network/ARP-Spoofing-The-man-in-the-middle) | 中間人雙向轉發流量分析與被竊取的敏感資訊重組。 |

---

### 4. 企業 Windows 網域協定 (Active Directory Network Forensics)
| ID | 題目名稱 | 官方連結 | 考察協定與 Wireshark 鑑識重點 |
| :---: | :--- | :--- | :--- |
| **4664**| **NTLM - Authentication** | [傳送門](https://www.root-me.org/en/Challenges/Network/NTLM-Authentication) | 提取 NTLMSSP 協商、Challenge 與 Response，組裝 NetNTLM Hash。 |
| **4665**| **Kerberos - Authentication** | [傳送門](https://www.root-me.org/en/Challenges/Network/Kerberos-Authentication) | 分析 Kerberos (TCP/UDP 88) 流量：AS-REQ, AS-REP, TGS-REQ 票據傳輸。 |
| **4666**| **Data extraction** | [傳送門](https://www.root-me.org/en/Challenges/Network/Data-extraction) | 使用 Wireshark `Export Objects` 功能完整還原封包中的被竊取檔案。 |

---

## 📌 第二部分：Forensic 分類（惡意流量與 C2 取證題目）

| ID | 題目名稱 | 官方連結 | 考察協定與 Wireshark 鑑識重點 |
| :---: | :--- | :--- | :--- |
| **313~317** | **Command & Control (Level 2 ~ 6)** | [傳送門](https://www.root-me.org/en/Challenges/Forensic/Command-and-Control-level-2) | 逐步進階分析木馬 C2 架構：從明文心跳到自訂協定、RSA 加密交握與命令執行。 |
| **1649**| **DNS exfiltration** | [傳送門](https://www.root-me.org/en/Challenges/Forensic/DNS-exfiltration) | 大規模 DNS Tunneling 流量分析，提取 Hex/Base32 分片並合併還原原始二進位。 |
| **4307**| **C2 Mythic** | [傳送門](https://www.root-me.org/en/Challenges/Forensic/C2-Mythic) | 現代紅隊開源 C2 框架 Mythic 的 WebSocket 與 HTTP Payload 取證。 |
| **4964**| **ICMP exfiltration** | [傳送門](https://www.root-me.org/en/Challenges/Forensic/ICMP-exfiltration) | 分析非標準 ICMP 回顯負載中的長篇外洩資料。 |
