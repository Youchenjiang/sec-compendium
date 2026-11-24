# CASE_STATE: [大題名稱] 案情事實看板

## 1. 代理人權責與狀態
- **大題代號**：`C00_Template`
- **主導代理人 (Lead Session)**：*(填入由 Main 指派之 Session 名稱，例: Session-CaseLead)*
- **當前攻堅狀態**：`⚪ 待認領` / `🟢 攻堅中` / `🏁 已結案`
- **開始時間**：`YYYY-MM-DD HH:MM:SS UTC`

---

## 2. 標本與環境資訊 (本機路徑，不進雲端！)
- **受害作業系統**：Windows 10 / Server 2019 / Ubuntu 22.04
- **標本本地路徑**：`D:\LabData\Challenges\sample.E01` (僅供本機讀取)
- **分析建議執行環境**：`host_local_gateway` / `portable_text_any`

---

## 2A. Execution Profile / Race Session（需要時填）

- **Execution Profile**：`governed` / `race`
- **Race Budget**：`30m`（若非 race 填 `N/A`）
- **Lane Routing**：例 `L01=execution+registry / L02=filesystem+browser / L03=network+SRUM / L04=reverse`
- **Live Answer View**：Race 時以 `.collab/runtime/race/<CaseID>/events/` 推導；**不要把 runtime board 複製成第二份 canonical state**。

> Race mode 期間本檔仍只有 Case Lead 可寫；worker 的即時答案走 append-only race events。Race 結束後再將穩定的 evidence-backed facts promotion 到下方核心事實。

## 3. 已確認之核心事實 (Evidence-backed Facts)
> 只有已有可追溯 finding/review、可重現且由 Case Lead 接受的事實才記錄於此；每項事實應附來源工件 ID，避免「高信心」取代證據。

- [ ] **受害主機名**：
- [ ] **受害主機 IP**：
- [ ] **攻擊者初始登入 IP**：
- [ ] **初始入侵時間點 (UTC)**：
- [ ] **已確認之惡意進程 / 後門路徑**：
- [ ] **確定之 C2 連線端點 (IP:Port)**：

---

## 4. 進行中之作戰假說 (Active Hypotheses)
> 記錄當前正在驗證但尚未完全閉環的推論，避免不同 Session 重複走冤枉路。

- **假說 1**：
- **假說 2**：
