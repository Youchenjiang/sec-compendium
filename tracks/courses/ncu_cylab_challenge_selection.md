# 🎯 中央資管《電腦網路安全》× picoCTF 逐課選題清單

> **用途**：把 [`ncu_cylab_curriculum_mapping_matrix.md`](ncu_cylab_curriculum_mapping_matrix.md) 的「方向」落到**具體題目**。配合講義逐課挑題。
>
> **定位**：這份是「**關卡解題**」軌——CyLab picoCTF，一題一技能、拿 flag。另一條「**情境演練**」軌（CDX 靶場，Nessus／Suricata 那種掃描與偵測實作，交報告不拿 flag）性質不同，教材在 `Common/Slide/workshops/`（攻擊側 `202610_CDX_CVE-2021-41773`、防守側 `202610_CDX_CVE-2021-41773-Blue`），兩軌互補。
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

### 6. 第一次上手（帶練 + 練習）
導論最後實際解題，把平台和核心工具摸過一遍：老師先帶著示範三個工具，再讓學員用同樣的工具自己練三題。這些**不是講義內容**，純粹是「怎麼在 CyLab 解題、怎麼用瀏覽器與 CyberChef」的手感。

**帶練（老師課堂示範，各示範一個工具）**

| 題名 | 示範的工具／動作 | 連結 |
| :-- | :-- | :-- |
| **Inspect HTML** | devtools／看網頁原始碼 | [library](https://learn.cylabacademy.org/library?search=Inspect%20HTML) |
| **Bases** | CyberChef 解 base64 | [library](https://learn.cylabacademy.org/library?search=Bases) |
| **Cookie Monster Secret Recipe** | 看 cookie ＋ 解碼 | [library](https://learn.cylabacademy.org/library?search=Cookie%20Monster%20Secret%20Recipe) |

**學員練習（自己做，重用剛示範的工具）**

| 題名 | 練的工具 | 連結 |
| :-- | :-- | :-- |
| **Insp3ct0r** | 看原始碼：flag 拆在 HTML/CSS/JS 三處 | [library](https://learn.cylabacademy.org/library?search=Insp3ct0r) |
| **Unminify** | 看原始碼：還原被壓縮的前端碼 | [library](https://learn.cylabacademy.org/library?search=Unminify) |
| **WebDecode** | 解碼：解元素屬性裡的編碼 | [library](https://learn.cylabacademy.org/library?search=WebDecode) |

🧠 **理解問題（解完就答）**

1. **Bases** - 你把它還原時，需要任何「別人沒有的秘密（密碼／金鑰）」嗎？
2. **Inspect HTML** - 畫面上沒顯示這段 flag，它是怎麼來到你瀏覽器裡的？
3. **Insp3ct0r** - flag 有一段在 CSS、一段在 JS，為什麼這些檔你也打得開？
4. **Unminify** - 同一頁，Ctrl+U 的原始碼和 devtools 的 Elements 為什麼長得差很多？
5. **WebDecode** - 開發者把 flag 編碼再藏，比起直接藏，多防住了想看的人什麼？
6. **Cookie Monster** - 這個裝著秘密的 cookie，存在誰的電腦上、誰能改它？

> **工具**：瀏覽器（devtools / view-source）＋ CyberChef。解碼時注意 CyberChef「**From Binary**（當位元解讀）vs **To Decimal**（逐字元取 ASCII）」的差別——`'0'`=48、`'1'`=49 是常見的踩坑點。

---

## 📘 Lesson 1 — What Is InfoSec?

> **定位**：對照講義本體（`Handout/NOW/Lesson 1`）。兩個 Critical Skill：(1.1) 用發展史定義資安；(1.2) 資安是「流程」，不是「單點產品」。

### 講義重點與配題

講義用安全發展史定義資安：實體 → 通訊（Caesar、Enigma）→ 輻射（TEMPEST）→ 電腦（BLP、Orange Book）→ 網路 → 資訊；接著逐一點出每種「產品」的盲點，結論是沒有單一產品足夠。

能落到 picoCTF 題的只有兩處；其餘（BLP、TEMPEST、Orange Book）屬純觀念，講義講授、不配題。

| 講義點 | 題名 | 難度 | 連結 |
| :-- | :-- | :--: | :-- |
| 通訊安全史：Caesar 位移密碼 | `62` **13**（ROT13） | Easy | [library](https://learn.cylabacademy.org/library?search=13) |
| 存取控制擋不住弱密碼（講義 §1.2 原話） | `245` **PW Crack 1** | Easy | [library](https://learn.cylabacademy.org/library?search=PW%20Crack%201) |

課後自選：`144` **Mod 26**（另一種位移）、`246` **PW Crack 2**。

### 每題三格（觀念 / 基本功 / 接續）

- **13（ROT13）**
  - 觀念：最早的通訊「加密」只是字母位移，規則一旦知道就形同沒加密
  - 基本功：辨識並還原位移／代換密碼
  - 接續：**中**（古典密碼打底；深入在 L12，真實系統少見）
- **PW Crack 1**
  - 觀念：講義 §1.2 明寫「存取控制擋不住弱密碼」——登入檢查再嚴，弱密碼一破就形同虛設
  - 基本功：對弱密碼做字典比對
  - 接續：**高**（弱密碼是真實最常見破口；情境演練裡 Nessus 常報弱憑證）

### 🧠 理解問題（解完就答）

1. **13** - 你沒用任何密碼就把它還原了，那它跟「要金鑰才能解」的加密差在哪？
2. **PW Crack 1** - 系統明明有「登入檢查」這道存取控制，為什麼一支弱密碼就讓它形同虛設？

### 這一課真正的重點：流程 ≠ 產品（直接接情境演練）

講義 §1.2 逐一點名產品盲點，其中兩句，正好就是情境演練那兩個工具的極限：

- 「**弱點掃描**不會抓到已在系統內的入侵者」→ Nessus 的極限
- 「**入侵偵測**不會抓到有合法權限的越權使用者」→ Suricata／IDS 的極限

所以做完情境演練（Nessus 掃、Suricata 偵測），回到 L1 這句話，學生就親身驗證了「沒有單一產品足夠、資安是流程」。**L1 的論點本身就是關卡解題與情境演練的橋。**

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
| `67` | Bases | General Skills | L0 | ✅ 帶練 |
| `275` | Inspect HTML | Web | L0 | ✅ 帶練 |
| `18` | Insp3ct0r | Web | L0 | ✅ 練習 |
| `426` | Unminify | Web | L0 | ✅ 練習 |
| `427` | WebDecode | Web | L0 | ✅ 練習 |
| `469` | Cookie Monster Secret Recipe | Web | L0 | ✅ 帶練 |
| `62` | 13（ROT13） | Cryptography | L1 | ✅ 已用（Caesar 史） |
| `245` | PW Crack 1 | General Skills | L1 | ✅ 已用（弱密碼破存取控制） |
| `144` | Mod 26 | Cryptography | L1 | ✅ 自選 |
| `246` | PW Crack 2 | General Skills | L1 | ✅ 自選 |
| 自建 | ftp-cleartext | wireshark_labs | L2 | ✅ 已用 |
| 自建 | http-basic | wireshark_labs | L2 | ✅ 已用 |
| `286` | Packets Primer | Forensics | L2 | ✅ 已用 |
| `30` | shark on wire 1 | Forensics | L2 | ✅ 已用 |
| `4` | where are the robots | Web | L3 | 🔒 預留（偵察） |
| `161` | Scavenger Hunt | Web | L3 | 🔒 預留（偵察示範） |
| `132` | GET aHEAD | Web | L10 | 🔒 預留（方法繞過） |
| `173` | Cookies | Web | L4? | ⏳ 候選（竄改/信任邊界，排 L4 時定） |

> **重疊提醒**：PW Crack（`245`/`246`）在 L1 是「弱密碼破存取控制」的角度；L12 的弱密碼題請改用**雜湊破解**角度的題（如 `475` hashcrack），別重用 `245`/`246`。

<!-- 後續 Lesson 3~13 待逐課定稿後續補；每定一課同步更新分配帳本 -->
