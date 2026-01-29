<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/ParseDark/wintermelon_scribe@main/assets/logo.jpg" alt="冬瓜速记 Logo" width="200">
</div>

# 冬瓜速记 (WinterMelon Scribe)

[🇺🇸 English](README.en.md) | 🇨🇳 简体中文

> 一个让语音输入变得如丝般顺滑的智能工具，专为开发者和创作者打造

## 🎯 产品定位

冬瓜速记是一个系统级的语音输入工具，致力于打造更快捷、更方便的输入体验。通过与各种开发工具和应用的深度集成，让语音输入成为日常工作中自然的一部分。我们的目标是：**让语音成为系统级的输入方式，让输入更高效**。

## 安装依赖

```bash
# 使用 uv (推荐)
uv pip install -r requirements.txt

# 或使用 pip
pip install -r requirements.txt
```

## 🚀 快速开始

```bash
# 激活虚拟环境并运行
source .venv/bin/activate
python main.py
```

## 🔧 macOS 权限设置

### 必需权限

1. **系统偏好设置** → **安全性与隐私** → **隐私**
2. 选择 **辅助功能**
3. 添加终端应用（Terminal.app、iTerm2 等）
4. 选择 **屏幕录制**
5. 再次添加终端应用

> ⚠️ 权限设置完成后需重启终端

## 🔌 集成开发工具

冬瓜速记可以与以下工具无缝配合：

- **VS Code**：代码编写、注释生成
- **Cursor**：AI 辅助编程时的语音输入
- **Continue.dev**：增强开发体验
- **JetBrains IDEs**：Java、Python 等开发
- **Vim/Neovim**：终端编辑器的语音增强
- **Obsidian/Notion**：笔记系统
- **iA Writer/Ulysses**：专业写作

## 🧠 LLM 增强功能

v3.0 新增 LLM 文本处理功能，支持在语音转文本后进行智能处理。

### 快捷键
- **Ctrl + /**：开始录音，自动根据配置处理并粘贴

### 支持的 LLM 提供商
- OpenAI (GPT-3.5, GPT-4, GPT-4-turbo 等)

### 处理模式
- `improve`：改进文本表达（默认）
- `summarize`：总结要点
- `correct`：纠正语法错误
- `format_code`：格式化代码
- `translate_en`：翻译为英文
- `translate_zh`：翻译为中文
- `meeting_notes`：整理会议纪要
- `todo_list`：转换为任务清单
- `email_draft`：草拟邮件

### 自定义系统提示

通过修改 .env 文件设置自定义提示：

```env
# 设置自定义提示，控制 LLM 如何处理文本
LLM_CUSTOM_PROMPT=请优化以下文本的表达，使其更加清晰和专业：

# 如果不设置，使用默认处理
```

### LLM 配置
```env
# 启用/禁用 LLM 处理
LLM_ENABLED=true

# OpenAI 配置
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# 处理参数
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
```

### 控制方式
- 设置 `LLM_ENABLED=false` 可完全禁用 LLM，仅做语音转文本
- 通过 `LLM_CUSTOM_PROMPT` 自定义处理方式
- 所有控制都通过环境变量，简单明了

## 🔒 API 配置
支持多个语音转录提供商，请根据需要选择配置：

### 支持的提供商
- **SiliconFlow**（默认）：支持中文优化的 SenseVoice 模型，推荐用于本地录音场景
- **Groq**：使用 Whisper Large V3 Turbo 模型，快速响应

### SiliconFlow 配置（默认）
1. 复制环境变量示例文件：
```bash
cp .env.example .env
```
2. 编辑 `.env` 文件，设置你的 API 密钥：
```env
SILICONFLOW_API_KEY=your-api-key-here
# 可选：指定模型
SILICONFLOW_MODEL=FunAudioLLM/SenseVoiceSmall
```

### Groq 配置
1. 编辑 `.env` 文件，设置 Groq API 密钥：
```env
GROQ_API_KEY=your-groq-api-key-here
# 可选：指定模型（默认为 whisper-large-v3-turbo）
GROQ_MODEL=whisper-large-v3-turbo
# 设置转录提供商为 Groq
TRANSCRIPTION_PROVIDER=groq
```


### 环境变量配置方式

#### SiliconFlow 环境变量
```bash
export SILICONFLOW_API_KEY="your-api-key-here"
```

#### Groq 环境变量
```bash
export GROQ_API_KEY="your-groq-api-key-here"
export TRANSCRIPTION_PROVIDER=groq
```

### 直接修改代码

在 `main.py` 中直接修改配置变量。

## 🛠️ 故障排除

| 问题 | 解决方案 |
|------|----------|
| 按键无响应 | 检查辅助功能权限 |
| 粘贴失败 | 检查屏幕录制权限 |
| 转录为空 | 检查麦克风权限和 API 密钥 |
| 首次粘贴失败 | 重启程序或检查系统权限 |

## 🤝 贡献

冬瓜速记正在快速发展中，欢迎贡献代码、提出建议或报告问题！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**让语音成为你的第三只手** 🎙️