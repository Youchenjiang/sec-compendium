# 📝 偵測工程與簽章撰寫深度學習路徑 (Detection Engineering - YARA, Sigma, Snort)
> 對應藍隊防衛矩陣：**領域 17** (17.1 ~ 17.4)
> 預計總投入時間：**35 ~ 45 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
只能被動等待廠商發布特徵 ──►    能獨立撰寫高品質 YARA 檔案特徵碼規則
日誌規則各家 SIEM 不相通 ──►    精通 Sigma 通用偵測語法並轉譯至 Splunk/Elastic
網路 IDS 誤報連連        ──►    能編寫嚴謹的 Suricata 網路入侵特徵規則並排除誤報
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
YARA二進位規則撰寫 Sigma日誌偵測工程  Suricata網路簽章 規則生命週期與除錯
(10h)             (10h)             (10h)            (8h)
```

---

## 🎯 階段一：YARA 二進位檔案簽章規則撰寫（約 10 小時）

```yara
rule Suspicious_WebShell_Strings {
    meta:
        description = "Detects common PHP WebShell execution strings"
        author = "BlueTeam"
        date = "2026-09-11"
    strings:
        $php = "<?php" nocase
        $eval = "eval(" ascii wide
        $base64 = "base64_decode(" ascii wide
        $system = "system(" ascii wide
    condition:
        $php at 0 and ( $eval or ( $base64 and $system ) )
}
```

---

## 📋 自我評估檢查點

- [ ] 寫出包含字串區塊與條件判斷的完整 YARA 規則。
- [ ] 說明 Sigma 規則如何實現「一次編寫，多平台轉譯 (Splunk/QRadar/Elastic)」。
- [ ] 掌握 Suricata 規則中 `content`, `offset`, `depth`, `distance` 關鍵字的精確定義。
