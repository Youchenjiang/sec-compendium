# 🛡️ 30days_sprint_roadmap.md (金盾獎 30 天極速衝刺課表)

> [!IMPORTANT]
> **發布版本**: `v2.1` (全網權威連結完整對接版)  
> **適用週期**: 2026-09-10 ～ 2026-10-10（倒數 30 天直攻 10 月中旬金盾獎初賽）  
> **真實考場規則**:
> 1. **題型規格**: **100 題單選題**，限時 90 分鐘～2 小時，**完全斷網閉卷 (No Internet)**，答錯不倒扣。
> 2. **晉級門檻**: 全國大專院校取**前 30～40 隊晉級決賽**。
> 3. **衝刺節奏**: **維持每 2 天為 1 個 Run**（30 天共 15 個 Run），落實 3 人主修領域包幹制，以實作內化記憶。
> 4. **讀書會聚會三部曲 (每 Run 第一天 22:00 線上聚會 90 分鐘)**:
>    * ⏱️ **00~25 分鐘**：3 人各自進行 5~8 分鐘實作亮點展示（示範封包截圖、Volatility 外掛結果或 Exploit）。
>    * ⏱️ **25~70 分鐘**：三人同步進行 **30~50 題限時單選情境模擬對戰**，當場錯題直接由該領域主修隊員解說！
>    * ⏱️ **70~90 分鐘**：檢討盲點、確認下一個 Run 的分工與靶場排錯。
> 5. **內部離線教材索引**: 課表中提及之「本地」教材與 PDF 講義目錄，完整索引請參見 👉 [【資料來源總索引 (sources_index.md)】](../90_runs/sources_index.md)。

---

## 👥 3 人小隊角色定位與包幹責任表

