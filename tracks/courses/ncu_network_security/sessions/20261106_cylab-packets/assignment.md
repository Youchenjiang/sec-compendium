# A4 - Cylab Packets

> 2026-11-06 發布。對應技能階梯 M3（明文流量與竊聽），選題與理解問題見 [`ncu_cylab_challenge_selection.md`](../../../ncu_cylab_challenge_selection.md)。期限、成績比重與 CyLab 作業連結以 eeclass 作業頁為準。

## 前置作業

在 [CyLab 平台](https://learn.cylabacademy.org/) 用 A2 加入的同一個教室帳號，完成平台上的 A4 作業。需要安裝 [Wireshark](https://www.wireshark.org/download.html)。

## 繳交格式

- 文件格式：作業區內容欄填寫，不需附件。
- 文字說明：數字列點回答。
- AI 限制：可詢問原理、討論實作，但繳交的是自己理解後的內容而非原始回應。

## 作業要求

CyLab 加入教室的帳號名稱（用來確認作答情況），並回答：

1. Packets Primer - flag 是「看」到的還是「解密」到的？這代表這段流量受保護了嗎？
2. Ph4nt0m 1ntrud3r - 封包裡的字串是 base64，攻擊者這樣傳，有讓旁觀的人看不到內容嗎？
3. shark on wire 1 - 為什麼光看單一封包不夠，要追蹤整條 stream？

## 額外加分（選做）

- Wireshark doo dooo do doo... - 你在 HTTP 回應裡看到的那串字還不是 flag，你怎麼判斷它被做了什麼處理？
