# 🗺️ 威脅情資 (CTI) 與 ATT&CK 映射深度學習路徑 (Threat Intelligence)
> 對應藍隊防衛矩陣：**領域 21** (21.1 ~ 21.3)
> 預計總投入時間：**30 ~ 40 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
只會拿 IP/Domain 對撞情資──►    理解痛苦金字塔 (Pyramid of Pain) 的攻防價值
看 ATT&CK 像看名詞字典   ──►    能將端點攻擊鏈精準映射至 TTPs 戰術矩陣
被動等待情資通報         ──►    能主動依據 APT 畫像建立假設 (Hunting Hypothesis)
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
痛苦之塔理論  MITRE ATT&CK矩陣  STIX/TAXII標準  獵捕假說設計實踐
(8h)         (10h)             (6h)            (10h)
```

---

## 🔺 階段一：Bianco 痛苦之塔 (Pyramid of Pain)（約 8 小時）

```
   /▲\\       TTPs (戰術、技術與程序)       ──► 極度痛苦 (Tough) - 迫使攻擊者重構攻擊鏈
  /───\\      Tools (攻擊工具)             ──► 具挑戰性 (Challenging) - 需重新編譯或換工具
 /─────\\     Network/Host Artifacts       ──► 煩躁 (Annoying) - 需更改 C2 配置
/───────\\    Domain Names (網域名稱)      ──► 簡單 (Simple) - 換個域名只需幾美元
─────────    IP Addresses (IP 位址)       ──► 微不足道 (Tiny) - 代理與跳板隨時更換
─────────    Hash Values (雜湊值 MD5/SHA)  ──► 毫無痛感 (Trivial) - 改動 1 個位元組雜湊即變
```

---

## 📋 自我評估檢查點

- [ ] 畫出痛苦之塔六層結構並解釋為什麼封鎖 IP 對高階 APT 幾乎無效。
- [ ] 說出 ATT&CK 戰術 (Tactics) 與技術 (Techniques) 的層級關係。
- [ ] 能撰寫一個基於 TTPs 的主動威脅獵捕假說 (Hypothesis)。
