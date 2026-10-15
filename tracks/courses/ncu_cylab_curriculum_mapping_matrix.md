# 🧭 中央資管《電腦網路安全》與 picoCTF 課程對齊方向指導綱領
## 雙向維度分析：課程進度章節視角 ＆ picoCTF 官方分類視角

> **文檔定位**：釐清「大學部資管課堂（陳奕明教授講義）」與「picoCTF (CyLab) 題庫」的真實交集與選題方向。  
> **核心指導原則**：
> 1. **允許學生安裝基礎工具**：學生具備資訊專業背景，可安裝與使用 Wireshark、Python 直譯器、標準終端機 (SSH) 及瀏覽器。
> 2. **本表不列具體題目，純留方向**：聚焦於「為什麼該章節該往這個方向找題」與「題庫分類的真實邊界」。
> 3. **誠實區分適用性**：管理與法規章節不強塞 CTF；技術章節則只留吻合講義原理的精準切入方向。
> 4. **明示「零門檻瘦身」取捨**：本表刻意排除需重裝工具或撰寫腳本的題型（記憶體鑑識、Ghidra 反組譯、RSA 數論、進階隱寫等）。這是為降低入門門檻的**主動取捨**，代價是捨棄 picoCTF 相當一部分深度內容，並非那些題型不重要——進階學員仍應另行補足。

---

## 📑 表一：依課程進度排序 (Lesson 1 ~ Lesson 13)

> **色階圖例（僅表示「教學契合度」，與工具門檻分開看）**：🟢 高度契合，可直接作為實作主軸｜🟡 中度／僅概念體驗，能印證原理但不宜深入｜🔴 不適合，回歸案例與制度教學｜🔵 現代拓展，加分選修。工具門檻另見表二「必備環境」欄。

