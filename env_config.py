#!/usr/bin/env python3
"""
WinterMelon Scribe Environment Configuration Tool
使用InquirerPy创建交互式TUI配置工具
"""

from InquirerPy import inquirer, prompt
from pathlib import Path
import os
import sys
from typing import Dict, Any


class EnvConfigurator:
    """环境配置器"""

    def __init__(self, env_file: str = ".env"):
        self.env_file = Path(env_file)
        self.config = {}

    def load_existing_config(self) -> Dict[str, str]:
        """加载现有的.env文件"""
        if self.env_file.exists():
            config = {}
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key] = value
            return config
        return {}

    def siliconflow_config(self) -> None:
        """SiliconFlow API配置"""
        print("\n🎯 === SiliconFlow API Configuration ===")

        # 显示免费API提示
        print("""
🎉 Start Using for FREE Today
✨ Thanks to SiliconFlow's free speech service
💰 FREE transcription - No charges to use WinterMelon Scribe
🎯 Just register at 硅基流动 to get your API key
🚀 No need for expensive voice input software

WinterMelon Scribe is FREE while SiliconFlow offers free service
🎯 Get FREE API Key

https://account.siliconflow.cn/en/login?redirect=https%3A%2F%2Fcloud.siliconflow.cn&invitation=VQcfhhQS
""")

        self.config['SILICONFLOW_API_KEY'] = inquirer.text(
            message="SiliconFlow API Key (FREE - register at the link above):",
            default=self.config.get('SILICONFLOW_API_KEY', 'your-api-key-here'),
            validate=lambda x: len(x) > 0 or "API Key cannot be empty"
        ).execute()

        self.config['SILICONFLOW_API_URL'] = inquirer.text(
            message="SiliconFlow API URL:",
            default=self.config.get('SILICONFLOW_API_URL', 'https://api.siliconflow.cn/v1/audio/transcriptions')
        ).execute()

        self.config['SILICONFLOW_MODEL'] = inquirer.text(
            message="SiliconFlow Model:",
            default=self.config.get('SILICONFLOW_MODEL', 'FunAudioLLM/SenseVoiceSmall')
        ).execute()

    def groq_config(self) -> None:
        """Groq API配置"""
        print("\n🚀 === Groq API Configuration ===")

        self.config['GROQ_API_KEY'] = inquirer.text(
            message="Groq API Key:",
            default=self.config.get('GROQ_API_KEY', 'your-groq-api-key-here'),
            validate=lambda x: len(x) > 0 or "API Key cannot be empty"
        ).execute()

        self.config['GROQ_MODEL'] = inquirer.text(
            message="Groq Model:",
            default=self.config.get('GROQ_MODEL', 'whisper-large-v3-turbo')
        ).execute()

    def transcription_config(self) -> None:
        """转录服务配置"""
        print("\n🎤 === Transcription Provider Selection ===")

        self.config['TRANSCRIPTION_PROVIDER'] = inquirer.select(
            message="Select transcription provider:",
            choices=["siliconflow", "groq"],
            default=self.config.get('TRANSCRIPTION_PROVIDER', 'siliconflow')
        ).execute()

        # 音频配置
        print("\n🔊 === Audio Configuration ===")

        self.config['AUDIO_SAMPLE_RATE'] = inquirer.text(
            message="Audio sample rate:",
            default=self.config.get('AUDIO_SAMPLE_RATE', '16000'),
            validate=lambda x: x.isdigit() or "Must be a number"
        ).execute()

    def llm_config(self) -> None:
        """LLM配置"""
        print("\n🤖 === OpenAI Configuration ===")

        self.config['OPENAI_API_KEY'] = inquirer.text(
            message="OpenAI API Key:",
            default=self.config.get('OPENAI_API_KEY', 'your-openai-api-key-here')
        ).execute()

        self.config['OPENAI_API_BASE'] = inquirer.text(
            message="OpenAI API Base (optional):",
            default=self.config.get('OPENAI_API_BASE', 'https://api.openai.com/v1')
        ).execute()

        self.config['OPENAI_MODEL'] = inquirer.select(
            message="OpenAI Model:",
            choices=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"],
            default=self.config.get('OPENAI_MODEL', 'gpt-3.5-turbo')
        ).execute()

        print("\n⚙️ === LLM Processing Configuration ===")

        self.config['LLM_ENABLED'] = str(inquirer.confirm(
            message="Enable LLM processing?",
            default=self.config.get('LLM_ENABLED', 'false').lower() == 'true'
        ).execute()).lower()

        if self.config['LLM_ENABLED'] == 'true':
            self.config['LLM_TEMPERATURE'] = inquirer.text(
                message="LLM Temperature (0.0-1.0):",
                default=self.config.get('LLM_TEMPERATURE', '0.7'),
                validate=lambda x: self._validate_float(x, 0.0, 1.0) or "Must be between 0.0 and 1.0"
            ).execute()

            self.config['LLM_MAX_TOKENS'] = inquirer.text(
                message="LLM Max Tokens:",
                default=self.config.get('LLM_MAX_TOKENS', '1000'),
                validate=lambda x: x.isdigit() and int(x) > 0 or "Must be a positive number"
            ).execute()

            # 自定义提示词
            use_custom_prompt = inquirer.confirm(
                message="Set custom system prompt?",
                default='LLM_CUSTOM_PROMPT' in self.config
            ).execute()

            if use_custom_prompt:
                self.config['LLM_CUSTOM_PROMPT'] = inquirer.text(
                    message="Custom prompt:",
                    default=self.config.get('LLM_CUSTOM_PROMPT', '请优化以下文本的表达，使其更加清晰和专业：')
                ).execute()
            elif 'LLM_CUSTOM_PROMPT' in self.config:
                del self.config['LLM_CUSTOM_PROMPT']

    def notification_config(self) -> None:
        """通知配置 (macOS only)"""
        print("\n🔔 === Notification Configuration (macOS only) ===")

        self.config['NOTIFICATION_ENABLED'] = str(inquirer.confirm(
            message="Enable system notifications?",
            default=self.config.get('NOTIFICATION_ENABLED', 'true').lower() == 'true'
        ).execute()).lower()

        if self.config['NOTIFICATION_ENABLED'] == 'true':
            self.config['NOTIFICATION_SOUND_ENABLED'] = str(inquirer.confirm(
                message="Enable notification sounds?",
                default=self.config.get('NOTIFICATION_SOUND_ENABLED', 'true').lower() == 'true'
            ).execute()).lower()

    def _validate_float(self, value: str, min_val: float, max_val: float) -> bool:
        """验证浮点数值范围"""
        try:
            float_val = float(value)
            return min_val <= float_val <= max_val
        except ValueError:
            return False

    def save_config(self) -> None:
        """保存配置到.env文件"""
        # 创建备份
        if self.env_file.exists():
            backup_path = self.env_file.with_suffix('.env.backup')
            self.env_file.rename(backup_path)
            print(f"✓ Backup created: {backup_path}")

        # 写入新配置
        env_content = []
        env_content.append("# SiliconFlow API Configuration")
        if 'SILICONFLOW_API_KEY' in self.config:
            env_content.append(f"SILICONFLOW_API_KEY={self.config['SILICONFLOW_API_KEY']}")
        if 'SILICONFLOW_API_URL' in self.config:
            env_content.append(f"SILICONFLOW_API_URL={self.config['SILICONFLOW_API_URL']}")
        if 'SILICONFLOW_MODEL' in self.config:
            env_content.append(f"SILICONFLOW_MODEL={self.config['SILICONFLOW_MODEL']}")
        env_content.append("")

        env_content.append("# Groq API Configuration")
        if 'GROQ_API_KEY' in self.config:
            env_content.append(f"GROQ_API_KEY={self.config['GROQ_API_KEY']}")
        if 'GROQ_MODEL' in self.config:
            env_content.append(f"GROQ_MODEL={self.config['GROQ_MODEL']}")
        env_content.append("")

        env_content.append("# Transcription Provider Selection")
        if 'TRANSCRIPTION_PROVIDER' in self.config:
            env_content.append(f"TRANSCRIPTION_PROVIDER={self.config['TRANSCRIPTION_PROVIDER']}")
        env_content.append("")

        env_content.append("# Audio Configuration")
        if 'AUDIO_SAMPLE_RATE' in self.config:
            env_content.append(f"AUDIO_SAMPLE_RATE={self.config['AUDIO_SAMPLE_RATE']}")
        env_content.append("")

        env_content.append("# LLM Configuration (for post-processing transcriptions)")
        env_content.append("# Choose one of the LLM providers below")
        env_content.append("")

        env_content.append("# OpenAI Configuration")
        if 'OPENAI_API_KEY' in self.config:
            env_content.append(f"OPENAI_API_KEY={self.config['OPENAI_API_KEY']}")
        if 'OPENAI_API_BASE' in self.config:
            env_content.append(f"OPENAI_API_BASE={self.config['OPENAI_API_BASE']}  # Optional, uses default if not set")
        if 'OPENAI_MODEL' in self.config:
            env_content.append(f"OPENAI_MODEL={self.config['OPENAI_MODEL']}  # or gpt-4, gpt-4-turbo, etc.")
        env_content.append("")

        env_content.append("# LLM Processing Configuration")
        if 'LLM_ENABLED' in self.config:
            env_content.append(f"LLM_ENABLED={self.config['LLM_ENABLED']}  # Enable/disable LLM processing (true/false)")
        if self.config.get('LLM_ENABLED') == 'true':
            if 'LLM_TEMPERATURE' in self.config:
                env_content.append(f"LLM_TEMPERATURE={self.config['LLM_TEMPERATURE']}  # 0.0-1.0, lower is more deterministic")
            if 'LLM_MAX_TOKENS' in self.config:
                env_content.append(f"LLM_MAX_TOKENS={self.config['LLM_MAX_TOKENS']}  # Maximum tokens in LLM response")
        env_content.append("")

        env_content.append("# Custom System Prompt (optional)")
        env_content.append("# Set a custom prompt to control how the LLM processes your text")
        if 'LLM_CUSTOM_PROMPT' in self.config:
            env_content.append(f"# LLM_CUSTOM_PROMPT={self.config['LLM_CUSTOM_PROMPT']}")
        else:
            env_content.append("# LLM_CUSTOM_PROMPT=请优化以下文本的表达，使其更加清晰和专业：")
        env_content.append("")

        env_content.append("# Notification Configuration (macOS only)")
        if 'NOTIFICATION_ENABLED' in self.config:
            env_content.append(f"NOTIFICATION_ENABLED={self.config['NOTIFICATION_ENABLED']}  # Enable/disable system notifications (true/false)")
        if self.config.get('NOTIFICATION_ENABLED') == 'true':
            if 'NOTIFICATION_SOUND_ENABLED' in self.config:
                env_content.append(f"NOTIFICATION_SOUND_ENABLED={self.config['NOTIFICATION_SOUND_ENABLED']}  # Enable notification sounds (true/false)")

        self.env_file.parent.mkdir(parents=True, exist_ok=True)
        self.env_file.write_text('\n'.join(env_content))

        print(f"\n✅ Configuration saved to {self.env_file.absolute()}")
        print(f"📝 {len(self.config)} variables configured")

    def run(self) -> None:
        """运行配置向导"""
        print("🚀 WinterMelon Scribe Configuration Tool")
        print("=" * 50)

        # 加载现有配置
        existing_config = self.load_existing_config()
        if existing_config:
            print(f"\n📂 Found existing config with {len(existing_config)} variables")
            use_existing = inquirer.confirm(
                message="Use existing values as defaults?",
                default=True
            ).execute()
            if use_existing:
                self.config = existing_config

        # 使用select逐个配置，而不是checkbox
        section_choice = inquirer.select(
            message="Select section to configure (or choose 'All'):",
            choices=[
                "All: Configure all sections",
                "SiliconFlow API",
                "Groq API",
                "Transcription",
                "LLM",
                "Notifications",
                "Skip: Keep current configuration"
            ],
            default="All: Configure all sections"
        ).execute()

        # 处理选择
        if section_choice == "All: Configure all sections":
            self.siliconflow_config()
            self.groq_config()
            self.transcription_config()
            self.llm_config()
            self.notification_config()
        elif section_choice == "SiliconFlow API":
            self.siliconflow_config()
        elif section_choice == "Groq API":
            self.groq_config()
        elif section_choice == "Transcription":
            self.transcription_config()
        elif section_choice == "LLM":
            self.llm_config()
        elif section_choice == "Notifications":
            self.notification_config()
        elif section_choice == "Skip: Keep current configuration":
            print("\n⚠️ Skipping configuration, keeping current values.")
        else:
            print("\n⚠️ Invalid choice, skipping configuration.")

        # 确认保存
        print("\n📋 Configuration Summary:")
        for key, value in self.config.items():
            display_value = value if 'API_KEY' not in key else "***"
            print(f"  {key} = {display_value}")

        save = inquirer.confirm(
            message="\n💾 Save configuration?",
            default=True
        ).execute()

        if save:
            self.save_config()
            print("\n🎉 Configuration completed successfully!")
        else:
            print("\n❌ Configuration discarded")


def main():
    """主函数"""
    try:
        # 获取env文件路径
        env_file = sys.argv[1] if len(sys.argv) > 1 else ".env"

        configurator = EnvConfigurator(env_file)
        configurator.run()

    except KeyboardInterrupt:
        print("\n\n⏹️ Configuration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()