# MCP 接線規範與註冊點 (`.agent/mcp`)

此目錄是 `hitcon-range-sprint` 框架的 **MCP（Model Context Protocol）註冊點**。它**不存放任何 MCP 伺服器原始碼**，只存放治理與註冊資料：

| 檔案 | 角色 |
|------|------|
| `README.md` | 這份接線規範（治理、掛載點、節點持有、金鑰） |
| `registry.json` | 機器可讀的伺服器註冊表，**單一真相來源** |
| `servers/<name>.md` | 單一伺服器的引入說明與操作手冊 |
| `servers/<name>.verification.md` | 可跑的驗證證據（原始輸出） |
| `tools/mcp_probe.py` | 活體 stdio MCP 客戶端探針（握手／列工具／呼叫工具） |
| `../../secrets.env.example` | 金鑰清單模板：只有**變數名稱**；複製成 Git-ignored 的 `secrets.env` 後才填值（第 9 節） |

掛載點刻意與 `.agent/skills/` 同層：技能是「知識面」，MCP 是「工具面」，兩者皆屬 agent 能力層，但以不同目錄區分意圖。

---

## 1. 掛載點與邊界

- MCP 一律註冊在 `.agent/mcp/`，與 `.agent/skills/` 同層。
- **伺服器原始碼不進本 repo（不 vendored）**：本 framework 的職責是協作與題庫治理，不是工具發行；把外部工具原始碼吞進來會讓 repo 膨脹且難以更新。
- 本目錄只描述「去哪裡取、釘在哪個版本、由誰跑、需要什麼」；實際程式碼留在外部快照。

## 2. 引入方式（import mode）

- **引用外部快照**：`Security-LabData/external-mcp-tools/<name>`。
- 每個伺服器在 `registry.json` 必須釘死三樣東西，缺一不可：
  1. 上游 git **commit**；
  2. 發行**版本**；
  3. 任何未被 vendored 的 **submodule commit**。
- 可重現的安裝／啟動步驟必須寫進 `servers/<name>.md`。

## 3. 節點持有（holder node）

- 決策：MCP 由 **Primary Analysis Gateway（宿主 `LabStrix`）** 持有——掃描、鑑識與本地算力集中在這台，agent 也在此進程內，`stdio` 子進程拉起最直接。
- **但宿主預設直譯器是 Python 3.14，不能硬跑所有 MCP**：多數 MCP 會釘死相依套件的舊版本（wheel 只服務特定 Python 版本）。因此規則是：
  - 每個伺服器在 `registry.json` 標明 `requires_python`；
  - 以**專屬且釘版本的執行環境**承載，不得用宿主預設直譯器硬跑；
  - 標明替代節點（Kali / FLARE-VM / container），供主節點無法滿足時分流。
- 「跑不起來」本身就是合法結論：若 wheel 不存在而無法安裝，**記錄失敗、指明應落在哪個節點**，不得宣稱成功。

## 4. 傳輸（transport）

- 預設 `stdio`：由 agent 進程直接拉起伺服器子進程，最單純、無網路面。
- `streamable-http` / `sse` 僅在需要跨節點共享一個長駐伺服器時使用；啟用時需另立網路與認證規範，不得預設開啟。
- **節點型傳輸**（`ssh`／`vmrun_guest`／`container`）由 `placement.holder_class` 推導，實作與規範見 §12。無論哪一種，MCP 客戶端看到的都還是 stdio：`ssh`、`docker -i`、vmrun 橋接器都只是把 stdin/stdout 轉進節點。

## 5. 金鑰與治理

- 金鑰一律由**環境變數**注入，**永不入版控**（`secrets.env` 已列於 `.gitignore`）。
- `registry.json` 只記錄「需要哪些 env 變數名稱」，**不記錄值**。
- 伺服器引入遵循原子化提交，固定拆成三顆：
  1. **接線／註冊**（規範、`registry.json` 骨架）——本顆為一次性治理底座；
  2. **單一伺服器引入**（`registry.json` 條目 + `servers/<name>.md`）；
  3. **可跑的驗證證據**（`servers/<name>.verification.md`）。
- 不碰既有 playbook、`.collab/`、其他未提交變更；只精準 `git add` 本次新增檔。

## 6. 新增下一個 MCP 的流程

