# 🛡️ 模組 04：國際藍隊與在線房間靶場 (CyberDefenders & TryHackMe)

> **資料來源**：
> - CyberDefenders 精選映射：[`cyberdefenders_free_catalog_mapping.md`](../../knowledge/blue_team/learning_paths/cyberdefenders_free_catalog_mapping.md)
> - TryHackMe 免費房間目錄：[`tryhackme_free_rooms_catalog.md`](../challenges/platforms/tryhackme/tryhackme_free_rooms_catalog.md)

---

## 🌐 第一部分：CyberDefenders 國際藍隊 PCAP 實戰靶場

CyberDefenders 專門提供逼真的企業級網路攻擊封包，以下為 Wireshark / Network Forensics 核心推薦：

| 靶場題目名稱 | 難度 / 建議時間 | 官方傳送門 | 實戰鑑識任務與情境 |
| :--- | :---: | :--- | :--- |
| **DanaBot** | `Easy` / 30m | [前往挑戰](https://cyberdefenders.org/blueteam-ctf-challenges/danabot/) | 使用 Wireshark 分析網路流量，識別 DanaBot 銀行木馬初期存取、解混淆惡意 JavaScript 並提取惡意 IP 與 Hash。 |
| **Lockdown** | `Easy` / 60m | [前往挑戰](https://cyberdefenders.org/blueteam-ctf-challenges/lockdown/) | 多階段網路入侵分析，利用 Wireshark 與 VirusTotal 計算 C2 心跳週期（Beaconing / Jitter），對齊 MITRE ATT&CK。 |
| **PsExec Hunt** | `Easy` / 30m | [前往挑戰](https://cyberdefenders.org/blueteam-ctf-challenges/psexec-hunt/) | 分析 PCAP 中的 SMB/RPC 協定，精確定位 PsExec 橫向移動痕跡、受害主機、使用者憑證與管理員共用目錄（ADMIN$）。 |
| **Tomcat Takeover** | `Easy` / 30m | [前往挑戰](https://cyberdefenders.org/blueteam-ctf-challenges/tomcat-takeover/) | 利用 Wireshark 自訂欄位、過濾器與統計功能，排查可疑的 Web 伺服器管理者異常連線與弱密碼爆破。 |
| **Web Investigation** | `Easy` / 45m | [前往挑戰](https://cyberdefenders.org/blueteam-ctf-challenges/web-investigation/) | 審查 PCAP 網路流量以調查 Web 伺服器入侵，定位 SQL 注入軌跡、提取攻擊者利用注入取得的憑證並偵測上傳的木馬。 |
| **PacketMaze** | `Medium` / 45m | [前往挑戰](https://cyberdefenders.org/blueteam-ctf-challenges/packetmaze/) | Wireshark 核心封包排查，橫跨多種協定（FTP, HTTP, DNS, ICMP）還原可疑連線、認證資訊與檔案傳輸。 |
| **WireDive** | `Medium` / 90m | [前往挑戰](https://cyberdefenders.org/blueteam-ctf-challenges/wiredive/) | **HTTPS 解密與協定分析經典**：導入 Keylog 解密多協定流量，識別協定配置錯誤並提取關鍵鑑識指標。 |

---

## 🖥️ 第二部分：TryHackMe 官方免費 Wireshark 房間

TryHackMe 提供了互動式虛擬環境（可於瀏覽器直接開啟 Wireshark 實操）：

1. **[Wireshark: The Basics](https://tryhackme.com/room/wiresharkthebasics)**
   - **學習目標**：介面導覽、網路介面選擇、封包顏色標記規則、封包詳情視窗（Packet Details）各層標頭解讀。
2. **[Wireshark: Packet Operations](https://tryhackme.com/room/wiresharkpacketoperations)**
   - **學習目標**：熟練掌握 Display Filters 邏輯運算（`and`, `or`, `not`）、Follow Stream、封包時間戳格式切換與匯出物件。
3. **[Wireshark: Traffic Analysis](https://tryhackme.com/room/wiresharktrafficanalysis)**
   - **學習目標**：Nmap 掃描行為識別（SYN / Connect / FIN / Xmas）、ARP 欺騙、DHCP 飢餓攻擊以及惡意軟體網路回傳特徵。
4. **[Tshark: CLI Wireshark Features](https://tryhackme.com/room/tsharkcliwiresharkfeatures)**
   - **學習目標**：Tshark 命令列工具參數實戰（`-r`, `-Y`, `-T fields`, `-e`, `-z`），在大流量場景下進行快速過濾與統計。
5. **[Wireshark](https://tryhackme.com/room/wireshark)**
   - **學習目標**：綜合演練房間，提供情境題深入檢驗封包分析綜合實力。

---

## 🦠 第三部分：Malware Traffic Analysis (MTA) 惡意流量專案

- **官方首頁**：[Malware Traffic Analysis (MTA)](https://www.malware-traffic-analysis.net/)
- **特色**：由知名威脅獵捕專家 Brad Duncan 維護，定期發布真實世界勒索軟體（如 LockBit、Qakbot、IcedID、Cobalt Strike）的 PCAP 與告警日誌。
- **訓練任務建議**：
  1. 下載最新 PCAP 樣本。
  2. 5 分鐘內用 Wireshark / Tshark 定位受害主機 IP、MAC 位址與 Hostname。
  3. 提取攻擊者下載的惡意二進位檔案（PE / DLL）並計算 SHA-256 雜湊值。
  4. 識別 C2 通訊網域名稱與請求特徵。
