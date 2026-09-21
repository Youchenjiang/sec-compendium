# 🏆 CTF 戰隊 6 個月培訓與國際賽戰略指南 (CTF Team Training & International Roadmap)

> 本指南為社團針對外部 CTF 賽事（從線上 Jeopardy 賽到國際資格賽如 HITCON CTF、DEFCON CTF）規劃之系統化 6 個月讀書會培訓路徑與出國參賽戰略。

---

## 定位與目標設定

小團體已具備網路安全課程基礎、資安新聞關注習慣，並接觸過 Kali Linux 與密碼學，代表已跨過「完全新手」階段，可以直接進入 CTF（Capture The Flag）導向的系統化訓練。CTF 是目前國際上最主流、也最容易被團體用來檢驗實力並取得出國資格的競賽形式，分為 Jeopardy（解題式）與 Attack-Defense（攻防式）兩種賽制，前者適合初期培養個人技能，後者更貼近實戰但需要更強的團隊協作與基礎設施能力。台灣最重要的出國參賽路徑是 HITCON CTF：其冠軍隊伍可直接取得 DEFCON CTF 決賽資格，是台灣選手前進拉斯維加斯世界頂級駭客大賽的主要管道。過去台灣隊伍如 HITCON、Balsn 都是透過這條路徑出國比賽，證明只要方法正確，學生團隊完全有機會晉級國際決賽。[^1][^2][^3][^4][^5]

## 技能領域總覽

CTF 比賽通常涵蓋六到八大類別，每類所需先備知識與學習曲線不同。建議團隊先做「廣度優先」，再依興趣分工深耕，而不是一開始就all-in單一領域。[^6]

| 類別 | 核心技能 | 難度定位 | 常用工具 |
|---|---|---|---|
| Web Exploitation | SQLi、XSS、SSRF、IDOR、檔案上傳漏洞 | 入門到中階 | Burp Suite、SQLmap、Gobuster[^6][^7] |
| Cryptography | 古典密碼、雜湊、RSA/AES 弱點、數論 | 入門(簡單題)到高階 | CyberChef、Hashcat、Python[^6][^8] |
| Reverse Engineering | 組合語言閱讀、二進位分析 | 中階 | Ghidra、IDA Free、Radare2[^6] |
| Binary Exploitation (Pwn) | Buffer Overflow、ROP chain、GDB 除錯 | 高階 | pwntools、GDB+pwndbg、ROPgadget[^6][^7] |
| Forensics | 封包分析、磁碟/記憶體鑑識 | 入門到中階 | Wireshark、Volatility、Autopsy、binwalk[^6][^7] |
| OSINT | 公開資訊蒐集、地理定位 | 入門 | Google Dork、Shodan、Maltego[^6][^7] |
| Steganography / Misc | 隱寫、邏輯謎題、雜項腳本 | 入門到中階 | steghide、stegsolve、binwalk[^7] |

由於團隊已上過密碼學課且用過 Kali，可以跳過純基礎課程，直接以「解題練習＋寫 writeup」的方式加深 Web、Crypto、Forensics 三類的實戰能力，再視隊員興趣分流至 Reverse/Pwn 這類需要較長學習曲線的高階領域。中國技術社群的分工建議也指出，A方向（Pwn＋Reverse＋Crypto）偏重底層與數學，B方向（Web＋Misc）偏重技巧與速度，多數強隊仍要求成員兩者都懂基礎，再各自精修一項。[^9][^1]

## 六個月讀書會 Roadmap

由於出國資格賽（如 HITCON CTF Quals）通常在每年 8月底登場，決賽落在 11月，建議以半年為一個訓練週期，搭配 CTFtime 上的賽事行事曆滾動式調整。[^10]

### 第 1 個月：基礎補強與分工定調
- 用 1-2 週重新校準 Linux/網路基礎與 Python 腳本能力，確保所有成員程度一致，即使已上過課也建議做一次「速通」複習。[^11][^1]
- 在 PicoCTF、TryHackMe、OverTheWire（Bandit/Natas）上做入門到中階題目，同步累積 Web、Crypto、Forensics、OSINT 四大類至少各20題的解題量。[^12][^6]
- 依團隊興趣與長處初步分組：A方向（Reverse/Pwn/Crypto）、B方向（Web/Forensics/Misc），但要求所有成員都碰過各領域基礎題。[^9]