1. 在 `servers/<name>.md` 記錄來源快照、釘死 commit/version/submodule、holder node 與 `requires_python`、操作手冊。
2. 在 `registry.json` 的 `servers[]` 增列對應條目。
3. 依 `servers/<name>.md` 實跑一次至少 `initialize` + `tools/list` 的 MCP 握手。
4. 把**原始輸出**存成 `servers/<name>.verification.md`，再依上述三顆原子化提交落地。

---

## 7. 由協作執行路徑自動呼叫（runner + collab bus）

註冊表不只是文件：`runner` 區塊把條目變成**可執行**的 stdio 伺服器，`collab` 層再把呼叫入口暴露給 agent。

### 7.1 `runner` schema（registry 條目的一部分）

```json
"runner": {
  "venv": ".agent/mcp/.verify/<env>",   // 釘版本的執行環境（repo 內、gitignored）
  "script": "<console-script>",           // venv Scripts/bin 下的可執行檔名
  "args": ["mcp", "-t", "stdio"],        // 啟動伺服器的 argv
  "env": { "KEY": "repo-relative/path" }  // 可選；值相對 repo root 解析
}
```

- **相依執行環境不可預設直譯器**：`runner.venv` 指向釘版本環境；缺環境即視為未 provisioning，由 bridge 明確回報並指到 `servers/<name>.md`。
- **只記環境變數名，不記值**（同第 5 節金鑰規則）。

### 7.2 協作呼叫入口（`collab_bus.py mcp`）

| 指令 | 行為 |
|------|------|
| `collab_bus.py mcp list` | 離線：列出已註冊伺服器、`requires_python`、runtime 是否就緒、retired 條目 |
| `collab_bus.py mcp tools --server <name>` | 活體 session：列出伺服器真的暴露的工具 |
| `collab_bus.py mcp call --server <name> --tool <tool> [--args JSON] [--json]` | 活體 session：呼叫單一工具並印出真實結果（失敗 exit 1） |

由 `security/tools/collab_mcp.py` 實作；session 在**伺服器自己的 venv** 裡以 `tools/mcp_probe.py` 執行（host 直譯器沒有 MCP SDK，伺服器有）。

### 7.3 逾時與錯誤

- 單一 session 預設上限 300s，逾時回報錯誤而非無限等待。
- 伺服器未 provisioning、registry 損壞、工具呼叫 `isError=true` 皆以 `ERROR ...` 印到 stderr，exit 2；工具本身的錯誤 exit 1。

---

> 目前狀態：`semgrep` 與 `cve-mcp-server` 已接入且可由 `collab_bus.py mcp ...` 自動呼叫；`semgrep-mcp` 已退役並移入 `retired[]`。

---

## 8. 節點擺放規範（node placement）

每一條 `servers[]` 條目以 `placement.holder_class` 指定**唯一承載節點**；沒有 `placement` 的伺服器不得進 `servers[]`（`mcp list` 會顯示該欄）。

### 8.1 四類節點

