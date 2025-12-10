<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/ParseDark/wintermelon_scribe@main/assets/logo.jpg" alt="冬瓜速记 Logo" width="200">
</div>

# 冬瓜速记 (WinterMelon Scribe)

[🇺🇸 English](README.en.md) | 🇨🇳 简体中文

> 一个让语音输入变得如丝般顺滑的智能工具，专为开发者和创作者打造

## 🎯 产品定位

冬瓜速记致力于成为像 GitHub Copilot、Cursor、Continue.dev 这样的开发者工具插件，通过语音技术让编码、写文档、记笔记变得更加高效自然。我们的目标是：**让双手解放，让思维跟上语速**。

## ✨ 核心功能

- **🎤 语音转文字**：高精度语音识别，支持技术术语和代码关键词
- **⌨️ 智能粘贴**：自动粘贴到光标位置，无需手动操作
- **🚀 极简交互**：一键启动，瞬间响应
- **🔒 隐私保护**：本地优先，自动清理敏感数据

## 🎮 快捷键

- **Cmd + ;**：开始录音，松开后自动转录并粘贴

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

## 📝 使用场景

### 💻 编程开发
- 向 AI 编程助手提问："这个 React 组件为什么报错？帮我分析一下"
- 询问代码改进建议："如何优化这个算法的时间复杂度？"
- 请求代码示例："给我写一个 Python 异步下载文件的例子"
- 调试时记录："在 userservice.py 第 45 行，用户数据更新后没有正确保存到数据库"

### 📚 文档编写
- 快速记录会议要点："今天产品会上确定了三个新功能点"
- 编写技术文档："API 返回格式需要包含 status 分页信息"
- 整理代码注释："这个函数的作用是过滤无效的用户输入"
- 撰写 README："安装步骤需要先配置环境变量"

### 💡 学习研究
- 记录学习心得："今天了解了 React Hooks 的原理"
- 整理技术要点："Docker 容器网络的三种模式：bridge host none"
- 收集问题清单："需要研究为什么这个接口响应时间突然变慢"

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

## 🎯 未来规划

- [ ] **插件化架构**：支持 VS Code、JetBrains 等原生插件
- [ ] **命令面板**：语音触发代码片段和命令
- [ ] **多语言支持**：中英文混合识别优化
- [ ] **代码模式**：自动识别并格式化代码块
- [ ] **团队协作**：共享语音模板和快捷短语
- [ ] **云同步**：跨设备同步设置和偏好

## 🔒 API 配置
支持多个语音转录提供商，请根据需要选择配置：

### 支持的提供商
- **SiliconFlow**（默认）：支持中文优化的 SenseVoice 模型
- **Groq**：使用 Whisper Large V3 Turbo 模型

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

## ⚡ 性能指标

- **响应时间**：< 100ms 按键响应
- **转录延迟**：实时率 (RTF) < 0.3x
- **准确率**：技术场景 > 95%
- **内存占用**：< 50MB 运行内存

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