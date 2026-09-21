# 國立中央大學資訊管理學系《電腦網路安全》
# 🧪 114學年度 CyLab (picoCTF) 課後加分作業題庫規劃指南 (14 道精選實作題)

> **課程名稱**：中央資管 114 學年度《電腦網路安全》（授課教師：陳奕明 教授）  
> **作業屬性**：CyLab 個人加分實作作業 (Bonus Lab Assignments)  
> **適用平台**：**CMU CyLab / picoCTF 官方題庫**（100% 嚴格源自本地題庫 [`cylab_all_challenges_2026-08-08.csv`](../../security/practice/challenges/platforms/cylab_picoctf/cylab_all_challenges_2026-08-08.csv)，含官方題目 ID）  
> **規劃規格**：共 **14 道題目**（完全滿足一學期至少 12 題以上之要求），嚴格對照 16 週各單元講義進度，兼具鑑別度與務實抑制 AI 複製貼上之題型設計。

---

## 🎯 一、 題庫設計原則與三大檢核維度

針對本課程之加分作業，本規劃依循四大原則：
1. **課程進度嚴密吻合**：每一道題目均直接呼應陳奕明教授各週 Handout 講義中的核心觀念（如 Eavesdropping、Reconnaissance、Sniffing、Authentication、Policy/Sudo、Audit Log、Firewall Method、NIDS/Anomaly、Substitution、RSA 等）。
2. **鑑別度階梯分明**：
   - **基礎得分題（6 題）**：只要肯動手開啟工具、跟隨課堂進度即可解出，保障認真同學的基本加分。
   - **中級進階題（5 題）**：需要理解多步驟過濾、黑箱字元測試或協定握手，檢驗實務排查能力。
   - **高手挑戰題（3 題）**：如隱蔽通道 Python 腳本解析、人工頻率分析、RSA 因數分解，專供實力頂尖的同學拉開差距。
3. **務實抑制 AI 直接求解 (Resilience to Direct AI Prompts)**：
   - **拒絕純文字複製秒殺題**：摒棄只要貼 3 行題幹字串給 ChatGPT 就能 0.5 秒吐出 Flag 的題目。
   - **優先挑選非文字/檔案載體 (Attachment-based)**：高達 7 題為 `.pcap` 流量側錄檔、大容量伺服器日誌或二進位檔案。AI 在處理未經提取的二進位封包時容易產生欄位遺漏與幻覺，迫使學生必須親自開啟 Wireshark / 終端機進行排查。
   - **納入最新與冷門題庫（2025~2026）**：挑選網路上無現成 Writeup 之新題，AI 無法依靠資料庫「背答案」。
4. **貼近現實平台操作流程**：完全採用 CyLab 標準流程（學生於平台操作、取得 Flag、在平台輸入框提交比對得分），不需額外架設繁複外部機制。

---

## 📊 二、 14 週課程對應與題目矩陣一覽表