| 講義章節 | 課堂核心觀念 (Lecture Concepts) | 本課適用度 | 建議查找方向 (Target Direction) | 為何是此方向？（原理與教學目的） |
| :--- | :--- | :---: | :--- | :--- |
| **Lesson 1**<br>What Is InfoSec? | • 資安是流程，非單點產品<br>• 隱藏不等於安全 (Obscurity ≠ Security)<br>• BLP 模型 (MLS) | ⚠️ **觀念破冰** | **基礎編碼破除迷思 ＆ 原始碼邊界認知** | 初學者常誤認「Base64/Hex 編碼就是加密」或「前端反灰就安全」。對應兩條皆零門檻又有價值的觀念軸：<br>(A) **編碼 ≠ 加密**：以 Base64/Hex 解碼，釐清編碼、加密、雜湊三者的差別。<br>(B) **隱藏 ≠ 安全**：檢視前端隱藏元素與原始碼註解，示範「藏起來」不等於保護。<br>註：BLP/MLS 多層次存取模型屬純理論，picoCTF 無對應題型，以講義與案例講授即可，不列查找方向。 |
| **Lesson 2**<br>Types of Attacks | • **Access Attacks**: Snooping 窺探, Eavesdropping 竊聽<br>• **Modification Attacks**: 竄改完整性<br>• **DoS & Repudiation** | 🟢 **高度適合** | **方向 1：未加密通訊側錄 (Eavesdropping)**<br>**方向 2：公開檔案窺探與參數竄改 (Snooping / Tampering)** | **【雙軌對應】**<br>1. **封包軌**：開啟 PCAP 檔，直接觀察未加密通訊在網路上洩漏明文。<br>2. **瀏覽器軌**：翻閱公開未保護檔案，或在前端竄改 Cookie/參數改變伺服器行為。 |
| **Lesson 3**<br>Hacker Techniques | • **Reconnaissance**: 網路探測, Google Hacking<br>• **Sniffing switch networks**: ARP/DNS 欺騙<br>• **Buffer overflow**: 記憶體覆寫歷史手法<br>• **Malicious code**: 病毒/木馬/Rootkit 特徵 | 🟢 **極高度適合** | **方向 1：網站公開情資探測 (Web Reconnaissance)**<br>**方向 2：交換網路嗅探與會話排查 (Switch Sniffing)**<br>**方向 3：危險函式原始碼審查 ＆ 緩衝區溢出概念 (Buffer Overflow Concept)**<br>**方向 4：二進位特徵字串提取 (Malware Strings Analysis)** | **【四大手法對應】**<br>1. 探測軌：爬蟲規則 (`/robots.txt`) 與源碼註解檢視。<br>2. 嗅探軌：利用 Wireshark 分析遭 ARP 毒化之流量，練習切換串流排除雜訊。<br>3. 溢出軌：以閱讀 C 原始碼辨識 `gets`／`strcpy` 等危險函式為主（理解溢出成因）；輔以超長字串觸發 Segfault 的崩潰示範。offset 計算與控制流劫持已排除，勿讓學生誤以為能就此完成 pwn。<br>4. 惡意程式軌：對標講義 YARA 規則，使用字串工具在二進位檔內尋找硬編碼特徵。 |
| **Lesson 4**<br>Security Services | • **Authentication**: 身分鑑別服務<br>• **Access Control**: 存取控制與越權<br>• 信任邊界原則 (Server-side 驗證) | 🟢 **極高度適合** | **方向 1：身分鑑別繞過 (Authentication Bypass)**<br>**方向 2：權限越權 (Access Control Bypass)** | 印證講義最核心原則：身分驗證必須在伺服端信任邊界內執行。<br>方向鎖定：前端 JavaScript 驗證缺陷、硬編碼帳密、以及偽造身分屬性（如修改 `admin=true`）。 |
| **Lesson 5**<br>Legal Issues | • 智慧財產權、電腦犯罪法規<br>• 隱私權保護與法律責任 | 🔴 **不適合** | **❌ 不宜配題** | 本單元純屬法律條文、法規遵從與司法判例，適合真實個案研討（Case Study），CTF 競賽平台無此題型，硬配只會適得其反。 |
| **Lesson 6**<br>Policy | • 最小特權原則 (Least Privilege)<br>• 職責分離 (Separation of Duties)<br>• 組織密碼與設備規範 | 🔴 **不適合** | **❌ 不宜配題** | 資安政策是組織管理規範與內控機制，屬於制度面。切勿把 Linux 提權或 Git 紀錄硬凹成政策題，應以企業政策審查案例教學。 |
| **Lesson 7**<br>Managing Risks | • 風險評估矩陣 (Risk Matrix)<br>• 威脅與脆弱性識別<br>• 風險處置策略 (減緩/轉移/接受) | 🔴 **不適合** | **❌ 不宜配題** | 屬於標準資訊管理學之風險量化與質化分析，CTF 題庫完全沒有對應場景，硬配只會模糊焦點。 |
| **Lesson 8**<br>Security Process | • ISMS 流程與 PDCA 循環<br>• 事件應變 (Incident Response)<br>• 稽核軌跡 (Audit Trails) | 🔴 **不適合** | **❌ 不宜配題** | 屬於管理體系規範（如 ISO 27001），適合搭配企業 SOC 應變流程案例探討，不適合使用解題式 CTF。 |
| **Lesson 10**<br>Firewall | • 封包過濾規則 (Packet Filtering)<br>• 應用層 WAF 與正規表達式<br>• 黑名單過濾盲點 (Method Bypass) | 🟡 **中度適合** | **方向：請求方法盲點 (Method Bypass) ＆ 簡易過濾繞過** | 聚焦於「規則盲點」：展示伺服器只擋 GET 卻放行 HEAD（如使用 `curl -I`）；或構造特定字串突破正規表達式檢查，印證黑名單過濾的不完美性。 |
| **Lesson 11**<br>VPN | • 隧道模式 (Tunnel) vs 傳輸模式<br>• IPsec, SSL-VPN<br>• 端對端加密 vs 明文傳輸 | 🟡 **中度適合** | **方向：加密連線通道驗證 (SSH/SSL) ＆ 傳輸防護概念** | 透過終端機連入 SSH 靶機，經歷主機公鑰指紋核驗與建立加密通訊通道，體會加密傳輸協定取代傳統明文通訊（Telnet/HTTP）的必要性。 |
| **Lesson 12**<br>Encryption | • 對稱 (DES/AES) vs 非對稱 (RSA)<br>• 單向雜湊 (Hash: MD5/SHA) 完整性<br>• 數位簽章與不可否認性 | 🟡 **中度適合** | **方向 1：單向雜湊不可逆性與完整性**<br>**方向 2：弱密碼雜湊反查與字典比對**<br>**方向 3：簡易對稱加密體驗 (ROT13/Caesar/XOR)** | **【堅決不選複雜數學算法推導題】**<br>驗證 Hash 的雪崩效應與完整性；以字典比對／線上雜湊反查理解弱密碼風險；並用 ROT13/Caesar/XOR 直觀體會對稱加密的位移與替換。排除 RSA 數論與長篇手動頻率分析。 |
| **Lesson 13**<br>Intrusion Detection | • NIDS (網路型) vs HIDS (主機型)<br>• 特徵碼比對 (Signature-based)<br>• 異常流量檢測 (Anomaly-based) | 🟡 **中度適合** | **方向：NIDS 流量特徵碼過濾排查 (Signature Filtering)** | 在 PCAP 側錄檔中，利用 Wireshark 過濾器比對攻擊特徵簽章（如特定通訊協定、異常 Payload、未加密外洩痕跡），扮演 NIDS 分析師角色。 |

