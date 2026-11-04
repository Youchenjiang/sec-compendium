# Wireshark 基礎與封包分析 教材套件 (Curriculum Kit)

> **類型**：實戰工作坊 (`WORKSHOP`)  
> **編號**：`WORKSHOP_202610_NET_Wireshark-Fundamentals`  
> **技術領域**：網路協定分析 · 封包側錄 · TCP 掉包重傳排查 · HTTP 明文側錄 · 異常外連檢查 · AI 輔助過濾  
> **建議時間**：20 分鐘（3 分鐘工具定位 + 3 分鐘角色用途 + 10 分鐘實務情境 + 4 分鐘 AI 協同與 QA）

---

## 📦 套件結構 (Kit Contents)

```text
202610_NET_Wireshark-Fundamentals/
├── docs/                                 # 核心教材文檔
│   ├── instructor-guide.md               # 教師課堂教案 (20 分鐘配速、提問設計、白話引導)
│   └── lab-handout.md                    # 學員實作手冊 (四大實戰情境、介面三區導覽、AI Prompt 範本、複習題)
│
├── slides/                               # 投影片原始碼獨立存檔與交付產物
│   └── index.tsx                         # 12 頁簡報原始碼 (Open Slide React)
│
└── README.md                             # 本說明文件
```

---

## 🎯 核心教學方向

1. **聽得懂、用得上**：
   - 拋棄死背通訊協定規格的做法，從生活與工作中常見的痛點（網頁卡住、前後端吵 API、電腦不明流量）切入。
   - 建立直覺觀念：Wireshark 就是在網路卡上側錄封包，用實際記錄確認通訊事實，不靠猜測。
2. **介面三塊區域清楚拆解**：
   - 上方：封包清單（時間、來源、目的、協定）。
   - 中間：協定詳細欄位（IP、TCP、HTTP 等具體內容，排錯最常看）。
   - 下方：原始 Hex/ASCII 資料。
3. **四個接地氣的實戰情境**：
   - 【維運】網頁卡住？用 `tcp.analysis.flags` 查看 TCP 掉包與超時重傳。
   - 【安全】為什麼不能用 HTTP？用 `http.request.method == "POST"` 側錄純文字帳號密碼。
   - 【開發】封包被切碎怎麼看？用右鍵 `Follow TCP Stream` 重組雙向對話。
   - 【檢查】待機卻有流量？排查異常 DNS 查詢與固定頻率的心跳連線。
4. **不用死背語法，讓 AI 寫過濾條件**：
   - 清楚表達想查的情境與條件，讓 AI 轉成正確的 Display Filter，工程師專注於排錯與解決問題。

---

## 🚀 快速開始

### 1. 課堂授課預覽 (Open Slide)
在 `Common/Slide/open-slide` 目錄啟動投影片伺服器：
```bash
cd ../../open-slide
npm run dev
# 瀏覽: http://localhost:5173/s/workshop-202610-net-wireshark-fundamentals
```

### 2. 閱讀教材
* 講師備課：檢視 [`docs/instructor-guide.md`](docs/instructor-guide.md)
* 學員實作：檢視 [`docs/lab-handout.md`](docs/lab-handout.md)
