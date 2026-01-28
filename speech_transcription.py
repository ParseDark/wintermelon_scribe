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

# 阿里云SDK导入
try:
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
    from aliyunsdktingwu.request.v20230930.CreateTaskRequest import CreateTaskRequest
    from aliyunsdktingwu.request.v20230930.GetTaskInfoRequest import GetTaskInfoRequest
    # 注意：停止任务的请求可能不存在或命名不同
    ALIYUN_SDK_AVAILABLE = True
except ImportError:
    ALIYUN_SDK_AVAILABLE = False

# 七牛云SDK导入
try:
    from qiniu import Auth as QiniuAuth, put_data
    QINIU_SDK_AVAILABLE = True
except ImportError:
    QINIU_SDK_AVAILABLE = False

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
        provider_name: 提供商名称，支持 "siliconflow", "groq", "aliyun_tingwu"
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
    elif provider_name.lower() in ["aliyun", "aliyun_tingwu", "tingwu"]:
        provider = AliyunTingwuProvider(
            access_key_id=kwargs.get("access_key_id"),
            access_key_secret=kwargs.get("access_key_secret"),
            region_id=kwargs.get("region_id", "cn-beijing"),
            project_name=kwargs.get("project_name", "default")
        )
        return TranscriptionManager(provider)
    else:
        raise ValueError(f"不支持的提供商: {provider_name}，支持的提供商: siliconflow, groq, aliyun_tingwu")


# 预留其他提供商的扩展接口
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


class GroqProvider(TranscriptionProvider):
    """Groq Whisper 提供商"""
    
    def __init__(self, api_key: str = None, model: str = "whisper-large-v3-turbo"):
        self.api_url = "https://api.groq.com/openai/v1/audio/transcriptions"
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


