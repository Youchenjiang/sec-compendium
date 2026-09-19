# NCtfU 資安社｜週五線上紫隊讀書會（同週紅藍攻防閉環 ✕ 基礎/進階雙軌自適應）

版本：v2.5｜制定日期：2026-09-19｜狀態：100% 免費非 Premium 實機認證、同晚攻防閉環（Purple Teaming）

---

## 1. 核心革命：同晚「紅藍攻防即時閉環 (Purple Teaming)」

過去隔週分開（單週攻擊、雙週防守）會面臨兩大死穴：
1. **社員一週後就忘記**：7 天後看日誌，早已忘記上週發了什麼 Payload。
2. **出席流動導致脫節**：隔週沒來的同學直接看不懂防守背景。

本學期正式採用業界推崇的 **Purple Team（紫隊即時閉環）**：
> 🎯 **核心爽感：「剛才我親手放的火，現在我親手抓抓看！」**
> 在同一晚 90～120 分鐘內，**前半場親手發動攻擊拿到 Shell/Flag ➔ 後半場立刻打開 Wireshark/Log 找出自己的攻擊痕跡**。

同時結合**「自適應雙軌機制」**：
* **零基礎同學（Track 101）**：幹部手把手教學帶做，瀏覽器與 DevTools 開搞，零環境負擔。
* **有基礎同學（Track 201）**：發放實戰題目包（PortSwigger、CyberDefenders、HTB），各自挑戰自習，最後合流 Demo。

---

## 2. 當晚 120 分鐘紫隊動態時間流

```text
19:30 ~ 19:40 【點名與動態分流（10 分鐘）】
  • 幹部看現場出席名單，彈性分流至「Track 101 基礎引導房」或「Track 201 進階研習室」。

19:40 ~ 20:20 【前半場：⚔️ 紅隊突破（40 分鐘）】
  • 基礎版：幹部帶領在瀏覽器送出 Payload，看到回顯拿到 Flag！
  • 進階版：老手獨立攻堅 PortSwigger / HTB，獲取反彈 Shell 或 Root 權限。

20:20 ~ 20:50 【後半場：🛡️ 藍隊追兇（30 分鐘）】
  • 立即切換視角！打開剛剛攻擊情境對應的 Wireshark 封包或系統 Access Log。
  • 任務：找出剛才攻擊者的 IP、使用的 Payload 特徵、被偷走的資料痕跡。

20:50 ~ 21:00 【大合流：☕ 紫隊總結覆盤（10 分鐘）】
  • 全體回到大語音房。
  • 幹部或老手展示：「如果攻擊者做編碼/混淆，防守方的規則要怎麼寫才攔得住？」
  • 零課外作業，準時下課放假！
```

---

## 3. 秋季 14 週「同週紅藍攻防閉環」實戰課表

時間：每週五 19:30～21:00（Discord 線上語音房）  
*全數選用經實機驗證非 Premium、免付費、免複雜設定之標準環境。*

