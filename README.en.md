<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/ParseDark/wintermelon_scribe@main/assets/logo.jpg" alt="WinterMelon Scribe Logo" width="200">
</div>

# WinterMelon Scribe (冬瓜速记)

🇺🇸 English | [🇨🇳 简体中文](README.md)

> An intelligent tool that makes voice input as smooth as silk, specially designed for developers and creators

## 🎯 Product Positioning

WinterMelon Scribe is a system-level voice input tool dedicated to creating a faster and more convenient input experience. Through deep integration with various development tools and applications, it makes voice input a natural part of daily work. Our goal is: **Make voice a system-level input method, making input more efficient**.

## Installing Dependencies

```bash
# Using uv (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

## 🚀 Quick Start

### Method 1: Direct Run (Recommended for Testing)

```bash
# Activate virtual environment and run
source .venv/bin/activate
python main.py
```

### Method 2: Background Service (Recommended for Daily Use) ⭐

Run WinterMelon Scribe as a background service with auto-start at boot:

```bash
# One-click install as background service
./install.sh
```

After installation, it will:
- 🔋 Auto-start at boot
- 🤫 Run silently in background
- 🚫 No terminal window needed
- ⌨️ Hotkeys and notifications work normally
- 🎙️ Process name shows as "WinterMelon Scribe"

Check status: `./status.sh`
Uninstall service: `./uninstall.sh`

For detailed instructions: [LAUNCH_AGENT.md](LAUNCH_AGENT.md)

## 🔧 macOS Permission Settings

### Required Permissions

1. **System Preferences** → **Security & Privacy** → **Privacy**
2. Select **Accessibility**
3. Add Terminal app (Terminal.app, iTerm2, etc.)
4. Select **Screen Recording**
5. Add Terminal app again

> ⚠️ Restart terminal after setting permissions

## 🔌 Integration with Development Tools

WinterMelon Scribe seamlessly works with:

- **VS Code**: Code writing, comment generation
- **Cursor**: Voice input during AI-assisted programming
- **Continue.dev**: Enhanced development experience
- **JetBrains IDEs**: Java, Python development
- **Vim/Neovim**: Voice enhancement for terminal editors
- **Obsidian/Notion**: Note-taking systems
- **iA Writer/Ulysses**: Professional writing

## 🧠 LLM Enhanced Features

v3.0 introduces LLM text processing capabilities, supporting intelligent processing after voice-to-text conversion.

### Shortcuts
- **Ctrl + /**: Start recording, automatically process and paste based on configuration

### Supported LLM Providers
- OpenAI (GPT-3.5, GPT-4, GPT-4-turbo, etc.)

### Custom System Prompts

Set custom prompts by modifying the .env file:

```env
# Set custom prompts to control how LLM processes text
LLM_CUSTOM_PROMPT=Please optimize the expression of the following text to make it clearer and more professional:

# If not set, default processing will be used
```

### LLM Configuration
```env
# Enable/disable LLM processing
LLM_ENABLED=true

# OpenAI configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Processing parameters
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
```

### Control Methods
- Set `LLM_ENABLED=false` to completely disable LLM, only perform voice-to-text
- Customize processing through `LLM_CUSTOM_PROMPT`
- All controls are through environment variables, simple and clear

## 🔒 API Configuration
Supports multiple speech transcription providers, please choose and configure according to your needs:

### Supported Providers
- **SiliconFlow** (default): Supports Chinese-optimized SenseVoice model, recommended for local recording scenarios
- **Groq**: Uses Whisper Large V3 Turbo model for fast responses

### SiliconFlow Configuration (Default)
1. Copy environment variable example file:
```bash
cp .env.example .env
```
2. Edit `.env` file and set your API key:
```env
SILICONFLOW_API_KEY=your-api-key-here
# Optional: specify model
SILICONFLOW_MODEL=FunAudioLLM/SenseVoiceSmall
```

### Groq Configuration
1. Edit `.env` file and set Groq API key:
```env
GROQ_API_KEY=your-groq-api-key-here
# Optional: specify model (default is whisper-large-v3-turbo)
GROQ_MODEL=whisper-large-v3-turbo
# Set transcription provider to Groq
TRANSCRIPTION_PROVIDER=groq
```

### Environment Variable Configuration

#### SiliconFlow Environment Variables
```bash
export SILICONFLOW_API_KEY="your-api-key-here"
```

#### Groq Environment Variables
```bash
export GROQ_API_KEY="your-groq-api-key-here"
export TRANSCRIPTION_PROVIDER=groq
```

### Direct Code Modification

Modify configuration variables directly in `main.py`.

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| No key response | Check Accessibility permissions |
| Paste failed | Check Screen Recording permissions |
| Empty transcription | Check microphone permissions and API key |
| First paste failed | Restart program or check system permissions |

## 🤝 Contributing

WinterMelon Scribe is rapidly developing. Contributions, suggestions, and issue reports are welcome!

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

**Let voice become your third hand** 🎙️