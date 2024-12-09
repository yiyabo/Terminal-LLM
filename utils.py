"""ChatGLM 工具模块。

此模块提供了与 ChatGLM 对话系统相关的工具类和辅助函数，主要包含以下功能：
1. 对话历史管理：记录、保存和加载用户与 AI 的对话历史
2. 响应缓存管理：缓存 AI 的响应，提高系统响应速度
3. 文本格式化：支持 Markdown 风格的文本格式化

主要组件：
- ChatHistory：管理对话历史的类
- ResponseCache：管理响应缓存的类
- format_bold_text：文本格式化函数

依赖：
- json：用于数据序列化
- hashlib：用于生成缓存键
- typing：类型注解支持
- re：正则表达式支持

作者：ChatGLM Team
日期：2024-12-10
"""

import json
import os
from typing import List, Dict, Optional
import hashlib

class ChatHistory:
    """对话历史管理类。

    该类负责管理和持久化存储用户与 AI 助手之间的对话历史记录。
    支持添加新对话、获取最近历史、清空历史等操作。

    属性：
        history_file (str): 历史记录文件的路径
        history (List[Dict]): 存储对话历史的列表，每条记录包含用户输入和 AI 响应

    示例：
        >>> chat_history = ChatHistory("history.json")
        >>> chat_history.add_interaction("你好", "你好！很高兴见到你。")
        >>> recent = chat_history.get_recent_history(5)
    """

    def __init__(self, history_file: str):
        """初始化对话历史管理器。

        参数：
            history_file (str): 历史记录文件的路径
        """
        self.history_file = history_file
        self.history: List[Dict] = self._load_history()

    def _load_history(self) -> List[Dict]:
        """从文件加载历史记录。

        返回：
            List[Dict]: 加载的历史记录列表，如果文件不存在或格式错误则返回空列表
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def add_interaction(self, user_input: str, response: str):
        """添加一条新的对话记录。

        参数：
            user_input (str): 用户的输入内容
            response (str): AI 的响应内容
        """
        self.history.append({
            'user': user_input,
            'assistant': response
        })
        self._save_history()

    def _save_history(self):
        """将历史记录保存到文件。"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def get_recent_history(self, n: int = 5) -> List[Dict]:
        """获取最近的 n 条对话历史。

        参数：
            n (int): 要获取的历史记录数量，默认为 5

        返回：
            List[Dict]: 最近的 n 条历史记录
        """
        return self.history[-n:] if self.history else []

    def clear_history(self):
        """清空所有对话历史。"""
        self.history = []
        self._save_history()

class ResponseCache:
    """响应缓存管理类。

    该类用于缓存 AI 的响应，通过 MD5 哈希值作为键来存储和检索响应，
    可以提高系统的响应速度，避免重复计算。

    属性：
        cache_file (str): 缓存文件的路径
        cache (Dict): 存储响应缓存的字典

    示例：
        >>> cache = ResponseCache("cache.json")
        >>> response = cache.get_cached_response("你好")
        >>> if response is None:
        ...     response = get_ai_response("你好")
        ...     cache.cache_response("你好", response)
    """

    def __init__(self, cache_file: str):
        """初始化响应缓存管理器。

        参数：
            cache_file (str): 缓存文件的路径
        """
        self.cache_file = cache_file
        self.cache: Dict = self._load_cache()

    def _load_cache(self) -> Dict:
        """从文件加载缓存。

        返回：
            Dict: 加载的缓存字典，如果文件不存在或格式错误则返回空字典
        """
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_cache(self):
        """将缓存保存到文件。"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _get_cache_key(self, prompt: str) -> str:
        """生成缓存键。

        使用 MD5 算法对输入文本进行哈希，生成唯一的缓存键。

        参数：
            prompt (str): 输入文本

        返回：
            str: MD5 哈希值作为缓存键
        """
        return hashlib.md5(prompt.encode()).hexdigest()

    def get_cached_response(self, prompt: str) -> Optional[str]:
        """获取缓存的响应。

        参数：
            prompt (str): 输入文本

        返回：
            Optional[str]: 如果存在缓存则返回缓存的响应，否则返回 None
        """
        cache_key = self._get_cache_key(prompt)
        return self.cache.get(cache_key)

    def cache_response(self, prompt: str, response: str):
        """缓存新的响应。

        参数：
            prompt (str): 输入文本
            response (str): 需要缓存的响应
        """
        cache_key = self._get_cache_key(prompt)
        self.cache[cache_key] = response
        self._save_cache()

def format_bold_text(text: str) -> str:
    """格式化文本，支持 Markdown 风格的加粗和列表。

    将 Markdown 风格的加粗语法（**文本**）转换为 Rich 库支持的样式，
    并将破折号列表转换为圆点列表。

    参数：
        text (str): 要格式化的文本

    返回：
        str: 格式化后的文本

    示例：
        >>> print(format_bold_text("**重要提示**"))
        [bold cyan]重要提示[/bold cyan]
        >>> print(format_bold_text("- 第一项"))
        • 第一项
    """
    import re
    # 首先处理加粗文本
    text = re.sub(r'\*\*(.*?)\*\*', lambda m: f'[bold cyan]{m.group(1)}[/bold cyan]', text)
    # 将行首的破折号转换为圆点
    text = re.sub(r'^\s*-\s*', '• ', text, flags=re.MULTILINE)
    return text
