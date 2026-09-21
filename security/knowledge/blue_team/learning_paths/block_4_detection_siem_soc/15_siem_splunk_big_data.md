# 📊 SIEM 大數據分析與 Splunk SPL 深度學習路徑
> 對應藍隊防衛矩陣：**領域 15** (15.1 ~ 15.4)
> 預計總投入時間：**40 ~ 50 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
只會下 index=xxx 的全字檢索 ──► 能熟練使用 stats/eval/rex 進行巨量日誌聚合
告警太多被警報疲勞淹沒   ──►    能設計基於基準線 (Baseline) 與標準差的動態告警
只會查單一事件           ──►    能用 transaction 串接橫跨多設備的端到端攻擊鏈
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
SPL管道管線基礎  正則動態欄位提取  統計聚合與異常基線  告警關聯規則設計
(10h)           (10h)             (10h)              (10h)
```

---

## 🔍 階段一：Splunk 核心 SPL 管道管線語法（約 10 小時）

```spl
# 經典暴力破解偵測：統計 5 分鐘內失敗次數超過 10 次且最終成功之來源
index=wineventlog EventCode=4625 OR EventCode=4624
| eval Status=if(EventCode==4625, "Failure", "Success")
| stats count(eval(Status=="Failure")) as Failures, 
        count(eval(Status=="Success")) as Successes by src_ip, user
| where Failures >= 10 AND Successes >= 1
```

---

## 📋 自我評估檢查點

- [ ] 說出 `stats` 與 `transaction` 在效能上的差異（巨量資料下優先推薦 `stats`）。
- [ ] 能使用 `rex` 從未結構化的 Syslog 訊息中抽取出 IP 與使用者名稱。
- [ ] 掌握如何用 `timechart` 繪製連線趨勢圖並找出異常流量突波 (Spike)。
