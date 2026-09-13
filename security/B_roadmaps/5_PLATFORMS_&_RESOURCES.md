# 🌐 外部平台與推薦工具箱 (5_PLATFORMS_&_RESOURCES.md)

> 本文件匯整線上實務靶場、CTF 競賽平台與必備輔助工具箱。

---

## 🎓 一、 主流線上實務靶場與學習平台

| 平台名稱 | 核心亮點與特色 | 對應比賽 / 求職目標 | 官方連結 |
|---|---|---|---|
| **PortSwigger Academy** | Web 漏洞理論與 Lab 標竿，全免費，包含 282 個實務 Labs。 | DEVCORE Red Team 必要條件 | [PortSwigger 官網](https://portswigger.net/web-security) |
| **Root-Me** | 包含 171 個虛擬環境、534+ 個挑戰題目，涵蓋 Web, Pwn, Crypto, DFIR。 | 全方位實力提升 (全領域) | [Root-Me 官網](https://www.root-me.org/) |
| **Hack The Box (HTB)** | 國際頂尖滲透平台，模擬真實企業環境；Pro Labs 提供 AD 內網攻防。 | DEVCORE 面試認可 / 全國賽 CTF II | [HTB 官網](https://www.hackthebox.com/) |
| **CyberDefenders** | 專業藍隊與數位鑑識靶場，包含 PCAP、Memory Dump、Disk Image 題型。 | 全國賽 Day1 AM (數位鑑識) | [CyberDefenders 官網](https://cyberdefenders.org/) |
| **pwnable.tw** | 高難度 Linux Binary Pwn 解題平台。 | DEVCORE 履歷加分指定平台 | [pwnable.tw 官網](https://pwnable.tw/) |
| **TryHackMe (THM)** | 引導式學習與雲端 VM 關卡，包含 Attacktive Directory 內網路線。 | AD 攻防觀念導入期 | [TryHackMe 官網](https://tryhackme.com/) |
| **CryptoHack** | 現代密碼學 (RSA, AES, ECC) 漸進式解題平台。 | 全國賽 CTF I (密碼學) | [CryptoHack 官網](https://cryptohack.org/) |
| **攻防世界 (XCTF)** | 全面開放之 CTF 題庫平台，包含大量中文歷年賽題。 | CTF 解題與快刷 | [XCTF 官網](https://adworld.xctf.org.cn/) |
| **VulnStack (紅日靶場)** | 免費下載之企業多層 AD 內網滲透靶場 VM。 | 內網橫向與 AD 實務演練 | [紅日安全](http://vulnstack.qiyuanxuetang.net/) |
| **picoCTF** | CMU 主辦，針對新手至中階之常態 Gym 練習區。 | 基礎能力建立 | [picoCTF 官網](https://picoctf.org/) |

---

## 🛠️ 二、 實踐推薦必備工具箱

### 1. Web 滲透與代理
- **Burp Suite Professional / Community**：HTTP 抓包、Replay、Intruder 爆破、Scanner。
- **Sqlmap**：SQL Injection 自動化偵測與數據庫拖庫工具。
- **Xray / AWVS**：Web 漏洞自動化主動/被動掃描器。
- **蟻劍 (AntSword) / 哥斯拉 (Godzilla)**：主流 Webshell 權限管理與後門利用工具。

### 2. 內網與 AD 攻防
- **GOAD (Game of Active Directory)**：Docker / Lab 一鍵建置 AD 內網演練環境。
- **Impacket 腳本集**：`psexec.py`, `wmiexec.py`, `GetUserSPNs.py` (Kerberoasting)。
- **Mimikatz**：Windows 記憶體 HASH/Pass-the-Hash 憑證提取工具。
- **Chisel / Ligolo-ng**：高效能內網代理與 SOCKS5 隧道穿透工具。

### 3. 數位鑑識與流量
- **Wireshark**：PCAP 封包解析與流量解密。
- **Volatility 2 / 3**：記憶體 Image (RAM Dump) 數位取證分析框架。
- **Autopsy / Sleuth Kit**：磁碟 Image 鑑識與刪除檔案復原。
- **VisualVM / jcmd**：Java JVM Live Heap Dump (`.hprof`) 密鑰與對象提取。

### 4. Binary 與逆向
- **Ghidra / IDA Free**：強大之反彙編與 Decompiler 逆向工程工具。
- **Radare2 (r2) / Cutter**：經典 Linux/UNIX 命令行二進制逆向分析、靜態反彙編與 Decompiler 工具。
- **pwntools**：Python 撰寫 Exploit Payload 之 Pwn 必備模組。
- **GDB + pwndbg**：Linux 二進制動態除錯器。
