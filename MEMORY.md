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