### 第 2-3 個月：核心技能深化
- Web：完成 PortSwigger Web Security Academy 的 apprentice/practitioner 等級實驗室，並精練 Burp Suite 使用。[^13]
- Crypto：從 CryptoHack 系列題目開始，補強數論、RSA/AES弱點與頻率分析，逐步進到中高階題目。[^8][^13]
- Reverse/Pwn（進階分組）：透過 LiveOverflow 教學與 pwnable.kr 練習 GDB、pwntools、緩衝區溢位與 ROP chain 基礎。[^13][^9]
- Forensics：熟練 Wireshark 封包分析、Volatility 記憶體鑑識、binwalk/exiftool 隱寫檔案分析。[^7]
- 每週固定一次讀書會，採「單一類別深耕」模式，避免同一場混雜多類別分散注意力，並要求每題寫「漏洞、影響、修補」三段式小結累積成寫作能力。[^14]

### 第 4 個月：實戰演練與寫 Writeup
- 開始參加真實 CTF 賽事（非練習模式），優先選擇 Jeopardy 賽制、有現成 writeup 的中小型比賽練手感，賽後對照官方或社群 writeup 檢討。[^1][^9]
- 建立團隊分工協作流程（如 Discord + 共享文件即時同步解題進度），這是攻防賽與長時賽的關鍵能力，也是與純自學最大差異之處。[^1]
- 開始追蹤 CTFtime 賽事日曆，篩選出接下來 2-3 個月內適合報名的比賽，並登記組隊。[^15][^16]

### 第 5-6 個月：資格賽準備與衝刺
- 鎖定目標資格賽，例如 HITCON CTF Quals（每年約8月底登場，Jeopardy形式，冠軍可直取 DEFCON CTF 決賽資格），或其他具高 Weight 分數（代表賽事難度與含金量較高）的國際賽事如 DEF CON CTF Qualifier、SECCON、SAS CTF 等。[^4][^17][^15][^10]
- 進行模擬賽（Mock CTF），依照正式比賽時長排練分工、時間分配與心理素質，24小時賽建議切成2-4個時段、每時段8-12小時專注作戰。[^11]
- 賽前一個月聚焦補強團隊弱項類別，並整理過去半年累積的 writeup 與工具腳本，形成團隊知識庫供賽中快速調用。[^14][^1]

## 出國參賽的具體路徑

台灣團隊過去多次證明「HITCON CTF → DEFCON CTF」是最直接的出國參賽路徑：2014年HITCON戰隊首次以第12名資格晉級DEFCON 22決賽，2015年以趨勢科技贊助之姿拿下第4名，2024年HITCON CTF 冠軍隊伍再度取得隔年DEFCON CTF決賽資格，賽事已發展為DEFCON CTF指定種子賽事之一。取得決賽資格的方式主要有兩種：一是在5月的DEFCON CTF線上資格賽（通常超過千隊參賽）擠進前10-15名，二是拿下少數幾場全球公認的DEFCON種子賽（如HITCON CTF）冠軍。除了DEFCON路線，讀書會也可同時關注SECCON（日本）、SAS CTF（印尼峇里島決賽）等亞洲區域強賽，這類賽事地緣位置較近、對台灣團隊參賽門檻相對友善。[^2][^18][^19][^3][^17][^20][^5][^15][^4]

## 分工與長期精進建議

團隊應在半年週期結束後，依據賽事表現決定是否要「集中火力衝一項專精」或「維持廣度多面手」定位；學術界與業界普遍認為，二元漏洞（Pwn）與逆向工程要達到真正競爭力，通常需要1-2年的持續練習，因此若目標是長期穩定出國參賽，建議將 Pwn/Reverse 列為次年重點培養對象，而非急於短期內求成。同時可考慮搭配 eJPT、PNPT 等對CTF能力有直接遷移價值且成本相對親民的實務型證照，作為個人技能檢核的輔助指標，而非唯一目標。[^7][^1]

---

## References

