# NCtfU 週五讀書會｜每週實作課表

版本：v0.5｜2026-09-08｜成員與輪值主持人使用

本文件只維護日期、指定題目、聚會流程、課外任務及材料準備。競賽選擇、學習目標、投入考量與下學期決策見 [目標與規劃考量](nctfu_friday_goals.md)。

## 1. 參加與操作方式

- 週五 19:00～21:00 線上；例外日期依下表。
- 會前 2～3 小時嘗試指定題，會後約 1 小時補做。每人至少主責一題，不要求完成全部延伸。
- 第一次確認會議工具、共筆、隊伍、前四次主持人與記錄者。
- 主持人提前 3～5 天公告題目、必要工具與附件，並試跑服務；會中分階段給提示，最後才討論完整解法。
- 每週共筆包含題名、嘗試、證據、卡點、提示來源、重現方式；模擬及正式賽依各自規則使用輔助工具。
- 已完成題目可改由未做過的隊友主責，重現題須標記，不能算未見題成績。
## 2. 每週排程

表內 A～F 是下方有實際題目連結的題組。核心題在課外先嘗試，週五帶著卡點討論；延伸題供主修者深挖。每位社員每週至少主責一題，無須把所有題組全刷完。

| 日期 | 訓練單元與指定材料 | 週五兩小時怎麼用 | 課外任務／驗收 |
|---|---|---|---|
| 9/18 | 六領域診斷與隊伍分工：A1、B1、C1、D1、E1，加 HTTP／Linux 知識盤點 | 15 分鐘規則與目標；60 分鐘各自選兩個不同領域試解；30 分鐘交流；15 分鐘分工 | 記錄「獨立完成／提示後完成／無方向」；每人選主修及副修。診斷不是完整初賽模擬 |
| 9/25 | Reverse／Pwn 判讀：B1、B2、C1，C2 選做 | 20 分鐘字串、控制流程、stack；60 分鐘程式判讀與驗證；40 分鐘錯誤原因與題解 | 主修者完成 B2 或 C2；其他人能說明輸入影響。連假若停辦，改非同步仍須補先備知識 |
| 10/2 | Web／Crypto 弱點判斷：A1、D1，A2、D2 選做 | 20 分鐘六領域快問；70 分鐘按弱項分兩組；30 分鐘互教 | 各組將實作整理成「成立條件、錯誤假設、驗證方法」；HTTP 社課後直接應用，不再教 Burp 介面 |
| 10/9 | 初賽形式模擬：自編 36 題單選，六領域各 6 題 | 90 分鐘隊伍共同作答；30 分鐘檢討 | 題目規格見第 4 節；每人負責解釋一個弱項。連假無法同步則各隊另外約 90 分鐘，最晚 10/14 完成 |
| 10/16 | 賽前錯題校正與規則確認 | 僅 19:00～20:00，自願參加；不開新題，20:00 後休息 | 整理上週錯題與報到資訊；合辦活動隔日、初賽前夕不加壓 |
| 10/23 | 初賽復盤＋Web／逆向深化：A3、B3 | 30 分鐘按知識／判讀／時間分類失分；70 分鐘攻堅新題；20 分鐘確認決賽專攻方向 | 不記憶式拼造官方題目；以可公開資料與自身知識缺口為主，確認各隊主修分工 |
| 10/30 | 段考休息；查看入圍結果 | 不開會 | 晉級者啟動第 5 節額外模擬；未晉級者照後續解題訓練，不改成只有講解 |
| 11/6 | 流量與註冊表鑑識：E2、E4 | 15 分鐘觀察框架；75 分鐘分工實作；30 分鐘證據交流 | 每人交付篩選依據／腳本／資料重組紀錄之一；11/4 Wireshark 社課作為工具背景 |
| 11/13 | Pwn 進階（格式化字串與 Heap）：C3、C4 | 20 分鐘必要概念；70 分鐘主修攻題、副修驗證；30 分鐘交接 | 主修者攻 C3，副修者嘗試 C4，先備不足用 format string 0 補觀念；重現時解釋 offset／行為 |
| 11/20 | 兩小時混合題與停損練習：F 組（全未見新題） | 10 分鐘分工；90 分鐘無提示計時；20 分鐘檢討 | 4 題各領域全新題盲測，每人挑 1 題；記錄何時求助／換題。這是縮短模擬，不等於完整 5 小時決賽 |
| 11/27 | 金盾決賽日 | 晚間不排例行讀書會，讓參賽者休息 | 未參賽者自主練習；正式賽後再依可公開範圍分享 |
| 12/4 | 技能方向試行一：磁碟鑑識 G1 | 20 分鐘檔案系統與證據位置；70 分鐘實作；30 分鐘對照證據 | 交可重現的提取紀錄，回答證據能支持什麼、不能支持什麼 |
| 12/11 | 技能方向試行二：防火牆配置 G2 | 20 分鐘拓撲與允許矩陣；70 分鐘設定；30 分鐘功能／阻擋測試 | 提交規則、允許／拒絕測試結果、重建方式；和 SQLi 社課分工，不重做 SQLi 暖身 |
| 12/18 | 技能方向試行三：規則故障排除 G3＋轉向評估 | 15 分鐘抽情境；60 分鐘排錯；25 分鐘重建與驗證；20 分鐘評估 | 保留證據與回復步驟，決定下學期主攻與環境維護人選 |
| 12/25 | 段考休息 | 不開會 | 不排補課 |

