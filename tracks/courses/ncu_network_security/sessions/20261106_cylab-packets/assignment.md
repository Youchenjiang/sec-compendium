# A4 - Cylab Packets

> 2026-11-06 發布。對應技能階梯 M3（明文流量與竊聽），選題與理解問題見 [`ncu_cylab_challenge_selection.md`](../../../ncu_cylab_challenge_selection.md)。期限、成績比重與 CyLab 作業連結以 eeclass 作業頁為準。

## 前置作業

參考講義：[從封包裡讀出別人的對話](handout.md)（課堂以 Packets Primer 示範）。用 A2 加入的同一個 CyLab 教室帳號，完成平台上的 A4 作業：

- **Ph4nt0m 1ntrud3r**
- **shark on wire 1**

## 繳交格式

- 文件格式：作業區內容欄填寫，不需附件。
- 文字說明：數字列點回答。
- AI 限制：可詢問原理、討論實作，但繳交的是自己理解後的內容而非原始回應。

## 作業要求

CyLab 加入教室的帳號名稱（用來確認作答情況），並針對兩題各回答：

1. Ph4nt0m 1ntrud3r
   - 你用了哪些過濾條件或操作，把 flag 所在的封包挑出來、排好順序？
   - 封包裡的字串是 base64，攻擊者這樣傳，有讓旁觀的人看不到內容嗎？
2. shark on wire 1
   - flag 在哪一條 stream？你是怎麼找到那一條的？
   - 為什麼光看單一封包不夠，要追蹤整條 stream？

## 額外加分（選做）

- Eavesdrop - 這份錄製檔裡有一段聊天和一次檔案傳輸，檔案本身是加密的。說明你從哪裡得到解密需要的資訊，以及「檔案有加密」為什麼還是沒擋住竊聽者。