class AliyunTingwuProvider(TranscriptionProvider):
    """阿里云听悟语音转录提供商"""
    
    def __init__(self, access_key_id: str = None, access_key_secret: str = None, 
                 region_id: str = None, project_name: str = None):
        if not ALIYUN_SDK_AVAILABLE:
            raise ImportError("阿里云SDK未安装，请运行: pip install aliyun-python-sdk-core aliyun-python-sdk-tingwu")
        
        self.access_key_id = access_key_id or os.getenv("ALIYUN_ACCESS_KEY_ID")
        self.access_key_secret = access_key_secret or os.getenv("ALIYUN_ACCESS_KEY_SECRET")
        self.region_id = region_id or os.getenv("ALIYUN_REGION_ID", "cn-beijing")
        self.project_name = project_name or os.getenv("ALIYUN_TINGWU_PROJECT_NAME", "default")
        
        # 七牛云配置
        self.qiniu_access_key = os.getenv("QINIU_ACCESS_KEY")
        self.qiniu_secret_key = os.getenv("QINIU_SECRET_KEY")
        self.qiniu_bucket_name = os.getenv("QINIU_BUCKET_NAME")
        self.qiniu_domain = os.getenv("QINIU_DOMAIN")
        
        # 初始化阿里云客户端
        self.client = None
        if self.access_key_id and self.access_key_secret:
            try:
                self.client = AcsClient(
                    ak=self.access_key_id,
                    secret=self.access_key_secret,
                    region_id=self.region_id
                )
                print("✅ 阿里云听悟客户端初始化成功")
            except Exception as e:
                print(f"⚠️ 阿里云听悟客户端初始化失败: {e}")
                self.client = None
    
    def upload_to_qiniu(self, audio_path: str) -> str:
        """上传音频文件到七牛云，返回公开访问URL"""
        if not all([QINIU_SDK_AVAILABLE, self.qiniu_access_key, self.qiniu_secret_key, 
                   self.qiniu_bucket_name, self.qiniu_domain]):
            print("❌ 七牛云配置不完整或SDK未安装")
            return ""
        
        try:
            # 生成唯一文件名
            import uuid
            file_ext = os.path.splitext(os.path.basename(audio_path))[1]
            filename = f"audio/{uuid.uuid4().hex}{file_ext}"
            
            # 读取文件内容
            with open(audio_path, 'rb') as f:
                file_data = f.read()
            
            # 创建七牛云认证对象
            q = QiniuAuth(self.qiniu_access_key, self.qiniu_secret_key)
            
            # 生成上传token
            token = q.upload_token(self.qiniu_bucket_name, filename, 3600)
            
            # 上传文件
            ret, info = put_data(token, filename, file_data)
            
            if info.status_code == 200 and ret:
                url = f"{self.qiniu_domain.rstrip('/')}/{filename}"
                print(f"☁️ 七牛云上传成功: {url}")
                return url
            else:
                print(f"❌ 七牛云上传失败: {info}")
                return ""
                
        except Exception as e:
            print(f"❌ 七牛云上传异常: {e}")
            return ""
    
    def transcribe(self, audio_path: str) -> tuple[str, float]:
        """使用阿里云听悟API转录音频"""
        if not self.is_configured():
            raise ValueError("阿里云听悟API未配置，请设置ALIYUN_ACCESS_KEY_ID和ALIYUN_ACCESS_KEY_SECRET")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")
        
        print("📝 阿里云听悟转录中...")
        start_time = time.time()
        
        try:
            # 1. 创建转录任务
            task_id = self._create_transcription_task(audio_path)
            if not task_id:
                inference_time = time.time() - start_time
                return "", inference_time
            
            # 2. 轮询任务状态
            result = self._wait_for_task_completion(task_id)
            
            inference_time = time.time() - start_time
            
            if result:
                print(f"✅ 转录结果: {result}")
                return result, inference_time
            else:
                print("❌ 转录失败或无结果")
                return "", inference_time
                
        except Exception as e:
            inference_time = time.time() - start_time
            error_msg = f"阿里云听悟转录异常: {e}"
            print(f"❌ {error_msg}")
            return "", inference_time
    
    def _create_transcription_task(self, audio_path: str) -> str:
        """创建转录任务"""
        try:
            # 检查是否为远程文件URL
            if audio_path.startswith(('http://', 'https://')):
                file_url = audio_path
                print(f"📁 使用远程文件URL: {file_url}")
            else:
                # 本地文件，上传到七牛云
                print("📤 本地音频文件，准备上传到七牛云...")
                file_url = self.upload_to_qiniu(audio_path)
                if not file_url:
                    print("❌ 七牛云上传失败，无法使用阿里云听悟")
                    print(f"💡 建议使用SiliconFlow或Groq提供商处理本地文件")
                    return ""
            
            request = CreateTaskRequest()
            
            # 构建请求参数
            body_params = {
                "ProjectName": self.project_name,
                "FileUrl": file_url,
                "FileFormat": os.path.splitext(os.path.basename(audio_path))[1][1:].lower(),
                "Language": "zh-CN",  # 中文
                "Model": "paraformer-v1",  # 使用的模型
                "SampleRate": 16000  # 采样率
            }
            
            request.set_body_params(body_params)
            response = self.client.do_action_with_exception(request)
            result = eval(response.decode('utf-8'))
            
            if result.get('Code') == '200':
                task_id = result.get('Data', {}).get('TaskId')
                print(f"📋 转录任务已创建: {task_id}")
                return task_id
            else:
                print(f"❌ 创建转录任务失败: {result.get('Message')}")
                return ""
                
        except (ServerException, ClientException) as e:
            print(f"❌ 创建转录任务异常: {e}")
            return ""
    
    def _wait_for_task_completion(self, task_id: str, max_wait_time: int = 120) -> str:
        """等待转录任务完成"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                request = GetTaskInfoRequest()
                request.set_query_params({"TaskId": task_id})
                
                response = self.client.do_action_with_exception(request)
                result = eval(response.decode('utf-8'))
                
                if result.get('Code') == '200':
                    data = result.get('Data', {})
                    status = data.get('Status')
                    
                    if status == 'completed':
                        # 解析转录结果
                        results = data.get('Results', [])
                        if results:
                            # 提取文本结果
                            sentences = []
                            for item in results:
                                if 'SentenceList' in item:
                                    for sentence in item['SentenceList']:
                                        if 'Text' in sentence:
                                            sentences.append(sentence['Text'])
                            return ''.join(sentences)
                    elif status == 'failed':
                        error_msg = data.get('FailReason', '未知错误')
                        print(f"❌ 转录任务失败: {error_msg}")
                        return ""
                    elif status in ['running', 'queued']:
                        print(f"⏳ 转录进行中... 状态: {status}")
                        time.sleep(2)
                        continue
                
            except (ServerException, ClientException) as e:
                print(f"⚠️ 查询任务状态异常: {e}")
                time.sleep(2)
                continue
        
        print(f"⏰ 转录任务超时 ({max_wait_time}秒)")
        return ""
    
    def is_configured(self) -> bool:
        """检查阿里云听悟是否已配置"""
        return bool(self.access_key_id and self.access_key_secret and self.client)
    
    def get_info(self) -> Dict[str, Any]:
        """获取提供商信息"""
        return {
            "name": "阿里云听悟",
            "model": "paraformer-v1",
            "region": self.region_id,
            "project": self.project_name,
            "configured": self.is_configured(),
            "sdk_available": ALIYUN_SDK_AVAILABLE,
            "qiniu_available": QINIU_SDK_AVAILABLE,
            "qiniu_configured": bool(self.qiniu_access_key and self.qiniu_secret_key and 
                                   self.qiniu_bucket_name and self.qiniu_domain)
        }


class AzureProvider(TranscriptionProvider):
    """Azure 语音服务提供商（预留接口）"""
    
    def transcribe(self, audio_path: str) -> tuple[str, float]:
        """使用 Azure API 转录音频"""
        # TODO: 实现 Azure Speech Services API 调用
        raise NotImplementedError("Azure 提供商尚未实现")
    
    def is_configured(self) -> bool:
        return False  # TODO: 实现配置检查
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "name": "Azure",
            "configured": self.is_configured()
        }


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
