# 🟣 紫隊自動化對抗模擬靶場 (Atomic Purple Range)

> **對接手冊**:
> - [27.1 模組化攻擊模擬：Atomic Red Team 原子測試手冊](../../27.1_automated_adversary_emulation_atomic_red_team.md)
> - [27.2 自動化對抗演練平台：MITRE Caldera 實戰指南](../../27.2_automated_adversary_emulation_platform_caldera.md)

---

## 🎯 靶場架構

本環境透過 Docker Compose 一鍵啟動：
1. **Caldera C2 Server (172.28.0.10:8888)**: 提供圖形化紅藍對抗指揮調度後台，預先啟用 `sandcat`、`stockpile`、`atomic` 外掛。
2. **Victim Node (172.28.0.20)**: Linux Ubuntu 靶機，內建 Auditd 鑑識日誌監控規則，模擬企業伺服器。

---

## 🚀 快速啟動

```bash
# 1. 啟動靶場容器叢集
docker compose up -d

# 2. 檢視容器狀態
docker compose ps

# 3. 進入 Caldera Web 控制台
# 瀏覽器造訪: http://localhost:8888
# 預設紅隊帳號: admin / admin
# 預設藍隊帳號: blue / blue123
```

---

## ⚔️ 紫隊對抗演練步驟

### 步驟一：在受測靶機一鍵觸發原子化攻擊 (Red Team)
```bash
docker compose exec victim-linux bash /opt/scripts/run_atomic_attack.sh
```

### 步驟二：在受測靶機驗證防禦規則捕獲 (Blue Team)
```bash
# 檢驗 Auditd 是否捕捉到 /etc/shadow 的未授權存取
docker compose exec victim-linux ausearch -k shadow_access -i

# 檢驗 Bash 混淆指令執行軌跡
docker compose exec victim-linux cat /tmp/purple_attack_execution.log
```

---

## 🧹 環境銷毀與清理

```bash
docker compose down -v
```
