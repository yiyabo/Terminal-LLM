"""核心功能模块

包含 Shell AI 和聊天功能的核心实现。
"""

from .chat import main as chat_main
from .commands import CommandFactory, Command
from .utils import ChatHistory

# 导入所有核心功能
__all__ = ['chat_main', 'CommandFactory', 'Command', 'ChatHistory']