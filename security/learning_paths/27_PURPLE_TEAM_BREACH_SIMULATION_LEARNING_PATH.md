# 🟣 防禦驗證工程與紫隊協同深度學習路徑 (Purple Teaming & BAS)
> 對應藍隊防衛矩陣：**領域 27** (27.1 ~ 27.3)
> 預計總投入時間：**30 ~ 40 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
紅隊打完丟份報告就結束   ──►    建立紅藍高頻協同 (Purple Team) 持續驗證迴路
不清楚防禦規則是否真有效 ──►    運用 Caldera/Atomic Red Team 自動化驗證防禦盲點
只監控告警卻不知漏報率   ──►    能精準量化遙測覆蓋率 (Telemetry Coverage)
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
紫隊協同理念與流程  Atomic Red Team佈建  MITRE Caldera自動化  防禦盲點閉環驗證
(8h)              (10h)                 (10h)                (8h)
```

---

## ⚛️ 階段一：Atomic Red Team 原子化對抗測試（約 10 小時）

- 依據 MITRE ATT&CK 每個具體技術編寫標準化可重複執行的測試指令碼：
```powershell
# 執行 T1003.001 (OS Credential Dumping: LSASS Memory)
Invoke-AtomicTest T1003.001 -TestNumbers 1
```
- **藍隊閉環驗證**：執行後立即檢視 EDR 或 SIEM 是否成功產生對應事件且阻斷連線。

---

## 📋 自我評估檢查點

- [ ] 說出傳統紅藍對抗演練與現代紫隊 (Purple Teaming) 的核心協同價值差異。
- [ ] 能夠在測試主機安全執行 Atomic Red Team 測試並驗證日誌捕獲情況。
- [ ] 能以 ATT&CK Navigator 繪製防禦覆蓋熱圖 (Detection Heatmap)。
