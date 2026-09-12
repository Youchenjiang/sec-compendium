# 🚩 NCU CTFd Kit (中央資管資安競賽平台核心資產與工具套件)

本套件整理自 **2026 中央資管碩一新生茶會 Mini-CTF**，收錄了競賽期間自研的防作弊動態旗標外掛、多架構二進位題目建置腳本、繁中化與首殺加分補丁，以及活動自動結算排程工具，方便日後系上或實驗室快速復用與部署。

---

## 📂 目錄結構

```text
ctfd-kit/
├── plugins/
│   └── dynamic_shuffle_flag/         # 核心自研插件 (動態 Flag 演算法、檔案下載端點、Web Lab 路由)
├── challenges/
│   ├── ctfd_challenges.csv           # 題目題庫設定檔 (可直接透過 sync 腳本匯入)
│   ├── sync_challenges.py            # 題庫與提示自動同步腳本
│   └── reverse_graduation/           # 魔王逆向題《咪挺、肝與黑咖啡》
│       ├── check_graduation.c        # 原始碼 (12回合生存冒險遊戲)
│       └── build_all.sh              # 跨平台建置腳本 (Win .exe / Linux / macOS Universal Binary)
├── patches/
│   └── core_changes.patch            # CTFd 核心補丁 (首殺加分邏輯、自訂主題/頁尾、繁中修復)
├── database/
│   └── ctfd_dump_2026.sql            # 本屆完整資料庫備份結構與題目紀錄 (mysqldump)
├── automation/
│   └── send_final_top10.py           # 賽事結束自動結算發信工具 (抓取前十名、發送客製化領獎通知)
├── install.sh                        # 一鍵快速套用腳本
└── README.md                         # 本說明文件
```

---

## ⚡ 核心功能特色

### 1. 防作弊動態旗標插件 (`dynamic_shuffle_flag`)
- **每人專屬 Flag**：依據參賽者帳號與伺服器 Secret Salt 即時計算雜湊種子，動態洗牌插入字元。
- **動態二進位修補 (Binary Patching on the fly)**：
  - 同學下載 Windows (`.exe`)、Linux ELF 或 macOS 執行檔時，伺服器記憶體動態替換預留的 XOR 混淆佔位符，每個人載到的檔案二進位特徵皆不同。
- **動態圖片隱寫與 EXIF 產生**：
  - 圖片題即時生成包含專屬 Flag 的 UTF-16LE EXIF 資訊。
  - 圖檔後綴 ZIP 封包即時寫入專屬 Flag 文件。
- **自帶練習實驗室**：內建 Web 開發者工具題 (`/labs/f12`) 與加簽信密碼解密題 (`/labs/crypto`)。

### 2. 跨架構通用執行檔建置 (`challenges/reverse_graduation`)
- 透過 **Zig C Compiler** 與 **llvm-lipo**，在單一 Linux 環境下即可一鍵編譯出：
  - Windows x86_64 (`.exe`)
  - Linux x86_64 (ELF)
  - macOS arm64 (Apple Silicon M1~M4)
  - macOS x86_64 (Intel Mac)
  - **macOS Universal Binary**（雙架構合一，Mac 使用者下載直接能跑）

### 3. 首殺與先鋒額外加分機制 (`Option C`)
- 題目維持標準固定底分（如 500 分）。
- 每題前三名解出者，系統自動額外發送 Awards 獎項加分：
  - 🥇 一血首殺：`+50`
  - 🥈 二血先鋒：`+30`
  - 🥉 三血新星：`+10`
- 兼顧「新手人人可破關」與「高手搶先得分」的平衡。

### 4. 賽後自動化結算與郵件派送 (`automation/send_final_top10.py`)
- 活動時間截止時，自動透過 API 與資料庫鎖定前十名同學。
- 透過 Gmail SMTP SSL 發送極簡卡片式、手機響應式 (Mobile-Optimized) 的得獎確認信。
- 自動回報完整名冊與發送紀錄至管理員信箱。

---

## 🚀 快速安裝與復用指南

### 步驟 1：啟動標準 CTFd
在目標主機複製官方 CTFd：
```bash
git clone https://github.com/CTFd/CTFd.git
cd CTFd
```

### 步驟 2：複製外掛並套用修改
將本套件放入主機並執行安裝腳本：
```bash
cd ctfd-kit
chmod +x install.sh
./install.sh /path/to/CTFd
```

或手動複製外掛：
```bash
cp -r plugins/dynamic_shuffle_flag /path/to/CTFd/CTFd/plugins/
```

### 步驟 3：重啟 CTFd 容器
```bash
cd /path/to/CTFd
docker compose restart ctfd
```

---

## 📝 授權與維護
- **維護者**：NCU 網安實驗室 | CYberMaw
- **適用環境**：CTFd 3.x / Docker Compose / Ubuntu 22.04+