| 週次 | 課綱進度單元 | 對應講義投影片概念 | CyLab ID | 官方題目名稱 (picoCTF) | 官方分類 | 難度 / 分數 | 鑑別度層級 | AI 求解阻力與防作弊核心特點 |
| :---: | :--- | :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| **W2** | **Types of Attacks** | Lesson 2 P.4: Eavesdropping (被動監聽) | **#286** | **Packets Primer** | Forensics | 難度 2 / 100 pt | ⭐ 基礎 | **二進位 PCAP 檔**：AI 無法直接看封包流，學生需開啟 Wireshark 追蹤 TCP 串流找出明文外洩。 |
| **W3** | **Hacker Techniques I** | Lesson 3 P.35: Reconnaissance & 探測 | **#757** | **ping-cmd** | General | 難度 1 / 100 pt | ⭐⭐ 中級 | **2026 新題無現成題解**：黑箱過濾黑名單，AI 給的通用指令會被阻擋，需手工嘗試 Linux 替代符號。 |
| **W4** | **Hacker Techniques II** | Lesson 3 P.19~P.20: Sniffing 交換網路嗅探 | **#30** | **shark on wire 1** | Forensics | 難度 2 / 150 pt | ⭐⭐ 中級 | **海量雜訊封包排查**：內含數百個 UDP 封包與假資料流，AI 讀檔極易抓錯假 Flag，需手動過濾串流。 |
| **W5** | **Security Services** | Lesson 4 P.15~P.18: Authentication 鑑別服務 | **#278** | **Local Authority** | Web | 難度 1 / 100 pt | ⭐ 基礎 | **Web 前端認證缺陷**：代碼將密碼明文放於前端 JS，直接印證講義「認證未在伺服端執行之致命傷」。 |
| **W7** | **Policy & Risk** | Lesson 6 P.5~P.8: 最小特權原則與存取控制 | **#735** | **SUDO MAKE ME A SANDWICH** | General | 難度 1 / 50 pt | ⭐⭐ 中級 | **2026 新題 + SSH 互動**：需連入臨時靶機檢視 `sudo -l` 政策，找出違規特權配置，AI 無法憑空給 Flag。 |
| **W9** | **Security Process & ISMS** | Lesson 8 P.15: 稽核軌跡 (Audit Trails) 與日誌 | **#527** | **Log Hunt** | General | 難度 1 / 50 pt | ⭐ 基礎 | **大容量日誌資料**：超大檔案無法直接貼入 Prompt，學生需在 Linux 終端機練習寫 `grep`/`awk` 過濾攻擊痕跡。 |
| **W10** | **Firewall** | Lesson 10 P.4~P.11: 封包過濾規則與方法漏洞 | **#132** | **GET aHEAD** | Web | 難度 1 / 20 pt | ⭐⭐ 中級 | **協定 Method 盲點**：伺服器過濾了 GET/POST 但放行 HEAD，需使用 `curl -I` 或 Burp 手動構造封包。 |
| **W10** | **Firewall** | Lesson 10 P.12: WAF / L7 代理與正則比對 | **#356** | **MatchTheRegex** | Web | 難度 2 / 100 pt | ⭐⭐ 中級 | **規則語意分析**：解析正規表達式邏輯邊界，動態在靶機前端構造可穿透檢驗之字串。 |
| **W12** | **VPN** | Lesson 11 P.3~P.5: 加密隧道與遠端安全存取 | **#424** | **Super SSH** | General | 難度 1 / 25 pt | ⭐ 基礎 | **加密連線實作**：連線臨時動態生成之 SSH 靶機，完成非對稱金鑰指紋核驗並建立通道。 |
| **W13** | **Intrusion Detection** | Lesson 13 P.9~P.11: NIDS 與未加密流量外洩 | **#115** | **Wireshark doo dooo do doo...** | Forensics | 難度 2 / 50 pt | ⭐⭐ 中級 | **多階段取證流程**：PCAP 檔中尋找可疑通訊，截獲之亂碼需自行辨識出 ROT13 進行還原，AI 難以一鍵直出。 |
| **W13** | **Intrusion Detection** | Lesson 13 P.5: 異常偵測 (Anomaly) 與隱蔽信道 | **#84** | **shark on wire 2** | Forensics | 難度 2 / 300 pt | ⭐⭐⭐ 高手 | **頂級鑑別度！** 資訊隱藏於 UDP 目的端口增量中，AI 無法看破，需自行撰寫 Python 封包提取腳本。 |
| **W14** | **Foundation of Encryption** | Lesson 12 P.10~P.11: 替代式密碼與頻率分析 | **#309** | **substitution2** | Crypto | 難度 2 / 100 pt | ⭐⭐⭐ 高手 | **抗 AI 幻覺題**：單表代換隨機映射，整篇丟 AI 容易產生單字腦補幻覺，需藉助雙字母頻率表手動推導。 |
| **W14** | **Foundation of Encryption** | Lesson 12 P.15, P.29: 密碼雜湊與 Unix 密碼破解 | **#475** | **hashcrack** | Crypto | 難度 1 / 100 pt | ⭐⭐ 中級 | **離線算力破解**：單向雜湊無法對話框反算，需使用 John the Ripper / Hashcat 配合字典檔進行運算碰撞。 |
| **W15** | **Applications of Encryption**| Lesson 12 P.22~P.26: RSA 演算法與質因數分解 | **#470** | **EVEN RSA CAN BE BROKEN???** | Crypto | 難度 1 / 200 pt | ⭐⭐⭐ 高手 | **數學邏輯鑑別題**：大數 $N$ 挑選結構有缺陷，需推導費馬分解法或質數弱點，撰寫 Python 解出私鑰 $d$。 |

