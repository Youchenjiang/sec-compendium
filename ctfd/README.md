# 🎯 CTFd 實戰評測與演練靶場模組 (CTFd Platform Module)

> 本模組為全專案的**「線上實戰靶場與競賽評測子系統」**。  
> 收錄自研防作弊動態 Flag 外掛、核心繁中化補丁、競賽題目原始碼、初始資料庫結構與一鍵部署腳本。
> 
> 💡 **概念區隔說明**：
> - **`ctfd/`（本模組）**：專用於維運與部署自架 CTFd 競賽伺服器（包含系上新生盃與校內 CTF 之自製題目源碼與匯入腳本）。
> - **[`../security/practice/challenges/`](../security/practice/challenges/README.md)**：專用於聚合與同步全網 8 大主流資安攻防平台（Hack The Box, TryHackMe, CyberDefenders 等 3,945+ 關卡）之公開題庫與學習目錄。

---

## 🏛️ 目錄架構

```text
ctfd/
├── README.md        # 本模組總覽
├── event_guide.md   # 🏆 中央資管碩一茶會 Mini-CTF 全套活動手冊暨官方解題指南 (Write-Up)
├── assets/          # 競賽認證範本、校園圖片素材與動態 Flag 置換資源
├── automation/      # 平台自動化維運腳本 (題目同步 sync_challenges.py、結算信 send_final_top10.py)
├── challenges/      # 靶機題目源碼、二進制編譯腳本與自架題目清單 CSV
├── database/        # CTFd 初始化資料庫結構與預設帳密 dump (ctfd_dump_2026.sql)
├── patches/         # CTFd 核心修改 Git Patch (首殺加分、繁中介面)
├── plugins/         # dynamic_shuffle_flag 動態 Flag 注入外掛
└── install.sh       # 一鍵快速部署與外掛套用腳本
```

---

## 🏆 官方競賽活動手冊暨 Write-Up

- 完整賽事架構、動態 Flag 外掛原理、7 大關卡破關攻略與伺服器運維手冊，請直接參閱 👉 [**`event_guide.md`**](event_guide.md)。


---

## 🚀 快速開始

若需將本套件部署至目標伺服器，請至本目錄下執行：

```bash
cd ctfd
./install.sh /path/to/CTFd
```

詳細參數與操作說明請參閱 [install.sh](install.sh)。
