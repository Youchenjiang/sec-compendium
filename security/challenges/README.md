# 🎯 Security Challenges & Ranges Catalog (實戰題庫與靶場目錄)

本目錄匯整各類資安攻防競賽、真實靶場以及實作演練之題庫清單、自動化驗證工具與解題 Writeup。

---

## 🌐 核心入口與全平台聚合

- [**`UNIFIED_FREE_CHALLENGES_INDEX.md`**](UNIFIED_FREE_CHALLENGES_INDEX.md)：**全域免費實戰題庫導航中心**。聚合 CyberDefenders (82 題)、Hack The Box (359 題)、MTA (113 套)、PortSwigger (274 題)、picoCTF/CyLab (525 題)、CryptoHack (308 題)、TryHackMe (992 間房間) 與 Root-Me (608 題) 八大主流平台免付費實作資源，共收錄逾 3,260 道免費實戰題目。

---

## 📂 題庫與實戰專案索引

| 目錄 / 文件 | 類型 | 說明 |
|---|---|---|
| [**`UNIFIED_FREE_CHALLENGES_INDEX.md`**](UNIFIED_FREE_CHALLENGES_INDEX.md) | 🌐 全平台聚合 | 八大平台完全免費題庫大導航與跨領域攻防映射（共 3,260+ 道已驗證免付費題目） |
| [**`hitcon-2026-wargame/`**](hitcon-2026-wargame/) | 🏆 高階競賽攻防 | HITCON 2026 Wargame PHP Composer 安全挑戰賽（含自動化掃描器、4 AC Exploit 腳本、賽後技術覆盤與全域攻防框架） |
| [**`platforms/cyberdefenders/`**](platforms/cyberdefenders/) | 🔵 藍隊實戰靶場 | CyberDefenders 全量 257 題與 82 題免費靶場目錄與 CSV 數據庫 |
| [**`platforms/hackthebox/`**](platforms/hackthebox/) | 📦 滲透與調查靶場 | Hack The Box 全量 1650 題與 359 題免費機器/調查 (Sherlocks) 目錄與 CSV 數據庫 |
| [**`platforms/mta/`**](platforms/mta/) | 🦈 流量分析靶場 | Malware-Traffic-Analysis 113 套真實惡意封包分析實戰題目目錄與 CSV 數據庫 |
| [**`platforms/portswigger/`**](platforms/portswigger/) | 🌐 Web 滲透實戰 | PortSwigger Web Security Academy 官方 274 個實戰靶場實驗目錄與 CSV 數據庫 |
| [**`platforms/cylab_picoctf/`**](platforms/cylab_picoctf/) | 🏛️ CTF 競賽題庫 | CyLab / picoCTF 官方題庫 525 題快照數據庫與學習路徑對照目錄 |
| [**`platforms/cryptohack/`**](platforms/cryptohack/) | 🔐 現代密碼學靶場 | CryptoHack 全量 14 大分類、308 道 100% 免費密碼學挑戰目錄與 CSV 數據庫 |
| [**`platforms/tryhackme/`**](platforms/tryhackme/) | 🎯 導引實戰與 AD 靶場 | TryHackMe 官方即時 992 間實戰房間（AD、SOC、取證、Linux/Windows）目錄與 CSV |
| [**`platforms/rootme/`**](platforms/rootme/) | 🚩 經典全領域攻防 | Root-Me 官方即時 608 道全領域免費挑戰（Web、系統、密碼、取證）目錄與 CSV |
| [**`sync/`**](sync/) | 🔄 自動同步框架 | 多平台實戰題庫通用同步器、API 爬蟲與標準化匯出 CLI |

---

## 🔄 題庫自動同步框架 (Challenge Sync Framework)

本目錄內建通用題庫同步框架，支援自動對接各平台官方 API / 網頁爬取最新題目，並自動生成統一規格之 CSV 與 Markdown Catalog：

```bash
# 1. 查看支援之平台適配器
python -m security.challenges.sync.main --list

# 2. 同步單一平台 (例如 MTA 或 CyberDefenders)
python -m security.challenges.sync.main --platform mta
python -m security.challenges.sync.main --platform cyberdefenders

# 3. 一鍵同步所有平台
python -m security.challenges.sync.main --all
```

---

## 📌 相關架構模組導航

- **數位鑑識取證資料集 (Forensics Evidence)**：已統整移至 [`security/exams/evidence/`](../exams/evidence/)（專供模擬測驗取證實作）。
- **90-Runs 實戰衝刺檢核表**：已統整移至 [`tracks/lab/90_runs/checklists/`](../../tracks/lab/90_runs/checklists/)（含 PortSwigger、picoCTF 與雙平台綜合檢核表）。
- **攻防實驗室教室環境手冊**：已統整移至 [`tracks/lab/setup/cylab_classroom_setup_guide.md`](../../tracks/lab/setup/cylab_classroom_setup_guide.md)。
