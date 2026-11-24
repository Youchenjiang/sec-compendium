# 🦈 Wireshark 網路封包分析與流量鑑識全量實戰題庫目錄

> **彙整目錄位置**：[`security/practice/wireshark_labs/`](.)  
> **建立時間**：2026-10-04  
> **專案定位**：全面整合本知識庫中分散於各課程、模擬考、技能競賽、CTF 平台與國際藍隊靶場的 **Wireshark / PCAP 實戰練習題**，形成由淺入深的標準化實作進階路徑。

---

## 🗺️ 題庫模組導覽

> 💡 **專屬學習路線推薦**：針對完全免訂閱、100% 免費練習需求，已特別編撰 👉 [**`CYLAB_ROOTME_LEARNING_PATH.md`（CyLab + Root-Me 雙平台 Wireshark 終極學習路徑）**](./CYLAB_ROOTME_LEARNING_PATH.md)。

| 模組編號 | 核心內容說明 | 涵蓋來源 | 檔案連結 |
| :---: | :--- | :--- | :--- |
| **⭐ 專屬路線** | **100% 免費雙平台通關路徑** | CyLab (9 題) + Root-Me (28 題) 6 階段完整進階 | [CYLAB_ROOTME_LEARNING_PATH.md](./CYLAB_ROOTME_LEARNING_PATH.md) |
| **01** | **CTF 初中階實戰精選** | picoCTF / CMU CyLab 官方精選 9 道題 | [01_picoctf_cylab_challenges.md](./01_picoctf_cylab_challenges.md) |
| **02** | **通訊協定與進階鑑識挑戰** | Root-Me 官方 Network（22+ 題）& Forensic（8 題） | [02_rootme_network_and_forensics.md](./02_rootme_network_and_forensics.md) |
| **03** | **技能競賽真題與模擬考題** | 全國技能競賽/金盾獎真題（Topic1/traffic）+ 模考 A/B 卷 | [03_competition_and_exam_questions.md](./03_competition_and_exam_questions.md) |
| **04** | **國際藍隊與在線房間靶場** | CyberDefenders 7 大 PCAP 靶場 + TryHackMe 5 大房間 + MTA | [04_cyberdefenders_and_tryhackme.md](./04_cyberdefenders_and_tryhackme.md) |
| **05** | **過濾語法與 Tshark 指令速查** | 常用 Display Filters、Capture Filters 與 Tshark 腳本化指令 | [05_wireshark_cheatsheet_and_filters.md](./05_wireshark_cheatsheet_and_filters.md) |

---

## 🎯 推薦通關學習路徑

```
[Level 1: 基礎操作與入門]
  ├── 01 picoCTF: Packets Primer & shark on wire 1 (追蹤串流與 UDP 雜訊排查)
  ├── 04 TryHackMe: Wireshark: The Basics & Packet Operations
  └── 02 Root-Me: FTP, TELNET, Twitter authentication (明文憑證提取)
        ▼
[Level 2: 協定解讀與異常分析]
  ├── 01 picoCTF: Wireshark doo dooo do doo... & PcapPoisoning
  ├── 02 Root-Me: SSL - HTTP exchange, DNS zone transfert, ICMP payload, ARP Spoofing
  └── 04 TryHackMe: Wireshark: Traffic Analysis & Tshark CLI
        ▼
[Level 3: 進階解密、密鑰與隱蔽通道]
  ├── 01 picoCTF: WebNet0 / WebNet1 (載入私鑰解密 TLS) & shark on wire 2 (Port 隱蔽通道)
  ├── 02 Root-Me: NTLM, Kerberos, WPA2/WPA3, DNS / ICMP Exfiltration
  └── 03 技能競賽真題: Topic1.pcap (DNS 隱蔽通道資料外洩)
        ▼
[Level 4: 企業攻擊鏈還原與威脅獵捕 (APT & C2)]
  ├── 03 技能競賽真題: traffic.pcap (SQLi ➔ RCE Web 攻擊鏈還原)
  ├── 04 CyberDefenders: PacketMaze, WireDive, DanaBot, Lockdown
  └── 02 Root-Me Forensic: Command & Control 2~6, C2 Mythic
```

---

## 🛠️ 本地常用分析工具配備

- **Wireshark GUI**：主要用於互動式視覺化分析、封包時序檢視、匯出物件。
- **Tshark**：命令列批次過濾、大量 PCAP 統計、自動化腳本分析。
- **Python (Scapy / Pyshark)**：自訂欄位解析、異常隱蔽通道字元轉換、批次處理。
- **NetworkMiner**：免設定自動提取圖片、傳輸檔案、憑證與主機資訊。
- **Zeek**：巨量流量（數 GB ~ 數十 GB）快速結構化轉日誌工具。
