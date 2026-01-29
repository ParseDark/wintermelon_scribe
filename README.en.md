<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/ParseDark/wintermelon_scribe@main/assets/logo.jpg" alt="WinterMelon Scribe Logo" width="200">
</div>

# WinterMelon Scribe (冬瓜速记)

🇺🇸 English | [🇨🇳 简体中文](README.md)

> An intelligent tool that makes voice input as smooth as silk, specially designed for developers and creators

## 🎯 Product Positioning

WinterMelon Scribe is a system-level voice input tool dedicated to creating a faster and more convenient input experience. Through deep integration with various development tools and applications, it makes voice input a natural part of daily work. Our goal is: **Make voice a system-level input method, making input more efficient**.

---

## 📦 User Installation (One-Click Install)

> Suitable for regular users, the program will run automatically in the background after installation

### Quick Install ⭐

```bash
# 1. Clone or download the project
git clone https://github.com/ParseDark/wintermelon_scribe.git
cd wintermelon_scribe

# 2. One-click install (automatically configures everything)
./install.sh
```

### After Installation

- 🔋 **Auto-start at boot**
- 🤫 **Runs silently in background**
- 🚫 **No terminal window needed**
- ⌨️ **Hotkey Ctrl + / ready to use**
- 🎙️ **Process name shows as "WinterMelon Scribe"**

### Common Operations

```bash
# Check running status
./status.sh

# Uninstall the program
./uninstall.sh
```

### First Time Use

1. **After installation**, authorize system permissions when prompted
2. **Configure API keys**: Edit `.env` file and set your API keys
3. **Start using**: Press `Ctrl + /` to start recording

---

## 👨‍💻 Developer Installation

> Suitable for developers, convenient for debugging and secondary development

### Environment Setup

```bash
# Check Python version (requires 3.8+)
python3 --version

# Recommended to use uv (faster package manager)
pip install uv
```

### Install Dependencies

```bash
# Method 1: Using uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Method 2: Using pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Direct Run

```bash
# Activate virtual environment
source .venv/bin/activate

# Run directly
python main.py
```

### Background Mode

```bash
# Install as background service
./install.sh

# View logs
tail -f logs/wintermelon_scribe.log
```

---

## 🔧 macOS Permission Settings

The following permissions need to be granted on first run:

### Required Permissions

1. **System Preferences** → **Security & Privacy** → **Privacy**
2. Select **Accessibility** → Add Terminal or Python application
3. Select **Screen Recording** → Add Terminal or Python application

> ⚠️ Restart the program after setting permissions

---

## 🎮 Usage

### Hotkeys

- **Ctrl + /**: Start recording, automatically process and paste when released

### Supported Applications

- **VS Code**: Code writing, comment generation
- **Cursor**: Voice input during AI-assisted programming
- **JetBrains IDEs**: Java, Python development
- **Vim/Neovim**: Voice enhancement for terminal editors
- **Obsidian/Notion**: Note-taking systems
- **iA Writer/Ulysses**: Professional writing
- Any application that supports text input

---

## 🧠 LLM Enhanced Features

v3.0 introduces LLM text processing capabilities, supporting intelligent processing after voice-to-text conversion.

### Supported LLM Providers

- OpenAI (GPT-3.5, GPT-4, GPT-4-turbo, etc.)

### Processing Modes

- `improve`: Improve text expression (default)
- `summarize`: Summarize key points
- `correct`: Correct grammatical errors
- `format_code`: Format code
- `translate_en`: Translate to English
- `translate_zh`: Translate to Chinese
- `meeting_notes`: Organize meeting minutes
- `todo_list`: Convert to task list
- `email_draft`: Draft emails

### Configuration Example

```env
# .env file
# Transcription service configuration (choose one)
SILICONFLOW_API_KEY=your-api-key-here
# or
GROQ_API_KEY=your-groq-api-key-here
TRANSCRIPTION_PROVIDER=groq

# LLM configuration (optional)
LLM_ENABLED=true
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Notification configuration
NOTIFICATION_ENABLED=true
NOTIFICATION_SOUND_ENABLED=true

# Custom prompt (optional)
LLM_CUSTOM_PROMPT=Please optimize the expression of the following text:
```

---

## 🔒 API Service Configuration

### SiliconFlow (Recommended)

1. Register and get API Key: https://siliconflow.cn
2. Configure in `.env` file:
   ```env
   SILICONFLOW_API_KEY=your-api-key-here
   ```

### Groq

1. Register and get API Key: https://groq.com
2. Configure in `.env` file:
   ```env
   GROQ_API_KEY=your-groq-api-key-here
   TRANSCRIPTION_PROVIDER=groq
   ```

### OpenAI (for LLM Processing)

1. Register and get API Key: https://platform.openai.com
2. Configure in `.env` file:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   LLM_ENABLED=true
   ```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| No key response | Check Accessibility permissions |
| Paste failed | Check Screen Recording permissions |
| Empty transcription | Check microphone permissions and API keys |
| Service not running | Run `./status.sh` to check status |

### Common Questions

**Q: How to view logs?**
```bash
# View runtime logs
tail -f logs/wintermelon_scribe.log

# View error logs
tail -f logs/wintermelon_scribe.err
```

**Q: How to restart service?**
```bash
# Stop
launchctl stop com.wintermelon.scribe

# Start
launchctl start com.wintermelon.scribe
```

**Q: How to update configuration?**
After modifying `.env` file, restart the service:
```bash
./uninstall.sh && ./install.sh
```

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

**Let voice become your third hand** 🎙️