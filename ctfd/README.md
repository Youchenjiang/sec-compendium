# 🎯 CTFd 實戰評測與演練靶場模組 (CTFd Platform Module)

> 本模組為全專案的**「線上實戰靶場與競賽評測子系統」**。  
> 收錄自研防作弊動態 Flag 外掛、核心繁中化補丁、競賽題目原始碼、初始資料庫結構與一鍵部署腳本。

---

## 🏛️ 目錄架構

`	ext
ctfd/
├── automation/      # 賽後自動化結算信件寄送腳本 (send_final_top10.py)
├── challenges/      # 靶機題目源碼、二進制編譯腳本與題目清單 CSV
├── database/        # CTFd 初始化資料庫結構與預設帳密 dump (ctfd_dump_2026.sql)
├── patches/         # CTFd 核心修改 Git Patch (首殺加分、繁中介面)
├── plugins/         # dynamic_shuffle_flag 動態 Flag 注入外掛
└── install.sh       # 一鍵快速部署與外掛套用腳本
`

---

## 🚀 快速開始

若需將本套件部署至目標伺服器，請至本目錄下執行：
`ash
cd ctfd
./install.sh /path/to/CTFd
`
詳細參數與操作說明請參閱 [install.sh](install.sh)。
