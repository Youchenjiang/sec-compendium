# 作業五題的檢討腳本

> 教師用，格式同 [demo.md](demo.md)：左欄照打，中欄是要指的那一行，右欄是要說的一句。作業檢討或有人卡住時用。這五題的路徑來自多份 writeup 交叉比對，沒有在 webshell 實跑過，上台前請自己走一遍。flag 不要唸出來；St3g0 以外都是固定 flag。

每題開場一樣：先清場，`rm -rf ~/*` 清空家目錄（沒有回收桶，確認提示字元是 `@webshell`），`mkdir -p ~/work/<題名> && cd ~/work/<題名>` 再 `wget`；唸題目說明和提示，問「你猜藏在檢查表哪一步」，再開始打。

## File types（步驟 3，十一層格式不同）

檔案 `Flag.pdf`。每層解出來都叫 `flag`；`lzma`、`lzop`、`xz` 看副檔名決定做不做，所以每層先 `file`，再照回答 `mv` 成對的副檔名。

| 打 | 指著哪一行 | 說一句 |
|---|---|---|
| `file Flag.pdf` | `shell archive text` | 它根本不是 PDF。 |
| `cat Flag.pdf \| head` 再 `sh Flag.pdf && ls` | `x - extracting flag (text)` | shar 是用 shell 腳本包檔案，解開它就是執行它。唯一要執行的一層，所以先看過內容。 |
| `file flag` | `current ar archive` | 回到步驟 1。 |
| `mv flag flag.a && ar x flag.a && file flag` | `cpio archive` | |
| `7z x flag -oout && file out/*` | `bzip2 compressed data` | webshell 沒 `cpio`，用 7z。有 cpio 的機器是 `cpio -idv < flag`，`<` 不能省。 |
| `mv out/flag flag.bz2 && bzip2 -d flag.bz2 && file flag` | `gzip compressed data` | |
| `mv flag flag.gz && gzip -d flag.gz && file flag` | `lzip compressed data` | |
| `mv flag flag.lz && lzip -d flag.lz && file flag` | `LZ4 compressed data` | |
| `lz4 -d flag flag2 && file flag2` | `LZMA compressed data` | |
| `mv flag2 flag.lzma && lzma -d flag.lzma && file flag` | `lzop compressed data` | |
| `mv flag flag.lzo && lzop -d flag.lzo && file flag` | `lzip compressed data` | lzip 第二次出現，不是做錯。 |
| `mv flag flag.lz && lzip -d flag.lz && file flag` | `XZ compressed data` | |
| `mv flag flag.xz && xz -d flag.xz && file flag` | `ASCII text` | |
| `cat flag` | 兩行 `7069636f...` | 不是壓縮，是十六進位寫的文字。 |
| `xxd -r -p flag` | `picoCTF{...}` | 十一層，每層都是認 → 查表 → 拆 → 回頭。 |

| 狀況 | 處理 |
|---|---|
| `sh Flag.pdf` 說 `bad interpreter: /bin/sh^M` | 在 Windows 下載過、換行變 CRLF：`sed -i 's/\r$//' Flag.pdf`。 |
| `lzma -d` 說 unknown suffix | 沒 `mv` 成 `.lzma`；`lzop` 要 `.lzo`，`xz` 要 `.xz`。 |
| 有人問能不能 `binwalk -e` | 它從 ar 自動拆到 gzip，到 lzip 就停。正好示範「認得的比拆得動的多」。 |

## St3g0（步驟 4，像素）

檔案 `pico.flag.png`。前三步故意全部跑，讓「都沒有」成為往下走的理由。

| 打 | 指著哪一行 | 說一句 |
|---|---|---|
| `file pico.flag.png` | 正常的 `PNG image data` | |
| `strings pico.flag.png \| grep -i pico` | 沒輸出 | |
| `exiftool pico.flag.png \| grep -iE "warning\|comment"` | 沒輸出 | 結構完全正常。 |
| `binwalk pico.flag.png` | 只有 PNG 那一列 | 尾巴沒接東西。三步都沒有，才輪到像素。 |
| `zsteg pico.flag.png` | `b1,rgb,lsb,xy .. text: "picoCTF{...$t3g0}"` | `b1` 取 1 位元、`rgb` 三通道交錯、`lsb` 最低位元、`xy` 逐列。提示給的 `$t3g0` 就是拿來對這一行的。 |
| `zsteg -E b1,rgb,lsb,xy pico.flag.png` | 只剩那一段 | 確定組合之後只抽那一組。 |

