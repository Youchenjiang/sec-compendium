# 🏛️ 資安知識庫架構重構與演進設計 RFC (Architecture Redesign RFC)

> **文檔狀態**：PROPOSED / ACCEPTED IN PRINCIPLE  
> **制定日期**：2026-09-13  
> **目標版本**：下一階段 PR 重整目標架構 (Phase 2 Restructuring)  
> **核心宗旨**：釐清「公共技術基石（紅白對稱）」與「雙軌執行計畫（實驗室 vs 社團）」的權責邊界，建立可長可久、容易擴展的標準化資安工程體系。

---

## 📜 一、 歷史背景與組織演進脈絡 (Historical Context)

整套資安知識庫與讀書會系統並非憑空捏造，而是經歷了三個具體的組織發展階段：

1. **階段一：實驗室內部深耕（2026/8/5 ～ 8/9）**：
   - 誕生了 framework（規範與本地 3.9 萬檔案索引）、B_roadmaps（180 天 90-Runs 主幹）、C_challenges（picoCTF / PortSwigger 題庫）、D_templates（討論與語法模板）。
   - 目標是為實驗室建立紮實的底層資安攻防能力。
2. **階段二：NCtfU 資安社線上讀書會規劃（2026/9/8）**：
   - 規劃社團每週五聚會的課表與機制，評估社團到底該以「金盾獎」還是「全國技能競賽」為導向。
   - 產出了 friday_study_group_officer_summary.md、B3_NCTFU_FRIDAY_GOALS（目標考量）與 C5_NCTFU_FRIDAY_PRACTICE（每週實作認領課表）。
3. **階段三：實驗室出征備戰 ➔ 藍隊高強度大補強（2026/8月下旬 ～ 9月）**：
   - 因為實驗室組隊報名了**「金盾獎」**與**「HITCON Cyber Range」**，急需強化藍隊調查、SOC 分流、系統硬化與取證能力。
   - 迅速攻堅產出 BLUE_TEAM_CAREER_CURRICULUM（Phase 0~6）、31 個領域的深度學習路徑（learning_paths/）、41 本原子實戰手冊（playbooks/）以及 A/B/C 卷全真模擬題本（final_mock_exams/）。

---

## ⚠️ 二、 現狀問題與痛點分析 (Problem Statement)

1. **公共資源與執行計畫邊界混淆**：
   - 目前所有的藍隊手冊與路徑都放在根目錄，但資安社讀書會與實驗室讀書會都需要引用這些資源，若放在單一實驗室或社團目錄下會造成所屬權責錯亂。
2. **紅藍資源嚴重失衡 (Asymmetric Knowledge Gap)**：
   - 藍隊資源極度充沛（31 份指南 + 41 本手冊）。
   - 紅隊資源目前僅有一份資源索引（RED_TEAM_PRACTICE_RESOURCES_INDEX.md），缺乏對應的領域指南與攻擊 Playbooks，且缺乏預留的標準目錄。
3. **名稱定義不夠精確**：
   - 原本將金盾獎與模擬考歸類為紫隊，但金盾獎與技能競賽本質上是「綜合性資安競賽/檢定」，應以競賽專項定位，避免名不符實。

---

## 🎯 三、 目標架構設計 (Target Architecture)

重構的核心思維：**「將『公共技術基石（紅白對稱）』與『雙軌執行計畫（實驗室 vs 社團）』徹底解耦」**。

