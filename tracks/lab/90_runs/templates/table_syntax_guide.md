# 📋 資訊安全讀書會 - 標準表格模板庫 (Roadmap Table Templates)

> [!IMPORTANT]
> **用途說明**: 本檔案提供讀書會各種版本路線圖與平台對照表的標準 Markdown 語法模板，方便後續擴充、調整課程進度與開設教室時統一格式。

---

## 🛡️ 模板 1: 4 欄組長帶練總綱模板 (Master Leader Roadmap Template)
適用於 `master_roadmap_leader.md`。包含相對路徑教材與線上超連結，以及帶練 PoC 腳本提示。

```markdown
#### ⚔️ **Run X (Day Y-Z): [Run 主題名稱]**
📁 **核心教材**: `教材名稱/路徑` ｜ 🌐 **線上專題**: `https://...`

| 天數 (Day) | 🎯 當日教學/學習重點 (Focus Task) | 📁 核心教材與 🌐 線上資源 | 🧪 指定練習與帶練講義/PoC 腳本 (Lab & Starter Kit) |
| :--- | :--- | :--- | :--- |
| **Day Y** | [觀念與教學重點] | 研讀 `教材檔名` <br>🌐 `https://...` | `https://...` <br>💡 **組長帶練指示**: 解題關鍵步驟與腳本說明 |
| **Day Z** | [實操與進階重點] | 研讀 `教材檔名` <br>🌐 `https://...` | `https://...` <br>💡 **組長帶練指示**: 解題關鍵步驟與腳本說明 |
```

---

## 🚀 模板 2: 3 欄成員自學路線圖模板 (Member Study Roadmap Template)
適用於 `study_roadmap_member.md`。100% 採用 `https://` 公開網址，嚴禁出現本機檔案絕對路徑。

```markdown
#### ⚔️ **Run X (Day Y-Z): [Run 主題名稱]**
🌐 **線上專題**: [專題名稱](https://...)

| 天數 (Day) | 🎯 當日學習重點 (Focus Task) | 🧪 指定練習與線上關卡 (Target Labs & Challenges) |
| :--- | :--- | :--- |
| **Day Y** | [學習與觀念重點] | [PortSwigger Lab](https://...) <br>＋ picoCTF: [題目名稱](https://...) |
| **Day Z** | [實操與關卡突破] | [PortSwigger Lab](https://...) <br>＋ picoCTF: [題目名稱](https://...) |
```

---

## 🏫 模板 3: 4 欄專屬平台速查與教室開設模板 (Platform Special List Template)
適用於 `picoCTF_Only_90_Runs_List.md` 與 `PortSwigger_Only_90_Runs_List.md`。

```markdown
# 🏫 [平台名稱] 專屬 90 個 Run 1 對 1 獨立對照表 (4 欄獨立分立版)

| ⚔️ Run 號碼 | 🎯 主題 (Topic) | 📚 對應 Learning Path / 專題連結 | 🧪 指定實操關卡與直達超連結 (Labs / Challenges) |
| :--- | :--- | :--- | :--- |
| **Run 1 (Day 1-2)** | [主題名稱] | [Learning Path 網址](https://...) | • [題目 1 (ID: XXX)](https://...) <br>• [題目 2 (ID: YYY)](https://...) |
| **Run 2 (Day 3-4)** | [主題名稱] | - | - |
```
