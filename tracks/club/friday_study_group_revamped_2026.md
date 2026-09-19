# NCtfU 資安社｜週五線上雙軌自適應讀書會（基礎引導 101 ✕ 進階自習 201）

版本：v2.0｜制定日期：2026-09-19｜狀態：100% 免費非 Premium 實機認證、動態分流自適應機制

---

## 1. 核心理念：自適應雙軌並行機制

社團讀書會過去最大的困境在於**「難度單一化」**：排太深嚇跑新生，排太淺勸退老手；每次來的人程度不一，導致課表無法推行。

本學期週五讀書會全面採用**「同主題、雙難度、動態分流」**的自適應機制：
* **看今天來的是誰，動態決定今晚怎麼跑**。
* **零基礎同學**：不強迫讀生硬手冊，由幹部手把手以「教學引導（Track 101）」帶做，保證拿 Flag 獲取成就感。
* **有基礎同學**：發放「進階實戰包（Track 201）」，各憑本事自習挑戰，卡關在文字區互丟線索，最後 15 分鐘合流分享。

---

## 2. 雙軌道定位與模式

| 軌道 | 目標受眾 | 運作型態 | 題目特徵 | 幹部/主持人心態 |
| :--- | :--- | :--- | :--- | :--- |
| **🟢 Track 101<br>基礎引導班** | 零基礎、大一新生、社課跟不上想動手摸索者 | **開螢幕 Demo、手把手教學**<br>(現場一起踩坑、講解核心觀念) | • 瀏覽器 / DevTools 即可操作<br>• picoCTF / 基礎 PortSwigger<br>• 乾淨的 Wireshark 封包抓明文 | **帶路教練**：確保零基礎同學當晚一定能親手拿到 Flag，建立信心。 |
| **🔴 Track 201<br>進階研習室** | 有基礎、想備戰金盾/技能競賽/CTF 的老手 | **各自自習、文字區交流**<br>(最後 15 分鐘全體合流成果 Demo) | • CyberDefenders 真實日誌與取證<br>• HackTheBox 靶機滲透 (Starting Point)<br>• MTA 惡意流量分析 | **同儕交流**：不講課，各顯神通破關，互相切磋 Payload 與調查思維。 |

---

## 3. 當晚 120 分鐘 Discord 動態時間流

```text
19:30 ~ 19:40 【點名與動態分流（10 分鐘）】
  主持人看今晚出席名單：
  • 若全都是零基礎：全體跑 Track 101，幹部開螢幕帶做，邊做邊講觀念。
  • 若全都是老手：直接發布 Track 201 題目包，全體進入自主挑戰與文字區交流。
  • 若新舊混雜（常態分流）：
      - 語音房 A【新手引導房】：幹部開螢幕帶零基礎同學做 Track 101。
      - 語音房 B【進階研究室】：老手各自開工打 Track 201，卡關在文字區丟截圖。

19:40 ~ 20:45 【分軌實作與現場自閉環（65 分鐘）】
  • 零基礎房：步步拆解題目背景、觀察點與驗證方法，當場解完當場懂。
  • 進階房：獨立下載 log/pcap 或開啟雲端實驗室，文字區形成「偵探線索板」。

20:45 ~ 21:00 【大合流與成果展示（15 分鐘）】
  • 全體回到大語音房。
  • 進階同學或幹部花 5~10 分鐘展示今晚 Track 201 最有趣的發現（如記憶體注入點、漏洞觸發點）。
  • 新手開眼界看進階實戰視野，老手獲得分享成就感，零課外作業準時下課放假！
```

---

## 4. 秋季 14 週「雙軌自適應」完整實戰課表

時間：每週五 19:30～21:00（Discord 線上語音房）  
*全數選用經實機驗證非 Premium、免付費、免複雜設定之標準環境。*

