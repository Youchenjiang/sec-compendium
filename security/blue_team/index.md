# 🛡️ 藍隊全領域實戰技能細分與可練習題庫總表 (八大現代防禦作戰區塊・全景31大領域・107項技術點終極矩陣)

> 📌 **驗證聲明**：本表所有資源經 100% 線上連線與存取機制審查，全數為**免訂閱、無付費牆、直接可進入**之官方靶場、開源挑戰、國家法規庫與實體真題。依據現代藍隊防衛作戰體系與資安金盾獎、iPAS 考評大綱，全面整合為**八大核心作戰區塊**。
>
> 💡 **配套學習路徑手冊**：若您在特定領域感到缺乏信心或需要底層知識系統化構建，請直接查閱 [【藍隊全領域 31 大深度學習路徑全景導航庫】](learning_paths/README.md)（涵蓋 31 個領域的底層架構、前置測試、核心指令、進階防禦與階段通過檢查表）。
>
> 🚀 **實戰通關主線課表**：**技術難度 (Level) ≠ 修課順序 (Phase)！** 請參閱 [【現代藍隊實戰通關課表與作戰主線 (Phase 0 ~ Phase 6)】](career_curriculum.md)（含 SOC 告警分流八問、Incident Response 圍堵 SOP 與 **36 項 Core 核心必修** 分流導引）。
>
> 🎯 **CyberDefenders 官方免費題庫對照表**：所有 82 題官方認證 100% 免費挑戰與 31 大領域深度映射，請參閱 [【CyberDefenders 全量 82 題免費實戰靶場・31 大學習路徑深度對照手冊】](learning_paths/cyberdefenders_free_catalog_mapping.md)。

### 📊 難度分級體系與項目分佈 (Difficulty Matrix)

| 難度等級 (Level) | 定位標籤 | 項目數量 | 適用階段與核心目標 |
| :---: | :--- | :---: | :--- |
| **🟢 L1** | **基礎通識與工具打底** | **39 項** | 觀念建構、命令列操作、協定與法規通識（Linux 權限、Switch Port-Security、TCP 狀態機、SNMP/VPN、802.11 無線、資安法、個資法等） |
| **🟡 L2** | **主力防衛與靶場核心** | **34 項** | 體系防禦策略、日誌關聯分析、常規靶場（防火牆加固、雲端責任模型、Windows 核心日誌、Splunk SPL、C2 流量、CVSS 評分與重大 CVE 等） |
| **🔴 L3** | **硬核對抗與深度溯源** | **24 項** | 底層對抗技術、二進位與記憶體分析（Kerberos 網域攻防、Sysmon 威脅獵捕、PE 靜態分流、Java 內存馬、Volatility 記憶體鑑識、NTFS 磁碟鐵證、Rootkit 等） |
| **👑 L4** | **全域架構與全真演習** | **10 項** | 跨維度實網對抗、持續驗證、企業級大賽（Atomic Red Team 自動化對抗、紫隊協同、Splunk BOTS 實網資料集、端到端 APT 全局溯源、Cyber Range 推演） |
| **合計** | **全景 31 領域終極矩陣** | **107 項** | 覆蓋從事前加固、即時監控、威脅獵捕、深度鑑識到法規合規的全生命週期 |

> 🎯 **三層修課分流建議 (消解資訊焦慮)**：
>
> - **🎯 核心主幹 (Core Track, 36 項)**：建立端點/網路可見性與 SOC 告警研判能力之**絕對必修**，優先拿下即可勝任 SOC L1 與金盾獎主力初賽！
> - **🔬 領域專精 (Specialization Track, 46 項)**：記憶體/磁碟深度鑑識、AD 網域進階攻防、重大 CVE 逆推、資通法規（按隊伍分工與個人興趣選修）。
> - **🚀 高階前沿 (Advanced Track, 25 項)**：Linux 核心 eBPF、行動裝置、K8s 逃逸、紫隊自動化閉環演練。

## 🏛️ 區塊一：事前架構、系統加固與基礎設施防衛 (Proactive Architecture & System Hardening)
> 💡 **作戰任務**：建立不可摧毀的第一道防線。涵蓋作業系統基準硬化、硬體交換機安全、網路邊界分段、DevSecOps 供應鏈審計以及現代雲原生運算共同責任架構。
>
> 📋 **本區塊核心領域說明 (Domains Overview)**：
>
> - [**領域 1：Linux 系統基礎加固**](learning_paths/block_1_hardening/01_linux_hardening.md)：系統權限模型、敏感檔案安全、SSH/PAM 硬化與排程排查。
> - [**領域 2：網路分段與防火牆加固**](learning_paths/block_1_hardening/02_network_segmentation_firewall.md)：Netfilter 邊界策略、狀態追蹤、內部網路微隔離與次世代防火牆 (NGFW/IPS) 聯防。
> - [**領域 3：交換機硬體安全與鏈路隔離**](learning_paths/block_1_hardening/03_switching_port_security.md)：Switch Port-Security 違規模式、802.1Q VLAN Tag 結構與生成樹 (STP) 防護。
> - [**領域 4：軟體供應鏈安全 (DevSecOps)**](learning_paths/block_1_hardening/04_devsecops_supply_chain.md)：開源依賴投毒、SBOM 審查與 CI/CD 管道金鑰審計。
> - [**領域 5：雲原生防衛與雲端責任模型**](learning_paths/block_1_hardening/05_cloud_security_shared_responsibility.md)：IaaS/PaaS/SaaS 共同責任模型、IMDSv2 SSRF 防護與容器逃逸防衛。

