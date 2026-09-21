# 🧪 實驗室專屬深耕計畫庫 (Lab Execution Tracks)

> 本目錄收錄實驗室內部專屬推動之攻防體系化培訓、全國競賽衝刺、實戰靶場演練與教室建置藍圖。
> 
> 💡 **概念區隔說明**：
> - **`tracks/lab/`（本目錄，實驗室訓練軌）**：實驗室內部人才培育計畫、180 天攻防路線圖與金盾/Cyber Range 衝刺課表。
> - **[`../../security/knowledge/blue_team/playbooks/phase_6_capstone/ranges/`](../../security/knowledge/blue_team/playbooks/phase_6_capstone/ranges/README.md)**：Docker Compose 一鍵啟動之實體攻防容器靶場（紫隊模擬、Splunk BOTS、APT CTF）。

---

## 🏛️ 實驗室三大專案導覽地圖

```text
tracks/lab/
├── README.md                      # 本總覽入口
│
├── 90_runs/                       # 🗓️【180 天 90-Runs 密集攻防培訓主幹】
│   ├── README.md                  # 90-Runs 培訓體系總指南
│   ├── master_roadmap_leader.md   # 組長帶練總綱 (Day 1~180 完整教學與帶練指示)
│   ├── study_roadmap_member.md    # 成員自學路線圖 (純淨線上超連結版)
│   ├── cylab_classroom_setup_guide.md # CyLab / CTF 教室創建與 90 個 Run 逐日選題手冊
│   ├── platforms_and_resources.md # 線上靶場與推薦工具箱
│   ├── targets_and_certifications.md # DEVCORE 實習門檻與全國賽考綱剖析
│   ├── sources_index.md           # 📂 內部離線教材與題庫總索引 (25 題源、394 模組)
│   ├── security_domains_map.md    # 🗺️ 全域知識領域演進地圖 (9 大技術領域)
│   ├── doc_rules_and_standards.md # 📐 課綱規範與命名工程標準 (Level 1~3 分類)
│   ├── checklists/                # 雙平台 (picoCTF / PortSwigger) 實戰檢核表
│   └── templates/                 # 討論主題與表格語法模板庫
│
├── golden_shield_sprint/          # 🛡️【教育部資安金盾獎 30 天極速衝刺】
│   ├── README.md                  # 金盾獎衝刺專案總覽
│   ├── 30days_sprint_roadmap.md   # 30 天極速衝刺課表 (3 人小隊角色包幹與每日實戰)
│   └── exam_analysis_manual.md    # 歷屆試題深度剖析與官方命題大綱對照手冊
│
└── hitcon_range/                  # 🏟️【HITCON 藍隊 Cyber Range 實戰攻防特訓】
    ├── README.md                  # Cyber Range 藍隊演練總覽
    ├── cyber_range_blue_team_roadmap.md # 企業混合網演練特訓指南 (全員全能、四大奪分維度)
    └── wargame_case_study/        # HITCON 2026 PHP Composer 供應鏈安全案例與自動化挖掘
```

---

## 🚀 快速跳轉入口

| 學習或備戰目標 | 推薦起步文檔 | 核心特色 |
| :--- | :--- | :--- |
| **新人扎根 / 長期攻防培訓** | [**90-Runs 培訓體系**](90_runs/README.md) | 180 天、90 個 Run，由淺入深覆蓋 Web、二進位、流量分析與內網攻防 |
| **開立線上 CyLab CTF 教室** | [**90-Runs 教室建置手冊**](90_runs/cylab_classroom_setup_guide.md) | 依序對照 Run 1 至 Run 90，將題目與 Learning Path 精準加入平台 |
| **備戰教育部資安金盾獎** | [**金盾獎 30 天衝刺方案**](golden_shield_sprint/README.md) | 3 人隊伍領域包幹制、高強度每日刷題、歷屆單選真題與實務解構 |
| **備戰 HITCON 藍隊實網演習** | [**HITCON Cyber Range 指南**](hitcon_range/README.md) | 告警分流、數位鑑識、圍堵加固與規則撰寫（全員全能同構基因） |
