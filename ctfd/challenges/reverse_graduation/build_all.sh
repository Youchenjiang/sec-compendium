#!/usr/bin/env bash
# ==============================================================================
# Challenge 43: 文字冒險遊戲 (mis_survival_game) 跨平台自動編譯腳本
# 依賴工具: Zig 0.11+ / 0.13+ 與 llvm-lipo
# ==============================================================================
set -e

SRC="check_graduation.c"
BUILD_DIR="dist"
mkdir -p "$BUILD_DIR"

echo "[*] 編譯 Windows x86_64 執行檔..."
zig cc -target x86_64-windows-gnu -O2 "$SRC" -o "$BUILD_DIR/mis_survival_game.exe"

echo "[*] 編譯 Linux x86_64 執行檔..."
zig cc -target x86_64-linux-gnu -O2 "$SRC" -o "$BUILD_DIR/mis_survival_game_linux"

echo "[*] 編譯 macOS Apple Silicon (arm64) 執行檔..."
zig cc -target aarch64-macos-none -O2 "$SRC" -o "$BUILD_DIR/mis_survival_game_mac_arm64"

echo "[*] 編譯 macOS Intel (x86_64) 執行檔..."
zig cc -target x86_64-macos-none -O2 "$SRC" -o "$BUILD_DIR/mis_survival_game_mac_intel"

echo "[*] 打包 macOS Universal Binary (跨架構通用執行檔)..."
if command -v llvm-lipo-18 &> /dev/null; then
    LIPO_BIN="llvm-lipo-18"
elif command -v llvm-lipo &> /dev/null; then
    LIPO_BIN="llvm-lipo"
elif command -v lipo &> /dev/null; then
    LIPO_BIN="lipo"
else
    echo "[!] 警告: 未找到 lipo / llvm-lipo，略過 Universal 打包，保留獨立架構檔案。"
    LIPO_BIN=""
fi

if [[ -n "$LIPO_BIN" ]]; then
    $LIPO_BIN -create "$BUILD_DIR/mis_survival_game_mac_arm64" "$BUILD_DIR/mis_survival_game_mac_intel" -output "$BUILD_DIR/mis_survival_game_mac"
    echo "[+] 成功生成 macOS 通用執行檔: $BUILD_DIR/mis_survival_game_mac"
fi

echo "[+] 全部平台編譯完成！成品位於 $BUILD_DIR/ 目錄"
