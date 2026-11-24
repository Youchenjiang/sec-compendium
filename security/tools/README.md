# 🛠️ 資安作戰與自動化工具庫 (Security Tools)

本目錄收錄專案通用之資安作戰工具、白箱原始碼審計引擎與自動化品質檢驗腳本。

---

## 🧰 工具清單

### 1. [Code Auditor](code_auditor/README.md) (自動化白箱原始碼審計與 PoC 驗證引擎)
- **路徑**：`security/tools/code_auditor/`
- **定位**：全功能 PHP / 開源供應鏈安全審計與動態驗證引擎。
- **能力**：
  - 🔍 **SAST 靜態分析**：AST 語法樹追蹤與 38 條核心危險 Sink 偵測（RCE, SQLi, SSTI, Unserialize, 任意讀寫）。
  - ⚡ **PoC 產生器**：自動根據 Sinks 與資料流合成漏洞利用代碼。
  - 🐳 **Docker 沙箱驗證**：在乾淨的隔離容器中即時動態驗證 Exploit 是否有效。
  - 🔌 **模組化平台介面**：支援本機離線審計與 CTF/Wargame 遠端競賽自動化。
  - 📐 **方法論指導**：👉 [全方位安全審計與攻防方法論 (audit_methodology.md)](code_auditor/audit_methodology.md)

### 2. [Unified Playbook Validator](validate_playbooks.py) (攻防手冊雙軌全能檢驗工具)
- **路徑**：`security/tools/validate_playbooks.py`
- **定位**：一鍵整合執行藍隊 (107 篇) 與紅隊 (110 篇) 實戰手冊規範稽核，並對全專案所有 Markdown 文檔執行跨模組超連結防護稽核。
- **參數支援**：`--all` (預設), `--blue`, `--red`, `--links-only`。

### 3. [Blue Team Playbook Validator](validate_blue_team_playbooks.py) (藍隊原子實戰手冊檢驗工具)
- **路徑**：`security/tools/validate_blue_team_playbooks.py`
- **定位**：自動化檢查 `blue_team/playbooks` 107 篇實戰手冊之七大黃金規格關鍵字（案發現場破題、第一動~第五動、靶場實戰、過關驗收）、行數門檻 (>=200 行) 與藍隊內部連結。

### 4. [Red Team Playbook Validator](validate_red_team_playbooks.py) (紅隊特戰手冊檢驗工具)
- **路徑**：`security/tools/validate_red_team_playbooks.py`
- **定位**：自動化檢查 `red_team/playbooks` 110 篇特戰手冊之五動戰術結構、速查規範篇幅 (150~210 行) 與紅隊內部連結。

### 5. [Commit Policy & Atomic Linter](lint_commits.py) (提交規範與四權分立稽核工具)
- **路徑**：`security/tools/lint_commits.py`
- **定位**：本機端 Conventional Commits 與「四權分立（目的/功能/脈絡/治理）」原子化稽核工具，對齊 CI 政策守門標準。
### 6. [PR Helper & Validator](pr_helper.py) (PR 自動生成、結構驗證與安全提交工具)
- **路徑**：`security/tools/pr_helper.py`
- **定位**：自動解析 Conventional Commits 產出合規 PR 說明文檔，本機端先跑完 CI 守門員再使用 `--body-file` 提交，徹底避免 Windows PowerShell 跳脫截斷與標籤時間差紅燈。
- **子命令**：
  - `generate`：自動分析分支 Commit 產出符合 `.github/pull_request_template.md` 規範之 PR Markdown。
  - `lint`：校驗 PR Body 三大章節、標題長度與 Conventional Commits。
  - `create`：本地全套驗證通過後，一鍵建立帶有標籤之 GitHub Pull Request。

