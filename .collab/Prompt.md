請在以下 repo 對目前的 HITCON Host-DFIR AI 協作架構做一次**全新的真實 blind Race benchmark**：

`C:\Users\LabStrix\Documents\GitHub\Youchen\Security\hitcon-range-sprint`

這是一個架構驗收，不是單純解題。請自主執行直到測試完整結束，不要中途停下來等我確認一般操作。

開始前先閱讀並遵循目前 repo 內的 canonical 規範，至少包括：

- `.collab/README.md`
- `security/tools/README.md`
- `tracks/lab/hitcon_range/playbooks/Holmes2026_人機協同解題流水線SOP.md`
- `tracks/lab/hitcon_range/playbooks/Holmes2026_雙機鑑識分工與作戰SOP.md`

先 inspect 現有 repo/runtime 狀態，不要假設前一個對話的狀態。

## 測試目的

驗證目前 Race architecture 是否能在約 30 分鐘級 budget 內，對一個**真正未看過答案的大型 Host-DFIR case**完成主要小題，並保持 evidence-first、fail-closed、secret-safe、可重現 provenance。

不要以 C01 BottleOut 或 C05 PaperGhost 當新的驗收樣本；它們已經是 calibration / benchmark history。

## STRICT BLIND 規則

測試開始後直到 Race close 前：

- 只能使用原始 evidence / specimen。
- 禁止讀取任何：
  - `analysis/`
  - `solution/`
  - `solved/`
  - `writeup`
  - `answer-key`
  - challenge metadata 中的答案
  - 既有 FINDING / REVIEW / questions 中可能洩露同一題答案的內容
  - MEMORY 或其他先前解題紀錄中關於該 challenge 的答案
- 不得上網搜尋該 challenge 的解答。
- 若發現 selected case 已被目前 workspace 的既有內容污染，立即棄用它，改選另一個真正 unseen case；不要假裝 blind。

可以閱讀 framework / tooling / SOP 文件，但不得閱讀目標 challenge 的既有答案材料。

## 執行要求

1. 找到合適的 unseen real Host-DFIR challenge 與原始 evidence。
2. 在開 Race clock **之前**先跑 DFIR preflight。
3. 如果 parser/toolchain 缺失：
   - 在開鐘前修好；
   - 使用 repo 已驗證的 pinned Race DFIR environment；
   - 不得把安裝/環境摸索算成正式 Race 解題時間。
4. 建立新的 Race case/session，不得重用舊 benchmark 的 runtime scoring state。
5. 預設：
   - budget = 30 minutes
   - worker START SLO = 60 seconds
6. 依 evidence domain 一次建立約 3–4 條 Investigation Lanes；不要一題一 task。
7. Worker 每解出一題就立即 publish `CANDIDATE` / `READY`，不要等 finding 或 DONE。
8. READY 必須符合目前 evidence gate：
   - high confidence
   - 至少兩個可定位 evidence references
   - 無 semantic risk / needs-review
9. 如果答案是 password/token/session secret：
   - 使用 secret-aware READY；
   - plaintext 不得進 tracked `.collab` 或 cloud-synced runtime。
10. 持續監看 worker START：
    - 超過 60 秒未 START 時立即使用 watchdog；
    - Case Lead 執行 cheap-pivot / Lead assist；
    - Lead assist 必須遵循既有 `LANE_ASSISTED` temporal provenance。
11. 不得因 worker/browser/composer 啟動失敗讓整條 critical path 卡住。
12. 在 15 分鐘時保留可重建的 cutoff。
13. 到全部主要小題完成或 30 分鐘 budget 到時立即 `close`。
14. `SESSION_CLOSED` 後發現的新答案只能算 postmortem，不得回灌 benchmark。
15. Race close 後，再完成各 lane 的 governed FINDING / DONE，保留完整 provenance。
16. 跑：
    - Race board
    - 15m / 30m cutoff
    - metrics
    - race doctor
    - collab doctor
17. 不要 stage、commit 或 push。

## 最終我要看到的驗收結果

請明確回報：

- 測試的 case / evidence scope
- 為什麼能合理認定是 blind
- preflight 結果
- lane routing
- routing_complete_seconds
- first_worker_start_seconds
- all_lanes_started_seconds
- worker START SLO breaches
- first_candidate_seconds
- first_ready_seconds
- ready_50_seconds
- ready_80_seconds
- ready_100_seconds
- 15m READY 比例
- 30m READY 比例
- close time
- 最終 READY/總題數
- race doctor 結果
- collab doctor 結果
- governed findings/DONE 是否完整
- secret hygiene 是否通過
- 觀察到的 bottleneck

最後請依 evidence 判斷：

- PASS：目前架構足以支援約 30 分鐘內完成一個大型 Host-DFIR 題組；
- 或 FAIL：仍太慢。

如果 FAIL，不要美化結果，也不要用 post-close 答案回填；請直接指出真正 bottleneck，並在同一輪中修正架構、補 regression tests，再用另一個新的 blind case 重測。

整個過程請自主推進。除非遇到真正需要我提供的外部資訊、人工平台提交、缺失的 specimen，或具有破壞性/不可逆的動作，否則不要停下來問我下一步。