```text
ctfd-kit/
│
├── security/                 # 🛡️【資安核心專業知識庫】(所有人共享的公共技術基石)
│   ├── 00_framework/         # 架構地圖 (A3)、本地索引 (A2)、規範標準 (A0)
│   │
│   ├── red_team/             # 🔴 紅隊體系 (Web, Pwn, Reverse, AD, 滲透手冊...)【擴展槽位】
│   │   ├── index.md          # 紅隊實戰資源全景索引
│   │   ├── learning_paths/   # 紅隊各領域自學路徑 (Web安全、逆向工程、內網滲透...)
│   │   └── playbooks/        # 紅隊武器與攻擊 SOP (SQLi Bypass、Kerberoasting、提權...)
│   │
│   ├── blue_team/            # 🔵 藍隊體系 (因金盾/Cyber Range 大補強，目前極度扎實)
│   │   ├── index.md          # 藍隊實戰資源全景索引
│   │   ├── career_curriculum.md # Phase 0~6 現代藍隊職涯課表
│   │   ├── learning_paths/   # 31 大領域深度路徑 (01~31)
│   │   └── playbooks/        # 41 本原子實戰手冊 (五動追兇流、Windows Logon、Sysmon...)
│   │
│   ├── challenges/           # 🎯 實體靶場與題庫清單 (picoCTF, PortSwigger, CyLab 題庫)
│   ├── exams/                # 📝 全真題庫與歷屆解析 (A/B/C 卷全真題本、考前速記卡)
│   └── notes/                # 基礎考點速查表 (Cheatsheets)
│
└── tracks/                   # 🚀【具體推動的各項讀書會與培訓計畫 (Plans & Execution)】
    │
    ├── lab/                  # 🧪【實驗室專屬計畫】
    │   ├── 90_runs/          # 實驗室 180 天 / 90-Runs 密集培訓藍圖 (B1, B2, 模板)
    │   ├── golden_shield_sprint/ # 實驗室金盾獎 30 天衝刺方案 (B4, 歷屆試題分析)
    │   └── hitcon_range/     # 實驗室 HITCON Cyber Range 出征藍圖 (B5)
    │
    └── club/                 # 👥【NCtfU 資安社讀書會計畫】
        ├── friday_study_group_officer_summary.md     # 社團幹部簡明進度表
        ├── nctfu_friday_goals.md    # 社團定位與戰略考量 (金盾 vs 技能競賽, 原 B3)
        ├── nctfu_friday_practice.md # 每週題目認領實作課表 (原 C5)
        ├── skills_competition.md    # 全國技能競賽培訓指南
        └── course_assignments.md    # 課程作業對照
```

---

## 📋 四、 紅隊擴展補齊清單 (Red Team Backlog / Gaps)

為了讓未來知識庫達到實質上的紅白平衡，後續應依循藍隊的標準規格逐步補齊紅隊資產：

1. **紅隊領域學習路徑 (security/red_team/learning_paths/)**：
   - 01_WEB_SQLI_COMMAND_INJECTION_LEARNING_PATH.md
   - 02_ACTIVE_DIRECTORY_INTERNAL_PENETRATION_LEARNING_PATH.md
   - 03_BINARY_EXPLOITATION_ROP_PWN_LEARNING_PATH.md
   - 04_REVERSE_ENGINEERING_GHIDRA_IDA_LEARNING_PATH.md
   - 05_CLOUD_ATTACK_SURFACE_IAM_LEARNING_PATH.md
2. **紅隊實戰攻擊武器庫 (security/red_team/playbooks/)**：
   - 包含漏洞利用 SOP、WAF Bypass 技巧、權限提升（Privilege Escalation）手冊、橫向移動（Lateral Movement）手冊。

---

## 🚀 五、 兩階段執行計畫 (Execution Plan)

- **Phase 1（本次 PR）**：
  - 將現有 103 份核心資安資產以最真實的歷史演進（8/5 始祖 ➔ 8/9 v5.0 ➔ 8/23 v5.8）及原子化提交全數安全入庫。
  - 將本 RFC（ARCHITECTURE_REDESIGN_RFC.md）提交入庫，作為全團隊共識與設計藍本。
  - 確保 CI 檢查 100% 通過（TruffleHog 無機敏私鑰洩漏、Markdown 格式合規）。
- **Phase 2（下一階段 PR）**：
  - 依據本 RFC，執行目錄實質重組遷移（使用 git mv 保持歷史紀錄）。
  - 將檔案分別歸位至 security/red_team/、security/blue_team/、	racks/lab/、	racks/club/。
  - 建立紅隊擴展的第一批基礎框架。
