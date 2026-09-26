# 答題卡：[大題名稱] (總題數: 0 / ACCEPTED: 0)

> **操作說明**：
> - **人類選手**：只有 `VERIFIED` 才建議提交；提交後回報平台結果，由 Main 更新為 `ACCEPTED` 或 `REJECTED`。
> - **Main / Lead Session**：本檔唯一 writer；負責答案、狀態、evidence reference 與平台結果。
> - **Secret hygiene**：密碼、token、session secret、private key 不得原文寫入本 tracked 檔案。

---

## 🎯 小題作答總表

| 題號 | 題目問題核心 | 作答狀態 | 候選答案 (Flag / IOC) | 信心等級 | 答題來源 / 依據工件 |
| :---: | :--- | :---: | :--- | :---: | :--- |
| **Q01** | 攻擊者最初登入的來源 IP 為何？ | `OPEN` | - | - | 待分析 Security.evtx 4624 |
| **Q02** | 遭到攻擊者利用/登入的使用者帳號名稱？ | `OPEN` | - | - | 待分析 Security.evtx 4624 |
| **Q03** | 攻擊者下載並落地之可疑檔案名稱？ | `OPEN` | - | - | 待分析 Prefetch / MFT |
| **Q04** | 該可疑檔案之 SHA-256 雜湊值？ | `OPEN` | - | - | 待抽取實體計算 Hash |
| **Q05** | 惡意程式首次被執行之精確時間 (UTC)？ | `OPEN` | - | - | 待分析 Prefetch / Amcache |
| **Q06** | 攻擊者建立的持久化後門機制（服務/排程）名稱？ | `OPEN` | - | - | 待分析 System.evtx 7045 |
| **Q07** | 後門連線之 C2 伺服器 IP 與 Port？ | `OPEN` | - | - | 待分析 記憶體 Netscan / Sysmon 3 |
| **Q08** | 攻擊者在內網進行橫向移動嘗試之目標 IP？ | `OPEN` | - | - | 待分析 防火牆日誌 / 4624 Type 3 |
| **Q09** | 攻擊者最後留下的勒索訊息檔名？ | `OPEN` | - | - | 待分析 磁碟根目錄 / 桌面文字檔 |
| **Q10** | 勒索訊息中要求的贖金錢包地址？ | `OPEN` | - | - | 待查看 勒索信內容 |

---

## Answer lifecycle
- `OPEN`：尚無候選答案。
- `CANDIDATE`：已有答案，但 evidence contract 尚未滿足。
- `VERIFIED`：證據可重現且格式已檢查，可提交；不代表平台已接受。
- `SUBMITTED`：已送出平台，等待結果。
- `ACCEPTED`：平台明確接受；只有此狀態計入 scoreboard 已解題數。
- `REJECTED`：平台明確拒絕；保留 evidence 與 submission history 後重新調查。
