# semgrep (MCP via `semgrep mcp`)

**現行**的 Semgrep MCP 伺服器。它不再是獨立的 `semgrep-mcp` 套件，而是**內建於 `semgrep` 二進位**、以 `semgrep mcp` 子命令啟動。本條目取代已棄用的 `semgrep-mcp`（見 `retired/semgrep-mcp.md`）。

- **用途**：把 Semgrep 掃描（OSS 引擎）以 MCP 工具暴露給 agent，供 code-security 分析使用。
- **狀態**：`wired`（活體客戶端 session 已驗證並真的呼叫到工具，見 `semgrep.verification.md`）。

---

## 1. 來源與釘版

| 項目 | 值 |
|------|-----|
| 來源 | PyPI `semgrep==1.178.0`（伺服器程式碼內建於此套件，`semgrep/mcp/server.py`） |
| 上游 | `https://github.com/semgrep/semgrep` |
| 發行版本 | `semgrep==1.178.0` |
| 授權 | LGPL-2.1（`semgrep` 套件；OSS 引擎） |

> **與舊 `semgrep-mcp` 的引入差異**：舊的是獨立套件（外部快照 + submodule 釘版）；新的**就是 semgrep 本身**，因此引入方式 = 「釘 PyPI 版本 `semgrep==1.178.0`」，無 submodule、無外部快照。

## 2. 節點持有與執行環境

| 項目 | 值 |
|------|-----|
| holder node | Primary Analysis Gateway（宿主 `LabStrix`） |
| `requires_python` | `>=3.10`；`semgrep==1.178.0` **有 `cp314` wheel**，故**可用宿主預設 Python 3.14.7 原生執行** |
| 實測執行環境 | 專屬 venv `.agent/mcp/.verify/semgrep178`（宿主 Python 3.14.7，gitignored） |
| entrypoint | `semgrep mcp`（`semgrep.exe mcp`） |
| 傳輸 | `stdio`（另有 `streamable-http`） |
| 替代節點 | Kali / FLARE-VM（任何 `semgrep==1.178.0` 可裝的節點） |

> 相較於舊 `semgrep-mcp`（需 Python <3.12），本條目**回到宿主原生執行**，不再需要特製 3.11 環境。

## 3. 安裝（可重現）

```bash
cd hitcon-range-sprint
python -m venv .agent/mcp/.verify/semgrep178
PY=.agent/mcp/.verify/semgrep178/Scripts/python.exe
"$PY" -m pip install --upgrade pip
"$PY" -m pip install "semgrep==1.178.0" "mcp>=1.12"
```

## 4. 啟動

```bash
ENV=.agent/mcp/.verify/semgrep178
PATH="$PWD/$ENV/Scripts:$PATH" "$ENV/Scripts/semgrep.exe" mcp -t stdio
```

## 5. MCP 客戶端設定片段

```json
{
  "mcpServers": {
    "semgrep": {
      "command": "<repo>/.agent/mcp/.verify/semgrep178/Scripts/semgrep.exe",
      "args": ["mcp", "-t", "stdio"],
      "env": { "PATH": "<repo>/.agent/mcp/.verify/semgrep178/Scripts;%PATH%" }
    }
  }
}
```

金鑰：OSS 本地掃描**不需要** token；`semgrep_findings`（平台查詢）與 remote/Pro 功能需要 `SEMGREP_APP_TOKEN`，以 env 注入、**不入版控**。

## 6. 工具面（實測 `tools/list` 共 7 個）

`semgrep_rule_schema`、`get_supported_languages`、`semgrep_findings`、`semgrep_scan_with_custom_rule`、`semgrep_scan`、`get_abstract_syntax_tree`、`semgrep_scan_supply_chain`。

## 7. 避坑（實測）

1. **`semgrep_scan` 用 `auto` config，與 metrics-off 互斥**：`SEMGREP_SEND_METRICS=off` 時 `semgrep_scan` 會回 `Cannot run scan with auto config when metrics are off`。要離線／關 metrics 就用 `semgrep_scan_with_custom_rule`（自帶規則、無需 registry 下載）。
2. **`code_files.path` 必須是「該 OS 的絕對路徑」**：Windows 上要 `C:/...`，Git Bash 的 `/c/...` 會被判為非絕對路徑而報 `must be a absolute path`。
3. **`python -m semgrep` 已棄用**：請直接用 `semgrep` 執行檔。
4. **首次 `semgrep_scan`（auto）會連網下載 registry 規則**；`semgrep_scan_with_custom_rule` 則完全離線。

## 8. 相關

- 活體驗證：`servers/semgrep.verification.md`
- 探針工具：`tools/mcp_probe.py`
- 已退役前身：`retired/semgrep-mcp.md`
