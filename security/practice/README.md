# 🎯 資安實踐驗證與評量中心 (Security Practice & Evaluation Center)

> 本目錄為全專案的**「實戰檢驗與能力評估中樞」**。  
> 承接 [`../knowledge/`](../knowledge/blue_team/README.md) 所建立之理論防禦與攻防知識，提供成套的實體線上題目、全真模擬試卷與數位鑑識樣本，以驗證實戰攻防與應變能力。

---

## 🏛️ 核心雙模組導覽

```text
security/practice/
├── challenges/      # 🌐【實戰題庫與線上靶場目錄】
│   ├── UNIFIED_FREE_CHALLENGES_INDEX.md  # 8 大平台完全免費題庫大導航 (3,260+ 題)
│   ├── platforms/   # 各大平台全量題目快照與 CSV 數據庫 (3,945+ 題)
│   └── sync/        # 多平台 API 題目自動同步爬蟲與 CLI
│
└── exams/           # 📝【全真模擬試卷與評量庫】
    ├── mock_exam_a_100q_questions.md     # 金盾獎客觀選擇題全真試卷 (100 題閉卷題本)
    ├── mock_exam_a_100q_solutions.md     # A 卷逐題正解與干擾項深度辨析
    ├── mock_exam_b_lab_questions.md      # 實務推演題本 (IR/加固/取證/CTF 題本，內嵌日誌截圖)
    ├── mock_exam_b_lab_solutions.md      # B 卷操作還原與官方解題手冊
    ├── high_frequency_flashcards.md      # 考前口試抽測速記卡 (3 人包幹分工)
    ├── cheatsheets/                      # 實務指令與核心考點速查專區
    └── evidence/                         # 實體數位鑑識 PCAP 流量封包與取證標本
```

---

## 🧭 模組索引與快速跳轉

| 模組名稱 | 路徑 | 核心內容與亮點 | 推薦使用情境 |
| :--- | :--- | :--- | :--- |
| **全平台實戰題庫** | [**`challenges/`**](challenges/README.md) | 聚合 CyberDefenders、HTB、MTA、PortSwigger、picoCTF、CryptoHack、THM、Root-Me 八大平台題庫與自動同步引擎。 | 平日演練、90-Runs 實作認領、專項技能補強 |
| **免費實戰題庫導航** | [**`UNIFIED_FREE_CHALLENGES_INDEX.md`**](challenges/UNIFIED_FREE_CHALLENGES_INDEX.md) | 跨領域攻防映射，精選 3,260+ 道 100% 免付費已驗證實作題目。 | 無需課金快速起步、新手入門引導 |
| **全真模擬測驗題本** | [**`exams/`**](exams/README.md) | A 卷（100 題客觀單選）＋ B 卷（81 題情境推演實作題），徹底告別無環境無法解題之困境。 | 金盾獎/技能競賽考前 4 天衝刺自評 |
| **考點核心速查專區** | [**`cheatsheets/`**](exams/cheatsheets/README.md) | 涵蓋名詞對稱、Wireshark 過濾器、Nmap 與 Linux 防火牆命令速查手冊。 | 考前速記、突發事件排查應變 |

---

## 🚀 常用操作指南

### 1. 執行題庫同步引擎
```bash
# 查看支援之 8 大平台適配器清單
python -m security.practice.challenges.sync.main --list

# 同步指定平台題庫數據 (例如 CyberDefenders 或 MTA)
python -m security.practice.challenges.sync.main --platform cyberdefenders
python -m security.practice.challenges.sync.main --platform mta
```

### 2. 開展模擬測驗與評量自評
- **客觀筆試自測**：前往 [A 卷題本](exams/mock_exam_a_100q_questions.md)，閉卷限時 90 分鐘作答。
- **實務推演測驗**：前往 [B 卷題本](exams/mock_exam_b_lab_questions.md)，三人小隊各司其職推演封包與日誌。
- **成績登記與自評**：於 [exams/README.md 評分表](exams/README.md#-團隊自評成績表-scorecard) 填寫成績指標。

---

> 💡 **相關研訓專軌指引**：  
> - 欲將本目錄題庫對接 180 天攻防課表，請查閱 👉 [`../../tracks/lab/90_runs/`](../../tracks/lab/90_runs/README.md)。  
> - 欲對接金盾獎 30 天衝刺方案，請查閱 👉 [`../../tracks/lab/golden_shield_sprint/`](../../tracks/lab/golden_shield_sprint/README.md)。
