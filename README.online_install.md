# 冬瓜速记 - 在线安装

## 🚀 一键安装

用户只需运行以下命令即可自动下载并安装最新版本：

```bash
# 使用 curl
curl -fsSL https://raw.githubusercontent.com/ParseDark/wintermelon_scribe/main/online_install.sh | bash

# 或使用 wget
wget -qO- https://raw.githubusercontent.com/ParseDark/wintermelon_scribe/main/online_install.sh | bash
```

## ✨ 特性

- 🔄 **自动获取最新版本** - 脚本会自动下载最新发布的版本
- ⚡ **国内加速下载** - 使用 GHFast 镜像站，下载速度更快
- 🎯 **智能架构识别** - 自动检测 Mac 是 Intel 还是 Apple Silicon
- 🛠️ **自动安装依赖** - 自动创建虚拟环境并安装所需依赖
- 🖥️ **创建桌面快捷** - 自动在桌面创建启动图标
- 🔧 **可选后台服务** - 可选择安装为开机自启动服务

## 📦 安装流程

1. **系统检测** - 确认是 macOS 系统
2. **架构识别** - 检测是 Intel 还是 Apple Silicon
3. **下载文件** - 从镜像站下载对应版本
4. **解压安装** - 解压到 `~/wintermelon_scribe` 目录
5. **安装依赖** - 自动安装 Python 依赖
6. **创建快捷** - 在桌面创建启动脚本
7. **可选服务** - 询问是否安装为后台服务

## 🎯 使用说明

### 启动程序
- 双击桌面上的 `冬瓜速记.command`
- 或在终端运行：`cd ~/wintermelon_scribe && ./start.sh`

### 卸载程序
在终端运行：`cd ~/wintermelon_scribe && ./uninstall.sh`

## 🔄 自动更新机制

这个 `online_install.sh` 文件会在每次发布新版本时自动更新：

1. 当在 GitHub 发布新版本时，GitHub Actions 会自动触发
2. 更新 `online_install.sh` 中的版本号和下载链接
3. 自动提交更改到仓库

确保用户始终能通过这个脚本获取到最新版本。

## ⚠️ 注意事项

- 需要 macOS 系统
- 需要安装 Python 3
- 首次安装需要网络连接
- 安装目录为 `~/wintermelon_scribe`

## 🐛 故障排除

如果下载失败，可以尝试：
1. 检查网络连接
2. 手动访问 GHFast 镜像站：https://ghfast.top
3. 从 GitHub 直接下载源码编译