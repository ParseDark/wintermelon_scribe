#!/bin/bash

# 冬瓜速记在线安装脚本
# 一键下载并安装冬瓜速记

set -e

VERSION="0.0.0.5.7"
# 配置
ZIP_URL="https://ghfast.top/https://github.com/ParseDark/wintermelon_scribe/archive/refs/tags/${VERSION}/wintermelon_scribe-${VERSION}.zip"
PROJECT_NAME="wintermelon_scribe-${VERSION}"
TEMP_DIR=$(mktemp -d)

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 清理函数
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

echo -e "${BLUE}🍌 冬瓜速记在线安装${NC}"

# 系统检查
[[ "$(uname)" == "Darwin" ]] || { echo -e "${RED}仅支持 macOS${NC}"; exit 1; }
command -v python3 &> /dev/null || { echo -e "${RED}需要 Python 3${NC}"; exit 1; }
python3 -m venv --help &> /dev/null || { echo -e "${RED}需要 venv 模块${NC}"; exit 1; }
command -v curl &> /dev/null || { echo -e "${RED}需要 curl${NC}"; exit 1; }
command -v unzip &> /dev/null || { echo -e "${RED}需要 unzip${NC}"; exit 1; }

echo -e "${GREEN}✓ 系统检查通过${NC}"

# 下载
cd "$TEMP_DIR"
echo -e "${BLUE}📥 下载中...${NC}"
curl -fsSL "$ZIP_URL" -o archive.zip || { echo -e "${RED}下载失败${NC}"; exit 1; }

# 解压
echo -e "${BLUE}📂 解压中...${NC}"
unzip -q archive.zip || { echo -e "${RED}解压失败${NC}"; exit 1; }

# 安装
if [ -d "$PROJECT_NAME/install.sh" ]; then
    cd "$PROJECT_NAME"
    chmod +x install.sh
    echo -e "${BLUE}⚙ 安装中...${NC}"
    ./install.sh || { echo -e "${RED}安装失败${NC}"; exit 1; }
 else
    echo -e "${RED}安装文件损坏${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 安装完成！按 Ctrl + / 开始使用${NC}"