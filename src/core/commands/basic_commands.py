"""基本命令实现"""

from typing import Optional

from rich.align import Align
from rich.box import DOUBLE
from rich.panel import Panel
from rich.text import Text

from src.config import get_current_language, set_current_language
from src.core.commands.base import Command
from src.ui import console, print_help


# pylint: disable=too-few-public-methods
class ExitCommand(Command):
    """退出命令"""

    async def execute(self, *args, **kwargs) -> Optional[bool]:
        # 创建一个居中对齐的富文本
        text = Text()
        text.append("✨ ", style="bright_yellow")
        text.append(get_current_language()["exit_message"], style="bold bright_white")
        text.append(" ✨", style="bright_yellow")

        # 将文本居中对齐
        aligned_text = Align.center(text)

        # 创建面板，使用渐变边框颜色
        panel = Panel(
            aligned_text,
            border_style="yellow",
            box=DOUBLE,
            padding=(1, 2),
            title="🌟 Terminal-LLM",
            title_align="center",
        )

        # 打印面板
        console.print("\n")  # 添加一个空行
        console.print(panel)
        console.print("\n")  # 添加一个空行
        return False


# pylint: disable=too-few-public-methods
class ClearCommand(Command):
    """清屏命令"""

    async def execute(self, *args, **kwargs) -> Optional[bool]:
        console.clear()
        return True


# pylint: disable=too-few-public-methods
class HelpCommand(Command):
    """帮助命令"""

    async def execute(self, *args, **kwargs) -> Optional[bool]:
        print_help()
        return True


# pylint: disable=too-few-public-methods
class LangCommand(Command):
    """语言切换命令"""

    async def execute(self, *args, **kwargs) -> Optional[bool]:
        try:
            if not args:
                raise KeyError("请指定语言代码 (en/zh)")
            lang_code = args[0]
            set_current_language(lang_code)
            console.print(get_current_language()["language_changed"])
            return True
        except KeyError as e:
            console.print(f"[red]{str(e)}[/red]")
            return True


# pylint: disable=too-few-public-methods
class CopyCommand(Command):
    """复制代码块命令"""

    async def execute(self, *args, **kwargs) -> Optional[bool]:
        try:
            if not args:
                raise ValueError("请指定要复制的代码块编号")
            block_id = int(args[0])
            from src.core.utils import copy_code_block

            copy_code_block(block_id)
            return True
        except ValueError as e:
            console.print(f"[red]错误：{str(e)}[/red]")
            return True
        except Exception as e:
            console.print(f"[red]复制失败：{str(e)}[/red]")
            return True
