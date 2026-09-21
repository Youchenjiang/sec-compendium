# 📧 電子郵件與社交工程防衛深度學習路徑 (Email Security & Anti-Phishing)
> 對應藍隊防衛矩陣：**領域 10** (10.1 ~ 10.4)
> 預計總投入時間：**30 ~ 40 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
單純看寄件者顯示名稱判斷 ──►    能深入解析 EML 標頭 Received 路由與發信 IP
不知道 SPF/DKIM 是什麼   ──►    精通三大郵件驗證協定與 DMARC 聚合回報配置
收到 Office 文件直接點開 ──►    能用 oledump 萃取巨集混淆程式碼並排查 Quishing
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
郵件三大認證協定  EML標頭路由剖析  惡意巨集與附件提取  QR Code釣魚與網址還原
(8h)             (10h)            (10h)              (8h)
```

---

## 🏁 階段一：三大郵件防偽認證協定 (SPF / DKIM / DMARC)（約 8 小時）

### 1.1 SPF (Sender Policy Framework)

- 記載於發信網域的 DNS `TXT` 記錄中。
- 列出授權發信的伺服器 IP 清單：`v=spf1 ip4:192.0.2.1 include:_spf.google.com -all`
  - `-all` (Fail): 硬阻斷未授權來源。
  - `~all` (SoftFail): 標記為可疑/垃圾郵件但允許接收。

### 1.2 DKIM (DomainKeys Identified Mail)

- 透過非對稱加密對郵件標頭與內容計算數位簽章。
- 發信端以私密金鑰簽署，收信端依據寄件網域 DNS 公開金鑰驗證信件是否在傳輸中途被竄改。

### 1.3 DMARC (Domain-based Message Authentication)

- 結合 SPF 與 DKIM 驗證結果，並定義收信端處置原則：
  - `p=none` (僅監控回報)
  - `p=quarantine` (隔離至垃圾箱)
  - `p=reject` (直接拒絕接收退信)

---

## 🔍 階段二：EML 郵件原始碼與 Received 路由溯源（約 10 小時）

```http
Received: from mail.attacker.com (attacker.com [198.51.100.25])
    by mx.company.com with ESMTP id ABC12345
    for <victim@company.com>; Wed, 11 Sep 2026 10:00:00 +0800
Received: from [10.0.0.5] (unknown [203.0.113.88])
    by mail.attacker.com with HTTP; ...
```

> 💡 **鑑識定律**：**由下往上看 (Bottom-Up)**！最下方的 `Received` 欄位代表最初發信客戶端與第一跳郵件伺服器的真實 IP！

---

## 📎 階段三：誘餌文件分析與 oledump 巨集程式碼提取（約 10 小時）

```bash
# 查看 Office 文件內的所有資料串流 (Stream)
python oledump.py maldoc.doc

# 針對帶有 'M' (含有巨集代碼) 的 Stream 進行解壓縮檢視
python oledump.py -s 7 -v maldoc.doc
```

---

## 📋 自我評估檢查點

- [ ] 清楚說明 SPF、DKIM、DMARC 三者在郵件防禦體系中的互補關係。
- [ ] 能在純文字郵件標頭中找出真實發信 IP，不受偽造的 `From:` 與 `Reply-To:` 欺騙。
- [ ] 熟練使用 `oledump.py` 提取出包含 AutoOpen/Document_Open 觸發器的 VBA 代碼。