| `holder_class` | 節點 | 能力 | 限制 |
| :--- | :--- | :--- | :--- |
| `host_gateway` | Primary Analysis Gateway（宿主 `LabStrix`） | 64 GB RAM、大映像／記憶體 dump、repo 內檔案直讀、`secrets.env` 所在地 | 不得把 VM 當算力用；command-capable 服務須過 Authorization Gate（第 10 節） |
| `flare_vm` | FLARE-VM（Windows 10 x64，`192.168.12.129`，vmrun Guest Operations） | `C:\Tools\DFIR\`（EZTools／Chainsaw／Hayabusa／Sysmon）、Windows 工件原生解析 | 2 GB RAM；防火牆全擋外部 TCP；**不持有任何金鑰** |
| `kali` | Kali（`192.168.12.128`，免密 SSH） | Linux CLI、`tshark`／pcap、文書與巨集分析 | 2 GB RAM；系統時區 `America/New_York`（一律換算 UTC）；**不持有任何金鑰** |
| `container` | 一次性容器（`docker compose run --rm`） | 隔離的掃描／offensive 工具鏈 | 需明示網路與掛載範圍；不得掛載宿主家目錄 |

### 8.2 擺放決策（依序判斷，先命中先決定）

1. **資料重力**：標本 > 2 GB 或記憶體 dump → `host_gateway`（VM 會 OOM）。
2. **作業系統相依**：Windows 工件解析器 → `flare_vm`；Linux CLI／pcap／文書 → `kali`。
3. **爆炸半徑**：會執行指令或改寫狀態者，優先 `container` 或 `kali`；只有宿主才做得到時才留 `host_gateway`，且**必須有 allowlist 條目**。
4. **金鑰暴露面**：需要對外 API 金鑰者一律留 `host_gateway`（`secrets.env` 在宿主）；**不得把金鑰帶上 VM**。
5. **時間語意**：跨節點時間線一律換算 UTC；Kali 時區不是 UTC。

### 8.3 目前與已評估的擺放

| 伺服器 | `holder_class` | 理由 | fallback |
| :--- | :--- | :--- | :--- |
| `semgrep`（已接入） | `host_gateway` | 需 repo 內檔案直讀＋宿主原生 cp314 執行環境 | `container` |
| `cve-mcp-server`（已接入） | `host_gateway` | 對外情報 API＋金鑰在宿主 | `container` |
| `Volatility-MCP-Server`（未接） | `host_gateway` | 記憶體 dump 只有宿主吃得下（VM 2 GB 會 OOM） | — |
| `WireMCP`（未接） | `host_gateway` 或 `kali` | 宿主已裝 Wireshark 但 `tshark` 不在 PATH；Kali 現成 | `kali` |
| `velociraptor-mcp-server`（未接） | `host_gateway` | 需 JWT／採集服務，金鑰留宿主 | `kali` |
| `android-mcp`（未接） | `kali`／`flare_vm` | 需 apktool／jadx／adb／frida 等節點工具鏈 | `container` |
| `reverse-engineering-assistant`（未接） | `host_gateway` | 需 Ghidra（JDK 已具備）＋大樣本處理 | — |
| `mcp-security-hub`（未接） | `container` | offensive 掃描需網路隔離 | — |

> 未接項目的級別與前置需求見引入判定矩陣；本表只決定「接上後跑哪裡」。

---

## 9. 金鑰注入（`secrets.env`）

### 9.1 單一來源

- 唯一來源是 repo 根目錄的 `secrets.env`（`.gitignore` 已排除）。
- 版控內只放 `secrets.env.example`（**只有變數名稱**，值一律留空）；新進人員複製成 `secrets.env` 後自行填值。
- `registry.json` 永遠**只記變數名稱**，不記值。

### 9.2 檔案格式

```text
# 註解行以 # 開頭
NVD_API_KEY=abc123          # KEY=value，值不加引號也支援單／雙引號
VM_GP="guest-password"      # 值不展開 shell 變數（$ 保持字面）
```

容忍空白行、`#` 註解與 `export ` 前綴；鍵必須符合 `[A-Za-z_][A-Za-z0-9_]*`。

### 9.3 最小權限注入

1. 每個伺服器在 `secrets_binding.env` 宣告**自己有權取得的變數名稱**；`secrets_binding.required` 決定缺值是否中止。
2. Session 啟動時只把**該伺服器宣告**的名稱注入其子行程環境；`secrets.env` 中其他條目的金鑰不會外洩給它。
3. 取值順序：`secrets.env` → 既有 process 環境變數（同名）。runner 自身指向路徑的 `runner.env` 與金鑰無關。
4. `required: true` 而缺值時，session 直接以 `ERROR ... missing required secret env names ...`（exit 2）中止，不半殘啟動。
5. 稽核用 `collab_bus.py mcp secrets --server <name>`：只印名稱與 `present`／`missing`，**永不印值**。

### 9.4 節點與輪替

- 金鑰留在 `host_gateway`；`flare_vm`／`kali` 不持有任何 token——需要憑證的工作由宿主代跑後回傳文字工件。
- 輪替＝改 `secrets.env` 後重跑對應 session，不需要改 registry（名稱不變）。
- **禁止**：把值寫進 registry／證據檔／playbook、貼進命令列參數，或提交 `secrets.env`。
- 既有框架層變數（非 MCP）：`SECURITY_LAB_DATA_ROOT`、`KALI_HOST`／`KALI_USER`／`KALI_PASSWORD`、`VM_GP`／`VM_GU`、`VM_VMRUN`／`VM_VMX`／`VM_CREDS_FILE`；同樣只記名稱。

---

## 10. Authorization Gate：指令執行型 MCP 白名單

### 10.1 能力分級與預設拒絕

