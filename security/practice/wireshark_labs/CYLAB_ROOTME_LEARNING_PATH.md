# 🦈 CyLab + Root-Me 雙平台 Wireshark 100% 免費終極實戰學習路徑
## ——從「CTF 找 Flag 玩具思維」蛻變為「真實企業資安鑑識與維運防衛」

> **設計核心**：完全摒棄付費平台限制，精選 **CMU CyLab (picoCTF)** 與 **Root-Me** 兩大 100% 免費優質靶場，組成由淺入深的 6 個進階階段。  
> **重大導讀**：在真實世界中，**沒有任何攻擊者會在封包裡留下一串 `flag{...}` 等你複製貼上**。本指南為每一個實驗關卡注入**【企業真實案發現場】**、**【封包解剖思維】**、**【Wireshark 調查 SOP】**與**【藍隊防禦工程處置】**，讓你在完成每道題目時，真正掌握可直接應用於工作與履歷的專業鑑識技能。

---

## 🗺️ 學習進階總覽

```
[Phase 1: 基礎嗅探與明文憑證] ──► [Phase 2: 雜訊過濾與物件導出] ──► [Phase 3: TLS 解密與網域認證]
    • Follow Stream 串流重組        • Display Filter 複合查詢        • RSA 私鑰解密 HTTPS
    • HTTP / FTP / Telnet 鑑識      • Export Objects 導出檔案       • NTLM / Kerberos 票據
                                                                               │
[Phase 6: 隱蔽通道與 C2 取證] ◄── [Phase 5: 無線網路協定安全] ◄── [Phase 4: 網路層欺騙與協定缺陷]
    • DNS / ICMP Tunneling          • WEP IV 碰撞分析                • ARP 欺騙與 MITM 重組
    • UDP Port / TTL 隱寫           • WPA2 Enterprise (EAP)          • DNS 區域傳送與 Rebinding
    • Botnet C2 惡意流量分析        • WPA3 Dragonfly 握手協定        • 路由協定廣播欺騙
```

---

## 🏁 Phase 1：基礎封包嗅探與明文憑證提取 (Sniffing & Cleartext Protocols)

### 📌 階段任務定位
- **CTF 表象**：點右鍵 Follow Stream 複製明文 Flag。
- **🌟 現實本質**：**【內網通訊安全盤點與合規稽查】**。證明「只要攻擊者滲透進企業內網，員工在老舊系統中打的所有帳號、密碼與未加密機密，在網線上全部形同裸奔（CWE-319）」。

---

