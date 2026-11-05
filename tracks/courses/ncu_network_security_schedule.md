# 《電腦網路安全》課程排課表索引

> 中央資管《電腦網路安全》(114 學年度・陳奕明 教授) 每一場次的**日期、主題、用了哪份教材**,集中在這一份。

**教材位置**:本課所有交付教材都收在同一個 repo 的 [`ncu_network_security/`](ncu_network_security/) 底下——`sessions/`(各堂文字教材)、`deck-studio/`(可編譯的簡報工作區)、`alt-materials/`(備選)。結構與預覽方式見 [`ncu_network_security/README.md`](ncu_network_security/README.md)。連結皆為同 repo 相對路徑,GitHub 上可直接點開。

---

## 一、CDX 情境演練軌（實作場次）

在 CDX 靶場把工具串起來跑一遍,按**堂次**排序。

| 堂次 | 日期 | 主題 | 文字教材 | 簡報 |
|---|---|---|---|---|
| 第一堂 | 2026-10-02 | Apache CVE-2021-41773:路徑穿越 → RCE → reverse shell | [`sessions/20261002_attack-cve-2021-41773/`](ncu_network_security/sessions/20261002_attack-cve-2021-41773/)（教案＋手冊＋腳本＋pptx）| [`deck-studio …cve-2021-41773/`](ncu_network_security/deck-studio/slides/workshop-202610-cdx-cve-2021-41773/) |
| 第二堂 | 2026-10-29 | 用 nmap 偵察 Metasploitable2:掃 → 讀成一張表 → 自選一條利用拿 shell | [`sessions/20261029_recon-to-shell-meta2/`](ncu_network_security/sessions/20261029_recon-to-shell-meta2/)（[handout](ncu_network_security/sessions/20261029_recon-to-shell-meta2/handout.md)・[assignment](ncu_network_security/sessions/20261029_recon-to-shell-meta2/assignment.md)・[answer-key](ncu_network_security/sessions/20261029_recon-to-shell-meta2/answer-key.md)）| 無 deck |
| 第三堂 | 未定 | 尚未排定 | — | — |

## 二、Wireshark 封包分析講座

| 日期 | 主題 | 文字教材 | 簡報 |
|---|---|---|---|
| 2026-10-03 | Wireshark 封包分析基礎（20 分鐘） | [`sessions/20261003_wireshark-fundamentals/`](ncu_network_security/sessions/20261003_wireshark-fundamentals/) | [`deck-studio …wireshark-fundamentals/`](ncu_network_security/deck-studio/slides/workshop-202610-net-wireshark-fundamentals/) |
| 2026-10-06 | Wireshark 實務操作與通訊協定檢視 | [`sessions/20261006_wireshark-v2/`](ncu_network_security/sessions/20261006_wireshark-v2/) | [`deck-studio …wireshark-v2/`](ncu_network_security/deck-studio/slides/workshop-202610-net-wireshark-v2/) |

## 三、CyLab 課後加分題庫（依週次，非場次日期）

picoCTF 官方題庫,14 道題嚴格對應講義週次 W2–W13,是課後加分而非單一上課場次,故按**週次**而非日期編排。

- 題庫與逐題導引:[`ncu_network_security_cylab_guide.md`](ncu_network_security_cylab_guide.md)
- 範圍:W2 監聽、W3 探測、W4 嗅探、W5 認證、W7 最小權限、W10 防火牆、W12 VPN、W13 侵入偵測。

## 四、備選・未排入堂次

| 主題 | 教材 |
|---|---|
| Nessus 弱掃 + Suricata 偵測（防守對照,堂次未定）| [`alt-materials/nessus-suricata/`](ncu_network_security/alt-materials/nessus-suricata/) |
| CyLab 封包分析（技能階梯 M3,與 Wireshark 工作坊重疊而未排入）| [`alt-materials/cylab-packets/`](ncu_network_security/alt-materials/cylab-packets/) |
| CyLab 認證與憑證（技能階梯 M4,等 L4 講完再排）| [`alt-materials/cylab-auth/`](ncu_network_security/alt-materials/cylab-auth/) |

---

## 日期出處說明

同一份課程的日期目前有兩種來源,本表據實標註、不統一造假:

- **明寫的場次日期**:CDX 第二堂在 `answer-key.md` 寫「日期 2026-10-29／場次 2026-10」,最可靠。CDX 第一堂 2026-10-02 由授課者確認。
- **簡報建立時間**:Wireshark 兩場目前只有 deck `index.tsx` 的 `createdAt`(授課前後的編寫時間,近似授課日期）——基礎 10-03、v2 10-06。
- `sessions/` 資料夾以 `YYYYMMDD_` 前綴命名,依上述日期排序即授課順序。

要讓每一場都有可靠日期,可在各堂自己的 README／answer-key 補一行明確場次,本表再改引那一行。
