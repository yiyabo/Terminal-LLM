"""命令模块。

此模块实现了命令模式，用于处理各种终端命令。
每个命令都是一个单独的类，实现了 Command 接口。

作者：Yiyabo!
日期：2024-12-10
"""

from abc import ABC, abstractmethod
from typing import Optional

from rich.align import Align
from rich.console import Console
from rich.panel import Panel

from src.config import get_current_language, set_current_language
from src.core.utils import ChatHistory
from src.ui import console, print_help, print_welcome

# 初始化历史记录
chat_history = ChatHistory("data/history/chat_history.json")


class Command(ABC):
    """命令接口。"""

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[bool]:
        """执行命令。

        返回：
            Optional[bool]:
            - True: 命令执行成功
            - False: 用户请求退出
            - None: 需要继续处理（如发送到 API）
        """
        pass


class ExitCommand(Command):
    """退出命令。"""

    def execute(self, *args, **kwargs) -> bool:
        message = get_current_language()["exit_message"]
        panel = Panel(Align.center(message), style="bold green")
        console.print(panel)
        return False


class ClearCommand(Command):
    """清屏命令。"""

    def execute(self, *args, **kwargs) -> bool:
        console.clear()
        print_welcome()
        console.print(get_current_language()["clear_message"])
        return True


class HistoryCommand(Command):
    """历史记录命令。"""

    def execute(self, *args, **kwargs) -> bool:
        from rich.panel import Panel

        history = chat_history.get_recent_history()
        history_text = "\n".join(
            [f"User: {h['user']}\nLLM: {h['assistant']}" for h in history]
        )
        console.print(
            Panel(
                history_text,
                title=get_current_language()["history_title"],
                expand=False,
            )
        )
        return True


class LangCommand(Command):
    """语言切换命令。"""

    def execute(self, lang_code: str, *args, **kwargs) -> bool:
        try:
            set_current_language(lang_code)
            console.print(get_current_language()["language_changed"])
        except KeyError as e:
            console.print(f"[red]{e}[/red]")
        return True


class HelpCommand(Command):
    """帮助命令。"""

    def execute(self, *args, **kwargs) -> bool:
        print_help()
        return True


class CommandFactory:
    """命令工厂类。"""

    _commands = {
        "exit": ExitCommand(),
        "quit": ExitCommand(),
        "/exit": ExitCommand(),
        "/quit": ExitCommand(),
        "clear": ClearCommand(),
        "/clear": ClearCommand(),
        "history": HistoryCommand(),
        "/history": HistoryCommand(),
        "help": HelpCommand(),
        "/help": HelpCommand(),
    }

    @classmethod
    def get_command(cls, user_input: str) -> Optional[Command]:
        """获取对应的命令对象。

        参数：
            user_input (str): 用户输入

        返回：
            Optional[Command]: 命令对象，如果不是命令则返回 None
        """
        # 处理语言切换命令
        if user_input.lower().startswith(("lang ", "/lang ")):
            return LangCommand()

        return cls._commands.get(user_input.lower())
