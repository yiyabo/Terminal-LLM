"""ChatGLM UI 模块。

此模块提供了终端用户界面相关的功能，包括：
1. 进度条显示
2. 格式化输出
3. 动画效果

作者：Yiyabo!
日期：2024-12-10
"""

from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.spinner import Spinner
from rich.table import Table
from rich.markdown import Markdown
from config import get_current_language, COMMANDS
from utils import format_bold_text

console = Console()

def create_progress() -> Progress:
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
        transient=True
    )

class ThinkingSpinner:
    """思考中动画的上下文管理器。"""
    
    def __init__(self):
        self.spinner = Spinner(
            "dots",
            text=f"[bold green]{get_current_language()['thinking']}[/bold green]",
            style="green"
        )
        self.live = Live(
            self.spinner,
            console=console,
            refresh_per_second=10,
            transient=True
        )
    
    def __enter__(self):
        self.live.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.live.stop()

def thinking_spinner() -> ThinkingSpinner:
    """创建思考中动画。
    
    返回：
        ThinkingSpinner: 支持上下文管理器的动画对象
    """
    return ThinkingSpinner()

def print_welcome() -> None:
    """打印欢迎信息。"""
    welcome_panel = Panel(
        Align.center(f"[bold cyan]✨{get_current_language()['welcome']}✨[/bold cyan]"),
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(welcome_panel)

def print_response(response: str, elapsed_time: float) -> None:
    """打印 AI 响应。
    
    参数：
        response (str): AI 的响应文本
        elapsed_time (float): 响应耗时（秒）
    """
    # 创建一个带边框的面板来显示响应
    formatted_response = format_bold_text(response)
    response_panel = Panel(
        formatted_response,
        title="[bold cyan]Assistant[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(response_panel)
    
    # 打印响应时间，使用暗色调
    console.print(
        f"[dim italic]{get_current_language()['response_time'].format(time=elapsed_time)}[/dim italic]",
        justify="right"
    )

def print_error(error: str) -> None:
    """打印错误信息。
    
    参数：
        error (str): 错误信息
    """
    error_panel = Panel(
        f"[red]{get_current_language()['error_message'].format(error=error)}[/red]",
        border_style="red",
        title="[bold red]Error[/bold red]",
        padding=(1, 2)
    )
    console.print(error_panel)

def print_retry(error: str, retry: int, max_retries: int) -> None:
    """打印重试信息。
    
    参数：
        error (str): 错误信息
        retry (int): 当前重试次数
        max_retries (int): 最大重试次数
    """
    retry_panel = Panel(
        f"[yellow]{get_current_language()['retry_message'].format(error=error, retry=retry, max_retries=max_retries)}[/yellow]",
        border_style="yellow",
        title="[bold yellow]Retry[/bold yellow]",
        padding=(1, 2)
    )
    console.print(retry_panel)

def print_help() -> None:
    """显示帮助信息。"""
    commands_table = Table(
        "Command", "Description",
        title="[bold cyan]Available Commands[/bold cyan]",
        border_style="cyan",
        header_style="bold cyan",
        padding=(0, 2)
    )
    
    for cmd, desc in COMMANDS.items():
        commands_table.add_row(f"[green]{cmd}[/green]", desc)
    
    help_panel = Panel(
        commands_table,
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(help_panel)
