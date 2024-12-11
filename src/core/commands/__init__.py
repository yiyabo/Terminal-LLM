"""命令模块

提供所有命令的实现。
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Type

class Command(ABC):
    """命令基类"""
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> Optional[bool]:
        """执行命令"""
        pass

class CommandFactory:
    """命令工厂类"""
    
    _commands: Dict[str, Type[Command]] = {}
    
    @classmethod
    def register(cls, name: str, command_class: Type[Command]):
        """注册命令"""
        cls._commands[name] = command_class
    
    @classmethod
    def get_command(cls, command_text: str) -> Optional[Command]:
        """获取命令实例"""
        if not command_text.startswith('/'):
            return None
            
        command_parts = command_text[1:].split()
        command_name = command_parts[0]
        
        command_class = cls._commands.get(command_name)
        if command_class:
            return command_class()
        return None

# 导入所有命令
from .basic_commands import ExitCommand, ClearCommand, HelpCommand, LangCommand
from .knowledge_commands import LoadCommand, ClearCommand as ClearKnowledgeCommand, vector_store
from .history_commands import HistoryCommand

# 注册命令
CommandFactory.register('exit', ExitCommand)
CommandFactory.register('clear', ClearCommand)
CommandFactory.register('help', HelpCommand)
CommandFactory.register('lang', LangCommand)
CommandFactory.register('load', LoadCommand)
CommandFactory.register('history', HistoryCommand)
CommandFactory.register('clearknowledge', ClearKnowledgeCommand)
