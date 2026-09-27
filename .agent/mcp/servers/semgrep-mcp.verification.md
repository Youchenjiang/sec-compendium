# semgrep-mcp — 可跑驗證證據

> 本檔為**實跑**證據，非推測。所有輸出皆取自實際指令；握手結果重跑兩次一致（`EXIT 0`）。

對應條目：`registry.json` → `servers[0]`（`semgrep-mcp`）。
操作手冊：`servers/semgrep-mcp.md`。

---

## 0. 環境（實測當下）

```
$ python --version
Python 3.14.7                       # 宿主預設直譯器（不支援本伺服器）
$ conda --version
conda 26.7.1
$ docker info
docker daemon: DOWN                 # CLI 29.7.2 存在，但引擎未啟動 → 容器路徑本次不可用
```

專屬執行環境（repo 內、gitignored）：

```
$ .agent/mcp/.verify/venv311/python.exe --version
Python 3.11.16

$ .agent/mcp/.verify/venv311/python.exe -m pip freeze | grep -iE "semgrep|^mcp|setuptools"
mcp==1.12.2
semgrep==1.135.0
semgrep-mcp @ file:///C:/Users/LabStrix/Documents/GitHub/Youchen/Security-LabData/external-mcp-tools/semgrep-mcp
setuptools==80.10.2
```

`semgrep` CLI 可執行：

```
$ .agent/mcp/.verify/venv311/Scripts/semgrep.exe --version
1.135.0
```

## 1. 為何宿主 3.14 裝不起來（wheel 天花板）

查 PyPI 發行檔（`semgrep==1.135.0`，即本伺服器釘死的版本）：

```
=== semgrep==1.135.0 (6 files) ===
  py tags: ['cp39.cp310.cp311.py39.py310.py311']
    semgrep-1.135.0-cp39.cp310.cp311.py39.py310.py311-none-win_amd64.whl
    ...
    semgrep-1.135.0.tar.gz
```

→ **只有 cp39 / cp310 / cp311 wheel，沒有 3.12/3.13/3.14**。宿主 3.14.7 上 pip 只能退回 sdist（需 OCaml 建置）→ 裝不起來。故以 Python 3.11.16 承載。

（對照：最新 `semgrep==1.178.0` 已提供 `cp310…cp314` wheel，含 `win_amd64`——這是後續改用 `semgrep mcp` 可回到宿主 3.14 的依據。）

## 2. 安裝（自外部快照）

首次直接安裝快照會**因未初始化的 submodule 而壞掉**：

```
ModuleNotFoundError: No module named 'semgrep_mcp.semgrep_interfaces'
```

補齊 submodule 後重裝成功：

```
$ cd Security-LabData/external-mcp-tools/semgrep-mcp
$ git submodule update --init --depth 1 src/semgrep_mcp/semgrep_interfaces
Submodule path 'src/semgrep_mcp/semgrep_interfaces': checked out '3ce3539b8d9e46b98cf73d08f0b44ef63c3e80a0'

$ <venv>/python.exe -m pip install "setuptools<81"          # 讓 pkg_resources 存在
$ <venv>/python.exe -m pip install --force-reinstall --no-deps "…/semgrep-mcp"
Successfully installed semgrep-mcp-0.9.0
```

## 3. MCP 握手（initialize → tools/list）

以 stdio 傳輸，將下列 JSON-RPC 依序寫入伺服器 stdin：

```
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"freebuff-probe","version":"0.1"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

啟動命令（等價）：

```
PATH="<repo>/.agent/mcp/.verify/venv311/Scripts:$PATH" \
  <venv>/Scripts/semgrep-mcp.exe -t stdio
```

### 原始輸出（stdout）

```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-06-18","capabilities":{"experimental":{},"prompts":{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":false}},"serverInfo":{"name":"Semgrep","version":"1.12.2"}}}
{"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"deprecation_notice","description":"\n    Deprecation notice for the `mcp.semgrep.ai` and `uvx semgrep-mcp` MCP servers.\n\n    You should invoke this tool whenever you would use any of the pre-existing\n    Semgrep MCP tools! This includes:\n    - `semgrep_rule_schema`\n    - `get_supported_languages`\n    - `semgrep_findings`\n    - `semgrep_scan_with_custom_rule`\n    - `semgrep_scan`\n    - `semgrep_scan_remote`\n    - `get_abstract_syntax_tree`\n    ","inputSchema":{"properties":{},"title":"deprecation_noticeArguments","type":"object"},"outputSchema":{"properties":{"result":{"title":"Result","type":"string"}},"required":["result"],"title":"deprecation_noticeOutput","type":"object"}}]}}
```

### 相關 stderr

```
INFO:root:Starting Semgrep MCP server v0.9.0, Semgrep version v1.135.0
INFO:root:Tracing initialized
WARNING:root:User doesn't have the Pro Engine installed, not running `semgrep mcp` daemon...
INFO:mcp.server.lowlevel.server:Processing request of type ListToolsRequest
```

### 解析結果

| 項目 | 值 |
|------|-----|
| 進程退出碼 | `0` |
| `initialize.serverInfo` | `{"name":"Semgrep","version":"1.12.2"}` |
| 協商 protocol | `2025-06-18` |
| capabilities | `experimental`, `prompts`, `resources`, `tools` |
| `tools/list` 工具數 | **1** |
| 工具名稱 | `["deprecation_notice"]` |

## 4. 結論

- **成功**：`semgrep-mcp` 0.9.0 在專屬 Python 3.11.16 環境可安裝、可啟動、可完成 `initialize` + `tools/list` 握手（退出碼 0，兩次一致）。
- **限制（已記錄為結論，非失敗宣稱）**：宿主預設 3.14.7 **不能**承載本伺服器（wheel 天花板）；需釘 3.11 環境。若改用容器（本次 Docker 引擎未啟動）或改用新版 `semgrep mcp`（有 cp314 wheel）則不受此限。
- **功能面警示**：`tools/list` 僅回 `deprecation_notice`——上游已棄用本套件，代理價值有限，遷移目標為 `semgrep mcp`（見 `servers/semgrep-mcp.md` 第 7 節）。
