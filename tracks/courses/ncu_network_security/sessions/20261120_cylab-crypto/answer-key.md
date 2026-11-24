# 密碼學題組：教師答案與排錯

> **定位**：2026-11-20 場次（技能階梯 M6 雜湊與密碼學）的教師參考答案。搭配同資料夾的 `handout.md`（學員跟課教材）、`demo.md`（台上示範腳本）、`assignment.md`（作業題目）。
>
> **驗證狀態**：四題都**還沒有在 CyLab 上實跑**。題目機制來自 picoCTF 原題的公開解法（來源列在文末）；講義裡的數字範例（位移、MD5、講義的 RSA 小數字）已在本機 Python 實跑。上課前請照「上課前要確認的事」走一遍。
>
> **本場配置**：示範 `470`；實作 `64`、`475`、`162`（三題也是作業）。flag 一律不寫進本文件。

---

## 一、題目與驗證狀態

| ID | 題名 | 難度 | 角色 | 講義三條路 | 狀態 |
|---|---|---|---|---|---|
| `64` | caesar | Medium | 實作一（也是作業） | 暴力破解金鑰；演算法弱點 | 未在 CyLab 實跑 |
| `475` | hashcrack | Easy | 實作二（也是作業） | 周邊系統 | 未在 CyLab 實跑 |
| `470` | EVEN RSA CAN BE BROKEN??? | Easy | 課堂示範 | 周邊系統 | 未在 CyLab 實跑 |
| `162` | Mind your Ps and Qs | Medium | 實作三（也是作業） | 暴力破解金鑰 | 未在 CyLab 實跑；ID 依 picoGym 編號推定 |

---

## 二、上課前要確認的事

| 要確認的 | 怎麼確認 | 不符合時 |
|---|---|---|
| CyLab terminal 的 Python 至少 3.8 | `python3 --version`；或 `python3 -c "print(pow(5,-1,96))"` 印出 `77` | 示範和實作三改在筆電做，或把 `pow(e, -1, phi)` 換成文末的替代寫法 |
| `162` 這個 ID 對得上 Mind your Ps and Qs | 在 library 搜尋題名 | 改 ID，講義和作業只寫題名，不受影響 |
| `470` 連上去的 N 是偶數 | `nc` 連一次，看最後一位 | 重連；多次都是奇數的話示範改用 `162` |
| `475` 給幾個雜湊、各是哪種 | `nc` 連一次 | 作業題目寫的是「每個雜湊」，數量不同不影響 |
| caesar 檔案裡的密文是大寫還是小寫 | `cat` 檔案 | 講義已說明小寫時把 65 改成 97 |
| 教室網路連得到 factordb.com、crackstation.net | 瀏覽器開一次 | FactorDB 的替代是 Alpertron 的線上分解器；雜湊改用講義那一行 `hashlib` 逐個驗證 |

---

## 三、逐題答案

### `64` caesar（實作一）

- **題目給的**：一個檔案，內容是 flag 格式，大括號裡面的字母被位移過，位移量未知。
- **做法**：把大括號裡那一段放進講義的迴圈，25 行裡只有一行讀得懂。位移量就是那一行開頭的數字。
- **作業答案要點**：
  - 位移量：一個 1 到 25 的數字。每位學生的檔案可能不同，以他寫出的明文能否對應為準。
  - 怎麼找到的：金鑰只有 25 種，全部試過，挑讀得懂的那一行。能再提到「字母頻率不變」的算超出要求。
- **常見錯誤**：把 `picoCTF`／`academy` 前綴和大括號一起丟進迴圈，前綴也被移位而看不出哪一行對。只放大括號內的字。

### `475` hashcrack（實作二）

- **題目給的**：`nc` 連上去，依序出現三個雜湊值，每答對一個才給下一個。公開解法記載的順序是 MD5 → SHA-1 → SHA-256，三個原文都是常見弱密碼。
- **做法**：從長度（32／40／64 個十六進位字元）判斷演算法，貼到 CrackStation 反查；或自己猜常見密碼，用 `hashlib` 驗證。
- **作業答案要點**：
  - 每個雜湊的演算法與原文。原文以學生實際拿到的為準；公開解法裡第一個 MD5 值是 `482c811da5d5b4bc6d497ffa98491e38`，本機驗證它是 `password123` 的 MD5。
  - 怎麼得到的：沒有「解開」，是查表或猜中。能說出「因為密碼常見、沒有加鹽，事先算好的表才查得到」是完整答案。
- **批改注意**：寫「用工具解密」「把雜湊解回來」的，機制沒有答對，給一半。

### `470` EVEN RSA CAN BE BROKEN???（課堂示範）

- **題目給的**：`nc` 連上去印出 `N`、`e`、`cyphertext`。另附加密程式的原始碼。
- **弱點**：N 是偶數，所以 p = 2、q = N // 2。
- **完整步驟**：見 `demo.md` 第二段，六行 Python。
- **為什麼 p = 2 時算式仍然成立**：φ(N) = (2 − 1)(q − 1) = q − 1，其餘不變。
- **不列入作業**，學生的加分題也排除這一題。

