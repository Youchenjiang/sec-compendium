# 🔴 紅隊全領域實戰與武器庫體系 (Red Team Offensive Knowledge Base)

> ⚔️ **本目錄宗旨**：  
> 與 [../blue_team/](../blue_team/) 完全對稱建立之現代紅隊進攻作戰體系！  
> 完整涵蓋六大作戰階段：外部資產情報偵察、邊界打點與 Web/API 突破、企業 Active Directory 網域統治、主機立足與本地提權、內網穿透與 C2 基礎設施、以及執行期防禦規避與雲端/容器攻防。

---

## 🏛️ 紅隊核心架構導覽

```text
security/knowledge/red_team/
├── README.md                          # 本總覽入口
├── career_curriculum.md               # 🚀 現代紅隊通關主線課表 (Phase 1 ~ Phase 6、作戰鏈主幹、40 項 Core 必修)
├── index.md                           # ⚔️ 實戰技能細分矩陣 (全景 23 大攻擊領域・110 個專項技術點・L1~L4 分級)
├── RED_TEAM_TECHNIQUES_CATALOG.md     # 📋 23 大領域與 110 項核心實戰技術索引目錄
│
├── operations/                        # 🎯【作戰編排與交戰方法論】(00~05 授權邊界、路徑路由、驗證與復盤)
│   └── README.md                      # 作戰編排層定位與核心流程
│
├── learning_paths/                    # 📚【領域深度自學路徑】（22 篇深度原理指南 + 全景自學地圖）
│   └── README.md                      # 自學指南全景說明
│
└── playbooks/                         # 📋【110 篇標準化原子實戰手冊】
    ├── README.md                      # Playbooks 體系總覽與階段說明
    ├── PLAYBOOK_SPECIFICATION_AND_TEMPLATE.md # 手冊規格書與標準模板
    ├── phase_1_recon_surface/         # 🌐 Phase 1: 外部情報與資產暴露面 (R01~R05，19 篇)
    ├── phase_2_perimeter_web/         # 🎯 Phase 2: 邊界打點與 Web/API 突破 (R06, R09~R15，30 篇)
    ├── phase_3_domain_dominance/      # 👑 Phase 3: 企業身分與 AD 網域統治 (R07, R08, R16, R17，21 篇)
    ├── phase_4_host_privesc/          # ⚡ Phase 4: 主機立足與本地提權 (R18~R19，14 篇)
    ├── phase_5_pivoting_c2/           # 🌪️ Phase 5: 內網橫向與穿透代理 (R20~R21，13 篇)
    └── phase_6_evasion_cloud/         # 🥷 Phase 6: 防禦規避與前沿環境攻防 (R22~R23，13 篇)
```

---

## 🧭 核心導覽與修課指引

| 模組 / 文檔 | 檔案連結 | 核心用途與適用對象 |
| :--- | :--- | :--- |
| **紅隊實戰通關課表** | [`career_curriculum.md`](career_curriculum.md) | **【修課主線】** Phase 1 ~ Phase 6 階段式進階課表、三層能力分流 (Core 40 篇必修) 與作戰鏈導引 |
| **全領域技能矩陣總表** | [`index.md`](index.md) | **【技術總覽】** 全景 23 大領域、110 項技術點（L1~L4 難度分級）與可練習靶場清單 |
| **110 項實戰技術索引** | [`RED_TEAM_TECHNIQUES_CATALOG.md`](RED_TEAM_TECHNIQUES_CATALOG.md) | **【原子清單】** 23 大領域、110 項技術點的標準命名、原語定義與檔案對照表 |
| **紅隊作戰編排方法論** | [`operations/`](operations/README.md) | **【戰略規劃】** 涵蓋授權 Scope 界定、攻擊面路由、立足點躍遷、真假陽性驗證與覆盤沉澱之 6 大全流程指南 |
| **領域深度自學指南** | [`learning_paths/`](learning_paths/README.md) | **【原理深潛】** 涵蓋 6 大作戰區塊、22 篇深度原理與全景自學地圖（偵察、Web、AD、提權、C2、防禦規避與雲原生） |
| **110 篇原子實戰手冊** | [`playbooks/`](playbooks/README.md) | **【即時作戰】** 嚴格遵循特戰速查標準（五動破題、指令速查、驗收閉環）之作戰手冊庫 |

---

## 🎯 相關模組交互參照

- **藍隊對稱體系**：防守方日誌研判、加固策略與 SOC 偵測規則，請參閱 👉 [`../blue_team/`](../blue_team/README.md)。
- **實體靶機與實作驗證**：真實靶機演練環境與題庫，請參閱 👉 [`../../practice/`](../../practice/README.md)。