#### 1-1. Packets Primer (CyLab ID: 286)
- **平台連結**：[CyLab 傳送門](https://learn.cylabacademy.org/library?search=Packets%20Primer)
- 🚨 **企業真實案發現場**：
  公司內部防外洩系統（DLP）發出告警，指稱某台開發伺服器有異常資料往外傳輸，分析師在核心交換器側錄到一段未知的 TCP 流量 `packets.pcap`。
- 🔬 **封包解剖思維（現場看到什麼）**：
  封包列表中充斥著碎片化的 ACK、PSH 訊框。你點擊 `Follow` ➔ `TCP Stream`，Wireshark 的底層重組引擎依據 Sequence/Acknowledgment 序號將碎裂的封包拼裝成人類讀得懂的會話。你在裡面看到的不是無意義文字，而是**應用層未經任何防護的明文外洩資料**。
- 🛠️ **分析師實戰 SOP**：
  1. 在封包列表任意 TCP 封包按右鍵 ➔ `Follow` ➔ `TCP Stream`。
  2. 觀察 Client（紅字）與 Server（藍字）的明文溝通結構。
- 🛡️ **藍隊防禦與工程加固**：
  在伺服器端強制啟用 TLS 加密；於 Web 伺服器配置 HTTP 嚴格傳輸安全標頭（`Strict-Transport-Security: max-age=31536000; includeSubDomains`），徹底杜絕明文通訊。
- 💡 **通關復盤提問**：
  *如果一個封包在傳輸途中掉了（Packet Loss），TCP 的 Sequence Number 是如何確保 Wireshark 依然能正確還原整篇文章順序的？*

---

#### 1-2 & 1-3. FTP - authentication (Root-Me 97) & TELNET - authentication (Root-Me 99)
- **平台連結**：[Root-Me FTP (97)](https://www.root-me.org/en/Challenges/Network/FTP-authentication) ｜ [Root-Me TELNET (99)](https://www.root-me.org/en/Challenges/Network/TELNET-authentication)
- 🚨 **企業真實案發現場**：
  資安顧問進行內部紅隊演練時，監聽到某位網管人員偷懶使用老舊協定連線至核心路由器與檔案伺服器進行維護。
- 🔬 **封包解剖思維（現場看到什麼）**：
  - **FTP**：控制通道（TCP 21）直接明文出現 `USER admin` 與 `PASS P@ssw0rd123`。
  - **Telnet**：TCP 23 終端會話中，每當使用者敲下鍵盤的一個字元，伺服器就會回彈一個字元（Character Echo），你在串流中必須將每個字元拼湊還原出完整的管理員密碼。
- 🛠️ **分析師實戰 SOP**：
  - FTP 過濾：`ftp.request.command == "USER" || ftp.request.command == "PASS"`
  - Telnet 串流：過濾 `telnet` ➔ 右鍵 `Follow TCP Stream`。
- 🛡️ **藍隊防禦與工程加固**：
  全面淘汰明文協定：停用系統中的 `vsftpd` 與 `telnetd` 守護行程，強制改用具備 SSH 加密的 **SFTP (TCP 22)** 與 **OpenSSH**；並在內部防火牆阻斷 21 與 23 連接埠。

---

#### 1-4. Twitter authentication (Root-Me 101)
- **平台連結**：[Root-Me 傳送門](https://www.root-me.org/en/Challenges/Network/Twitter-authentication)
- 🚨 **企業真實案發現場**：
  開發團隊宣稱「我們的 API 已經加密認證過了，很安全」，但安全審查時發現只是自欺欺人的「偽加密」。
- 🔬 **封包解剖思維（現場看到什麼）**：
  封包標頭出現 `Authorization: Basic dXNlcjpwYXNzd29yZA==`。**Base64 只是資料編碼（Encoding），根本不是加密（Encryption）！** 任何攔截到封包的人只要 0.1 秒就能逆向還原帳密。
- 🛠️ **分析師實戰 SOP**：
  過濾 `http.authorization`，複製 `Basic` 後方的字串，在 Linux 終端執行 `echo "字串" | base64 -d` 還原。
- 🛡️ **藍隊防禦與工程加固**：
  全面廢棄 HTTP Basic Authentication，換裝現代化 OAuth 2.0 / OpenID Connect (OIDC) 搭配短期有效期的 Bearer JWT Token，且必須強制綁定 HTTPS 傳輸。

---

#### 1-5. shark on wire 1 (CyLab ID: 30)
- **平台連結**：[CyLab 傳送門](https://learn.cylabacademy.org/library?search=shark%20on%20wire%201)
- 🚨 **企業真實案發現場**：
  內網存在多個微服務與廣播程式，同時產生海量的 UDP 串流與假訊號。分析師接獲通報其中隱藏著被惡意竊取的一小段機密，如何在幾百條對話中不迷失？
- 🔬 **封包解剖思維（現場看到什麼）**：
  UDP 是無連線的，但 Wireshark 會利用 **四元組（來源IP:Port ↔ 目的IP:Port）** 自動把相近時間的封包歸類為同一個「UDP Stream」。如果只看封包清單會眼花撩亂，必須利用串流索引切換進行排查。
- 🛠️ **分析師實戰 SOP**：
  1. 輸入顯示過濾器 `udp`。
  2. 選擇任一封包右鍵 ➔ `Follow` ➔ `UDP Stream`。
  3. 在對話框右下角點擊箭頭或直接輸入串流編號（`Stream 0`, `Stream 1`, `Stream 6` ...），逐一比對每個通訊會話的 Payload 內容。
- 🛡️ **藍隊防禦與工程加固**：
  在內網落實微隔離（Micro-segmentation），非必要之 UDP 廣播或未知 UDP 連接埠應在主機防火牆（iptables / Windows Firewall）預設丟棄（Default Deny）。

---

#### 1-6. ETHERNET - frame (Root-Me 338)
- **平台連結**：[Root-Me 傳送門](https://www.root-me.org/en/Challenges/Network/ETHERNET-frame)
- 🚨 **企業真實案發現場**：
  底層二層網路發生異常通訊，資料鏈結層的封包損毀或出現異常 MAC 位址偽造。
- 🔬 **封包解剖思維（現場看到什麼）**：
  脫離 IP 與 TCP 視角，將顯微鏡對準最底層的 **乙太網訊框（Ethernet Frame II）**：前 6 bytes 目的 MAC、後 6 bytes 來源 MAC、2 bytes Type/Length（如 `0x0800` 代表 IPv4、`0x0806` 代表 ARP）以及最後的 FCS 訊框校驗碼。
- 🛠️ **分析師實戰 SOP**：
  在 Wireshark 展開最上層的 `Ethernet II` 樹狀目錄，檢視十六進位原始 Hex 結構。
- 🛡️ **藍隊防禦與工程加固**：
  在企業接入交換器開啟 **Port Security**，限制單一實體連接埠僅允許特定 MAC 位址連線，違反時自動關閉埠位（err-disable）。

---

## 🔍 Phase 2：雜訊過濾、編碼混淆與物件導出 (Filters & Object Extraction)

### 📌 階段任務定位
- **CTF 表象**：過濾特定字元、導出 TFTP 檔案、找藏在圖片裡的字串。
- **🌟 現實本質**：**【釣魚信件攻擊鏈與惡意下載還原】**。員工點了釣魚信或惡意連結，防毒軟體沒有攔截。資安人員從側錄封包中，直接把受害者下載的惡意二進位檔案抽出來，送交沙箱逆向分析。

---

#### 2-1. Wireshark doo dooo do doo... (CyLab ID: 115)
- **平台連結**：[CyLab 傳送門](https://learn.cylabacademy.org/library?search=Wireshark%20doo%20dooo%20do%20doo...)
- 🚨 **企業真實案發現場**：
  入侵偵測系統（NIDS）攔截到通訊，但流量中的文字被攻擊者使用了簡單的替換式混淆，企圖躲避純字串特徵碼比對。
- 🔬 **封包解剖思維（現場看到什麼）**：
  攻擊者企圖發送機密資料，但在外發前做了 **ROT13（Caesar Cipher 位移 13 位元）**。在封包中你看到的是似懂非懂的亂碼，例如標準關鍵字被轉成了混淆特徵。
- 🛠️ **分析師實戰 SOP**：
  過濾 HTTP 流量 ➔ 追蹤串流 ➔ 提取混淆文字 ➔ 丟入 CyberChef 進行 `ROT13` 解密。
- 🛡️ **藍隊防禦與工程加固**：
  傳統基於精確字串比對的防禦（Signature-based）容易被簡易編碼擊潰；企業應部署支援深度封包檢測（DPI）與行為熵值（Entropy）異常檢測的次世代 IDS（Suricata / Zeek）。

---

#### 2-2. PcapPoisoning (CyLab ID: 362)
- **平台連結**：[CyLab 傳送門](https://learn.cylabacademy.org/library?search=PcapPoisoning)
- 🚨 **企業真實案發現場**：
  攻擊者在入侵時使用了 **Chaffing（干擾雜訊投毒）** 手法，同時發送成千上萬個偽造的封包，試圖製造海量假告警將 SOC 監控中心的分析人員淹沒。
- 🔬 **封包解剖思維（現場看到什麼）**：
  面對動輒數萬筆的 PCAP 封包，肉眼一筆筆點開是不可能的。分析人員必須學會使用底層十六進位字串匹配與特徵快速定位。
- 🛠️ **分析師實戰 SOP**：
  按快捷鍵 `Ctrl + F` ➔ 選擇搜尋類型為 `String` ➔ 搜尋範圍切換為 `Packet bytes` ➔ 全局檢索關鍵字或特徵碼。

---

#### 2-3 & 2-4. Data extraction (Root-Me 4666) & TFTP (CyLab 434)
- **平台連結**：[Root-Me (4666)](https://www.root-me.org/en/Challenges/Network/Data-extraction) ｜ [CyLab TFTP (434)](https://learn.cylabacademy.org/library?search=Trivial%20Flag%20Transfer%20Protocol)
- 🚨 **企業真實案發現場**：
  終端 EDR 顯示某台辦公室電腦被植入了惡意巨集，巨集從內網 TFTP/HTTP 伺服器下載了第二階段攻擊程式（Dropper）。電腦已被拔網線隔離，分析師手頭只有網路側錄檔。
- 🔬 **封包解剖思維（現場看到什麼）**：
  檔案在網路傳輸時，會被拆解成數百個連續的封包資料塊。你不需要手動複製每個封包的 Hex 再拼湊，Wireshark 具備強大的 **物件重建（Export Objects）** 功能，能自動重組檔案標頭、二進位資料並寫入磁碟。
- 🛠️ **分析師實戰 SOP**：
  1. 點擊頂部功能表 `File` ➔ `Export Objects` ➔ 選擇對應協定（`HTTP` 或 `TFTP`）。
  2. 視窗會列出封包中傳輸的所有檔案名稱（如 `payload.deb`, `picture.bmp`, `script.txt`）。
  3. 點擊 `Save All` 匯出至本地資料夾進行靜態分析或計算雜湊值（SHA-256）。
- 🛡️ **藍隊防禦與工程加固**：
  將導出的惡意檔案 Hash 匯入企業 EDR 系統進行全網威脅獵捕（Threat Hunting）；在防火牆封鎖 UDP 69（TFTP）跨網段連線，嚴禁內網主機隨意使用無認證的 TFTP。

---

#### 2-5. SNMP - Authentification (Root-Me 424)
- **平台連結**：[Root-Me 傳送門](https://www.root-me.org/en/Challenges/Network/SNMP-Authentification)
- 🚨 **企業真實案發現場**：
  機房交換器設定被神秘篡改，VLAN 配置全亂。網管宣稱設定有設密碼，資安人員在網段中抓包排查。
- 🔬 **封包解剖思維（現場看到什麼）**：
  SNMPv1 / v2c 協定使用明文的 **社群字串（Community String）** 當作認證。只要看到 `public`（常見預設唯讀）或 `private`（常見預設讀寫），任何人都可以在內網使用 `snmpset` 指令直接重設交換器組態。
- 🛠️ **分析師實戰 SOP**：
  過濾器輸入 `snmp`，展開 `Simple Network Management Protocol` ➔ 檢視 `community` 欄位文字。
- 🛡️ **藍隊防禦與工程加固**：
  徹底停用 SNMPv1 與 SNMPv2c，全面強制升級至 **SNMPv3 (`authPriv` 模式)**，此模式具備 HMAC-SHA 身份驗證與 AES-128/256 資料加密，即便封包被截獲也無法破解社群字串。

---

## 🔐 Phase 3：HTTPS / TLS 密鑰解密與企業身份驗證 (TLS Decryption & Auth)

### 📌 階段任務定位
- **CTF 表象**：把題目給的私鑰載入 Wireshark 解開密文看 Flag。
- **🌟 現實本質**：**【企業級 SSL 深層檢測 (SSL Inspection) 與網域橫向移動排查】**。現代 95% 流量皆為 HTTPS，惡意木馬也全都用 TLS 加密通訊。如果你不會解密，面對流量就是「全盲」；同時，本階段剖析企業 Active Directory 內網最核心的 NTLM 與 Kerberos 驗證。

---

#### 3-1, 3-2 & 3-3. SSL 解密系列 (Root-Me 105 / CyLab 32 WebNet0 / CyLab 42 WebNet1)
- **平台連結**：[Root-Me SSL (105)](https://www.root-me.org/en/Challenges/Network/SSL-HTTP-exchange) ｜ [CyLab WebNet0 (32)](https://learn.cylabacademy.org/library?search=WebNet0) ｜ [CyLab WebNet1 (42)](https://learn.cylabacademy.org/library?search=WebNet1)
- 🚨 **企業真實案發現場**：
  某內部網站疑似被植入 Webshell，但所有流量都走 HTTPS 443 加密。從外部看只有 TLS 握手與 Application Data，根本看不到攻擊者下了什麼指令。資安團隊調閱了伺服器的 SSL 私鑰或主機的 `SSLKEYLOGFILE`，要將流量全部還原成明文進行取證。
- 🔬 **封包解剖思維（現場看到什麼）**：
  未解密前，Wireshark 只會顯示一堆黑底灰字的 `TLSv1.2 / TLSv1.3 Application Data`。當你正確配置密鑰後，Wireshark 會即時在記憶體中進行對稱金鑰推導，封包列表下層會瞬間長出解密後的 **「Decrypted TLS」** 分頁，明文 HTTP 請求一覽無遺。
- 🛠️ **分析師實戰 SOP**：
  1. 進入 `Edit` ➔ `Preferences` ➔ `Protocols` ➔ `TLS`。
  2. 若有 RSA 私鑰：在 `RSA keys list` 點擊 `Edit`，填入 `IP`, `Port: 443`, `Protocol: http`, 載入 `.key` 檔案。
  3. 若有 Client Keylog：在 `(Pre)-Master-Secret log filename` 載入 `sslkeylog.txt`。
  4. 回到主視窗，過濾 `http` 即可直接追蹤解密後的 HTTP 串流！
- 🛡️ **藍隊防禦與工程加固**：
  在企業邊界部署次世代防火牆（NGFW）的 **SSL Forward Proxy（深層封包解密檢驗）**，透過企業自簽 CA 根憑證對出境流量進行即時解密，阻斷隱藏在 HTTPS 中的惡意 C2 通訊。

---

#### 3-6 & 3-7. NTLM (Root-Me 4664) & Kerberos Authentication (Root-Me 4665)
- **平台連結**：[Root-Me NTLM (4664)](https://www.root-me.org/en/Challenges/Network/NTLM-Authentication) ｜ [Root-Me Kerberos (4665)](https://www.root-me.org/en/Challenges/Network/Kerberos-Authentication)
- 🚨 **企業真實案發現場**：
  Active Directory (AD) 網域環境中發生了橫向移動攻擊（Lateral Movement）。攻擊者正在使用 Responder 進行 LLMNR 毒化竊取密碼雜湊，或者利用 Kerberoasting 請求高權限服務票據。
- 🔬 **封包解剖思維（現場看到什麼）**：
  - **NTLM 握手**：
    1. `Type 1 (Negotiate)`：客戶端請求認證。
    2. `Type 2 (Challenge)`：伺服器丟回一串 8-byte 隨機數（Server Challenge）。
    3. `Type 3 (Authenticate)`：客戶端使用使用者密碼計算出的加密回應（NTProofStr / Response Hash）。**這串東西就是駭客用 Hashcat 離線破解字典的來源！**
  - **Kerberos (Port 88)**：
    分析 `AS-REQ`（使用者認證請求）、`AS-REP`（KDC 回覆 TGT 票據）、`TGS-REQ`（請求特定伺服器服務票據）。
- 🛠️ **分析師實戰 SOP**：
  - 過濾 NTLM：`ntlmssp`
  - 過濾 Kerberos：`kerberos`
- 🛡️ **藍隊防禦與工程加固**：
  群組原則（GPO）強制禁用 NTLMv1，全面提升至 NTLMv2；進一步配置限制 NTLM 外發；啟用 **SMB 簽章（SMB Signing）** 徹底阻斷 NTLM 中繼攻擊（NTLM Relay）；將服務帳戶密碼長度提升至 25 字元以上防範 Kerberoasting 破解。

---

## ⚡ Phase 4：網路層欺騙與協定缺陷分析 (L2/L3 Spoofing & Anomalies)

### 📌 階段任務定位
- **CTF 表象**：辨識 ARP 封包、找出 DNS 區域傳送資訊。
- **🌟 現實本質**：**【內網中間人攻擊 (MITM) 與特權竊聽排查】**。整層辦公室或機房伺服器突然跳出連線警告或異常斷線，分析師必須在封包中指認是誰在冒充閘道器、又是哪台 DNS 伺服器把整間公司的內部拓撲外洩。

---

#### 4-1 & 4-2. ARP Spoofing 欺騙與中間人攻擊 (Root-Me 4260 & 4261)
- **平台連結**：[Root-Me (4260)](https://www.root-me.org/en/Challenges/Network/ARP-Spoofing-Active-listening) ｜ [Root-Me (4261)](https://www.root-me.org/en/Challenges/Network/ARP-Spoofing-The-man-in-the-middle)
- 🚨 **企業真實案發現場**：
  內網主機回報網路奇慢無比，且對外連線時不時斷線。網管懷疑有被感染勒索軟體的主機正在內網進行流量劫持與嗅探。
- 🔬 **封包解剖思維（現場看到什麼）**：
  正常情況下，只有需要知道 IP 對應 MAC 時才會發 ARP 請求。但封包中突然出現大量無端發出的 **免費 ARP（Gratuitous ARP）** 廣播，宣稱「192.168.1.1（閘道器）的 MAC 現在變成我的 MAC 了！」Wireshark 狀態列會直接跳出醒目的黃紅警告：`Duplicate IP address detected for 192.168.1.1`。
- 🛠️ **分析師實戰 SOP**：
  過濾 `arp.duplicate-address-detected || arp.opcode == 2`，比對同一 IP 是否在短時間內被不同的 MAC 位址宣告，立刻鎖定下毒攻擊機的真實 MAC 位址。
- 🛡️ **藍隊防禦與工程加固**：
  在企業接入交換器全面啟用 **DHCP Snooping** 與 **動態 ARP 檢查（Dynamic ARP Inspection, DAI）**，交換器硬體會自動比對 IP-MAC 繫結表，任何偽造來源的 ARP 封包直接在實體埠丟棄！

---

#### 4-3. DNS - zone transfert (Root-Me 340)
- **平台連結**：[Root-Me 傳送門](https://www.root-me.org/en/Challenges/Network/DNS-zone-transfert)
- 🚨 **企業真實案發現場**：
  外部攻擊者在情蒐階段，對企業 DNS 伺服器發動 AXFR 查詢，將公司內部所有伺服器清單一次打包帶走。
- 🔬 **封包解剖思維（現場看到什麼）**：
  一般 DNS 查詢（UDP 53）只查單一主機（Type A / AAAA）。但區域傳送（AXFR）走的是 **TCP 53**，伺服器會將該網域所有的內部主機名稱、測試機位址（如 `dev-db.internal`, `vpn.company.com`）全部一次性明文回傳。
- 🛠️ **分析師實戰 SOP**：
  過濾 `dns.qry.type == 252` 或 `tcp.port == 53`，檢視 DNS 回應中列出的整張網域名稱記錄表。
- 🛡️ **藍隊防禦與工程加固**：
  檢查 DNS 伺服器（Bind9 / Windows DNS）組態，限制區域傳送權限：配置 `allow-transfer { none; };` 或僅允許明確指定的次要 DNS 伺服器 IP。

---

## 📶 Phase 5：無線網路協定與握手機制 (Wireless 802.11 & WPA Security)

### 📌 階段任務定位
- **CTF 表象**：收集 IV 破 WEP、分析 WPA 握手包。
- **🌟 現實本質**：**【企業無線滲透與惡意雙胞胎基地台（Evil Twin）獵捕】**。駭客帶著網卡在公司大廳或樓下咖啡廳側錄企業員工的 Wi-Fi 握手，分析師必須鑑別企業無線加密強度與金鑰協商漏洞。

---

#### 5-1. Wired Equivalent Privacy (Root-Me 274)
- **平台連結**：[Root-Me 傳送門](https://www.root-me.org/en/Challenges/Network/Wired-Equivalent-Privacy)
- 🚨 **企業真實案發現場**：
  倉庫裡的舊型條碼掃描機或老舊 IoT 設備依然連線在 WEP 加密的 Wi-Fi 網段上。
- 🔬 **封包解剖思維（現場看到什麼）**：
  WEP 採用 RC4 串流密碼，其 **初始向量（IV）僅有 24-bit**，在傳輸時以純明文附加在封包頭部。只要收集到足夠的重複 IV（Fluhrer-Mantin-Shamir, FMS 漏洞），數學上就能直接反推共享金鑰。
- 🛠️ **分析師實戰 SOP**：
  在 Wireshark 觀察 `wlan.wep.iv` 欄位，結合 Aircrack-ng 工具計算金鑰。
- 🛡️ **藍隊防禦與工程加固**：
  全面淘汰 WEP，禁止任何老舊設備使用 WEP 上網；升級為 WPA2-AES (CCMP) 或 WPA3。

---

#### 5-2 & 5-3. WPA2 - Enterprise (Root-Me 4667) & WPA3 - SAE (Root-Me 4668)
- **平台連結**：[Root-Me WPA2 (4667)](https://www.root-me.org/en/Challenges/Network/WPA2-Enterprise) ｜ [Root-Me WPA3 (4668)](https://www.root-me.org/en/Challenges/Network/WPA3-SAE)
- 🚨 **企業真實案發現場**：
  攻擊者架設具備相同 SSID 的偽造基地台（Rogue AP），誘騙員工手機連入以截獲 802.1X 認證；同時評估企業升級 WPA3 的防護效益。
- 🔬 **封包解剖思維（現場看到什麼）**：
  - **WPA2 企業版**：觀察 **EAP-PEAP / EAP-TTLS** 認證過程，外層建立 TLS 隧道，內層傳遞 MSCHAPv2 握手。
  - **WPA3 SAE (Dragonfly 握手)**：封包中不再傳輸可供離線暴力破解的金鑰資訊，而是採用基於橢圓曲線密碼學的同時對等認證（Simultaneous Authentication of Equals），具備完美的**前向保密性（Forward Secrecy）**。
- 🛠️ **分析師實戰 SOP**：
  過濾 `eapol`，觀察 EAPOL 4 次交握（4-Way Handshake）或 EAP-TLS 認證訊框交互。
- 🛡️ **藍隊防禦與工程加固**：
  在終端設備派送企業 MDM 政策，強制員工裝置校驗 RADIUS 伺服器 CA 根憑證，防止連線至假 AP；逐步全面遷移至 WPA3-Enterprise。

---

## 🥷 Phase 6：高階隱蔽通道與 C2 惡意流量鑑識 (Covert Channels & Threat Hunting)

### 📌 階段任務定位
- **CTF 表象**：從 Ping 或 DNS 封包裡拼出字串、寫腳本算端口。
- **🌟 現實本質**：**【進階持續性威脅 (APT) 隱蔽通道阻斷與勒索軟體 C2 溯源】**。內部最高機密資料庫被斷網，防火牆阻斷了所有 HTTP/SSH/FTP 對外連線，只放行系統必需的 DNS 與 Ping。駭客把機密拆成微小碎片偷渡出去，分析師如何從看似正常的背景流量中揪出蛛絲馬跡？

---

#### 6-1 & 6-2. IP TTL (Root-Me 109) & ICMP payload (Root-Me 107 / 4964)
- **平台連結**：[Root-Me TTL (109)](https://www.root-me.org/en/Challenges/Network/IP-Time-To-Live) ｜ [Root-Me ICMP (107)](https://www.root-me.org/en/Challenges/Network/ICMP-payload)
- 🚨 **企業真實案發現場**：
  木馬程式（如 `icmpsh` 工具）被植入隔離區伺服器，利用看似無害的 Ping 探測（ICMP Echo Request/Reply）做為雙向 C2 通道或資料外洩途徑。
- 🔬 **封包解剖思維（現場看到什麼）**：
  標準作業系統的 Ping 封包，Data 欄位通常是固定的英文字母表（如 Windows 的 `abcdefghijklmnopqrstuvw...` 32 bytes）。但惡意木馬會把指令或外洩字元塞進 Data 欄位中，或者透過人為篡改 IP 標頭的 `Time to Live (TTL)` 數值來隱寫二進位位元！
- 🛠️ **分析師實戰 SOP**：
  1. 輸入顯示過濾器：`icmp.type == 8 && data.len > 0`
  2. 展開 `Data` 欄位，檢視十六進位內容與 ASCII 字符，觀察是否隨時間呈現非標準的動態負載。
- 🛡️ **藍隊防禦與工程加固**：
  在邊界防火牆禁止內部機密伺服器主動向外網發送 ICMP Echo Request；在次世代防火牆設定特徵：阻斷長度大於 64 bytes 或負載不符合作業系統標準的 ICMP 流量。

---

#### 6-3. shark on wire 2 (CyLab ID: 84)
- **平台連結**：[CyLab 傳送門](https://learn.cylabacademy.org/library?search=shark%20on%20wire%202)
- 🚨 **企業真實案發現場**：
  **極度狡猾的隱蔽通道！** 木馬連 Payload 都沒有填寫，DPI 深層檢測完全抓不到任何敏感字串，傳統防禦設備全數靜默。
- 🔬 **封包解剖思維（現場看到什麼）**：
  攻擊者將資料藏在 **UDP 目的通訊埠號（Destination Port）** 裡！例如發送到 `Port 5065`（扣除基底 5000 得 65，ASCII 為 `'A'`）、隨後發送到 `Port 5073`（得 73，ASCII 為 `'I'`）。分析師必須透過統計學視角，發現特定來源 IP 的目的埠號呈現異常規律跳動。
- 🛠️ **分析師實戰 SOP（Python 自動化提取）**：
  這種題目如果手動抄端口會瘋掉，必須展現自動化腳本實力：
  ```python
  from scapy.all import rdpcap, UDP
  pcap = rdpcap("capture.pcap")
  # 篩選特定通訊埠範圍並轉換 ASCII
  leaked = "".join([chr(pkt[UDP].dport - 5000) for pkt in pcap if pkt.haslayer(UDP) and 5000 < pkt[UDP].dport < 5255])
  print(f"[+] 外洩數據還原: {leaked}")
  ```
- 🛡️ **藍隊防禦與工程加固**：
  部署基於機器學習與統計基線的網路流量分析系統（NTA / NDR），對主機在短時間內隨機掃描或大量建立離散連接埠通訊的異常行為發出「通訊埠跳變（Port Hopping）隱蔽外洩」高危警報。

---

#### 6-4 & 6-5. DNS Tunneling 隱蔽通道外洩 (CyLab 110 & Root-Me 1649)
- **平台連結**：[CyLab (110)](https://learn.cylabacademy.org/library?search=Wireshark%20twoo%20twooo%20two%20twoo...) ｜ [Root-Me (1649)](https://www.root-me.org/en/Challenges/Forensic/DNS-exfiltration)
- 🚨 **企業真實案發現場**：
  **真實 APT 與勒索軟體組織最泛濫的外洩手法！** 內部資料庫主機深夜對外部權威 DNS 伺服器發送連續上千筆長子網域查詢（如 `a1b2c3d4.data.attacker.com`），將客戶個資無聲無息地送往境外。
- 🔬 **封包解剖思維（現場看到什麼）**：
  過濾 `dns.flags.response == 0`，你會看到海量非正規的 DNS 查詢，子域名具有三個致命特徵：
  1. **長度異常**：子域名長度接近上限（50 ~ 63 字元）。
  2. **高熵值（High Entropy）**：全是 Base32 / Base64 / Hex 編碼的亂數字串。
  3. **頻率極高**：每秒十幾次連續查詢。
- 🛠️ **分析師實戰 SOP（Tshark 極速命令列）**：
  ```bash
  # 1. 一秒提取所有查詢的子域名
  tshark -r dns.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name | sort -u > subdomains.txt
  # 2. 撰寫簡單 Python 腳本將子域名開頭的 Hex/Base32 拆出並解碼還原檔案
  ```
- 🛡️ **藍隊防禦與工程加固**：
  在企業內部部署專屬 DNS 代理（如 Cisco Umbrella / Infoblox / CoreDNS），開啟 **DNS Tunneling 阻斷功能**：自動識別子網域長度超過閾值、字符熵值異常或包含大量 TXT/NULL 記錄的查詢並立即在解析層 Drop。

---

#### 6-7. Command & Control Level 2~6 (Root-Me 313~317)
- **平台連結**：[Root-Me 傳送門](https://www.root-me.org/en/Challenges/Forensic/Command-and-Control-level-2)
- 🚨 **企業真實案發現場**：
  受害主機已被木馬持久化控制，每隔固定時間向外部黑客 C2 伺服器回傳「心跳包（Beaconing）」，並接收攻擊者下達的二進位執行指令。
- 🔬 **封包解剖思維（現場看到什麼）**：
  在 Wireshark 分析封包的時間差（Delta Time），觀察通訊是否呈現規律的週期性（如每 60 秒 ± 10% 抖動 Jitter）；剖析 Payload 中的自訂二進位標頭（Magic Number、指令碼 Opcode、Payload 長度）。
- 🛠️ **分析師實戰 SOP**：
  1. 檢視 `Statistics` ➔ `Conversations` ➔ 查看連線最頻繁的外部 IP。
  2. 啟用 Wireshark 時間欄位切換：`View` ➔ `Time Display Format` ➔ `Seconds Since Previous Displayed Packet`，觀察心跳間隔。
  3. 逆向通訊協定，還原攻擊者下發的 `whoami`、`dir` 或提權命令。
- 🛡️ **藍隊防禦與工程加固**：
  在邊界防火牆全面阻斷該外部 C2 IP 與惡意 ASN；立即針對受害端點下發隔離指令，使用 Volatility 進行記憶體傾印（Memory Dump），抓取正在執行該連線的木馬進程與注入執行緒。

---

## 🎯 總結：資安工程師的通關心法

當你做完這套路徑中的題目時，請試著不要只看分數，而是拿起筆問自己：
1. **「如果這個情境發生在我任職的公司，誰會被開除？造成了什麼法規風險？」**
2. **「我在 Wireshark 裡看到的每一欄 Hex，對應的是哪一條 RFC 規範的哪個欄位？」**
3. **「如果我是藍隊防禦架構師，我有辦法在交換器、防火牆或 EDR 寫下一條規則，在攻擊發生的第 1 秒就自動阻斷它嗎？」**

當你能清楚回答這三個問題，這套學習路徑帶給你的，就已經遠遠超越了 CTF 的複製貼上，而是貨真價實的**工業級網路鑑識與防衛工程實力**！
