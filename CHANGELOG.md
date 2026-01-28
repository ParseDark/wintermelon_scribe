# 更新日志

## v3.0.0 (2026-01-28)

### 🆕 新增功能
- **LLM 文本处理增强**: 支持在语音转文本后调用 LLM 进行智能处理
- **多 LLM 提供商支持**: 兼容 OpenAI、SiliconFlow、DeepSeek 等主流 API
- **多种处理模式**: 提供总结、纠错、改进、翻译、会议纪要等 10 种预设模式
- **快捷键增强**:
  - `Ctrl + /`: 原有的直接转录模式
  - `Ctrl + Shift + /`: 新增 LLM 增强处理模式

### 📦 新增依赖
- `openai>=1.0.0`: Python OpenAI SDK，用于调用各种兼容 OpenAI API 的 LLM 服务

### 🔧 新增配置项
- `OPENAI_API_KEY`: OpenAI API 密钥
- `LLM_TEMPERATURE`: LLM 温度参数（默认: 0.7）
- `LLM_MAX_TOKENS`: LLM 最大输出令牌数（默认: 1000）

### 📁 新增文件
- `llm_processor.py`: LLM 文本处理核心模块

### ⚡ 改进
- 性能统计显示 LLM 处理时间
- 启动时显示当前 LLM 配置状态
- 优化了错误处理和用户提示

## v2.0.0

### 🎯 主要功能
- 语音转文字核心功能
- 支持 SiliconFlow 和 Groq 转录服务
- 自动粘贴到光标位置
- macOS 权限集成

### ⌨️ 快捷键
- `Ctrl + /`: 开始录音，松开后自动转录并粘贴