| `capability_class` | 意義 | 是否需白名單 |
| :--- | :--- | :---: |
| `read_only` | 只讀資訊，不改狀態 | 否 |
| `analysis` | 對我們給的檔案做解析／掃描，不改狀態 | 否 |
| `network` | 會連外部服務（金鑰走第 9 節） | 否 |
| `write` | 會改寫本地狀態 | **是** |
| `command_exec` | 會執行指令或驅動工具（nmap／nuclei／hashcat／Kali server／採集器） | **是** |
| （未宣告） | `unclassified`：無證據證明安全 | **是**（fail-closed） |

`registry.authorization.default_decision = "deny"`；白名單目前**刻意留空**，因此現行兩條已接入伺服器（`read_only`／`analysis`／`network`）不受影響，而任何 `command_exec`／`write`／未宣告的伺服器一律拒絕。

### 10.2 白名單條目（`authorization.command_exec_allowlist[]`）

| 欄位 | 必填 | 說明 |
| :--- | :---: | :--- |
| `server` | ✅ | 條目對應的伺服器名（與 `servers[].name` 一致） |
| `tools` | ✅ | 允許的工具名清單；`["*"]` 只在確實需要時使用，且必須搭配 `requires_authorization` |
| `paths_allow` | ✅ | 允許的**路徑根**（repo 相對或絕對）。任何看起來像路徑的參數都必須落在這些根之內；未宣告根＝一律拒絕 |
| `requires_authorization` | ✅ | `true` 時每次呼叫都要有明確事由＋授權變數 |
| `deny_patterns` | ⬜ | 正規表達式黑名單（如 `;\s*rm\b`、`\|\s*(sh|bash)\b`），任何參數命中即拒絕 |
| `expires` | ⬜ | `YYYY-MM-DD`；過期即拒絕（強迫定期複審） |
| `authorization_env` | ⬜ | 覆寫預設授權變數名（預設 `MCP_AUTHORIZATION`） |
| `note`／`reviewed_by` | ⬜ | 為何開這條、誰審的 |

### 10.3 判定流程與稽核

```text
[Authorization Gate] 🧭 server/tool/arguments
  ➔ 🚪 條目存在？ 無 → DENY（default_decision=deny）
  ➔ 🚪 capability 是否已具備？（未宣告視為 unclassified）→ 無需白名單 → ALLOW
  ➔ 🚪 tool 在 tools 內？ 否 → DENY
  ➔ 🚪 expires 未過期？ 否 → DENY
  ➔ 🚪 deny_patterns 未命中？ 命中 → DENY
  ➔ 🚪 路徑型參數在 paths_allow 內？ 否 → DENY
  ➔ 🚪 --authorized 事由非空？＋授權變數存在？ 否 → DENY
  ➔ ✅ ALLOW（並寫入稽核）
```

- 閘門在**拉起子行程之前**執行；被拒的呼叫不會 spawn 任何伺服器。
- 每次判定（含 dry-run）追加一行 JSON 到 `.collab/runtime/mcp-gate.jsonl`（Git-ignored）：`at`／`mode`／`server`／`tool`／`capabilities`／`decision`／`reason`／`authorized_reason`；**不含參數內容與金鑰值**。
- 與 `.agent/rules.md` 的 Authorization Gate 對齊：「外部變更需當回合明確授權」在工具面落地為 `--authorized "<事由>"` ＋ `MCP_AUTHORIZATION` 存在，且事由入稽核。

### 10.4 指令

| 指令 | 行為 |
| :--- | :--- |
| `collab_bus.py mcp gate --server <s> [--tool <t>] [--args JSON] [--authorized "<why>"]` | 離線試算判定，印出決策 JSON；allow exit 0／deny exit 2 |
| `collab_bus.py mcp call ... --authorized "<why>"` | 先過閘門再開 session；被拒時 `ERROR authorization gate denied ...`（exit 2） |
| `collab_bus.py mcp list` | 顯示每條的 `holder=` 與 `capabilities=`／`gated=` |
| `collab_bus.py mcp secrets --server <s>` | 顯示宣告的金鑰名稱與 present／missing（不顯示值） |

### 10.5 尚未開放的例子（C 級，不引入）

`mcp-security-hub`（nmap／nuclei／sqlmap／hashcat）與 `MCP-Kali-Server` 屬指令執行型。若要真的接，除了 §4 的網路與認證規範，還必須給出像下面這種**收斂的**條目——而不是一句「整台掃」：

