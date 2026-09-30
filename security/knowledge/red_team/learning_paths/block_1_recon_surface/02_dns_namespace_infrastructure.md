# 🌐 DNS 命名空間、憑證透明度與基礎設施測繪深度學習路徑 (DNS & Infrastructure)
> 對應紅隊作戰矩陣：**Phase 1 (R03、R04)** (R03.1 ~ R03.5, R04.1 ~ R04.2)  
> 預計總投入時間：**25 ~ 30 小時**（視 DNS 協定與網路路由基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
只會用 ping/nslookup 查 IP  ──►      精通 AXFR 區域傳送、TXT 驗證標籤與被動 DNS
依賴單一字典暴破子網域      ──►      精通 CT Logs 串流監控與 MassDNS 百萬級並發解析
看到 Cloudflare CDN 便放棄  ──►      精通 SSL 憑證反查、MX 標頭與 Host 碰撞穿透真實 IP
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| DNS 階層架構與記錄類型 | 熟知 A, AAAA, CNAME, MX, TXT, NS, SOA 記錄語意 | [IETF RFC 1035: DNS Specification](https://datatracker.ietf.org/doc/html/rfc1035) |
| TLS 憑證與 X.509 結構 | 理解 SAN (Subject Alternative Name)、CA 簽章與公鑰指紋 | [RFC 5280: X.509 PKI](https://datatracker.ietf.org/doc/html/rfc5280) |
| BGP 路由與 ASN 宣告 | 熟悉自治系統號 (ASN)、BGP IP Prefix 宣告與網段歸屬 | [BGP Toolkit by HE](https://bgp.he.net/) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
WHOIS/RDAP    權威/被動DNS   憑證透明度CT   BGP/ASN網段   CDN真實IP穿透
(4h)           (6h)           (6h)           (6h)           (6h)
```

---

## 🏁 階段一：WHOIS 與 RDAP 網域名稱註冊情資（約 4 小時）

### 1.1 從傳統 WHOIS 到現代 RDAP JSON
RDAP (Registration Data Access Protocol) 是 ICANN 推出的新一代結構化查詢協定，回傳標準 JSON 物件，免去正則表達式解析的脆弱性：
```bash
# 透過 RDAP API 獲取目標網域名稱結構化資料
curl -s "https://rdap.org/domain/target.com" | jq '{name: .handle, registrar: .entities[0].vcardArray[1][1][3], nameservers: [.nameservers[].ldhName]}'
```

### 1.2 反向 Whois 與關係網擴展
透過註冊人電子郵件、電話或技術聯絡人反向關聯其註冊的其他數十個影子網域。

---

## 📡 階段二：權威 DNS 枚舉與被動歷史解析（約 6 小時）

### 2.1 權威 DNS 區域傳送 (AXFR) 測試
若目標名稱伺服器配置不當，允許未授權之 AXFR 請求，將直接外洩全量內部拓撲：
```bash
# 測試目標 DNS 伺服器是否存在區域傳送漏洞
dig axfr @ns1.target.com target.com
```

### 2.2 被動 DNS (Passive DNS) 歷史解析
透過 SecurityTrails 與 VirusTotal 檢索歷史解析記錄，發現已廢棄但在內網仍有路由的「沉睡子網域 (Dangling DNS)」，評估子網域接管 (Subdomain Takeover) 風險。

---

## 📜 階段三：憑證透明度日誌 (Certificate Transparency)（約 6 小時）

### 3.1 憑證透明度 (CT Logs) 物理原理
自 2018 年起，CA 發行的每一張公開可信 TLS 憑證都必須寫入不可篡改的公開 CT 日誌庫中。攻擊者可藉此發現內網命名的子網域（如 `dev-api-internal.target.com`）：
```bash
# 透過 crt.sh API 提取目標組織所有的 SAN 憑證網域名稱
curl -s "https://crt.sh/?q=%25.target.com&output=json" \
  | jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u
```

### 3.2 高速 DNS 字典枚舉 (MassDNS)
搭配優質字典（如 SecLists），以多執行緒非同步 UDP 驗證候選網域名稱：
```bash
# 利用 MassDNS 進行百萬級子域名枚舉
massdns -r resolvers.txt -t A -o S subdomains_wordlist.txt -w resolved.txt
```

---

## 🌐 階段四：BGP、ASN 與外部網段歸屬測繪（約 6 小時）

### 4.1 自治系統號 (ASN) 與 IP 網段聚合
確認目標組織合法擁有的 IP 區段，避免攻擊踩過界到第三方託管服務商：
```bash
# 查詢目標公司的 ASN 宣告網段 (以 BGPView 為例)
curl -s "https://api.bgpview.io/asn/AS1337/prefixes" | jq '.data.ipv4_prefixes[].prefix'
```

---

## 🥷 階段五：CDN 與邊緣節點歸屬與真實 IP 穿透（約 6 小時）

### 5.1 CDN 防護機制與繞過原理
當目標網站被 Cloudflare / Akamai 代理時，直接請求只會抵達邊界節點。紅隊必須尋找目標的原始來源主機 (Origin Server)：
1. **SSL 證書公鑰反查 (Shodan / Censys)**：
   目標原始伺服器可能直接在 443 埠掛載相同的萬用字元憑證：
   ```bash
   shodan search --fields ip_str,port 'ssl.cert.subject.CN:"target.com" !http.title:"Cloudflare"'
   ```
2. **對外發起連線外帶真實 IP**：
   註冊新帳號觸發系統發送啟用郵件，檢驗郵件標頭中 `Received: from` 的原始主機 IP。
3. **Host 標頭直接碰撞驗證**：
   ```bash
   curl -k -H "Host: target.com" https://203.0.113.50/
   ```

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 能使用 `dig` 正確發起 AXFR 查詢並分析 SOA/NS 記錄。
- [ ] 能利用 crt.sh API 編寫自動化腳本獲取萬用憑證下的隱蔽子網域。
- [ ] 掌握 MassDNS 工具鏈並能有效過濾萬用解析 (Wildcard DNS) 雜訊。
- [ ] 能從 BGPView API 提取企業專屬 ASN 網段邊界。
- [ ] 能運用至少 3 種手法（憑證反查、郵件標頭溯源、Host 碰撞）定位 CDN 背後的真實原始 IP。
