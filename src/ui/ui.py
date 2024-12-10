"""ChatGLM UI 模块。

此模块提供了终端用户界面相关的功能，包括：
1. 进度条显示
2. 格式化输出
3. 动画效果

作者：Yiyabo!
日期：2024-12-10
"""

from dataclasses import dataclass
from typing import List, Optional

from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from src.config import COMMANDS, get_current_language
from src.core.utils import format_bold_text

# 创建控制台对象
console = Console()


@dataclass
class Message:
    """Message data structure."""

    role: str
    content: str


class ChatHistory:
    """Chat history management class."""

    def __init__(self):
        """Initialize chat history."""
        self.messages: List[Message] = []

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the chat history."""
        self.messages.append(Message(role=role, content=content))

    def get_messages(self) -> List[Message]:
        """Get all messages in the chat history."""
        return self.messages


def format_message(message: str) -> Text:
    """Format a message for display."""
    return Text(message)


def create_panel(
    response: str, border_style: str = "green", width: Optional[int] = None
) -> Panel:
    """Create a panel with the given response."""
    formatted_response = format_message(response)

    # Create panel
    panel = Panel(
        formatted_response,
        title="Assistant",
        title_align="left",
        border_style=border_style,
        width=width,
    )

    return panel


def display_response(response: str) -> None:
    """Display the response in a panel."""
    panel = create_panel(response)
    console.print(panel)


def display_error(error: str) -> None:
    """Display an error message in a panel."""
    panel = create_panel(error, border_style="red")
    console.print(panel)


def create_progress():
    """创建进度条。

    返回：
        Progress: Rich 进度条对象
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    )


class ThinkingSpinner:
    """思考中动画的上下文管理器。"""

    def __init__(self):
        """Initialize thinking spinner."""
        self.spinner = Spinner(
            "dots",
            text=f"[bold green]{get_current_language()['thinking']}[/bold green]",
            style="green",
        )
        self.live = Live(
            self.spinner, console=console, refresh_per_second=10, transient=True
        )

    def __enter__(self):
        """Enter thinking spinner context."""
        self.live.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit thinking spinner context."""
        self.live.stop()


def thinking_spinner():
    """创建思考中动画。

    返回：
        ThinkingSpinner: 支持上下文管理器的动画对象
    """
    return ThinkingSpinner()


def print_welcome():
    """打印欢迎信息。"""
    welcome_text = get_current_language()["welcome"]
    panel = Panel(Align.center(welcome_text), style="bold green")
    console.print(panel)


def print_response(response: str, elapsed_time: float):
    """打印 AI 响应。

    参数：
        response (str): AI 的响应文本
        elapsed_time (float): 响应耗时（秒）
    """
    # 格式化响应文本
    formatted_response = format_bold_text(response)

    # 创建面板
    panel = Panel(
        formatted_response, title="Assistant", title_align="left", border_style="green"
    )

    # 打印响应和耗时
    console.print(panel)
    console.print(
        get_current_language()["response_time"].format(time=elapsed_time),
        style="italic green",
    )


def print_error(error: str):
    """打印错误信息。

    参数：
        error (str): 错误信息
    """
    error_text = get_current_language()["error_message"].format(error=error)
    panel = Panel(error_text, style="bold red", title="Error")
    console.print(panel)


def print_retry(error: str, retry: int, max_retries: int):
    """打印重试信息。

    参数：
        error (str): 错误信息
        retry (int): 当前重试次数
        max_retries (int): 最大重试次数
    """
    retry_text = get_current_language()["retry_message"].format(
        error=error, retry=retry, max_retries=max_retries
    )
    console.print(retry_text, style="yellow")


def print_help():
    """显示帮助信息。"""
    # 创建帮助表格
    table = Table(title="Commands", show_header=True)
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")

    # 添加命令说明
    for command, description in COMMANDS.items():
        table.add_row(command, description)

    # 打印表格
    console.print(table)