```json
{
  "server": "mcp-security-hub",
  "tools": ["nmap_scan"],
  "paths_allow": ["tracks/lab/hitcon_range/", "security/"],
  "deny_patterns": ["\\.\\./", ";", "\\|", "&&"],
  "requires_authorization": true,
  "expires": "2026-12-31",
  "note": "僅限靶場網段掃描；每次呼叫需記錄事由",
  "reviewed_by": "primary-gateway-operator"
}
```

---

## 11. 實作現況與待辦

| 能力 | 狀態 |
| :--- | :--- |
| 擺放欄位（`placement`）與能力分級（`capability_class`） | ✅ 已進 registry，`mcp list` 顯示 |
| 金鑰最小權限注入（`secrets_binding`）＋`mcp secrets` 稽核 | ✅ 已實作於 `collab_mcp.py` |
| Authorization Gate（白名單／路徑範圍／黑名單／到期／事由）＋稽核日誌 | ✅ 已實作，`mcp gate`／`mcp call --authorized` |
| 節點型傳輸（`kali` SSH／`flare_vm` vmrun／`container` exec） | ✅ 已實作（§12）：三個傳輸都以活體 session 驗證過（container 真的在容器內、ssh 真的在 Kali 上、vmrun 真的經 Guest Operations 進到 VMware 客體） |
| `mcp launch`（離線檢視傳輸、argv、金鑰名稱） | ✅ 已實作，secret 值永不輸出 |
| `mcp doctor`（檢查 venv／pin／工具數與證據是否一致） | ⬜ 待做 |

> 尚未把任何**真實**伺服器擺到節點上：目前 registry 內兩個已接伺服器都是 `host_gateway`／`stdio_local`。傳輸本身已可跑，缺的是「有伺服器真的需要那個節點」——見 §8.3 的擺放表與引入判定矩陣。

---

## 12. 節點型傳輸（實作）

規範在 §8 決定「跑哪裡」，這裡決定「怎麼連上去」。實作：`security/tools/mcp_transports.py`（規劃）、`.agent/mcp/tools/mcp_node_bridge.py`（客體內側）、`.agent/mcp/tools/mcp_vmrun_bridge.py`（宿主側 vmrun 適配器）、`security/tools/collab_mcp.py`（接線）。

### 12.1 傳輸對照

| `holder_class` | transport | 實際拉起的子行程 | 節點需要什麼 |
| :--- | :--- | :--- | :--- |
| `host_gateway` | `stdio_local` | 伺服器自己的 venv 執行檔 | 該 venv |
| `kali` | `ssh` | `ssh`（`BatchMode=yes`） | 金鑰登入（或 `sshpass`）、客體上的伺服器 argv |
| `flare_vm` | `vmrun_guest` | 宿主 `mcp_vmrun_bridge.py` | VMware Tools；**不需要**客體開任何埠或 SSH |
| `container` | `container` | `docker run --rm -i` | 映像；預設 `--network none` |

- 傳輸由 `placement.holder_class` 推導；要偏離必須明寫 `runner.node.transport`。
- 節點型 session 的 MCP 客戶端（`mcp_probe.py`）跑在**宿主**的 probe 環境（`policy.node_transports.probe_env`，預設 `.agent/mcp/.verify/probe`，內容為 `pip install "mcp<2"`）；伺服器 venv 只在節點上存在，不能拿來跑客戶端。

### 12.2 `runner.node` schema

```jsonc
"runner": {
  "node": {
    "transport": "vmrun_guest",           // 可省略＝由 holder_class 推導
    "probe_env": ".agent/mcp/.verify/probe", // 可省略＝用 policy 預設
    "exec": {                              // 在節點上真正跑什麼
      "command": "python.exe", "args": ["C:/Tools/mcp/server.py"],
      "cwd": "C:/Tools/mcp", "env": {"MCP_MODE": "stdio"}, "path_prepend": null
    },
    "ssh":      {"host": {"secret": "KALI_HOST"}, "user": {"secret": "KALI_USER"},
                 "port": 22, "options": ["-o", "BatchMode=yes"], "password_secret": null},
    "container":{"image": "python:3.12-alpine", "network": "none", "workdir": "/work",
                 "mounts": [{"host": ".agent/mcp/.verify/fixtures", "container": "/work", "mode": "ro"}],
                 "secrets": []},
    "vmrun":    {"vmx": {"secret": "FLARE_VMX"}, "guest_user": {"secret": "VM_GU"},
                 "guest_password": {"secret": "VM_GP"}, "guest_dir": "C:\\Windows\\Temp\\mcp-bridge",
                 "guest_python": "python.exe", "idle_seconds": 120, "poll_interval": 0.4}
  }
}
```

