"""
语音转录模块
统一的语音转文本接口，支持多个供应商
"""

from abc import ABC, abstractmethod
import os
import time
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

import json

load_dotenv()


class TranscriptionProvider(ABC):
    """语音转录提供商的抽象基类"""
    
    @abstractmethod
    def transcribe(self, audio_path: str) -> tuple[str, float]:
        """
        转录音频文件
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            tuple: (转录文本, 转录耗时)
        """
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """检查提供商是否已正确配置"""
        pass


class SiliconFlowProvider(TranscriptionProvider):
    """SiliconFlow 语音转录提供商"""
    
    def __init__(self, api_url: str = None, api_token: str = None, model: str = None):
        self.api_url = api_url or os.getenv("SILICONFLOW_API_URL", "https://api.siliconflow.cn/v1/audio/transcriptions")
        self.api_token = api_token or os.getenv("SILICONFLOW_API_KEY")
        self.model = model or os.getenv("SILICONFLOW_MODEL", "FunAudioLLM/SenseVoiceSmall")
    
    def transcribe(self, audio_path: str) -> tuple[str, float]:
        """使用 SiliconFlow API 转录音频"""
        if not self.is_configured():
            raise ValueError("SiliconFlow API 未配置，请设置 SILICONFLOW_API_KEY")
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
        }
        
        print("📝 转录中...")
        start_time = time.time()
        
        try:
            with open(audio_path, "rb") as audio_file:
                files = {"file": audio_file}
                data = {"model": self.model}
                response = requests.post(self.api_url, headers=headers, files=files, data=data)
            
            inference_time = time.time() - start_time
            response.raise_for_status()
            
            result = response.json()
            text = result.get("text", "")
            print(f"✅ 转录结果: {text}")
            return text, inference_time
            
        except requests.exceptions.RequestException as e:
            inference_time = time.time() - start_time
            error_msg = f"API 请求失败: {e}"
            print(f"❌ {error_msg}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"响应内容: {e.response.text}")
            return "", inference_time
        
        except Exception as e:
            inference_time = time.time() - start_time
            error_msg = f"转录异常: {e}"
            print(f"❌ {error_msg}")
            return "", inference_time
    
    def is_configured(self) -> bool:
        """检查 SiliconFlow 是否已配置"""
        return bool(self.api_token)
    
    def get_info(self) -> Dict[str, Any]:
        """获取提供商信息"""
        return {
            "name": "SiliconFlow",
            "model": self.model,
            "api_url": self.api_url,
            "configured": self.is_configured()
        }


class GroqProvider(TranscriptionProvider):
    """Groq Whisper 提供商"""
    
    def __init__(self, api_key: str = None, model: str = "whisper-large-v3-turbo"):
        self.api_url = "https://gateway.ai.cloudflare.com/v1/b01c38cdbde6badc45f3c084e2a05485/proxy/groq/v1/audio/transcriptions"
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
    
    def transcribe(self, audio_path: str) -> tuple[str, float]:
        """使用 Groq API 转录音频"""
        if not self.is_configured():
            raise ValueError("Groq API 未配置，请设置 GROQ_API_KEY")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        print("📝 转录中...")
        start_time = time.time()
        
        try:
            with open(audio_path, "rb") as audio_file:
                files = {"file": audio_file}
                data = {
                    "model": self.model,
                    "temperature": 0,
                    "response_format": "verbose_json"
                }
                response = requests.post(self.api_url, headers=headers, files=files, data=data)
            
            inference_time = time.time() - start_time
            response.raise_for_status()
            
            result = response.json()
            text = result.get("text", "")
            print(f"✅ 转录结果: {text}")
            return text, inference_time
            
        except requests.exceptions.RequestException as e:
            inference_time = time.time() - start_time
            error_msg = f"API 请求失败: {e}"
            print(f"❌ {error_msg}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"响应内容: {e.response.text}")
            return "", inference_time
        
        except Exception as e:
            inference_time = time.time() - start_time
            error_msg = f"转录异常: {e}"
            print(f"❌ {error_msg}")
            return "", inference_time
    
    def is_configured(self) -> bool:
        """检查 Groq 是否已配置"""
        return bool(self.api_key)
    
    def get_info(self) -> Dict[str, Any]:
        """获取提供商信息"""
        return {
            "name": "Groq",
            "model": self.model,
            "api_url": self.api_url,
            "configured": self.is_configured()
        }


class OpenAIProvider(TranscriptionProvider):
    """OpenAI Whisper 提供商（预留接口）"""
    
    def __init__(self, api_key: str = None, model: str = "whisper-1"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
    
    def transcribe(self, audio_path: str) -> tuple[str, float]:
        """使用 OpenAI API 转录音频"""
        # TODO: 实现 OpenAI Whisper API 调用
        raise NotImplementedError("OpenAI 提供商尚未实现")
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "name": "OpenAI",
            "model": self.model,
            "configured": self.is_configured()
        }


class TranscriptionManager:
    """语音转录管理器"""
    
    def __init__(self, provider: TranscriptionProvider = None):
        """初始化转录管理器
        
        Args:
            provider: 语音转录提供商，默认使用 SiliconFlow
        """
        self.provider = provider or SiliconFlowProvider()
        
        # 验证提供商配置
        if not self.provider.is_configured():
            print(f"⚠️ 语音转录提供商未配置: {self.provider.__class__.__name__}")
    
    def set_provider(self, provider: TranscriptionProvider):
        """设置转录提供商"""
        self.provider = provider
        if not self.provider.is_configured():
            print(f"⚠️ 新提供商未配置: {provider.__class__.__name__}")
    
    def transcribe(self, audio_path: str) -> tuple[str, float]:
        """转录音频文件"""
        if not self.provider.is_configured():
            print("❌ 语音转录提供商未配置")
            return "", 0.0
        
        return self.provider.transcribe(audio_path)
    
    def get_provider_info(self) -> Dict[str, Any]:
        """获取当前提供商信息"""
        return self.provider.get_info()
    
    @classmethod
    def create_siliconflow(cls, api_key: str = None, model: str = None) -> 'TranscriptionManager':
        """工厂方法：创建 SiliconFlow 提供商"""
        provider = SiliconFlowProvider(api_token=api_key, model=model)
        return cls(provider)
    
    @classmethod
    def create_with_env(cls) -> 'TranscriptionManager':
        """工厂方法：从环境变量创建提供商"""
        return cls()


def create_transcription_manager(provider_name: str = "siliconflow", **kwargs) -> TranscriptionManager:
    """创建转录管理器的工厂函数
    
    Args:
        provider_name: 提供商名称，支持 "siliconflow", "groq", "openai"
        **kwargs: 提供商配置参数
        
    Returns:
        TranscriptionManager: 转录管理器实例
    """
    if provider_name.lower() == "siliconflow":
        if kwargs:
            provider = SiliconFlowProvider(
                api_token=kwargs.get("api_key"),
                model=kwargs.get("model"),
                api_url=kwargs.get("api_url")
            )
        else:
            provider = SiliconFlowProvider()
        return TranscriptionManager(provider)
    elif provider_name.lower() == "groq":
        provider = GroqProvider(
            api_key=kwargs.get("api_key"),
            model=kwargs.get("model", "whisper-large-v3-turbo")
        )
        return TranscriptionManager(provider)
    elif provider_name.lower() == "openai":
        provider = OpenAIProvider(
            api_key=kwargs.get("api_key"),
            model=kwargs.get("model", "whisper-1")
        )
        return TranscriptionManager(provider)
    else:
        raise ValueError(f"不支持的提供商: {provider_name}，支持的提供商: siliconflow, groq, openai")


if __name__ == "__main__":
    # 模块测试
    print("🔧 语音转录模块测试")
    print("=" * 40)
    
    # 创建转录管理器
    manager = create_transcription_manager()
    
    # 显示提供商信息
    info = manager.get_provider_info()
    print(f"提供商: {info['name']}")
    print(f"模型: {info['model']}")
    print(f"已配置: {'✅' if info['configured'] else '❌'}")
    
    if info['configured']:
        print("🚀 语音转录模块已准备就绪")
    else:
        print("⚠️ 请配置 API 密钥后使用")
        print("   方法1: 设置环境变量 SILICONFLOW_API_KEY")
        print("   方法2: 创建 .env 文件")
