# CyLab 題庫技能分類

> 把 [`cylab_all_challenges_2026-08-08.csv`](cylab_all_challenges_2026-08-08.csv) 的 525 題，從官方 8 類改依「要學會的技能」分成 16 類，給排課選題用。逐題結果在 [`cylab_skill_classification_2026-08-08.csv`](cylab_skill_classification_2026-08-08.csv)，由 [`classify_skills.py`](classify_skills.py) 產生。M1～M7 對應《電腦網路安全》的技能階梯，見 [`ncu_cylab_challenge_selection.md`](../../../../../tracks/courses/ncu_cylab_challenge_selection.md)。

## 為何不用官方分類

官方分類一類裡混了好幾種技能：Forensics 同時有封包、中繼資料、磁碟映像、隱寫；General Skills 同時有編碼、Linux 指令、git、密碼。排課要的是「這週練哪一種能力」，所以改依技能分。

## 各技能題數

| 技能 | 題數 | Easy | 逐題歸類 | 依題名推測 | 官方分類預設 |
|---|---|---|---|---|---|
| M1 編碼與資料表示 | 14 | 10 | 9 | 5 | 0 |
| M2 前端暴露與 HTTP | 19 | 11 | 19 | 0 | 0 |
| M3 封包分析 | 13 | 1 | 13 | 0 | 0 |
| M4 認證、Session 與 Cookie | 26 | 10 | 26 | 0 | 0 |
| M5 伺服器端注入與輸入信任 | 23 | 2 | 21 | 2 | 0 |
| M6 古典密碼與雜湊 | 32 | 6 | 32 | 0 | 0 |
| M7a 檔案、中繼資料與隱寫 | 51 | 12 | 48 | 1 | 2 |
| M7b 磁碟、記憶體、日誌與 Git 調查 | 22 | 1 | 16 | 6 | 0 |
| M7c 讀程式找密鑰（入門逆向） | 23 | 3 | 23 | 0 | 0 |
| Linux、工具與程式操作 | 54 | 34 | 43 | 11 | 0 |
| 現代密碼學（RSA／AES／XOR 等） | 52 | 3 | 0 | 0 | 52 |
| 二進位逆向（組語、除錯器） | 79 | 0 | 0 | 0 | 79 |
| Binary Exploitation（pwn） | 76 | 4 | 0 | 0 | 76 |
| 進階 Web（XSS、WASM 等） | 21 | 0 | 12 | 1 | 8 |
| AI | 16 | 16 | 0 | 0 | 16 |
| Blockchain | 4 | 0 | 0 | 0 | 4 |
| 合計 | 525 | 113 | | | |

課程範圍（M1～M7c）共 223 題，加上 Linux 工具 54 題；其餘 248 題（現代密碼、二進位逆向、pwn、進階 Web、AI、Blockchain）超出這門課。

## 歸類依據與限制

CSV 只有題名、分類、難度，沒有題目說明，所以每題標了歸類依據：

| 歸類依據 | 意思 | 可信度 |
|---|---|---|
| 逐題歸類 | 認得這題、知道它考什麼 | 高 |
| 依題名推測 | 只從題名判斷，多為 picoCTF 2026 新題 | 中，選題前先看題目說明 |
| 官方分類預設 | 沒逐題看，依官方分類丟進對應的大類 | 低，但多落在超出課程的類別 |

幾個值得注意的分布：

- **M3 封包只有 1 題 Easy**（Ph4nt0m 1ntrud3r），其餘都是 Medium。
- **M4 認證有 10 題 Easy**，選題空間最大。
- Easy 集中在 Linux 工具（34）與 AI（16），真正能當課程帶練的 Easy 約 56 題。

## 更新方式

題庫快照更新後，在本目錄執行：

```bash
python classify_skills.py
```

新出現的題目會依官方分類落入預設類別；要精確歸類，把 ID 加進 `classify_skills.py` 的 `SKILLS`（只憑題名判斷的另外加進 `NAME_ONLY`）。