| 角色編號 | 核心主修領域 (Primary Domain) | 負責實作平台與武器庫 | 金盾初賽守備範圍 |
| :---: | :--- | :--- | :--- |
| **隊員 A** | **Web 應用安全 ＋ 資安法規與雲端治理 (GRC)** | picoCTF / PortSwigger / [iPAS 題庫 (法規管理)](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E7%AE%A1%E7%90%86%E6%A6%82%E8%AB%96%E2%97%86%E5%88%9D%E7%B4%9A-5273.htm) | OWASP Top 10、資通安全管理法、責任等級制、事件通報時限、個資法、IaaS/PaaS/SaaS 雲端責任模型 |
| **隊員 B** | **系統安全 ＋ 數位鑑識 (Forensics) ＋ 藍隊防禦工具** | [CyberDefenders](https://cyberdefenders.org/) / [Volatility 3](https://github.com/volatilityfoundation/volatility3) / [Autopsy](https://tryhackme.com/room/autopsy2handsdown) / [THM](https://tryhackme.com/) | 記憶體鑑識、NTFS MFT 磁碟鑑識、Windows Event Log、RFC 3227 揮發順序、Tripwire/Sysmon/Snort 工具對照 |
| **隊員 C** | **網路硬體與協定安全 ＋ 密碼學與 PKI 架構** | [Wireshark](https://www.wireshark.org/) / [MTA 流量分析](https://www.malware-traffic-analysis.net/) / [CryptoHack](https://cryptohack.org/) / [CyberChef](https://gchq.github.io/CyberChef/) | TCP/IP 三向交握、Switch Port-Security/VLAN、VPN 種類 (PPTP/IPsec/SSL)、SNMP v3、TLS 1.3、RSA/AES |

---

## 🗓️ 30 天極速衝刺課表 (15 個 Run 逐日完整規劃)

---

### ⚔️ **Run 1 (Day 1-2, 09/10-09/11): 網路封包與交換機安全 ＆ 資通安全法體系入門**
🌐 **本 Run 核心目標**: 建立 Wireshark 抓包手感，掌握三向交握狀態機、交換機 Port-Security 與《資通安全管理法》基礎架構。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 1** (09/10) | **TCP/IP 協定棧與三向交握**<br>SYN/ACK 旗標流轉、Wireshark 語法與交換機安全 | • **隊員 A**: [picoCTF: Insp3ct0r (ID: 18)](https://learn.cylabacademy.org/library?search=Insp3ct0r) 暖手 HTTP 標頭<br>• **隊員 B**: [THM: Windows Event Logs](https://tryhackme.com/room/windowseventlogs) 實作檢視 Security 4624/4625<br>• **隊員 C**: [THM: Wireshark 101](https://tryhackme.com/room/wireshark101) 實作過濾 `tcp.flags.syn==1` | • **三向交握狀態**：LISTEN ➔ SYN_SENT ➔ SYN_RCVD ➔ ESTABLISHED。<br>• **四向揮手**：FIN_WAIT_1/2、TIME_WAIT（解決延遲抵達封包，持續 2MSL）。<br>• **Switch Port-Security 違規處理三模式 (必考)**：<br>  1. `Protect`: 丟棄未授權封包，不發 SNMP Trap，不記錄日誌。<br>  2. `Restrict`: 丟棄未授權封包，**會發送 SNMP Trap** 並增加違規計數。<br>  3. `Shutdown` (預設): **直接將埠關閉 (進入 err-disable 狀態)**，發送 Trap 並記錄日誌。 |
| **Day 2** (09/11) | **《資通安全管理法》基本架構**<br>公務機關 vs 特定非公務機關之定義與權利義務 | • **隊員 A**: 刷 [阿摩 iPAS 資安管理與法規題庫 (初級)](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E7%AE%A1%E7%90%86%E6%A6%82%E8%AB%96%E2%97%86%E5%88%9D%E7%B4%9A-5273.htm) 15 題 ＋ 研讀 [全國法規資料庫: 資通安全管理法](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=A0030294)<br>• **隊員 B**: 參考 [GitHub: Volatility 3 官方倉庫](https://github.com/volatilityfoundation/volatility3) 部署本機環境<br>• **隊員 C**: 下載 [MTA 流量分析教學庫](https://www.malware-traffic-analysis.net/tutorials/index.html) 練習追蹤 TCP Stream | • **特定非公務機關範圍**：關鍵基礎設施提供者、公營事業、政府捐助之財團法人。<br>• **資通安全長（CISO）設置**：公務機關應置資通安全長，由副首長或幕僚長兼任。<br>• **VLAN 802.1Q**：在乙太網路訊框中插入 4 Bytes Tag（包含 12 bits VLAN ID，支援 4096 個 VLAN）。 |

---

### ⚔️ **Run 2 (Day 3-4, 09/12-09/13): 數位鑑識揮發順序 ＆ 經典 Web 注入實戰**
🌐 **本 Run 核心目標**: 實作 SQL 注入原理，理解 RFC 3227 資料揮發順序與記憶體獲取標準程序。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 3** (09/12) | **RFC 3227 數據揮發順序 (Order of Volatility)**<br>現場數位證據獲取先後次序與合法性規範 | • **隊員 A**: [picoCTF: Web Gauntlet (ID: 88)](https://learn.cylabacademy.org/library?search=Web%20Gauntlet) SQL 注入過濾繞過<br>• **隊員 B**: 研讀本地 `../../../security/practice/exams/mock_exam_b_lab_questions.md`（第 1~10 題 IR 證據鏈）<br>• **隊員 C**: [CryptoHack: XOR Starter](https://cryptohack.org/challenges/introduction/) 熟練位元運算 | • **RFC 3227 順序 (100% 必考排序題)**：<br>  1. 暫存器與快取 (Registers/Cache)<br>  2. 路由表、ARP 快取、進程表、核心記憶體 (RAM)<br>  3. 暫時檔案系統 (Temporary File Systems)<br>  4. 磁碟 (Disks)<br>  5. 遠端日誌與監控資料<br>  6. 實體配置拓撲、網路纜線 |
| **Day 4** (09/13) | **SQL Injection 防禦架構 (Prepared Statement)**<br>參數化查詢底層原理與 WAF 防禦繞過 | • **隊員 A**: 參考 [OWASP SQLi 預防指引](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) 撰寫 Python PDO 參數化查詢<br>• **隊員 B**: 研讀 [Volatility 3 官方指令手冊](https://volatility3.readthedocs.io/en/latest/) (`pslist`, `pstree`, `netscan`)<br>• **隊員 C**: 參考 [Wireshark Display Filters 官方手冊](https://www.wireshark.org/docs/dfref/) 分析 SQL 盲注特徵與 URL 編碼 | • SQLi 防護最佳實踐是「參數化查詢 (Prepared Statements)」，將代碼與數據分開編譯；單純字串過濾與黑名單極易被繞過。 |

---

### ⚔️ **Run 3 (Day 5-6, 09/14-09/15): 惡意流量實戰分析 ＆ Windows 安全日誌核心**
🌐 **本 Run 核心目標**: 透過 MTA 真實 pcap 分析惡意感染鏈，精準識別 Windows Event ID。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 5** (09/14) | **Windows 重要安全性 Event ID 判讀**<br>身分驗證失敗、特權指派與惡意服務建立特徵 | • **隊員 A**: [picoCTF: SQLiLite (ID: 304)](https://learn.cylabacademy.org/library?search=SQLiLite)<br>• **隊員 B**: 參考 [Microsoft Learn: Event ID 4625 稽核登入失敗](https://learn.microsoft.com/zh-tw/windows/security/threat-protection/auditing/event-4625) 篩選暴力破解次數<br>• **隊員 C**: [MTA 2024 惡意流量實戰題目](https://www.malware-traffic-analysis.net/2024/index.html) 提取可疑 EXE | • **Windows Event ID 核心清單 (必背)**：<br>  • `4624`: 帳戶成功登入 (Logon Type 2 本地, 3 網路共享, 10 RDP 遠端桌面)<br>  • `4625`: 登入失敗 (暴力破解或字典攻擊識別指標)<br>  • `4672`: 指派特殊權限 (管理員登入)<br>  • `4720`: 建立使用者帳戶 (攻擊者留後門)<br>  • `7045`: 系統安裝新服務 (常見於木馬與勒索軟體持久化) |
| **Day 6** (09/15) | **惡意網路連線模式分析 (C2 Beaconing)**<br>固定週期發送、DNS Fast Flux 與 HTTP 心跳特徵 | • **隊員 A**: 研讀 [全國法規資料庫: 資通安全事件通報及應變辦法](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=A0030297) 時限表<br>• **隊員 B**: [CyberDefenders: RedLine Lab](https://cyberdefenders.org/blueteam-ctf-challenges/redline/) 實作記憶體分析<br>• **隊員 C**: 參考 [Wireshark User's Guide: TCP Analysis](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html) 計算封包抵達時間差抓 C2 | • **DNS Fast Flux**：惡意集團利用極短的 TTL（如 60 秒）頻繁變更 A 記錄的 IP 地址，將域名對應到全球多台被感染的主機，躲避 IP 黑名單封鎖。<br>• **水坑攻擊 (Watering Hole)**：攻擊者先入侵目標群體經常訪問的合法網站並植入惡意代碼，守株待兔等待受害者上鉤。 |

---

### ⚔️ **Run 4 (Day 7-8, 09/16-09/17): 記憶體鑑識實戰 ＆ 資安責任等級制 (A~E 級)**
🌐 **本 Run 核心目標**: 實作 Volatility 記憶體還原，掌握台灣資通安全責任等級規範與配置義務。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 7** (09/16) | **Volatility 記憶體鑑識標準步驟**<br>進程樹檢視、DLL 隱藏模組與已建立網路連線提取 | • **隊員 A**: 刷 [阿摩 iPAS 責任等級與防護題庫 (初級管理)](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E7%AE%A1%E7%90%86%E6%A6%82%E8%AB%96%E2%97%86%E5%88%9D%E7%B4%9A-5273.htm) 15 題<br>• **隊員 B**: 實作 [CyberDefenders: RedLine Lab](https://cyberdefenders.org/blueteam-ctf-challenges/redline/) 實戰提取 `oneetx.exe` 注入 dump<br>• **隊員 C**: [picoCTF: Wireshark twoo twooo two twoo... (ID: 110)](https://learn.cylabacademy.org/library?search=Wireshark%20twoo%20twooo%20two%20twoo...) | • Volatility 3 核心指令：<br>  • `windows.pslist.PsList`: 列出進程<br>  • `windows.pstree.PsTree`: 進程父子關係樹<br>  • `windows.netscan.NetScan`: 掃描網路連線 (TCP/UDP)<br>  • `windows.malfind.Malfind`: 尋找隱藏/注入的代碼區塊 (VAD 標籤帶 PAGE_EXECUTE_READWRITE) |
| **Day 8** (09/17) | **資通安全責任等級 A/B/C/D/E 級規範**<br>核心系統、資安專職人員證照與 ISO 27001 要求 | • **隊員 A**: 研讀 [全國法規資料庫: 資通安全責任等級分級辦法](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=A0030295) 並製作 A~E 級人員配置速記卡<br>• **隊員 B**: 實作 Volatility `malfind` 提取 Shellcode 並以 [CyberChef](https://gchq.github.io/CyberChef/) 解碼<br>• **隊員 C**: 研讀 B2 Run 14 教材 `00_密碼學基礎與RSA解密實戰通關手冊_中文版.md` | • **責任等級要求重點 (必考數字題)**：<br>  • **A 級**：專職人員至少 **4 人**（每人每年受訓 12 小時以上），初次受核定 **2 年內** 通過第三方 ISO 27001 驗證。<br>  • **B 級**：專職人員至少 **2 人**，初次受核定 2 年內通過 ISO 27001。<br>  • **C 級**：專職人員至少 **1 人**。<br>  • 核心資通系統：遭破壞將導致機關業務無法運作或國家機密外洩之系統。 |

---

### ⚔️ **Run 5 (Day 9-10, 09/18-09/19): SSL/TLS 加密傳輸安全 ＆ 非對稱密碼 RSA/ECC**
🌐 **本 Run 核心目標**: 剖析 TLS 1.2 vs 1.3 握手細節，精通 RSA 大數分解與小指數攻擊。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 9** (09/18) | **SSL/TLS 握手流程與憑證鏈 (PKI)**<br>ClientHello、密鑰交換、CA 根憑證信任與 CRL/OCSP | • **隊員 A**: [picoCTF: Cookies (ID: 173)](https://learn.cylabacademy.org/library?search=Cookies) 實作 Cookie 偽造<br>• **隊員 B**: 研讀 [內部離線教材] `07_藍隊防禦與護網營運/04_護網專案營運/藍隊日誌/HW16-告警日志分析技术-v1.1.pdf` 實作 Web 日誌分析<br>• **隊員 C**: [picoCTF: Mind your Ps and Qs (ID: 162)](https://learn.cylabacademy.org/library?search=Mind%20your%20Ps%20and%20Qs) 實戰 RSA 分解（搭配 [FactorDB 質數庫](http://factordb.com/)） | • **TLS 1.2 vs TLS 1.3 核心差異 (必考)**：<br>  • TLS 1.2 完整握手需 **2-RTT**；TLS 1.3 簡化至 **1-RTT**，且支援 **0-RTT (Early Data)**。<br>  • TLS 1.3 廢除靜態 RSA 密鑰交換與 CBC 模式，強制使用具備前向保密性（PFS）的 (EC)DHE 密鑰交換與 AEAD 認證加密（AES-GCM）。<br>  • **數位簽章**：發送方用自己的**私鑰**對訊息 Hash 進行簽名，接收方用發送方的**公鑰**驗證，確保「完整性」與「不可否認性」。 |
| **Day 10** (09/19) | **RSA 公私鑰數學與經典攻擊**<br>$n = p \times q$、歐拉函數 $\phi(n)$ 與 $e=3$ 小指數開方攻擊 | • **隊員 A**: [picoCTF: More Cookies (ID: 124)](https://learn.cylabacademy.org/library?search=More%20Cookies) CBC 位元翻轉<br>• **隊員 B**: 參考 [SANS: Windows 鑑識與 MFT 分析指南](https://www.sans.org/posters/windows-forensic-analysis/) 研讀 MFT 檔案記錄結構<br>• **隊員 C**: [picoCTF: Mini RSA (ID: 188)](https://learn.cylabacademy.org/library?search=Mini%20RSA) 執行開立方根攻擊 | • RSA 私鑰公式：$d \equiv e^{-1} \pmod{(p-1)(q-1)}$。<br>• 若 $m^e < n$（未發生模數溢出），密文可直接開 $e$ 次方根還原明文。 |

---

### ⚔️ **Run 6 (Day 11-12, 09/20-09/21): Active Directory 網域安全 ＆ 磁碟檔案系統鑑識**
🌐 **本 Run 核心目標**: 理解 Windows Kerberos 認證票據機制，掌握 NTFS MFT 時間戳記與 MACB 鑑識。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 11** (09/20) | **Kerberos 身分驗證機制**<br>KDC (密鑰分發中心)、AS-REQ/AS-REP、TGT 票據與黃金票據 (Golden Ticket) | • **隊員 A**: 刷 [阿摩 iPAS 身分識別與防護題庫 (中級防護)](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E9%98%B2%E8%AD%B7%E5%AF%A6%E5%8B%99%E2%97%86%E4%B8%AD%E7%B4%9A-6252.htm) 15 題<br>• **隊員 B**: [THM: Active Directory Basics](https://tryhackme.com/room/activedirectorybasics) 實作網域架構<br>• **隊員 C**: 參考 [Wireshark Wiki: Kerberos](https://wiki.wireshark.org/Kerberos) 抓包分析 88 埠通訊流程與 SPN 特徵 | • **Kerberos 認證流程 (必考順序)**：<br>  1. 使用者向 AS 請求 TGT (AS-REQ ➔ AS-REP)<br>  2. 使用者持 TGT 向 TGS 請求服務票據 ST (TGS-REQ ➔ TGS-REP)<br>  3. 使用者向服務伺服器出示 ST (AP-REQ ➔ AP-REP)<br>• **黃金票據（Golden Ticket）**：利用 `krbtgt` 帳戶 NTLM 雜湊偽造任何 TGT！<br>• **白銀票據（Silver Ticket）**：利用服務帳號 NTLM 雜湊偽造特定服務的 ST 票據。 |
| **Day 12** (09/21) | **NTFS 檔案系統結構與時間戳記**<br>MFT (主檔案表)、`$STANDARD_INFORMATION` vs `$FILE_NAME` 與時間竄改 (Timestomping) | • **隊員 A**: [picoCTF: MatchTheRegex (ID: 356)](https://learn.cylabacademy.org/library?search=MatchTheRegex)<br>• **隊員 B**: 研讀 [內部離線教材] `07_藍隊防禦與護網營運/04_護網專案營運/藍隊日誌/HW17-快速应急响应技术-v1.0.pdf` 實作硬碟映像檔分析<br>• **隊員 C**: [CryptoHack: Diffie-Hellman Starter](https://cryptohack.org/challenges/diffie-hellman/) | • **MACB 時間戳記**：Modified (修改)、Accessed (存取)、Created (建立)、Entry Modified (MFT紀錄變更)。<br>• Timestomping 攻擊通常只能竄改 `$STANDARD_INFORMATION`，而在 `$FILE_NAME` 中會留下原始時間戳記。 |

---

### ⚔️ **Run 7 (Day 13-14, 09/22-09/23): 網路防禦設備 ＆ VPN 技術比較 (PPTP/IPsec/SSL)**
🌐 **本 Run 核心目標**: 理解 WAF/IDS/IPS 部署架構，全方位比較四大 VPN 協定優劣與連接埠。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 13** (09/22) | **網路安全防護設備 (Firewall / IDS / IPS / WAF)**<br>封包過濾型 vs 狀態檢視型、In-line 串接 vs Out-of-band 側掛 | • **隊員 A**: [picoCTF: logon (ID: 46)](https://learn.cylabacademy.org/library?search=logon) 實作身分繞過<br>• **隊員 B**: 實作本地 `../../../security/practice/exams/mock_exam_b_lab_questions.md`（第 52~65 題 封包分析與 IDS）<br>• **隊員 C**: 參考 [Ubuntu iptables 官方配置教學](https://help.ubuntu.com/community/IptablesHowTo) 撰寫規則封鎖特定 IP 與 SYN Flood | • **IDS**（入侵偵測）通常採「旁路/鏡像監聽 (SPAN Port)」，只發出警報不阻斷；<br>• **IPS**（入侵防禦）採「串接 (In-line)」，能即時攔截丟棄惡意封包；<br>• **WAF** 專注於第七層應用層（HTTP/HTTPS）攻擊防禦（防止 SQLi, XSS）。 |
| **Day 14** (09/23) | **VPN 協定深度對決 (PPTP / L2TP / IPsec / SSL VPN)**<br>通訊埠、封裝協定 (GRE) 與安全性弱點比較 | • **隊員 A**: 參考 [Cisco: VPN 拓撲與技術手冊](https://www.cisco.com/c/en/us/support/docs/security/vpn-3000-series-concentrators/10757-vpntop.html) 製作比較表<br>• **隊員 B**: 研讀 [NIST SP 800-86: 數位鑑識整合指南](https://csrc.nist.gov/publications/detail/sp/800-86/final) 監管鏈標準表單<br>• **隊員 C**: [CryptoHack: AES ECB Mode](https://cryptohack.org/challenges/aes/) 觀察企鵝圖漏洞 | • **VPN 種類必考比較**：<br>  • **PPTP**：使用 TCP 1723 埠與 **GRE 協定 (IP 協定號 47)**，搭配 MS-CHAPv2 驗證，已被證實不安全！<br>  • **L2TP/IPsec**：使用 UDP 500/4500/1701 埠，IPsec **AH** 提供驗證完整性（不防 NAT），**ESP** 提供資料加密。<br>  • **SSL/TLS VPN (OpenVPN)**：走 TCP/UDP 443 埠，穿透防火牆能力最強，無須專屬客戶端軟體。 |

---

### ⚔️ **Run 8 (Day 15-16, 09/24-09/25): Linux 主機安全機制 ＆ 資安事件通報時限 (1~4 級)**
🌐 **本 Run 核心目標**: 掌握 Linux SUID/Capabilities 權限模型，精確背熟 1~4 級資安事件通報時限。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 15** (09/24) | **Linux 安全與權限提升防護**<br>PAM 模組機制、SELinux 狀態判讀與 SUID 權限管理 | • **隊員 A**: 研讀 B2 Run 11 教材 `00_Linux本地權限提升實戰通關手冊_中文版.md`<br>• **隊員 B**: 研讀 [內部離線教材] `07_藍隊防禦與護網營運/01_系統與資料庫加固/Linux系統安全加固/` 實作 Linux 系統稽核<br>• **隊員 C**: 參考 [Cloudflare: DNS 放大攻擊原理與防禦](https://www.cloudflare.com/zh-tw/learning/ddos/dns-amplification-ddos-attack/) 抓包分析放大攻擊 | • Linux 密碼存放在 `/etc/shadow`，`$6$` 代表 SHA-512，`$y$` 代表 yescrypt。<br>• PAM 配置原則：`required` 必須成功但不中斷後續、`requisite` 失敗立即返回、`sufficient` 成功且無其他失敗則立即返回通過。 |
| **Day 16** (09/25) | **《資通安全事件通報及應變辦法》實務 (必考重中之重)**<br>1~4 級資安事件分級定義、通報時限與損害控制完成時限 | • **隊員 A**: 參考 [國家資通安全研究院: 資安事件分級指引](https://www.nics.nat.gov.tw/) 製作通報對照表<br>• **隊員 B**: 刷 [阿摩 iPAS 資安法規遵循題庫 (初級管理)](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E7%AE%A1%E7%90%86%E6%A6%82%E8%AB%96%E2%97%86%E5%88%9D%E7%B4%9A-5273.htm) 20 題<br>• **隊員 C**: [picoCTF: 2warm (ID: 86)](https://learn.cylabacademy.org/library?search=2warm) 與 [picoCTF: Warmed Up (ID: 58)](https://learn.cylabacademy.org/library?search=Warmed%20Up) | • **資通安全事件通報時限（100% 必考）**：<br>  • **通報時限**：知悉事件後 **1 小時內** 完成通報（1~4 級皆為 1 小時）！<br>  • **應變/損害控制時限**：<br>    - 第 1、2 級事件：知悉後 **72 小時內** 完成應變復原。<br>    - 第 3、4 級事件：知悉後 **36 小時內** 完成應變復原。<br>  • **事後調查與改善報告**：事件解除後 **1 個月內** 提出。 |

---

### ⚔️ **Run 9 (Day 17-18, 09/26-09/27): 無線網路安全 (WPA2/3) ＆ 數位證據監管鏈**
🌐 **本 Run 核心目標**: 剖析 802.11 四向握手原理，掌握 ISO/IEC 27037 數位證據處理程序規範。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 17** (09/26) | **無線通訊安全機制 (WPA2 vs WPA3)**<br>802.11 4-Way Handshake、EAP 認證與 WPA3 Dragonfly 握手協定 | • **隊員 A**: [picoCTF: SQL Direct (ID: 303)](https://learn.cylabacademy.org/library?search=SQL%20Direct)<br>• **隊員 B**: 參考 [SANS: 網路鑑識與封包分析專案](https://www.sans.org/white-papers/) 實作 SHA-256 封存模擬<br>• **隊員 C**: 參考 [Wireshark: EAPOL 封包過濾指南](https://www.wireshark.org/docs/dfref/e/eapol.html) 篩選封包觀察 4-Way Handshake 過程 | • WPA2 弱點在於離線字典攻擊 (Dictionary Attack) 與重送攻擊；<br>• WPA3 採用 SAE (Simultaneous Authentication of Equals，代號 Dragonfly 協定)，具備前向保密性，能徹底免疫離線字典攻擊。 |
| **Day 18** (09/27) | **ISO/IEC 27037 數位證據處理規範**<br>證據的識別 (Identification)、收集 (Collection)、獲取 (Acquisition) 與保存 (Preservation) | • **隊員 A**: 研讀 [全國法規資料庫: 個人資料保護法](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021) 告知義務與罰則<br>• **隊員 B**: 刷 [阿摩 iPAS 數位鑑識題庫 (中級防護)](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E9%98%B2%E8%AD%B7%E5%AF%A6%E5%8B%99%E2%97%86%E4%B8%AD%E7%B4%9A-6252.htm) 20 題<br>• **隊員 C**: [CryptoHack: Block Cipher CBC](https://cryptohack.org/challenges/aes/) 實作 IV 初始化 | • 證據監管鏈（Chain of Custody）：詳細記錄「誰、在何時、以何種方式、取得/移動/分析了該證物」，確保證據具備法律證據能力與無污染性。 |

---

### ⚔️ **Run 10 (Day 19-20, 09/28-09/29): 雲端安全責任模型 ＆ SNMP 協定安全演進**
🌐 **本 Run 核心目標**: 徹底搞懂 IaaS/PaaS/SaaS 共同責任邊界，掌握 SNMP v1/v2c vs v3 安全機制。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 19** (09/28) | **雲端運算共同責任模型 (Shared Responsibility Model)**<br>IaaS、PaaS、SaaS 各層級安全責任劃分（資料/OS/實體硬體） | • **隊員 A**: 參考 [Microsoft Learn: 雲端中的共同責任模型](https://learn.microsoft.com/zh-tw/azure/security/fundamentals/shared-responsibility) 繪製責任矩陣表<br>• **隊員 B**: 刷 [阿摩 iPAS 雲端安全題庫 (中級規劃)](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E8%A6%8F%E5%8A%83%E5%AF%A6%E5%8B%99%E2%97%86%E4%B8%AD%E7%B4%9A-5274.htm) 20 題<br>• **隊員 C**: 參考 [Net-SNMP: snmpwalk 指南](http://www.net-snmp.org/wiki/index.php/TUT:snmpwalk) 實作查詢 OID 與社群字串 | • **雲端責任模型 (每年必考送分題)**：<br>  • **IaaS**（基礎設施即服務，如 AWS EC2）：雲端廠商管實體機房與虛擬化；**租戶負責作業系統 (OS) 更新、防火牆設定、應用程式與資料安全**！<br>  • **PaaS**（平台即服務，如 Heroku, Google App Engine）：廠商管 OS 與執行環境；**租戶負責應用程式代碼與資料**。<br>  • **SaaS**（軟體即服務，如 M365, Gmail）：廠商全包；**租戶僅負責存取權限與自身輸入的資料**。 |
| **Day 20** (09/29) | **網路管理協定安全 (SNMP v1/v2c vs v3)**<br>UDP 161/162 埠、社群字串 (Community String) 弱點與 v3 認證加密 | • **隊員 A**: [picoCTF: SOAP (ID: 376)](https://learn.cylabacademy.org/library?search=SOAP) XXE 注入實戰<br>• **隊員 B**: [THM: Network Services](https://tryhackme.com/room/networkservices) 實作網路服務枚舉與弱點分析<br>• **隊員 C**: 參考 [Wireshark SNMP 封包範例](https://wiki.wireshark.org/SNMP) 抓包比對 SNMP v1 與 v3 加密流量 | • **SNMP 版本演進考點**：<br>  • SNMP v1 / v2c 採用明文社群字串（Community String，常見預設 `public` 唯讀、`private` 讀寫），極易遭竊聽篡改。<br>  • **SNMP v3 三種安全等級**：<br>    1. `noAuthNoPriv`：無認證、無加密。<br>    2. `authNoPriv`：支援 HMAC-MD5 / SHA 身份認證，無加密。<br>    3. `authPriv`：**同時支援認證與 DES / AES 資料加密**（最高安全等級）。 |

---

### ⚔️ **Run 11 (Day 21-22, 09/30-10/01): 重大 CVE 漏洞剖析 ＆ CVSS 評分系統實戰**
🌐 **本 Run 核心目標**: 剖析 Log4Shell 等歷史重大漏洞成因，精確計算 CVSS v3.1 基本指標分數。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 21** (09/30) | **CVSS v3.1 / v4.0 漏洞通用評分系統**<br>基本指標 (Base Metrics)、時效指標 (Temporal) 與環境指標 (Environmental) | • **隊員 A**: [NVD CVSS v3.1 官方在線計算機](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator) 計算 5 個 CVE<br>• **隊員 B**: [THM: Log4j (Solar)](https://tryhackme.com/room/solar) 實作 JNDI 注入原理<br>• **隊員 C**: [picoCTF: caesar (ID: 64)](https://learn.cylabacademy.org/library?search=caesar) 與 [picoCTF: interencdec (ID: 418)](https://learn.cylabacademy.org/library?search=interencdec) | • **CVSS v3.1 基本指標群（必考計算題）**：<br>  • 可利用性（AV 攻擊途徑：Network/Adjacent/Local/Physical、AC 複雜度、PR 特權、UI 使用者互動）<br>  • 影響範圍（Scope：Unchanged vs Changed）<br>  • 影響衝擊（CIA：Confidentiality 機密性、Integrity 完整性、Availability 可用性，等級為 None/Low/High）。 |
| **Day 22** (10/01) | **歷史重大 CVE 漏洞運作機制剖析**<br>Log4j (CVE-2021-44228 JNDI/LDAP)、Spring4Shell、Heartbleed (CVE-2014-0160) | • **隊員 A**: 參考 [CISA: 已知利用漏洞目錄 (KEV Catalog)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) 製作 CVE 對照表<br>• **隊員 B**: 參考 [CrowdStrike: Log4j 攻擊日誌分析指南](https://www.crowdstrike.com/blog/log4j2-vulnerability-analysis-and-mitigation-recommendations/) 分析 `${jndi:ldap://...}` 特徵<br>• **隊員 C**: 研讀 [Cloudflare: 密鑰交換與 Diffie-Hellman 原理](https://www.cloudflare.com/zh-tw/learning/ssl/what-is-key-exchange/) | • Heartbleed：OpenSSL TLS 心跳延伸（Heartbeat）未做長度邊界檢查，導致每次溢位讀取 64KB 記憶體。<br>• Log4Shell：Log4j 框架對 `${...}` 語法進行不安全的 JNDI 查找，導致攻擊者透過 LDAP 下載並執行惡意 Java Class。 |

---

### ⚔️ **Run 12 (Day 23-24, 10/02-10/03): 經典藍隊防禦工具庫 ＆ 網路隱蔽隧道分析**
🌐 **本 Run 核心目標**: 建立 Tripwire/Snort/Sysmon 藍隊名詞庫，實作識別 DNS Tunneling 與 ICMP 隧道。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 23** (10/02) | **經典主機與網路防禦工具對照庫 (名詞題必考)**<br>Tripwire、AIDE、Snort、Suricata、Sysmon、Wazuh | • **隊員 A**: [picoCTF: Forbidden Paths (ID: 270)](https://learn.cylabacademy.org/library?search=Forbidden%20Paths)<br>• **隊員 B**: 研讀 [Snort 3 官方規則手冊](https://docs.snort.org/rules/) 語法結構<br>• **隊員 C**: 參考 [Microsoft Learn: Sysmon 官方手冊與 Event ID](https://learn.microsoft.com/zh-tw/sysinternals/downloads/sysmon) 整理防禦工具對照表 | • **防禦工具名詞配對 (必考)**：<br>  • **Tripwire / AIDE**：檔案完整性監控 (File Integrity Monitoring, FIM)，透過 Baseline Hash 偵測系統檔案是否遭竄改。<br>  • **Snort / Suricata**：開源網路入侵偵測/防禦系統 (NIDS/NIPS)。<br>  • **Sysmon**：Windows 進階端點記錄工具（Event ID 1 建立進程、3 網路連線、7 載入 DLL）。 |
| **Day 24** (10/03) | **網路隱蔽傳輸通道 (Covert Channels)**<br>DNS Tunneling (碘通道 iodine)、ICMP 資料隱寫與 NTP 同步 | • **隊員 A**: 刷 [阿摩 iPAS 資安防護實務題庫 (中級防護)](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E9%98%B2%E8%AD%B7%E5%AF%A6%E5%8B%99%E2%97%86%E4%B8%AD%E7%B4%9A-6252.htm) 20 題<br>• **隊員 B**: [Malware Traffic Analysis (MTA): 封包鑑識實戰](https://www.malware-traffic-analysis.net/tutorials/index.html) 實作惡意流量與 PCAP 鑑識<br>• **隊員 C**: 參考 [Wireshark: ICMP 封包分析](https://wiki.wireshark.org/Internet_Control_Message_Protocol) 篩選提取 payload 隱寫文字 | • DNS 隧道特徵：大量請求異常長子網域（如 `a1b2c3d4.attacker.com`）、查詢頻率極高、TXT 與 NULL 記錄使用比例高。<br>• SIEM 關聯分析關鍵在於「時間同步 (NTP)」，如果設備間時間未對齊，跨系統時間線將無法精確重構。 |

---

### ⚔️ **Run 13 (Day 25-26, 10/04-10/05): 個資法規與隱私框架 ＆ NIST CSF 企業防禦架構**
🌐 **本 Run 核心目標**: 熟記《個人資料保護法》罰則與義務，掌握 NIST CSF 五大核心功能。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 25** (10/04) | **《個人資料保護法》重點解析**<br>特種個資定義（醫療/基因/性生活/健康檢查/犯罪前科）、告知同意義務與外洩通報 | • **隊員 A**: 研讀 [全國法規資料庫: 個人資料保護法施行細則](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050022) 製作特種個資對照卡<br>• **隊員 B**: [THM: Windows Forensics 1](https://tryhackme.com/room/windowsforensics1) 實作磁碟證據提取與 Registry 鑑識<br>• **隊員 C**: [picoCTF: buffer overflow 0 (ID: 257)](https://learn.cylabacademy.org/library?search=buffer%20overflow%200) | • 特種個資（病歷、醫療、基因、性生活、健康檢查及犯罪前科）原則上不得蒐集、處理或利用，除非符合法定除外要件。<br>• 損害賠償：每人每一事件新臺幣 500 元以上 2 萬元以下；最高總額上限新臺幣 2 億元。 |
| **Day 26** (10/05) | **NIST CSF (網路安全框架) 與 MITRE ATT&CK**<br>IPDRR 五大核心（Identify / Protect / Detect / Respond / Recover） | • **隊員 A**: 刷 [阿摩 iPAS 資安規劃與治理題庫 (中級規劃)](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E8%A6%8F%E5%8A%83%E5%AF%A6%E5%8B%99%E2%97%86%E4%B8%AD%E7%B4%9A-5274.htm) 25 題<br>• **隊員 B**: 參考 [MITRE ATT&CK: 企業矩陣 Enterprise Matrix](https://attack.mitre.org/matrices/enterprise/) 梳理三大階段戰術<br>• **隊員 C**: [picoCTF: buffer overflow 1 (ID: 258)](https://learn.cylabacademy.org/library?search=buffer%20overflow%201) ret2text | • **NIST CSF 2.0 更新**：在原有的五大核心（IPDRR）之外，新增了 **「Govern 治理」**，形成六大核心功能！ |

---

### ⚔️ **Run 14 (Day 27-28, 10/06-10/07): 【全真全科模擬一】標準 100 題 90 分鐘極速測驗**
🌐 **本 Run 核心目標**: 模擬金盾初賽真實 100 題單選作答節奏（平均每題 54 秒），演練 3 人分工刪除法。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 27** (10/06) | **全真模擬測驗 A 卷 (標準 100 題單選，限時 90 分鐘)**<br>涵蓋七大領域，三人連線獨立完成並記錄答案 | • **全員**: <br>  1. 開啟 [mock_exam_a_100q_questions.md](../../../security/practice/exams/mock_exam_a_100q_questions.md) 進行 90 分鐘閉卷實測（純試卷，末尾附標準答題卡，作答前嚴禁翻閱解析）<br>  2. 亦可至 [阿摩 iPAS 技術概論全真題庫](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E6%8A%80%E8%A1%93%E6%A6%82%E8%AB%96%E2%97%86%E5%88%9D%E7%B4%9A-6299.htm) 與 [防護實務題庫](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E9%98%B2%E8%AD%B7%E5%AF%A6%E5%8B%99%E2%97%86%E4%B8%AD%E7%B4%9A-6252.htm) 進行在線刷題<br>• **隊長**: 統計全員成績與時間耗費，登錄至 [../../../security/practice/exams/README.md](../../../security/practice/exams/README.md) 自評表 | • **100 題極速作答策略 (必練)**：<br>  1. 前 45 分鐘：快速秒殺 60 題「一眼看懂的記憶題與法規題」（每題 40 秒）。<br>  2. 中間 30 分鐘：集中攻克 25 題計算題（CVSS、RSA 參數、子網路遮罩）。<br>  3. 最後 15 分鐘：難題四選一刪除法猜題，答錯不倒扣，絕對不可留白！ |
| **Day 28** (10/07) | **A 卷深度復盤與弱點科目專項掃除**<br>檢視各隊員失分題型，立即由主修成員進行 1 對 1 補課 | • **全員**: 開啟 [mock_exam_a_100q_solutions.md](../../../security/practice/exams/mock_exam_a_100q_solutions.md) 核對標準答案，細讀誘答干擾項辨析<br>• **隊員 A**: 主講法規與 Web 錯題（對照 [全國法規資料庫](https://law.moj.gov.tw/) 與 [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/)）<br>• **隊員 B**: 主講系統與鑑識錯題（對照 [Microsoft Learn Security](https://learn.microsoft.com/zh-tw/windows/security/) 與 [CyberDefenders Writeup](https://cyberdefenders.org/)）<br>• **隊員 C**: 主講網路與密碼錯題（對照 [Wireshark Wiki](https://wiki.wireshark.org/) 與 B2 Run 14 教材 `00_密碼學基礎與RSA解密實戰通關手冊_中文版.md`） | • 錯題分類原則：<br>  • 「粗心看錯題目」：加強題目關鍵字圈選（如：「何者非屬」、「何者錯誤」）。<br>  • 「觀念完全盲區」：對照 A卷解析中的 7 大領域診斷指標進行弱項專項加強。 |

---

### ⚔️ **Run 15 (Day 29-30, 10/08-10/09): 【全真全科模擬二】壓軸總決戰 ＆ 考前高頻清單掃蕩**
🌐 **本 Run 核心目標**: 第二次全真模擬驗收（結合全國賽官方實體題本情境），確認臨場設備與答題默契。

| 天數 | 🎯 當日教學與實作重點 | 🧪 3 人分工具體實作任務與關卡 (Member Tasks & Labs) | 📝 金盾初賽單選高頻考點 (Exam Notes) |
| :--- | :--- | :--- | :--- |
| **Day 29** (10/08) | **全真模擬測驗 B 卷 (實體真題無環境推演，目標 80 分以上)**<br>完整包含 IR (23題)、Hardening (28題)、CTF I 封包 (30題)、CTF II (12題) | • **全員**: <br>  1. 開啟 [mock_exam_b_lab_questions.md](../../../security/practice/exams/mock_exam_b_lab_questions.md)，所有封包流量、DNS 序列、日誌片段與 Hex Dump 已內嵌題本中，三人分工於作答卷填寫答案<br>  2. 完成後開啟 [mock_exam_b_lab_solutions.md](../../../security/practice/exams/mock_exam_b_lab_solutions.md) 進行解題思路校正與 Flag 核對<br>• **隊長**: 檢查全隊通關率是否達到 80% | • 建立三人臨場答題默契：一人專注封包協議過濾、一人主攻系統配置加固、一人負責 Web 與日誌取證，確保每道推演題精準破題。 |
| **Day 30** (10/09) | **考前口測檢定 ＆「高頻速記卡」全面總複習**<br>法規通報時限、RFC 3227 揮發順序、Event ID 與密碼模式速記 | • **全員**: 開啟 [high_frequency_flashcards.md](../../../security/practice/exams/high_frequency_flashcards.md) 進行三人面對面快問快答口測檢定（每人抽測 15 題，3 秒內作答反應）<br>• **隊員 A/B/C**: 針對失誤盲點進行最後 30 分鐘救命卡清單複查 | • **初賽前最後確認**：<br>  • 登入 [金盾獎官網](https://csc.nics.nat.gov.tw/shield.aspx) 確認規範。<br>  • 初賽時間為 90 分鐘，前 30 分鐘不得交卷。<br>  • 答錯不倒扣，保持冷靜細心作答！ |

---

## 🏁 初賽倒數衝刺週 (10/10 ～ 10/16 考前調適)
* **10/10～10/15**：不再安排全新高難度題目，每天只需花 30 分鐘反覆翻閱 3 份《金盾初賽速記卡》加深記憶。
* **10/16**：充足睡眠、放鬆心情，確認准考資訊與考場位置。
* **10/17 (初賽日)**：**出征金盾獎初賽！全力發揮，強勢晉級 11 月決賽！**

---

## 📚 歷屆試題與官方題庫直達專區 (真實可用試卷總表)

> 💡 **阿摩線上測驗分類說明**：先前阿摩後台曾重整分類，部分測試分類（如 `testA / 6415`）為空卷。請一律使用下方經實際驗證、包含數十份歷屆考卷的專屬分類直達：

| 科目名稱 | 級別 | 阿摩在線測驗直達 (含解析討論) | 官方試題與樣題 PDF 下載 |
| :--- | :---: | :---: | :---: |
| **資訊安全管理概論** | 初級 (GRC/法規) | [阿摩 18 份歷屆試卷列表](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E7%AE%A1%E7%90%86%E6%A6%82%E8%AB%96%E2%97%86%E5%88%9D%E7%B4%9A-5273.htm) | [官方考試簡章與樣題下載](https://ipd.nat.gov.tw/ipas/certification/ISE/downloads) |
| **資訊安全技術概論** | 初級 (網路/系統) | [阿摩 19 份歷屆試卷列表](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E6%8A%80%E8%A1%93%E6%A6%82%E8%AB%96%E2%97%86%E5%88%9D%E7%B4%9A-6299.htm) | [官方考試簡章與樣題下載](https://ipd.nat.gov.tw/ipas/certification/ISE/downloads) |
| **資訊安全防護實務** | 中級 (鑑識/防禦) | [阿摩 12 份歷屆試卷列表](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E9%98%B2%E8%AD%B7%E5%AF%A6%E5%8B%99%E2%97%86%E4%B8%AD%E7%B4%9A-6252.htm) | [中級樣題與學習指引下載](https://ipd.nat.gov.tw/ipas/certification/ISE/downloads) |
| **資訊安全規劃實務** | 中級 (治理/雲端) | [阿摩 13 份歷屆試卷列表](https://yamol.tw/cat-iPAS%E2%97%86%E8%B3%87%E8%A8%8A%E5%AE%89%E5%85%A8%E8%A6%8F%E5%8A%83%E5%AF%A6%E5%8B%99%E2%97%86%E4%B8%AD%E7%B4%9A-5274.htm) | [中級樣題與學習指引下載](https://ipd.nat.gov.tw/ipas/certification/ISE/downloads) |
| **經濟部官方能力鑑定專區** | 官網 | [經濟部 iPAS 官方考證專區](https://ipd.nat.gov.tw/ipas/certification/ISE/news) | [官方考試簡章與最新消息](https://ipd.nat.gov.tw/ipas/certification/ISE/exam-info) |
| **官方資源與樣題下載** | 官網 | [iPAS 資訊安全工程師學習資源](https://ipd.nat.gov.tw/ipas/certification/ISE/learning-resources) | [官方檔案與樣題下載區](https://ipd.nat.gov.tw/ipas/certification/ISE/downloads) |
| **沈老師 iPAS 試題解析網** | 社群 | [沈老師資安考題解析 (推薦閱讀)](https://ipas.tw/) | 逐題詳細背景與觀念拆解 |

