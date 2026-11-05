# WORKSHOP_202610_NET_Wireshark-v2：封包分析實務與網路資安鑑識

> **課程代號**：`WORKSHOP_202610_NET_Wireshark-v2`  
> **建議授課時數**：20 分鐘實務引導 ＋ 課後動手實作（約 15 分鐘可完成）  
> **適用對象**：資訊管理系 / 電資相關科系學生（幾乎無 Wireshark 先備經驗）  
> **核心目標**：透過情境化的真實工程案件，引導初學者掌握 Wireshark 介面操作、連線診斷（ICMP）與未加密協定鑑識（FTP/Telnet）。

---

## 💡 為什麼要有 v2 版本？（舊版痛點與改版核心）

| 項目 | 上屆舊版設計 ❌ | v2 新版架構 ✅ |
| :--- | :--- | :--- |
| **視覺與排版** | 過度渲染的 AI Bento Box、四根柱子卡片嵌套、字級過小 | 經典左文右圖分欄、大字級（≥ 30px）、無多餘裝飾色塊 |
| **文風口吻** | 「Log 會漏、人會猜，唯有網卡不說謊」等心靈雞湯口號 | 純工程敘述：明確的商業情境、故障現象、排查語法與技術結論 |
| **實作一 (ICMP)** | 盲目 ping 8.8.8.8 截圖，學生不知道為何需要開 Wireshark | 延伸 Tracert 與 TTL=0 路由器報錯機制，看清終端機隱藏的底層真相 |
| **實作二 (明文)** | 叫學生連線已廢棄或隨時斷線的未加密 HTTP 測試網站 | 採用國際標準開源靶場 **Root-Me 97 (FTP)**，全班檔案統一，100% 穩定能開 |
| **實作三 (進階)** | 要求用指令列 editcap 切割大檔與繪製 I/O Graph（難度斷崖超綱） | 簡化為 **Root-Me 99 (Telnet)** 互動式終端鑑識，體會字元回彈（Character Echo） |

---

## 🗺️ 課程與實作架構

```
[20 分鐘課堂導引]
  ├─ P.1~P.2 觀念定位：從 Application Log 走向 Network Traffic
  ├─ P.3~P.4 介面全景：Packet List / Details / Bytes 三段核心視野
  ├─ P.5 案例一：TCP Retransmission 與網路延遲排查
  ├─ P.6~P.8 案例二與對比：HTTP/FTP 明文傳輸風險 ＆ Follow TCP Stream 技法
  ├─ P.9~P.10 案例三與 AI：待機異常流量分析 ＆ AI Display Filter Prompting
  └─ P.11~P.12 排錯流程五步驟 ＆ 實作作業發布
      │
[課後動手實作]
  ├─ 實作一（本機實戰）：ICMP Ping & Tracert 深度解剖（通暢 vs 超時 vs 節點報錯）
  ├─ 實作二（離線靶場）：Root-Me 97 · FTP 明文密碼側錄（Follow Stream 實戰）
  └─ 實作三（加分挑戰）：Root-Me 99 · Telnet 終端連線鑑識（字元回彈 Character Echo）
```

---

## 📂 文件清單
* [`docs/LAB_ASSIGNMENT_AND_SCENARIOS.md`](./docs/LAB_ASSIGNMENT_AND_SCENARIOS.md)：完整的題目情境設定、實作步驟與技術結論。
* [`docs/instructor-guide.md`](./docs/instructor-guide.md)：助教與講師授課指引、關鍵問題解答劇本、改作業評分標準。
* [`docs/student-handout.md`](./docs/student-handout.md)：學生作業實作講義（可直接公告至 ee-class）。
* [`deck-studio/…/workshop-202610-net-wireshark-v2/index.tsx`](../../deck-studio/slides/workshop-202610-net-wireshark-v2/index.tsx)：14 頁全新高清大圖版 Open Slide 原始碼（置入完整實測 Wireshark 截圖）。