---

## 📝 三、 14 道加分題目詳細設計與教學導引

### 🚩 [W2 加分題] Packets Primer (CyLab ID: 286)
- **課綱對應**：第 2 週《Types of attacks》
- **講義知識點**：`Lesson 2 P.4` —— **Eavesdropping (被動監聽)**。
- **官方屬性**：Forensics ｜ 難度 2 ｜ 100 分
- **題目檔案**：提供二進位流量封包檔 `packets.pcap`。
- **解題核心概念**：
  在傳統 Shared Media 或未加密網段中，攻擊者可藉由網卡監聽任何通過的封包。學生需下載該 PCAP 檔，在 Wireshark 中定位 TCP 通訊，點擊右鍵選擇「Follow」➔「TCP Stream」，即可看見未加密協議中以明文直接洩漏的 Flag。
- **AI 阻力與鑑別度**：
  學生無法直接複製題目文字丟給 AI。作為學期第一道加分題，它能有效破除「只用瀏覽器」的習慣，引導學生親自下載並熟悉資安標準工具 Wireshark 的介面。

---

### 🚩 [W3 加分題] ping-cmd (CyLab ID: 757)
- **課綱對應**：第 3 週《Hacker Techniques I》
- **講義知識點**：`Lesson 3 P.35~P.36` —— **Internet Reconnaissance（主機探測與指令執行）**。
- **官方屬性**：General Skills ｜ 難度 1 ｜ 100 分 (picoCTF 2026)
- **題目環境**：提供一個 Web 輸入框，表面上供使用者輸入 IP 執行 ping 偵測。
- **解題核心概念**：
  後端程式直接將使用者輸入拼接到系統 shell 中執行。學生需利用 Linux 指令拼接符號（如 `;`、`&&`、`|`）進行 Command Injection，越權讀取系統內的檔案。
- **AI 阻力與鑑別度**：
  **2026 年新題，網路上無公開 writeup**。且題目後端設計了過濾黑名單，AI 給的制式 Payload（如 `; cat flag.txt`）會被直接擋下，學生必須親自在靶機介面上嘗試換行、萬用字元或替代指令。

---

### 🚩 [W4 加分題] shark on wire 1 (CyLab ID: 30)
- **課綱對應**：第 4 週《Hacker Techniques II》
- **講義知識點**：`Lesson 3 P.19~P.20` —— **Sniffing Switch Networks（交換網路監聽與流量過濾）**。
- **官方屬性**：Forensics ｜ 難度 2 ｜ 150 分
- **題目檔案**：包含數百個 UDP 封包的流量側錄檔 `capture.pcap`。
- **解題核心概念**：
  真實網路環境中充滿了雜訊。題目在不同的 UDP 串流中塞入了大量干擾封包與虛假字串。學生需學會使用 Wireshark 顯示過濾器（例如 `udp.stream eq X`），依序排查不同對話串流，才能找到隱藏在特定傳輸中的真實 Flag。
- **AI 阻力與鑑別度**：
  若學生把二進位封包直接丟給具備檔案分析能力的 AI，AI 極易在多個假資料流中迷失並抓錯 Flag。學生必須親自翻查串流並辨識出哪一個才是有效 payload。

