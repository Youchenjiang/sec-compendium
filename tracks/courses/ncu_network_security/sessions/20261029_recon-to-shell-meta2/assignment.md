# A3 - Recon to Shell

## 繳交格式

- 檔名「姓名_A3.pdf」，例：「謝宸祐_A3.pdf」。
- 標題用 14 粗體標楷，內文用 12 標楷，皆採 1.5 行距。

## 環境

- **Metasploitable2**（Linux）——必做。
- **Metasploitable3**（Windows）——選做加分。

## 作業要求（在 Metasploitable2）

參考講義：[從偵察到拿下一個 shell](https://ncueeclass.ncu.edu.tw/media/doc/254434)（跟課教材）。

- 用 nmap 掃出開放埠與服務版本，把結果整理成一張表（至少 6 列），每列用一句話說出那個版本代表什麼。
- 從表裡**自己挑一個服務**（**不能用課堂示範的 vsftpd 2.3.4**），實際利用它拿到一個 shell，進去打 `id` / `whoami` 確認身分。拿到 shell 就收，不要求提權。
- 將流程截圖，並說明每一步的目的（掃到它、用的指令、拿到 shell、確認身分）。

> 評分看「會讀 > 跑得多」：能把掃描結果說出重點、而且是自己掃出、查出、打出來的，就是滿分；不比速度、不交 flag。

## 額外加分（課外，在 Metasploitable3）

- 在 Windows 的 **Metasploitable3** 上也拿一個 shell。它跑的服務（GlassFish、Jenkins、Tomcat、SMB、弱密碼…）和 Meta2 很不一樣，也更接近真實環境；一樣附上掃描、挑的目標、拿到 shell 的截圖與說明。
