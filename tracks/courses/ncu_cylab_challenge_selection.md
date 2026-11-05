# 🎯 中央資管《電腦網路安全》× picoCTF 技能階梯選題

> **用途**：把 picoCTF 題排成一條**技能階梯（M0~M7）**，一階建在前一階上。講義（Lesson）降成**對照欄**，給老師排課對應用。
>
> **骨架為何是技能、不是講義 Lesson**：講義是概念／管理導向的課，硬把動手題塞進 Lesson 1~13 會一直跑偏（半數課沒題配、框架被污染、技能接不起來）。技能軸才會真的疊起來。講義的對齊與偏差修正另見 [`ncu_cylab_curriculum_mapping_matrix.md`](ncu_cylab_curriculum_mapping_matrix.md)。
>
> **定位（兩軌）**：這份是「**關卡解題**」軌——CyLab picoCTF，一題一技能、拿 flag。另一條「**情境演練**」軌（CDX 靶場，Nessus／Suricata 掃描與偵測，交報告不拿 flag）在 [`ncu_network_security/`](ncu_network_security/)（攻擊側 `sessions/20261002_attack-cve-2021-41773`、防守側備選 `alt-materials/nessus-suricata`）。兩軌互補。
>
> **選題原則**
> 1. **難度靠脈絡換取**：Easy 進場暖身；一階鋪好「帶練 → 練習」後，可用 **Medium 當實戰 capstone** 收尾。要避開的是 **Hard 與重工具**，不是 Medium 本身。
> 2. **依賴順序**：整條階梯就是「先會的技能 → 疊上去的技能」，M0→M7 不跳階。
> 3. **帶練 → 練習**：每階老師先示範，學員再用同工具自己練。
> 4. **不跨階重複**：一題的技能屬於哪一階，就在那階出現；別的階要用同概念，換不同題。
> 5. **flag ≠ 學習成果**：每題配一個「🧠 理解問題」，解完就答。flag 只當「做過」的門票，成績看能否講清機制；這也是對「貼 GPT 拿 flag 卻沒懂」的防線。自建題（wireshark_labs）每人 flag 不同，再加一層防抄。
>
> **題數／難度來源**：`security/practice/challenges/platforms/cylab_picoctf/cylab_all_challenges_2026-08-08.csv`（2026-08-08 快照）。連結為 `https://learn.cylabacademy.org/library?search=<題名>`。

---

## 🧭 M0 — 平台與工具上手（導論，不配題）

> 對應講義：導論。第一次上課先講清楚「這是什麼、怎麼開始」，**不解題**，實際解題從 M1 開始。

1. **什麼是 CTF**：每題藏一個 flag（`picoCTF{...}`，本站 `academy{...}`），弄出來提交即解開。題目分 Web、Forensics、Crypto、Reverse、Pwn、General。
2. **為何用 CTF**：自己動手、合法安全的靶機、真實攻擊由小技巧堆成，一階一階補起來。
3. **難度定位（上週 CVE、這週很簡單）**：上週 CVE-2021-41773 是帶你們看一次完整攻擊，重點在動機；這條階梯是從頭累積基礎，一開始簡單是正常的，看老師做過跟自己做得出來差很遠。
4. **CyLab Academy**：learn.cylabacademy.org，免費。註冊 → 用老師給的代碼加入班級 → Challenge Library 找題。flag 格式 `picoCTF{...}`／自建題 `academy{...}`，提交前看清楚。班級細節老師課堂補。
5. **評量**：flag 只代表做出來、不代表懂，每題還要答一個理解問題；練習在聚會現場做、口頭講機制。

---

## 🔡 M1 — 資料表示與編碼

> 對應講義：L12（編碼／表示法）、L1 通訊安全史。｜觀念：編碼可逆、**不是加密**。｜工具：CyberChef。

