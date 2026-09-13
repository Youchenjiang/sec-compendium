# Agent Persistent Memory

> **Every agent session MUST read this file first** (defined in .agent/rules.md).
> **Every agent session MUST update this file before ending.**

---

## 🔑 User Preferences
- **Language**: 繁體中文 preferred for casual conversation; code/commits in English.
- **Style**: Direct, no fluff. Get things done with high engineering rigor.

---

## 📋 Current Active Tasks
- 專案轉型規劃：定位為**資安讀書會輔助專案**（CTFd 作為實戰演練與評測子模組）。
- 規劃讀書會核心結構：課程大綱（Syllabus）、每週議題導讀（Weekly Digests）、實戰任務清單（Labs & Milestones）。

---

## 🏗️ Architectural Context
- **Project**: 資安讀書會輔助專案（Study Group Assistant & Security Training Platform）
- **Core Modules**:
  - `study/` (規劃中): 讀書會進度排程、每週主題規劃、論文/技術簡報共筆與研討導讀
  - `ctfd/` / `plugins/` (實戰靶場模組):
    - `plugins/dynamic_shuffle_flag/`: Python / Flask 防作弊動態 Flag 外掛（即時置換二進位執行檔、圖片 EXIF 與尾部 ZIP）
    - `challenges/reverse_graduation/`: C 語言逆向題（Zig C Compiler / macOS Universal Binary 跨架構建置）
    - `patches/core_changes.patch`: CTFd 核心補丁（首殺/先鋒加分、繁中介面）
    - `database/ctfd_dump_2026.sql`: 演練資料庫結構
    - `automation/send_final_top10.py`: 賽後自動化結算信件工具
  - `install.sh`: 一鍵快速套用腳本

---

## ✅ Completed Decisions & Lessons Learned
- Initialized with `research` scaffolding preset.
- **2026-09-13 專案轉型決策**：確立以「讀書會輔助」為核心主體，CTFd 套件收斂為「實戰靶場演練模組」。
- 更新 `policy.yml` 允許 scope 擴充 `study`, `plan`, `ctfd`, `labs`, `challenge`, `infra`, `build`, `release`, `governance`。
- 配置 Conventional Commits、TruffleHog 機敏金鑰防外洩與 PR-Agent 自動審查。
- 解決 Sourcery-AI 與 LlamaPReview 提出的 7 則審查建議（補齊 issues 權限、分支名稱正規驗證、移除 unverified 過濾、限制 PR Agent 觸發範疇、鎖定第三方 Action Commit SHA、明確漏洞通報管道），PR #2 審查執行緒全數標記 Resolved 並達 100% 通過。
- **2026-09-13 知識庫與讀書會真實歷史重構（Phase 1 Ingestion）**：
  - 徹底清除未經授權開立的 PR #3 及 5 個虛構提交，關閉 PR #3 並刪除遠端分支。
  - 嚴格遵守版本演進（Git Version Evolution）原則：保留檔案原始名稱與時間線，透過 `git mv` 100% Rename 無損銜接歷史，重現從 8/5 始祖檔案 $\rightarrow$ 8/9 v5.0 $\rightarrow$ 8/13~8/23 v5.3~v5.8 細部迭代。
  - 實施嚴格原子化提交（Atomic Commits）：按模組獨立拆分（領域架構 A3、藍隊職涯課表、31 大學習路徑、41 本原子 Playbooks、週五讀書會實體課表、金盾獎衝刺與全真模擬考庫）。
  - 資安防線：在 `.gitignore` 阻擋 `*.key`、`*.pem` 及 `security/projects/`（排除 CYM 專案），防止私鑰與研究專案外洩。
  - 採納「公共技術基石（紅白對稱） $\times$ 雙軌執行計畫（實驗室 vs 社團）」架構，撰寫並通過 `security/ARCHITECTURE_REDESIGN_RFC.md`。
- **PR #4 合併完成（Phase 1 Ingestion Completed）**：PR #4 已成功合入 `main`，包含全部 103 份核心資安資產、RFC 文檔與 PR-Agent 韌性架構，本地分支已同步清理完畢。
- **Phase 2 架構重整完成（Decoupling & Restructuring）**：
  - 公共技術基石：建立 `security/blue_team/`（31 路徑 + 41 手冊 + 課表）與 `security/red_team/`（資源索引 + 對稱槽位），標準化題庫 `security/challenges/`、框架規範 `security/framework/` 與考卷庫 `security/exams/`。
  - 雙軌執行計畫解耦：建立 `tracks/lab/`（180天90-Runs、金盾衝刺、Cyber Range）與 `tracks/club/`（資安社週五讀書會實體課表與目標）。
  - 平台資產收斂：將 CTFd 核心與插件收納於 `ctfd/`。
  - 檔名規範化重構：移除歷史前綴 `A_`、`B1_`~`B5_`、`C1_`~`C4_`、`D1_`~`D2_` 與中文字元檔名，全數標準化為 Linux/Git 友善之 `lower_snake_case`，全程透過 `git mv` 達成 100% Rename 無損遷移並修復全庫內部 Markdown 相對鏈結。