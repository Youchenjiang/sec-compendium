import subprocess
import base64
import os

key = os.environ.get("CTFD_SSH_KEY", os.path.expanduser("~/.ssh/id_rsa"))
host = os.environ.get("CTFD_SSH_HOST", "ubuntu@129.225.174.13")

challenges_data = [
    {
        "id": 37,
        "name": "中央資管歡迎你！",
        "description": """歡迎來到中央資管碩一新生茶會！🌟
恭喜大家成為資管所的一份子，這是系上為大家準備的開場祝福：

`NCUMIS{welcome_to_central_mis}`""",
        "hints": [
            {
                "title": "新手操作指引",
                "content": "將題目中的 `NCUMIS{welcome_to_central_mis}` 完整複製（包含大括號），貼到下方的輸入框並點擊「提交」即可獲得分數！",
                "cost": 0,
            }
        ],
    },
    {
        "id": 38,
        "name": "學長的最後目擊照片",
        "description": """據說上週有一位研二學長宣稱「我論文寫完了」之後，就再也沒有出現在管二館了。

系辦只在百花川附近找到他遺留的手機與這張打卡照片。身為系上的資安偵探，你能從這張數位照片留下的蛛絲馬跡中，調查出學長到底逃去了哪裡嗎？

📥 **[點擊下載學長失蹤前的照片 (campus.jpg)](https://im2026ctf.duckdns.org/download/campus)**""",
        "hints": [
            {
                "title": "💡 提示 1：線索方向",
                "content": "【線索方向】數位相機或手機在拍攝照片時，除了記錄可見像素外，通常還會將拍攝時間、相機型號、甚至主旨備註等「中繼資料 (Metadata / EXIF)」一併寫入圖檔內。",
                "cost": 20,
            },
            {
                "title": "🛠️ 提示 2：破關手法",
                "content": "【解題手法】在 Windows 下對下載的照片檔案點「右鍵 -> 內容 -> 詳細資料 (Details)」，在「主旨」或「備註」欄位即可直接看見 Flag！亦可使用線上 EXIF 工具（如 exiftool、jimpl.com）解析中繼資料。",
                "cost": 50,
            },
        ],
    },
    {
        "id": 39,
        "name": "學長留下的屎山代碼",
        "description": """這是十年前某位畢業學長留下來的內部測試系統，畫面上空無一物，據說是因為前端工程師早就跑路了。

身為 Web 考古學家，你知道瀏覽器呈現出來的畫面往往只是冰山一角。你能深入這個頁面的背後，找出學長當年偷偷留下的兩段自白碎片並拼出完整的 Flag 嗎？

🌐 **[點擊進入屎山代碼考古實驗室](https://im2026ctf.duckdns.org/labs/f12)**""",
        "hints": [
            {
                "title": "💡 提示 1：第一段碎片",
                "content": "【第一段碎片】現代瀏覽器都內建開發者工具。按下鍵盤 F12（或右鍵點擊檢查），在 Elements（元素）分頁仔細翻找 HTML 原始碼與綠色的註解文字！",
                "cost": 20,
            },
            {
                "title": "🛠️ 提示 2：第二段碎片",
                "content": "【第二段碎片】第二段碎片並沒有寫在 HTML 中，而是被存放在瀏覽器的本地儲存區。請在 F12 開發者工具中切換至「Application (應用程式)」分頁，展開左側「Storage -> Cookies」，查看名為 `flag_part2` 的值，將兩段碎片拼湊為完整的 `NCUMIS{...}` 送出！",
                "cost": 50,
            },
        ],
    },
    {
        "id": 40,
        "name": "教授的機密加簽信",
        "description": """聽說系上的熱門研究所課程一開放就被秒殺，幾十個同學擠在研究室門口排隊求加簽？

教授特別把今年最後一份「人工加選授權密碼 (Add-Drop Code)」加密鎖在底下這封機密信件中，宣稱只有具備密碼破譯能力的同學才能加選。你能解開這封神秘信件嗎？

📜 **[點擊拆封教授的機密加簽信件](https://im2026ctf.duckdns.org/labs/crypto)**""",
        "hints": [
            {
                "title": "💡 提示 1：第一層解密",
                "content": "【第一層解密】觀察信件中的密文特徵：末尾有 `=` 填充符號，字元由大小寫英文字母與數字組成。這是一種極常見的編碼方式（Base64）。推薦使用線上解密神器 CyberChef (From Base64) 進行第一層解碼！",
                "cost": 20,
            },
            {
                "title": "🛠️ 提示 2：第二層解密",
                "content": "【第二層解密】Base64 解碼後會看到類似 `QFXPLV{...}` 的文字，字母似乎都被固定位移了（古典密碼學的凱撒密碼 Caesar Cipher / ROT）。因為 N 被移成了 Q（位移 +3），請嘗試使用 Caesar Cipher (ROT -3 / Shift -3) 即可還原出 `NCUMIS{...}` 通關 Flag！",
                "cost": 50,
            },
        ],
    },
    {
        "id": 41,
        "name": "咪挺出席與成績系統",
        "description": """這台內部伺服器掌握了全系研究生的「咪挺出席率」與「期末考評鑑紀錄」。管理員密碼設了 30 碼連教授自己都記不得，一般人根本無法正常登入。

你能利用資料庫身分驗證邏輯的弱點，在完全不知道密碼的情況下繞過登入驗證、一窺後台真相嗎？

🛡️ **[點擊前往出席評鑑系統閘道](https://im2026ctf.duckdns.org/labs/sqli)**""",
        "hints": [
            {
                "title": "💡 提示 1：攻擊思路",
                "content": "【攻擊思路】登入驗證後台通常使用 SQL 查詢比對帳號密碼（如 `SELECT * FROM users WHERE user='$user' AND pass='$pass'`）。若未妥善過濾輸入，可透過單引號 ' 提前閉合字串，構造出恆真 (Always True) 的邏輯條件。",
                "cost": 20,
            },
            {
                "title": "🛠️ 提示 2：通關語法",
                "content": "【通關語法】在「管理員帳號」欄位直接輸入經典萬能密碼：`' OR 1=1 --` 或 `' OR ''='`，後方的 `--` 或 `#` 註解符號會將密碼比對邏輯略過，使系統判定登入成功！",
                "cost": 50,
            },
        ],
    },
    {
        "id": 42,
        "name": "這隻貓吃掉了碩士論文",
        "description": """「教授問我這週論文進度在哪裡，我說被這隻貓吃了，教授不信。」

其實學長是真的把重要文件偷偷塞進這張貓咪照片裡了！這張看似人畜無害的貓咪圖片究竟暗藏了什麼玄機？你能把被貓咪吃掉的檔案救回來嗎？

🐱 **[點擊下載吃掉論文的貓咪圖片 (cat.jpg)](https://im2026ctf.duckdns.org/download/cat)**""",
        "hints": [
            {
                "title": "💡 提示 1：隱寫原理",
                "content": "【隱寫原理】在檔案隱寫術 (Steganography) 中，常有人利用 JPEG 檔案結尾標記（FF D9）之後的空間附加其他檔案（例如 ZIP 壓縮包）。這使得檔案在看圖軟體中是一張正常圖片，但同時也是一個壓縮檔！",
                "cost": 20,
            },
            {
                "title": "🛠️ 提示 2：提取手法",
                "content": "【提取手法】\\n1. 最簡單的方式：直接將 `cat.jpg` 檔案重新命名為 `cat.zip`，然後解壓縮！\\n2. 或使用 7-Zip / WinRAR 對圖片按右鍵選擇「開啟壓縮檔」。\\n3. Linux 使用者亦可使用 `unzip cat.jpg` 或 `binwalk -e cat.jpg` 進行提取。",
                "cost": 50,
            },
        ],
    },
    {
        "id": 43,
        "name": "中央資管碩士生存戰",
        "description": """傳說中，每一位進入中央資管的新生，都必須經歷兩年（？）的修羅場考驗。
這是一款由學長開發的「中央資管碩士生涯模擬遊戲 (12 回合制)」，據說只有兼顧體力、抗壓性與論文進度、順利存活到口試畢業的勇者，才能在結算畫面上獲得系上頒發的專屬畢業證書 Flag！

身為資安專家，你可以選擇靠真實策略破關，或者發揮逆向工程分析技巧，直接解開通關秘辛！

💻 **[點擊下載 Windows 版遊戲 (mis_survival_game.exe)](https://im2026ctf.duckdns.org/download/check_graduation.exe)**
*(Windows 使用者下載後直接雙擊即可開始遊玩！)*

🐧 **[點擊下載 Linux / Mac 版遊戲 (mis_survival_game)](https://im2026ctf.duckdns.org/download/check_graduation)**
*(Linux / WSL 使用者請使用 chmod +x 賦予權限後執行)*""",
        "hints": [
            {
                "title": "💡 提示 1：破關策略指南",
                "content": "【破關策略】這是一款 12 回合的資源管理遊戲！初期先建立研究基礎，過勞時適時休息補眠，在論文有進展時把握 Meeting 提升進度，並在關鍵時刻喝下大禮堂黑咖啡回血！",
                "cost": 20,
            },
            {
                "title": "🛠️ 提示 2：逆向工程分析",
                "content": "【資安逆向解法】若想跳過遊戲直接破解，請使用 Ghidra / IDA 等逆向工具載入執行檔，分析口試通過判定函數，你會發現 Flag 是由一組位元組透過 XOR 運算即時還原出來的，逆向推導或除錯跟蹤即可取得！",
                "cost": 50,
            },
        ],
    },
]


