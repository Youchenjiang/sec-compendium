# 🚪 伺服端資源信任、SSRF 內網穿透與檔案包含深度學習路徑 (SSRF & File Inclusion)
> 對應紅隊作戰矩陣：**Phase 2 (R11)** (R11.1 ~ R11.4)  
> 預計總投入時間：**30 ~ 35 小時**（視雲端架構、Linux 檔案系統與 HTTP 協定基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
SSRF 只會打 127.0.0.1 遇到過濾沒招 ──► 精通 DNS Rebinding 與 IP 各進制編碼繞過
不懂如何藉由 SSRF 拿下雲端主機    ──► 精通 AWS/GCP/Azure IMDSv1/v2 憑證竊取與橫向提權
LFI 只會讀取 /etc/passwd        ──► 精通 PHP Wrappers 濾鏡鏈、日誌投毒與 RCE 獲取
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| 公有雲中繼資料服務 (IMDS) | 理解 169.254.169.254 的鏈路本地地址與 IAM 角色憑證 | [AWS IMDS 官方文檔](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) |
| Linux 虛擬檔案系統 `/proc` | 熟悉 `/proc/self/environ`, `/proc/self/fd/`, `/proc/version` | [Linux proc man page](https://man7.org/linux/man-pages/man5/proc.5.html) |
| PHP 串流封裝協定 (Wrappers) | 理解 `php://filter`, `data://`, `php://input` 運作邏輯 | [PHP 手冊: 支援的協議與封裝協定](https://www.php.net/manual/en/wrappers.php) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
SSRF成因與繞過 雲端IMDS憑證   內網埠與服務漫遊 LFI/RFI利用鏈  日誌投毒與RCE
(8h)           (8h)           (6h)           (6h)           (5h)
```

---

## 🌐 階段一：伺服端請求偽造 (SSRF) 機制與 IP 解析過濾繞過（約 8 小時）

### 1.1 SSRF 漏洞的物理本質
當伺服端接受使用者提供的 URL 並在伺服器本機發起 HTTP/FTP 請求時，攻擊者可迫使伺服器扮演跳板，訪問其內部網路或本機服務（Bypass 防火牆邊界）。

### 1.2 黑名單過濾繞過技巧
- **十進制 / 十六進制 IP 表示法**：
  `127.0.0.1` ➔ `2130706433` (十進制) 或 `0x7f000001` (十六進制)。
- **IPv6 迴環簡寫**：`http://[::1]:80/` 或 `http://[0:0:0:0:0:ffff:127.0.0.1]/`。
- **DNS 重綁定攻擊 (DNS Rebinding)**：
  配置自定義 DNS 伺服器，第一次解析（TTL=0）返回公網合法 IP 繞過驗證，第二次連線時返回 `169.254.169.254`。

---

## ☁️ 階段二：雲端中繼資料服務 (IMDS) 憑證竊取（約 8 小時）

### 2.1 AWS IMDSv1 vs IMDSv2
- **IMDSv1 (無 Header 直接訪問)**：
  ```bash
  curl http://169.254.169.254/latest/meta-data/iam/security-credentials/EC2-Role
  ```
  直接回傳包含 `AccessKeyId`, `SecretAccessKey`, `Token` 的臨時特權憑證！
- **IMDSv2 (Session Token 機制)**：需要發送 `X-aws-ec2-metadata-token-request-ttl-seconds` 的 PUT 請求。在受限 SSRF 下較難直接利用，但可透過開放重定向或特定反向代理繞過。

---

## 📁 階段三：檔案路徑穿越與任意檔案讀取（約 6 小時）

### 3.1 路徑穿越關鍵技巧
- **遞迴過濾繞過**：若程式碼僅以 `replace("../", "")` 單次清洗，可使用 `....//....//` 繞過。
- **URL 雙重編碼**：`%252e%252e%252f` 逃避應用層檢測。

---

## 🧬 階段四：本機與遠端檔案包含 (LFI / RFI)（約 6 小時）

### 4.1 PHP Wrappers 濾鏡讀取源碼
當 `include($file)` 遇到 PHP 檔案時會直接執行而非顯示源碼。使用 Base64 編碼濾鏡可安全外帶原始碼：
```
php://filter/read=convert.base64-encode/resource=config.php
```

---

## 💣 階段五：從 LFI 躍遷至 RCE (日誌投毒與 Proc 文件利用)（約 5 小時）

### 5.1 Apache / Nginx 日誌投毒 (Log Poisoning)
1. 發送包含惡意 PHP 代碼的畸形 HTTP 請求（如在 User-Agent 寫入 `<?php system($_GET['c']); ?>`）。
2. 代碼被伺服器寫入 Access Log（如 `/var/log/apache2/access.log`）。
3. 透過 LFI 包含該日誌檔案，直譯器解析惡意代碼，達成 RCE：
   ```bash
   curl "https://target.com/index.php?page=/var/log/apache2/access.log&c=id"
   ```

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 能使用至少 3 種 IP 變形編碼方式繞過 SSRF 內部黑名單過濾。
- [ ] 掌握 AWS/GCP 雲端中繼資料端點結構與臨時金鑰提取步驟。
- [ ] 能清楚解析 DNS Rebinding 攻擊在 TTL=0 下的雙次解析競爭時序。
- [ ] 能使用 `php://filter` 串流成功提取後端 PHP 原始代碼。
- [ ] 熟練實施 Web 訪問日誌投毒與 SSH 認證日誌投毒獲取互動式 WebShell。
