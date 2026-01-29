#!/bin/bash

# 冬瓜速记安装脚本 - 一键安装并在后台运行

set -e

# 项目路径 - 获取脚本的绝对路径
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="com.wintermelon.scribe"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 冬瓜速记安装程序${NC}"
echo ""

# 检查系统
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}❌ 此安装脚本仅支持 macOS${NC}"
    exit 1
fi

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到 python3，请先安装 Python 3${NC}"
    exit 1
fi

# 检查是否存在必要文件
if [ ! -f "$PROJECT_DIR/main.py" ]; then
    echo -e "${RED}❌ 未找到 main.py，请确保在正确的目录运行安装脚本${NC}"
    exit 1
fi

# 检查并创建虚拟环境
if [ ! -d "$PROJECT_DIR/.venv" ]; then
    echo -e "${BLUE}📦 创建虚拟环境...${NC}"
    python3 -m venv "$PROJECT_DIR/.venv"
fi

# 激活虚拟环境并安装依赖
source "$PROJECT_DIR/.venv/bin/activate"

# 检查 uv 是否可用（更快的包管理器）
if command -v uv &> /dev/null; then
    echo -e "${BLUE}📚 使用 uv 安装依赖...${NC}"
    uv pip install -q -r "$PROJECT_DIR/requirements.txt"
else
    echo -e "${BLUE}📚 安装依赖...${NC}"
    pip install -q -r "$PROJECT_DIR/requirements.txt"
fi

python env_config.py

# 创建日志目录
mkdir -p "$PROJECT_DIR/logs"

# 安装 Launch Agent
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="$LAUNCH_AGENTS_DIR/$SERVICE_NAME.plist"
mkdir -p "$LAUNCH_AGENTS_DIR"

# 检查是否已经安装
if [ -f "$PLIST_FILE" ]; then
    echo -e "${YELLOW}⚠️  检测到已安装的服务，正在更新...${NC}"
    launchctl unload "$PLIST_FILE" 2>/dev/null || true
fi

# 生成 plist 文件
sed "s|__PROJECT_DIR__|${PROJECT_DIR//\//\\/}|g" "$PROJECT_DIR/com.wintermelon.scribe.plist" > "$PLIST_FILE"

# 启动服务
echo -e "${BLUE}🎯 启动服务...${NC}"
launchctl load "$PLIST_FILE"
launchctl start "$SERVICE_NAME"

# 最终输出
echo ""
echo -e "${GREEN}✨ 安装完成！${NC}"
echo -e "${GREEN}🎙️  冬瓜速记已在后台运行${NC}"
echo ""
echo -e "${BLUE}使用方法：${NC}"
echo -e "  • 快捷键: Ctrl + /"
echo -e "  • 查看状态: ./status.sh"
echo -e "  • 查看日志: tail -f logs/wintermelon_scribe.log"
echo -e "  • 卸载: ./uninstall_launch_agent.sh"
echo ""
echo -e "${GREEN}💻 现在就可以按 Ctrl + / 开始使用了！${NC}"

# 立即退出
exit 0