> **📝 關於 Lesson 9**：本表由 Lesson 8 直接銜接 Lesson 10，Lesson 9 刻意未列入對齊（非漏植）。該堂內容未對應到適合的 CTF 題型，故不配題。確切主題請以陳奕明教授講義課綱為準，若該堂含可對齊之技術觀念，再依序補列。

---

## 📑 表二：依 picoCTF 官方分類排序 (Category Perspective)

| picoCTF 官方分類 | 庫存題數 (CSV) | 本課適用度 | 必備環境 / 工具 | 可對應講義章節 | 課堂選題「建議方向」 | 嚴格剔除的地雷方向 (Must Exclude) |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **Web Exploitation**<br>(網頁安全) | **83 題** | 🟢 **極高**<br>(核心支柱) | 瀏覽器 (Chrome/Edge F12) | **L2, L3, L4, L10** | • 網頁原始碼與註解探測<br>• 爬蟲目錄探測 (`/robots.txt`)<br>• 前端身分驗證邏輯繞過<br>• Cookie 與參數竄改<br>• HTTP 請求方法盲點繞過 | ❌ 需安裝重度掃描工具或本機架設伺服端者<br>❌ 需編寫大量自動化發包腳本者 |
| **Forensics**<br>(數位鑑識 / 流量) | **86 題** | 🟢 **極高**<br>(核心支柱) | **Wireshark** / `exiftool`·`strings` | **L2, L3, L13** | • **未加密 TCP/UDP 流量側錄分析**<br>• **ARP 毒化與交換網路會話排查**<br>• **多串流切換與雜訊過濾**<br>• **NIDS 惡意通訊特徵比對**<br>• **檔案中繼資料與夾帶字串檢視**：以 `exiftool` 讀中繼資料、或對檔案跑 `strings` 找藏字串，建立「資料常藏在檔案角落」的鑑識直覺 | ❌ 記憶體 Dump (Volatility 分析)<br>❌ 磁碟映像檔 (Sleuthkit / Autopsy)<br>❌ 需撰寫 Python Scapy 提取隱蔽通道者<br>❌ 圖片盲水印、LSB 位元平面、需 Stegsolve 之深層隱寫術（簡易中繼資料／strings 檢視不在此限） |
| **General Skills**<br>(通用技能) | **75 題** | 🟢 **高度** | 終端機 (SSH) / 基礎命令 | **L1, L11, L12** | • SSH 加密連線通道體驗與指紋驗證<br>• 基礎資料表示法與編碼轉換 (Base64/ASCII)<br>• 伺服器文字日誌基礎過濾<br>• **版控歷史洩密排查**：以 `git log`／`git show` 翻提交歷史，找出誤入版控的 flag／密鑰（對應「敏感資料誤入版本庫」此真實資安風險） | ❌ 純 Linux 核心除錯或特殊命令雜技<br>❌ Git 內部物件／版本庫結構原理探索（偏工具內部、與資安脫節；翻歷史找洩密不在此限） |
| **Binary Exploitation**<br>(二進位安全 / PWN) | **76 題** | 🟡 **原始碼審查** | 標準終端機 / 文本編輯器（讀 C 原始碼） | **L1, L3** | • **危險函式與邊界缺陷審查（主）**：閱讀題目附帶的 C 原始碼，辨識 `gets`／`strcpy`／`scanf("%s")` 等無邊界檢查函式，從源頭理解溢出成因——相關、零門檻、有實質教學價值<br>• **緩衝區溢出「現象」示範（次）**：以超長字串觸發 Segfault，僅觀察崩潰現象，不進入 offset 計算與記憶體覆寫利用 | ❌ 計算記憶體偏移量、構造 ROP 鏈<br>❌ Shellcode 編寫、ASLR/Canary 繞過<br>❌ 暫存器級別之 GDB 動態調試 |
| **Reverse Engineering**<br>(逆向工程) | **102 題** | 🟡 **分析實作** | 字串工具 (`strings`) / 文本編輯器 / Python | **L3** | • **二進位靜態特徵提取 (Strings Analysis)**：對標講義 YARA 規則，提取執行檔內硬編碼之機密字串<br>• **高階語言腳本審查**：閱讀簡單 Python/Java 邏輯找出密鑰 | ❌ 使用 Ghidra / IDA Pro 反組譯組合語言<br>❌ 動態脫殼、花指令混淆、控制流平坦化 |
| **Cryptography**<br>(密碼學) | **83 題** | 🟡 **觀念驗證** | 線上工具 / Python 基礎 | **L12** | • **單向雜湊 (Hash) 不可逆性與完整性**<br>• **弱密碼雜湊反查與字典比對**（體會預運算查表／字典如何降低破解成本，及其與密碼強度的關係；字典比對與 Rainbow table 為不同技術，勿混用）<br>• **簡易對稱加密直觀體驗**：ROT13／Caesar 位移、單純 XOR，用線上工具或幾行 Python 理解「位移／替換」與對稱金鑰概念 | ❌ RSA 費馬大數因數分解、數論算法推導<br>❌ 長篇古典密碼之手動字母頻率分析（簡易 ROT13/Caesar/XOR 不在此限）<br>❌ 複雜的非對稱數學公私鑰攻擊 |
| **Artificial Intelligence**<br>(AI 基礎) | **16 題** | 🔵 **現代拓展**<br>(加分/選修) | 瀏覽器互動 | **L13 延伸** | • **AI Agent 信任邊界與提示詞驗證探討**<br>• **異常偵測與分類模型邊界概念**（現代資安視野拓展） | ❌ 與網路安全主軸無關的深層機器學習公式 |
| **Blockchain**<br>(區塊鏈) | **4 題** | 🔴 **不適合**<br>(課程外) | — | — | ❌ **不宜配題**：題數稀少，且需 Solidity／智能合約與 Web3 專業背景，與本課「電腦網路安全」主軸脫節 | ❌ 智能合約漏洞、Web3/DeFi 攻擊、鏈上交易分析 |