9/25、10/9 的連假與校曆仍待確認。停辦不將多個新單元硬塞下一週；初賽必要知識改個人或隊內完成。上述日期皆為週五。

## 3. 指定題組與實驗

CyLab 題名／ID 以本地 CSV 核對，連結是題名搜尋入口。標為補基礎的題只用來判斷是否需要補課，不能當整場備賽核心。所有題目避開課程 14 題作業，且全學期零重複。

| 編號 | 實際題目 | 用途與完成要求 |
|---|---|---|
| A1 | [SSTI1 #492](https://learn.cylabacademy.org/library?search=SSTI1) | Web 診斷／補基礎：區分輸入被當資料或模板處理 |
| A2 | [SSTI2 #488](https://learn.cylabacademy.org/library?search=SSTI2) | Web 核心：研究限制與替代方式；要解釋測試過程 |
| A3 | [Crack the Gate 1 #520](https://learn.cylabacademy.org/library?search=Crack%20the%20Gate%201) | Web 延伸：黑箱認證繞過與身分邏輯漏洞 |
| B1 | [vault-door-3 #60](https://learn.cylabacademy.org/library?search=vault-door-3) | Reverse 核心：重建字串轉換與驗證流程 |
| B2 | [keygenme-py #121](https://learn.cylabacademy.org/library?search=keygenme-py) | Reverse 延伸：推導合法輸入並獨立驗證 |
| B3 | [Flag Hunters #472](https://learn.cylabacademy.org/library?search=Flag%20Hunters) | Reverse 延伸：二進位特徵與程式邏輯分析 |
| C1 | [Local Target #399](https://learn.cylabacademy.org/library?search=Local%20Target) | Pwn 診斷：輸入、記憶體布局與變數變化 |
| C2 | [buffer overflow 1 #258](https://learn.cylabacademy.org/library?search=buffer%20overflow%201) | Pwn 核心：理解控制流程與測試依據 |
| C3 | [format string 1 #434](https://learn.cylabacademy.org/library?search=format%20string%201) | Pwn 延伸：格式化字串任意記憶體讀寫；先備不足用 [format string 0 #433](https://learn.cylabacademy.org/library?search=format%20string%200) 補觀念 |
| C4 | [heap 0 #438](https://learn.cylabacademy.org/library?search=heap%200) | Pwn 延伸：Heap 堆積記憶體基礎與覆寫概念 |
| D1 | [Dachshund Attacks #159](https://learn.cylabacademy.org/library?search=Dachshund%20Attacks) | Crypto 核心：辨識 RSA 弱參數，解釋攻擊適用條件，不只呼叫現成套件 |
| D2 | [No Padding, No Problem #154](https://learn.cylabacademy.org/library?search=No%20Padding%2C%20No%20Problem) | Crypto 延伸：研究 RSA 代數性質與互動服務 |
| E1 | [Wireshark twoo twooo two twoo... #110](https://learn.cylabacademy.org/library?search=Wireshark%20twoo%20twooo%20two%20twoo...) | 流量核心：定位資料與排除干擾，保留封包證據 |
| E2 | [Trivial Flag Transfer Protocol #103](https://learn.cylabacademy.org/library?search=Trivial%20Flag%20Transfer%20Protocol) | 檔案／協定延伸：從流量提取並分析檔案 |
| E4 | [Riddle Registry #530](https://learn.cylabacademy.org/library?search=Riddle%20Registry) | 鑑識延伸：Windows 註冊表分析與隱藏機碼提取 |

### F：11/20 決賽模擬混合題組（全未見新題，當天盲測公佈）

- **Web**: [Web Gauntlet #88](https://learn.cylabacademy.org/library?search=Web%20Gauntlet)
- **Pwn**: [PIE TIME #490](https://learn.cylabacademy.org/library?search=PIE%20TIME)
- **Crypto**: [StegoRSA #719](https://learn.cylabacademy.org/library?search=StegoRSA)
- **Forensic**: [Binary Digits #698](https://learn.cylabacademy.org/library?search=Binary%20Digits)

F 組為金盾決賽前全真模擬：事前不透露題解，限時 90 分鐘各隊自選題目分工，練習卡關停損與換題決策。真正盲測由帶領者當天公佈連結與題目。

### G：12 月技能方向試行

- **G1：[Disk, disk, sleuth! II #137](https://learn.cylabacademy.org/library?search=Disk%2C%20disk%2C%20sleuth%21%20II)**。使用題目磁碟映像練習提取證據。這是技能方向的橋接題，不是全國技能真題，也不包含完整事件應變。
- **G2：[SEED Firewall Exploration Lab](https://seedsecuritylabs.org/Labs_20.04/Networking/Firewall/)**。使用官方 Labsetup 的網路拓撲，只取 iptables 配置部分；不做核心模組程式撰寫。本組自訂驗收：列出管理流量與一般流量的允許矩陣、實作阻擋／放行、檢查回程流量、保存規則及重建流程。具體位址依官方配置，不在課表猜寫。
- **G3：同一 SEED 環境上的自訂排錯任務**，由另一組置入「先行拒絕遮蔽允許規則」「規則套到錯誤方向／鏈」「回程流量被擋」其中一種，提供服務需求、不直接揭露錯誤。修復後要證明允許項目可用、禁止項目仍被阻擋。這是本組設計的延伸任務，並非官方原題。

G2/G3 的環境需 12/8 前由帶領者試跑，成員於會前下載與啟動。官方有 x86 與 Apple Silicon 的配置選項；依實際設備測試。環境無法運作時，12/11 改為規則推演與測試計畫，實作另約，不能算完成安全強化驗收。


## 4. 初賽模擬卷製作規格

平台實作不等同初賽單選題。9/18～10/9 每位社員以自己主修領域整理概念與短題，來源用平台題幹／已驗證的觀察／官方工具文件。題目須有四選一、唯一答案、理由與來源，由另一位成員覆核。不得宣稱這是金盾歷屆題或預測題。

10/9 的自編模擬卷為 36 題、每類 6 題、90 分鐘，題數是社團自訂，不是官方題數：

| 領域 | 指定涵蓋的判讀點 |
|---|---|
| Web | HTTP 方法與狀態、Cookie、認證／授權、SQLi、SSTI、輸入處理信任邊界 |
| Reverse | 字元與編碼、位元運算、端序、分支迴圈、字串變換、短程式輸出 |
| Pwn | stack／heap、指標與長度、溢出、格式字串、NX／ASLR／PIE／canary 的作用與限制 |
| Crypto | 編碼／雜湊／加密差別、對稱／非對稱、RSA 參數、nonce／IV、模式與填充、弱參數適用條件 |
| Misc | shell 管線、檔案格式、壓縮封裝、權限、正則表達式、基本腳本處理 |
| Forensic | 封包欄位、串流、DNS／HTTP、檔頭、時間戳／時區、證據與推測的區分 |

模擬卷尚待輪值者於 10/5 前編好、10/7 前覆核；本文件已指定範圍與責任，未冒充已存在的題庫。出題者若參加同份測驗，標記已知題，該分數只用於討論，不作盲測成績。錯題須分為「不知道概念／看錯資料／推理錯／時間不足」，避免只抄正解。

## 5. 額外模擬與分流執行

- **晉級**：維持週五，另於 11/14 或 11/15 約一場 5 小時模擬（建議 13:00～18:00，日期待隊員同意）。由不參賽的帶領者挑 6～8 道隊員未做過的實題，涵蓋三個主修以上；未有題目與可用環境前不稱已備妥。各隊使用單一進度板、每 30 分鐘短同步，卡住時記錄求助／換題時間。
- **未晉級**：照常練 A～F，不強制額外五小時；將初賽錯題補完，每人至少在主修方向獨立完成一題原先不會的題。
- **尚未報名／只想學習**：可參與同一讀書會，沒有競賽成果承諾。

若無人能協助準備陌生題，使用公開比賽的可練習題庫，事先核對是否看過；有看過的題必須標記，不用總分推估實際決賽排名。

## 6. 輪值準備與交付

| 項目 | 負責角色 | 截止／執行時間 | 交付物 |
|---|---|---|---|
| 每週帶練 | 當週主持人 | 會前 3～5 天 | 題目連結、環境需求、分階段提示、服務試跑結果 |
| 共筆 | 當週記錄者及各題主責 | 聚會後 | 嘗試、證據、卡點、重現步驟 |
| 初賽模擬卷 | 六領域分工出題、另一人覆核 | 10/5 完稿、10/7 覆核 | 36 題、答案、理由與來源；目前尚未製作 |
| 五小時模擬 | 帶領者與參賽隊 | 建議 11/14 或 11/15，隊員確認後執行 | 6～8 題未見題、可用環境、計時及分工紀錄；目前未備妥 |
| 防火牆實驗 | G2/G3 主持人 | 12/8 前試跑 | 可啟動環境、需求矩陣、允許／拒絕測試 |
| 故障情境 | G3 出題組 | 12/18 前 | 一種規則故障、服務需求、還原方法；目前未置入故障 |
| 轉向評估紀錄 | 全體成員 | 12/18 最後 20 分鐘 | 依 B3 的三項判斷記錄意願、能力及維護人選 |
## 7. 題目核對與準備狀態

- [本地 CyLab 題庫快照](../../security/challenges/platforms/cylab_picoctf/cylab_all_challenges_2026-08-08.csv)：核對本表 CyLab 題名／ID；線上搜尋連結沿用本地平台格式，目前附件、服務與耗時未逐題通關驗證。
- [雙平台題庫規劃](../lab/90_runs/checklists/combined_90_runs_challenges.md)、[CyLab 題庫規劃](../lab/90_runs/checklists/picoctf_90_runs.md)：只參考主題結構，舊表部分 ID 與 CSV 不符，不直接沿用。
- [既有課程作業](cylab_course_assignments.md)：E3 與既有作業重複，其他本版 CyLab 題目避開該 14 題清單。
- [金盾競賽要點](https://csc.nics.nat.gov.tw/shield.aspx) 與 [SEED Firewall Exploration Lab](https://seedsecuritylabs.org/Labs_20.04/Networking/Firewall/) 已於 2026-09-08 讀取官方頁面。
- 10/9 自編卷、額外五小時模擬卷及 G3 故障環境屬後續輪值準備事項；此文件是完整排程與選題方案，不是已建好的所有訓練材料。



