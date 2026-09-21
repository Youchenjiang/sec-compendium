# Buffy + Framework 協作流程

## 角色分工

### Buffy（我）= 戰略指揮官 + 深度分析師

| 能力 | 用途 |
|------|------|
| 深度程式碼審計 | 分析複雜邏輯漏洞、追踪數據流 |
| 判斷優先順序 | 哪些題目分數高、難度低，先打 |
| 客製化 exploit | 模板搞不定的複雜漏洞 |
| Debug | exploit 失敗時分析原因 |
| 戰略決策 | 資源分配、時間管理 |

### 框架 = 自動化引擎

| 能力 | 用途 |
|------|------|
| 批次掃描 | 一次掃描所有 packages |
| 自動產生 exploit | 簡單漏洞自動化 |
| Docker 測試 | 自動驗證 exploit |
| 自動提交 | 批次提交到平台 |
| 記錄保存 | 所有結果永久保存 |

---

## 工作流程

### Phase 1: 全面掃描（框架主導）

```bash
# 框架自動掃描所有 packages
python main.py --scan-only

# 輸出：
# results/reports/*.json  → 漏洞報告
# results/writeups/*.md   → 初步 writeup
```

### Phase 2: 分析報告（ Buffy 主導）

我會看框架產生的報告，判斷：

1. **哪些漏洞最值得打**（分數高 + 難度低）
2. **哪些 exploit 框架已經自動搞定了**
3. **哪些需要我客製化**
4. **整體戰略**（先打哪幾題）

### Phase 3: 批次自動化（框架主導）

框架自動處理簡單漏洞：

```bash
# 自動產生 + 測試 + 提交
python main.py --package owasp/phprbac
```

### Phase 4: 深度攻擊（ Buffy 主導）

我接手複雜的漏洞：

1. 分析原始碼
2. 設計攻擊鏈
3. 寫客製化 exploit
4. 測試 + 調試
5. 提交

### Phase 5: 迭代優化（協作）

1. 看提交結果（AC/PA/JE）
2. 分析失敗原因
3. 改進 exploit
4. 重新提交

---

## 溝通格式

### 我問框架

```
幫我掃描 owasp/phprbac 的所有 PHP 檔案
列出所有 code injection 漏洞
幫我測試 exploit.py 在 PHP 7.4.33 環境
提交 exploit 到平台
```

### 框架回報

```json
{
  "package": "owasp/phprbac",
  "vulnerabilities": [
    {"type": "Code Injection", "file": "install.php", "line": 278, "severity": "critical"}
  ],
  "exploits_generated": 3,
  "exploits_working": 2,
  "submission": {"status": "accepted", "verdict": "AC"}
}
```

---

## 優先順序策略

### 高優先（先打）

| 指標 | 條件 |
|------|------|
| 分數 | Stars > 100 |
| 難度 | 有 known exploit pattern |
| 漏洞類型 | Code Injection / File Inclusion |
| 框架能自動化 | 模板匹配度高 |

### 中優先（其次）

| 指標 | 條件 |
|------|------|
| 分數 | Stars 50-100 |
| 難度 | 需要一些客製化 |
| 漏洞類型 | SQL Injection / Deserialization |

### 低優先（最後）

| 指標 | 條件 |
|------|------|
| 分數 | Stars < 50 |
| 難度 | 需要複雜攻擊鏈 |
| 漏洞類型 | 邏輯漏洞 / Race condition |

---

## 工具清單

### 框架工具

| 工具 | 用途 | 位置 |
|------|------|------|
| `scanner.py` | 基礎 pattern matching | bot/ |
| `advanced_scanner.py` | 進階安全規則 | bot/ |
| `generator.py` | Exploit 自動生成 | bot/ |
| `tester.py` | Docker 測試 | bot/ |
| `storage.py` | 結果持久化 | bot/ |

### 外部工具（可選）

| 工具 | 用途 | 安裝 |
|------|------|------|
| semgrep | 靜態分析 | `pip install semgrep` |
| Composer | PHP 套件管理 | 系統安裝 |
| Docker | 本地測試 | 系統安裝 |

---

## 範例：完整攻擊流程

### 1. 框架掃描

```bash
$ python main.py --scan-only

[Phase 2] Fetching packages
[+] Found 25 packages

[Phase 3] Scanning: owasp/phprbac:2.0.0
[+] Scanned 45 files
[+] Found 5 vulnerabilities
    High: 3
    Medium: 2
```

### 2. 我分析報告

看 `results/reports/owasp_phprbac.json`：

```json
{
  "vulnerabilities": [
    {
      "rule_id": "PHP-FILE-001",
      "severity": "critical",
      "file": "install.php",
      "line": 278,
      "code": "$pass=\"' . $_GET['db_auth'] . '\";",
      "exploit_pattern": "x\";system(\"cmd\");//"
    }
  ]
}
```

我判斷：**這是 code injection，可以直接 RCE，先打！**

### 3. 框架自動 exploit

```bash
$ python main.py --package owasp/phprbac

[Phase 4] Generating exploits
[+] Exploit saved: results/exploits/owasp_phprbac/code_injection.py

[Phase 5] Testing exploits
[+] Exploit successful!
    Flag 1: Found
    Flag 2: Found

[Phase 6] Submitting exploits
[+] Submitted successfully
```

### 4. 我接手複雜題

如果某題框架搞不定，我會：

1. 讀原始碼
2. 找到邏輯漏洞
3. 寫客製化 exploit
4. 測試
5. 提交

---

## 總結

| 階段 | 主導者 | 工具 |
|------|--------|------|
| 全面掃描 | 框架 | scanner.py |
| 分析決策 | Buffy | 我的判斷 |
| 簡單漏洞 | 框架 | generator.py |
| 複雜漏洞 | Buffy | 我的手寫 exploit |
| 測試 | 框架 | tester.py |
| 提交 | 框架 | client.py |
| 記錄 | 框架 | storage.py |
| Writeup | 框架 | storage.py |
