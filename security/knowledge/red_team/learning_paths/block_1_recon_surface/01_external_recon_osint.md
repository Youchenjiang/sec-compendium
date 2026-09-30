# 🌐 組織架構、人員情報與公開代碼倉庫洩漏深度學習路徑 (OSINT & Digital Footprint)
> 對應紅隊作戰矩陣：**Phase 1 (R01、R02)** (R01.1 ~ R01.2, R02.1 ~ R02.2)  
> 預計總投入時間：**20 ~ 25 小時**（視情報收集與文字探勘熟練度而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
只會用 Google 搜尋公司名稱 ──►        能透過 SEC 10-K 與工商數據穿透多層股權架構
依賴手工查找目標郵件       ──►        精通 Hunter.io 模式與 theHarvester 自動化枚舉
以為開源代碼只看當前檔案   ──►        精通 Git 歷史樹遍歷與 TruffleHog 高熵值金鑰萃取
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| 商業法人登記與證券監管 | 理解母公司、子公司、持股比例與 SEC EDGAR 申報法規意義 | [SEC EDGAR 檢索指南](https://www.sec.gov/edgar/searchedgar/companysearch) |
| Regex 正則表達式與語法過濾 | 熟練使用正則表達式篩選 Email、API Key 與 IP 格式 | [Regex101 線上除錯](https://regex101.com/) |
| Git 內部版本控制結構 | 理解 `.git/` 目錄、commit 物件、樹狀節點與分支歷史 | [Pro Git 官方開源手冊](https://git-scm.com/book/zh-tw/v2) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
法定實體穿透   人員與職能枚舉  搜尋引擎進階   代碼倉庫金鑰   防禦規避與合規
(4h)           (5h)           (5h)           (6h)           (3h)
```

---

## 🏁 階段一：法定實體結構與商業股權穿透（約 4 小時）

### 1.1 SEC 10-K 表格與附錄 21 (Exhibit 21) 剖析
在針對跨國企業發起紅隊演練時，母公司通常具有頂級防護，但剛收購的子公司往往存在遺留系統與薄弱邊界。
- **Exhibit 21 的法定意義**：美股上市公司依法必須在年度 10-K 申報的 Exhibit 21 中列出其所有重大子公司名稱及註冊地。
- **自動化抓取 SEC EDGAR API**：
  ```bash
  # 查詢目標公司的 CIK 編號並獲取申報文件索引
  curl -s "https://data.sec.gov/submissions/CIK0001337000.json" \
    -H "User-Agent: ResearchAnalyst admin@example.com" | jq '.filings.recent'
  ```

### 1.2 全球工商登記與 OpenCorporates 整合
利用法人代表、董監事名單與登記地址進行跨國實體關聯：
```bash
# 透過 OpenCorporates API 查詢特定集團名下所有子實體
curl -s "https://api.opencorporates.com/v0.4/companies/search?q=Target+Holdings" \
  | jq -r '.results.companies[].company | "\(.name) | \(.jurisdiction_code) | \(.company_number)"'
```

---

## 👥 階段二：公開人員職能與公務電子郵件枚舉（約 5 小時）

### 2.1 企業郵箱命名慣例逆推
企業通常採用標準化的郵件生成規則（如 `{first}.{last}@corp.com` 或 `{f}{last}@corp.com`）：
1. 檢索公開發表的白皮書、專利文件或新聞稿聯絡人。
2. 利用 Hunter.io API 驗證網域之電子郵件模式與可信度：
   ```bash
   curl -s "https://api.hunter.io/v2/domain-search?domain=target.com&api_key=YOUR_API_KEY" | jq '.data.pattern'
   ```

### 2.2 theHarvester 多來源情報聚合實作
```bash
# 針對目標網域，從 LinkedIn、Bing、DuckDuckGo 併發提取人員與郵件
theHarvester -d target.com -b bing,duckduckgo,linkedin -l 500 -f target_recon.xml
```

---

## 🔍 階段三：開放網路搜尋引擎情資偵察 (Google Dorking)（約 5 小時）

### 3.1 關鍵進階搜尋語法
- `site:target.com filetype:pdf "internal use only"`：挖掘機密內部文檔。
- `site:target.com inurl:admin | inurl:login | inurl:portal`：定位外部登入閘道。
- `site:target.com ext:env | ext:yml | ext:sql | ext:log`：尋找意外暴露的配置與備份檔。

### 3.2 歷史快照與廢棄端點還原
利用 Wayback Machine API 檢索目標網域已被下架的 API 文件或歷史檔案路徑：
```bash
curl -s "http://web.archive.org/cdx/search/cdx?url=*.target.com/*&output=json&fl=original&collapse=urlkey" \
  | jq -r '.[][]' | grep -iE "\.(json|sql|env|bak|zip)"
```

---

## 🔑 階段四：公開代碼倉庫與高熵值金鑰洩漏偵察（約 6 小時）

### 4.1 Git 歷史 Commit 深度回溯
開發者往往在發布代碼前刪除了包含金鑰的檔案，但該檔案仍存在於 Git commit 歷史中。
```bash
# 使用 git log 搜尋包含關鍵字的所有歷史提交
git log -p -S "AWS_SECRET_ACCESS_KEY"

# 檢視歷史特定 commit 的內容
git show <commit-hash>
```

### 4.2 TruffleHog 高熵值秘密偵測
TruffleHog 能夠透過 Shannon 資訊熵演算法與 Regex 特徵，掃描整個 Git 倉庫歷史中隱藏的私鑰、Slack Webhook、Token 等：
```bash
# 掃描目標開源倉庫的全量 Git 歷史
trufflehog git https://github.com/target-org/open-project.git --json
```

---

## 🛡️ 階段五：被動情報防禦規避與合規審查（約 3 小時）

### 5.1 100% 被動模式保障
- 本階段所有操作嚴格限制於公開資料庫與中介索引伺服器，**嚴禁發送任何直接抵達目標網路介面的 TCP/UDP 封包**。
- 透過 Tor / 商業代理輪替查詢，防止 Google Dorking 或 API 查詢觸發來源 IP 限流或告警。

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 能自 SEC EDGAR 10-K 中精確提取 Exhibit 21 子公司清單並識別併購盲區。
- [ ] 能根據已知少數員工郵箱，逆推出全組織的標準郵件命名正規化規則。
- [ ] 熟練運用 5 種以上 Google Dorking 語法定位外部敏感暴露文件。
- [ ] 掌握 Wayback Machine CDX API 批次導出歷史備份路徑。
- [ ] 能使用 TruffleHog 在 Git 儲存庫完整歷史中挖掘已刪除的 API Key。
