# A4 - Cylab Auth

> 2026-11-06 發布。對應技能階梯 M4（認證與憑證），選題與理解問題見 [`ncu_cylab_challenge_selection.md`](../../../ncu_cylab_challenge_selection.md)。期限、成績比重與 CyLab 作業連結以 eeclass 作業頁為準。

## 前置作業

參考講義：[伺服器憑什麼相信你是誰](handout.md)（課堂以 logon 示範）。用 A2 加入的同一個 CyLab 教室帳號，完成平台上的 A4 作業（三題皆為 Medium）：

- **Most Cookies**
- **Crack the Gate 2**
- **No FA**

需要 Python 3，並安裝 `flask-unsign` 與 `requests`（`pip install flask-unsign requests`）。

## 繳交格式

- 文件格式：作業區內容欄填寫，不需附件。
- 文字說明：數字列點回答；有寫程式或下指令的，附上你實際用的程式碼或指令。
- AI 限制：可詢問原理、討論實作，但繳交的是自己理解後的內容而非原始回應。

## 作業要求

CyLab 加入教室的帳號名稱（用來確認作答情況），並針對三題各回答：

1. Most Cookies
   - 你的候選金鑰清單從哪裡來？找到的金鑰是什麼、你把 cookie 改成了什麼內容？
   - cookie 明明有簽章，為什麼你還是能偽造？簽章的安全靠的是什麼？
2. Crack the Gate 2
   - 附上你用來嘗試密碼的程式，說明每次請求改了什麼。
   - 伺服器用什麼判斷「同一個人一直猜錯」？為什麼這個依據擋不住你？
3. No FA
   - 你怎麼拿到密碼、又怎麼通過雙因素驗證？
   - 密碼雜湊為什麼查得到原文？這個網站的雙因素驗證為什麼沒有發揮作用？

## 額外加分（選做）

- JAuth - 你把 token 改成了什麼？伺服器為什麼會接受一個沒有簽章的 token？
