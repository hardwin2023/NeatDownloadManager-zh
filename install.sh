#!/bin/bash
#
# Neat Download Manager 中文汉化 - 一键安装/恢复脚本
# =================================================
# 自动将 translated_nibs/ 内的汉化文件复制到 /Applications/NeatDownloadManager.app
# 同时复制汉化后的二进制
# 自动重签应用（ad-hoc 签名）
#

set -e

APP_PATH="/Applications/NeatDownloadManager.app"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
NIB_SRC="$SCRIPT_DIR/translated_nibs"
BIN_SRC="$SCRIPT_DIR/translated_nibs/NeatDownloadManager"
BIN_DST="$APP_PATH/Contents/MacOS/NeatDownloadManager"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ACTION="${1:-install}"  # install | restore

if [ "$ACTION" = "restore" ]; then
    echo -e "${YELLOW}=== 恢复原始 Neat Download Manager ===${NC}"
    if [ ! -f "$SCRIPT_DIR/work/NeatDownloadManager.app.backup/Contents/Resources/NeatAboutWindow.nib" ]; then
        echo -e "${RED}错误: 找不到备份。请先运行 install 安装汉化。${NC}"
        exit 1
    fi
    BACKUP="$SCRIPT_DIR/work/NeatDownloadManager.app.backup"
    echo "从备份恢复: $BACKUP"
    rm -rf "$APP_PATH"
    cp -R "$BACKUP" "$APP_PATH"
    echo -e "${GREEN}✓ 已恢复原始版本${NC}"
    exit 0
fi

echo -e "${YELLOW}=== Neat Download Manager 中文汉化安装 ===${NC}"

# 检查前提条件
if [ ! -d "$APP_PATH" ]; then
    echo -e "${RED}错误: 找不到 $APP_PATH${NC}"
    echo "请先安装 Neat Download Manager"
    exit 1
fi

if [ ! -d "$NIB_SRC" ]; then
    echo -e "${RED}错误: 找不到 $NIB_SRC${NC}"
    echo "请确认下载的汉化包完整"
    exit 1
fi

# 关闭 NDM
echo "关闭 Neat Download Manager..."
pkill -f NeatDownloadManager 2>/dev/null || true
sleep 1

# 备份原始版本（首次安装时）
if [ ! -d "$SCRIPT_DIR/work/NeatDownloadManager.app.backup" ]; then
    echo "备份原始版本..."
    mkdir -p "$SCRIPT_DIR/work"
    cp -R "$APP_PATH" "$SCRIPT_DIR/work/NeatDownloadManager.app.backup"
    cp "$APP_PATH/Contents/MacOS/NeatDownloadManager" "$SCRIPT_DIR/work/NeatDownloadManager.bin.backup" 2>/dev/null || true
fi

# 移除旧签名
echo "移除旧代码签名..."
codesign --remove-signature "$APP_PATH" 2>/dev/null || true

# 复制汉化后的 NIB 文件
echo "复制汉化后的 NIB 文件..."
for nib in "$NIB_SRC"/*.nib; do
    name=$(basename "$nib")
    if [ -d "$nib" ]; then
        # 目录格式（如 NeatMainWindow.nib/）
        rm -rf "$APP_PATH/Contents/Resources/$name"
        cp -R "$nib" "$APP_PATH/Contents/Resources/$name"
        echo "  ✓ $name (目录)"
    else
        # 单文件格式
        rm -f "$APP_PATH/Contents/Resources/$name"
        cp "$nib" "$APP_PATH/Contents/Resources/$name"
        echo "  ✓ $name"
    fi
done

# 复制 Base.lproj 下的主窗口
if [ -d "$NIB_SRC/Base.lproj" ]; then
    echo "复制主窗口 NIB (Base.lproj)..."
    for nib in "$NIB_SRC/Base.lproj"/*.nib; do
        name=$(basename "$nib")
        if [ -d "$nib" ]; then
            rm -rf "$APP_PATH/Contents/Resources/Base.lproj/$name"
            mkdir -p "$APP_PATH/Contents/Resources/Base.lproj"
            # 复制目录内的所有文件，不创建多余的子目录
            mkdir -p "$APP_PATH/Contents/Resources/Base.lproj/$name"
            for f in "$nib"/*; do
                fname=$(basename "$f")
                cp "$f" "$APP_PATH/Contents/Resources/Base.lproj/$name/$fname"
            done
            echo "  ✓ Base.lproj/$name (目录)"
        fi
    done
fi

# 复制汉化后的二进制
if [ -f "$BIN_SRC" ]; then
    echo "复制汉化后的二进制..."
    cp "$BIN_SRC" "$BIN_DST"
    chmod +x "$BIN_DST"
    echo "  ✓ NeatDownloadManager (二进制)"
fi

# ad-hoc 重签
echo "重签应用 (ad-hoc)..."
codesign --force --deep --sign - "$APP_PATH" 2>&1 | sed 's/^/  /'
codesign --verify --deep "$APP_PATH" 2>&1 | sed 's/^/  /' && echo -e "${GREEN}  ✓ 签名验证通过${NC}"

echo ""
echo -e "${GREEN}=== 安装完成 ===${NC}"
echo ""
echo "启动 NDM 即可看到中文界面。"
echo ""
echo "如需恢复英文原版，请运行: $0 restore"
echo ""
echo "注意事项:"
echo "  1. 首次打开时如被 Gatekeeper 拦截，请在 '系统设置 → 隐私与安全性' 中点击 '仍要打开'"
echo "  2. NDM 升级后汉化会被覆盖，请重新运行本脚本"
echo "  3. 安装脚本会在 work/ 目录保留原始备份，方便恢复"
