# NCtfU 資安社｜週五線上藍隊探案茶館（100% 官方非 Premium 免費題庫認證版）

版本：v1.2｜校驗日期：2026-09-15｜狀態：已比對官方全量清單，100% 非 Premium、免付費、免複雜環境

---

## 1. 核心定位與設計原則（三大解綁）

1. **解綁週三社課通識**：
   * **週三社課**為全校普及與入門漏斗（Top of Funnel），講授環境安裝、基礎指令與科普。
   * **週五讀書會**正名為 **「獨立純藍隊實戰／威脅獵捕／事件調查專題班（Blue Team Studio）」**，不重複教基礎指令，直接進入真實 Log、pcap、取證調查。
2. **解綁金盾單選刷題**：
   * 金盾初賽 100 題單選死背法規與標準，僅供 3 人參賽戰隊於實驗室專班（`tracks/lab/golden_shield_sprint/`）自律衝刺。
   * 週五讀書會專注於動手調查，維持一氣呵成的攻擊調查與威脅獵捕鏈（Kill Chain），不讓非參賽社員枯燥陪跑。
3. **解綁課外作業與報告壓力**：
   * 取消會前 2～3 小時課外刷題要求。
   * 120 分鐘現場自閉環（Live Investigation），當場玩、當場解、解完即下課，零課外作業。

---

## 2. 目標受眾畫像

* **一句話定位**：「給那群**『想稍微認真動手玩資安，但不想有上課與報告壓力』**的社員，一個週五晚上能動動手、有同伴能問問題的線上黑客咖啡廳。」
* **三類核心組成**：
  1. **主力基本盤（約 60%）**：想動手但有拖延症，需要固定時段和同伴氛圍一起摸索的社員。
  2. **提問探索者（約 25%）**：看得懂社課，但面對龐大封包/日誌不知如何下手，需要隨時能在文字區丟截圖求救的環境。
  3. **潛水技術宅（約 15%）**：不想社交、不愛開麥，題目一出默默飆完，文字區丟一句 Flag 享受破關成就感（潛在比賽種子）。

---

## 3. Discord 運作機制（超 Chill 線上茶館模式）

* **頻道型態**：全體掛在**同一個大語音房**（週五藍隊自習室），開麥打屁隨意、閉麥當聽眾也完全 OK。
* **主持人角色**：**「開房管理員」**（不開螢幕畫面，零台上表演壓力）。
* **現場 120 分鐘時間流**：
  * **19:30（文字區丟包）**：主持人貼出題目下載連結、當晚要找的 3 個線索 (Flag)、對應知識庫手冊路徑。開麥交代背景 2 分鐘後閉麥自由行動。
  * **19:35 ~ 20:45（自主摸索與文字截圖交流）**：各自下載 log 或 pcap 檔案摸索。卡關或發現異常直接截圖丟文字頻道，文字區形成「偵探線索板」。
  * **20:45 ~ 21:00（隨緣收尾）**：解出者貼出答案，沒解完者參考官方題解或知識庫手冊，準時下課放假。

---

## 4. 採用平台與本機環境準備（100% 實機驗證非 Premium）

平台挑選鐵則：**「絕無付費鎖、免信用卡、下載單一檔案即開工」**。

1. **CyberDefenders（非 Premium 免費題）**：比對官方全量題庫，全部挑選 `Locked: False` 之免費題，註冊一般帳號即可免費下載封包。
2. **Malware-Traffic-Analysis - MTA**：Brad 頂尖真實流量 pcap，公開免登入，解壓密碼固定 `infected`。
3. **SEED Labs 2.0 (Docker)**：技能競賽實體加固體驗，官方開源 Docker 一鍵啟動。

> **社員本機自備工具**：
> 1. **Wireshark**（分析封包）
> 2. **VS Code 或任何文字編輯器**（分析文字日誌）
> 3. **Volatility 3**（記憶體取證週使用，免安裝解壓即可）

---

## 5. 秋季 14 週純線上實戰課表（全數經實機驗證非 Premium、無付費鎖）

時間：每週五 19:30～21:00（Discord 線上語音房）

