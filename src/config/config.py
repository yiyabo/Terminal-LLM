"""Terminal-LLM 配置模块。

此模块包含了 Terminal-LLM 终端应用程序的所有配置项，包括：
1. API 配置：API密钥、URL和模型名称
2. 重试策略：最大重试次数、重试延迟和超时设置
3. 缓存配置：缓存开关和文件路径
4. 多语言支持：支持中英文的界面文本
5. 命令配置：可用的终端命令及其描述

依赖：
- os：用于环境变量操作
- python-dotenv：用于加载 .env 文件中的环境变量
- aiohttp：用于超时设置

使用方法：
    >>> from config import API_KEY, API_URL
    >>> print(f"Using API at {API_URL}")

注意：
    使用前请确保 .env 文件中包含必要的环境变量：
    - API_KEY
    - API_URL (可选)
    - MODEL_NAME (可选)

作者：Yiyabo!
日期：2024-12-10
"""

import os

import aiohttp
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 日志文件路径
# 获取当前文件所在目录的父目录（src）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 构建日志文件的绝对路径
LOG_FILE = os.path.join(BASE_DIR, "data", "chat.log")

# API配置
API_KEY = os.getenv("API_KEY", "")  # API密钥
API_URL = os.getenv(
    "API_URL", "https://open.bigmodel.cn/api/paas/v4/chat/completions"
)  # API端点URL
MODEL_NAME = os.getenv("MODEL_NAME", "glm-4-flash")  # 使用的模型名称

# 重试配置
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 2  # 重试间隔（秒）
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=30)  # 请求超时时间（秒）

# 缓存配置
CACHE_ENABLED = True  # 是否启用响应缓存
# 缓存配置
CACHE_FILE = os.path.join(BASE_DIR, "data", "cache", "chat_cache.json")  # 缓存文件路径
HISTORY_FILE = os.path.join(
    BASE_DIR, "data", "history", "chat_history.json"
)  # 历史记录文件路径
MAX_HISTORY_ITEMS = 100  # 最大历史记录数量


# 多语言支持配置
LANGUAGES = {
    "en": {
        "welcome": "🤖 Welcome to Terminal-LLM! How can I assist you today? 🚀",
        "user_prompt": "🔎 User: ",
        "exit_message": "👋 Goodbye! Have a great day! ✨",
        "thinking": "Thinking, please wait...",
        "response_time": "Response time: {time:.2f} seconds",
        "error_message": "Error: {error}",
        "retry_message": "Request failed: {error}. Retrying {retry}/{max_retries}...",
        "clear_message": "Screen cleared.",
        "history_title": "Chat History",
        "language_changed": "Language changed to English.",
        "invalid_command": "Invalid command. Type /help to see available commands.",
        "timeout": "Request timeout, please try again later",
    },
    "zh": {
        "welcome": "🤖 欢迎使用 Terminal-LLM！我能为您做些什么？🚀",
        "user_prompt": "🔎 User: ",
        "exit_message": "👋 再见！祝您愉快！✨",
        "thinking": "正在思考中，请稍候...",
        "response_time": "响应时间: {time:.2f} 秒",
        "error_message": "错误: {error}",
        "retry_message": "请求失败: {error}. 重试 {retry}/{max_retries}...",
        "clear_message": "屏幕已清除。",
        "history_title": "聊天记录",
        "language_changed": "语言已切换为中文。",
        "invalid_command": "无效的命令。输入 /help 查看可用命令。",
        "timeout": "请求超时，请稍后重试",
    },
}

class LanguageManager:
    """语言管理器"""
    _current_language = "zh"

    @classmethod
    def get_current_language(cls):
        """获取当前语言配置。"""
        return LANGUAGES[cls._current_language]

    @classmethod
    def set_current_language(cls, lang_code: str):
        """设置当前语言。

        参数：
            lang_code (str): 语言代码，支持 'en' 和 'zh'

        异常：
            KeyError: 当语言代码不存在时抛出
        """
        if lang_code not in LANGUAGES:
            raise KeyError(f"Language '{lang_code}' not supported")
        cls._current_language = lang_code


# 导出语言管理方法
get_current_language = LanguageManager.get_current_language
set_current_language = LanguageManager.set_current_language

# 命令配置
COMMANDS = {
    "/exit": "退出程序",
    "/clear": "清除屏幕",
    "/history": "显示历史记录",
    "/lang": "切换语言 (en/zh)",
    "/help": "显示帮助信息",
    "/load": "加载文档 (/load [文件路径])",
}
