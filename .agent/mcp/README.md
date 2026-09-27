# MCP 接線規範與註冊點 (`.agent/mcp`)

此目錄是 `hitcon-range-sprint` 框架的 **MCP（Model Context Protocol）註冊點**。它**不存放任何 MCP 伺服器原始碼**，只存放治理與註冊資料：

| 檔案 | 角色 |
|------|------|
| `README.md` | 這份接線規範（治理、掛載點、節點持有、金鑰） |
| `registry.json` | 機器可讀的伺服器註冊表，**單一真相來源** |
| `servers/<name>.md` | 單一伺服器的引入說明與操作手冊 |
| `servers/<name>.verification.md` | 可跑的驗證證據（原始輸出） |

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

> 目前狀態：註冊表為空骨架（第 1 顆），第一個伺服器見後續 commit。