| 難度 | 細分實戰技術點 (Sub-Topic & Technique) | 🎯 具體線上靶場、實戰房間、開源數據集與題目清單 (Practicable Challenges & Labs) |
| :---: | :--- | :--- |
| **🟢 L1** | **1.1 Linux 權限模型與敏感檔案檢視**<br>(`/etc/passwd`, `/etc/shadow`, Umask, SUID) | • [OverTheWire: Bandit (Level 0~10 權限模型與 SUID 排查)](https://overthewire.org/wargames/bandit/)<br>• [SadServers: "Saint John" (Fix permissions 權限修復實機)](https://sadservers.com/)<br>• [CIS Linux Benchmark 安全配置手冊](https://www.cisecurity.org/cis-benchmarks/) |
| **🟢 L1** | **1.2 Linux 連線狀態與服務進程排查**<br>(`ss -antup`, `netstat`, `ps -ef`, `lsof -i`) | • [SadServers: "Saskatoon" (Check port listening 監聽埠鑑識)](https://sadservers.com/)<br>• [OverTheWire: Bandit (Level 11~14 服務進程排查)](https://overthewire.org/wargames/bandit/)<br>• `07_藍隊防禦與護網營運/01_系統與資料庫加固/Linux系統安全加固/` |
| **🟢 L1** | **1.3 帳號安全與 SSH 遠端登入硬化**<br>(SSH 金鑰認證、停用 Root 登入、PAM 限制) | • [OverTheWire: Bandit (Level 15~17 SSH 金鑰認證與憑證)](https://overthewire.org/wargames/bandit/)<br>• [SadServers: "Rosario" (Restore SSH access 遠端登入加固)](https://sadservers.com/) |
| **🟢 L1** | **1.4 排程作業與自啟動項排查**<br>(`/etc/cron*`, `crontab -l`, `systemd` 計時器) | • [OverTheWire: Bandit (Level 21~24 排程 Cron 作業檢視)](https://overthewire.org/wargames/bandit/)<br>• [SadServers: "Bilbao" (Cron process 故障鑑識)](https://sadservers.com/) |
| **🟡 L2** | **2.1 邊界防火牆策略與微創阻斷實務**<br>(iptables In-line 串接、DROP 規則與連線追蹤) | • `07_藍隊防禦與護網營運/02_存取控制與防火牆/Linux存取控制與防火牆/`<br>• [Netfilter iptables 官方封包過濾與狀態追蹤手冊](https://netfilter.org/)<br>• [`../exams/mock_exam_b_lab_questions.md`](../exams/mock_exam_b_lab_questions.md)（第 24~28 題） |
| **🟡 L2** | **2.2 內部網路微隔離與 VLAN 存取控制**<br>(零信任存取控制、ACL 限制橫向移動、管理平面隔離) | • [iptables-nft 規則集加固實作指南](https://netfilter.org/)<br>• [NIST SP 800-207: Zero Trust Architecture 網路分段指南](https://csrc.nist.gov/) |
| **🟡 L2** | **2.3 次世代防火牆 (NGFW) 與 IPS 聯防**<br>(應用層 App-ID 辨識、TLS 解密檢測、IPS 特徵阻斷) | • [Suricata Inline IPS 模式實操指南](https://suricata.io/)<br>• [OPNsense 開源防火牆防護手冊](https://opnsense.org/) |
| **🟢 L1** | **3.1 Switch Port-Security 違規處理模式**<br>(Protect / Restrict / Shutdown 進入 err-disable、安全 MAC 學習機制) | • [Packet Tracer 官方免費實驗與題庫 (Cisco Networking Academy)](https://skillsforall.com/course/getting-started-cisco-packet-tracer)<br>• [Cisco 開放社群: Port-Security 違規模式與 Errdisable 復原指引](https://community.cisco.com/)<br>• [Yamol: iPAS 資訊安全工程師 - Switch 埠安全性與 MAC 欺騙歷屆真題庫](https://yamol.tw/) |
| **🟢 L1** | **3.2 IEEE 802.1Q VLAN Tag 結構與跨交換機 Trunk**<br>(4-Byte Tag、12-bit VID、TPID 0x8100、Native VLAN 跳躍防範) | • [IEEE 802.1Q 官方標準與 Frame 結構技術規格](https://en.wikipedia.org/wiki/IEEE_802.1Q)<br>• [Wireshark 官方封包範例庫: 802.1Q VLAN Tag 跨交換機流量分析](https://gitlab.com/wireshark/wireshark/-/wikis/SampleCaptures) |
| **🟢 L1** | **3.3 交換機鏈路防護與生成樹安全**<br>(BPDU Guard、Root Guard、廣播風暴抑制與 DHCP Snooping 防禦) | • [Packet Tracer: STP 生成樹協定與 BPDU 防禦實戰配置](https://skillsforall.com/course/getting-started-cisco-packet-tracer)<br>• [Wireshark 官方封包範例庫: STP 生成樹 BPDU 封包取樣](https://gitlab.com/wireshark/wireshark/-/wikis/SampleCaptures) |
| **🔴 L3** | **4.1 開源依賴投毒與相依性混淆**<br>(Dependency Confusion、Typosquatting 惡意套件排查) | • [visma-prodsec/confused (相依性混淆開源檢測工具)](https://github.com/visma-prodsec/confused)<br>• [jeremylong/DependencyCheck 官方開源專案](https://jeremylong.github.io/DependencyCheck/) |
| **🔴 L3** | **4.2 軟體物料清單 (SBOM) 審查與弱點追蹤**<br>(CycloneDX, SPDX 格式比對、Grype 弱點掃描) | • [Anchore Grype 開源弱點掃描實戰](https://github.com/anchore/grype)<br>• [Aqua Security Trivy 容器與相依性安全掃描](https://github.com/aquasecurity/trivy) |
| **🔴 L3** | **4.3 CI/CD 管道審計與密鑰外洩防範**<br>(GitHub Actions 權限硬化、Trufflehog 金鑰掃描) | • [TruffleHog (開源高熵值金鑰洩漏檢測器)](https://github.com/trufflesecurity/trufflehog)<br>• [StepSecurity CI/CD 加固與權限最小化指南](https://www.stepsecurity.io/) |
| **🟡 L2** | **5.1 雲端運算共同責任模型**<br>(IaaS vs PaaS vs SaaS 各層實體/主機/網路/應用/資料安全權責劃分矩陣) | • [AWS 官方: 共同責任模型 (Shared Responsibility Model) 深度架構白皮書](https://aws.amazon.com/compliance/shared-responsibility-model/)<br>• [Microsoft Learn: 雲端共同責任模型互動式課程與檢定題](https://learn.microsoft.com/training/modules/describe-cloud-service-types/) |
| **👑 L4** | **5.2 雲端多租戶 IAM 提權與審計日誌研判**<br>(AWS CloudTrail, GuardDuty, CloudGoat) | • [RhinoSecurityLabs: CloudGoat (AWS 脆弱場景演練)](https://github.com/RhinoSecurityLabs/cloudgoat)<br>• [Pwned Labs (雲端資安攻防挑戰)](https://pwnedlabs.io/) |
| **👑 L4** | **5.3 容器逃逸與 K8s 叢集運行時安全**<br>(Kubernetes Goat 演練、Privileged 容器逃逸) | • [madhuakula: Kubernetes Goat (K8s 容器攻防與日誌偵測)](https://github.com/madhuakula/kubernetes-goat)<br>• [CyberDefenders: AzurePot (Linux 伺服器入侵與漏洞鑑識)](https://cyberdefenders.org/blueteam-ctf-challenges/azurepot/)<br>• [Kube-bench CIS Kubernetes Benchmark 自動化審計](https://github.com/aquasecurity/kube-bench) |
| **👑 L4** | **5.4 雲端儲存桶外洩與中繼資料劫持**<br>(SSRF 獲取 IMDSv1 憑證防禦、S3 Bucket 審計) | • [Flaws.cloud (AWS 雲端實戰滲透與日誌鑑識)](http://flaws.cloud/)<br>• [CloudGoat: lambda_privesc (雲端無伺服器提權場景)](https://github.com/RhinoSecurityLabs/cloudgoat) |

## 🌐 區塊二：應用程式、協定安全與通訊防禦 (Protocols, Cryptography & Application Security)
> 💡 **作戰任務**：捍衛通訊與傳輸基石。涵蓋核心 TCP/IP 協定棧分析、SNMP 網管與 VPN 通道加密、802.11 無線通訊防護、Web 應用程式防護、社交工程郵件防禦以及現代密碼學證書安全。
>
> 📋 **本區塊核心領域說明 (Domains Overview)**：
>
> - [**領域 6：網路協定與基礎封包分析**](learning_paths/block_2_protocols_crypto_app/06_network_protocols_packet_analysis.md)：TCP 三向交握狀態機、Wireshark 高階過濾、DNS 異常排查與 HTTP 串流導出。
> - [**領域 7：網路管理協定 (SNMP) 與 VPN 傳輸安全**](learning_paths/block_2_protocols_crypto_app/07_snmp_vpn_security.md)：SNMPv1/v2c/v3 authPriv 安全等級、四大 VPN 協定對決與 IPsec AH/ESP。
> - [**領域 8：無線通訊安全機制與協定演進**](learning_paths/block_2_protocols_crypto_app/08_wireless_security_wpa.md)：802.11 四向握手 PTK 計算、KRACK 重放攻擊與 WPA3 SAE 前向保密。
> - [**領域 9：Web 基礎弱點識別**](learning_paths/block_2_protocols_crypto_app/09_web_vulnerability_defense.md)：SQL/命令注入防護、路徑穿越、XXE 外部實體注入與 XSS/CSRF 安全標頭。
> - [**領域 10：電子郵件與社交工程防衛**](learning_paths/block_2_protocols_crypto_app/10_email_phishing_defense.md)：SPF/DKIM/DMARC 驗證、EML 標頭 Received 溯源與 oledump 巨集提取。
> - [**領域 11：密碼學基礎與證書安全**](learning_paths/block_2_protocols_crypto_app/11_cryptography_certificates.md)：對稱/非對稱演算法、X.509 憑證鏈、OCSP Stapling 與 PFS 前向保密。

| 難度 | 細分實戰技術點 (Sub-Topic & Technique) | 🎯 具體線上靶場、實戰房間、開源數據集與題目清單 (Practicable Challenges & Labs) |
| :---: | :--- | :--- |
| **🟢 L1** | **6.1 TCP 協定棧與三向交握狀態機**<br>(SYN/ACK 旗標、交握異常、RST 阻斷) | • [Wireshark 官方封包範例庫 (TCP 三向交握與 RST 狀態機)](https://gitlab.com/wireshark/wireshark/-/wikis/SampleCaptures)<br>• [picoCTF: Wireshark twoo twooo... (ID: 110)](https://learn.cylabacademy.org/library?search=Wireshark%20twoo%20twooo%20two%20twoo...)<br>• [picoCTF: Shark on wire 1 (ID: 60)](https://learn.cylabacademy.org/library?search=Shark%20on%20wire%201) |
| **🟢 L1** | **6.2 HTTP 明文串流重組與檔案導出**<br>(Follow TCP Stream、Export Objects) | • [MTA: 惡意軟體 PCAP 追蹤教學手冊 (HTTP 串流重組與檔案導出)](https://www.malware-traffic-analysis.net/tutorials/index.html)<br>• [picoCTF: Trivial Flag Transfer Protocol (ID: 103)](https://learn.cylabacademy.org/library?search=Trivial%20Flag%20Transfer%20Protocol)<br>• [picoCTF: Shark on wire 2 (ID: 61)](https://learn.cylabacademy.org/library?search=Shark%20on%20wire%202) |
| **🟢 L1** | **6.3 DNS 基礎查詢解析與異常頻率排查**<br>(A/AAAA/TXT/PTR 查詢特徵、NXDOMAIN 洪泛) | • [CyberDefenders: PacketMaze (多協定與 DNS 異常流量分析)](https://cyberdefenders.org/blueteam-ctf-challenges/packetmaze/)<br>• [MTA: 2021-02-01 Emotet 異常 DNS 查詢樣本分析](https://www.malware-traffic-analysis.net/2021/02/01/index.html) |
| **🟢 L1** | **6.4 ICMP/ARP 區域網路掃描與嗅探特徵**<br>(ARP 欺騙、Ping Sweep 掃描、過濾語法實作) | • [picoCTF: Packets Primer (ID: 286)](https://learn.cylabacademy.org/library?search=Packets%20Primer)<br>• [Wireshark 官方封包範例庫 (ARP Spoofing 與 ICMP 樣本)](https://gitlab.com/wireshark/wireshark/-/wikis/SampleCaptures) |
| **🟢 L1** | **7.1 SNMP 版本演進與安全等級**<br>(SNMP v1/v2c 明文 Community String vs v3 USM authPriv 等級: HMAC+AES 加密) | • [IETF RFC 3414: User-based Security Model (USM) for SNMPv3](https://datatracker.ietf.org/doc/html/rfc3414)<br>• [Wireshark 官方範例庫: SNMPv1/v2c 明文與 SNMPv3 認證加密封包對比](https://gitlab.com/wireshark/wireshark/-/wikis/SNMP)<br>• [Yamol: iPAS 與金盾獎 SNMP 網管協定歷屆客觀題庫](https://yamol.tw/) |
| **🟢 L1** | **7.2 四大 VPN 協定深度對決與安全性**<br>(PPTP: TCP 1723+GRE 47, L2TP/IPsec: UDP 500/4500 AH/ESP, SSL VPN: 443, WireGuard) | • [IETF RFC 4301: Security Architecture for IPsec (AH/ESP/IKE 協定)](https://datatracker.ietf.org/doc/html/rfc4301)<br>• [Wireshark 官方範例庫: IPsec IKEv1/IKEv2 與 ESP 封包分析](https://gitlab.com/wireshark/wireshark/-/wikis/SampleCaptures)<br>• [OpenVPN 官方社群開源伺服器建置與證書配置指南](https://openvpn.net/community-resources/) |
| **🟢 L1** | **8.1 802.11 四向握手 (4-Way Handshake) 與 EAPOL 認證流程**<br>(ANonce、SNonce、PTK、GTK 產生機制與金鑰層級結構) | • [Wireshark 官方範例庫: 802.11 WPA/WPA2 4-Way Handshake 封包](https://gitlab.com/wireshark/wireshark/-/wikis/SampleCaptures)<br>• [Aircrack-ng 官方測試套件與 EAPOL 捕捉驗證手冊](https://www.aircrack-ng.org/) |
| **🟢 L1** | **8.2 WPA2 離線字典攻擊與 WPA3 Dragonfly (SAE) 前向保密防禦**<br>(KRACK 重放攻擊、抗離線字典暴破與 Simultaneous Authentication of Equals) | • [Wi-Fi Alliance: WPA3 Security Technology Overview 官方技術規格](https://www.wi-fi.org/discover-wi-fi/security)<br>• [Mathy Vanhoef: KRACK Attacks 官方研究論文與驗證封包](https://www.krackattacks.com/)<br>• [Yamol: 歷屆金盾獎與資安證照無線網路安全技術題庫](https://yamol.tw/) |
| **🟢 L1** | **9.1 注入類漏洞流量特徵與防禦**<br>(SQL Injection / Command Injection) | • [PortSwigger: SQLi UNION Attack (注入流量特徵與防禦)](https://portswigger.net/web-security/sql-injection/union-attacks)<br>• [PortSwigger: OS Command Injection (命令注入攔截)](https://portswigger.net/web-security/os-command-injection)<br>• [picoCTF: SQL Direct (ID: 303)](https://learn.cylabacademy.org/library?search=SQL%20Direct) |
| **🟢 L1** | **9.2 檔案路徑穿越與 XML 外部實體特徵**<br>(Path Traversal / XXE 注入特徵) | • [PortSwigger: File Path Traversal (路徑穿越防護實驗)](https://portswigger.net/web-security/file-path-traversal)<br>• [picoCTF: Forbidden Paths (ID: 270)](https://learn.cylabacademy.org/library?search=Forbidden%20Paths)<br>• [picoCTF: SOAP (ID: 376)](https://learn.cylabacademy.org/library?search=SOAP) |
| **🟢 L1** | **9.3 跨站腳本與請求偽造防範**<br>(XSS 反射/儲存型特徵、CSRF Token 機制) | • [PortSwigger: Cross-site Scripting (XSS 流量特徵與編碼防禦)](https://portswigger.net/web-security/cross-site-scripting)<br>• [picoCTF: Cookies (ID: 173)](https://learn.cylabacademy.org/library?search=Cookies) |
| **🟢 L1** | **9.4 敏感資訊洩漏與目錄遍歷**<br>(Web 目錄爬取、`.git` 外洩、錯誤堆疊洩漏) | • [picoCTF: Inspect HTML (ID: 275)](https://learn.cylabacademy.org/library?search=Inspect%20HTML)<br>• [picoCTF: Local Authority (ID: 276)](https://learn.cylabacademy.org/library?search=Local%20Authority)<br>• [picoCTF: Roboto Sans (ID: 281)](https://learn.cylabacademy.org/library?search=Roboto%20Sans) |
| **🟢 L1** | **10.1 郵件認證協定與仿冒偵測**<br>(SPF、DKIM、DMARC 驗證與 DNS 紀錄) | • [dmarcian: DMARC Record Checker (在線解析驗證工具)](https://dmarcian.com/dmarc-inspector/)<br>• [MXToolbox: SuperTool SPF/DKIM 即時驗證庫](https://mxtoolbox.com/SuperTool.aspx) |
| **🟢 L1** | **10.2 釣魚郵件標頭與惡意附件初篩**<br>(EML 標頭分析、Received 路由、惡意巨集) | • [CyberDefenders: Maldoc101 (郵件標頭與惡意附件分析)](https://cyberdefenders.org/blueteam-ctf-challenges/maldoc101/)<br>• [Spamhaus: Received Header Analysis 逆推指南](https://www.spamhaus.org/) |
| **🟢 L1** | **10.3 誘餌文件與巨集程式碼萃取**<br>(OLE 結構提取、`oledump`、VBA 混淆逆推) | • [Didier Stevens: oledump.py 開源工具手冊](https://blog.didierstevens.com/programs/oledump-py/)<br>• [SANS Reading Room: Analyzing Malicious Documents (巨集文檔分析手冊)](https://www.sans.org/white-papers/) |
| **🟢 L1** | **10.4 QR Code 釣魚 (Quishing) 與跳轉識別**<br>(多重 HTTP 重定向追蹤、縮短網址還原) | • [SANS Phishing Triage Guidelines (釣魚應變指引)](https://www.sans.org/)<br>• [URLScan.io 雲端沙盒與跳轉排查](https://urlscan.io/) |
| **🟢 L1** | **11.1 TLS 憑證鏈驗證與加密傳輸**<br>(X.509 憑證鏈、CA 根證書、自簽憑證辨識) | • [CryptoHack: Introduction to Cryptography (密碼學基礎通識)](https://cryptohack.org/challenges/introduction/)<br>• [BadSSL.com 官方憑證驗證與錯誤測試矩陣](https://badssl.com/) |
| **🟢 L1** | **11.2 雜湊演算法完整性檢驗與碰撞辨析**<br>(MD5、SHA-1、SHA-256、HMAC 訊息鑑別碼) | • [CyberChef 在線雜湊運算與碰撞驗證](https://gchq.github.io/CyberChef/)<br>• [picoCTF: Mod 26 (ID: 144)](https://learn.cylabacademy.org/library?search=Mod%2026)<br>• [picoCTF: Transformation (ID: 104)](https://learn.cylabacademy.org/library?search=Transformation) |
| **🟢 L1** | **11.3 密碼套件協商與弱加密協定降級防範**<br>(SSLv3/TLS 1.0/1.1 廢止、RC4 淘汰、PFS 前向保密) | • [SSL Labs Server Test 官方在線測試](https://www.ssllabs.com/ssltest/)<br>• [testssl.sh 開源指令碼實戰檢驗](https://testssl.sh/)<br>• [Mozilla SSL Configuration Generator 加固指引](https://ssl-config.mozilla.org/) |

## 🔑 區塊三：身分驗證、特權存取與目錄服務防護 (Identity, Directory & Access Governance)
> 💡 **作戰任務**：涵蓋 Active Directory 網域攻防（Kerberos 票據防偽、DCSync 監控、ACL 審查）與現代雲端 IAM 身分治理。
>
> 📋 **本區塊核心領域說明 (Domains Overview)**：
>
> - [**領域 12：AD 網域攻防**](learning_paths/block_3_identity_directory/12_active_directory_defense.md)：Kerberos 票據交握、AS-REP/Kerberoasting、黃金/白銀票據防護與 DCSync 偵測。
> - [**領域 13：身分存取管理安全 (IAM)**](learning_paths/block_3_identity_directory/13_identity_access_management.md)：OAuth 2.0 授權碼模式、MFA 疲勞轟炸防衛與 FIDO2 Passkey 架構。

| 難度 | 細分實戰技術點 (Sub-Topic & Technique) | 🎯 具體線上靶場、實戰房間、開源數據集與題目清單 (Practicable Challenges & Labs) |
| :---: | :--- | :--- |
| **🔴 L3** | **12.1 Kerberos 預驗證弱點與 AS-REP Roasting**<br>(DONT_REQ_PREAUTH 帳戶爆破分析) | • [Orange-Cyberdefense/GOAD (AS-REP Roasting 實戰環境)](https://github.com/Orange-Cyberdefense/GOAD)<br>• [Hashcat Mode 18200 票據碰撞防護指引](https://hashcat.net/) |
| **🔴 L3** | **12.2 SPN 服務票據請求與 Kerberoasting**<br>(RC4-HMAC 票據截獲、日誌 Event ID 4769) | • [Orange-Cyberdefense/GOAD (Game of Active Directory 實戰靶場)](https://github.com/Orange-Cyberdefense/GOAD)<br>• [HTB Sherlocks: GhostTrace (AD 橫向移動調查)](https://app.hackthebox.com/sherlocks/GhostTrace) |
| **🔴 L3** | **12.3 偽造票據攻擊與全域特權維持**<br>(Golden Ticket 偽造 TGT / Silver Ticket 偽造 ST) | • [`../exams/mock_exam_a_100q_questions.md`](../exams/mock_exam_a_100q_questions.md)（Kerberos 核心題群）<br>• [BloodHound 官方開源專案 (AD 攻擊路徑繪製)](https://github.com/SpecterOps/BloodHound) |
| **🔴 L3** | **12.4 NTDS.dit 憑證導出與 DCSync 偵測**<br>(DRSUAPI 複製協定呼叫、Event ID 4662 權限審查) | • [sbousseaden/EVTX-ATTACK-SAMPLES (DCSync Event 4662 樣本)](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES)<br>• [Impacket `secretsdump.py` 流量特徵檢測實務](https://github.com/fortra/impacket) |
| **🔴 L3** | **12.5 AD 存取控制路徑與特權提升分析**<br>(ACL 濫用 GenericAll/WriteDacl、GPO 劫持) | • [GOAD v2 實戰環境 (多樹林域安全測試環境)](https://github.com/Orange-Cyberdefense/GOAD)<br>• [SpecterOps BloodHound 攻擊圖解析手冊](https://bloodhound.specterops.io/) |
| **🔴 L3** | **13.1 OAuth 2.0 / SAML 權杖竊取與重放**<br>(Token Theft、偽造 Assertion、授權碼攔截) | • [PortSwigger: OAuth 2.0 認證漏洞防衛實驗](https://portswigger.net/web-security/oauth)<br>• [CloudGoat: IAM Privilege Escalation 演練場景](https://github.com/RhinoSecurityLabs/cloudgoat) |
| **🔴 L3** | **13.2 MFA 疲勞轟炸與繞過攻擊防衛**<br>(MFA Fatigue / Push Bombing 日誌特徵、條件式存取) | • [CISA Alert AA22-074A 防護手冊](https://www.cisa.gov/news-events/cybersecurity-advisories)<br>• [Microsoft Entra ID 條件式存取原則最佳實踐](https://learn.microsoft.com/azure/active-directory/) |
| **🔴 L3** | **13.3 服務帳戶特權濫用與 Session 劫持**<br>(Pass-the-PRT 攻擊、Azure AD / Okta 審計日誌) | • [AADInternals 開源工具研習 (Azure AD 鑑識)](https://github.com/Gerenios/AADInternals) |

## 📡 區塊四：即時監控、偵測工程與 SIEM 大數據分析 (Detection Engineering, SIEM & SOC Monitoring)
> 💡 **作戰任務**：SOC 戰情核心樞紐。涵蓋主機系統日誌基準線、Splunk SPL 大數據檢索、C2 隱蔽通訊流量鑑識與 YARA / Sigma / Suricata 規則工程。
>
> 📋 **本區塊核心領域說明 (Domains Overview)**：
>
> - [**領域 14：端點核心日誌與排查**](learning_paths/block_4_detection_siem_soc/14_endpoint_logs_triage.md)：Windows Logon Types 2/3/10、4688 命令列參數審計與 7045 服務安裝日誌。
> - [**領域 15：SIEM 大數據分析**](learning_paths/block_4_detection_siem_soc/15_siem_splunk_big_data.md)：Splunk SPL 管道語法、rex 欄位抽取、stats 統計聚合與動態基準線告警。
> - [**領域 16：惡意流量與隱蔽通訊**](learning_paths/block_4_detection_siem_soc/16_malicious_traffic_covert_comm.md)：C2 心跳與 Jitter 方差分析、DNS 隱蔽通道外洩與重大 N-day 漏洞利用封包逆推。
> - [**領域 17：偵測工程與簽章**](learning_paths/block_4_detection_siem_soc/17_detection_engineering_rules.md)：YARA 二進位特徵碼撰寫、Sigma 跨平台日誌規則轉譯與 Suricata 網路簽章。

| 難度 | 細分實戰技術點 (Sub-Topic & Technique) | 🎯 具體線上靶場、實戰房間、開源數據集與題目清單 (Practicable Challenges & Labs) |
| :---: | :--- | :--- |
| **🟢 L1** | **14.1 Windows 身分驗證與暴力破解日誌**<br>(Event ID 4624 登入類型 / 4625 爆破) | • [CyberDefenders: Spotlight (Event ID 4624/4625 登入排查)](https://cyberdefenders.org/blueteam-ctf-challenges/spotlight/)<br>• [Ultimate Windows Security Event ID 4624 官方參照手冊](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/)<br>• [sbousseaden/EVTX-ATTACK-SAMPLES (RDP 爆破與登入樣本)](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES) |
| **🟢 L1** | **14.2 Windows 正常核心進程基準線**<br>(`System` ➔ `smss` ➔ `services` 親緣關係) | • [SANS Hunt Evil Poster (Windows 核心進程基準對照圖)](https://www.sans.org/posters/hunt-evil/)<br>• [CyberDefenders: RedLine (進程親緣樹排查實戰)](https://cyberdefenders.org/blueteam-ctf-challenges/redline/) |
| **🟢 L1** | **14.3 基礎系統管理與服務安裝日誌**<br>(Event ID 7045 新服務 / 4720 帳戶建立) | • [HTB Sherlocks: Logjammer (Defender/PowerShell/System 日誌取證)](https://app.hackthebox.com/sherlocks/Logjammer)<br>• [sbousseaden/EVTX-ATTACK-SAMPLES (EID 7045 新服務樣本)](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES)<br>• [`../exams/mock_exam_b_lab_questions.md`](../exams/mock_exam_b_lab_questions.md)（第 6~8 題） |
| **🟢 L1** | **14.4 防毒與主機防護日誌鑑識**<br>(Defender Event ID 1116 威脅偵測 / 1117 隔離) | • [sbousseaden/EVTX-ATTACK-SAMPLES (Defender Operational 阻斷樣本)](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES)<br>• [CyberDefenders: Spotlight (Defender 告警研判)](https://cyberdefenders.org/blueteam-ctf-challenges/spotlight/) |
| **🟡 L2** | **15.1 Splunk SPL 管道檢索與過濾最佳化**<br>(`index=`, `sourcetype=`, `eval`, `where`) | • [Splunk Boss of the SOC: BOTSv1 開源資料庫](https://github.com/splunk/botsv1)<br>• [Splunk Search Reference (SPL 核心手冊)](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference) |
| **🟡 L2** | **15.2 SPL 動態欄位提取與聚合統計分析**<br>(`rex field=_raw`, `stats count by`, `transaction`) | • [Splunk Boss of the SOC: BOTSv1 (SPL 欄位提取演練)](https://github.com/splunk/botsv1) |
| **🟡 L2** | **15.3 關聯分析規則建立與告警門檻設計**<br>(跨來源關聯、暴力破解成功後橫向移動告警) | • [Elastic Security Detection Rules 開源專案](https://github.com/elastic/detection-rules)<br>• [Splunk Security Content 關聯偵測分析庫](https://github.com/splunk/security_content) |
| **🟡 L2** | **15.4 巨量資安日誌基準線與異常偏離偵測**<br>(非上班時間異常存取、流量突增 Baseline 塑模) | • [Splunk BOTSv1 威脅 hunting 全流程演練](https://github.com/splunk/botsv1)<br>• [SANS SOC Anomaly Baseline Modeling 白皮書](https://www.sans.org/white-papers/) |
| **🟡 L2** | **16.1 DNS 隱蔽通道與外洩特徵鑑識**<br>(DNS Tunneling, dnscat2, 異常長子網域) | • [CyberDefenders: WireDive (PCAP 流量與異常封包鑑識)](https://cyberdefenders.org/blueteam-ctf-challenges/wiredive/)<br>• [MTA: 2020-09-02 DNS Tunneling 流量樣本分析](https://www.malware-traffic-analysis.net/)<br>• [`../exams/mock_exam_b_lab_questions.md`](../exams/mock_exam_b_lab_questions.md)（第 30~35 題：DNS 隧道推演） |
| **🟡 L2** | **16.2 C2 心跳模式與週期抖動分析**<br>(Cobalt Strike Beaconing, Jitter 抖動計算) | • [HTB Sherlocks: Knock Knock (勒索軟體 PCAP 網路鑑識)](https://app.hackthebox.com/sherlocks/Knock%20Knock)<br>• [MTA: 2024 C2 流量樣本專題實戰](https://www.malware-traffic-analysis.net/2024/index.html) |
| **🟡 L2** | **16.3 知名 N-day 漏洞利用封包逆推**<br>(Log4j JNDI 注入、ActiveMQ OpenWire) | • [CyberDefenders: OpenWire (ActiveMQ CVE-2023-46604 封包分析)](https://cyberdefenders.org/blueteam-ctf-challenges/openwire/)<br>• [Emerging Threats (ET Open Rules) 開源特徵規則庫](https://rules.emergingthreats.net/) |
| **🟡 L2** | **16.4 協定走私與反向代理混淆鑑識**<br>(HTTP Request Smuggling、WebSocket 隱蔽通道) | • [PortSwigger: HTTP Request Smuggling (協定走私防護實驗)](https://portswigger.net/web-security/request-smuggling)<br>• [Zeek 網路安全監控開源專案日誌排查](https://zeek.org/) |
| **🟡 L2** | **17.1 YARA 檔案二進位特徵碼規則撰寫**<br>(Strings, Hex, Wildcard, Condition 語法) | • [YARA 官方語法手冊與線上編輯器](https://yara.readthedocs.io/)<br>• [Florian Roth: Signature-Base 開源規則庫](https://github.com/Neo23x0/signature-base) |
| **🟡 L2** | **17.2 Sigma 通用日誌偵測規則與轉譯**<br>(YAML 語法、`sigmac` 轉譯 Splunk/Elastic) | • [SigmaHQ 官方開源規則庫 (數千條 ATT&CK 規則)](https://github.com/SigmaHQ/sigma)<br>• [Uncoder.io (在線 Sigma 轉譯引擎)](https://uncoder.io/)<br>• [Chainsaw 內嵌 Sigma 引擎即時獵捕實務](https://github.com/countercept/chainsaw) |
| **🟡 L2** | **17.3 Snort/Suricata 網路入侵特徵規則撰寫**<br>(Header, Content, Distance, Within, Flow, Pcre) | • [Emerging Threats (ET Open Rules) 開源特徵規則庫](https://rules.emergingthreats.net/)<br>• [Suricata User Guide 規則調校手冊](https://docs.suricata.io/) |
| **🟡 L2** | **17.4 偵測規則生命週期與誤判除錯**<br>(False Positive 抑制、基準線測試、覆蓋度評估) | • [Florian Roth: Detection Engineering 指南](https://github.com/Neo23x0)<br>• [MITRE ATT&CK Navigator 官方視覺化覆蓋工具](https://mitre-attack.github.io/attack-navigator/) |

## 🏹 區塊五：主動威脅獵捕、惡意樣本分流與無檔案防禦 (Threat Hunting, Malware Triage & Active Defense)
> 💡 **作戰任務**：主動出擊消滅潛伏威脅。涵蓋 Sysmon 端點獵捕、惡意二進位靜態分流、記憶體無檔案 (Fileless) 後門清剿、威脅情資 (CTI) 以及 CVSS 漏洞評分量化與重大 CVE 逆推。
>
> 📋 **本區塊核心領域說明 (Domains Overview)**：
>
> - [**領域 18：端點威脅獵捕**](learning_paths/block_5_threat_hunting_triage/18_threat_hunting_sysmon.md)：Sysmon Event 1/3/7/8 遙測、LOLBAS 合法程式白利用排查與 CreateRemoteThread 注入。
> - [**領域 19：惡意程式靜態分流 (Triage)**](learning_paths/block_5_threat_hunting_triage/19_malware_static_triage.md)：PE 結構區段表、Shannon 資訊熵加殼辨識與 Win32 API 導入表功能逆推。
> - [**領域 20：Web 無檔案防禦**](learning_paths/block_5_threat_hunting_triage/20_web_fileless_defense.md)：Tomcat Filter/Servlet 內存馬原理與 Arthas 記憶體反編譯排查。
> - [**領域 21：威脅情資 (CTI)**](learning_paths/block_5_threat_hunting_triage/21_cyber_threat_intelligence.md)：Bianco 痛苦之塔 (Pyramid of Pain)、MITRE ATT&CK 戰術映射與主動獵捕假說。
> - [**領域 22：漏洞通用評分系統 (CVSS) 與重大 CVE 剖析**](learning_paths/block_5_threat_hunting_triage/22_cvss_metrics_cve_analysis.md)：CVSS v3.1 基本指標計算、Log4Shell 滿分 10.0 逆推與 Heartbleed。

| 難度 | 細分實戰技術點 (Sub-Topic & Technique) | 🎯 具體線上靶場、實戰房間、開源數據集與題目清單 (Practicable Challenges & Labs) |
| :---: | :--- | :--- |
| **🟡 L2** | **18.1 Sysmon 驅動級進程遙測與命令行**<br>(Event ID 1 Process Creation / Hash 計算) | • [sbousseaden/EVTX-ATTACK-SAMPLES (EID 1 樣本分析)](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES)<br>• [Chainsaw 快速日誌獵捕工具實操](https://github.com/countercept/chainsaw) |
| **🟡 L2** | **18.2 合法程式白利用 (LOLBAS) 特徵識別**<br>(`certutil -urlcache`, `powershell -enc`, `wmic`) | • [LOLBAS 專案特徵對照庫](https://lolbas-project.github.io/)<br>• [DeepBlueCLI (PowerShell 官方日誌排查開源專案)](https://github.com/sans-blue-team/DeepBlueCLI)<br>• [Hayabusa (日誌即時偵測引擎)](https://github.com/Yamato-Security/hayabusa) |
| **🟡 L2** | **18.3 系統持久化與排程任務建立審查**<br>(Scheduled Tasks, RunKey, WMI Event) | • [sbousseaden/EVTX-ATTACK-SAMPLES (排程任務建立事件樣本)](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES)<br>• [Sysinternals Autoruns 命令列鑑識工具手冊](https://learn.microsoft.com/sysinternals/) |
| **🟡 L2** | **18.4 處理程序代碼注入與遠端執行緒監控**<br>(Sysmon Event ID 8 CreateRemoteThread / EID 10) | • [sbousseaden/EVTX-ATTACK-SAMPLES (Process Injection 專題)](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES)<br>• [SigmaHQ Process Injection 規則庫](https://github.com/SigmaHQ/sigma) |
| **🟡 L2** | **19.1 PE 結構、區段屬性與雜湊特徵**<br>(PE Header, Import Table, Imphash, SSDEEP) | • [CyberDefenders: Maldoc101 (惡意文件分析實戰)](https://cyberdefenders.org/blueteam-ctf-challenges/maldoc101/)<br>• [PE-bear 工具靜態剖析 PE Section 實戰手冊](https://github.com/hasherezade/pe-bear) |
| **🟡 L2** | **19.2 程式碼混淆還原與字串解密**<br>(CyberChef Recipes, Base64/XOR/ROT 逆推) | • [CyberChef 官方在線工具 (解密特徵食譜)](https://gchq.github.io/CyberChef/)<br>• [Mandiant FLOSS (字串混淆自動提取工具手冊)](https://github.com/mandiant/flare-floss) |
| **🟡 L2** | **19.3 文件型惡意巨集與內嵌物件萃取**<br>(PDF JavaScript 注入、RTF 漏洞利用、OLE 串流) | • [Didier Stevens: pdf-parser 開源腳本解析](https://blog.didierstevens.com/programs/pdf-tools/)<br>• [ViperMonkey VBA 巨集模擬執行框架手冊](https://github.com/decalage2/ViperMonkey) |
| **🟡 L2** | **19.4 動態沙箱行為報告解讀**<br>(API Hooking 序列、釋放二進位檔案、連線行為) | • [ANY.RUN 公開惡意樣本沙箱資料庫](https://any.run/)<br>• [Hybrid Analysis 公開自動化沙箱報告庫](https://www.hybrid-analysis.com/) |
| **🔴 L3** | **20.1 Java Filter/Servlet 內存馬清剿**<br>(Alibaba Arthas JVM 掛載、`sc` 列舉、`jad` 反編譯) | • [Alibaba Arthas 官方開源工具庫與實機演練](https://arthas.aliyun.com/)<br>• [Neo23x0/Loki (IOC / Webshell 開源掃描器)](https://github.com/Neo23x0/Loki)<br>• `07_藍隊防禦與護網營運/03_日誌與告警研判/Web日誌分析與逃逸檢測/` |
| **🔴 L3** | **20.2 加密 WebShell 流量辨析與日誌還原**<br>(冰蠍 Behinder / 哥斯拉 Godzilla 流量解密) | • [PortSwigger: File Upload Attacks (Webshell 上傳防禦實驗)](https://portswigger.net/web-security/file-upload)<br>• [`../exams/mock_exam_b_lab_questions.md`](../exams/mock_exam_b_lab_questions.md)（第 15~23 題） |
| **🔴 L3** | **20.3 .NET 與 PHP 內存馬無檔案後門排查**<br>(IIS 模組注入、PHP 記憶體執行碼檢測) | • [CyberDefenders: OpenWire (Web 漏洞日誌鑑識)](https://cyberdefenders.org/blueteam-ctf-challenges/openwire/)<br>• [tennc/webshell 知名 WebShell 鑑識特徵庫](https://github.com/tennc/webshell) |
| **🔴 L3** | **21.1 威脅指標管理與 ATT&CK 戰術映射**<br>(IOC 提取、MISP 共享、ATT&CK 導航器) | • [OpenCTI 官方開源平台 (威脅情資知識庫)](https://github.com/OpenCTI-Platform/opencti)<br>• [OpenCTI (開源威脅情資在線知識庫)](https://www.opencti.io/) |
| **🔴 L3** | **21.2 攻擊者基礎設施拓撲關聯追蹤**<br>(Passive DNS 歷史解析、JARM SSL 指紋比對) | • [salesforce/jarm (TLS 伺服器指紋開源掃描工具)](https://github.com/salesforce/jarm)<br>• [Shodan Community (連網設備檢索)](https://www.shodan.io/) |
| **🔴 L3** | **21.3 APT 組織特徵畫像與獵捕假說建立**<br>(威脅狩獵假說驅動、TTP 矩陣對抗映射) | • [MITRE CAR (Cyber Analytics Repository 官方分析庫)](https://car.mitre.org/)<br>• [OTRF ThreatHunter-Playbook (開源狩獵劇本庫)](https://github.com/OTRF/ThreatHunter-Playbook) |
| **🟡 L2** | **22.1 CVSS v3.1 / v4.0 基本指標群與漏洞評分計算**<br>(AV、AC、PR、UI、Scope/MSI/MSA、CIA 權重計算與嚴重度量化) | • [FIRST.org: 官方 CVSS v3.1 評分計算機與規格書](https://www.first.org/cvss/calculator/3.1)<br>• [NVD (NIST): Common Vulnerability Scoring System 評分實例庫](https://nvd.nist.gov/vuln-metrics/cvss)<br>• [FIRST.org: 最新 CVSS v4.0 計算機與指標評級手冊](https://www.first.org/cvss/calculator/4.0) |
| **🟡 L2** | **22.2 歷史重大 CVE 運作機制逆推**<br>(Log4Shell CVE-2021-44228 JNDI/LDAP、Heartbleed CVE-2014-0160、Spring4Shell) | • [MITRE CVE 官方庫: CVE-2021-44228 Log4Shell 核心定義](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44228)<br>• [Vulhub: 開源一鍵 CVE 漏洞複現靶場集合](https://vulhub.org/)<br>• [picoCTF: CVE-XXXX-XXXX (ID: 396)](https://learn.cylabacademy.org/library?search=CVE-XXXX-XXXX) |

## 🔬 區塊六：深度數位鑑識、主機核心與行動取證 (Digital Forensics & Incident Response - DFIR)
> 💡 **作戰任務**：還原入侵現場之決定性鐵證。涵蓋 Volatility 揮發性記憶體取證、NTFS 磁碟神器鑑識、Linux 核心 Rootkit 破譯與行動裝置提取。
>
> 📋 **本區塊核心領域說明 (Domains Overview)**：
>
> - [**領域 23：記憶體鑑識實戰**](learning_paths/block_6_dfir_memory_disk/23_memory_forensics.md)：EPROCESS 雙向鏈表、VAD 二元樹、Volatility 3 核心 Plugin 與 DKOM 斷鏈隱蔽排查。
> - [**領域 24：磁碟檔案系統鑑識**](learning_paths/block_6_dfir_memory_disk/24_disk_filesystem_forensics.md)：NTFS `$MFT`、`$SI` vs `$FN` 時間偽造辨析與 Prefetch/ShimCache/Amcache 三大鐵證。
> - [**領域 25：Linux 核心鑑識**](learning_paths/block_6_dfir_memory_disk/25_linux_kernel_forensics.md)：LKM 核心模組 Rootkit、/etc/ld.so.preload 劫持與 eBPF 核心級追蹤。
> - [**領域 26：行動裝置取證 (Mobile)**](learning_paths/block_6_dfir_memory_disk/26_mobile_device_forensics.md)：APK 靜態解包、classes.dex 反編譯、SQLite 快取分析與 iOS Keychain。

| 難度 | 細分實戰技術點 (Sub-Topic & Technique) | 🎯 具體線上靶場、實戰房間、開源數據集與題目清單 (Practicable Challenges & Labs) |
| :---: | :--- | :--- |
| **🟡 L2** | **23.1 隱藏進程與 DKOM 斷鏈破譯**<br>(`pslist` 雙向鏈表 vs `psscan` 核心搜尋) | • [CyberDefenders: RedLine (記憶體進程分析)](https://cyberdefenders.org/blueteam-ctf-challenges/redline/)<br>• [SANS Memory Forensics Cheat Sheet (進程斷鏈篇)](https://www.sans.org/posters/memory-forensics-cheat-sheet/)<br>• [`../exams/mock_exam_b_lab_questions.md`](../exams/mock_exam_b_lab_questions.md)（第 1~3 題） |
| **🟡 L2** | **23.2 代碼注入與 VAD 記憶體屬性排查**<br>(`malfind` / `PAGE_EXECUTE_READWRITE`) | • [CyberDefenders: Spotlight (VAD 結構注入定位)](https://cyberdefenders.org/blueteam-ctf-challenges/spotlight/)<br>• [Volatility 3 `windows.malfind` 官方範例解析庫](https://volatility3.readthedocs.io/) |
| **🟡 L2** | **23.3 核心網路連線還原與二進位導出**<br>(`netscan` / `dumpfiles` 提取 Payload) | • [CyberDefenders: DeepDive (進階記憶體取證)](https://cyberdefenders.org/blueteam-ctf-challenges/deepdive/)<br>• [DFIR Madness: Case 001 (開源記憶體映像檔實戰)](https://dfirmadness.com/case-001-the-stolen-szechuan-sauce/)<br>• [Volatility 3 `windows.netscan` 實機演練手冊](https://volatility3.readthedocs.io/) |
| **🟡 L2** | **23.4 記憶體憑證抓取與暫存區取證**<br>(`hashdump`、`lsadump`、剪貼簿與命令列歷程提取) | • [Gentilkiwi Mimikatz 記憶體特徵對照庫](https://github.com/gentilkiwi/mimikatz)<br>• [CyberDefenders: Spotlight (記憶體憑證抓取分析)](https://cyberdefenders.org/blueteam-ctf-challenges/spotlight/) |
| **🟡 L2** | **24.1 NTFS 主檔案表與時間戳偽造辨析**<br>(`$MFT` / `$STANDARD_INFORMATION` vs `$FILE_NAME`) | • [HTB Sherlocks: BFT (MFT 主檔案表與 Timestomping 深度鑑識)](https://app.hackthebox.com/sherlocks/BFT)<br>• [Eric Zimmerman's MFTECmd 實機解析演練](https://ericzimmerman.github.io/)<br>• [`../exams/mock_exam_b_lab_questions.md`](../exams/mock_exam_b_lab_questions.md)（第 12~14 題） |
| **🟡 L2** | **24.2 程式執行三大鐵證深度鑑識**<br>(Prefetch `.pf`、Amcache、Shimcache) | • [Eric Zimmerman's PECmd & AmcacheParser 工具鏈實作](https://ericzimmerman.github.io/)<br>• [CyberDefenders: Spotlight (檔案系統執行鐵證取證)](https://cyberdefenders.org/blueteam-ctf-challenges/spotlight/)<br>• [ShimcacheParser 開源取證腳本實操](https://github.com/mandiant/ShimCacheParser) |
| **🟡 L2** | **24.3 使用者活動軌跡與登錄檔鑑識**<br>(Registry RunKey / USBSTOR / Shellbags) | • [HTB Sherlocks: Latus (RDP 連線日誌、註冊表分析)](https://app.hackthebox.com/sherlocks/Latus)<br>• [NIST CFReDS: Hacking Case Datasets (官方磁碟映像檔)](https://cfreds.nist.gov/)<br>• [Eric Zimmerman's Registry Explorer 與 ShellBags Explorer 演練](https://ericzimmerman.github.io/) |
| **🟡 L2** | **24.4 系統更新日誌與陰影複製取證**<br>(`$LogFile`、`$UsnJrnl`、VSS Volume Shadow Copy) | • [Eric Zimmerman's USNParser 實戰演練](https://ericzimmerman.github.io/)<br>• [SANS SIFT Workstation 鑑識工作站手冊](https://www.sans.org/tools/sift-workstation/) |
| **🔴 L3** | **25.1 Linux 核心模組 Rootkit 與隱蔽技術**<br>(LKM Hooking, `LD_PRELOAD` 動態庫劫持) | • [CyberDefenders: Hacked (Linux 伺服器入侵鑑識與持久化分析)](https://cyberdefenders.org/blueteam-ctf-challenges/hacked/)<br>• [chkrootkit / rkhunter (Linux 核心模組檢測)](http://www.chkrootkit.org/) |
| **🔴 L3** | **25.2 用戶態動態庫劫持與防禦**<br>(`LD_PRELOAD` 環境變數、`/etc/ld.so.preload` 攔截) | • [OverTheWire: Bandit (Level 26~32 動態庫與權限實務)](https://overthewire.org/wargames/bandit/) |
| **🔴 L3** | **25.3 雲原生 eBPF 核心級威脅偵測**<br>(Falco 規則編寫、系統呼叫攔截分析) | • [Falco 官方專案 (雲原生 eBPF 運行時威脅偵測引擎)](https://falco.org/) |
| **🔴 L3** | **25.4 Linux 記憶體採集與符號表還原**<br>(LiME 核心模組採集、Volatility 3 ISF 符號生成) | • [LiME (Linux Memory Extractor 開源採集工具)](https://github.com/504ensicsLabs/LiME)<br>• [Volatility 3 Linux 記憶體取證實戰指引](https://volatility3.readthedocs.io/) |
| **🔴 L3** | **26.1 Android APK 惡意行為與靜態解包**<br>(APK 靜態解包、Manifest 權限審查、JADX 反編譯) | • [NIST CFReDS: Mobile Device Datasets (官方手機取證鏡像)](https://cfreds.nist.gov/)<br>• [skylot/jadx (開源 APK 反編譯工具鏈)](https://github.com/skylot/jadx) |
| **🔴 L3** | **26.2 Android 系統執行時日誌與暫存提取**<br>(ADB Logcat 鑑識、SQLite 資料庫剖析、通訊歷程) | • [DB Browser for SQLite (行動通訊歷程資料庫鑑識)](https://sqlitebrowser.org/) |
| **🔴 L3** | **26.3 iOS 備份檔案與鑰匙圈取證分析**<br>(iTunes 備份解構、Keychain 取證、位置軌跡還原) | • [NIST CFReDS: iOS Test Image (官方測試映像檔)](https://cfreds.nist.gov/)<br>• [libimobiledevice 開源取證通訊協定庫](https://libimobiledevice.org/) |

## ⚔️ 區塊七：持續防禦驗證、紫隊協同與全真對抗 (Continuous Validation, Purple Teaming & Cyber Range)
> 💡 **作戰任務**：以實戰檢驗防禦體系。涵蓋 BAS 自動化對抗測試、紫隊協同實踐以及企業級 Cyber Range 全真綜合演練。
>
> 📋 **本區塊核心領域說明 (Domains Overview)**：
>
> - [**領域 27：防禦驗證工程**](learning_paths/block_7_purple_team_range/27_purple_team_breach_simulation.md)：Atomic Red Team 原子化對抗測試、MITRE Caldera 與遙測覆蓋率量化。
> - [**領域 28：全真綜合演練**](learning_paths/block_7_purple_team_range/28_enterprise_cyber_range.md)：Splunk BOTSv2/v3 實網數據集、跨主機橫向移動全局溯源與金盾獎全真模擬。

| 難度 | 細分實戰技術點 (Sub-Topic & Technique) | 🎯 具體線上靶場、實戰房間、開源數據集與題目清單 (Practicable Challenges & Labs) |
| :---: | :--- | :--- |
| **👑 L4** | **27.1 自動化對抗測試與遙測完整度評估**<br>(Atomic Red Team 自動化對抗模擬) | • [Red Canary: Atomic Red Team (對齊 ATT&CK 之單元測試庫)](https://github.com/redcanaryco/atomic-red-team)<br>• [Invoke-AtomicRedTeam (PowerShell 執行框架)](https://github.com/redcanaryco/invoke-atomicredteam) |
| **👑 L4** | **27.2 自動化攻擊模擬平台佈建與排程**<br>(MITRE CALDERA 攻擊路徑模擬、藍隊告警反應驗證) | • [MITRE CALDERA (開源自動化對抗模擬系統)](https://github.com/mitre/caldera)<br>• [guardicore/monkey (開源橫向移動模擬演練平台)](https://github.com/guardicore/monkey) |
| **👑 L4** | **27.3 Purple Teaming 紫隊協同演練實務**<br>(攻擊破壞與防守即時規則驗證、覆蓋率量化) | • [MITRE CTI 官方威脅技術矩陣對照庫](https://github.com/mitre/cti)<br>• [VECTR (紫隊演練成果量化與追蹤系統)](https://vectr.io/) |
| **👑 L4** | **28.1 端到端 APT 攻擊鏈全局溯源與奪旗**<br>(Initial Access ➔ Privilege Escalation ➔ C2 ➔ Data Exfil) | • [SANS Holiday Hack Challenge (KringleCon 全真 DFIR 攻防奪旗賽)](https://www.sans.org/mlp/holiday-hack-challenge/)<br>• [Digital Corpora (DFRWS 歷年真實硬碟/記憶體/網路映像檔)](https://digitalcorpora.org/) |
| **👑 L4** | **28.2 大規模企業級實網攻防對抗資料集**<br>(Splunk Boss of the SOC: BOTSv2 & BOTSv3) | • [Splunk Boss of the SOC: BOTSv2 官方資料集](https://github.com/splunk/botsv2)<br>• [Splunk Boss of the SOC: BOTSv3 官方資料集](https://github.com/splunk/botsv3)<br>• [OpenSOC 官方社群公開資料庫](https://github.com/opensoc) |
| **👑 L4** | **28.3 跨主機橫向移動與多源鑑識綜合歸因**<br>(端點日誌 + 封包流量 + 記憶體混合鑑識題組) | • [HTB Sherlocks 跨主機混合攻防調查場景](https://app.hackthebox.com/sherlocks)<br>• [CyberDefenders: DeepDive 綜合關卡](https://cyberdefenders.org/blueteam-ctf-challenges/deepdive/) |
| **👑 L4** | **28.4 台灣資安法規與實體攻防檢定真題演練**<br>(台灣資通安全事件通報、實體推演題本與答案解構) | • [`../exams/mock_exam_b_lab_questions.md`](../exams/mock_exam_b_lab_questions.md)（全套 81 題實體推演）<br>• [`../exams/mock_exam_b_lab_solutions.md`](../exams/mock_exam_b_lab_solutions.md)<br>• [`../exams/mock_exam_a_100q_questions.md`](../exams/mock_exam_a_100q_questions.md) |

## 📜 區塊八：法規遵循、合規治理與數位證據監管 (GRC, Standards & Chain of Custody)
> 💡 **作戰任務**：企業與國家級合規治理與法律保障。涵蓋 ISO/IEC 27037 證據監管鏈、台灣《資通安全管理法》與責任等級制、台灣《個人資料保護法》以及 ISO 27001 / NIST CSF 國際標準框架。
>
> 📋 **本區塊核心領域說明 (Domains Overview)**：
>
> - [**領域 29：數位證據法規與監管鏈**](learning_paths/block_8_grc_standards_custody/29_digital_evidence_chain_of_custody.md)：RFC 3227 數據揮發次序、ISO/IEC 27037 標準與防寫設備雙雜湊驗證。
> - [**領域 30：台灣《資通安全管理法》與責任等級制**](learning_paths/block_8_grc_standards_custody/30_cyber_security_management_act.md)：A~E 級責任等級劃分、專職配置與受訓時數、1~4 級事件「1 小時法定通報時限」。
> - [**領域 31：《個人資料保護法》與隱私安全架構**](learning_paths/block_8_grc_standards_custody/31_personal_data_protection_frameworks.md)：六大特種個資法定除外要件、個資外洩罰則、ISO 27001:2022 與 NIST CSF 2.0。

| 難度 | 細分實戰技術點 (Sub-Topic & Technique) | 🎯 具體線上靶場、實戰房間、開源數據集與題目清單 (Practicable Challenges & Labs) |
| :---: | :--- | :--- |
| **🟢 L1** | **29.1 數位證據監管鏈與 ISO/IEC 27037**<br>(證據識別、收集、獲取與保存標準程序) | • [NIST SP 800-86: 數位鑑識整合指引手冊](https://csrc.nist.gov/publications/detail/sp/800-86/final)<br>• [DFRWS 數位證據監管鏈標準指引範本](https://dfrws.org/)<br>• [`../exams/mock_exam_a_100q_questions.md`](../exams/mock_exam_a_100q_questions.md)（鑑識法規題群） |
| **🟢 L1** | **29.2 資安事件通報時限與 RFC 3227**<br>(1~4 級事件 1 小時通報、數據揮發次序) | • [國家資通安全研究院: 資安事件分級指引](https://www.nics.nat.gov.tw/)<br>• [SANS Incident Handler's Handbook 應變步驟](https://www.sans.org/white-papers/)<br>• [`../exams/high_frequency_flashcards.md`](../exams/high_frequency_flashcards.md) |
| **🟢 L1** | **29.3 證據真偽性與鑑識複製完整性驗證**<br>(防寫設備 Write Blocker、雙重雜湊 MD5+SHA256) | • [Autopsy 官方開源取證訓練樣本庫](https://www.autopsy.com/)<br>• [FTK Imager 映像檔製作與雜湊比對指南](https://www.exterro.com/digital-forensics-software/ftk-imager)<br>• [NIST CFTT 鑑識複製驗證測試數據集](https://www.cftt.nist.gov/) |
| **🟢 L1** | **30.1 《資通安全管理法》體系與公務/特定非公務機關權利義務**<br>(CISO 設置規範、資通安全維護計畫、關鍵基礎設施 CI 提供者責任) | • [全國法規資料庫: 《資通安全管理法》母法現行條文全文](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=A0030297)<br>• [數位發展部資通安全署: 資通安全管理法專區與法遵指引](https://moda.gov.tw/ACS/)<br>• [Yamol: 公共數位歷屆公務人員高考、技師與金盾獎資通法規歷屆考古題庫](https://yamol.tw/) |
| **🟢 L1** | **30.2 資通安全責任等級分級辦法**<br>(A~E 級劃分標準、專職人員配置、每人每年受訓時數、ISO 27001 導入與驗證期限) | • [全國法規資料庫: 《資通安全責任等級分級辦法》法規條文與附表標準](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=A0030300)<br>• [iPAS 資訊安全工程師: 能力鑑定官方考試指引與法規試題大綱](https://www.ipas.org.tw/)<br>• [Yamol: iPAS 資訊安全法規與責任等級歷屆模擬題庫](https://yamol.tw/) |
| **🟢 L1** | **30.3 資通安全事件通報及應變辦法**<br>(1~4 級資安事件定義、法定 1 小時內通報時限、36h 損害控制與 72h 復原規範) | • [全國法規資料庫: 《資通安全事件通報及應變辦法》條文與通報流程圖](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=A0030301)<br>• [TWCERT/CC 台灣電腦網路危機處理暨協調中心: 資安事件通報與協處作業指引](https://www.twcert.org.tw/) |
| **🟢 L1** | **31.1 《個人資料保護法》特種個資定義與法定除外要件**<br>(病歷/醫療/基因/性生活/健康檢查/犯罪前科六大特種個資之蒐集處理利用限制) | • [全國法規資料庫: 《個人資料保護法》最新修正條文](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021)<br>• [國家發展委員會: 個人資料保護法解析手冊與問答集](https://www.ndc.gov.tw/)<br>• [Yamol: 金盾獎初賽特種個資與個人資料保護歷屆題庫](https://yamol.tw/) |
| **🟢 L1** | **31.2 個資外洩通報時限、當事人權利與損害賠償上限**<br>(當事人查閱/複製/更正/刪除五大權利、外洩查明通知、每人 500~2萬、最高總額 2 億元) | • [全國法規資料庫: 《個人資料保護法施行細則》第 22 條外洩通知規定](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050022)<br>• [司法院法學資料檢索系統: 個資外洩損害賠償裁判書研析](https://judgment.judicial.gov.tw/) |
| **🟢 L1** | **31.3 國際資安管理與網路安全框架**<br>(ISO/IEC 27001:2022 控制項四大面向、NIST CSF 2.0 Govern+IPDRR 六大核心功能) | • [NIST 官方: Cybersecurity Framework (CSF) 2.0 官方參考套件](https://www.nist.gov/cyberframework)<br>• [ISO/IEC 27001: 資訊安全管理系統國際標準架構解析](https://en.wikipedia.org/wiki/ISO/IEC_27001)<br>• [Yamol: NIST CSF 與 ISO 27001 控制措施歷屆認證試題](https://yamol.tw/) |