任何欄位都可以是字面值或 `{"secret": "NAME"}`；值只從 `secrets.env` 取，`registry.json` 只記名稱。

### 12.3 三條由程式強制執行的紅線

1. **金鑰不上節點**：`exec.env` 不得引用 secret（規劃階段即 `TransportError`）。只有 `container.secrets`（明寫清單、以 `docker -e NAME` 讓值從容器客戶端環境轉入，值不進 argv）可以跨邊界。節點位址／客體憑證則只進**宿主 wrapper** 的環境或 argv，VM 不持有。
2. **不得掛到 repo 外**：`container.mounts[].host` 必須解析在 repo 內（`／`、`$HOME`、`..` 逃逸一律拒絕）；`network` 預設 `none`，要用網路必須明寫。
3. **節點型伺服器不得宣告宿主金鑰**：`secrets_binding.env` 若要求非 forwarded 的名稱，session 在拉起任何行程前就以 exit 2 拒絕（`secrets X cannot reach a <transport> node`）。

### 12.4 vmrun 傳輸的兩個實務陷阱（實測踩到）

- **不要用 `runProgramInGuest` 傳複雜 argv**：`vmrun` 轉交參數時的引用不完整，JSON argv 會走樣，客體程式**還沒開始就結束**，而 `runProgramInGuest` 仍回報成功。因此整個啟動描述會先落地成 `bridge-config.json`，客體只收到一個 `--config <file>`。（與 `vmrun_guest.py` 對 `.cmd` payload 的結論相同。）
- **客體程式要寫絕對路徑**：`vmrun` 不做 PATH 查找，`python3` 會失敗，`/usr/bin/python3` 才對；規劃與錯誤訊息都會提示這點。

傳輸本身是「兩個檔案當管道」：宿主把 JSON-RPC 逐行追加到 `requests` 後上傳，客體橋接器把伺服器 stdout 逐行追加到 `responses`，宿主再拉回來。只轉發**完整行**（尾端半行會被扣住），因此複製時機不會造成截斷的訊息。

### 12.5 清理語意（誰負責收尾）

MCP 客戶端結束 session 時通常是**硬殺**子行程（不是關 stdin），所以宿主適配器的 `finally` 不一定跑得到。因此：

- 客體橋接器在**收到關機哨兵或閒置逾時**後會自行刪掉宿主 staging 的所有檔案（含自己），並且在 host 已消失時仍一定會執行；
- 宿主收到 `SIGTERM`／`SIGINT` 時也會轉成正常退出（POSIX 有效），先把哨兵送進客體；
- 客體橋接器的 `--idle` 是安全網：主機死亡後最遲在該秒數後自行收工，不會留下孤兒伺服器（這正是 `vmrun_guest.py` 記錄過的痛點）。

實測：三個 vmrun session 結束後，客體 6 個 staged 檔與 3 個橋接行程在 60 秒內全數自行消失（`node_transport_demo.txt` §7）。

### 12.6 驗證狀態

| 傳輸 | 活體驗證 | 證據 |
| :--- | :--- | :--- |
| `container` | ✅ `python:3.12-alpine`、`--network none`、read-only 掛載；`whoami` 回容器 hostname／`python 3.12.14` | `.agent/mcp/.verify/node_transport_demo.txt` §2 |
| `ssh` | ✅ 真的在 Kali 節點執行（`host=kali`、`cwd=/home/kali`） | 同上 §3 |
| `vmrun_guest` | ✅ 真的經 VMware Guest Operations 進到執行中的客體（`host=kali`、無任何客體埠） | 同上 §4 |
| `vmrun_guest` 對 Windows 客體（FLARE-VM） | ⬜ 未實測：FLARE-VM 目前關機中，且未持有它的客體帳密；檔案橋接器的邏輯已由 `security/tools/tests/fake_vmrun.py`（假 vmrun＋真橋接器）端到端覆蓋 | `security/tools/tests/test_mcp_transports.py` |

驗證用的伺服器是拋棄式 echo fixture，跑在**另外一份** scratch registry（`.agent/mcp/.verify/node-demo-registry.json`）上；生產 registry 完全沒被改動。
