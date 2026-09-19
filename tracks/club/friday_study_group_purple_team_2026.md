# NCtfU 資安社｜週五線上紅藍攻防對抗班（方案 B：Purple Team 100% 免費非 Premium 認證版）

版本：v1.1｜校驗日期：2026-09-15｜定位：兼具深度紅隊滲透與真實藍隊鑑識的 14 週交錯攻防課表（全數非 Premium 免費）

---

## 1. 核心定位與特色（為什麼做紅藍交錯？）

全新規劃的 **「方案 B：紅藍攻防對抗班 (Purple Team)」**，採取**「單數週攻擊、雙數週防守」**的鏡像設計：
* **「知己知彼」的閉環**：奇數週親手執行漏洞利用（紅隊突破、提權、橫向、植入），偶數週立刻切換視角，分析剛才那種攻擊在系統、日誌與網路封包中留下的蛛絲馬跡（藍隊捕獵）。
* **深度完全不縮水**：
  * 紅隊端：對接權威的 **PortSwigger Web Security Academy**（業界 Web 滲透天花板）、**HackTheBox Starting Point**、**Linux SUID 實戰**，親手寫 Payload 拿 Root/Admin。
  * 藍隊端：對接 **CyberDefenders 官方認證非 Premium 之真實免費題**、**MTA 真實勒索流量**、**Volatility 3 記憶體取證**，硬核還原攻擊鏈。
* **運作機制同樣維持超 Chill 模式**：
  * 線上 Discord 單一大語音房，現場即席動手，不用開螢幕、不要求會前刷題，零課外作業。

---

## 2. 採用平台與前置準備（100% 驗證免費無門檻）

| 陣營 | 主要平台與工具 | 特色與費用說明 |
| :--- | :--- | :--- |
| **⚔️ 紅隊滲透** | **PortSwigger Academy**<br>**Hack The Box (Starting Point)**<br>**Linux 提權靶機** | 免費註冊即可啟動專屬雲端實驗室（免在本地裝 Kali / 配網卡），用瀏覽器即可動手發動攻擊。 |
| **🛡️ 藍隊調查** | **CyberDefenders（非 Premium 免費題）**<br>**MTA 封包分析站**<br>**SEED Labs (Docker)** | 全數選用經實機驗證 `Locked: False` 之免費題目，下載單一 log/pcap/img 即可分析。 |

> **社員本機自備工具**：
> 1. 瀏覽器（操作 PortSwigger / HTB）
> 2. Burp Suite Community（免費版即可）
> 3. Wireshark（封包分析）
> 4. VS Code / 記事本（日誌分析與腳本）

---

## 3. 秋季 14 週「紅藍交錯 (Purple Team)」深度攻防實戰課表

時間：每週五 19:30～21:00（Discord 線上語音房）

