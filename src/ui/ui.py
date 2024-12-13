"""UI 模块。

此模块提供了终端用户界面相关的功能，包括：
1. 面板显示：StreamingPanel, MessagePanel
2. 动画效果：进度条、加载动画
3. 状态提示：错误、重试、帮助信息

作者：Yiyabo!
日期：2024-12-10
"""

import time
import math
from dataclasses import dataclass
from typing import List

from rich.align import Align
from rich.box import DOUBLE
from rich.console import Console, Group
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
from rich.style import Style

from src.config import COMMANDS, MODEL_NAME, get_current_language
from src.core.utils import format_bold_text

# 创建控制台对象
console = Console()


# ===== 基础消息类 =====
@dataclass
class Message:
    """消息数据结构"""
    role: str
    content: str


class ChatHistory:
    """聊天历史管理类"""

    def __init__(self):
        """初始化聊天历史"""
        self.messages: List[Message] = []

    def add_message(self, role: str, content: str) -> None:
        """添加消息"""
        self.messages.append(Message(role=role, content=content))

    def get_messages(self) -> List[Message]:
        """获取所有消息"""
        return self.messages


# ===== 面板组件 =====
class StreamingPanel:
    """流式响应面板类"""

    def __init__(self):
        """初始化流式响应面板"""
        self.panel_style = Style(color="green", bold=True)
        self.text_style = Style(color="white")
        self.full_response = ""
        self.is_thinking = True
        self.start_time = time.time()
        
        # 进度条配置 - 超精细的渐变方块字符集
        self.progress_chars = [
            "█", "▉", "▊", "▋", "▌", "▍", "▎", "▏",  # 8种左右渐变
            "▐", "▕",  # 2种边缘方块
            "▀", "▄", "▔", "▁", # 4种上下边缘
            "▆", "▅", "▃", "▂",  # 4种渐变高度
            "▇", "▆", "▅", "▄", "▃", "▂", "▁",  # 7种渐变厚度
            "░", "▒", "▓", "█",  # 4种不同密度
            "⣿", "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷",  # 9种点阵渐变
            "⠿", "⠷", "⠯", "⠟", "⠻", "⠽", "⠾",  # 7种点阵填充
            "⬛", "⬜", "◼", "◾", "▪", "◾", "▫", "◽",  # 8种方块变体
            "∎", "⊞", "⊟", "⊡", "⊠",  # 5种特殊方块
            "◰", "◱", "◲", "◳", "◴", "◵", "◶", "◷",  # 8种分块渐变
            "⯀", "⯁", "⯂", "⯃", "⯄", "⯅", "⯆", "⯇", "⯈",  # 9种几何形状
            "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"  # 6种骰子点数
        ]
        self.bar_width = 20
        
        self.live = Live(
            self._get_panel(),
            refresh_per_second=15,
            auto_refresh=True
        )

    def _get_progress_bar(self, elapsed: float) -> Text:
        """生成动画进度条"""
        # 使用多个动画周期，创造更复杂的动画效果
        char_count = len(self.progress_chars)
        wave_count = 3  # 同时显示的波浪数
        
        # 创建基础进度条
        bar = ["░"] * self.bar_width
        
        # 为每个波浪创建动画
        for wave in range(wave_count):
            # 使用正弦函数创造波浪效果，不同的波浪有不同的速度和相位
            phase = wave * 2 * math.pi / wave_count
            speed = (wave + 1) * 2
            
            # 计算当前波浪的位置
            pos = int(self.bar_width * (0.5 + 0.5 * math.sin(elapsed * speed + phase)))
            
            # 在波浪位置周围添加渐变效果
            gradient_width = char_count // wave_count  # 每个波浪使用的字符数
            for i in range(gradient_width):
                # 计算字符位置，考虑循环
                char_idx = (wave * gradient_width + i) % char_count
                pos_idx = (pos - i) % self.bar_width
                
                # 在合适的位置放置字符
                if 0 <= pos_idx < self.bar_width:
                    bar[pos_idx] = self.progress_chars[char_idx]
        
        return Text("".join(bar), style="bright_green")

    def _get_panel(self) -> Panel:
        """获取当前面板"""
        # 格式化文本
        formatted_text = format_bold_text(self.full_response)
        
        # 如果正在生成，添加进度条
        if self.is_thinking:
            elapsed = time.time() - self.start_time
            content = Group(
                formatted_text,
                Text("", end="") if not formatted_text else Text("\n"),
                self._get_progress_bar(elapsed)
            )
        else:
            content = formatted_text
        
        return Panel(
            content,
            title=f"🤖 {MODEL_NAME}",
            title_align="left",
            border_style=self.panel_style,
            padding=(1, 2),
            width=console.width - 2
        )

    def __enter__(self):
        """进入上下文"""
        console.print()
        self.live.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        self.is_thinking = False
        self.live.update(self._get_panel(), refresh=True)
        self.live.stop()
        console.print()

    def update(self, content: str):
        """更新面板内容"""
        self.full_response += content
        self.live.update(self._get_panel(), refresh=True)

    def get_response(self) -> str:
        """获取完整响应"""
        return self.full_response


class ThinkingSpinner:
    """思考中动画的上下文管理器"""

    def __init__(self):
        """初始化思考中动画"""
        self.spinner = Spinner(
            "dots",
            text=f"[bold green]{get_current_language()['thinking']}[/bold green]",
            style="green",
        )
        self.live = Live(
            self.spinner,
            console=console,
            refresh_per_second=10,
            transient=True
        )

    async def __aenter__(self):
        """异步进入上下文"""
        self.live.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出上下文"""
        self.live.stop()

    def __enter__(self):
        """同步进入上下文"""
        self.live.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """同步退出上下文"""
        self.live.stop()


# ===== 辅助函数 =====
def create_progress() -> Progress:
    """创建进度条"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    )


def thinking_spinner() -> ThinkingSpinner:
    """创建思考中动画"""
    return ThinkingSpinner()


# ===== 显示函数 =====
def print_welcome():
    """打印欢迎信息"""
    text = Text()
    text.append("✨ ", style="bright_yellow")
    text.append(get_current_language()["welcome"], style="bold bright_white")
    text.append(" ✨", style="bright_yellow")

    panel = Panel(
        Align.center(text),
        border_style="yellow",
        box=DOUBLE,
        padding=(1, 2),
        title="🌟 Terminal-LLM",
        title_align="center",
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")


def print_response(response: str, elapsed_time: float):
    """打印 AI 响应"""
    panel = Panel(
        format_bold_text(response),
        title=MODEL_NAME,
        title_align="left",
        border_style="green"
    )

    console.print(panel)
    console.print(
        get_current_language()["response_time"].format(time=elapsed_time),
        style="italic green",
    )


def print_error(error: str):
    """打印错误信息"""
    error_text = get_current_language()["error_message"].format(error=error)
    panel = Panel(error_text, style="bold red", title="Error")
    console.print(panel)


def print_retry(error: str, retry: int, max_retries: int):
    """打印重试信息"""
    retry_text = get_current_language()["retry_message"].format(
        error=error, retry=retry, max_retries=max_retries
    )
    console.print(retry_text, style="yellow")


def print_help():
    """显示帮助信息"""
    table = Table(title="Commands", show_header=True)
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")

    for command, description in COMMANDS.items():
        table.add_row(command, description)

    console.print(table)
