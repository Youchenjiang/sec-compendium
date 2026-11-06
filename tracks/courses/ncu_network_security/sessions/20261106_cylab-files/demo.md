# 台上示範腳本：Matryoshka doll

> 教師用。講義 [handout.md](handout.md) 的走查壓成一頁：左欄照打，中欄是打完要指給學生看的那一行，右欄是要說的一句。全程在 CyLab webshell，約 15 分鐘。作業五題的同款腳本在 [demo-assignment.md](demo-assignment.md)。

## 開始前（學生進場時做完）

```bash
cd ~ && rm -rf _dolls.jpg.extracted base_images dolls.jpg
wget <題目頁 dolls.jpg 的連結>
ls -l
```

- 投影講義的題目表（「這堂用哪幾題」），題目說明和提示先唸一遍：檔案裡藏檔案，問題只剩「怎麼找」。
- 終端字體放大到後排看得到 binwalk 那四列。
- 先不要打 `binwalk`，示範的重點是前兩步怎麼把你帶到第三步。

## 照這個順序打

| 打 | 指著哪一行 | 說一句 |
|---|---|---|
| `file dolls.jpg` | 冒號後第一個詞 `PNG image data` | 副檔名是 jpg，它說是 PNG。`file` 不看檔名，看開頭的位元組。 |
| `strings dolls.jpg \| grep -i pico` | 沒有輸出 | flag 沒有用明文放在裡面。沒輸出也是資訊。 |
| `exiftool dolls.jpg` | 讓它整頁捲過去 | 一百多行，大半是色彩描述檔，不用看。 |
| `exiftool dolls.jpg \| grep -iE "warning\|comment\|type\|image (width\|height)"` | `Warning: Trailer data after PNG IEND chunk` | PNG 以 IEND 結尾，後面不該有東西。它說有。這才是去「拆」的理由。 |
| `binwalk dolls.jpg` | 第三列 `272492 ... Zip archive ... name: base_images/2_c.jpg` | 表頭：十進位、十六進位是同一個位置，DESCRIPTION 是看到什麼。第二列 TIFF 是 EXIF，不理。 |
| 同一畫面 | 第四列 `651587 End of Zip archive` | 651587 + 22 = 651609，就是檔案大小。zip 從 272492 一路接到檔尾。 |
| `binwalk -e dolls.jpg && ls _dolls.jpg.extracted/` | `4286C.zip  base_images` | `_extracted` 是 binwalk 取的，`4286C` 是那個 offset 的十六進位；`base_images` 是出題者壓進 zip 的路徑。 |
| `unzip dolls.jpg` | `272492 extra bytes at beginning` | 同一件事，不靠 binwalk 也行。binwalk 自己不解壓，`-e` 是替你叫 unzip。 |
| `cd _dolls.jpg.extracted/base_images && file 2_c.jpg` | `PNG image data, 526 x 1106` | 新檔案，回到步驟 1。 |
| `binwalk 2_c.jpg` | `187707 ... name: base_images/3_c.jpg` 和兩列 `End of Zip` | 同一個樣子，尺寸變小。結尾標記有兩個：383897 + 22 = 383919 是這一層的；另一個是更裡面那層露出來的簽名，binwalk 只認簽名不驗證。 |
| `cd ~ && rm -rf _dolls.jpg.extracted base_images && binwalk -e -M dolls.jpg` | 它自己一層層往下列 | `-M` 就是剛才的迴圈交給它跑。第一次要手動走，才知道它在做什麼。 |
| `find _dolls.jpg.extracted -name flag.txt -exec cat {} \;` | `p i c o C T F { ... }` | 去掉空白就是 flag。四層，每層都是：認 → 看 → 拆 → 回頭。 |

## 收尾

- 投影講義的階梯圖（`img/09_dolls_structure.png`）：每一層接在上一層 zip 的正下方，一層比一層小。
- 再投檢查表那張五步的表：示範只走到第三步，作業三題各往下一步。
- 問學生：為什麼不一開始就 `binwalk -e -M`？等一兩個回答，再給講義那段的答案：它看不到壞檔頭、看不到明文 flag，而且輸出要靠 `file` 的答案來讀。

## 會出狀況的地方

| 狀況 | 處理 |
|---|---|
| `wget` 抓到的是網頁 | `file dolls.jpg` 會說 `HTML document`。正好拿來示範步驟 1 的用處，然後重新複製正確的連結。 |
| `exiftool` 整頁捲太快 | 直接打 grep 那行，或 `exiftool dolls.jpg \| tail -5`，Warning 在倒數第三行。 |
| `binwalk -e` 沒拆出 `base_images` | 改用做法 B `unzip dolls.jpg`，順便講 binwalk 不自己解壓。 |
| `-M` 之後找不到 flag.txt | 手動再走一層：`find . -name "*.jpg" \| sort` 看到哪一層，從那層 `binwalk -e`。 |
| 家目錄塞滿（128 MB） | `rm -rf ~/_dolls.jpg.extracted ~/base_images`。這題連拆出來的副本在內只有幾 MB，塞滿多半是前面留的別題。 |
