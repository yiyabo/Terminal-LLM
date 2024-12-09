"""ChatGLM 配置模块。

此模块包含了 ChatGLM 终端应用程序的所有配置项，包括：
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
    - CHATGLM_API_KEY
    - CHATGLM_API_URL (可选)
    - CHATGLM_MODEL (可选)

作者：ChatGLM Team
日期：2024-12-10
"""

import os
import aiohttp
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
API_KEY = os.getenv('CHATGLM_API_KEY', '')  # ChatGLM API密钥
API_URL = os.getenv('CHATGLM_API_URL', 'https://open.bigmodel.cn/api/paas/v4/chat/completions')  # API端点URL
MODEL_NAME = os.getenv('CHATGLM_MODEL', 'glm-4-flash')  # 使用的模型名称

# 重试配置
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 2  # 重试间隔（秒）
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=30)  # 请求超时时间（秒）

# 缓存配置
CACHE_ENABLED = True  # 是否启用响应缓存
CACHE_FILE = 'chat_cache.json'  # 缓存文件路径
HISTORY_FILE = 'chat_history.json'  # 历史记录文件路径

# 多语言支持配置
LANGUAGES = {
    "en": {
        "welcome": "✨ Welcome to the ChatGLM Terminal Version ✨",
        "user_prompt": "🔎 User: ",
        "exit_message": "🌟🌟 Exiting 🌟🌟",
        "thinking": "Thinking, please wait...",
        "response_time": "Response time: {time:.2f} seconds",
        "error_message": "Error: {error}",
        "retry_message": "Request failed: {error}. Retrying {retry}/{max_retries}...",
        "clear_message": "Screen cleared.",
        "history_title": "Chat History",
        "language_changed": "Language changed to English.",
    },
    "zh": {
        "welcome": "✨欢迎使用终端版本ChatGLM✨",
        "user_prompt": "🔎 User: ",
        "exit_message": "🌟🌟正在退出🌟🌟",
        "thinking": "正在思考中，请稍候...",
        "response_time": "响应时间: {time:.2f} 秒",
        "error_message": "错误: {error}",
        "retry_message": "请求失败: {error}. 重试 {retry}/{max_retries}...",
        "clear_message": "屏幕已清除。",
        "history_title": "聊天记录",
        "language_changed": "语言已切换为中文。",
    },
}

# 命令配置
COMMANDS = {
    'exit': '退出程序',
    'clear': '清除屏幕',
    'history': '显示聊天历史',
    'lang': '切换语言 (lang en/zh)',
    'help': '显示帮助信息'
}
