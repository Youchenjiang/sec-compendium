# 《電腦網路安全》課程排課表索引

> 中央資管《電腦網路安全》(114 學年度・陳奕明 教授) 每一場次的**日期、主題、用了哪份教材**，集中在這一份。
> 這是課程的主索引：教材分散在兩個 repo，這裡當家，各教材當衛星連過去。

**教材分佈**

- **本課程專案** `ctfd-kit/tracks/courses/`：課後加分題庫、週次對照。
- **Open Slide** `Common/Slide/workshops/`：實際上課的簡報、跟課教材、作業、備選教材。

> 下表連到 Open Slide 的路徑是相對路徑（`../../../../Common/Slide/...`），在本機磁碟可直接開；兩個 repo 在 GitHub 上是分開的，故那些連結在 GitHub 網頁上不會解析——詳見末尾〈教材跟著專案走〉。

---

## 一、CDX 情境演練軌（實作場次）

在 CDX 靶場把工具串起來跑一遍，按**堂次**排序。

| 堂次 | 日期 | 主題 | 教材 |
|---|---|---|---|
| 第一堂 | 2026-10 | Apache CVE-2021-41773：路徑穿越 → RCE → reverse shell | [`01_attack-cve-2021-41773/`](../../../../Common/Slide/workshops/CDX_scenario-drills/01_attack-cve-2021-41773/)（簡報＋教案＋學員手冊＋腳本）|
| 第二堂 | 2026-10-29 | 用 nmap 偵察 Metasploitable2：掃 → 讀成一張表 → 自選一條利用拿 shell | [`handout.md`](../../../../Common/Slide/workshops/CDX_scenario-drills/02_recon-to-shell-meta2/handout.md)（跟課）・[`assignment.md`](../../../../Common/Slide/workshops/CDX_scenario-drills/02_recon-to-shell-meta2/assignment.md)（作業）・[`answer-key.md`](../../../../Common/Slide/workshops/CDX_scenario-drills/02_recon-to-shell-meta2/answer-key.md)（教師）|
| 第三堂 | 未定 | 尚未排定 | — |

堂次來源：[`CDX_scenario-drills/README.md`](../../../../Common/Slide/workshops/CDX_scenario-drills/README.md)。

## 二、Wireshark 封包分析講座

| 日期 | 主題 | 教材 |
|---|---|---|
| 2026-10-03 | Wireshark 封包分析基礎（20 分鐘） | [`202610_NET_Wireshark-Fundamentals/`](../../../../Common/Slide/workshops/202610_NET_Wireshark-Fundamentals/) |
| 2026-10-06 | Wireshark 實務操作與通訊協定檢視 | [`202610_NET_Wireshark-v2/`](../../../../Common/Slide/workshops/202610_NET_Wireshark-v2/) |

## 三、CyLab 課後加分題庫（依週次，非場次日期）

picoCTF 官方題庫，14 道題嚴格對應講義週次 W2–W13，是課後加分而非單一上課場次，故按**週次**而非日期編排。

- 題庫與逐題導引：[`ncu_network_security_cylab_guide.md`](ncu_network_security_cylab_guide.md)
- 範圍：W2 監聽、W3 探測、W4 嗅探、W5 認證、W7 最小權限、W10 防火牆、W12 VPN、W13 侵入偵測。

## 四、備選・未排入堂次

| 主題 | 教材 |
|---|---|
| Nessus 弱掃 + Suricata 偵測（防守對照，堂次未定）| [`CDX_alt-materials/nessus-suricata/`](../../../../Common/Slide/workshops/CDX_alt-materials/nessus-suricata/) |

---

## 日期出處說明

同一份課程的日期目前有兩種來源，本表據實標註、不統一造假：

- **明寫的場次日期**：CDX 第二堂在 `answer-key.md` 寫「日期 2026-10-29／場次 2026-10」，最可靠。
- **簡報建立時間**：其餘場次目前只有 slide `index.tsx` 的 `createdAt`（授課前後的編寫時間，近似授課月份）——CDX 第一堂 10-02、Wireshark 基礎 10-03、v2 10-06。

要讓每一場都有可靠日期，可在各堂自己的 README／answer-key 補一行明確場次，本表再改引那一行。

## 教材跟著專案走（待辦）

目前 Open Slide 的實作教材住在獨立的 `Common/Slide` repo，課程專案得跨 repo 相對路徑去引，GitHub 網頁上連結會斷。較徹底的作法是讓 Open Slide 的本課程教材**跟著課程專案走**（像 python venv 跟著專案），把本課相關的 workshop 收進課程專案、或以 submodule 納入，連結才能在同一 repo 內解析。這是一次跨 repo 搬遷，牽涉 git 歷史與 `Common/Slide` 裡其他非本課教材，屬另一項決定，尚未進行。
