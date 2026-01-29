#!/bin/bash

# 冬瓜速记在线安装脚本 - 自动下载最新版本并安装
# 自动生成的文件，请勿手动修改！

set -e

# 配置信息
REPO_OWNER="ParseDark"
REPO_NAME="wintermelon_scribe"
# LATEST_VERSION 和下载链接会在 Release 时自动更新
LATEST_VERSION="0.0.5.3"
MIRROR_BASE_URL="https://ghfast.top/https://github.com"

# 下载链接（自动更新）
MAC_ARM_URL="${MIRROR_BASE_URL}/${REPO_OWNER}/${REPO_NAME}/releases/download/${LATEST_VERSION}/wintermelon_scribe-macos-arm64.tar.gz"
MAC_INTEL_URL="${MIRROR_BASE_URL}/${REPO_OWNER}/${REPO_NAME}/releases/download/${LATEST_VERSION}/wintermelon_scribe-macos-x86_64.tar.gz"
SOURCE_ZIP_URL="${MIRROR_BASE_URL}/${REPO_OWNER}/${REPO_NAME}/archive/refs/tags/${LATEST_VERSION}/${REPO_NAME}-${LATEST_VERSION}.zip"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 显示横幅
echo -e "${BLUE}🍐 冬瓜速记 在线安装程序${NC}"
echo -e "${BLUE}==============================${NC}"
echo ""

# 检查系统
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}❌ 此安装脚本仅支持 macOS${NC}"
    exit 1
fi

# 检查架构
ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" ]]; then
    DOWNLOAD_URL=$MAC_ARM_URL
    ARCH_NAME="Apple Silicon (M1/M2/M3)"
elif [[ "$ARCH" == "x86_64" ]]; then
    DOWNLOAD_URL=$MAC_INTEL_URL
    ARCH_NAME="Intel (x86_64)"
else
    echo -e "${RED}❌ 不支持的架构: ${ARCH}${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 检测到系统: macOS ${ARCH_NAME}${NC}"
echo -e "${GREEN}✅ 最新版本: ${LATEST_VERSION}${NC}"
echo ""

# 选择安装目录
INSTALL_DIR="$HOME/wintermelon_scribe"
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠️  检测到已安装的版本${NC}"
    read -p "是否要重新安装？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}安装已取消${NC}"
        exit 0
    fi
    echo -e "${YELLOW}🗑️  清理旧版本...${NC}"
    rm -rf "$INSTALL_DIR"
fi

# 创建安装目录
echo -e "${BLUE}📁 创建安装目录...${NC}"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# 下载文件
ARCHIVE_NAME="wintermelon_scribe-${LATEST_VERSION}.tar.gz"
echo -e "${BLUE}⬇️  下载最新版本...${NC}"
echo -e "${BLUE}   URL: ${DOWNLOAD_URL}${NC}"

# 使用 curl 下载
if command -v curl >/dev/null 2>&1; then
    curl -L -o "$ARCHIVE_NAME" "$DOWNLOAD_URL"
else
    echo -e "${RED}❌ 未找到 curl，请先安装 curl${NC}"
    exit 1
fi

# 检查下载是否成功
if [ ! -f "$ARCHIVE_NAME" ]; then
    echo -e "${RED}❌ 下载失败！${NC}"
    echo -e "${YELLOW}💡 如持续失败，可以手动下载源码：${NC}"
    echo -e "${YELLOW}   ${SOURCE_ZIP_URL}${NC}"
    exit 1
fi

# 解压
echo -e "${BLUE}📦 解压文件...${NC}"
tar -xzf "$ARCHIVE_NAME"

# 查找解压后的目录
EXTRACTED_DIR=$(find . -maxdepth 1 -type d -name "wintermelon_scribe*" | head -1)
if [ -z "$EXTRACTED_DIR" ]; then
    echo -e "${RED}❌ 解压后未找到程序目录${NC}"
    exit 1
fi

# 移动文件到安装目录
echo -e "${BLUE}🔧 安装文件...${NC}"
mv "$EXTRACTED_DIR"/* .
rmdir "$EXTRACTED_DIR"
rm "$ARCHIVE_NAME"

# 设置权限
chmod +x install.sh uninstall.sh start.sh status.sh

# 安装依赖
echo -e "${BLUE}📚 安装依赖...${NC}"
if [ -f "requirements.txt" ]; then
    if command -v uv >/dev/null 2>&1; then
        uv venv
        uv pip install -r requirements.txt
    else
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
    fi
fi

# 创建桌面快捷方式
echo -e "${BLUE}🖥️  创建桌面快捷方式...${NC}"
DESKTOP_LINK="$HOME/Desktop/冬瓜速记.command"
cat > "$DESKTOP_LINK" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
./start.sh
EOF
chmod +x "$DESKTOP_LINK"

# 安装服务（可选）
echo ""
read -p "是否要安装为后台服务（开机自启动）？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "install.sh" ]; then
        echo -e "${BLUE}🔧 安装服务...${NC}"
        ./install.sh
    fi
fi

# 完成
echo ""
echo -e "${GREEN}✅ 安装完成！${NC}"
echo ""
echo -e "${BLUE}启动方式：${NC}"
echo -e "  1. 双击桌面上的 ${YELLOW}冬瓜速记.command${NC}"
echo -e "  2. 在终端运行: ${YELLOW}cd $INSTALL_DIR && ./start.sh${NC}"
echo ""
echo -e "${BLUE}卸载方式：${NC}"
echo -e "  在终端运行: ${YELLOW}cd $INSTALL_DIR && ./uninstall.sh${NC}"
echo ""
echo -e "${GREEN}🎉 感谢使用冬瓜速记！${NC}"