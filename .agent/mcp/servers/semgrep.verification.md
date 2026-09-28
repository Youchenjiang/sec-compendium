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

---

## 7. sample 目標掃描（可重現 fixture，2026-09-28）

前幾節掃的是真實 repo 檔案（乾淨結果，或單一規則）。本節改用**固定 fixture**，證明 MCP 掃描路徑能一次回傳多條 findings，且重跑逐筆一致。

### 7.1 fixture（不進版控；以下原文可一秒重建）

置於 Git-ignored 的 `.agent/mcp/.verify/sample-target/`。刻意不入庫：內容是刻意弱點與假憑證常數，入庫只會干擾 secret／SAST 掃描與閱讀。

`sample-target/vulnerable.py`：

```python
"""Deliberately vulnerable sample used as an MCP scan target.

This file is a throwaway fixture in the Git-ignored .verify/ scratch area; it
is never imported, executed, or committed. It exists only so the semgrep MCP
server has a small, known target with deterministic findings.
"""

import hashlib
import os
import sqlite3
import subprocess

API_TOKEN = "hardcoded-sample-token-0000"
PASSWORD = "SampleP@ssw0rd!"


def weak_hash(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def run(cmd: str) -> None:
    subprocess.run(cmd, shell=True, check=False)


def lookup(user_input: str) -> None:
    conn = sqlite3.connect("sample.db")
    conn.execute(f"SELECT * FROM users WHERE name = '{user_input}'")


def evaluate(expr: str):
    return eval(expr)


def read(path: str) -> str:
    with open(os.path.join("/tmp", path)) as handle:
        return handle.read()
```

`sample-target/sample-rules.yaml`：

```yaml
rules:
  - id: sample-python-hardcoded-secret
    languages: [python]
    severity: WARNING
    message: Hardcoded credential-like constant in source
    patterns:
      - pattern-regex: (?i)(password|passwd|token|api_key|secret)\s*=\s*"[^"]{8,}"

  - id: sample-python-md5
    languages: [python]
    severity: WARNING
    message: MD5 used as a hash function
    patterns:
      - pattern: hashlib.md5(...)

  - id: sample-python-shell-true
    languages: [python]
    severity: ERROR
    message: subprocess invoked with shell=True
    patterns:
      - pattern: subprocess.$FUNC(..., shell=True, ...)

  - id: sample-python-eval
    languages: [python]
    severity: ERROR
    message: eval() called on a value
    patterns:
      - pattern: eval(...)

  - id: sample-python-fstring-sql
    languages: [python]
    severity: ERROR
    message: SQL statement built with an f-string
    patterns:
      - pattern: $CONN.execute(f"...")
```

### 7.2 呼叫（活體 MCP session）

```text
<venv>/python.exe .agent/mcp/tools/mcp_probe.py \
  --cmd <repo>/.agent/mcp/.verify/semgrep178/Scripts/semgrep.exe \
  --arg mcp --arg=-t --arg stdio \
  --path-prepend .agent/mcp/.verify/semgrep178/Scripts \
  --metrics-off \
  --call semgrep_scan_with_custom_rule \
  --arguments "$(cat .agent/mcp/.verify/sample-scan-args.json)" \
  --out .agent/mcp/.verify/semgrep_scan_1178_sample.txt
```

`arguments` 形狀：`{"code_files": [{"path": "sample-target/vulnerable.py", "content": "<fixture 全文>"}], "rule": "<規則 YAML 全文>"}`。
選 custom rule 而非 `auto`：`SEMGREP_SEND_METRICS=off` 與 auto config 互斥（第 6 節已記錄），且 custom rule 為離線決定性。

### 7.3 結果（伺服器自報 `semgrep version 1.178.0`，`isError: false`）

| # | check_id | 位置 | 嚴重度 | 對應 fixture 內容 |
|---|----------|------|--------|------------------|
| 1 | `sample-python-hardcoded-secret` | `vulnerable.py` L13 | WARNING | `API_TOKEN = "hardcoded-sample-token-0000"` |
| 2 | `sample-python-hardcoded-secret` | `vulnerable.py` L14 | WARNING | `PASSWORD = "SampleP@ssw0rd!"` |
| 3 | `sample-python-md5` | `vulnerable.py` L18 | WARNING | `hashlib.md5(data).hexdigest()` |
| 4 | `sample-python-shell-true` | `vulnerable.py` L22 | ERROR | `subprocess.run(cmd, shell=True, ...)` |
| 5 | `sample-python-fstring-sql` | `vulnerable.py` L27 | ERROR | `conn.execute(f"SELECT ...")` |
| 6 | `sample-python-eval` | `vulnerable.py` L31 | ERROR | `eval(expr)` |

→ 5 條規則全數命中（`hardcoded-secret` 命中 2 處），fixture 植入的 6 個弱點 **6/6** 被回報，路徑為該工具接收的 `sample-target/vulnerable.py`。

### 7.4 重跑一致性

同一命令第二次執行，輸出至 `semgrep_scan_1178_sample_run2.txt`，以 `(check_id, path, line, severity)` 逐筆比對：**rerun identical = True**（6/6 相同，無行號或順序漂移）。

### 7.5 負面對照（同日）

- **舊線不可用**：`semgrep==1.135.0`（OSS）在同世代的 `semgrep mcp` 拒絕啟動——`[ERROR]: MCP subcommand requires Pro Engine--make sure you are using the proprietary semgrep binary.`（客戶端 `McpError: Connection closed`）。故 3.14 上的掃描供應者只有 1.178.0 這條線。
- **被棄用的 `semgrep-mcp` 0.9.0** 只有墓碑工具，無法提供掃描；其 3.14 再驗見 `servers/retired/semgrep-mcp.verification.md` 第 5 節。
