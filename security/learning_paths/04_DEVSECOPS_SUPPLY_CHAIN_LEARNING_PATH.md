# 📦 軟體供應鏈安全 (DevSecOps) 深度學習路徑
> 對應藍隊防衛矩陣：**領域 4** (4.1 ~ 4.3)
> 預計總投入時間：**30 ~ 40 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
直接 npm/pip install 套件 ──►    能識別相依性混淆 (Dependency Confusion) 投毒
不知道什麼是 SBOM        ──►    能熟練使用 Syft/Grype 產生並審查 SPDX/CycloneDX
只在最後階段找漏洞       ──►    能將 SAST/DAST/Secret Scan 融入 CI/CD 管道
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
供應鏈攻擊手法  SBOM標準解析  CI/CD密鑰審計  DevSecOps流水線實作
(8h)          (8h)          (6h)          (10h)
```

---

## 🏁 階段一：現代軟體供應鏈攻擊手法剖析（約 8 小時）

### 1.1 相依性混淆 (Dependency Confusion)

- 企業內部常有私有套件（如 `corp-auth-utils`）。
- 攻擊者在公開倉庫（npm, PyPI）註冊同名套件，但將版本號提高為 `99.0.0`。
- 若建置系統未嚴格限定私有來源，套件管理器會自動抓取版本號較高的惡意公開套件執行安裝腳本。

### 1.2 搶注域名與錯字偽造 (Typosquatting)

- 攻擊者註冊與熱門套件極為相似的名稱（例如將 `requests` 拼寫為 `requsts` 或 `python-requests`）。
- 惡意套件在 `setup.py` 或 `preinstall` 腳本中植入反彈 Shell 或竊密腳本。

---

## 📄 階段二：軟體物料清單 (SBOM) 標準與審查實戰（約 8 小時）

### 2.1 兩大主流 SBOM 標準對比

| 標準名稱 | 主導機構 | 核心特點 | 常見格式 |
|---------|---------|---------|---------|
| **SPDX** | Linux Foundation (ISO/IEC 5962) | 強調軟體版權授權合規、精確套件雜湊 | JSON, YAML, Tag:Value |
| **CycloneDX** | OWASP | 專為資安脆弱性追蹤 (Vulnerability Analysis) 設計 | JSON, XML |

### 2.2 使用開源工具 Syft 與 Grype 生成與掃描

```bash
# 使用 Syft 掃描 Docker 映像檔並產出 CycloneDX JSON 格式 SBOM
syft packages alpine:latest -o cyclonedx-json > sbom.json

# 使用 Grype 依據 SBOM 自動比對已知 CVE 漏洞庫
grype sbom:sbom.json
```

---

## 🔑 階段三：CI/CD 管道審計與密鑰洩漏防禦（約 6 小時）

### 3.1 程式碼密鑰掃描工具 Trivy & Gitleaks

```bash
# 使用 Gitleaks 掃描 Git 全提交歷史中的硬編碼金鑰
gitleaks detect --source . -v

# 使用 Trivy 掃描專案相依性與配置檔案錯誤 (IaC Misconfigurations)
trivy fs --security-checks vuln,config,secret .
```

---

## 📋 自我評估檢查點

- [ ] 清楚說明相依性混淆與錯字搶注的攻擊機制及管道隔離對策。
- [ ] 解釋 SBOM 兩大格式 SPDX 與 CycloneDX 的適用場景。
- [ ] 能在 GitHub Actions 或本機透過指令產出 Container 映像檔的 SBOM 並用 Grype 找出 CVE。