### `162` Mind your Ps and Qs（實作三）

- **題目給的**：一個檔案，內容是 `c`、`n`、`e`（e 為 65537）。題目敘述暗示 N 太小。
- **做法**：把 `n` 貼到 factordb.com，得到兩個質因數；之後和示範相同：

  ```python
  p = <查到的>
  q = <查到的>
  phi = (p - 1) * (q - 1)
  d = pow(e, -1, phi)
  m = pow(c, d, n)
  print(m.to_bytes((m.bit_length() + 7) // 8, "big"))
  ```

- **作業答案要點**：
  - p、q 怎麼得到：n 太短，在公開的因數分解資料庫查得到（或用分解工具算出來）。
  - 如何算出明文：φ = (p − 1)(q − 1) → d 是 e 對 φ 的乘法反元素 → m = c^d mod n → 整數轉回文字。四步都寫到是完整答案；只貼程式碼沒有說明的給一半。
- **常見錯誤**：
  - 沿用示範的 `p = 2`：這一題 n 是奇數，會算出亂碼。
  - 嘗試「e 很小就開 e 次方根」：這題 e 是 65537，不適用。
  - 用 `/` 而不是 `//`：只在自己手動除的時候發生，結果是浮點數，後面全錯。

---

## 四、加分題批改

作業的加分是「自己在 CyLab 另找一題 Cryptography 題目」，排除三題實作與示範題。這一項沿用 A5 的做法（A5 是教授指定「自己找一題 SQL 注入」）；**本次是否照辦還沒有和教授確認**，不要的話從 `assignment.md` 刪掉整段。

批改看三件事：題目確實屬於 Cryptography、寫得出自己用的方法、說得出弱點屬於三條路的哪一條。只貼 flag 不給分。學生最可能找到的題：

| 題 | 重點 | 屬於哪一條路 |
|---|---|---|
| `62` 13、`144` Mod 26 | ROT13，位移量固定 13 | 暴力破解金鑰（甚至不用試） |
| `316` Vigenere | 題目直接給金鑰，照表解回去 | 嚴格說沒有攻擊；學生若這樣回答要接受 |
| `307` substitution0 | 檔案開頭就是代換表 | 周邊系統（金鑰和密文放在一起） |
| `308`／`309` substitution1／2 | 單表代換，要做頻率分析 | 演算法弱點 |
| `418` interencdec | 兩層 Base64 再加位移 | 暴力破解金鑰；前兩層是編碼不是加密 |
| miniRSA 這類 e 很小的 RSA | 明文的 e 次方沒有超過 n，直接開根號 | 周邊系統（參數選擇與沒有填充） |

> 批改原則同前幾次：flag 只證明「做到」，分數看能不能講清機制。

---

## 五、常見排錯

| 狀況 | 原因與處理 |
|---|---|
| `pow(e, -1, phi)` 報 `ValueError: pow() 2nd argument cannot be negative…` | Python 低於 3.8。替代寫法見下。 |
| 最後印出的不是文字 | 數字貼錯、漏位，或 p、q 用錯。重新複製；`470` 重連後三個數字要一起換。 |
| `ValueError: base is not invertible for the given modulus` | e 和 φ 不互質，幾乎都是 p、q 貼錯。 |
| CrackStation 查不到 | 多半是複製時多了空白或少了字元；先數長度是不是 32／40／64。 |
| `nc` 連不上或立刻斷 | 題目的實例要先在題目頁啟動，且有時限。 |

**Python 低於 3.8 時求 d 的替代寫法**（擴展歐幾里得演算法）：

```python
def inv(a, m):
    g, x, y = m, 0, 1
    r = a % m
    while r:
        k = g // r
        g, r = r, g - k * r
        x, y = y, x - k * y
    return x % m

d = inv(e, phi)
```

已在本機用講義的數字驗證：`inv(5, 96)` 得 `77`。

---

## 六、來源

題目機制依據以下公開解法，官方題目頁未能直接取得：

- EVEN RSA CAN BE BROKEN???：<https://mh4ck3r0n3.github.io/posts/2025/03/19/even-rsa-can-be-broken>、<https://p4wnda.github.io/picoCTF-even-rsa-can-be-broken>
- hashcrack：<https://sktr13055.github.io/posts/Hash-Crack/>、<https://nullvm.github.io/posts/picoctf-hashcrack>
- Mind your Ps and Qs：<https://ir0nstone.gitbook.io/notes/writeups/picogym/cryptography/mind-your-ps-and-qs>、<https://7rocky.github.io/en/ctf/picoctf/cryptography/mind-your-ps-and-qs>
- caesar：<https://tan-junwei.github.io/CTF-Writeups/PicoCTF/Cryptography/caesar>
