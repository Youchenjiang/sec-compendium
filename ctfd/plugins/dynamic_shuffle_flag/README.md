# 🚩 CTFd Dynamic Shuffle Flag Plugin (防作弊動態 Flag 外掛)

> 本外掛為 CTFd 專用之防作弊動態 Flag 生成與即時注入外掛。  
> 依據隊伍名稱（Team Name）與伺服端密鑰（Secret Salt），動態為不同隊伍計算並注入獨一無二的 Flag，有效杜絕競賽期間 Flag 複製抄襲。

---

## ⚙️ 核心特性

1. **隊伍專屬動態雜湊**：
   - 使用 HMAC-SHA256 結合伺服端 Salt 與參賽隊伍識別碼，動態生成每隊專屬 Flag（格式：`NCUMIS{<inner>_<hash>}`）。
2. **多載體即時二進位注入**：
   - **二進位執行檔**：下載二進位題目時即時置換特定特徵碼區段。
   - **圖片 EXIF 標籤**：透過 `piexif` 即時寫入 UserComment / Artist 欄位。
   - **ZIP 註釋與尾部資料**：即時打包專屬題檔提供下載。
3. **安全隔離**：
   - 伺服端 Salt 透過環境變數 `CTFD_FLAG_SALT` 注入，預設值與競賽生產密鑰分離。

---

## 🚀 部署方式

由根目錄執行一鍵套用腳本，或將本目錄軟連結/複製至 CTFd 的 `CTFd/plugins/` 目錄下重啟即可：

```bash
cp -r ctfd/plugins/dynamic_shuffle_flag /path/to/CTFd/CTFd/plugins/
docker compose restart
```
