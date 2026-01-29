#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WinterMelon Scribe - 主入口文件
用于 Launch Agent 后台运行，提供更好的进程标识
"""

import sys
import os

# 设置进程名称
try:
    import setproctitle
    setproctitle.setproctitle("WinterMelon Scribe")
except ImportError:
    # 如果没有安装 setproctitle，尝试使用系统调用
    try:
        import ctypes
        import ctypes.util
        libc = ctypes.CDLL(ctypes.util.find_library('c'))
        libc.prctl(15, b'WinterMelon Scribe', 0, 0, 0)
    except:
        pass

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# 导入并运行主程序
if __name__ == "__main__":
    # 运行主程序
    from main import main
    main()