### 7. [PR Review Tool](pr_tool.py) (PR 審查、診斷與最終驗收工具)
- **路徑**：`security/tools/pr_tool.py`（搭配 `pr_audit.py`、`pr_verification.py`、`pr_reports.py`、`sonar_audit.py`、`gh_guard.py`、`process_guard.py`）
- **來源**：移植自 Clickra 倉庫的 `scripts/pr_tool.py`（Apache-2.0）；只保留審查與驗收功能。建立 PR 與 PR 說明檢查仍用 `pr_helper.py`，推送仍由人明確核准後手動執行。
- **原則**：除了 `resolve` 以外全部唯讀；`resolve` 一次只處理一個 thread，預設只預覽，需 `--execute --authorize <PR>:<thread>`；絕不發表或修改留言；不為了讓 PR 變綠而關掉還沒修好的問題。
- **子命令**：
  - `status` / `review`：PR 狀態、CI 彙總與所有未解決 review thread（DeepSource 留言只顯示標題）。
  - `audit [--json] [--sonar]`：逐頁讀取 inline 留言、一般留言與 review 摘要，不改變任何審查狀態。
  - `sonar [--json]`：列出 SonarCloud 該 PR 的 open/confirmed issues 與 quality gate。
  - `diagnose [--reports failed|all]`：讀取失敗 check 的 log、GitHub Check Run 摘要與 DeepSource 行內發現。
  - `verify`：唯讀最終驗收；確認 PR HEAD 等於遠端分支 SHA，盤點 review threads、SonarCloud issues 與必要 CI checks，任一未通過即回傳非 0。
  - `body --output <新檔>`：把既有 PR 說明匯出成新檔（不覆寫既有檔案）。
  - `resolve <PR> --thread <PRRT_...>`：預覽或在明確授權下解決單一已驗證修好的 thread。
- **SonarCloud 專案**：依序取 `SONAR_PROJECT_KEY`、`sonar-project.properties` 的 `sonar.projectKey`、`owner_repo`；私有專案設 `SONAR_TOKEN`。
- **必要 checks**（`pr_verification.REQUIRED`）：PR and commit policy、Documentation & Playbooks Quality Audit、TruffleHog Secrets Scan、DeepSource: Secrets、SonarCloud、SonarCloud Code Analysis；有 `.py` 變更時另需 DeepSource: Python。缺少或被略過的必要 check 一律視為未通過。

---

## 🚀 常用指令速查

```bash
# 1. 執行雙軌實戰手冊全能自動化品質稽核 (預設執行藍隊、紅隊與全專案超連結防護)
python security/tools/validate_playbooks.py

# 2. 單獨執行藍隊實戰手冊品質稽核
python security/tools/validate_blue_team_playbooks.py
# 或
python security/tools/validate_playbooks.py --blue

# 3. 單獨執行紅隊特戰手冊品質稽核
python security/tools/validate_red_team_playbooks.py
# 或
python security/tools/validate_playbooks.py --red

# 4. 僅執行全專案 Markdown 跨模組超連結稽核
python security/tools/validate_playbooks.py --links-only

# 5. 執行本地白箱代碼審計 (純靜態掃描)
python -m security.tools.code_auditor.main --local-dir /path/to/target --scan-only

# 6. 執行本地審計並生成 Exploit
python -m security.tools.code_auditor.main --local-dir /path/to/target

# 7. 執行本地 Commit 規範與四權分立稽核
python security/tools/lint_commits.py --base origin/main

# 8. 自動產出當前分支之合規 PR 說明檔 (避免 PowerShell 跳脫字元問題)
python security/tools/pr_helper.py generate --base origin/main -o PR_BODY.md

# 9. 本地全套驗證並一鍵安全提交 PR (附帶必備標籤)
python security/tools/pr_helper.py create --title "feat(tools): add pr helper and validator" --label "documentation"

# 10. 查看 PR 未解決的 review threads 與失敗 check 的原因 (唯讀)
python security/tools/pr_tool.py review 38
python security/tools/pr_tool.py diagnose 38

# 11. 合併前的唯讀最終驗收 (未通過時回傳非 0，並列出原因)
python security/tools/pr_tool.py verify 38

# 12. 預覽、再於明確授權後解決一個已驗證修好的 review thread (不留言)
python security/tools/pr_tool.py resolve 38 --thread PRRT_xxx
python security/tools/pr_tool.py resolve 38 --thread PRRT_xxx --execute --authorize 38:PRRT_xxx
```
