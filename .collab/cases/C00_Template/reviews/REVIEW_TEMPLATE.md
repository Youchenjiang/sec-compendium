# REVIEW: <REVIEW_TASK_ID> 獨立審查

> **檔名**：`REVIEW_<REVIEW_TASK_ID>.md`。`<REVIEW_TASK_ID>` 必須與 REVIEW task 的 `Task ID` 完全一致；被審查的 finding 由 task 的 `Review Target Finding` 指定，兩個 ID 不要求相同。

## 1. 審查資訊
- **對應 Task**：`<REVIEW_TASK_ID>`
- **對應 Finding**：`<TARGET_FINDING_ID>`
- **Reviewer Session**：`Session-Reviewer`
- **完成時間**：`YYYY-MM-DD HH:MM:SS UTC`

## 2. 審查結論
- **Verdict**：`APPROVED` / `CHALLENGED`
- **可支持答案狀態**：`CANDIDATE` / `VERIFIED`

## 3. Evidence Cross-check
- **重現結果**：說明是否可依 finding 的 artifact、tool 與步驟得到相同 observation。
- **時間與因果**：確認時區、事件順序與因果鏈沒有倒置。
- **替代解釋 / False Positive**：列出已排除與仍未排除的合理替代解釋。
- **格式檢查**：確認大小寫、時間格式、IP:Port、hash、路徑或 flag 格式。

## Race profile 邊界

> 正式 `REVIEW` task 屬 Governed mode，不能作為 Race lane。競賽中需要快速處理 `CONFLICT / semantic_risk / needs_review` 時，由 Lead 另建 `VERIFY` race lane；只有賽後、重大風險或需要完整獨立 provenance 時才進本 REVIEW 模板。

## 4. Blockers / Residual Risk
- `None`，或列出阻止 Main 將答案升為 `VERIFIED` 的具體 evidence gap。