> **📊 題數來源**：以上庫存題數依據 `security/practice/challenges/platforms/cylab_picoctf/cylab_all_challenges_2026-08-08.csv`（2026-08-08 快照），全站共 **525 題**（83+86+75+76+102+83+16+4）。Blockchain 列出以求分類完整與誠實，不納入課程選題範圍。

---

### 🎯 總結：兩張表的戰略共識

1. **章節邊界分明**：
   - **實作核心章節**：聚焦於 **Lesson 2, 3, 4, 10, 11, 12, 13**（涵蓋攻擊、探測、認證、過濾、通道、雜湊與封包）。
   - **管理法規章節**：**Lesson 5, 6, 7, 8** 誠實不配題，回歸個案討論與制度教學。
2. **題庫分類各有精準定位**：
   - `Web` 與 `Forensics` 為**兩大主力**（涵蓋應用層與網路層封包）。
   - `Binary` 與 `Reverse` 抽取最貼近講義原理的**「危險函式原始碼審查」**與**「靜態字串特徵提取 (Strings/YARA)」**，排除 offset/ROP 等高階競賽雜技。
   - `Crypto` 聚焦於**「雜湊完整性、弱密碼與簡易對稱加密」**，排除純數論與長篇手動頻率分析。
   - `AI` 定位為**「現代資安加分拓展」**。