| 週次 / 日期 | 當晚攻防主題 | 🟢 Track 101 基礎引導班<br>(幹部手把手教學・零環境門檻) | 🔴 Track 201 進階研習室<br>(各自挑戰挑戰・硬核實戰對抗) | 當晚閉環獵捕目標 (藍隊追兇關鍵) |
| :---: | :--- | :--- | :--- | :--- |
| **W1 (9/18)** | **【Web 命令注入與流量追兇】** | **⚔️ 紅**：[picoCTF: Web Gauntlet](https://learn.cylabacademy.org/library?search=Web%20Gauntlet)（繞過驗證）<br>**🛡️ 藍**：Wireshark 觀察剛才網頁請求中的明文指令 | **⚔️ 紅**：[PortSwigger: OS Command Injection](https://portswigger.net/web-security/os-command-injection/lab-simple)（命令拼接）<br>**🛡️ 藍**：[CyberDefenders: Web Investigation](https://cyberdefenders.org/blueteam-ctf-challenges/web-investigation/)（Webshell 還原） | 1. 抓出攻擊來源 IP<br>2. 揪出在封包中明文傳遞的 `whoami` 指令<br>3. 提取被偷走的敏感表單 |
| **W2 (9/25)** | **【密碼爆破與登入日誌獵捕】** | **⚔️ 紅**：[picoCTF: Most Cookies](https://learn.cylabacademy.org/library?search=Most%20Cookies)（Cookie 偽造）<br>**🛡️ 藍**：本地瀏覽器 DevTools 檢查 Session 機制 | **⚔️ 紅**：[PortSwigger: Username Enumeration](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-subtly-different-responses)（爆破探測）<br>**🛡️ 藍**：[CyberDefenders: Hammered](https://cyberdefenders.org/blueteam-ctf-challenges/hammered/)（Linux 日誌分析） | 1. 攻擊者爆破時觸發的 HTTP/SSH 錯誤次數<br>2. 成功登入的時間戳記<br>3. 攻擊者登入後留下的後門帳號 |
| **W3 (10/2)** | **【Linux 提權與審計追蹤】** | **⚔️ 紅**：[OverTheWire: Bandit (0~5)](https://overthewire.org/wargames/bandit/)（基礎指令排查）<br>**🛡️ 藍**：觀察 Linux 檔案權限（rwx / SUID 標記） | **⚔️ 紅**：[OverTheWire: Bandit (19~20)](https://overthewire.org/wargames/bandit/bandit20.html)（SUID 提權）<br>**🛡️ 藍**：審查 `/var/log/auth.log` 中的 sudo 與特權執行紀錄 | 1. 哪一個特權二進位被濫用？<br>2. 提權過程中派生的新進程 PID<br>3. 取得系統 Root Flag |
| **W4 (10/9)** | **【Windows 事件與惡意持久化】** | **⚔️ 紅**：本地撰寫一條惡意註冊表/排程任務<br>**🛡️ 藍**：打開 Windows 事件檢視器看 Event ID 4688 / 7045 | **⚔️ 紅**：[Hack The Box: Archetype](https://app.hackthebox.com/machines/Archetype)（MSSQL 滲透提權）<br>**🛡️ 藍**：[CyberDefenders: Sysinternals](https://cyberdefenders.org/blueteam-ctf-challenges/sysinternals/)（Windows 行為鑑識） | 1. 惡意程式修改了哪一個登錄檔機碼？<br>2. 攻擊者建立的隱蔽排程任務名稱<br>3. 惡意行程觸發的外聯 IP 與連接埠 |
| **W5 (10/16)** | **【內網 SMB 橫向與流量偵測】** | **⚔️ 紅**：[picoCTF: Mod 26](https://learn.cylabacademy.org/library?search=Mod%2026)（編碼解讀）<br>**🛡️ 藍**：使用 CyberChef 分析雜湊與編碼特徵 | **⚔️ 紅**：[Hack The Box: Dancing](https://app.hackthebox.com/machines/Dancing)（SMB 匿名共享枚舉）<br>**🛡️ 藍**：[CyberDefenders: PsExec Hunt](https://cyberdefenders.org/blueteam-ctf-challenges/psexec-hunt/)（SMB 流量與 PsExec 捕獲） | 1. 識別哪台主機在內網發起 SMB 枚舉<br>2. 橫向移動時利用的命名管道（Named Pipe）<br>3. 提取被偷走的機密憑證檔 |
| **W6 (10/23)** | **【真實木馬外聯與 C2 流量獵捕】** | **⚔️ 紅**：[picoCTF: Wireshark (ID: 115)](https://learn.cylabacademy.org/library?search=Wireshark)（串流跟隨）<br>**🛡️ 藍**：跟隨 TCP Stream 提取通訊特徵 | **⚔️ 紅**：[picoCTF: Safe Opener](https://learn.cylabacademy.org/library?search=Safe%20Opener)（逆向提取 C2）<br>**🛡️ 藍**：[MTA 2024-03-14 Traffic](https://www.malware-traffic-analysis.net/2024/03/14/index.html)（AsyncRAT 流量分析） | 1. 中毒受害者的內網 IP 與主機名<br>2. 木馬連回的惡意 C2 域名與 IP<br>3. 封包中下載的第二階段惡意載荷 Hash |
| **W7 (10/30)** | 🛑 **【期中段考週】** | 全體暫停休息 | 安心準備期中考 | — |
| **W8 (11/6)** | **【SSRF 邊界突破與請求偽造鑑識】** | **⚔️ 紅**：使用 curl 發起本地回環請求（127.0.0.1）<br>**🛡️ 藍**：在 Web Log 中辨認內部偽造的存取記錄 | **⚔️ 紅**：[PortSwigger: Basic SSRF](https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost)（偽造內部存取）<br>**🛡️ 藍**：[CyberDefenders: PacketMaze](https://cyberdefenders.org/blueteam-ctf-challenges/packetmaze/)（異常通道與內網探測流量） | 1. 偽造請求突破存取到的內部後台網址<br>2. 辨認利用哪種協定/管道穿透邊界<br>3. 成功刪除目標用戶奪旗 |
| **W9 (11/13)** | **【惡意釣魚套件與憑證竊取溯源】** | **⚔️ 紅**：VirusTotal 分析釣魚網址特徵<br>**🛡️ 藍**：提取 HTML 原始碼中的表單發送對象 | **⚔️ 紅**：[PortSwigger: Authentication Bypass](https://portswigger.net/web-security/authentication)<br>**🛡️ 藍**：[CyberDefenders: GrabThePhisher](https://cyberdefenders.org/blueteam-ctf-challenges/grabthephisher/)（釣魚套件拆解） | 1. 釣魚網站將偷得的帳密外傳至哪一個 Telegram Chat ID？<br>2. 釣魚後門的接收 API 網址<br>3. 鑑識原始碼中的後門邏輯 |
| **W10 (11/20)** | **【進階 Web 注入與記憶體獵捕】** | **⚔️ 紅**：[PortSwigger: SQLi UNION Attack](https://portswigger.net/web-security/sql-injection/union-attacks)（資料提取）<br>**🛡️ 藍**：比對 Access Log 中的 SQL 關鍵字頻率 | **⚔️ 紅**：[PortSwigger: SSTI Exploitation](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic)（模板注入 RCE）<br>**🛡️ 藍**：[CyberDefenders: Brave](https://cyberdefenders.org/blueteam-ctf-challenges/brave/)（記憶體進程注入取證） | 1. 哪一個合法進程被注入惡意代碼？<br>2. 隱藏的惡意 PID 與記憶體位址<br>3. RAM Dump 中挖出的 C2 控制端 |
| **W11 (11/27)** | **【雜湊毒化與 NTLMv2 離線破解】** | **⚔️ 紅**：CyberChef 實作 MD5 / NTLM 雜湊產生<br>**🛡️ 藍**：比對線上字典彩虹表破譯原理 | **⚔️ 紅**：[Hack The Box: Responder](https://app.hackthebox.com/machines/Responder)（LLMNR/NBT-NS 毒化）<br>**🛡️ 藍**：提取 Windows 流量中的 NetNTLMv2 Challenge/Response 結構 | 1. 捕獲的 NetNTLMv2 雜湊格式分析<br>2. 離線 Hashcat / John 破譯出的明文密碼<br>3. 透過 WinRM 取得最高管理權限 |
| **W12 (12/4)** | **【雲端蜜罐與真實 Path Traversal】** | **⚔️ 紅**：本地測試 `../../../../etc/passwd` 目錄遍歷<br>**🛡️ 藍**：Web Access Log 中篩選 `%2e%2e%2f` 編碼特徵 | **⚔️ 紅**：CVE-2021-41773 Apache 路徑遍歷驗證<br>**🛡️ 藍**：[CyberDefenders: AzurePot](https://cyberdefenders.org/blueteam-ctf-challenges/azurepot/)（雲端蜜罐日誌分析） | 1. 攻擊者利用路徑遍歷讀取的系統檔案名稱<br>2. 伺服器遭執行的 RCE 挖礦指令<br>3. 撰寫一條攔截此遍歷攻擊的 Sigma 規則 |
| **W13 (12/11)** | **【主動防禦：主機硬化與防火牆實戰】** | **⚔️ 紅**：嘗試 Ping / 探測本機服務埠<br>**🛡️ 藍**：手動開啟本機防火牆規則成功阻斷探測 | **⚔️ 紅**：發動 Nmap 掃描與封包泛洪<br>**🛡️ 藍**：[SEED Labs: Firewall Exploration Lab](https://seedsecuritylabs.org/Labs_20.04/Networking/Firewall/)（iptables 白名單硬化實戰） | 1. 撰寫 iptables 規則阻斷指定來源 Ping<br>2. 建立僅放行 Web 服務的最小權限白名單<br>3. 驗證服務未受損且成功阻斷攻擊 |
| **W14 (12/18)** | ☕ **【期末紫隊成果總結與茶會】** | **全體自由交流**<br>• 盤點這學期親手發動過的攻擊與親手抓過的日誌<br>• 票選本學期最過癮的攻防回合 | **戰隊評估與未來方向**<br>• 評估寒假/下學期組隊（金盾獎 / 技能競賽 / CTF）<br>• 社團幹部交接與回饋交流 | 攻防一體，融會貫通！ |