| 角色 | ID | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `67` | **Bases** | Easy | Base64 解碼 | [library](https://learn.cylabacademy.org/library?search=Bases) |
| 練習 | `710` | **MultiCode** | Easy | 辨識並逐層剝多種編碼 | [library](https://learn.cylabacademy.org/library?search=MultiCode) |

🧠 **理解問題**
1. **Bases** - 你把它還原時，需要任何「別人沒有的秘密（密碼／金鑰）」嗎？
2. **MultiCode** - 你怎麼判斷它是哪一種編碼、該用哪個 operation？

> **工具坑**：CyberChef「**From Binary**（當位元解讀）vs **To Decimal**（逐字元取 ASCII）」不一樣——`'0'`=48、`'1'`=49 是常見踩坑。

---

## 🔍 M2 — 前端暴露與 obscurity

> 對應講義：L2 Snooping（「翻看檔案找有趣的東西」）、L3 recon。｜觀念：client 端一定看得到、隱藏 ≠ 安全。｜工具：瀏覽器 devtools / view-source。

| 角色 | ID | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `275` | **Inspect HTML** | Easy | devtools／看原始碼 | [library](https://learn.cylabacademy.org/library?search=Inspect%20HTML) |
| 練習 | `18` | **Insp3ct0r** | Easy | flag 拆在 HTML/CSS/JS 三處 | [library](https://learn.cylabacademy.org/library?search=Insp3ct0r) |
| 練習 | `426` | **Unminify** | Easy | 還原被壓縮的前端碼 | [library](https://learn.cylabacademy.org/library?search=Unminify) |
| 練習（接 M1） | `427` | **WebDecode** | Easy | inspect 出編碼屬性 → 解開 | [library](https://learn.cylabacademy.org/library?search=WebDecode) |
| 練習（接 M1） | `469` | **Cookie Monster Secret Recipe** | Easy | inspect 出 base64 cookie → 解開 | [library](https://learn.cylabacademy.org/library?search=Cookie%20Monster%20Secret%20Recipe) |

🧠 **理解問題**
1. **Inspect HTML** - 畫面上沒顯示這段 flag，它是怎麼來到你瀏覽器裡的？
2. **Insp3ct0r** - flag 有一段在 CSS、一段在 JS，為什麼這些檔你也打得開？
3. **Unminify** - 同一頁，Ctrl+U 的原始碼和 devtools 的 Elements 為什麼長得差很多？
4. **WebDecode** - 開發者把 flag 編碼再藏，比起直接藏，多防住了想看的人什麼？
5. **Cookie Monster** - 這個裝著秘密的 cookie，存在誰的電腦上、誰能改它？

> WebDecode／Cookie Monster 同時要 M1 的解碼 + M2 的 inspect，是這階的收尾。

---

## 📡 M3 — 明文流量與竊聽

> 對應講義：L2 Eavesdropping、L13 入侵偵測。｜工具：Wireshark（Follow TCP Stream）。｜接情境演練：Suricata 偵測。

| 角色 | ID／來源 | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | 自建 | **ftp-cleartext** | Easy | Follow Stream，明文密碼裸奔 | [plugin](../../ctfd/plugins/wireshark_labs/) |
| 練習 | 自建 | **http-basic** | Easy | 同招 + base64 解碼（`Authorization: Basic` 不是加密，呼應 M1） | [plugin](../../ctfd/plugins/wireshark_labs/) |
| capstone | `286` | **Packets Primer** | Medium | 第一題真 picoCTF 封包：開 pcap、讀 payload | [library](https://learn.cylabacademy.org/library?search=Packets%20Primer) |
| capstone | `30` | **shark on wire 1** | Medium | 跟隨 stream，把拆散的 flag 拼回來 | [library](https://learn.cylabacademy.org/library?search=shark%20on%20wire%201) |

🧠 **理解問題**
1. **ftp-cleartext** - 你不是這段連線的收發雙方，為什麼還能看到那組密碼？
2. **http-basic** - `Authorization: Basic` 裡的帳密是加密過的，還是只是換個樣子？
3. **Packets Primer** - flag 是「看」到的還是「解密」到的？這代表這段流量受保護了嗎？
4. **shark on wire 1** - 為什麼光看單一封包不夠，要追蹤整條 stream？

> 選配：`telnet-echo`（自建，重組無回顯密碼）。DoS／Repudiation 無對應題型，講義帶過。

---

## 🔑 M4 — 認證與弱憑證

> 對應講義：L4 安全服務（Accountability 下的認證）、L1 存取控制。｜觀念：存取控制擋不住弱密碼、伺服器別盲信 client 送回來的東西。

| 角色 | ID | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `245` | **PW Crack 1** | Easy | 弱密碼字典比對 | [library](https://learn.cylabacademy.org/library?search=PW%20Crack%201) |
| 練習 | `246` | **PW Crack 2** | Easy | 同招，多一點變化 | [library](https://learn.cylabacademy.org/library?search=PW%20Crack%202) |
| 練習 | `173` | **Cookies** | Easy | 改 cookie 值竄改伺服器行為 | [library](https://learn.cylabacademy.org/library?search=Cookies) |

🧠 **理解問題**
1. **PW Crack 1** - 系統明明有登入檢查，為什麼一支弱密碼就讓它形同虛設？
2. **Cookies** - 你改了瀏覽器裡的 cookie，伺服器為什麼會信你改過的值？

> 弱密碼的**雜湊**深入在 M6；這裡只做「弱密碼破存取控制」的角度。

---

## 🧩 M5 — 輸入信任與注入

> 對應講義：無（紅隊補充）。｜與情境演練的分工：**路徑穿越已經由情境演練（CVE-2021-41773 workshop）做掉了，M5 不重複**；這階補的是那個 CVE 沒碰到的另一類「伺服器盲信輸入」破口——**注入**。｜觀念：伺服器把你送的輸入當成「程式／查詢」而非「資料」。
>
> ⚠️ Easy 很少，多為 Medium。依原則 1，踩前面四階上去。

| 角色 | ID | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `492` | **SSTI1** | Easy | 你送的字串被當模板「程式」執行（SSTI） | [library](https://learn.cylabacademy.org/library?search=SSTI1) |
| capstone | `304` | **SQLiLite** | Medium | SQL 注入：你的輸入改寫了資料庫查詢 | [library](https://learn.cylabacademy.org/library?search=SQLiLite) |

🧠 **理解問題**
1. **SSTI1** - 你送出去的字串，為什麼被伺服器當成「程式」執行，而不是「資料」？
2. **SQLiLite** - 你在輸入框打的東西，為什麼能改變資料庫查詢的意思？

> 命令注入、反序列化等其他注入在紅隊 playbook，想深入再看。路徑穿越（本 CVE 的命門）走情境演練，不在此重複。

---

## 🔐 M6 — 雜湊與密碼學

> 對應講義：L12。｜觀念：古典密碼（位移／代換）規則一旦知道就形同沒加密；雜湊單向、只能查表反推不能「解開」。｜工具：CyberChef／線上雜湊查詢。排除 RSA 數論與長篇手動頻率分析。

**古典密碼（位移／代換）**

| 角色 | ID | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `62` | **13** | Easy | ROT13 位移 | [library](https://learn.cylabacademy.org/library?search=13) |
| 練習 | `144` | **Mod 26** | Easy | 另一種位移 | [library](https://learn.cylabacademy.org/library?search=Mod%2026) |
| 練習 | `68` | **The Numbers** | Easy | 字母↔數字代換（A1Z26） | [library](https://learn.cylabacademy.org/library?search=The%20Numbers) |

**雜湊**

| 角色 | ID | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `475` | **hashcrack** | Easy | 用字典／查表反推弱密碼雜湊 | [library](https://learn.cylabacademy.org/library?search=hashcrack) |
| 選配 | `243` | **HashingJobApp** | Easy | 算雜湊、體會單向 | [library](https://learn.cylabacademy.org/library?search=HashingJobApp) |

🧠 **理解問題**
1. **13 / Mod 26** - 你沒有任何金鑰就把它還原了，為什麼位移密碼這麼容易破？
2. **hashcrack** - 雜湊號稱「不可逆」，那你是怎麼「還原」出原文的？（提示：你不是解開它，是猜中）

---

## 🧷 M7 — 鑑識與逆向基礎

> 對應講義：L3 惡意碼（硬編碼特徵字串）、forensics。｜觀念：祕密常被硬編碼在檔案／程式裡，靜態就能抽出來。｜工具：`strings`、`exiftool`。排除記憶體 dump、Ghidra 反組譯。

**靜態字串／中繼資料**

| 角色 | ID | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `37` | **strings it** | Easy | 對檔案跑 `strings` 抽硬編碼字串 | [library](https://learn.cylabacademy.org/library?search=strings%20it) |
| 練習 | `408` | **CanYouSee** | Easy | `exiftool` 看圖片中繼資料 | [library](https://learn.cylabacademy.org/library?search=CanYouSee) |
| 練習 | `186` | **information** | Easy | 中繼資料藏 flag | [library](https://learn.cylabacademy.org/library?search=information) |

**讀簡單程式找密鑰**

| 角色 | ID | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `7` | **vault-door-training** | Easy | 讀簡單 Java 找寫死的密碼 | [library](https://learn.cylabacademy.org/library?search=vault-door-training) |
| 練習 | `104` | **Transformation** | Easy | 讀／逆簡單 Python 轉換 | [library](https://learn.cylabacademy.org/library?search=Transformation) |

🧠 **理解問題**
1. **strings it** - 執行檔是二進位，`strings` 為什麼還能把裡面的文字撈出來？
2. **CanYouSee** - flag 不在圖片「畫面」裡，卻在檔案裡——它藏在哪個部分？
3. **vault-door-training** - 密鑰就寫在原始碼裡，為什麼「把密鑰藏在程式碼裡」本身就不安全？

---

## 📒 題目分配帳本（避免跨階重複搶題）

> **Web Easy 僅 20 題**，跨階共用，逐階登記防重複。自建 wireshark_labs 不佔此池。

| ID／來源 | 題名 | 分類 | 階 | 狀態 | 對應講義 |
| :-- | :-- | :-- | :--: | :-- | :-- |
| `67` | Bases | General Skills | M1 | ✅ 帶練 | L12 |
| `710` | MultiCode | General Skills | M1 | ✅ 練習 | L12 |
| `275` | Inspect HTML | Web | M2 | ✅ 帶練 | L2/L3 |
| `18` | Insp3ct0r | Web | M2 | ✅ 練習 | L2/L3 |
| `426` | Unminify | Web | M2 | ✅ 練習 | L2/L3 |
| `427` | WebDecode | Web | M2 | ✅ 練習 | L2/L3 |
| `469` | Cookie Monster Secret Recipe | Web | M2 | ✅ 練習 | L2 |
| 自建 | ftp-cleartext | wireshark_labs | M3 | ✅ 帶練 | L2/L13 |
| 自建 | http-basic | wireshark_labs | M3 | ✅ 練習 | L2/L13 |
| `286` | Packets Primer | Forensics | M3 | ✅ capstone | L2 |
| `30` | shark on wire 1 | Forensics | M3 | ✅ capstone | L2 |
| `245` | PW Crack 1 | General Skills | M4 | ✅ 帶練 | L4/L1 |
| `246` | PW Crack 2 | General Skills | M4 | ✅ 練習 | L4/L1 |
| `173` | Cookies | Web | M4 | ✅ 練習 | L4 |
| `492` | SSTI1 | Web | M5 | ✅ 帶練 | 紅隊補充 |
| `304` | SQLiLite | Web | M5 | ✅ capstone (Medium) | 紅隊補充 |
| ~~`270`~~ | ~~Forbidden Paths~~ | Web | — | ❌ 不用（路徑穿越走情境演練 CVE，不重複） | — |
| `62` | 13（ROT13） | Cryptography | M6 | ✅ 帶練 | L12 |
| `144` | Mod 26 | Cryptography | M6 | ✅ 練習 | L12 |
| `68` | The Numbers | Cryptography | M6 | ✅ 練習 | L12 |
| `475` | hashcrack | Cryptography | M6 | ✅ 帶練(雜湊) | L12 |
| `243` | HashingJobApp | General Skills | M6 | ✅ 選配 | L12 |
| `37` | strings it | General Skills | M7 | ✅ 帶練 | L3 |
| `408` | CanYouSee | Forensics | M7 | ✅ 練習 | L3 |
| `186` | information | Forensics | M7 | ✅ 練習 | L3 |
| `7` | vault-door-training | Reverse Engineering | M7 | ✅ 帶練(讀碼) | L3 |
| `104` | Transformation | Reverse Engineering | M7 | ✅ 練習 | L3 |
| `4` | where are the robots | Web | M2? | ⏳ 候選（偵察，排細時定） | L3 |
| `161` | Scavenger Hunt | Web | M2? | ⏳ 候選（偵察示範） | L3 |

<!-- 每定一階同步更新帳本。偏差修正見 matrix。 -->