| 週次 / 日期 | 攻防陣營 | 當晚調查主題 (攻防情境) | 實戰靶場與精確連結 (100% 實測非 Premium 免費) | 核心動手任務 (Flag / 實戰目標) |
| :---: | :---: | :--- | :--- | :--- |
| **W1 (9/18)** | ⚔️ **紅隊** | **【邊界打點】Web 命令注入與反彈 Shell**<br>利用參數拼接漏洞突破邊界，取得系統交互式 Shell | PortSwigger Academy<br>👉 [Lab: OS Command Injection Simple](https://portswigger.net/web-security/os-command-injection/lab-simple) | 1. 繞過前端過濾傳遞 `whoami` 指令<br>2. 執行指令讀取 `/etc/passwd`<br>3. 取得系統 Flag！ |
| **W2 (9/25)** | 🛡️ **藍隊** | **【邊界獵捕】Web 伺服器異常與入侵痕跡追兇**<br>分析 Wireshark 封包還原駭客上傳 Webshell 與偷取資料的過程 | CyberDefenders (FREE)<br>👉 [Lab: Web Investigation](https://cyberdefenders.org/blueteam-ctf-challenges/web-investigation/) | 1. 攻擊者最初掃描與注入的 IP 為何？<br>2. 攻擊者上傳的 Webshell 檔名為何？<br>3. 攻擊者從後台偷走的資料庫表單名稱？ |
| **W3 (10/2)** | ⚔️ **紅隊** | **【主機提權】Linux SUID 二進位與權限提升**<br>利用系統配置不當的 SUID 程式，從一般用戶提權為 root | OverTheWire / GTFOBins<br>👉 [Bandit: Level 19~20 (SUID 提權)](https://overthewire.org/wargames/bandit/bandit20.html) | 1. 使用 `find / -perm -4000` 找出特權二進位<br>2. 搭配 GTFOBins 語法獲取 root 權限<br>3. 讀取 `/etc/bandit_pass/bandit20` 旗標！ |
| **W4 (10/9)** | 🛡️ **藍隊** | **【端點獵捕】Windows 系統事件與登入行為鑑識**<br>分析特權提升與惡意修改後的系統事件日誌 | CyberDefenders (FREE)<br>👉 [Lab: Sysinternals](https://cyberdefenders.org/blueteam-ctf-challenges/sysinternals/) | 1. 惡意程式修改了哪一個登錄檔機碼？<br>2. 攻擊者留下的排程任務名稱與路徑？<br>3. 惡意行程觸發的網路外聯目的地？ |
| **W5 (10/16)** | ⚔️ **紅隊** | **【內網橫向】SMB 服務枚舉與服務橫向滲透**<br>利用無密碼共享存取與 SMB 協定滲透目標主機 | Hack The Box (Starting Point)<br>👉 [HTB: Dancing (Tier 0 實戰)](https://app.hackthebox.com/starting-point) | 1. 使用 `smbclient -L` 枚舉開放的共享資料夾<br>2. 存取非公開資料夾下載機密憑證<br>3. 取得 User.txt 與 Root.txt Flag！ |
| **W6 (10/23)** | 🛡️ **藍隊** | **【橫向獵捕】PsExec 遠端執行與 SMB 痕跡分析**<br>從流量封包還原黑客在內網穿梭跳躍的特徵 | CyberDefenders (FREE)<br>👉 [Lab: PsExec Hunt](https://cyberdefenders.org/blueteam-ctf-challenges/psexec-hunt/) | 1. 哪台主機發起了 PsExec 橫向移動？<br>2. 目標主機建立的服務名稱與執行檔？<br>3. 橫向移動時利用的 SMB 共享管道名稱？ |
| **W7 (10/30)** | 🛑 **休息** | **【期中段考週休息】** | 全體暫停休息 | 安心準備期中考 |
| **W8 (11/6)** | ⚔️ **紅隊** | **【進階 Web】SSRF 伺服器端請求偽造實施**<br>偽造伺服器向內網發起請求，突破邊界讀取中繼資料 | PortSwigger Academy<br>👉 [Lab: Basic SSRF Against Local Server](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost) | 1. 攔截 API 請求並修改目標網址至 127.0.0.1<br>2. 存取內部管理後台 `/admin`<br>3. 刪除 carlos 使用者完成攻堅任務！ |
| **W9 (11/13)** | 🛡️ **藍隊** | **【流量獵捕】真實木馬 C2 隱蔽通訊與外聯偵測**<br>分析真實 AsyncRAT / XWorm 惡意流量封包 | Malware-Traffic-Analysis (MTA)<br>👉 [2024-03-14 Traffic Analysis](https://www.malware-traffic-analysis.net/2024/03/14/index.html) | 1. 中毒受害者的內網 IP 與主機名稱？<br>2. 攻擊者連回的 C2 惡意域名與 IP？<br>3. 封包中下載的惡意 exe 之 SHA256？ |
| **W10 (11/20)** | ⚔️ **紅隊** | **【模板注入】SSTI 漏洞利用與沙盒逃逸**<br>利用 Python Jinja2 模板執行任意 Python 代碼 RCE | PortSwigger Academy<br>👉 [Lab: SSTI Exploitation (Basic)](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic) | 1. 注入 `${7*7}` 確定模板引擎類型<br>2. 尋找 Python `__mro__` 與 `subprocess.Popen`<br>3. 執行指令刪除 `morale.txt` 檔案通關！ |
| **W11 (11/27)** | 🛡️ **藍隊** | **【記憶體獵捕】Windows 記憶體取證神技！惡意進程獵捕**<br>使用 Volatility 3 抓出注入在合法進程裡的木馬 | CyberDefenders (FREE)<br>👉 [Lab: Brave](https://cyberdefenders.org/blueteam-ctf-challenges/brave/) | 1. 哪一個合法進程被注入了惡意代碼？<br>2. 被隱藏的真正惡意 PID 為何？<br>3. 從 RAM Dump 挖出的 C2 控制端網址？ |
| **W12 (12/4)** | ⚔️ **紅隊** | **【全真滲透】從無憑證踩點到奪得最高管理權限**<br>綜合實施服務枚舉、漏洞利用與權限獲取 | Hack The Box (Starting Point)<br>👉 [HTB: Responder (Tier 1 實戰)](https://app.hackthebox.com/starting-point) | 1. 識別目標 Web 服務中的 LFI 漏洞<br>2. 使用 Responder 擷取 NTLMv2 雜湊並破解<br>3. 使用 WinRM 登入伺服器取得 Root Flag！ |
| **W13 (12/11)** | 🛡️ **藍隊** | **【主動防禦】技能競賽好玩嗎？Linux iptables 阻斷黑客**<br>當防守方，配置防火牆放行合法服務、徹底阻斷攻擊 | SEED Labs 官方開源<br>👉 [Firewall Exploration Lab](https://seedsecuritylabs.org/Labs_20.04/Networking/Firewall/) | 1. 寫一條 iptables 阻斷某台主機的 Ping<br>2. 寫一條白名單只允許 80 Port 存取<br>3. 驗證服務有沒有被自己不小心配壞！ |
| **W14 (12/18)** | ☕ **結算** | **【期末茶會 / 自由閒聊】** | Discord 語音純聊天 | 聊聊本學期大家解過最爽的一題、評估寒假與下學期是否組隊參賽。 |
