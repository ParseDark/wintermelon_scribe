"""
LLM 文本处理模块
支持多种 LLM 提供商对转录后的文本进行处理
"""

from abc import ABC, abstractmethod
import os
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class LLMConfig:
    """LLM 配置类"""
    provider: str
    model: str
    api_key: Optional[str] = None
    api_url: Optional[str] = None
    max_tokens: int = 1000
    temperature: float = 0.7
    system_prompt: Optional[str] = None


class LLMProvider(ABC):
    """LLM 提供商抽象基类"""

    @abstractmethod
    def process_text(self, text: str, config: LLMConfig) -> tuple[str, float]:
        """
        处理文本

        Args:
            text: 输入文本
            config: LLM 配置

        Returns:
            tuple: (处理后的文本, 处理耗时)
        """
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """检查提供商是否已配置"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI GPT 提供商"""

    def __init__(self):
        self.client = None
        self._init_client()

    def _init_client(self):
        """初始化 OpenAI 客户端"""
        try:
            import openai
            self.client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
            )
        except ImportError:
            print("❌ 未安装 openai 库，请运行: pip install openai")
            self.client = None

    def process_text(self, text: str, config: LLMConfig) -> tuple[str, float]:
        """使用 OpenAI API 处理文本"""
        if not self.is_configured():
            raise ValueError("OpenAI API 未配置，请设置 OPENAI_API_KEY")

        if not self.client:
            raise RuntimeError("OpenAI 客户端未初始化")

        # 构建消息
        messages = []
        if config.system_prompt:
            messages.append({"role": "system", "content": config.system_prompt})
        messages.append({"role": "user", "content": text})

        print("🤖 LLM 处理中...")
        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=config.model,
                messages=messages,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
            )

            process_time = time.time() - start_time
            result = response.choices[0].message.content or ""
            print(f"✅ LLM 处理完成: {result}")
            return result, process_time

        except Exception as e:
            process_time = time.time() - start_time
            print(f"❌ LLM 处理失败: {e}")
            return "", process_time

    def is_configured(self) -> bool:
        """检查 OpenAI 是否已配置"""
        return bool(os.getenv("OPENAI_API_KEY")) and self.client is not None

    def get_info(self) -> Dict[str, Any]:
        """获取提供商信息"""
        return {
            "name": "OpenAI",
            "configured": self.is_configured(),
            "default_model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        }






class LLMProcessor:
    """LLM 文本处理器"""

    @classmethod
    def get_system_prompt(cls) -> Optional[str]:
        """获取系统提示"""
        # 从环境变量读取自定义提示
        custom_prompt = os.getenv("LLM_CUSTOM_PROMPT")
        return custom_prompt if custom_prompt else None

    def __init__(self, provider: LLMProvider = None):
        """初始化 LLM 处理器

        Args:
            provider: LLM 提供商，默认自动选择
        """
        if provider:
            self.provider = provider
        else:
            self.provider = self._auto_select_provider()

    def _auto_select_provider(self) -> LLMProvider:
        """自动选择可用的提供商"""
        # 只使用 OpenAI
        provider = OpenAIProvider()

        if provider.is_configured():
            print(f"✅ 使用 LLM 提供商: {provider.get_info()['name']}")
            return provider

        print("⚠️ OpenAI API 未配置，请设置 OPENAI_API_KEY")
        return provider  # 返回 OpenAI 提供商（未配置状态）

    def process(self, text: str, model: Optional[str] = None,
                temperature: float = 0.7, max_tokens: int = 1000) -> tuple[str, float]:
        """处理文本

        Args:
            text: 输入文本
            model: 使用的模型，如果不指定则使用默认模型
            temperature: 温度参数（0-1）
            max_tokens: 最大输出令牌数

        Returns:
            tuple: (处理后的文本, 处理耗时)
        """
        if not self.provider.is_configured():
            print("❌ LLM 提供商未配置")
            return text, 0.0

        # 获取配置
        provider_info = self.provider.get_info()
        config = LLMConfig(
            provider=provider_info["name"],
            model=model or provider_info["default_model"],
            api_key=os.getenv(f"{provider_info['name'].upper()}_API_KEY"),
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=self.get_system_prompt()
        )

        # 处理文本
        return self.provider.process_text(text, config)

    def get_provider_info(self) -> Dict[str, Any]:
        """获取当前提供商信息"""
        return self.provider.get_info()


if __name__ == "__main__":
    # 模块测试
    print("🤖 LLM 处理模块测试")
    print("=" * 40)

    # 创建处理器
    processor = LLMProcessor()

    # 显示提供商信息
    info = processor.get_provider_info()
    print(f"LLM 提供商: {info['name']}")
    print(f"已配置: {'✅' if info['configured'] else '❌'}")
    print()

    if info['configured']:
        custom_prompt = os.getenv("LLM_CUSTOM_PROMPT")
        if custom_prompt:
            print(f"\n💬 自定义提示: {custom_prompt[:50]}...")
        print("\n🚀 LLM 处理模块已准备就绪")
    else:
        print("\n⚠️ 请配置 API 密钥后使用")
        print("   支持的环境变量：")
        print("   - OPENAI_API_KEY")