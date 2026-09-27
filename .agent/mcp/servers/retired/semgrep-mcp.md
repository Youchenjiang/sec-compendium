> **RETIRED (2026-09-27)** — 本伺服器已被上游棄用（`tools/list` 只回 `deprecation_notice`），已由 `servers/semgrep.md`（`semgrep mcp`）取代並自 `registry.json` 的 `servers[]` 移除。此檔保留為歷史與決策紀錄。

# semgrep-mcp

第一個接入 `.agent/mcp` 的伺服器。選它當第一顆，是因為它**自足**：entrypoint `semgrep_mcp.server:main`、pip 相依內含 `semgrep==1.135.0`，不需要外部工具鏈（不像 Ghidra/Volatility/Velociraptor 那些要先備好宿主工具或金鑰）。

- **用途**：把 Semgrep（OSS 靜態掃描）以 MCP 工具暴露給 agent，供 code-security 分析使用。
- **狀態**：`wired`（握手已驗證，見 `semgrep-mcp.verification.md`）。

---

## 1. 來源與釘版

| 項目 | 值 |
|------|-----|
| 外部快照 | `Security-LabData/external-mcp-tools/semgrep-mcp` |
| 上游 | `https://github.com/semgrep/mcp` |
| 上游 commit | `cade782501e611373844696edc2ceef31eb7e1f7` |
| 發行版本 | `semgrep-mcp==0.9.0` |
| submodule | `src/semgrep_mcp/semgrep_interfaces` @ `3ce3539b8d9e46b98cf73d08f0b44ef63c3e80a0`（`https://github.com/semgrep/semgrep-interfaces.git`） |
| 授權 | MIT |

**引入方式 = 引用外部快照，不 vendored。** 快照本身是一個 git checkout，可釘 commit；其 submodule **未被 vendored**，因此必須一併釘住其 commit。

## 2. 節點持有與執行環境

| 項目 | 值 |
|------|-----|
| holder node | Primary Analysis Gateway（宿主 `LabStrix`） |
| `requires_python` | `>=3.9,<3.12`（因 `semgrep==1.135.0` 的 wheel 只有 `cp39/cp310/cp311`，**無 3.12/3.13/3.14 wheel**） |
| 實測執行環境 | 專屬 Python **3.11.16** env（`.agent/mcp/.verify/venv311`，已 gitignore） |
| 傳輸 | `stdio` |
| 替代節點 | Kali / FLARE-VM（若其 Python 為 3.9–3.11），或官方容器 `ghcr.io/semgrep/mcp` |

> **宿主預設 Python 3.14.7 直接安裝會失敗**：`semgrep==1.135.0` 無 cp314 wheel，pip 只能退回 sdist 並嘗試 OCaml 建置。故本伺服器**不得用宿主預設直譯器硬跑**，必須以釘版本的 3.11 環境承載。

## 3. 安裝（可重現）

```bash
# 0) 在外部快照補齊未 vendored 的 submodule（否則 import 失敗）
cd Security-LabData/external-mcp-tools/semgrep-mcp
git submodule update --init --depth 1 src/semgrep_mcp/semgrep_interfaces

# 1) 建專屬 3.11 環境（於框架 repo 內、gitignore 的 .verify/ 下）
cd ../../../Security/hitcon-range-sprint
conda create -y -p .agent/mcp/.verify/venv311 python=3.11
PY=.agent/mcp/.verify/venv311/python.exe
"$PY" -m pip install --upgrade pip
"$PY" -m pip install "setuptools<81"          # 讓 pkg_resources 存在（見避坑 3）
"$PY" -m pip install "Security-LabData/external-mcp-tools/semgrep-mcp"
```

## 4. 啟動

```bash
ENV=.agent/mcp/.verify/venv311
PATH="$PWD/$ENV/Scripts:$PATH" "$ENV/Scripts/semgrep-mcp.exe" -t stdio
```

`stdio` 模式下看似「卡住不輸出」是正常的——它改走 stdin/stdout 的 JSON-RPC。伺服器需能從 `PATH` 找到 `semgrep`（見避坑 4）。

## 5. MCP 客戶端設定片段

```json
{
  "mcpServers": {
    "semgrep": {
      "command": "<repo>/.agent/mcp/.verify/venv311/Scripts/semgrep-mcp.exe",
      "args": ["-t", "stdio"],
      "env": {
        "PATH": "<repo>/.agent/mcp/.verify/venv311/Scripts;%PATH%",
        "SEMGREP_SEND_METRICS": "off"
      }
    }
  }
}
```

金鑰：OSS 本地掃描**不需要** token；只有 remote/Pro 功能才需要 `SEMGREP_APP_TOKEN`。若啟用，以環境變數注入，**不入版控**。

## 6. 避坑（實測踩到的）

1. **Python 版本**：`semgrep==1.135.0` 僅 `cp39/cp310/cp311`。宿主 3.14 不行，3.12/3.13 也不行。
2. **未初始化的 submodule**：快照的 `semgrep_interfaces` 為空 → `ModuleNotFoundError: No module named 'semgrep_mcp.semgrep_interfaces'`。需先 `git submodule update --init`。
3. **`pkg_resources` 被移除**：`opentelemetry-instrumentation` import `pkg_resources`；`setuptools>=81` 已移除它 → `semgrep` CLI 直接 traceback。需 `pip install "setuptools<81"`。
4. **`semgrep` 必須在 PATH**：伺服器 `ensure_semgrep_available()` 以 `PATH` 尋找 `semgrep`，否則 `initialize` 時丟 `McpError: Semgrep is not installed or not in your PATH`。啟動時把 `<venv>/Scripts` 前置到 `PATH`。

## 7. 工具面重大發現與後續遷移

實測 `tools/list` **只回一個工具 `deprecation_notice`**——因為 **上游已棄用 `semgrep-mcp` 0.9.0**，新的 MCP 伺服器改由 **`semgrep` 二進位的 `semgrep mcp` 子命令**提供（見 `deprecation_notice` 回傳內容）。

- 影響：本伺服器能跑、握手正常，但**功能面已被上游標為 deprecated**，代理價值有限。
- 遷移路徑：改用新版 `semgrep`（例如 `1.178.0`，**具 cp314 wheel**）提供的 `semgrep mcp`。此舉還有附帶好處——新版 semgrep 支援 Python 3.14，**可直接回到宿主預設直譯器**，不再需要 3.11 特製環境。
- 建議：把 `semgrep mcp`（新版）列為下一個要接的 MCP，並在 `registry.json` 以獨立條目登記；本 `semgrep-mcp` 條目保留為「已驗證但已棄用」的對照。
