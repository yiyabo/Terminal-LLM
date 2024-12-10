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
from src.config import get_current_language, COMMANDS
from src.core.utils import format_bold_text

# 创建控制台对象
console = Console()

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

def thinking_spinner():
    """创建思考中动画。
    
    返回：
        ThinkingSpinner: 支持上下文管理器的动画对象
    """
    return ThinkingSpinner()

def print_welcome():
    """打印欢迎信息。"""
    welcome_text = get_current_language()['welcome']
    panel = Panel(
        Align.center(welcome_text),
        style="bold green"
    )
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
        formatted_response,
        title="ChatGLM",
        title_align="left",
        border_style="green"
    )
    
    # 打印响应和耗时
    console.print(panel)
    console.print(
        get_current_language()['response_time'].format(time=elapsed_time),
        style="italic green"
    )

def print_error(error: str):
    """打印错误信息。
    
    参数：
        error (str): 错误信息
    """
    error_text = get_current_language()['error_message'].format(error=error)
    panel = Panel(
        error_text,
        style="bold red",
        title="Error"
    )
    console.print(panel)

def print_retry(error: str, retry: int, max_retries: int):
    """打印重试信息。
    
    参数：
        error (str): 错误信息
        retry (int): 当前重试次数
        max_retries (int): 最大重试次数
    """
    retry_text = get_current_language()['retry_message'].format(
        error=error,
        retry=retry,
        max_retries=max_retries
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
