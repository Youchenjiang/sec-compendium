# 🎯 中央資管《電腦網路安全》× picoCTF 技能階梯選題

> **用途**：把 picoCTF 題排成一條**技能階梯（M0~M7）**，一階建在前一階上。講義（Lesson）降成**對照欄**，給老師排課對應用。
>
> **骨架為何是技能、不是講義 Lesson**：講義是概念／管理導向的課，硬把動手題塞進 Lesson 1~13 會一直跑偏（半數課沒題配、框架被污染、技能接不起來）。技能軸才會真的疊起來。講義的對齊與偏差修正另見 [`ncu_cylab_curriculum_mapping_matrix.md`](ncu_cylab_curriculum_mapping_matrix.md)。
>
> **定位（兩軌）**：這份是「**關卡解題**」軌——CyLab picoCTF，一題一技能、拿 flag。另一條「**情境演練**」軌（CDX 靶場，Nessus／Suricata 掃描與偵測，交報告不拿 flag）在 [`ncu_network_security/`](ncu_network_security/)（攻擊側 `sessions/20261002_attack-cve-2021-41773`、防守側備選 `alt-materials/nessus-suricata`）。兩軌互補。
>
> **選題原則**
> 1. **難度靠脈絡換取**：Easy 進場暖身；一階鋪好「帶練 → 練習」後，可用 **Medium 當實戰 capstone** 收尾。要避開的是 **Hard 與重工具**，不是 Medium 本身。
> 2. **依賴順序**：整條階梯就是「先會的技能 → 疊上去的技能」，M0→M7 不跳階。M3～M7 彼此只依賴 M1、M2，不互相依賴，**排課順序可依講義進度調整**（實際：M0–M2 → M7 → M5 → M4，M3 因 Wireshark 工作坊已教而略過）。
> 3. **帶練 → 練習**：每階老師先示範，學員再用同工具自己練。
> 4. **不跨階重複**：一題的技能屬於哪一階，就在那階出現；別的階要用同概念，換不同題。
> 5. **flag ≠ 學習成果**：每題配一個「🧠 理解問題」，解完就答。flag 只當「做過」的門票，成績看能否講清機制；這也是對「貼 GPT 拿 flag 卻沒懂」的防線。自建題（wireshark_labs）每人 flag 不同，再加一層防抄。
>
> 6. **從候選池挑，不憑印象**：每階附「候選池」，列出同技能、還沒選用的 Easy／Medium 題（依難度、全站解出人數排序），來自 [技能分類](../../security/practice/challenges/platforms/cylab_picoctf/cylab_skill_classification.md)。換題、加分題、補考題都從這裡挑；標「題名推測」的題目要先看題目說明。
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

<details><summary>候選池（12 題）</summary>

`58` Warmed Up（E・172k）、`86` 2warm（E・169k）、`239` convertme.py（E・79k）、`371` repetitions（E・43k）、`404` binhexa（E・27k）、`414` endianness（E・27k）、`762` bytemancy 1（E・9k・題名推測）、`742` bytemancy 0（E・9k・題名推測）、`35` Based（M・41k）、`390` ASCII Numbers（M・36k）、`724` bytemancy 2（M・3k・題名推測）、`730` bytemancy 3（M・2k・題名推測）

</details>

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

<details><summary>候選池（12 題）</summary>

`132` GET aHEAD（E・119k）、`274` Includes（E・89k）、`406` Bookmarklet（E・67k）、`476` head-dump（E・28k）、`295` Search source（M・39k）、`9` picobrowser（M・38k）、`152` Some Assembly Required 1（M・36k）、`296` Secrets（M・31k）、`349` findme（M・28k）、`291` Roboto Sans（M・28k）、`356` MatchTheRegex（M・25k）、`131` Some Assembly Required 2（M・9k）。另有帳本中的候選 `4` where are the robots、`161` Scavenger Hunt。

</details>

---

## 📡 M3 — 明文流量與竊聽

> 對應講義：L2 Eavesdropping、L13 入侵偵測。｜工具：Wireshark（Follow TCP Stream）。｜接情境演練：Suricata 偵測。