---

### 🚩 [W5 加分題] Local Authority (CyLab ID: 278)
- **課綱對應**：第 5 週《Security Services》
- **講義知識點**：`Lesson 4 P.15~P.18` —— **Identification & Authentication (身份鑑別服務與機制失當)**。
- **官方屬性**：Web Exploitation ｜ 難度 1 ｜ 100 分
- **題目環境**：包含帳號與密碼輸入框的網站登入頁面。
- **解題核心概念**：
  開發者誤將身份驗證邏輯實現在前端客戶端。學生按下 F12 開啟瀏覽器開發者工具，檢視載入的 JavaScript（`secure.js`），即可發現硬編碼 (Hardcoded) 的帳號與密碼，直接登入取得 Flag。
- **教學呼應**：
  完美對標講義所強調的「身份鑑別必須在信任邊界（伺服端）內嚴格校驗，任何置於客戶端的安全檢查皆為無效防護」。

---

### 🚩 [W7 加分題] SUDO MAKE ME A SANDWICH (CyLab ID: 735)
- **課綱對應**：第 7 週《Policy and Risk Management》
- **講義知識點**：`Lesson 6 P.5~P.8` —— **Information Policy & 最小特權原則 (Principle of Least Privilege)**。
- **官方屬性**：General Skills ｜ 難度 1 ｜ 50 分 (picoCTF 2026)
- **題目環境**：提供 SSH 連線位址與一般使用者帳號密碼。
- **解題核心概念**：
  管理員配置系統時違反了最小權限原則。學生連線進入 Linux 主機後，執行 `sudo -l` 檢視被授權執行的特殊指令，利用特定二進位執行檔的提權特性（GTFOBins 手法）突破限制讀取敏感檔案。
- **AI 阻力與鑑別度**：
  2026 新題無現成答案。學生若不親自連入主機下達探索指令，AI 根本無法預知該虛擬機內的 sudoers 配置。

---

### 🚩 [W9 加分題] Log Hunt (CyLab ID: 527)
- **課綱對應**：第 9 週《Security Process and ISMS》
- **講義知識點**：`Lesson 8 P.15~P.17` —— **Incident Response & 稽核軌跡 (Audit Trails)**，`Lesson 13 P.7` 日誌分析器。
- **官方屬性**：General Skills ｜ 難度 1 ｜ 50 分 (picoMini)
- **題目檔案**：包含大量伺服器運作日誌的記錄檔集合。
- **解題核心概念**：
  在海量系統事件日誌中，駭客入侵時會留下時間、IP 與非正常操作軌跡。學生需在 Linux 環境中使用 `grep`、正規表達式與管線過濾指令，精確鎖定異常日誌行並拼湊出 Flag。
- **AI 阻力與鑑別度**：
  大容量文字檔案會超過一般 AI 視窗的處理極限。學生必須練習在本地終端下達精確的文字搜尋指令。

---

### 🚩 [W10 加分題 1] GET aHEAD (CyLab ID: 132)
- **課綱對應**：第 10 週《Firewall》
- **講義知識點**：`Lesson 10 P.4~P.11` —— **Packet Filtering / 應用層過濾規則設計盲點**。
- **官方屬性**：Web Exploitation ｜ 難度 1 ｜ 20 分
- **題目環境**：網頁提供紅/藍切換按鈕，分別向伺服器發送 GET 與 POST。
- **解題核心概念**：
  過濾規則僅攔截或回應了常見的 GET 與 POST，但伺服器支援所有 HTTP 規範方法。學生必須使用 `curl -I` 或 Burp Suite 手工發送 HTTP `HEAD` 請求，Flag 便會藏在伺服器回傳的 HTTP Header 中。
- **教學呼應**：
  直接呼應陳老師投影片 P.7~P.11 所討論的「封包過濾規則若未全面考慮所有協定細節，攻擊者只要稍微更換 Method 即可穿透防線」。

