# semgrep (MCP) — 活體客戶端 session 驗證證據

> 本檔為**活體**證據：由真正的 MCP 客戶端 session（`tools/mcp_probe.py`）連上 `semgrep mcp` 伺服器，**真的呼叫到工具並取回真實結果**。這比上一段的 `initialize`＋`tools/list` 握手更進一步——握手只證明連得上，這裡證明**叫得動、回得來**。

對應條目：`registry.json` → `servers[1]`（`semgrep`）。
操作手冊：`servers/semgrep.md`。

---

## 0. 環境

```
$ python --version                         # 宿主預設直譯器
Python 3.14.7

$ .agent/mcp/.verify/semgrep178/Scripts/python.exe --version
Python 3.14.7                              # 專屬 venv，宿主原生 3.14

$ .agent/mcp/.verify/semgrep178/Scripts/python.exe -m pip freeze | grep -iE "^(semgrep|semgrep-mcp|mcp)=="
mcp==1.29.0
semgrep==1.178.0                           # cp314 wheel → 宿主原生可跑

$ .agent/mcp/.verify/semgrep178/Scripts/semgrep.exe --version
1.178.0
```

伺服器啟動命令（客戶端以 stdio 拉起）：

```
semgrep.exe mcp -t stdio
```

客戶端探針命令（本檔所有呼叫皆由它產生）：

```
<venv>/python.exe .agent/mcp/tools/mcp_probe.py \
  --cmd <repo>/.agent/mcp/.verify/semgrep178/Scripts/semgrep.exe \
  --arg mcp --arg=-t --arg stdio \
  --path-prepend .agent/mcp/.verify/semgrep178/Scripts \
  [--metrics-off] --call <tool> --arguments '<json>'
```

## 1. initialize（session 建立）

```json
{
  "serverInfo": {"name": "Semgrep", "version": "1.29.0"},
  "protocolVersion": "2025-11-25",
  "capabilities": {"experimental": {}, "prompts": {"listChanged": false},
                   "resources": {"subscribe": false, "listChanged": false},
                   "tools": {"listChanged": false}}
}
```

## 2. tools/list（7 個工具）

```json
{
  "count": 7,
  "tools": [
    {"name": "semgrep_rule_schema"},
    {"name": "get_supported_languages"},
    {"name": "semgrep_findings"},
    {"name": "semgrep_scan_with_custom_rule"},
    {"name": "semgrep_scan"},
    {"name": "get_abstract_syntax_tree"},
    {"name": "semgrep_scan_supply_chain"}
  ]
}
```

（對照上一段：舊 `semgrep-mcp` 0.9.0 只回 1 個 `deprecation_notice`。）

## 3. 真呼叫 A — `get_supported_languages`

```json
// tools/call.request
{"name": "get_supported_languages", "arguments": {}}
// tools/call.result
{
  "isError": false,
  "structuredContent": {"result": ["supported languages are: apex, bash, c, c#, c++, ... , yaml"]}
}
```

真實回傳（節錄）：`apex, bash, c, c#, c++, ... python, ... powershell, ... yaml`。

## 4. 真呼叫 B — `semgrep_scan`（auto 規則，掃真實 repo 路徑）

對真實 repo 檔案 `security/tools/vmrun_guest.py` 以預設 `auto` config 掃描：

```json
// tools/call.request
{"name": "semgrep_scan",
 "arguments": {"code_files": [
   {"path": "C:/Users/LabStrix/Documents/GitHub/Youchen/Security/hitcon-range-sprint/security/tools/vmrun_guest.py"}]}}
// tools/call.result
{
  "isError": false,
  "structuredContent": {
    "version": "1.178.0",
    "results": [],
    "errors": [],
    "paths": {"scanned": ["vmrun_guest.py"]},
    "skipped_rules": [],
    "mcp_scan_results": {}
  }
}
```

→ 掃描**真的執行**（`paths.scanned` 有該檔），OSS 引擎回報 0 findings（乾淨結果，非錯誤）。

## 5. 真呼叫 C — `semgrep_scan_with_custom_rule`（自訂規則，真實 repo 檔案內容）

對真實 repo 檔案 `security/tools/collab_watch.py` 的內容，套用本機自訂規則（偵測 `subprocess.run(...)`）：

```json
// tools/call.request（content 為該檔原文，此處節錄）
{"name": "semgrep_scan_with_custom_rule",
 "arguments": {
   "code_files": [{"path": "security/tools/collab_watch.py", "content": "#!/usr/bin/env python3\n..."}],
   "rule": "rules:\n  - id: real-repo-subprocess-list\n    languages: [python]\n    severity: INFO\n    message: subprocess invocation detected in real repo file\n    patterns:\n      - pattern: subprocess.run(...)\n"
 }}
// tools/call.result（節錄，完整 4 findings）
{
  "isError": false,
  "structuredContent": {
    "version": "1.178.0",
    "results": [
      {"check_id": "real-repo-subprocess-list", "path": "security\\tools\\collab_watch.py",
       "start": {"line": 83, "col": 13}, "extra": {"severity": "INFO", "engine_kind": "OSS"}},
      {"check_id": "real-repo-subprocess-list", "path": "security\\tools\\collab_watch.py",
       "start": {"line": 85, "col": 13}, "extra": {"severity": "INFO", "engine_kind": "OSS"}},
      {"check_id": "real-repo-subprocess-list", "path": "security\\tools\\collab_watch.py",
       "start": {"line": 87, "col": 13}, "extra": {"severity": "INFO", "engine_kind": "OSS"}},
      {"check_id": "real-repo-subprocess-list", "path": "security\\tools\\collab_watch.py",
       "start": {"line": 153, "col": 21}, "extra": {"severity": "INFO", "engine_kind": "OSS"}}
    ]
  }
}
```

→ **真實結果**：4 個 findings，行號對應 `collab_watch.py` 真實的 `subprocess.run` 呼叫（第 83、85、87、153 行），引擎為 OSS。

## 6. 結論

| 檢查 | 結果 |
|------|------|
| 活體 session 建立 | ✅ `initialize` 回 `Semgrep/1.29.0`，protocol `2025-11-25` |
| 工具可列舉 | ✅ 7 個工具 |
| 真的呼叫工具並回真實結果 | ✅ `get_supported_languages`（語言清單）、`semgrep_scan`（掃真實路徑，0 findings）、`semgrep_scan_with_custom_rule`（真實 4 findings） |
| 宿主原生執行 | ✅ Python 3.14.7 直接可跑（`semgrep==1.178.0` 有 cp314 wheel） |
| 明確失敗原因（若遇到的） | `semgrep_scan` 於 `SEMGREP_SEND_METRICS=off` 時回 `Cannot run scan with auto config when metrics are off`；`/c/...` 形式路徑回 `code_files.path must be a absolute path`（皆已記入 `servers/semgrep.md` 避坑） |

本段證明了「這條線」：**現行 semgrep MCP 可被活體客戶端連上、列工具、並真的跑掃描取回真實結果**。