| 角色 | ID／來源 | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `286` | **Packets Primer** | Medium | 開 pcap、Follow TCP Stream，payload 直接看到 flag | [library](https://learn.cylabacademy.org/library?search=Packets%20Primer) |
| 練習（接 M1） | `459` | **Ph4nt0m 1ntrud3r** | Easy | 依時間排序封包，拼回分段的 base64 再解開 | [library](https://learn.cylabacademy.org/library?search=Ph4nt0m%201ntrud3r) |
| capstone | `30` | **shark on wire 1** | Medium | 在多條 stream 中找出藏 flag 的那條，拼回來 | [library](https://learn.cylabacademy.org/library?search=shark%20on%20wire%201) |
| 選配 | `264` | **Eavesdrop** | Medium | 從明文聊天讀出解密指令，匯出傳輸的檔案再解密 | [library](https://learn.cylabacademy.org/library?search=Eavesdrop) |

🧠 **理解問題**
1. **Packets Primer** - flag 是「看」到的還是「解密」到的？這代表這段流量受保護了嗎？
2. **Ph4nt0m 1ntrud3r** - 封包裡的字串是 base64，攻擊者這樣傳，有讓旁觀的人看不到內容嗎？
3. **shark on wire 1** - 為什麼光看單一封包不夠，要追蹤整條 stream？
4. **Eavesdrop** - 檔案明明加密了，為什麼還是沒擋住竊聽者？

> 全用 CyLab 題，不另架環境。CyLab 的封包題沒有 Easy 的純明文題，故以 Medium 當帶練、用 Easy 的 `459` 練習。選配 `264` 題名就是講義的 Eavesdropping，金鑰在明文聊天裡傳，正好收束「加密也要整條路都保護」。`115` Wireshark doo dooo do doo... 不用：flag 套了 ROT13，屬 M6。DoS／Repudiation 無對應題型，講義帶過。
>
> 講義與作業（備選，未排入堂次）：[`alt-materials/cylab-packets/`](ncu_network_security/alt-materials/cylab-packets/)。課堂只示範 `286`，作業必做 `459`、`30`。學生若已上過 Wireshark 工作坊，Follow Stream 與明文帳密已教過，這階可略過或只用作業兩題當進階。

<details><summary>候選池（7 題，全為 Medium）</summary>

`115` Wireshark doo dooo do doo...（M・41k，ROT13 屬 M6，不用）、`362` PcapPoisoning（M・22k）、`103` Trivial Flag Transfer Protocol（M・16k）、`110` Wireshark twoo twooo two twoo...（M・13k）、`84` shark on wire 2（M・7k）、`237` WPA-ing Out（M・6k）、`311` Torrent Analyze（M・6k）

</details>

---

## 🔑 M4 — 認證與憑證

> 對應講義：L4 安全服務（Accountability 下的身分識別與認證，I&A）、L1 存取控制。｜觀念：登入後伺服器靠一張「憑證」（cookie／token）認人；每一種保護措施（簽章、嘗試次數限制、密碼雜湊、雙因素）都只在「它依賴的東西不在使用者手裡」時才有效。｜工具：瀏覽器 devtools、`flask-unsign`、Python `requests`、CyberChef。
>
> **難度定位**：學生已在 A1、A3 自己用 exploit 拿過 shell，Easy 只留給課堂示範；必做全用 Medium。

| 角色 | ID | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `46` | **logon** | Easy | cookie 沒簽章，權限旗標 `admin` 改了就生效 | [library](https://learn.cylabacademy.org/library?search=logon) |
| 必做 | `177` | **Most Cookies** | Medium | Flask cookie 有簽章，但金鑰只從 28 個字中挑一個；猜出金鑰再自己簽 | [library](https://learn.cylabacademy.org/library?search=Most%20Cookies) |
| 必做 | `521` | **Crack the Gate 2** | Medium | 登入失敗會鎖，但鎖的依據是使用者自己能填的 `X-Forwarded-For`；換值逐一試 20 個密碼 | [library](https://learn.cylabacademy.org/library?search=Crack%20the%20Gate%202) |
| 必做 | `765` | **No FA** | Medium | 無 salt 的密碼雜湊被查表還原；雙因素驗證碼放在 client 的 cookie | [library](https://learn.cylabacademy.org/library?search=No%20FA) |
| 選配 | `236` | **JAuth** | Medium | JWT 改成 `alg: none`，伺服器接受沒有簽章的 token | [library](https://learn.cylabacademy.org/library?search=JAuth) |

🧠 **理解問題**
1. **logon** - 你改了瀏覽器裡的 cookie，伺服器為什麼會信你改過的值？
2. **Most Cookies** - cookie 明明有簽章，為什麼你還是能偽造？簽章的安全靠的是什麼？
3. **Crack the Gate 2** - 伺服器用什麼判斷「同一個人一直猜錯」？為什麼這個依據擋不住你？
4. **No FA** - 密碼雜湊為什麼查得到原文？雙因素的第二個因素應該只有誰拿得到？這題它放在哪裡？
5. **JAuth** - token 上寫著用什麼演算法簽章，為什麼「讓 token 自己決定」會出事？

> 本組已備妥但**未排入堂次**（原排 2026-11-06，改先上 M7 接剛講完的 L3）；等 L4 講義上完再排。原 PW Crack 1／2 解法是讀程式碼與還原編碼，與 A2 重複；Old Sessions、Crack the Gate 1、Password Profiler 雖然切題但都是 Easy，移入候選池當暖身。全組不需 Burp：Crack the Gate 2 用 Python `requests` 迴圈即可。雜湊的單向性本身仍在 M6 教；這裡只從「沒加 salt 可查表」的角度用到。講義與作業（備選）：[`alt-materials/cylab-auth/`](ncu_network_security/alt-materials/cylab-auth/)。

<details><summary>候選池（21 題）</summary>

暖身（Easy）：`739` Old Sessions（E・16k，session 不過期又被列出）、`520` Crack the Gate 1（E・34k，原始碼裡的後門 header）、`712` Password Profiler（E・5k，用個資產生候選密碼）、`66` dont-use-client-side（E・96k）、`278` Local Authority（E・90k）、`173` Cookies（E・107k，與 logon 同招）、`245` PW Crack 1（E・84k，與 A2 重複）、`246` PW Crack 2（E・81k，與 A2 重複）、`419` IntroToBurp（E・46k，需 Burp）。

Medium：`743` Fool the Lockout（M・3k，每 30 秒重置的鎖定，放慢速度暴力猜）、`749` Credential Stuffing（M・3k，拿外洩帳密逐一試，需連線腳本）、`247` PW Crack 3（M・60k）、`248` PW Crack 4（M・51k，100 個候選，需寫迴圈）、`249` PW Crack 5（M・45k）、`200` login（M・56k）、`288` Power Cookie（M・40k，與 logon 同招）、`69` Client-side-again（M・25k）、`124` More Cookies（M・11k）、`25` JaWT Scratchpad（M・9k）、`355` Java Code Analysis!?!（M・7k）、`467` Apriti sesamo（M・3k）。

</details>

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

<details><summary>候選池（19 題）</summary>

`482` n0s4n1ty 1（E・20k）、`270` Forbidden Paths（M・34k，路徑穿越，與情境演練重複，不用）、`80` Irish-Name-Repo 1（M・27k）、`303` SQL Direct（M・25k）、`202` caas（M・23k）、`358` More SQLi（M・22k）、`59` Irish-Name-Repo 2（M・20k）、`376` SOAP（M・19k）、`445` Trickster（M・16k）、`8` Irish-Name-Repo 3（M・16k）、`88` Web Gauntlet（M・16k）、`488` SSTI2（M・12k）、`443` No Sql Injection（M・11k）、`484` 3v@l（M・10k）、`174` Web Gauntlet 2（M・10k）、`180` Super Serial（M・9k）、`128` Web Gauntlet 3（M・7k）、`729` Sql Map1（M・3k・題名推測）、`108` Startup Company（M・1k）

</details>

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

<details><summary>候選池（25 題）</summary>

`418` interencdec（E・61k）、`64` caesar（M・62k）、`43` Easy1（M・45k）、`316` Vigenere（M・36k）、`373` rotation（M・30k）、`307` substitution0（M・29k）、`31` Flags（M・28k）、`253` basic-mod1（M・25k）、`21` Tapping（M・23k）、`280` morse-code（M・22k）、`261` credstuff（M・21k）、`309` substitution2（M・20k）、`308` substitution1（M・20k）、`289` rail-fence（M・19k）、`254` basic-mod2（M・18k）、`40` Mr-Worldwide（M・17k）、`3` la cifra de（M・16k）、`312` transposition-trial（M・16k）、`351` HideToSee（M・15k）、`158` New Caesar（M・15k）、`210` spelling-quiz（M・7k）、`38` waves over lambda（M・6k）、`407` C3（M・6k）、`473` Guess My Cheese (Part 1)（M・6k）、`474` Guess My Cheese (Part 2)（M・2k）

</details>

---

## 🧷 M7 — 靜態檔案分析與讀程式找密鑰

> 對應講義：L3 惡意碼（硬編碼特徵字串、藏在檔案裡的東西）、forensics。｜觀念：不執行檔案，也能把裡面藏的東西挖出來；副檔名、畫面、塗黑都不可信，要看位元組。｜工具：`file`、`strings`、`exiftool`、`binwalk`、`zsteg`、`xxd`。排除記憶體 dump、Ghidra 反組譯。
>
> **教法**：示範的不是一招，是一張「拿到不明檔案時」的檢查表（辨識 → 看明文 → 拆 → 看像素 → 修檔頭）；作業每一題都是跑同一張表，flag 停在不同的步驟。難度定位同 M4：學生已在 A1、A3 自己拿過 shell，必做全用 Medium。

**藏在檔案裡的東西（2026-11-06）**

| 角色 | ID | 題名 | 難度 | flag 停在哪一步 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `129` | **Matryoshka doll** | Medium | 辨識 → 拆，反覆四層：`.jpg` 其實是 PNG，IEND 後面接著 zip，拆出下一張圖 | [library](https://learn.cylabacademy.org/library?search=Matryoshka%20doll) |
| 必做 | `268` | **File types** | Medium | 同一個「辨識 → 拆」迴圈，但 11 層每層格式不同（shar、ar、cpio、bzip2、gzip、lzip、lz4、lzma、lzop、xz），最後是 hex | [library](https://learn.cylabacademy.org/library?search=File%20types) |
| 必做 | `305` | **St3g0** | Medium | 前三步都沒東西，資料在像素最低位元；`zsteg` 的 `b1,rgb,lsb,xy` | [library](https://learn.cylabacademy.org/library?search=St3g0) |
| 必做 | `112` | **tunn3l v1s10n** | Medium | `file` 說是 data；BMP 檔頭三個欄位被改，修回後高度還被砍掉，藏了上半張圖 | [library](https://learn.cylabacademy.org/library?search=tunn3l%20v1s10n) |
| 加分 | `81` | **like1000** | Medium | 第三步「拆」做到 1000 層：`1000.tar` 裝 `999.tar`，一路到 `1.tar` 裝 `flag.png`；手動拆不完，必須寫迴圈 | [library](https://learn.cylabacademy.org/library?search=like1000) |
| 選做不計分 | `290` | **Redaction gone wrong** | Medium | 第二步就有：PDF 的塗黑只是蓋一層，文字物件還在；補「塗黑」這種藏法的觀念 | [library](https://learn.cylabacademy.org/library?search=Redaction%20gone%20wrong) |

🧠 **理解問題**
1. **Matryoshka doll** - 副檔名是 `.jpg`、看起來也是一張正常的圖，`file` 和 `binwalk` 憑什麼知道裡面還有東西？
2. **File types** - 你的 PDF 閱讀器打不開它，`file` 卻認得出來；`file` 看的是什麼？為什麼副檔名不算數？
3. **St3g0** - 圖片看起來完全正常，`exiftool`、`binwalk` 也都沒東西，資料到底放在哪裡？為什麼肉眼看不出差別？
4. **tunn3l v1s10n** - 你改了哪幾個欄位、各代表什麼？為什麼把高度改大就看得到被藏起來的那一半？
5. **like1000** - 你的迴圈怎麼知道下一層叫什麼、什麼時候該停？不邊拆邊刪會發生什麼事？
6. **Redaction gone wrong** - 畫面上明明是黑的，為什麼複製得到文字？真正的刪除該做什麼？

> 加分題選 like1000 而非 Redaction：Redaction 只到第二步、動作是複製貼上，比必做還輕，不該拿加分；like1000 是示範的同一個迴圈放大到 1000 層，逼學生把手動流程寫成程式，接 A3 的程度。它的 flag 固定，所以評分看腳本與回答，不看 flag。St3g0 與 What Lies Within 同招（`zsteg` 同一行），選 St3g0 是因為它的 flag 每個環境不同、且有 `$t3g0` 結尾可自我確認；What Lies Within 的 flag 固定，留候選池。講義與作業：[`sessions/20261106_cylab-files/`](ncu_network_security/sessions/20261106_cylab-files/)。
>
> **安裝**：Kali 已有 `binwalk`、`exiftool`；另需 `sudo apt install binutils lzip lz4 lzop sharutils` 與 `gem install zsteg`。

**讀簡單程式找密鑰（未排入堂次，另一套方法，不與上面混在同一堂）**

| 角色 | ID | 題名 | 難度 | 練什麼 | 連結 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 帶練 | `7` | **vault-door-training** | Easy | 讀簡單 Java 找寫死的密碼 | [library](https://learn.cylabacademy.org/library?search=vault-door-training) |
| 練習 | `104` | **Transformation** | Easy | 讀／逆簡單 Python 轉換 | [library](https://learn.cylabacademy.org/library?search=Transformation) |

🧠 **理解問題**
1. **vault-door-training** - 密鑰就寫在原始碼裡，為什麼「把密鑰藏在程式碼裡」本身就不安全？

> 排入時依 M4／M7 的難度定位，把必做換成候選池裡的 Medium（crackme-py、keygenme-py、vault-door-1）。原本的 Easy 題 strings it、CanYouSee、information 移入候選池當暖身。

<details><summary>候選池：檔案、中繼資料與隱寫（32 題）</summary>

`37` strings it（E・117k，暖身）、`408` CanYouSee（E・47k，暖身）、`186` information（E・148k，暖身）、`44` Glory of the Garden（E・96k）、`444` Scan Surprise（E・70k）、`450` Verify（E・62k）、`423` Secret of the Polyglot（E・44k）、`530` Riddle Registry（E・43k）、`524` Hidden in plainsight（E・32k）、`460` RED（E・29k）、`523` Flag in Flame（E・23k）、`519` Corrupted file（E・19k）、`698` Binary Digits（E・10k・題名推測）、`265` Enhance!（M・48k）、`52` extensions（M・35k）、`19` So Meta（M・34k）、`279` Lookey here（M・30k）、`74` What Lies Within（M・27k，與 St3g0 同招，flag 固定）、`350` hideme（M・18k）、`420` Mob psycho（M・10k）、`348` FindAndOpen（M・10k）、`205` advanced-potion-making（M・9k）、`359` MSB（M・8k）、`51` WhitePages（M・8k）、`26` m00nwalk（M・8k）、`139` Milkslap（M・7k）、`53` c0rrupt（M・7k）、`415` endianness-v2（M・6k）、`432` Blast from the past（M・4k）、`481` flags are stepic（M・4k）、`714` Rogue Tower（M・3k）、`101` Weird File（M・2k）

</details>

<details><summary>候選池：讀程式找密鑰（19 題）</summary>

`472` Flag Hunters（E・26k）、`175` crackme-py（M・44k）、`121` keygenme-py（M・42k）、`12` vault-door-1（M・36k）、`294` Safe Opener（M・23k）、`287` patchme.py（M・20k）、`116` speeds and feeds（M・18k）、`314` unpackme.py（M・17k）、`400` Picker I（M・16k）、`375` Safe Opener 2（M・16k）、`60` vault-door-3（M・13k）、`256` bloat.py（M・13k）、`71` vault-door-4（M・11k）、`271` Fresh Java（M・11k）、`401` Picker II（M・10k）、`77` vault-door-5（M・9k）、`402` Picker III（M・8k）、`45` vault-door-6（M・7k）、`428` weirdSnake（M・3k）

</details>

<details><summary>候選池：磁碟、記憶體、日誌與 Git 調查（21 題，多數超出本階「排除記憶體 dump」的範圍，列供進階參考）</summary>

`505` DISKO 1（E・36k）、`301` Sleuthkit Intro（M・29k）、`300` Sleuthkit Apprentice（M・21k）、`130` MacroHard WeakEdge（M・21k）、`137` Disk, disk, sleuth! II（M・18k）、`113` Disk, disk, sleuth!（M・14k）、`285` Operation Orchid（M・11k）、`456` Event-Viewing（M・7k）、`506` DISKO 2（M・7k）、`87` Pitter, Patter, Platters（M・6k）、`284` Operation Oni（M・6k）、`507` DISKO 3（M・6k）、`413` Dear Diary（M・4k）、`453` Bitlocker-1（M・4k）、`720` Timeline 0（M・3k・題名推測）、`705` Forensics Git 0（M・3k・題名推測）、`704` DISKO 4（M・3k・題名推測）、`706` Forensics Git 1（M・2k・題名推測）、`721` Timeline 1（M・2k・題名推測）、`454` Bitlocker-2（M・2k）、`707` Forensics Git 2（M・2k・題名推測）

</details>

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
| `286` | Packets Primer | Forensics | M3 | ✅ 帶練 | L2 |
| `459` | Ph4nt0m 1ntrud3r | Forensics | M3 | ✅ 練習 | L2 |
| `30` | shark on wire 1 | Forensics | M3 | ✅ capstone | L2 |
| `264` | Eavesdrop | Forensics | M3 | ✅ 選配 | L2 |
| `46` | logon | Web | M4 | ✅ 帶練 | L4 |
| `177` | Most Cookies | Web | M4 | ✅ 必做 (Medium) | L4 |
| `521` | Crack the Gate 2 | Web | M4 | ✅ 必做 (Medium) | L4 |
| `765` | No FA | Web | M4 | ✅ 必做 (Medium) | L4 |
| `236` | JAuth | Web | M4 | ✅ 選配 (Medium) | L4 |
| `739` | Old Sessions | Web | M4 | ⏳ 候選（暖身） | L4 |
| `520` | Crack the Gate 1 | Web | M4 | ⏳ 候選（暖身） | L4 |
| `712` | Password Profiler | General Skills | M4 | ⏳ 候選（暖身） | L4 |
| `245` | PW Crack 1 | General Skills | M4 | ⏳ 候選（與 A2 重複） | L4/L1 |
| `246` | PW Crack 2 | General Skills | M4 | ⏳ 候選（與 A2 重複） | L4/L1 |
| `173` | Cookies | Web | M4 | ⏳ 候選（與 logon 同招） | L4 |
| `492` | SSTI1 | Web | M5 | ✅ 帶練 | 紅隊補充 |
| `304` | SQLiLite | Web | M5 | ✅ capstone (Medium) | 紅隊補充 |
| ~~`270`~~ | ~~Forbidden Paths~~ | Web | — | ❌ 不用（路徑穿越走情境演練 CVE，不重複） | — |
| `62` | 13（ROT13） | Cryptography | M6 | ✅ 帶練 | L12 |
| `144` | Mod 26 | Cryptography | M6 | ✅ 練習 | L12 |
| `68` | The Numbers | Cryptography | M6 | ✅ 練習 | L12 |
| `475` | hashcrack | Cryptography | M6 | ✅ 帶練(雜湊) | L12 |
| `243` | HashingJobApp | General Skills | M6 | ✅ 選配 | L12 |
| `129` | Matryoshka doll | Forensics | M7 | ✅ 帶練 | L3 |
| `268` | File types | Forensics | M7 | ✅ 必做 (Medium) | L3 |
| `305` | St3g0 | Forensics | M7 | ✅ 必做 (Medium) | L3 |
| `112` | tunn3l v1s10n | Forensics | M7 | ✅ 必做 (Medium) | L3 |
| `81` | like1000 | Forensics | M7 | ✅ 加分 (Medium) | L3 |
| `290` | Redaction gone wrong | Forensics | M7 | ✅ 選做不計分 | L3 |
| `37` | strings it | General Skills | M7 | ⏳ 候選（暖身） | L3 |
| `408` | CanYouSee | Forensics | M7 | ⏳ 候選（暖身） | L3 |
| `186` | information | Forensics | M7 | ⏳ 候選（暖身） | L3 |
| `7` | vault-door-training | Reverse Engineering | M7 | ✅ 帶練(讀碼，未排) | L3 |
| `104` | Transformation | Reverse Engineering | M7 | ✅ 練習(讀碼，未排) | L3 |
| `4` | where are the robots | Web | M2? | ⏳ 候選（偵察，排細時定） | L3 |
| `161` | Scavenger Hunt | Web | M2? | ⏳ 候選（偵察示範） | L3 |

<!-- 每定一階同步更新帳本。偏差修正見 matrix。 -->