## tunn3l v1s10n（步驟 5，檔頭）

檔案 `tunn3l_v1s10n`，沒有副檔名，2893454 bytes。讀檔頭在 webshell；改檔頭和看圖在自己電腦（HxD），示範前先把檔案下載到筆電。

| 打 | 指著哪一行 | 說一句 |
|---|---|---|
| `file tunn3l_v1s10n` | `data` | 不是沒格式，是開頭對不上任何格式。 |
| `xxd -g 1 tunn3l_v1s10n \| head -4` | 第一行 `42 4d`；0x0A 和 0x0E 都是 `ba d0 00 00` | `BM` 是 BMP 的開頭。0x0A 該是 54（`36 00 00 00`，像素從哪開始），0x0E 該是 40（`28 00 00 00`，第二段檔頭大小），兩個都被填成 53434。 |
| 同一畫面 | 0x12 `6e 04 00 00`、0x16 `32 01 00 00` | 寬 1134、高 306，記下來。 |
| HxD：0x0A → `36 00 00 00`、0x0E → `28 00 00 00`，存成 `.bmp` 開圖 | 只有下面一條的圖，寫著 `notaflag` | 檔頭修好了，但只畫 306 列，而且是假 flag。 |
| 算：(2893454 − 54) ÷ 每列位元組 | 1134 × 3 = 3402，補到 4 的倍數 = 3404；2893400 ÷ 3404 = 850 | 實際有 850 列，高度欄位說 306。有人把高度改小了。 |
| HxD：0x16 → `52 03 00 00`（850），開圖 | 整張 1134×850，上半是真 flag | BMP 從最下面一列往上存，高度改小只砍上面，資料還在。 |

| 狀況 | 處理 |
|---|---|
| 只改高度、沒改 0x0A/0x0E | 有些看圖軟體照樣開，但會歪或有雜訊；三個欄位都改才乾淨。 |
| 高度改成別的數 | 比 850 小會少一截，比 850 大會多出垃圾列。用算的，不用猜。 |

## like1000（加分，步驟 3 做一千次）

檔案 `1000.tar`，9.8 MB，純 tar 沒壓縮。在 webshell 示範特別合適：家目錄 128 MB，不邊拆邊刪，十幾層就滿。

| 打 | 指著哪一行 | 說一句 |
|---|---|---|
| `file 1000.tar && tar tf 1000.tar` | `POSIX tar archive`；`999.tar`、`filler.txt` | 裡面是下一個 tar 和一個填充檔。 |
| `tar xf 1000.tar && ls -l` | `999.tar` 跟 `1000.tar` 差不多大 | 一千層，每層只小 10 KB。手動做不完，提示也叫你寫腳本。 |
| `df -h ~` | Avail | 記住這個數字。 |
| `for i in $(seq 1000 -1 1); do tar xf $i.tar && rm $i.tar; done; ls` | 剩 `filler.txt` 和 `flag.png` | 作業三個問題的答案都在這一行：下一層叫 i−1（所以倒數）、停在 1（沒有 `0.tar`）、拆完就 `rm`。 |
| `df -h ~` | 沒變多少 | 不 `rm` 的話每層留 10 MB，十二層就塞爆 webshell。 |
| `flag.png` 下載到筆電開 | 圖上的文字 | flag 固定，所以作業看腳本不看 flag。 |

| 狀況 | 處理 |
|---|---|
| `tar: not in gzip format` | 有人加了 `-z`，它不是 `.tar.gz`。 |
| 迴圈對 `flag.png` 噴 `does not look like a tar archive` | 迴圈多跑了一次（`seq 1000 0`），無害。 |
| 家目錄滿了 | `rm -f *.tar` 重來，這次邊拆邊刪。 |

## Redaction gone wrong（選做，步驟 2）

檔案 `Financial_Report_for_ABC_Labs.pdf`。不打指令也能做：在 PDF 閱讀器裡把黑色方塊選起來、複製、貼到記事本，字就出來了。要用終端的話，`pdftotext` 一行（webshell 有沒有裝沒確認）。要講的只有一句：塗黑是在文字上面蓋一層圖形，文字物件還在檔案裡；真正的刪除要把文字物件拿掉再存檔。
