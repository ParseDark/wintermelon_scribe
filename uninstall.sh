#!/bin/bash

# 冬瓜速记卸载脚本

set -e

# 服务名称
SERVICE_NAME="com.wintermelon.scribe"
PLIST_FILE="$HOME/Library/LaunchAgents/$SERVICE_NAME.plist"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🗑️  冬瓜速记卸载程序${NC}"

# 检查是否已安装
if [ ! -f "$PLIST_FILE" ]; then
    echo -e "${YELLOW}⚠️  未找到安装的服务${NC}"
    exit 0
fi

# 停止服务
if launchctl list | grep -q "$SERVICE_NAME"; then
    echo -e "${BLUE}停止服务...${NC}"
    launchctl stop "$SERVICE_NAME" 2>/dev/null || true
fi

# 卸载 Launch Agent
echo -e "${BLUE}卸载服务...${NC}"
launchctl unload "$PLIST_FILE" 2>/dev/null || true

# 删除 plist 文件
rm "$PLIST_FILE" 2>/dev/null || true
echo -e "${GREEN}✅ Launch Agent 已卸载${NC}"

# 询问是否删除日志
echo ""
read -p "是否删除日志文件? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    PROJECT_DIR="$(dirname "$0")"
    PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"
    if [ -d "$PROJECT_DIR/logs" ]; then
        rm -rf "$PROJECT_DIR/logs"
        echo -e "${GREEN}✅ 日志已删除${NC}"
    fi
fi

# 询问是否删除虚拟环境
echo ""
read -p "是否删除虚拟环境 (.venv)? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    PROJECT_DIR="$(dirname "$0")"
    PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"
    if [ -d "$PROJECT_DIR/.venv" ]; then
        rm -rf "$PROJECT_DIR/.venv"
        echo -e "${GREEN}✅ 虚拟环境已删除${NC}"
    fi
fi

echo ""
echo -e "${GREEN}🎉 卸载完成！${NC}"
echo -e "${BLUE}如需重新安装，运行: ./install.sh${NC}"