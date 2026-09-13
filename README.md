# 🛡️ NCtfU 資安社與實驗室研訓平台 (NCtfU Security Platform & Knowledge Base)

> 本專案為兼具**「資安核心公共技術基石」**、**「雙軌讀書會執行計畫」**與**「CTFd 實戰評測靶場」**之綜合性資安工程體系。

---

## 🏛️ 專案三大核心支柱 (Three Architectural Pillars)

`	ext
ctfd-kit/
│
├── 🛡️ security/      # 【資安核心技術知識庫】(全體共享技術基石)
│   ├── framework/  # 全域架構地圖 (A3)、3.9萬檔案索引 (A2)、文檔規範 (A0)
│   ├── blue_team/    # 🔵 藍隊體系 (Phase 0~6 課表、31大學習路徑、41本原子手冊)
│   ├── red_team/     # 🔴 紅隊體系 (實戰資源索引、攻防手法與滲透擴展槽位)
│   ├── challenges/   # 🎯 靶場與實戰題庫清單 (picoCTF, PortSwigger, CyLab)
│   ├── exams/        # 📝 全真模擬考卷 (金盾/技能競賽 A/B卷題本與解析、速記卡)
│   └── notes/        # ⚡ 基礎考點名詞速查、網路安全指令速查
│
├── 🚀 tracks/        # 【雙軌執行計畫庫】(實施方案與日程對齊)
│   ├── lab/          # 🧪 實驗室專屬深耕計畫 (180天 90-Runs、金盾衝刺、HITCON Range)
│   └── club/         # 👥 NCtfU 資安社讀書會 (週五讀書會簡表、每週實作課表、目標規劃)
│
└── 🎯 ctfd/          # 【CTFd 實戰靶場與演練模組】(線上評測平台)
    ├── automation/   # 賽後自動化結算信件寄送腳本
    ├── challenges/   # 靶機題目源碼 (C/Zig) 與同步工具
    ├── database/     # CTFd 初始化資料庫結構與預設帳密 dump
    ├── patches/      # CTFd 核心繁中化與首殺加分補丁
    ├── plugins/      # dynamic_shuffle_flag 動態 Flag 外掛
    └── install.sh    # 一鍵快速部署至目標 CTFd 伺服器
`

---

## 🧭 快速導覽與指引

- **想查閱藍隊實戰手冊與應變 SOP？** 👉 請進 [security/blue_team/](security/blue_team/)
- **想查閱紅隊攻擊技術與武器庫？** 👉 請進 [security/red_team/](security/red_team/)
- **想查看實驗室 180 天 90-Runs 學習進度？** 👉 請進 [	racks/lab/90_runs/](tracks/lab/90_runs/)
- **想參與資安社週五讀書會每週選題實作？** 👉 請進 [	racks/club/](tracks/club/)
- **想架設與部署 CTFd 靶場？** 👉 請進 [ctfd/](ctfd/)
