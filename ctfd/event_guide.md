# 國立中央大學 資訊管理學系 碩一新生茶會
# 🏆 Mini-CTF 資安闖關賽 全套活動手冊暨官方解題指南 (Write-Up)

---

## 📌 目錄
1. [活動架構與技術機制](#1-活動架構與技術機制)
2. [7 大題目設計矩陣與故事背景](#2-7-大題目設計矩陣與故事背景)
3. [官方詳細題解與破關指南 (Write-Up)](#3-官方詳細題解與破關指南-write-up)
4. [伺服器維運與應變操作手冊](#4-伺服器維運與應變操作手冊)

---

## 1. 活動架構與技術機制

### 🌐 競賽環境資訊
* **競賽平台網址**：`https://im2026ctf.duckdns.org`
* **主機環境**：Oracle Cloud Infrastructure (Ubuntu 24.04, 1 OCPU, 1 GB RAM + 2 GB Swap)
* **核心架構**：Docker 容器化 CTFd + Caddy 自動 HTTPS 反向代理
* **參賽規模**：約 70 位研一新生，2~3 人為一組自由組隊。

### 🛡️ 核心防作弊：確定性動態洗牌 Flag 機制 (Deterministic PRNG Dynamic Shuffle)
為避免各小組直接抄襲、口耳相傳答案，本系統開發了專屬 CTFd 外掛 `dynamic_shuffle_flag`：
1. **零狀態儲存 (Stateless)**：主機不需為各隊伍在資料庫建立額外 Flag 欄位。
2. **確定性計算 (Deterministic & Idempotent)**：
   $$\text{Seed} = \text{SHA-256}(\text{SECRET\_KEY} + \text{TeamName} + \text{BaseFlag})$$
   同一隊伍在任何時間、下載多少次檔案，取得的 Flag **永遠 100% 相同**。
3. **隊名特徵隨機混淆**：系統從隊名中動態截取 1~2 個前後字元，隨機洗牌後穿插於基底 Flag 中。即使兩隊並排坐，彼此看到的 Flag 也完全不同。
4. **極致輕量化 Blueprint**：附件動態下載與實驗室網頁全由 CTFd 內部 Flask Blueprint 即時渲染，免開外部 Port、不耗費額外記憶體。
5. **🎬 破關結局爆料彈窗 (Post-Solve Story Epilogue Modal)**：
   當學生提交正確 Flag 時，平台前端會自動彈出沉浸式的【劇情結局卡片】，為該題的故事畫下爆笑句點！
6. **💡 兩階段階梯式提示機制 (2-Tier Progressive Hints)**：
   題幹敘述移除破梗直接指令，改為情境敘述，將破關關鍵線索收納於 CTFd 的 Hint 機制中：
   * **Hint 1（線索方向 / 20 pts）**：引導思考與觀察盲點。
   * **Hint 2（破關手法 / 50 pts）**：提供具體工具推薦與關鍵步驟。

---

## 2. 7 大題目設計矩陣與故事背景

| 題號 | 題目名稱 | 題型類別 | 分數機制 | 內建端點 / 下載路徑 | 翻轉結局 Flag 基底 (Base Flag) | Hint 提示設計 |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- |
| **1** | **中央資管歡迎你！** | Misc / 簽到 | 100 固定分 | 平台直接作答 | `NCUMIS{welcome_to_central_mis}` *(固定送分)* | 0 pt 簽到指引 |
| **2** | **學長的最後目擊照片** | Misc / OSINT | 500 動態遞減 | `/download/campus` | `senior_fled_to_kenting` | 20 pt (EXIF概念) / 50 pt (檢視手法) |
| **3** | **學長留下的屎山代碼** | Web / DevTools | 500 動態遞減 | `/labs/f12` | `do_not_touch_this_trash` | 20 pt (HTML註解) / 50 pt (Cookie儲存) |
| **4** | **教授的機密加簽信** | Crypto / 密碼學 | 500 動態遞減 | `/labs/crypto` | `prof_please_sign_course` | 20 pt (Base64) / 50 pt (Caesar-3) |
| **5** | **咪挺出席與成績系統** | Web / SQLi | 500 動態遞減 | `/labs/sqli` | `prof_also_overslept` | 20 pt (注入思維) / 50 pt (萬能語法) |
| **6** | **這隻貓吃掉了碩士論文** | Forensics / 隱寫 | 500 動態遞減 | `/download/cat` | `the_cat_is_innocent` | 20 pt (隱寫原理) / 50 pt (改副檔名/7-Zip) |
| **7** | **畢業資格自動審查程式** | Reverse / 逆向 | 500 動態遞減 | `/download/check_graduation` | `graduation_is_a_lie` | 20 pt (字串原理) / 50 pt (strings/搜尋) |

---

## 3. 官方詳細題解與破關指南 (Write-Up)

### 🚩 第 1 題：中央資管歡迎你！
* **難易度**：⭐（入門送分題）
* **技術點**：熟悉 CTFd 介面與 Flag 提交流程。
* **解題步驟**：
  1. 閱讀題目說明。
  2. 直接複製題目中給出的 `NCUMIS{welcome_to_central_mis}`。
  3. 貼入提交框點擊「提交」即可獲得 100 分。
* **破關劇情彈窗**：
  > 🌟 **【入學啟程：中央資管大家庭】**  
  > 恭喜你完成簽到！在未來的兩年裡，有學長姐與老師們陪伴你們一起探索學術與技術的精彩世界。歡迎加入中央資管大家庭！

---

### 🚩 第 2 題：學長的最後目擊照片
* **難易度**：⭐⭐（中繼資料分析）
* **技術點**：圖片中繼資料 (EXIF Metadata)、Windows 原生 UTF-16LE 屬性標籤 (`XPComment` / `XPSubject`)。
* **防文字搜尋機制**：
  * Flag 在圖檔中採用 Windows 原生 EXIF UTF-16LE 二進位編碼，**以 Notepad++ / 一般文字編輯器搜尋 `NCUMIS` 結果為 0（找不到）**，確保參賽者必須透過正規 EXIF 檢視方式解題。
* **解題步驟**：
  1. 點擊題目連結 `https://im2026ctf.duckdns.org/download/campus` 下載隊伍專屬照片 `disappeared_senior_for_<隊名>.jpg`。
  2. **方法 A（Windows 檔案總管 - 最直接）**：
     * 對圖片點「右鍵」➔「內容」➔ 切換至「**詳細資料 (Details)**」分頁。
     * 查看「**主旨**」或「**備註**」欄位，即可清晰看見專屬 Flag！
  3. **方法 B（線上工具）**：
     * 將圖片上傳至線上 EXIF 檢視器（如 [exifinfo.org](https://exifinfo.org/) 或 [jimpl.com](https://jimpl.com/)）。
  4. 取得該隊專屬 Flag（如 `NCUMIS{senior_fled_to_kenting...}`）並提交。
* **破關劇情彈窗**：
  > 🏖️ **【結局爆料：全網通緝叛逃學長】**  
  > 恭喜你從照片 EXIF 找到了學長在墾丁衝浪的自白！系辦助教看到你的通報後震怒：「難怪學長剛剛在 IG 發海邊打卡限動！立刻打電話叫他下週一早上 8 點回來報告 Paper！」

---

### 🚩 第 3 題：學長留下的屎山代碼
* **難易度**：⭐⭐（前端檢查）
* **技術點**：瀏覽器開發者工具 (F12)、HTML 註解檢查、Cookie 儲存區。
* **解題步驟**：
  1. 點擊進入實驗室 `https://im2026ctf.duckdns.org/labs/f12`。
  2. 按下鍵盤 **F12**（或右鍵點擊「檢查」）打開開發者工具。
  3. **取得前半段 Flag (Part 1)**：
     * 切換至 **Elements (元素 / 原始碼)** 標籤頁。
     * 在 `<body>` 標籤開頭找到 HTML 註解：`<!-- [Part 1 of Flag - 學長留下的註解自白]: NCUMIS{do_not_... -->`。
  4. **取得後半段 Flag (Part 2)**：
     * 切換至 **Application (應用程式)** 標籤頁 ➔ 左側展開 **Cookies** ➔ 點擊該站網址。
     * 找到名為 `flag_part2` 的 Cookie 鍵值（如 `...touch_this_trash}`）。
  5. 將兩段字串首尾拼湊，組成完整的 `NCUMIS{...}` 提交。
* **破關劇情彈窗**：
  > 💥 **【結局爆料：實驗室伺服器危機】**  
  > 恭喜你拼湊出學長十年前寫在註解裡的自白：`do_not_touch_this_trash`！但因為你剛才在 F12 裡不小心刪了一行註解，實驗室的主機風扇突然開始狂轉冒煙……「快關掉瀏覽器裝作什麼事都沒發生！」

---

### 🚩 第 4 題：教授的機密加簽信
* **難易度**：⭐⭐⭐（密碼學編碼與位移）
* **技術點**：Base64 解碼、古典凱撒密碼 (Caesar Cipher) 逆向位移。
* **解題步驟**：
  1. 點擊開啟教授機密加簽信件 `https://im2026ctf.duckdns.org/labs/crypto`。
  2. 複製羊皮紙中央打字機區塊中的密文字串（如 `c3VyaV9wbGVhc2Vfc2lnbl9jb3Vyc2U=`）。
  3. 使用萬能密碼工具 [CyberChef](https://gchq.github.io/CyberChef/)：
     * 拖入第一層配方：**From Base64**（解出凱撒密文字串）。
     * 拖入第二層配方：**ROT13 / Caesar Cipher**（設定 Amount 為 **-3** 或 **23**）。
  4. 解出明文真相 `NCUMIS{prof_please_sign_course...}` 並提交。
* **破關劇情彈窗**：
  > 🎓 **【結局爆料：加簽的殘酷真相】**  
  > 恭喜你成功解出加選授權碼！正當你興高采烈衝去系辦要送出時，助教突然拍了拍你的肩膀：「同學……教授剛剛走出辦公室宣佈，因為教室容納不下，這門課今年不開了……」（新生崩潰：那我剛才算凱撒密碼到底在忙什麼？！）

---

### 🚩 第 5 題：咪挺出席與成績系統
* **難易度**：⭐⭐⭐（Web 漏洞初探）
* **技術點**：SQL Injection 登入繞過（萬能密碼）。
* **解題步驟**：
  1. 進入系統閘道 `https://im2026ctf.duckdns.org/labs/sqli`。
  2. 觀察頁面提示的後端 SQL 語法：
     ```sql
     SELECT * FROM users WHERE user='$user' AND pass='$pass'
     ```
  3. 在 **帳號 (Username)** 欄位輸入經典萬能密碼：
     ```text
     ' OR 1=1 --
     ```
     （密碼欄位隨意輸入或留空）。
  4. 點擊登入，SQL 邏輯被恆真式 `'1'='1'` 閉合繞過，頁面成功彈出綠色提示與專屬 Flag（`NCUMIS{prof_also_overslept...}`）。
* **破關劇情彈窗**：
  > 🏆 **【結局爆料：拯救全班的無名英雄】**  
  > 恭喜你用萬能密碼 `' OR 1=1 --` 成功潛入出席系統！你順手把這學期全體研一新生的出席率改成了 100 分。教授隨後在 Line 大群廣播：「看在大家這學期全勤的份上，期末報告全部免試！」

---

### 🚩 第 6 題：這隻貓吃掉了碩士論文
* **難易度**：⭐⭐⭐（二進位檔案結構）
* **技術點**：JPEG 尾端藏匿 Zip 封包 (File Append Steno)、解壓縮分離。
* **解題步驟**：
  1. 點擊下載專屬貓咪圖片 `https://im2026ctf.duckdns.org/download/cat`（檔案為 `cat_ate_my_thesis_for_<隊名>.jpg`）。
  2. **方法 A（改副檔名直接解壓）**：
     * 將檔案名稱由 `.jpg` 重新命名為 `.zip`。
     * 直接使用 Windows 內建解壓縮或 7-Zip / WinRAR 開啟。
  3. **方法 B（7-Zip 右鍵開啟）**：
     * 對圖片點右鍵 ➔「7-Zip」➔「開啟壓縮檔」。
  4. 開啟壓縮檔內部的 `eaten_thesis.txt`，即可看見自白 Flag（`NCUMIS{the_cat_is_innocent...}`）。
* **破關劇情彈窗**：
  > 🐱 **【結局爆料：這隻貓咪要來咪挺了】**  
  > 恭喜你剖開圖片提取出學長「其實連 Abstract 都沒寫」的自白！教授看完這份自白檔案後默默把貓咪抱到椅子上：「這隻貓咪看起來比學長誠實，下週開始由這隻貓代替學長來 Meeting 報告。」

---

### 🚩 第 7 題：中央資管碩士生存戰
* **難易度**：⭐⭐⭐⭐（逆向工程與模擬遊戲）
* **技術點**：Windows PE / Linux ELF 雙平台二進位、12 回合文字模擬遊戲、XOR 動態解密混淆。
* **防文字搜尋機制**：
  * 二進位檔案內的 Flag 採用 **XOR `0x5A` 動態加密混淆**，在文字編輯器（Notepad++ / VS Code / strings）中搜尋 `NCUMIS` 結果為 0！程式在玩家順利通過 12 回合口試判定時，動態於記憶體中解密印出。
* **解題步驟**：
  1. 點擊題目連結下載隊伍專屬執行檔：
     * Windows 使用者：下載 `mis_survival_game.exe`，直接雙擊即可開始遊玩！
     * Linux / Mac 使用者：下載 `mis_survival_game`，下指令 `chmod +x mis_survival_game` 即可執行。
  2. **方法 A（策略通關遊玩 - 沉浸體驗）**：
     * 經歷 12 個關鍵月份（碩一上 9/10/12月、碩一下 3/5/7月、碩二上 9/11/1月、碩二下 3/5/7月口試）。
     * 每回合平衡【💚 體力】、【🧠 壓力】、【📑 論文進度】與【☕ 特濃黑咖啡】，於第 12 回合 Final Defense 結算時論文達到 100% 且體力未耗盡、壓力未爆表，程式即解密印出畢業證書 Flag！
  3. **方法 B（逆向工程分析 - 頂尖駭客解法）**：
     * 使用 Ghidra / IDA Pro / x64dbg 載入二進位檔案。
     * 定位 `print_victory()` 函數，分析 `ENCRYPTED_FLAG` 陣列與 `0x5A` XOR 解密循環，直接撰寫 2 行 Python 解出 Flag！
  4. 取得 Flag（`NCUMIS{graduation_is_a_lie...}`）並送出。
* **破關劇情彈窗**：
  > 🎓 **【結局爆料：恭喜碩士順利登頂】**  
  > 恭喜你成功通關資管碩士生涯模擬器！不論你是靠神乎其技的時間管理能力，還是靠強大的逆向分析實力通關，系主任都對你的實力深感佩服：  
  > **「這位同學兼具頂尖的資安實力與超強抗壓性，下週開始由你擔任研究室大組長！」**

---

## 4. 伺服器維運與應變操作手冊

### 🔑 伺服器連線
* **主機 IP**：`129.225.174.13` (User: `ubuntu`)
* **SSH 連線指令**：
  ```bash
  ssh -i "f:\OutClass\資訊應用\網路安全\security\ssh-key-2026-08-24.key" ubuntu@129.225.174.13
  ```

### ⚡ 常用維運指令

#### 1. 查看 CTFd 與資料庫運行狀態
```bash
cd ~/CTFd
sudo docker compose ps
```

#### 2. 即時查看 CTFd 存取日誌與報錯
```bash
sudo docker compose logs -f ctfd
```

#### 3. 重新載入外掛與重啟服務
```bash
cd ~/CTFd
sudo docker compose restart ctfd
```

#### 4. 本地一鍵更新外掛與重啟指令
在本地 Windows 終端機執行：
```powershell
python "f:\OutClass\資訊應用\網路安全\deploy_plugin.py"
```

#### 5. 匯出競賽備份檔
* 競賽結束後，進入 CTFd 管理後台 ➔ **Config** ➔ **Backup** ➔ 點擊 **Export** 下載完整 Zip 備份。

---
*文件編制日期：2026 年 8 月*  
*國立中央大學 資訊管理學系 資安研討團隊*
