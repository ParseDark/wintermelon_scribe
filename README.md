<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/ParseDark/wintermelon_scribe@main/assets/logo.jpg" alt="冬瓜速记 Logo" width="200">
</div>

# 冬瓜速记 (WinterMelon Scribe)

[🇺🇸 English](README.en.md) | 🇨🇳 简体中文

> 一个让语音输入变得如丝般顺滑的智能工具，专为开发者和创作者打造

## 🎯 产品定位

冬瓜速记是一个系统级的语音输入工具，致力于打造更快捷、更方便的输入体验。通过与各种开发工具和应用的深度集成，让语音输入成为日常工作中自然的一部分。我们的目标是：**让语音成为系统级的输入方式，让输入更高效**。

---

## 📦 用户安装（一键安装）

> 适合普通用户，安装后程序将在后台自动运行

### 快速安装 ⭐

```bash
# 1. 克隆或下载项目
git clone https://github.com/ParseDark/wintermelon_scribe.git
cd wintermelon_scribe

cp .env.example .env

# 2. 一键安装（自动配置所有环境）
./install.sh
```

### 安装后效果

- 🔋 **开机自动启动**
- 🤫 **后台静默运行**
- 🚫 **无需打开终端**
- ⌨️ **快捷键 Ctrl + / 立即可用**
- 🎙️ **进程名称显示为 "WinterMelon Scribe"**

### 常用操作

```bash
# 查看运行状态
./status.sh

# 卸载程序
./uninstall.sh
```

### 首次使用

1. **安装**后需要授权系统权限（弹窗提示时点击允许）
2. **配置 API 密钥**：编辑 `.env` 文件，设置你的 API 密钥
3. **开始使用**：按 `Ctrl + /` 开始录音

---

## 👨‍💻 开发者安装

> 适合开发者，便于调试和二次开发

### 环境准备

```bash
# 检查 Python 版本（需要 3.8+）
python3 --version

# 推荐使用 uv（更快的包管理器）
pip install uv
```

### 安装依赖

```bash
# 方式一：使用 uv（推荐）
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 直接运行（调试模式）

```bash
# 激活虚拟环境
source .venv/bin/activate

# 直接运行
python main.py
```

### 后台运行模式

```bash
# 安装为后台服务
./install.sh

# 查看日志
tail -f logs/wintermelon_scribe.log
```

---

## 🔧 macOS 权限设置

首次运行时需要授予以下权限：

### 必需权限

1. **系统偏好设置** → **安全性与隐私** → **隐私**
2. 选择 **辅助功能** → 添加终端或 Python 应用
3. 选择 **屏幕录制** → 添加终端或 Python 应用

> ⚠️ 权限设置完成后需重启程序

---

## 🎮 使用方法

### 快捷键

- **Ctrl + /**：开始录音，松开自动处理并粘贴

### 支持的应用

- **VS Code**：代码编写、注释生成
- **Cursor**：AI 辅助编程时的语音输入
- **JetBrains IDEs**：Java、Python 等开发
- **Vim/Neovim**：终端编辑器的语音增强
- **Obsidian/Notion**：笔记系统
- **iA Writer/Ulysses**：专业写作
- 任何支持文本输入的应用

---

## 🔧 环境配置工具

WinterMelon Scribe 提供了一个交互式的环境配置工具 `env_config.py`，帮助你轻松配置所有必需的 API 密钥和设置。

### 使用配置工具

```bash
# 运行交互式配置工具
python3 env_config.py

