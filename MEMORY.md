# Agent Persistent Memory

> **Every agent session MUST read this file first** (defined in .agent/rules.md).
> **Every agent session MUST update this file before ending.**

---

## 🔑 User Preferences
- **Language**: 繁體中文 preferred for casual conversation; code/commits in English.
- **Style**: Direct, no fluff. Get things done with high engineering rigor.

---

## 📋 Current Active Tasks
- 專案架構與規範化整頓：確立「公共技術基石（`security/`） $\times$ 三大研訓專軌（`tracks/`） $\times$ CTFd 實戰靶場（`ctfd/`）」三足鼎立體系。
- 嚴格落實 Git 原子化提交與分支政策，確保所有變更具備高可逆性與精準 scope 標註。

---

## 🏗️ Architectural Context
- **Project**: NCtfU 資安研訓平台與技術知識庫 (NCtfU Security Platform & Knowledge Base)
- **Core Modules**:
  - `security/` (公共技術基石庫):
    - `knowledge/`:
      - `blue_team/`: Phase 0~6 藍隊職涯課表、31 大領域學習路徑、107 篇原子化實戰防禦手冊、實體靶場 ranges/
      - `red_team/`: 16 大作戰維度全景索引、武器庫與攻防路徑
    - `practice/`:
      - `challenges/`: 8 大主流攻防平台 (HTB, THM, CyberDefenders, PortSwigger, etc.) 3,945+ 免費關卡目錄與全自動爬蟲
      - `exams/`: 金盾獎/技能競賽 A/B 卷全真題本解析、離線取證封包標本 (evidence/) 與考點 Cheatsheets
    - `tools/`: Playbook 品質驗證器 (`validate_playbooks.py`) 與 Code Auditor 白箱審計引擎
  - `tracks/` (三大研訓專軌庫):
    - `lab/`: 實驗室專屬深耕計畫 (180 天 90-Runs 課表與 CyLab 教室建置、金盾 30 天衝刺、HITCON Range 與 Wargame 案例庫)
    - `club/`: NCtfU 資安社讀書會 (週五讀書會雙軌課表、Discord 分流、CTF 戰隊 6 個月培訓與出國指南)
    - `courses/`: 大學學術課程與教學出題專軌 (中央資管陳奕明教授《電腦網路安全》14 週課表與 CyLab 出題指南)
  - `ctfd/` (實戰評測靶場模組):
    - `event_guide.md`: 🏆 中央資管碩一茶會 Mini-CTF 全套活動手冊暨官方解題指南 (Write-Up)
    - `plugins/dynamic_shuffle_flag/`: Python / Flask 防作弊動態 Flag 外掛
    - `challenges/`: 題目原始碼、二進制編譯與自架題目 CSV
    - `patches/`: CTFd 核心繁中化與首殺加分補丁
    - `database/ctfd_dump_2026.sql`: 初始化資料庫結構
    - `automation/send_final_top10.py`: 賽後自動化結算信件工具
    - `assets/`: 競賽認證範本與素材資源
    - `install.sh`: 一鍵快速套用腳本

---

## ✅ Completed Decisions & Lessons Learned
- Initialized with `research` scaffolding preset.
- **2026-09-13 專案轉型決策**：確立以「讀書會輔助」為核心主體，CTFd 套件收斂為「實戰靶場演練模組」。
- 更新 `policy.yml` 允許 scope 擴充 `study`, `plan`, `ctfd`, `labs`, `challenge`, `infra`, `build`, `release`, `governance`, `sec`, `agent`, `tracks`。
- 配置 Conventional Commits、TruffleHog 機敏金鑰防外洩與 PR-Agent 自動審查。
- 解決 Sourcery-AI 與 LlamaPReview 提出的 7 則審查建議，PR #2 審查執行緒全數標記 Resolved 並達 100% 通過。
- **2026-09-13 知識庫與讀書會真實歷史重構（Phase 1 Ingestion）**：
  - 徹底清除未經授權開立的 PR #3 及 5 個虛構提交，關閉 PR #3 並刪除遠端分支。
  - 嚴格遵守版本演進原則：透過 `git mv` 100% Rename 無損銜接歷史。
  - 採納「公共技術基石 $\times$ 雙軌執行計畫」架構，撰寫並通過 `docs/rfc/0001_architecture_redesign_rfc.md`。