1. [Top Web Application CTF Challenges You Must Try in 2026](https://www.appsecmaster.net/blog/complete-ctf-roadmap-for-beginners-entering-cybersecurity/) - CTF (Capture The Flag) competitions offer hands-on cybersecurity challenges, helping learners practi...

2. [駭客界巔峰對決！HITCON CTF 2024 駭客競賽收官](https://today.line.me/tw/v3/article/0MgyyE3) - 由台灣駭客協會主辦，HITCON CTF 2024（台灣駭客年會 – Capture the Flag 駭客競賽）周末圓滿落幕。今年的 HI...

3. [【出國比賽側錄】HITCON 征戰世界最大駭客競賽 DEF CON CTF 實錄（上） | TechOrange 科技報橘](https://buzzorange.com/techorange/2015/08/31/hitcon-in-2015-defcon/) - 【快訊】趨勢科技所贊助的 HITCON 戰隊擊敗中國等其餘 11 支隊伍，勇奪第四名!!!!

4. [HITCON CTF - Association of Hackers in Taiwan](https://hacker.org.tw/en/projects/hitcon-ctf-/) - 社團法人台灣駭客協會（HIT）旨於推廣資訊安全，協助政府、企業、民間，搭起合作的橋樑，讓台灣能與全世界一同成長，並讓台灣的資安能量發光發熱。

5. [DEF CON CTF資格賽，臺灣聯隊攜手獲得第二名，八月進軍賭城實體較勁](https://www.ithome.com.tw/news/151209) - 臺灣參賽隊伍Balsn.217@TSJ.TW戰隊，囊括臺灣四個世代的CTF比賽選手，總計有53名選手參加，參賽成員以在學學生為主力，政府也有資源挹注參賽選手。總計16個隊伍參加DEF CON CTF決...

6. [CTF Deep Dive: Choosing the Right Category for Your Level](https://tryhackme.com/resources/blog/ctf-deep-dive-how-to-choose-the-right-category-for-your-skill-level) - CTF categories are not equally accessible at every skill level. They have different prior knowledge ...

7. [Module10 Ctf and Career | PDF | Security Hacker | Computing - Scribd](https://www.scribd.com/document/1008421348/Module10-Ctf-and-Career) - This document provides an overview of Capture The Flag (CTF) competitions, detailing various categor...

8. [Guide To CTF | PDF | Cryptography | Cryptanalysis](https://www.scribd.com/document/837662928/Guide-To-CTF) - The document is a comprehensive guide to Capture The Flag (CTF) competitions, outlining various cate...

9. [CTF学习路线指南(附刷题练习网址)](https://www.cnblogs.com/Bubgit/p/9721272.html) - PWN,Reverse：偏重对汇编，逆向的理解； Gypto：偏重对数学，算法的深入学习； Web：偏重对技巧沉淀，快速搜索能力的挑战； Mic：则更为复杂，所有与计算机安全挑战有关的都算在其中 常规...

10. [CTFtime events](https://t.me/s/ctftimeorg_events?before) - Бот является неофициальным. Логотип и название принадлежат ctftime.org. Разработан командой LIFE.

11. [Ethical Hacking Roadmap 2026: From Fundamentals to Your ...](https://www.nucamp.co/blog/ethical-hacking-roadmap-2026-from-fundamentals-to-your-first-ctf) - Ethical Hacking Roadmap 2026: 6-month, 10-15 hrs/wk plan to master networking, Linux, Bash/Python, f...

12. [Hamed233/Cybersecurity-Mastery-Roadmap](https://github.com/Hamed233/Cybersecurity-Mastery-Roadmap) - A comprehensive, step-by-step guide to mastering cybersecurity from beginner to expert level with cu...

13. [CTF Learning Path Table: Step 1 | PDF - Scribd](https://www.scribd.com/document/998513032/CyS) - The document outlines a structured learning path for Capture The Flag (CTF) challenges, detailing se...

14. [Web Security CTF: A Practice Roadmap by Skill Level](https://appsecmaster.blogspot.com/2026/06/web%20security%20CTF.html) - A web security CTF capture the flag is a hands on exercise where players find a hidden flag by explo...

15. [CTF Events - CTFtime.org / All about CTF (Capture The Flag)](https://ctftime.org/event/list/?year=2026&online=-1&format=0&restrictions=-1) - Capture The Flag, CTF teams, CTF ratings, CTF archive, CTF writeups

16. [upcoming CTF events - CTFtime](https://ctftime.org/event/list/upcoming) - Capture The Flag, CTF teams, CTF ratings, CTF archive, CTF writeups

17. [SAS CTF 2026 Quals](https://ctftime.org/event/3109/) - Top 8 teams from the qualification stage will compete for a share of the $18.000 prize pot at SAS 20...

18. [臺灣HITCON團隊進軍全球駭客競賽，挑戰全球20強](https://www.ithome.com.tw/news/88072) - 繼先前在中國百度杯駭客戰奪冠後，HITCON接著挑戰全球駭客競賽，將於今年8月8～10日和全球20隊最強團隊，爭取前八強桂冠

19. [逆轉勝！台灣隊伍取得網路攻防競賽世界盃DEF CON 22 CTF決賽資格](https://www.bnext.com.tw/article/32263/BN-ARTICLE-32263) - 長期聚焦於全球、台灣與中國等地最新的科技、網路、創業、數位行銷等議題的動態及趨勢。受到企業領袖與新世代菁英的喜愛，更引領台灣社會對「新商業」的關注與討論。

20. [台灣駭客賽獲國際肯定取得DEFCON種子賽資格- 生活 - 自由時報](https://news.ltn.com.tw/news/life/breakingnews/1467320) - 根據世界駭客大賽DEFCON CTF主辦單位剛剛公布的消息，將於12月舉辦的台灣駭客攻防大賽HITCON CTF冠軍隊伍，將可以取得DEF CON CTF的決賽資格，這是台灣HITCON首次成為國際認...

