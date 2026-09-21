#!/usr/bin/env bash
# ==============================================================================
# NCU CTFd Kit: 一鍵快速部署與外掛安裝腳本
# 用途: 快速將本套件中的自研外掛、修補檔案與客製化設定套用至目標 CTFd 伺服器
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CTFD_DIR="${1:-${HOME}/CTFd}"

if [[ ! -d "$CTFD_DIR" ]]; then
    echo "[!] 找不到 CTFd 目錄: $CTFD_DIR"
    echo "使用方式: ./install.sh [CTFd目錄路徑]"
    exit 1
fi

echo "[*] 目標 CTFd 路徑: $CTFD_DIR"

# 1. 複製 dynamic_shuffle_flag 插件
echo "[+] 安裝 dynamic_shuffle_flag 插件..."
mkdir -p "$CTFD_DIR/CTFd/plugins"
cp -r "$SCRIPT_DIR/plugins/dynamic_shuffle_flag" "$CTFD_DIR/CTFd/plugins/"

# 2. 詢問是否套用核心修補檔案
if [[ -f "$SCRIPT_DIR/patches/core_changes.patch" ]]; then
    echo "[?] 是否套用核心自訂修改（包含首殺加分、自訂主題與繁中化）? (y/N)"
    read -r apply_patch
    if [[ "$apply_patch" =~ ^[Yy]$ ]]; then
        echo "[+] 套用 Git Patch..."
        cd "$CTFD_DIR"
        git apply "$SCRIPT_DIR/patches/core_changes.patch" || echo "[!] Patch 套用時有衝突，請手動檢視 patches/core_changes.patch"
        cd - > /dev/null
    fi
fi

# 3. 重啟 CTFd 容器
echo "[+] 重新載入 CTFd 服務..."
cd "$CTFD_DIR"
docker compose restart ctfd || docker-compose restart ctfd

echo "=================================================="
echo "🎉 部署完成！"
echo "- 動態 Flag 路由與下載功能已就緒。"
echo "- 競賽自動維運腳本位於 automation/sync_challenges.py 與 send_final_top10.py"
echo "=================================================="
