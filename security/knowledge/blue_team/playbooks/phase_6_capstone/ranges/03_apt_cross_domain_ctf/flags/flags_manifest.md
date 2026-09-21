# 🚩 APT 實體奪旗關卡 Flag 清單與驗證金鑰

| 關卡階段 | 權限目標 | 取得位置 | 旗標內容 |
| :--- | :--- | :--- | :--- |
| **Stage 1 (Initial Access)** | DMZ Web RCE | 注入指令讀取環境變數 | `FLAG{dmz_rce_initial_foothold_9182}` |
| **Stage 2 (Lateral Pivot)** | 內網跳板提權 | `/opt/stage2_note.txt` | `FLAG{pivot_corp_jumpbox_breached_3389}` |
| **Stage 3 (Core Vault DB)** | 核心機密資料庫 | 跨網段連線 `http://172.30.3.30:9999/flag.txt` | `FLAG{apt_full_chain_pwned_7721_v4ult}` |