def _quote_sql(val):
    escaped = str(val).replace("\\", "\\\\").replace("'", "''")
    return f"'{escaped}'"


sql_lines = ["SET NAMES utf8mb4;", "DELETE FROM hints;"]
for c in challenges_data:
    cid = str(c["id"])
    name_q = _quote_sql(c["name"])
    desc_q = _quote_sql(c["description"])
    sql_lines.append(
        "".join(
            [
                "UPDATE challenges SET name=",
                name_q,
                ", description=",
                desc_q,
                " WHERE id=",
                cid,
                ";",
            ]
        )
    )
    for h in c["hints"]:
        content_q = _quote_sql(h["content"])
        title_q = _quote_sql(h.get("title", ""))
        cost_str = str(h["cost"])
        sql_lines.append(
            "".join(
                [
                    "INSERT INTO hints (type, challenge_id, content, cost, requirements, title) VALUES ('standard', ",
                    cid,
                    ", ",
                    content_q,
                    ", ",
                    cost_str,
                    ", NULL, ",
                    title_q,
                    ");",
                ]
            )
        )

sql_payload = "\n".join(sql_lines)
b64_sql = base64.b64encode(sql_payload.encode("utf-8")).decode()

cmd = f"echo {b64_sql} | base64 -d | sudo docker exec -i ctfd-db-1 mariadb -uctfd -pctfd ctfd"
# skipcq: BAN-B603, BAN-B607
subprocess.run(  # nosec
    ["ssh", "-i", key, "-o", "StrictHostKeyChecking=no", host, cmd], check=True
)
print("Updated MariaDB challenge names, descriptions, and hint titles successfully!")
