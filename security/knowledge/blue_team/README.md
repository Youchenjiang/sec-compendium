# 🔵 藍隊體系與實戰防衛知識庫 (Blue Team Defensive Knowledge Base)

> 本目錄為全專案的**「藍隊體系化防護作戰體系」**。  
> 涵蓋事前架構加固、即時 SOC 告警研判、威脅獵捕、數位鑑識（DFIR）、紫隊自動化對抗與法規合規標準。

---

## 🏛️ 藍隊核心架構導覽

```text
security/knowledge/blue_team/
├── README.md                      # 本總覽入口
├── career_curriculum.md           # 🚀 現代藍隊通關主線課表 (Phase 0 ~ Phase 6、36 項核心必修)
├── index.md                       # 🛡️ 實戰技能細分矩陣 (八大作戰區塊・31 大領域・107 項技術矩陣)
│
├── learning_paths/                # 📚【31 大領域深度自學路徑】
│   ├── README.md                  # 學習路徑全景導覽庫
│   ├── cyberdefenders_free_catalog_mapping.md # CyberDefenders 82 題免費靶場深度映射
│   └── block_1_hardening/ ~ block_8_grc_standards_custody/ # 8 大區塊專案指南
│
└── playbooks/                     # 📋【107 篇標準化實戰防禦手冊】
    ├── README.md                  # Playbooks 體系總覽與驗證說明
    ├── PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md # 手冊規格書與標準模板
    └── phase_0_foundation/ ~ phase_6_capstone/ # 7 大階段原子手冊庫
```

---

## 🧭 核心導覽與修課指引

| 模組 / 文檔 | 檔案連結 | 核心用途與適用對象 |
| :--- | :--- | :--- |
| **藍隊實戰通關課表** | [`career_curriculum.md`](career_curriculum.md) | **【修課主線】** Phase 0 ~ Phase 6 階段式進階課表、SOC 告警分流八問、IR 圍堵 SOP 與 36 項 Core 核心必修 |
| **全領域技能矩陣總表** | [`index.md`](index.md) | **【技術總覽】** 八大現代防禦區塊、31 大領域、107 項技術點（L1~L4 難度分級）與可練習靶場清單 |
| **31 大深度學習路徑** | [`learning_paths/`](learning_paths/README.md) | **【觀念扎根】** 底層架構剖析、前置測試、核心指令、進階防禦與階段通過檢查表 |
| **107 篇原子實戰手冊** | [`playbooks/`](playbooks/README.md) | **【即時作戰】** 包含可複製程式碼、環境驗證、防禦加固與關聯規則之作戰 Playbooks |

---

## 🎯 相關模組交互參照

- **紅隊對稱體系**：與進攻手法、武器庫對照，請參閱 👉 [`../red_team/`](../red_team/README.md)。
- **實體容器靶場**：啟動 Docker 實戰靶場（Caldera 紫隊、Splunk BOTS、APT CTF），請參閱 👉 [`playbooks/phase_6_capstone/ranges/`](playbooks/phase_6_capstone/ranges/README.md)。
- **全真模擬試卷與取證標本**：進行金盾獎/技能競賽題本驗收，請參閱 👉 [`../../practice/exams/`](../../practice/exams/README.md)。
