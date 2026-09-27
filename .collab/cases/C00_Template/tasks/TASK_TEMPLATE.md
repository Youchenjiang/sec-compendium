# TASK: T000 - [簡短名稱]

> **檔名**：`T000_TYPE.md`，例如 `T001_TRIAGE.md`。Task 發布後 immutable。

## 1. 任務基本資訊
- **所屬大題**：`C00_Template`
- **關聯小題**：例如 `Q03, Q04`
- **任務類型**：`DISCOVERY` / `TRIAGE` / `VERIFY` / `REVERSE` / `REVIEW`
- **Protocol Contract**：`v2.3`
- **Target Role**：`ROLE_01_TRIAGE_HUNTER` / `ROLE_02_REVERSE_ENGINEER` / `ROLE_03_DEVILS_ADVOCATE`
- **Assignee Session**：`Session-...`（必填且唯一）
- **發起 Session**：`Session-Main`
- **發起時間**：`YYYY-MM-DD HH:MM:SS UTC`
- **Execution Environment**：`host_local_gateway` / `portable_text_any`（必填；對應 canonical metadata `execution_environment`）
- **Review Target Finding**：`FINDING_T000`（僅 `REVIEW` 必填；其他 task 移除此列）
- **期望技能**：`[代碼逆向 / 去混淆]` / `[海量日誌過濾]` / `[封包解構]` / `[第二意見審查]`
- **Task ID**：`T000`

---

## 2. 案情背景與目標
*(簡述目前遇到的瓶頸與需要輔助 Session 協助解答的具體問題)*
> 例如：在受害主機的排程任務中發現一段 Base64 編碼的 PowerShell 指令，請協助還原其真實執行的 Payload、解出連線網址與寫入的檔案路徑。

---

## 3. 待分析資料片段 (Context Payload)
*(直接附上文字、日誌片段、Base64 字串或十六進位 Hex，切勿上傳二進位大檔)*

```text
powershell.exe -enc JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMgAwADMALgAwAC4AMQAxADMALgAxADAAIgAsADgAMAA4ADAAKQA7AA==
```

---

## 4. 接單 Session 輸出規範
請支援 Session 在完成後：
1. **不得修改本 task 檔案**；發布後 task 為 immutable，由 Case Lead 保有唯一建立權。
2. 只有 `Assignee Session` 精確等於目前 Session 才能接單；`Target Role` 相同不授予接單權。
3. `Execution Environment` 是強制治理欄位：`host_local_gateway` 只能由明確配置成 `primary` node class 的 watcher 執行；`portable_text_any` 才可跨節點。
4. `DISCOVERY` / `TRIAGE` / `VERIFY` / `REVERSE` 在 `findings/` 新增精確 `FINDING_T000.md`。
5. `REVIEW` 在 `reviews/` 新增精確 `REVIEW_T000.md`。
6. `REVIEW` 必須用 `Review Target Finding` 明確指向既有 governed finding；review output 的 `對應 Finding` 必須完全相同。
7. 若為 `VERIFY` 且既有候選皆不成立，必須明確回報「皆非」並附上反證，不可為了符合題目而硬選 A/B/C。
