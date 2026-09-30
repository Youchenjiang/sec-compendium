# 🔴 紅隊全領域實戰與武器庫體系 (Red Team Offensive Knowledge Base)

> ⚔️ **本目錄宗旨**：  
> 與 [../blue_team/](../blue_team/) 完全對稱建立之現代紅隊進攻作戰體系！  
> 涵蓋：外部資產情報偵察、邊界打點與 Web/API 突破、企業 Active Directory 網域統治，並預留主機提權、內網穿透與防禦規避擴充槽位。

---

## 🏛️ 紅隊核心架構導覽

```text
security/knowledge/red_team/
├── README.md                          # 本總覽入口
├── career_curriculum.md               # 🚀 現代紅隊通關主線課表 (Phase 1 ~ Phase 6、作戰鏈主幹)
├── index.md                           # ⚔️ 實戰技能細分矩陣 (全景 16 大攻擊領域・50 個專項技術點)
├── RED_TEAM_TECHNIQUES_CATALOG.md     # 📋 17 大領域與 70 項核心實戰技術索引目錄
│
├── learning_paths/                    # 📚【領域深度自學路徑】（預留擴展槽位）
│   └── README.md                      # 自學指南全景說明
│
└── playbooks/                         # 📋【70 篇標準化原子實戰手冊】
    ├── README.md                      # Playbooks 體系總覽與階段說明
    ├── PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md # 手冊規格書與標準模板
    ├── phase_1_recon_surface/         # 🌐 Phase 1: 外部情報與資產暴露面 (R01~R05，19 篇)
    ├── phase_2_perimeter_web/         # 🎯 Phase 2: 邊界打點與 Web/API 突破 (R06, R09~R15，30 篇)
    └── phase_3_domain_dominance/      # 👑 Phase 3: 企業身分與 AD 網域統治 (R07, R08, R16, R17，21 篇)
```

---

## 🧭 核心導覽與修課指引

| 模組 / 文檔 | 檔案連結 | 核心用途與適用對象 |
| :--- | :--- | :--- |
| **紅隊實戰通關課表** | [`career_curriculum.md`](career_curriculum.md) | **【修課主線】** Phase 1 ~ Phase 6 階段式進階課表、三層能力分流 (Core 25 篇必修) 與作戰鏈導引 |
| **全領域技能矩陣總表** | [`index.md`](index.md) | **【技術總覽】** 全景 16 大領域、50 項技術點（L1~L4 難度分級）與可練習靶場清單 |
| **70 項實戰技術索引** | [`RED_TEAM_TECHNIQUES_CATALOG.md`](RED_TEAM_TECHNIQUES_CATALOG.md) | **【原子清單】** 17 大領域、70 項技術點的標準命名、原語定義與檔案對照表 |
| **70 篇原子實戰手冊** | [`playbooks/`](playbooks/README.md) | **【即時作戰】** 嚴格遵循特戰速查標準（五動破題、指令速查、驗收閉環）之作戰手冊庫 |

---

## 🎯 相關模組交互參照

- **藍隊對稱體系**：防守方日誌研判、加固策略與 SOC 偵測規則，請參閱 👉 [`../blue_team/`](../blue_team/README.md)。
- **實體靶機與實作驗證**：真實靶機演練環境與題庫，請參閱 👉 [`../../practice/`](../../practice/README.md)。
