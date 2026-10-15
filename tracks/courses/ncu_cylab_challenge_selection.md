# 🎯 中央資管《電腦網路安全》× picoCTF 逐課選題清單

> **用途**：把 [`ncu_cylab_curriculum_mapping_matrix.md`](ncu_cylab_curriculum_mapping_matrix.md) 的「方向」落到**具體題目**。配合講義逐課挑題。
>
> **選題原則**
> 1. **Easy 優先**：以 cylab 難度欄位（`1=Easy`）為準，確保「不太難」。
> 2. **依賴順序排列**：題目依「先會的技能 → 疊上去的技能」排成一條學習鏈，而非平行清單。
> 3. **機制 → 情境**：先用操練題建立手感，再用有「受害系統」的情境題打破迷思（才有沉浸感）。
> 4. **不跨課重複**：一旦題目需要別課的核心觀念（如金鑰→L12、驗證繞過→L4），就留給那一課。
>
> **題數來源**：`security/practice/challenges/platforms/cylab_picoctf/cylab_all_challenges_2026-08-08.csv`（2026-08-08 快照）。
> 連結為 cylab 題庫搜尋入口 `https://learn.cylabacademy.org/library?search=<題名>`。

---

## 📘 Lesson 1 — What Is InfoSec?

**對應迷思**：① 編碼 ≠ 加密（Obscurity 之一）｜② 隱藏 ≠ 安全（Obscurity ≠ Security）
**BLP/MLS 多層次存取模型** 屬純理論，picoCTF 無對應題型，以講義與案例講授，不配題。

### 選題邏輯（依賴順序，非平行兩軸）

這六題是一條**依賴鏈**：要先會「找」（看原始碼）＋會「解」（decode 機制），才解得動最後的情境 capstone。

```
階段 1  打底（各自獨立）
  ├─ 67  Bases         →  decode 機制（decode ≠ decrypt）
  └─ 275 Inspect HTML  →  看網頁原始碼

階段 2  隱藏 ≠ 安全（疊在「看原始碼」上）
  ├─ 18  Insp3ct0r     →  flag 拆在 HTML/CSS/JS 三處，多處檢視
  └─ 426 Unminify      →  還原被壓縮/混淆的前端碼

階段 3  編碼 ≠ 加密・情境 capstone（同時需要 decode + inspect）
  ├─ 427 WebDecode           →  inspect 出編碼屬性 → 解開
  └─ 469 Cookie Monster      →  inspect 出 base64 cookie → 解開
```

> **為什麼這樣排**：`469`/`427` 不是獨立的解碼題，而是「在網頁裡找到一段編碼過的東西再解開」——要先具備 `275`/`18` 的 inspect 能力與 `67` 的 decode 手感。它們是 Lesson 1 的收尾高潮，一題同時打中「藏了也沒用 + 編碼不是加密」兩個迷思。
>
> 隱藏軸（`275`/`18`/`426`）天生自帶情境——「粗心的開發者以為藏進原始碼就沒人看」，那個開發者就是受害主體；編碼軸缺的正是這個受害者，所以從 Web 的 cookie/屬性把情境補回來。

### 題目清單

| 階段 | ID | 題名 | 分類 | 難度 | 角色 / 教學點 | 連結 |
| :--: | :-- | :-- | :-- | :--: | :-- | :-- |
| 1 | `67` | **Bases** | General Skills | Easy | decode 機制：Base64，釐清「編碼可逆、不是加密」 | [library](https://learn.cylabacademy.org/library?search=Bases) |
| 1 | `275` | **Inspect HTML** | Web | Easy | 看原始碼：單頁 view-source | [library](https://learn.cylabacademy.org/library?search=Inspect%20HTML) |
| 2 | `18` | **Insp3ct0r** | Web | Easy | 隱藏≠安全：flag 拆在 HTML/CSS/JS 三處 | [library](https://learn.cylabacademy.org/library?search=Insp3ct0r) |
| 2 | `426` | **Unminify** | Web | Easy | 隱藏≠安全：還原被壓縮的前端碼 | [library](https://learn.cylabacademy.org/library?search=Unminify) |
| 3 | `427` | **WebDecode** | Web | Easy | capstone：編碼藏在元素屬性，inspect → decode | [library](https://learn.cylabacademy.org/library?search=WebDecode) |
| 3 | `469` | **Cookie Monster Secret Recipe** | Web | Easy | capstone：base64 cookie 當保護，inspect → decode | [library](https://learn.cylabacademy.org/library?search=Cookie%20Monster%20Secret%20Recipe) |

> **工具**：瀏覽器（devtools / view-source）＋ CyberChef。解碼時注意 CyberChef「**From Binary**（當位元解讀）vs **To Decimal**（逐字元取 ASCII）」的差別——`'0'`=48、`'1'`=49 是常見的踩坑點。
>
> **刻意留給後面課**：`4` where are the robots（/robots.txt）→ L3 偵察；cookie/屬性若進一步要「偽造身分、繞過驗證」→ L4。

<!-- 後續 Lesson 2~13 待逐課定稿後續補 -->
