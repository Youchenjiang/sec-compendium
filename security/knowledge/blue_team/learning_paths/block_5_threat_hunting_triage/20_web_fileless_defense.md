# 👻 Web 無檔案與記憶體馬防禦深度學習路徑 (Web Fileless & Memory WebShell)
> 對應藍隊防衛矩陣：**領域 20** (20.1 ~ 20.3)
> 預計總投入時間：**30 ~ 40 小時**

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                     這份路徑帶你到達的位置
──────────────────               ────────────────────────────
以為 Web 後門一定是 .php/.jsp──►掌握記憶體馬 (Memory Shell) 磁碟無痕原理
硬碟掃描抓不到後門       ──►    能深入 Java JVM 執行緒清查 Filter/Servlet 注入
不知道怎麼排查動態注入   ──►    熟練使用 Arthas / Copagent 進行記憶體反編譯排查
```

---

## 🗺️ 整體學習地圖（四個階段）

```
階段一 → 階段二 → 階段三 → 階段四
記憶體馬原理機制  Java Filter/Servlet注入  Arthas清查與導出  .NET與PHP內存馬
(8h)            (10h)                  (10h)            (8h)
```

---

## ☕ 階段一：Java 記憶體馬運作原理（約 8 小時）

記憶體馬利用 Java 容器（如 Tomcat）的動態註冊機制，直接在 JVM 記憶體中註冊惡意物件，不需落地任何檔案：
1. **Filter 型**：向 StandardContext 註冊惡意 Filter，優先攔截所有 HTTP 請求。
2. **Servlet 型**：動態新增惡意路由與處理常式。
3. **Agent 型**：利用 Java Instrumentation API 動態修改現有類別字節碼 (Bytecode Hook)。

---

## 🔍 階段二：使用開源診斷工具 Arthas 排查實務（約 10 小時）

```bash
# 啟動 Arthas 掛載目標 Java 進程
java -jar arthas-boot.jar

# 檢索已載入且沒有對應實體檔案的異常 Filter
mbean | grep Filter
sc *.Filter*

# 反編譯記憶體中的類別位元組碼以檢視原始邏輯
jad com.example.suspicious.EvilFilter
```

---

## 📋 自我評估檢查點

- [ ] 說明為什麼傳統防毒軟體無法偵測 Java 記憶體馬。
- [ ] 說出 Tomcat Filter 型記憶體馬在請求處理流程中的攔截順序優勢。
- [ ] 能使用 Arthas 或 JVM 工具列出目標應用的所有動態註冊元件。
