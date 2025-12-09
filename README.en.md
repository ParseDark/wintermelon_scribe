<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/ParseDark/wintermelon_scribe@main/assets/logo.jpg" alt="WinterMelon Scribe Logo" width="200">
</div>

# WinterMelon Scribe (冬瓜速记)

🇺🇸 English | [🇨🇳 简体中文](README.md)

> An intelligent tool that makes voice input as smooth as silk, specially designed for developers and creators

## 🎯 Product Vision

WinterMelon Scribe aims to become a developer tool plugin like GitHub Copilot, Cursor, and Continue.dev, making coding, documentation, and note-taking more efficient and natural through voice technology. Our goal is: **Free your hands, let your thoughts keep up with your speech**.

## ✨ Core Features

- **🎤 Voice-to-Text**: High-accuracy speech recognition supporting technical terms and code keywords
- **⌨️ Smart Paste**: Automatically paste to cursor position without manual operation
- **🚀 Minimal Interaction**: One-click activation, instant response
- **🔒 Privacy Protection**: Local-first, automatic cleanup of sensitive data

## 🎮 Shortcuts

- **Cmd + ;**: Start recording, automatically transcribe and paste after release

## Installation

```bash
# Using uv (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

## 🚀 Quick Start

```bash
# Activate virtual environment and run
source .venv/bin/activate
python main.py
```

## 📝 Use Cases

### 💻 Programming & Development
- Ask AI programming assistants: "Why is this React component throwing an error? Please analyze it"
- Request code improvement suggestions: "How can I optimize this algorithm's time complexity?"
- Request code examples: "Give me a Python example for asynchronously downloading files"
- Debug logging: "Line 45 in userservice.py, user data is not being saved to the database correctly after update"

### 📚 Documentation Writing
- Quick meeting notes: "Three new features were confirmed in today's product meeting"
- Technical documentation: "API response format needs to include status and pagination info"
- Code comments: "This function filters invalid user input"
- README writing: "Installation steps require configuring environment variables first"

### 💡 Learning & Research
- Learning notes: "Today I learned about the principles of React Hooks"
- Technical points summary: "Docker container networking has three modes: bridge, host, none"
- Issue tracking: "Need to investigate why this API endpoint's response time suddenly increased"

## 🔧 macOS Permission Settings

### Required Permissions

1. **System Preferences** → **Security & Privacy** → **Privacy**
2. Select **Accessibility**
3. Add Terminal app (Terminal.app, iTerm2, etc.)
4. Select **Screen Recording**
5. Add Terminal app again

> ⚠️ Restart terminal after setting permissions

## 🔌 IDE Integration

WinterMelon Scribe seamlessly integrates with:

- **VS Code**: Code writing, comment generation
- **Cursor**: Voice input during AI-assisted programming
- **Continue.dev**: Enhanced development experience
- **JetBrains IDEs**: Java, Python development
- **Vim/Neovim**: Voice enhancement for terminal editors
- **Obsidian/Notion**: Note-taking systems
- **iA Writer/Ulysses**: Professional writing

## 🎯 Future Plans

- [ ] **Plugin Architecture**: Native plugins for VS Code, JetBrains, etc.
- [ ] **Command Palette**: Voice-triggered code snippets and commands
- [ ] **Multi-language Support**: Optimized mixed Chinese-English recognition
- [ ] **Code Mode**: Automatic recognition and formatting of code blocks
- [ ] **Team Collaboration**: Shared voice templates and quick phrases
- [ ] **Cloud Sync**: Cross-device sync of settings and preferences

## 🔒 API Configuration

Using SiliconFlow API for speech transcription:

1. Copy `.env.example` to `.env`
2. Set your API key in `.env`:
```env
SILICONFLOW_API_KEY=your-api-key-here
```

## ⚡ Performance Metrics

- **Response Time**: < 100ms key response
- **Transcription Latency**: Real-time Factor (RTF) < 0.3x
- **Accuracy**: > 95% in technical scenarios
- **Memory Usage**: < 50MB runtime memory

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