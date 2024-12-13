"""模型适配器模块。

提供不同 LLM API 的适配器，支持：
1. ChatGLM API
2. Qwen API
3. Meta Llama API
4. Silicon Flow API

每个适配器负责处理特定模型的：
1. API 请求格式
2. 响应解析
3. 流式输出处理
4. 错误处理
"""

import os
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncGenerator, Dict, List, Optional

import aiohttp
from rich.console import Console

console = Console()
MODEL_NAME = os.getenv("MODEL_NAME", "glm-4")
@dataclass
class Message:
    """聊天消息"""
    role: str
    content: str

class ModelAdapter(ABC):
    """模型适配器基类"""

    def __init__(self, api_key: str, api_url: str):
        """初始化适配器

        Args:
            api_key: API 密钥
            api_url: API 端点 URL
        """
        self.api_key = api_key
        self.api_url = api_url

    @abstractmethod
    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        pass

    @abstractmethod
    def format_request(self, messages: List[Message], stream: bool = True) -> Dict:
        """格式化请求数据"""
        pass

    @abstractmethod
    async def parse_stream_line(self, line: str) -> Optional[str]:
        """解析流式响应的单行数据"""
        pass

class ChatGLMAdapter(ModelAdapter):
    """ChatGLM API 适配器"""

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def format_request(self, messages: List[Message], stream: bool = True) -> Dict:
        return {
            "model": MODEL_NAME,
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
            "stream": stream,
            "temperature": 0.7,
            "top_p": 0.7,
        }

    async def parse_stream_line(self, line: str) -> Optional[str]:
        if not line.startswith('data: '):
            return None
        try:
            data = json.loads(line[6:])
            if not data.get('choices') or len(data['choices']) == 0:
                return None
            if data['choices'][0].get('finish_reason') is not None:
                return None
            return data['choices'][0].get('delta', {}).get('content', '')
        except json.JSONDecodeError:
            return None

class QwenAdapter(ModelAdapter):
    """通义千问 API 适配器"""

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def format_request(self, messages: List[Message], stream: bool = True) -> Dict:
        return {
            "model": MODEL_NAME,  # 或其他千问模型
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
            "stream": stream,
            "temperature": 0.7,
            "top_p": 0.7,
        }

    async def parse_stream_line(self, line: str) -> Optional[str]:
        if not line.startswith('data: '):
            return None
        try:
            data = json.loads(line[6:])
            if not data.get('choices'):
                return None
            if data['choices'][0].get('finish_reason') is not None:
                return None
            return data['choices'][0].get('delta', {}).get('content', '')
        except json.JSONDecodeError:
            return None

class LlamaAdapter(ModelAdapter):
    """Meta Llama API 适配器"""

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def format_request(self, messages: List[Message], stream: bool = True) -> Dict:
        return {
            "model": MODEL_NAME,  # 或其他 Llama 模型
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
            "stream": stream,
            "temperature": 0.7,
            "max_tokens": 4096,
        }

    async def parse_stream_line(self, line: str) -> Optional[str]:
        try:
            data = json.loads(line)
            if not data.get('choices'):
                return None
            if data['choices'][0].get('finish_reason') is not None:
                return None
            return data['choices'][0].get('delta', {}).get('content', '')
        except json.JSONDecodeError:
            return None

class SiliconFlowAdapter(ModelAdapter):
    """Silicon Flow API 适配器"""

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def format_request(self, messages: List[Message], stream: bool = True) -> Dict:
        return {
            "model": MODEL_NAME,  # 或其他模型
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
            "stream": stream,
            "temperature": 0.7,
            "max_tokens": 4096,
        }

    async def parse_stream_line(self, line: str) -> Optional[str]:
        if not line.startswith('data: '):
            return None
        try:
            data = json.loads(line[6:])
            if not data.get('choices'):
                return None
            if data['choices'][0].get('finish_reason') is not None:
                return None
            return data['choices'][0].get('delta', {}).get('content', '')
        except json.JSONDecodeError:
            return None

def get_model_adapter(model_type: str, api_key: str, api_url: str) -> ModelAdapter:
    """获取模型适配器实例

    Args:
        model_type: 模型类型 ('chatglm', 'qwen', 'llama', 'silicon')
        api_key: API 密钥
        api_url: API 端点 URL

    Returns:
        对应的模型适配器实例
    """
    adapters = {
        'chatglm': ChatGLMAdapter,
        'qwen': QwenAdapter,
        'llama': LlamaAdapter,
        'silicon': SiliconFlowAdapter,
    }
    adapter_class = adapters.get(model_type.lower())
    if not adapter_class:
        raise ValueError(f"不支持的模型类型: {model_type}")
    return adapter_class(api_key, api_url) 