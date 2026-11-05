# A4 - Cylab Auth

> 2026-11-06 發布。對應技能階梯 M4（認證、Session 與 Cookie），選題與理解問題見 [`ncu_cylab_challenge_selection.md`](../../../ncu_cylab_challenge_selection.md)。期限、成績比重與 CyLab 作業連結以 eeclass 作業頁為準。

## 前置作業

參考講義：[伺服器憑什麼相信你是誰](handout.md)（課堂以 logon 示範）。用 A2 加入的同一個 CyLab 教室帳號，完成平台上的 A4 作業：

- **Old Sessions**
- **Crack the Gate 1**
- **Password Profiler**（題目提示會指向密碼字典產生工具 CUPP，需要 Python 3）

## 繳交格式

- 文件格式：作業區內容欄填寫，不需附件。
- 文字說明：數字列點回答。
- AI 限制：可詢問原理、討論實作，但繳交的是自己理解後的內容而非原始回應。

## 作業要求

CyLab 加入教室的帳號名稱（用來確認作答情況），並針對三題各回答：

1. Old Sessions
   - 你是怎麼拿到管理員身分的？用了哪些操作？
   - 一串 session ID 為什麼就能代表一個人？伺服器該怎麼限制它？
2. Crack the Gate 1
   - 後門藏在哪裡、你怎麼把它送出去？
   - 「只有開發者知道的後門」為什麼不算一種認證？
3. Password Profiler
   - 你用了目標的哪些資料產生候選密碼？
   - 密碼存成雜湊，為什麼還是被猜中了？

## 額外加分（選做）

- No FA - 這題有密碼也有雙因素驗證。說明你怎麼通過這兩關，以及這個網站的雙因素驗證為什麼沒有發揮作用。