---

### 🚩 [W10 加分題 2] MatchTheRegex (CyLab ID: 356)
- **課綱對應**：第 10 週《Firewall》
- **講義知識點**：`Lesson 10 P.12` —— **Application Layer Firewalls (WAF 語意解析與正規表達式過濾)**。
- **官方屬性**：Web Exploitation ｜ 難度 2 ｜ 100 分
- **題目環境**：Web 輸入表單，後端以正規表達式校驗輸入內容。
- **解題核心概念**：
  現代應用層防火牆 (WAF) 深度仰賴正規表達式 (RegEx) 進行攻擊特徵比對。學生需逆向分析該正則規則（查看特殊符號 `^`, `$`, `*`, `[]` 的配對範圍），構造出能滿足驗證條件的特殊字串。
- **AI 阻力與鑑別度**：
  AI 雖然懂正則語法，但常會忽略邊界字元的寬鬆定義。學生必須親自將構造出的字串提交到靶機驗證。

---

### 🚩 [W12 加分題] Super SSH (CyLab ID: 424)
- **課綱對應**：第 12 週《Virtual Private Networks》
- **講義知識點**：`Lesson 11 P.3~P.5, P.24` —— **VPN / 加密隧道與遠端安全存取**。
- **官方屬性**：General Skills ｜ 難度 1 ｜ 25 分
- **題目環境**：系統動態生成之 SSH 伺服器主機、Port 與連線密碼。
- **解題核心概念**：
  SSH 與 SSL-VPN 均使用相同的傳輸層端對端加密機制。學生需打開終端機，執行 `ssh -p <port> user@host`，經歷主機公鑰指紋 (Host Key Fingerprint) 驗證與加密連線建立，登入後即可取得 Flag。
- **教學呼應**：
  讓學生親身體驗安全通訊協定在建立隧道時的認證握手歷程。

---

### 🚩 [W13 加分題 1] Wireshark doo dooo do doo... (CyLab ID: 115)
- **課綱對應**：第 13 週《Intrusion Detection》
- **講義知識點**：`Lesson 13 P.9~P.11` —— **NIDS（網路入侵偵測與未加密流量檢視）**。
- **官方屬性**：Forensics ｜ 難度 2 ｜ 50 分
- **題目檔案**：邊界 IDS 側錄之 `shark.pcap` 檔案。
- **解題核心概念**：
  NIDS 能夠側錄網路所有通訊，但面對加密或編碼流量時需要輔助分析。學生需在 Wireshark 中過濾出疑似惡意通訊的封包，發現其文字經過了凱撒密碼 (ROT13) 變換，需進一步進行代換還原出明文 Flag。
- **AI 阻力與鑑別度**：
  封包搜尋 + 密碼辨識雙重流程，AI 無法直接在對話框幫學生點開 Wireshark 找封包。

---

### 🚩 [W13 加分題 2] shark on wire 2 (CyLab ID: 84)
- **課綱對應**：第 13 週《Intrusion Detection》
- **講義知識點**：`Lesson 13 P.5` —— **Anomaly Detection（異常偵測與隱蔽通道 Covert Channel）**。
- **官方屬性**：Forensics ｜ 難度 2 ｜ 300 分
- **題目檔案**：包含大量異常 UDP 流量之 `capture.pcap`。
- **解題核心概念**：
  **【高鑑別度挑戰題】** 駭客為了逃避特徵碼型 IDS 偵測，將機密資料隱藏在數十個 UDP 封包的「目的通訊埠號 (Destination Port)」中（例如 Port 5065 代表 ASCII 碼 65 即字元 'A'）。
- **AI 阻力與鑑別度**：
  **AI 根本無法直接看出這份 PCAP 的玄機！** 學生必須自行分析封包特徵，發現端口異常規律後，撰寫 Python 腳本（使用 Scapy 或 pyshark）自動化提取封包端口並轉換為字元。能獨立解出此題的學生具備頂尖資安實作水準。

