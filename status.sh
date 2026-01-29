#!/bin/bash

# 冬瓜速记状态检查脚本

SERVICE_NAME="com.wintermelon.scribe"
PROJECT_DIR="$(dirname "$0")"
PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e "${BLUE}冬瓜速记运行状态"
echo -e "${BLUE}========================================${NC}"

# 检查服务状态
echo -e "${BLUE}服务状态：${NC}"
if launchctl list | grep -q "$SERVICE_NAME"; then
    # 获取进程信息
    PID=$(launchctl list | grep "$SERVICE_NAME" | awk '{print $1}')
    if [ "$PID" != "-" ]; then
        # 检查进程名称
        if ps -p $PID -o command= 2>/dev/null | grep -q "wintermelon_scribe" || ps -p $PID -o comm= 2>/dev/null | grep -q "wintermelon"; then
            echo -e "  ${GREEN}✅ 运行中 (PID: $PID, 进程: WinterMelon Scribe)${NC}"
        else
            echo -e "  ${GREEN}✅ 运行中 (PID: $PID)${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  已加载但未运行${NC}"
    fi
else
    echo -e "  ${RED}❌ 未安装或已卸载${NC}"
fi

echo ""

# 检查日志文件
echo -e "${BLUE}日志文件：${NC}"
if [ -f "$PROJECT_DIR/logs/wintermelon_scribe.log" ]; then
    LOG_SIZE=$(du -h "$PROJECT_DIR/logs/wintermelon_scribe.log" | cut -f1)
    LAST_LINE=$(tail -n 1 "$PROJECT_DIR/logs/wintermelon_scribe.log")
    echo -e "  📄 wintermelon_scribe.log ($LOG_SIZE)"
    echo -e "     最新: $LAST_LINE"
else
    echo -e "  ${RED}❌ 无日志文件${NC}"
fi

if [ -f "$PROJECT_DIR/logs/wintermelon_scribe.err" ]; then
    ERR_SIZE=$(du -h "$PROJECT_DIR/logs/wintermelon_scribe.err" | cut -f1)
    ERR_COUNT=$(wc -l < "$PROJECT_DIR/logs/wintermelon_scribe.err" 2>/dev/null || echo "0")
    if [ "$ERR_COUNT" -gt 0 ]; then
        LAST_ERR=$(tail -n 1 "$PROJECT_DIR/logs/wintermelon_scribe.err")
        echo -e "  ⚠️  wintermelon_scribe.err ($ERR_SIZE, $ERR_COUNT 行)"
        echo -e "     最新: $LAST_ERR"
    else
        echo -e "  ${GREEN}✓ wintermelon_scribe.err (空)${NC}"
    fi
else
    echo -e "  ${GREEN}✓ 无错误文件${NC}"
fi

echo ""

# 快捷命令
echo -e "${BLUE}快捷命令：${NC}"
echo -e "  • 查看日志: tail -f logs/wintermelon_scribe.log"
echo -e "  • 查看错误: tail -f logs/wintermelon_scribe.err"
echo -e "  • 重启服务: launchctl stop com.wintermelon.scribe && launchctl start com.wintermelon.scribe"
echo -e "  • 重新安装: ./install.sh"

echo ""
echo -e "${BLUE}========================================${NC}"