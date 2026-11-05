# CDX 備選教材：Nessus 弱掃 + Suricata 偵測（CVE-2021-41773）

> **狀態**：**備選教材，課程堂次未定**（原規劃的防守對照場次，暫不排入正式堂次）。
> **技術領域**：弱點掃描（Nessus，偏偵察／**非藍隊**）· 入侵偵測（Suricata，藍隊 IDS）
> **對應講義**：L7 弱點識別 · L13 入侵偵測。

搭配攻擊側 [`20261002_attack-cve-2021-41773`](../../sessions/20261002_attack-cve-2021-41773/)（紅隊把同一個 CVE 的靶機打穿）。這套負責掃出漏洞、偵測攻擊。

> 弱掃那一塊的「預裝工具實證 + 學員作業」已獨立成**第二堂** [`20261029_recon-to-shell-meta2`](../../sessions/20261029_recon-to-shell-meta2/)，不在本備選教材內。

## 套件結構

```text
nessus-suricata/
├── docs/
│   └── course-design.md   # 課程源頭文件（Nessus 掃描 + Suricata 偵測教案）
└── scripts/
    ├── watch_suricata.sh   # 靶機上：更新規則、監聽網卡、盯 alert
    └── README.md
```

攻擊流量直接用攻擊側套件的 `scripts/01_test_traversal.sh`，這邊不重複造。

## 快速開始

1. 讀 [`docs/course-design.md`](docs/course-design.md)。
2. 靶機上跑 `scripts/watch_suricata.sh` 起 Suricata。
3. 工具機用 Nessus 掃靶機，再發一次攻擊，回靶機看 alert。