# 或指定特定的 .env 文件路径
python3 env_config.py /path/to/.env
```

### 配置选项

配置工具支持以下配置模块：

1. **SiliconFlow API** - 免费的语音转转录服务
   - API Key（必需）
   - API URL
   - 模型选择（默认：FunAudioLLM/SenseVoiceSmall）

2. **Groq API** - 备选的转录服务
   - API Key
   - 模型选择（默认：whisper-large-v3-turbo）

3. **Transcription Provider** - 选择转录服务商
   - siliconflow（推荐，免费）
   - groq

4. **Audio Configuration** - 音频设置
   - 采样率（默认：16000）

5. **LLM Configuration** - 文本后处理
   - OpenAI API Key
   - API Base URL（可选）
   - 模型选择（gpt-3.5-turbo, gpt-4, gpt-4-turbo, gpt-4o）
   - LLM 处理开关
   - Temperature（0.0-1.0）
   - 最大 Token 数
   - 自定义系统提示（可选）

6. **Notification Configuration** - macOS 系统通知
   - 启用/禁用通知
   - 启用/禁用提示音

### SiliconFlow 免费获取 API Key

🎉 **免费使用语音转录服务**

感谢 SiliconFlow 提供的免费语音服务，让 WinterMelon Scribe 完全免费使用：

- ✨ **免费转录** - 无需承担任何费用
- 💰 **零成本使用** - 注册即可获得 API Key
- 🎯 **无需昂贵的语音输入软件**
- 🚀 **高精度识别**

注册地址：https://account.siliconflow.cn/en/login?redirect=https%3A%2F%2Fcloud.siliconflow.cn&invitation=VQcfhhQS

### 配置文件示例

运行配置工具后，会生成类似以下的 `.env` 文件：

```env
# SiliconFlow API Configuration
SILICONFLOW_API_KEY=your-api-key-here
SILICONFLOW_API_URL=https://api.siliconflow.cn/v1/audio/transcriptions
SILICONFLOW_MODEL=FunAudioLLM/SenseVoiceSmall

# Groq API Configuration
# GROQ_API_KEY=your-groq-api-key-here
# GROQ_MODEL=whisper-large-v3-turbo

# Transcription Provider Selection
TRANSCRIPTION_PROVIDER=siliconflow

# Audio Configuration
AUDIO_SAMPLE_RATE=16000

# LLM Configuration (for post-processing transcriptions)
# Choose one of the LLM providers below
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1  # Optional, uses default if not set
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4, gpt-4-turbo, etc.

# LLM Processing Configuration
LLM_ENABLED=true  # Enable/disable LLM processing (true/false)
LLM_TEMPERATURE=0.7  # 0.0-1.0, lower is more deterministic
LLM_MAX_TOKENS=1000  # Maximum tokens in LLM response

# Custom System Prompt (optional)
# Set a custom prompt to control how the LLM processes your text
# LLM_CUSTOM_PROMPT=请优化以下文本的表达，使其更加清晰和专业：

# Notification Configuration (macOS only)
NOTIFICATION_ENABLED=true  # Enable/disable system notifications (true/false)
NOTIFICATION_SOUND_ENABLED=true  # Enable notification sounds (true/false)
```

### 配置示例

```env
# .env 文件
# 转录服务配置（二选一）
SILICONFLOW_API_KEY=your-api-key-here
# 或
GROQ_API_KEY=your-groq-api-key-here
TRANSCRIPTION_PROVIDER=groq

# LLM 配置（可选）
LLM_ENABLED=true
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# 通知配置
NOTIFICATION_ENABLED=true
NOTIFICATION_SOUND_ENABLED=true

# 自定义提示（可选）
LLM_CUSTOM_PROMPT=请优化以下文本的表达：
```

---

## 🔒 API 服务配置

### SiliconFlow（推荐）

1. 注册并获取 API Key：https://siliconflow.cn
2. 在 `.env` 文件中配置：
   ```env
   SILICONFLOW_API_KEY=your-api-key-here
   ```

### Groq

1. 注册并获取 API Key：https://groq.com
2. 在 `.env` 文件中配置：
   ```env
   GROQ_API_KEY=your-groq-api-key-here
   TRANSCRIPTION_PROVIDER=groq
   ```

### OpenAI（用于 LLM 处理）

1. 注册并获取 API Key：https://platform.openai.com
2. 在 `.env` 文件中配置：
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   LLM_ENABLED=true
   ```

---

## 🛠️ 故障排除

| 问题 | 解决方案 |
|------|----------|
| 按键无响应 | 检查辅助功能权限 |
| 粘贴失败 | 检查屏幕录制权限 |
| 转录为空 | 检查麦克风权限和 API 密钥 |
| 服务未运行 | 运行 `./status.sh` 查看状态 |

### 常见问题

**Q: 如何查看日志？**
```bash
# 查看运行日志
tail -f logs/wintermelon_scribe.log

# 查看错误日志
tail -f logs/wintermelon_scribe.err
```

**Q: 如何重启服务？**
```bash
# 停止
launchctl stop com.wintermelon.scribe

# 启动
launchctl start com.wintermelon.scribe
```

**Q: 如何更新配置？**
修改 `.env` 文件后，需要重启服务：
```bash
./ uninstall.sh && ./install.sh
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**让语音成为你的第三只手** 🎙️