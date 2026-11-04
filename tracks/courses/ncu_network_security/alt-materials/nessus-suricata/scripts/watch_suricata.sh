#!/usr/bin/env bash
# 在靶機上跑：更新 ET Open 規則、用指定網卡起 Suricata、盯 alert。
# 用法： sudo ./watch_suricata.sh <網卡名，例如 ens33>
set -e

IFACE="${1:?用法: sudo ./watch_suricata.sh <網卡名，例如 ens33>}"

echo "[*] 更新 ET Open 規則..."
suricata-update

echo "[*] 確認 CVE-2021-41773 的規則有載到..."
if grep -Rq 41773 /var/lib/suricata/rules/ 2>/dev/null; then
    echo "    OK：找到規則（SID 2034124/2034125/2034126）"
else
    echo "    [!] 警告：規則集裡找不到 41773，Suricata 可能不會對攻擊跳 alert。"
    echo "        先確認 suricata-update 有成功、ET Open 已啟用。"
fi

echo "[*] 用 $IFACE 啟動 Suricata（alert 寫到 /var/log/suricata/fast.log）"
suricata -i "$IFACE" -D
sleep 2

echo "[*] 盯 alert（Ctrl-C 離開；Suricata 仍在背景跑）："
tail -f /var/log/suricata/fast.log
