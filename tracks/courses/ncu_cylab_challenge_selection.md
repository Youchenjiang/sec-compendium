# 🎯 中央資管《電腦網路安全》× picoCTF 逐課選題清單

> **用途**：把 [`ncu_cylab_curriculum_mapping_matrix.md`](ncu_cylab_curriculum_mapping_matrix.md) 的「方向」落到**具體題目**。配合講義逐課挑題。
>
> **定位**：這份是「**關卡解題**」軌——CyLab picoCTF，一題一技能、拿 flag。另一條「**情境演練**」軌（CDX 靶場，Nessus／Suricata 那種掃描與偵測實作，交報告不拿 flag）性質不同，放在 `tracks/lab/`，兩軌互補。
>
> **選題原則**
> 1. **難度靠脈絡換取**：Easy 進場暖身；一課鋪好「奠基示範 → 練習」後，可用 **Medium 當實戰 capstone** 收尾（踩前面的階梯上去）。要避開的是 **Hard 與重工具**，不是 Medium 本身。
> 2. **依賴順序排列**：題目依「先會的技能 → 疊上去的技能」排成一條學習鏈，而非平行清單。
> 3. **機制 → 情境**：先用操練題建立手感，再用有「受害系統」的情境題打破迷思（才有沉浸感）。
> 4. **不跨課重複**：一旦題目需要別課的核心觀念（如金鑰→L12、驗證繞過→L4），就留給那一課。
> 5. **flag ≠ 學習成果**：每題配一個「🧠 理解問題」（問「為什麼／怎麼回事」，對準該題要破的迷思），解完就答。flag 只當「做過」的門票，成績看能否**講清機制**。這也是對「貼 GPT 拿 flag 卻沒懂」的防線——聚會時口頭答最有效；用 per-player 動態 flag 的課（如 wireshark_labs）再加一層天然防抄。
>
> **題數來源**：`security/practice/challenges/platforms/cylab_picoctf/cylab_all_challenges_2026-08-08.csv`（2026-08-08 快照）。
> 連結為 cylab 題庫搜尋入口 `https://learn.cylabacademy.org/library?search=<題名>`。

---

## 🧭 Lesson 0 — 導論（開課前先講）

### 1. 什麼是 CTF
每題藏一個 flag（像 `picoCTF{...}`，本站是 `academy{...}`），想辦法把它弄出來提交，就算解開。題目分 Web、Forensics、Crypto、Reverse、Pwn、General 幾類，本課主要碰前幾類。

### 2. 為何用 CTF
自己動手做，不是只在台下聽。題目都在靶機上，合法也安全。真正的攻擊其實是一堆小技巧堆出來的，CTF 就是一題一題把這些基礎補起來。

### 3. 難度定位（上週 CVE、這週 base64）
上週 CVE-2021-41773 是帶你們看一次完整的攻擊，重點在動機。picoCTF 這邊是從頭累積基礎：編碼、看原始碼、cookie、封包這些。所以一開始題目簡單是正常的，看老師做過，跟自己做得出來，差很遠。

### 4. CyLab Academy
網站是 learn.cylabacademy.org，免費。流程是註冊帳號、用老師給的代碼加入班級、到 Challenge Library 找題。flag 格式 picoCTF 原題是 `picoCTF{...}`，我們自建的是 `academy{...}`，提交前看清楚。班級註冊的細節老師上課再講。

### 5. 評量
交 flag 只代表你弄出來了，不代表懂，所以每題還要回答一個理解問題。練習題在聚會現場做、講給大家聽。像 wireshark 那種自建題，每個人的 flag 都不一樣，抄別人的沒用。

---

## 📘 Lesson 1 — What Is InfoSec?

> **定位**：承 Lesson 0 §3，本課從基礎起步。L1 先破兩個最常見的入門迷思。

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

### 🧠 理解問題（解完就答——收 flag 之外，收「懂了沒」）

> 每題一問，問「為什麼／怎麼回事」，對準該題要破的迷思；flag 證明「做到」，這題證明「懂了」，兩者分開收。

1. **Bases** - 你把它還原時，需要任何「別人沒有的秘密（密碼／金鑰）」嗎？
2. **Inspect HTML** - 畫面上沒顯示這段 flag，它是怎麼來到你瀏覽器裡的？
3. **Insp3ct0r** - flag 有一段在 CSS、一段在 JS，為什麼這些檔你也打得開？
4. **Unminify** - 同一頁，Ctrl+U 的原始碼和 devtools 的 Elements 為什麼長得差很多？
5. **WebDecode** - 開發者把 flag 編碼再藏，比起直接藏，多防住了想看的人什麼？
6. **Cookie Monster** - 這個裝著秘密的 cookie，存在誰的電腦上、誰能改它？

> **工具**：瀏覽器（devtools / view-source）＋ CyberChef。解碼時注意 CyberChef「**From Binary**（當位元解讀）vs **To Decimal**（逐字元取 ASCII）」的差別——`'0'`=48、`'1'`=49 是常見的踩坑點。
>
> **刻意留給後面課**：`4` where are the robots（/robots.txt）→ L3 偵察；cookie/屬性若進一步要「偽造身分、繞過驗證」→ L4。