| 週次 / 日期 | 當晚核心主題 | 🟢 Track 101 基礎引導班<br>(幹部教學帶做・零環境門檻) | 🔴 Track 201 進階研習室<br>(各自自習挑戰・硬核實戰分享) |
| :---: | :--- | :--- | :--- |
| **W1 (9/18)** | **【Web 邊界攻擊與輸入驗證】** | **picoCTF: Web Gauntlet (ID: 88)**<br>👉 [題目連結](https://learn.cylabacademy.org/library?search=Web%20Gauntlet)<br>• 工具：瀏覽器 DevTools<br>• 任務：理解 SQL 註解語法與前端過濾繞過 | **PortSwigger: OS Command Injection Simple**<br>👉 [題目連結](https://portswigger.net/web-security/os-command-injection/lab-simple)<br>• 工具：Burp Suite / 瀏覽器<br>• 任務：利用命令注入拼接 `whoami` 讀取系統檔案 |
| **W2 (9/25)** | **【Web 伺服器異常與入侵痕跡】** | **Wireshark 基礎流量入門**<br>👉 [picoCTF: GET aHEAD (ID: 132)](https://learn.cylabacademy.org/library?search=GET%20aHEAD)<br>• 工具：瀏覽器 / curl<br>• 任務：認識 HTTP 請求方法（GET/POST/HEAD）與封包結構 | **CyberDefenders: Web Investigation**<br>👉 [Lab: Web Investigation](https://cyberdefenders.org/blueteam-ctf-challenges/web-investigation/)<br>• 工具：Wireshark<br>• 任務：還原 Webshell 上傳歷程、揪出注入攻擊 IP 與脫庫痕跡 |
| **W3 (10/2)** | **【主機系統指令與權限基礎】** | **OverTheWire: Bandit (Level 0~5)**<br>👉 [Bandit 入門關卡](https://overthewire.org/wargames/bandit/)<br>• 工具：SSH 終端機<br>• 任務：學習基礎 Linux 檔案操作、隱藏檔排查與 grep 搜尋 | **OverTheWire: Bandit (Level 19~20 SUID 提權)**<br>👉 [Bandit: SUID 關卡](https://overthewire.org/wargames/bandit/bandit20.html)<br>• 工具：SSH 終端機 / GTFOBins<br>• 任務：找出配置不當的特權二進位，實施 SUID 提權突破 |
| **W4 (10/9)** | **【端點行為與系統事件分析】** | **Windows 基礎日誌觀察**<br>👉 本地 Event Viewer 實作<br>• 工具：Event Viewer / 記事本<br>• 任務：學會查看 Event ID 4624（成功登入）與 4625（登入失敗） | **CyberDefenders: Sysinternals**<br>👉 [Lab: Sysinternals](https://cyberdefenders.org/blueteam-ctf-challenges/sysinternals/)<br>• 工具：Event Viewer / VS Code<br>• 任務：分析登錄檔機碼惡意修改、惡意排程任務與外聯網路連線 |
| **W5 (10/16)** | **【內網服務枚舉與共享存取】** | **密碼學與雜湊基礎概念**<br>👉 [picoCTF: Mod 26 (ID: 144)](https://learn.cylabacademy.org/library?search=Mod%2026)<br>• 工具：CyberChef<br>• 任務：理解編碼 (Base64/ROT13) 與加密的差異，學會常用解碼鏈 | **Hack The Box: Dancing (Tier 0 實戰)**<br>👉 [HTB: Dancing](https://app.hackthebox.com/machines/Dancing)<br>• 工具：smbclient<br>• 任務：枚舉無密碼 SMB 共享資料夾，定位機密憑證獲取雙 Flag |
| **W6 (10/23)** | **【內網橫向移動與封包鑑識】** | **基礎封包擷取與明文帳密追查**<br>👉 [picoCTF: Wireshark doo dooo do doo (ID: 115)](https://learn.cylabacademy.org/library?search=Wireshark)<br>• 工具：Wireshark<br>• 任務：跟隨 TCP 串流 (Follow Stream)，從明文通訊中提取帳密 | **CyberDefenders: PsExec Hunt**<br>👉 [Lab: PsExec Hunt](https://cyberdefenders.org/blueteam-ctf-challenges/psexec-hunt/)<br>• 工具：Wireshark<br>• 任務：捕捉 PsExec 遠端呼叫、分析具體服務名稱與橫向移動管道 |
| **W7 (10/30)** | 🛑 **【期中段考週】** | 全體暫停休息 | 安心準備期中考 |
| **W8 (11/6)** | **【真實惡意程式與流量獵捕】** | **VirusTotal 惡意樣本初探**<br>👉 VirusTotal 線上平台<br>• 工具：瀏覽器<br>• 任務：學會看檔案 Hash、防毒引擎檢測率與靜態特徵提取 | **Malware-Traffic-Analysis (MTA) 流量實戰**<br>👉 [MTA 2024-03-14 Traffic Analysis](https://www.malware-traffic-analysis.net/2024/03/14/index.html)<br>• 工具：Wireshark<br>• 任務：分析 AsyncRAT 感染封包，還原受害者 IP、C2 域名與惡意載荷 |
| **W9 (11/13)** | **【身份憑證安全與服務爆破】** | **認證機制弱點實測**<br>👉 [PortSwigger: Username Enumeration](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-subtly-different-responses)<br>• 工具：Burp Suite<br>• 任務：觀察回傳訊息差異（細微文字/反應時間）判斷帳號是否存在 | **CyberDefenders: Hammered**<br>👉 [Lab: Hammered](https://cyberdefenders.org/blueteam-ctf-challenges/hammered/)<br>• 工具：VS Code / grep<br>• 任務：深入 Linux auth.log，分析暴力破譯時間軸與攻擊者新建的後門 |
| **W10 (11/20)** | **【釣魚套件拆解與進階 Web】** | **基礎 Cookie 偽造與 Session**<br>👉 [picoCTF: Most Cookies (ID: 209)](https://learn.cylabacademy.org/library?search=Most%20Cookies)<br>• 工具：瀏覽器 DevTools / Python<br>• 任務：解讀 Flask Session Cookie 結構，理解客戶端 Cookie 安全性 | **CyberDefenders: GrabThePhisher**<br>👉 [Lab: GrabThePhisher](https://cyberdefenders.org/blueteam-ctf-challenges/grabthephisher/)<br>• 工具：VS Code / 記事本<br>• 任務：拆解釣魚網站原始碼，逆向追查惡意回傳的 Telegram Chat ID |
| **W11 (11/27)** | **【主機記憶體分析與取證】** | **基礎進程排查與工作管理員**<br>👉 本地 Windows / Linux 實習<br>• 工具：工作管理員 / Process Explorer<br>• 任務：學會觀察合法系統進程路徑（如 svchost, explorer）與異常特徵 | **CyberDefenders: Brave**<br>👉 [Lab: Brave](https://cyberdefenders.org/blueteam-ctf-challenges/brave/)<br>• 工具：Volatility 3<br>• 任務：使用 Volatility 3 獵捕遭注入的合法進程、揪出隱藏 PID 與 C2 網址 |
| **W12 (12/4)** | **【綜合滲透與漏洞利用】** | **SQL 注入基礎原理**<br>👉 [PortSwigger: SQLi UNION Attack](https://portswigger.net/web-security/sql-injection/union-attacks)<br>• 工具：瀏覽器 / Burp Suite<br>• 任務：理解 UNION 注入欄位對齊原理，提取資料庫文字資訊 | **Hack The Box: Responder (Tier 1 實戰)**<br>👉 [HTB: Responder](https://app.hackthebox.com/machines/Responder)<br>• 工具：Responder / Hashcat<br>• 任務：識別 Web LFI 漏洞，攔截 NTLMv2 雜湊並破解，透過 WinRM 奪得管理權限 |
| **W13 (12/11)** | **【系統硬化與防火牆防禦】** | **基礎防火牆規則體驗**<br>👉 本地 Windows Defender 防火牆 / UFW<br>• 工具：Windows Defender 防火牆介面<br>• 任務：手動配置一條入站封鎖規則，親自驗證連接埠阻斷效果 | **SEED Labs: Firewall Exploration Lab**<br>👉 [SEED Labs 官方開源](https://seedsecuritylabs.org/Labs_20.04/Networking/Firewall/)<br>• 工具：Docker / iptables<br>• 任務：在 Linux 環境撰寫 iptables 防火牆白名單規則，實施主機隔離加固 |
| **W14 (12/18)** | ☕ **【期末茶會 / 成果總結】** | **期末自由交流**<br>• 盤點學期所學工具鏈與技能點<br>• 自由提問社課與讀書會疑惑 | **競賽轉向與成果分享**<br>• 評估寒假/下學期組隊（金盾獎 / 技能競賽 / CTF）<br>• 各自分享本學期解過最過癮的一道題 |