- **PR #4 合併完成**：包含核心資安資產、RFC 文檔與 PR-Agent 韌性架構。
- **Phase 3 CyberDefenders 全自動化同步與題庫整併（2026-09-16）**：
  - 建立官方 API 自動化爬取工具，精準標記 82 題完全免費與 174 題需訂閱。
  - 建立 `security/blue_team/learning_paths/cyberdefenders_free_catalog_mapping.md`。
- **2026-09-20 專案全域架構清理與標準化重構（Branch: `refactor/security-tracks-structure-cleanup`）**：
  - **學術專軌獨立**：由 `competitions/` 剝離並建立獨立 `tracks/courses/`，收納中央資管《電腦網路安全》出題指南。
  - **社團計畫模組化**：`tracks/club/` 劃分為 `friday_study_group/`（現行課表＋歷史存檔 `archive/`）與 `competitions/`（純競賽培訓）。
  - **實驗室培訓導覽體系化**：補齊 `tracks/lab/` 總覽及 4 個子目錄 README 導覽，明確界定「培訓課表」與「Docker 容器靶場」分工。
  - **藍隊知識庫門戶化**：建立 `security/blue_team/README.md` 首頁入口。
  - **超連結與語法零缺陷**：全庫 240 份 Markdown、747 個相對路徑連結 100% 暢通無死鏈；修復目錄錨點跳轉；`ctfd/README.md` 圍欄修復。
  - **品質驗收基準線**：`python security/tools/validate_playbooks.py` 107 篇手冊（31,971 行）100% 全數通過驗收。
  - **解散架構大雜燴**：解散 `security/framework/`，白黑盒審計方法論移入 `security/tools/code_auditor/audit_methodology.md`，RFC 提升至 `docs/rfc/`，90-Runs 課綱規範與地圖移入 `tracks/lab/90_runs/`。
  - **考點速查全面收斂**：消滅單薄的 `security/notes/` 目錄，將速查表整併至 `security/exams/cheatsheets/`。
  - **競賽實戰案例歸位**：將 `security/challenges/hitcon-2026-wargame/` 搬移至 `tracks/lab/hitcon_range/wargame_case_study/`，使 `challenges/` 專注於平台題庫與爬蟲。
  - **清理二進制編譯垃圾**：從 `ctfd/challenges/binaries/` 刪除亂碼 `.obj` 與 `vc140.pdb`，在 `.gitignore` 加入 C/C++ 編譯產物規則。
  - **架構整頓方案 A 落地**：`security/` 收斂為 `knowledge/`（`blue_team/`, `red_team/`）＋ `practice/`（`challenges/`, `exams/`）＋ `tools/`；實體容器靶場歸位至 `blue_team/playbooks/phase_6_capstone/ranges/`。
  - **誤放檔案與名不符實精準歸位**：
    - `ctf_event_guide.md`（中央資管碩一茶會 Mini-CTF 活動手冊暨 Write-Up）從社團專軌遷移至 `ctfd/event_guide.md`。
    - `skills_competition.md` 檔名名不符實問題：正式重命名為 `tracks/club/competitions/ctf_competition_roadmap.md`（CTF 戰隊 6 個月培訓與國際賽指南），並增設標準 H1 標題與導覽。
    - `tracks/lab/setup/` 單檔案碎片化問題：將 `cylab_classroom_setup_guide.md` 移入 `tracks/lab/90_runs/`，刪除冗餘目錄。
    - 修復全庫所有相對路徑斷鏈，達成全庫 Markdown 內部超連結 0 broken links 與 107 篇 Playbooks 100% 綠燈通過。
    - **自動化腳本收納**：將 `ctfd/sync_challenges.py` 移入 `ctfd/automation/`，消除 `ctfd/` 根目錄雜散腳本。
    - **社團專軌層級扁平化**：將 `ctf_competition_roadmap.md` 提升至 `tracks/club/` 根目錄，刪除僅容納單一檔案的 `competitions/` 冗餘目錄。
    - **內部離線教材與題庫規範化標註**：全面將各學習路徑與解析手冊（`full_learning_path.md`、`cyber_range_blue_team_roadmap.md`、`exam_analysis_manual.md`、`30days_sprint_roadmap.md`）中的本機目錄引用標記為 `[內部離線教材]` / `[內部離線題庫]`，並統一超連結至 `tracks/lab/90_runs/sources_index.md`，消除外部閱讀者對工作區不存在目錄的混淆。
    - **挑戰題庫同步引擎修復 (P0)**：修復 `security/practice/challenges/sync/` 內 12 份 Python 檔案的舊模組路徑，改採相對導入（`from ..base import ...`），並修正 `base.py` 輸出目錄至 `security/practice/challenges/platforms/`，`python -m security.practice.challenges.sync.main --list` 恢復 100% 正常。
    - **CI/CD 門禁路徑更新 (P1)**：修正 `.github/workflows/validate-playbooks.yml` 的 `paths:` 觸發條件為 `security/knowledge/blue_team/**`，保障 PR/push 正常執行手冊合規校驗。
    - **代碼品質排除規則對齊 (P2)**：同步 `.sonarcloud.properties` 排除路徑至最新架構，避免 SonarCloud 自動掃描靶場故意漏洞造成誤報。
    - **文檔全景樹補齊 (P3)**：更新 `tracks/lab/README.md`、`security/knowledge/blue_team/README.md` 與專案根目錄 `README.md`，收錄 `sources_index.md`、`event_guide.md` 等重要資產。
    - **實踐中心導覽樞紐補齊**：建立 `security/practice/README.md`，統整 8 大線上攻防平台實戰題庫與全真模擬評量題本，並同步更新 `security/README.md` 索引入口。
    - **PR-Agent CI 忽略規則對齊**：更新 `.github/workflows/pr_agent.yml` 與 `.pr_agent.toml`，排除 `security/practice/exams/evidence/**`、`tracks/lab/**/datasets/**` 與練習題庫，避免大型二進制封包耗損 AI Review 配額。
    - **DeepSource 幽靈排除項清理**：從 `.deepsource.toml` 移除已廢棄之舊版 `study/**` 排除項，維持靜態分析設定與現行倉庫一致。
    - **Agent 治理規範對齊專軌架構**：更新 `AGENTS.md` 與 `.agent/rules.md` 中的課程模組化描述，全面對齊 `tracks/` 體系（`tracks/lab/`, `tracks/club/`, `tracks/courses/`）。
    - **課表內容截斷與 Markdown 反引號修復**：修正 `tracks/lab/90_runs/cylab_classroom_setup_guide.md` 中 Run 3 Day 5 與 Day 6 的語法截斷與命令符未閉合問題，還原完整 Lab 連結與帶練指引。
    - **根目錄 CTFd 自動化能力標註對齊**：更新 `README.md` 中的架構圖與 ASCII 樹，完整呈現 `ctfd/automation/` 包含之題目同步與結算雙重能力。
    - **CI/CD 門禁規範全面對齊新架構**：更新 `.github/workflows/policy.yml` 允許 commit scopes 包含 `practice`, `tools`, `knowledge`, `memory`, `deepsource`, `links`，並恪守標準 72 字元上限，使全分支所有原子提交 100% 符合 Conventional Commits 與 PR Policy 檢查標準。
    - **驗證工具升級為全庫超連結守門員**：重構 `security/tools/validate_playbooks.py`，將斷鏈檢查從原本僅限藍隊手冊，擴展至全專案 235 份 Markdown 文檔（嚴格遵守不變更 `red_team` 之防護邊界），並擴充 `.github/workflows/validate-playbooks.yml` 監聽路徑至所有專軌與文檔，實現全專案跨模組斷鏈即時自動化攔截。
    - **專案全庫 Git 排除規則與部署腳本對齊**：在 `.gitignore` 補齊 OS 桌面中繼資料（`.DS_Store`、`Thumbs.db` 等）與 Zig 編譯快取（`.zig-cache/`、`zig-out/`），並同步更新 `ctfd/install.sh` 提示訊息，完整涵蓋 `sync_challenges.py` 與 `send_final_top10.py` 雙重維運能力。
    - **全庫 Shell 腳本執行權限與專軌導覽補齊**：使用 `git update-index --chmod=+x` 為全庫 4 份 `.sh` 腳本標記標準 POSIX 執行位元（`100755`），並在 `tracks/README.md` 補齊 HITCON 2026 Wargame 實戰案例庫索引，全專案 235 份 Markdown 超連結 100% 暢通。
    - **安全審計器暫態 IO 競爭防護**：強化 `security/tools/code_auditor/core/scanner_utils.py` 之 `read_php_file`，在檔案讀取時兼捕 `(PermissionError, OSError)` 暫態檔案鎖，並增至 5 次指數退避重試，徹底消除 Windows/CI 環境下快速單元測試的偶發 IO 競爭，15/15 測試穩定通過。
  - **嚴格原子化提交**：全流程無任何 `git add .` 或 `git add -A`，全部採顯式檔案暫存，提交歷史極度乾淨且每步可獨立 Revert。