---

## 📗 Lesson 2 — Types of Attacks

**對應攻擊型態**：Access Attacks（Snooping 窺探 / Eavesdropping 竊聽）、Modification（竄改）、DoS & Repudiation。
動手題**聚焦工具一致、可爬升的「竊聽」一條線**；其餘型態用講義講概念，實作留到工具/觀念更對的課：**竄改 → L4（信任邊界）、窺探 → L3（Web 偵察）**。這樣不占用別課的 Web Easy 池（見分配帳本）。

### 選題邏輯（一個工具一條線 + 脈絡換難度）

L2 的新技術是 **Wireshark Follow TCP Stream**。全程同一工具，難度 Easy → Easy → Medium 自然爬升：

```
🎓 奠基示範（Easy・自建）  ftp-cleartext  →  教 Follow Stream，明文 PASS 直接讀到
🔁 練習（Easy・自建）       http-basic     →  同招 + base64 解碼（Authorization: Basic 不是加密，呼應 L1）
🏁 實戰 capstone（Medium）  286 → 30       →  第一次碰真正的 picoCTF 封包題；前面已鋪好脈絡，踩得上去
```

> **為什麼含 Medium**：依原則 1「難度靠脈絡換取」。picoCTF 的封包題全是 Medium，與其排斥，不如用自建的 Easy 當上山階梯，爬到真正的 picoCTF 封包題。工具全程是 Wireshark，不中途換工具。

### 題目清單

| 階段 | ID / 來源 | 題名 | 分類 | 難度 | 角色 / 教學點 | 連結 |
| :--: | :-- | :-- | :-- | :--: | :-- | :-- |
| 奠基 | 自建 | **ftp-cleartext** | wireshark_labs | Easy | 教 Wireshark Follow TCP Stream，明文密碼裸奔 | [plugin](../../ctfd/plugins/wireshark_labs/) |
| 練習 | 自建 | **http-basic** | wireshark_labs | Easy | 同招 + base64 解碼；`Authorization: Basic` 不是加密（呼應 L1） | [plugin](../../ctfd/plugins/wireshark_labs/) |
| capstone | `286` | **Packets Primer** | Forensics | Medium | 第一題真 picoCTF 封包：開 pcap、讀 payload | [library](https://learn.cylabacademy.org/library?search=Packets%20Primer) |
| capstone | `30` | **shark on wire 1** | Forensics | Medium | 跟隨 stream，把拆散的 flag 拼回來 | [library](https://learn.cylabacademy.org/library?search=shark%20on%20wire%201) |

### 🧠 理解問題（解完就答）

1. **ftp-cleartext** - 你不是這段連線的收發雙方，為什麼還能看到那組密碼？
2. **http-basic** - `Authorization: Basic` 裡的帳密是加密過的，還是只是換個樣子？
3. **Packets Primer** - flag 是從封包裡「看」到的，還是「解密」出來的？這代表這段流量受保護了嗎？
4. **shark on wire 1** - 為什麼光看單一封包不夠，要「追蹤整條 stream」才拼得出 flag？

> **工具**：Wireshark（Follow TCP Stream）。**選配**：`telnet-echo`（自建，重組無回顯密碼）。
> **刻意不配題**：DoS & Repudiation（picoCTF 無對應題型，純講義）。
> **刻意外移**：竄改（cookie）→ L4；窺探（公開路徑）→ L3。避免跨工具孤兒，也不占別課的 Web Easy 名額。

---

## 📒 題目分配帳本（避免跨課重複搶題）

> **Web Easy 僅 20 題**，須跨 L1 / L3 / L4 / L10 共用，故逐課登記，防止重複或占位。（自建 wireshark_labs 不佔此池。）

| ID / 來源 | 題名 | 分類 | 歸屬 | 狀態 |
| :-- | :-- | :-- | :--: | :-- |
| `67` | Bases | General Skills | L1 | ✅ 已用 |
| `275` | Inspect HTML | Web | L1 | ✅ 已用 |
| `18` | Insp3ct0r | Web | L1 | ✅ 已用 |
| `426` | Unminify | Web | L1 | ✅ 已用 |
| `427` | WebDecode | Web | L1 | ✅ 已用 |
| `469` | Cookie Monster Secret Recipe | Web | L1 | ✅ 已用 |
| 自建 | ftp-cleartext | wireshark_labs | L2 | ✅ 已用 |
| 自建 | http-basic | wireshark_labs | L2 | ✅ 已用 |
| `286` | Packets Primer | Forensics | L2 | ✅ 已用 |
| `30` | shark on wire 1 | Forensics | L2 | ✅ 已用 |
| `4` | where are the robots | Web | L3 | 🔒 預留（偵察） |
| `161` | Scavenger Hunt | Web | L3 | 🔒 預留（偵察示範） |
| `132` | GET aHEAD | Web | L10 | 🔒 預留（方法繞過） |
| `173` | Cookies | Web | L4? | ⏳ 候選（竄改/信任邊界，排 L4 時定） |

<!-- 後續 Lesson 3~13 待逐課定稿後續補；每定一課同步更新分配帳本 -->
