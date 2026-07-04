#!/bin/bash
# Neat Download Manager 中文汉化安装脚本
# 用法: ./install.sh          安装汉化
#       ./install.sh --restore 恢复英文原版

set -e

APP_PATH="/Applications/NeatDownloadManager.app"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NIB_SRC="${SCRIPT_DIR}/translated_nibs"
BACKUP_DIR="${HOME}/Desktop/NeatDownloadManager.app.backup"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${CYAN}[信息]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[成功]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[警告]${NC} $1"
}

print_error() {
    echo -e "${RED}[错误]${NC} $1"
}

# 检查是否为恢复操作
if [ "$1" = "--restore" ]; then
    print_info "开始恢复英文原版..."
    
    if [ ! -d "$BACKUP_DIR" ]; then
        print_error "未找到备份文件: $BACKUP_DIR"
        print_info "请从官网重新下载安装: https://neatdownloadmanager.com"
        exit 1
    fi
    
    pkill -f NeatDownloadManager 2>/dev/null || true
    sleep 1
    
    cp -R "$BACKUP_DIR/"* "$APP_PATH/"
    codesign --force --deep --sign - "$APP_PATH"
    
    print_success "已恢复英文原版！"
    exit 0
fi

# === 安装流程 ===

echo ""
echo "============================================"
echo "  Neat Download Manager 中文汉化安装程序"
echo "============================================"
echo ""

# 1. 检查 NDM 是否已安装
print_info "检查 Neat Download Manager 是否已安装..."
if [ ! -d "$APP_PATH" ]; then
    print_error "未找到 Neat Download Manager: $APP_PATH"
    print_info "请先从官网下载安装: https://neatdownloadmanager.com"
    exit 1
fi
print_success "已检测到 Neat Download Manager"

# 2. 检查汉化文件
print_info "检查汉化文件..."
if [ ! -d "$NIB_SRC" ]; then
    print_error "未找到汉化文件目录: $NIB_SRC"
    exit 1
fi
NIB_COUNT=$(ls -1 "$NIB_SRC"/*.nib 2>/dev/null | wc -l | tr -d ' ')
if [ "$NIB_COUNT" -eq 0 ]; then
    print_error "汉化文件目录中没有 .nib 文件"
    exit 1
fi
print_success "找到 $NIB_COUNT 个汉化 NIB 文件"

# 3. 检查 codesign 命令
print_info "检查 codesign 命令..."
if ! command -v codesign &> /dev/null; then
    print_error "未找到 codesign 命令"
    print_info "请安装 Xcode Command Line Tools: xcode-select --install"
    exit 1
fi
print_success "codesign 命令可用"

# 4. 关闭正在运行的 NDM
print_info "关闭正在运行的 Neat Download Manager..."
pkill -f NeatDownloadManager 2>/dev/null || true
sleep 2

# 5. 备份原始应用
print_info "备份原始应用到: $BACKUP_DIR"
if [ -d "$BACKUP_DIR" ]; then
    print_warn "备份目录已存在，将覆盖"
    rm -rf "$BACKUP_DIR"
fi
cp -R "$APP_PATH" "$BACKUP_DIR"
print_success "备份完成"

# 6. 移除代码签名
print_info "移除代码签名..."
codesign --remove-signature "$APP_PATH" 2>/dev/null || true
print_success "签名已移除"

# 7. 替换 NIB 文件
print_info "替换 NIB 文件..."
RES_DIR="$APP_PATH/Contents/Resources"
for nib in "$NIB_SRC"/*.nib; do
    name=$(basename "$nib")
    rm -rf "$RES_DIR/$name"
    cp -R "$nib" "$RES_DIR/$name"
done
print_success "NIB 文件替换完成"

# 8. 重新签名
print_info "重新 ad-hoc 签名..."
codesign --force --deep --sign - "$APP_PATH"
print_success "签名完成"

# 9. 验证签名
print_info "验证签名..."
if codesign --verify --deep --strict "$APP_PATH" 2>/dev/null; then
    print_success "签名验证通过"
else
    print_warn "签名验证有警告（通常不影响使用）"
fi

# 10. 完成
echo ""
echo "============================================"
echo "  ${GREEN}汉化安装完成！${NC}"
echo "============================================"
echo ""
print_info "备份位置: $BACKUP_DIR"
print_info "如需恢复英文原版，运行: ./install.sh --restore"
print_info "正在启动应用..."
echo ""
open "$APP_PATH"