---

### 🚩 [W14 加分題 1] substitution2 (CyLab ID: 309)
- **課綱對應**：第 14 週《Foundation of Encryption》
- **講義知識點**：`Lesson 12 P.10~P.11` —— **Substitution Ciphers（單表代換密碼與英文字母頻率分析）**。
- **官方屬性**：Cryptography ｜ 難度 2 ｜ 100 分
- **題目檔案**：一段長篇的隨機字母代換密文。
- **解題核心概念**：
  對標講義 P.11 的 Caesar/Substitution 原理。雖然每個字母被隨機映射，但英文字母出現的頻率（如 E, T, A, O）與常見雙字母組合（th, he, in）維持不變。學生需利用頻率分析工具逐步猜測並還原對照表。
- **AI 阻力與鑑別度**：
  **高度抗 AI 題**。若將隨機替換的密文丟給 AI，AI 經常會「腦補」字典裡的英文單字，導致 Flag 內部的非標準單字或混淆字符被徹底改壞。學生必須親自手動校對置換表。

---

### 🚩 [W14 加分題 2] hashcrack (CyLab ID: 475)
- **課綱對應**：第 14 週《Foundation of Encryption》
- **講義知識點**：`Lesson 12 P.15` Unix 密碼雜湊，`P.29` Secure Hash Functions。
- **官方屬性**：Cryptography ｜ 難度 1 ｜ 100 分
- **題目內容**：提供多組單向雜湊值（Hash Values）。
- **解題核心概念**：
  單向雜湊函數不可逆。學生必須在本機安裝密碼破解工具（如 John the Ripper 或 Hashcat），掛載字典檔（如 `rockyou.txt`）進行離線碰撞計算，體會密碼強度與字典長度對破解時間的影響。
- **AI 阻力與鑑別度**：
  AI 在對話框內沒有算力或彩虹表可反算雜湊，學生必須親自操作資安算力工具。

---

### 🚩 [W15 加分題] EVEN RSA CAN BE BROKEN??? (CyLab ID: 470)
- **課綱對應**：第 15 週《Applications of Encryption》
- **講義知識點**：`Lesson 12 P.22~P.26` —— **RSA 演算法數學原理與質因數分解**。
- **官方屬性**：Cryptography ｜ 難度 1 ｜ 200 分
- **題目內容**：給予較大的 RSA 公鑰參數 $N, e$ 與密文 $C$。
- **解題核心概念**：
  **【高鑑別度挑戰題】** RSA 的安全性立基於大數分解的困難度。本題之模數 $N$ 的質因數挑選存在數學漏洞（例如兩個質數過於接近，符合費馬因數分解法條件）。學生需理解 RSA 數學架構，撰寫 Python 腳本分解出 $p, q$，進而求得私鑰 $d = e^{-1} \pmod{(p-1)(q-1)}$ 並解密出 Flag。
- **AI 阻力與鑑別度**：
  考驗學生對密碼學核心數學邏輯的掌握度，需親自推導公式並編寫運算腳本。

---

## 📈 四、 成績核算與評分階梯建議

建議助教與授課老師可按以下方式計入學期個人作業或加分：
1. **及格基礎門檻（完成任意 8 題）**：
   - 適合跟隨進度操作基礎題（如 #286, #278, #132, #424, #527 等）的同學，可穩拿基礎加分 80 分。
2. **優良進階門檻（完成任意 12 題）**：
   - 滿足學期加分上限（100 分），需具備基本 Wireshark 篩選與黑箱探測能力。
3. **滿分與資安榮譽挑戰（全數完成 14 題）**：
   - 凡能完整攻克 **#84 (UDP 隱蔽通道腳本)**、**#309 (人工頻率分析)** 與 **#470 (RSA 數學分解)** 之同學，代表具備極佳的資安實作天賦，建議直接推薦加入資安社競賽隊伍培訓！