| 週次與日期 | 當晚調查主題 (案件背景) | 使用平台與精確題目連結 (100% 實測免費非 Premium) | 難度 | 所需工具 | 當晚要找的 3 個線索 (Flag) | 對應知識庫手冊 |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **W1 (9/18)** | **【Web 邊界獵捕】**<br>伺服器異常告警！網站入侵與 Webshell 追兇 | CyberDefenders<br>👉 [Lab: Web Investigation](https://cyberdefenders.org/blueteam-ctf-challenges/web-investigation/) | Easy | Wireshark | 1. 攻擊者最初掃描與注入的 IP 為何？<br>2. 攻擊者上傳的 Webshell 檔名為何？<br>3. 攻擊者從後台偷走的資料庫表單名稱？ | `security/blue_team/playbooks/phase_2_traffic_analysis/09_web_application_firewall_traffic.md` |
| **W2 (9/25)** | **【系統日誌調查】**<br>Linux 伺服器遭受暴力攻擊與入侵跡證分析 | CyberDefenders<br>👉 [Lab: Hammered](https://cyberdefenders.org/blueteam-ctf-challenges/hammered/) | Medium | VS Code / grep | 1. 哪一個 IP 發起了密碼爆破攻擊？<br>2. 攻擊者成功登入的時間戳記？<br>3. 攻擊者登入後新增的後門帳號名稱？ | `security/blue_team/playbooks/phase_1_log_triage/01_linux_auth_logons.md` |
| **W3 (10/2)** | **【鑑識工具神技】**<br>Windows 事件與系統行為深度分析 | CyberDefenders<br>👉 [Lab: Sysinternals](https://cyberdefenders.org/blueteam-ctf-challenges/sysinternals/) | Medium | Event Viewer / VS Code | 1. 惡意程式修改了哪一個登錄檔機碼？<br>2. 攻擊者留下的排程任務名稱與路徑？<br>3. 惡意行程觸發的網路外聯目的地？ | `security/blue_team/playbooks/phase_1_log_triage/04_windows_security_logons.md` |
| **W4 (10/9)** | **【內網橫向獵捕】**<br>黑客在內網跳舞！抓出 PsExec 橫向移動與 SMB 跡證 | CyberDefenders<br>👉 [Lab: PsExec Hunt](https://cyberdefenders.org/blueteam-ctf-challenges/psexec-hunt/) | Easy | Wireshark | 1. 攻擊者使用哪台主機發起 PsExec 橫向移動？<br>2. 目標主機建立的服務名稱與執行檔檔名？<br>3. 橫向移動時利用的 SMB 共享管道名稱？ | `security/blue_team/playbooks/phase_2_traffic_analysis/10_lateral_movement_traffic.md` |
| **W5 (10/16)** | **【真實流量實戰】**<br>員工電腦中木馬！AsyncRAT / XWorm 感染流量分析 | Malware-Traffic-Analysis (MTA)<br>👉 [2024-03-14 Traffic Analysis](https://www.malware-traffic-analysis.net/2024/03/14/index.html) | — | Wireshark | 1. 中毒受害者的內網 IP 與主機名稱？<br>2. 攻擊者連回的 C2 惡意域名與 IP？<br>3. 封包中下載的惡意 exe 之 SHA256？ | `security/blue_team/playbooks/phase_2_traffic_analysis/08_c2_beacon_detection.md` |
| **W6 (10/23)** | **【封包迷宮】**<br>多元協定流量還原與異常通道偵測 | CyberDefenders<br>👉 [Lab: PacketMaze](https://cyberdefenders.org/blueteam-ctf-challenges/packetmaze/) | Medium | Wireshark | 1. 哪一個內網主機在進行 ARP 欺騙？<br>2. 異常 FTP/TFTP 傳輸中提取的機密檔案？<br>3. 攻擊者利用哪種隧道技術回連？ | `security/blue_team/playbooks/phase_2_traffic_analysis/07_dns_tunneling_hunting.md` |
| **W7 (10/30)** | 🛑 **【期中段考週】** | 全體暫停休息 | — | — | 安心準備期中考 | — |
| **W8 (11/6)** | **【HTTPS 解密與流量深潛】**<br>利用私鑰解密 TLS 流量，揪出隱蔽傳輸內容 | CyberDefenders<br>👉 [Lab: WireDive](https://cyberdefenders.org/blueteam-ctf-challenges/wiredive/) | Medium | Wireshark | 1. 匯入 SSLKEYLOG 成功解密的 HTTP 請求網址？<br>2. 隱藏在加密流量中的帳號密碼？<br>3. 攻擊者下載的第二階段惡意檔案 Hash？ | `security/blue_team/playbooks/phase_2_traffic_analysis/06_wireshark_packet_fundamentals.md` |
| **W9 (11/13)** | **【記憶體取證進階】**<br>真實 Windows 記憶體 Dump 獵捕惡意進程樹 | CyberDefenders<br>👉 [Lab: Brave](https://cyberdefenders.org/blueteam-ctf-challenges/brave/) | Medium | Volatility 3 | 1. 哪一個合法進程被注入了惡意代碼？<br>2. 被隱藏的真正惡意 PID 為何？<br>3. 從 RAM Dump 挖出的 C2 控制端網址？ | `security/blue_team/playbooks/phase_5_deep_dfir/23_volatility3_memory_triage.md` |
| **W10 (11/20)** | **【釣魚套件拆解】**<br>釣魚網站原始碼與憑證竊取後門溯源 | CyberDefenders<br>👉 [Lab: GrabThePhisher](https://cyberdefenders.org/blueteam-ctf-challenges/grabthephisher/) | Easy | VS Code / 記事本 | 1. 釣魚網站將偷得的帳密外傳至哪一個 Telegram Chat ID？<br>2. 攻擊者使用的釣魚套件版本？<br>3. 攻擊者接收憑證的 API 伺服器網址？ | `security/blue_team/playbooks/phase_4_hunting_intel/18_threat_intel_enrichment.md` |
| **W11 (11/27)** | **【雲端蜜罐與 Linux 漏洞】**<br>分析 Apache Path Traversal (CVE-2021-41773) 攻擊 | CyberDefenders<br>👉 [Lab: AzurePot](https://cyberdefenders.org/blueteam-ctf-challenges/azurepot/) | Medium | VS Code / 終端機 | 1. 攻擊者利用路徑遍歷讀取的系統檔案名稱？<br>2. 攻擊者在伺服器上執行的 RCE 挖礦指令？<br>3. 部署於蜜罐中的防禦告警特徵？ | `security/blue_team/playbooks/phase_4_hunting_intel/17_sigma_detection_rule_authoring.md` |
| **W12 (12/4)** | **【行動與端點鑑識】**<br>真實 Android 映像檔分析與通訊鑑識 | CyberDefenders<br>👉 [Lab: LGDroid](https://cyberdefenders.org/blueteam-ctf-challenges/lgdroid/) | Medium | SQLite 檢視器 / ALEAPP | 1. 嫌疑人通話紀錄中最後撥出的電話號碼？<br>2. 嫌疑人在通訊軟體中發送的敏感訊息？<br>3. 裝置最後連線的 Wi-Fi SSID？ | `security/blue_team/playbooks/phase_5_deep_dfir/21_disk_filesystem_evidence_collection.md` |
| **W13 (12/11)** | **【硬派實務】**<br>技能競賽好玩嗎？玩玩 Linux 防火牆 iptables 擋黑客 | SEED Labs 官方開源<br>👉 [Firewall Exploration Lab](https://seedsecuritylabs.org/Labs_20.04/Networking/Firewall/) | — | Docker | 1. 寫一條 iptables 阻斷某台主機的 Ping<br>2. 寫一條白名單只允許 80 Port 存取<br>3. 驗證服務有沒有被自己不小心配壞！ | `security/blue_team/playbooks/phase_3_containment_hardening/14_linux_iptables_nftables_isolation.md` |
| **W14 (12/18)** | ☕ **【期末茶會 / 自由閒聊】** | Discord 語音純聊天 | — | 麥克風與零食 | 聊聊本學期大家解過最爽的一題、評估寒假與下學期是否組隊參賽。 | — |
