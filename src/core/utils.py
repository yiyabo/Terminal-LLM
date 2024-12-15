"""工具模块。

此模块提供了与 Terminal-LLM 对话系统相关的工具类和辅助函数，主要包含以下功能：
1. 对话历史管理：记录、保存和加载用户与 AI 的对话历史
2. 响应缓存管理：缓存 AI 的响应，提高系统响应速度
3. 文本格式化：支持 Markdown 风格的文本格式化

主要组件：
- ChatHistory：管理对话历史的类
- ResponseCache：管理响应缓存的类
- format_bold_text：文本格式化函数
- format_code_blocks：代码块格式化函数

依赖：
- json：用于数据序列化
- hashlib：用于生成缓存键
- typing：类型注解支持
- re：正则表达式支持
- pyperclip：系统剪贴板支持

作者：Yiyabo!
日期：2024-12-10
"""

import hashlib
import json
import os
import re
from typing import Dict, List, Optional, Tuple

import pyperclip
from rich import box
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.spinner import Spinner
from rich.syntax import Syntax
from rich.text import Text

from src.config import MAX_HISTORY_ITEMS

console = Console()

try:
    import pyperclip

    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print(
        "[yellow]警告: pyperclip 模块未安装，复制功能将不可用。请运行 'pip install pyperclip' 安装。[/yellow]"
    )


def detect_code_blocks(text: str) -> List[Tuple[str, str, int, int]]:
    """检测文本中的代码块。

    参数：
        text (str): 要检测的文本

    返回：
        List[Tuple[str, str, int, int]]: 代码块列表，每个元素为 (语言, 代码内容, 起始位置, 结束位置)
    """
    # 匹配 ```language\ncode\n``` 格式的代码块
    pattern = r"```(\w*)\n(.*?)\n```"
    matches = []

    for match in re.finditer(pattern, text, re.DOTALL):
        lang = match.group(1) or "text"  # 如果没有指定语言，默认为text
        code = match.group(2)
        start = match.start()
        end = match.end()
        matches.append((lang, code, start, end))

    return matches


def copy_to_clipboard(text: str) -> None:
    """复制文本到系统剪贴板。

    参数：
        text (str): 要复制的文本
    """
    if not CLIPBOARD_AVAILABLE:
        console.print("[yellow]复制功能未启用，请先安装 pyperclip：pip install pyperclip[/yellow]")
        return

    try:
        pyperclip.copy(text)
        console.print("[green]✓ 代码已复制到剪贴板[/green]")
    except Exception as e:
        console.print(f"[red]复制失败: {str(e)}[/red]")


# 全局代码块存储
class CodeBlockStore:
    """代码块存储类，用于管理所有代码块"""

    def __init__(self):
        self.blocks = []

    def add_block(self, code: str, language: str) -> int:
        """添加代码块并返回其ID"""
        self.blocks.append((code, language))
        return len(self.blocks)

    def get_block(self, index: int) -> tuple[str, str]:
        """获取代码块，支持负数索引"""
        if not self.blocks:
            raise ValueError("没有可用的代码块")

        # 处理负数索引（相对引用）
        if index < 0:
            index = len(self.blocks) + index

        # 将索引转换为1-based到0-based
        real_index = index - 1

        if not (0 <= real_index < len(self.blocks)):
            raise ValueError(f"代码块 #{index} 不存在")

        return self.blocks[real_index]

    def clear(self):
        """清空所有代码块"""
        self.blocks = []


# 创建全局实例
code_store = CodeBlockStore()


def format_code_block(code: str, language: str = "text", block_id: int = 1) -> Panel:
    """格式化单个代码块。

    参数：
        code (str): 代码内容
        language (str): 代码语言
        block_id (int): 代码块编号

    返回：
        Panel: 格式化后的代码面板
    """
    # 存储代码块
    code_store.add_block(code.strip(), language)

    # 创建语法高亮对象
    syntax = Syntax(
        code.strip(),
        language,
        theme="monokai",
        line_numbers=True,
        word_wrap=True,
        code_width=80,
        background_color="default",
    )

    # 创建面板
    panel = Panel(
        syntax,
        box=box.ROUNDED,
        title=f"[bold blue]{language}[/bold blue]",
        subtitle=f"[bold white]代码块 #{block_id}[/bold white]",
        border_style="blue",
        padding=(0, 1),
        width=console.width - 4,
        expand=False,
    )

    return panel


def copy_code_block(block_id: int) -> bool:
    """复制指定编号的代码块。

    参数：
        block_id (int): 代码块编号（支持负数索引）

    返回：
        bool: 是否成功复制
    """
    if not CLIPBOARD_AVAILABLE:
        console.print("[yellow]复制功能未启用，请先安装 pyperclip：pip install pyperclip[/yellow]")
        return False

    try:
        code, _ = code_store.get_block(block_id)
        pyperclip.copy(code)
        console.print(f"[green]✓ 代码块 #{block_id} 已复制到剪贴板[/green]")
        return True
    except ValueError as e:
        console.print(f"[red]错误：{str(e)}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]复制失败: {str(e)}[/red]")
        return False


def format_text_with_code_blocks(text: str) -> Group:
    """格式化包含代码块的文本。

    参数：
        text (str): 要格式化的文本

    返回：
        Group: 包含文本和代码块的渲染组
    """
    # 检测代码块
    code_blocks = detect_code_blocks(text)
    if not code_blocks:
        return Group(Text.from_markup(format_bold_text(text)))

    # 处理文本和代码块
    renderables = []
    last_end = 0
    block_id = 1

    for lang, code, start, end in code_blocks:
        # 添加代码块之前的文本
        if start > last_end:
            normal_text = Text.from_markup(format_bold_text(text[last_end:start]))
            renderables.append(normal_text)

        # 添加代码面板
        panel = format_code_block(code, lang, block_id)
        renderables.append(panel)

        # 添加复制提示
        copy_hint = Text.from_markup(
            f"[blue]输入 [bold]/copy {block_id}[/bold] 或 [bold]/copy -{len(code_blocks)-block_id+1}[/bold] 复制此代码块[/blue]"
        )
        renderables.append(copy_hint)
        renderables.append(Text("\n"))  # 添加空行

        last_end = end
        block_id += 1

    # 添加最后一个代码块之后的文本
    if last_end < len(text):
        final_text = Text.from_markup(format_bold_text(text[last_end:]))
        renderables.append(final_text)

    return Group(*renderables)


class ChatHistory:
    """对话历史管理类。

    该类负责管理和持久化存储用户与 AI 助手之间的对话历史记录。
    支持添加新对话、获取最近历史、清空历史等操作。

    属性：
        history_file (str): 历史记录文件的路径
        history (List[Dict]): 存储对话历史的列表，每条记录包含用户输入和 AI 响应

    示例：
        >>> chat_history = ChatHistory("history.json")
        >>> chat_history.add_interaction("你好", "你好！很高兴见你。")
        >>> recent = chat_history.get_recent_history(5)
    """

    def __init__(self, history_file: str):
        """初始化对话历史管理器。

        参数：
            history_file (str): 历史记录文件的路径
        """
        self.history_file = history_file
        self.history: List[Dict] = self._load_history()

    def _load_history(self) -> List[Dict]:
        """从文件加载历史记录。

        返回：
            List[Dict]: 加载的历史记录列表，果文件不存在或格式错误则返回空列表
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def add_interaction(self, user_input: str, response: str):
        """添加一条新的对话记录。

        参数：
            user_input (str): 用户的输入内容
            response (str): AI 的响应内容
        """
        self.history.append({"user": user_input, "assistant": response})

        # 如果超过最大记录数，删除最旧的记录
        if len(self.history) > MAX_HISTORY_ITEMS:
            self.history = self.history[-MAX_HISTORY_ITEMS:]

        self._save_history()

    def _save_history(self):
        """将历史记录保存到文件。"""
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def get_recent_history(self, n: int = 5) -> List[Dict]:
        """获取最近的 n 条对话历史。

        参数：
            n (int): 要获取的历史记录数量，默认为 5

        返回：
            List[Dict]: 最近的 n 条史记录
        """
        return self.history[-n:] if self.history else []

    def clear_history(self):
        """清空所有对话历史。"""
        self.history = []
        self._save_history()


class ResponseCache:
    """响应缓存管理类。

    该类用于存 AI 的响应，通过 MD5 哈希值作为键来存储和检索响应，
    可以提高系统的响应速度，避免重复计算。

    属性：
        cache_file (str): 缓存文件的路径
        cache (Dict): 存储响应缓存的字典

    示例：
        >>> cache = ResponseCache("cache.json")
        >>> response = cache.get_cached_response("你好")
        >>> if response is None:
        ...     response = get_ai_response("你好")
        ...     cache.cache_response("你好", response)
    """

    def __init__(self, cache_file: str):
        """初始化响应缓存管理器。

        参数：
            cache_file (str): 缓存文件��路径
        """
        self.cache_file = cache_file
        self.cache: Dict = self._load_cache()

    def _load_cache(self) -> Dict:
        """从文件加载缓存。

        返回：
            Dict: 加载的缓存字典，如果文件不存在或格式错误则返回空字典
        """
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_cache(self):
        """将缓存存到文。"""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _get_cache_key(self, prompt: str) -> str:
        """生成缓存键。

        使用 MD5 算法对输入文本进行哈希，生成唯一的缓存键。

        参数：
            prompt (str): 输入文本

        返回：
            str: MD5 哈希值作为缓存键
        """
        return hashlib.md5(prompt.encode()).hexdigest()

    def get_cached_response(self, prompt: str) -> Optional[str]:
        """获取缓存的响应。

        参数：
            prompt (str): 输入文本

        返回：
            Optional[str]: 如果存在缓存则返回缓存的响应，否则返回 None
        """
        cache_key = self._get_cache_key(prompt)
        return self.cache.get(cache_key)

    def cache_response(self, prompt: str, response: str):
        """缓存新的响应。

        参数：
            prompt (str): 输入文本
            response (str): 需要缓存的响应
        """
        cache_key = self._get_cache_key(prompt)
        self.cache[cache_key] = response
        self._save_cache()


def format_bold_text(text: str) -> str:
    """格式化本，支持 Markdown 风格的加粗和表。

    将 Markdown 风格的加粗法（**文本**）转换为 Rich 库支持的样式，
    并将破折号列表转换为圆点列表。

    参数：
        text (str): 要格式化的文本

    返回：
        str: 格式化后的文本
    """
    # 处理标题（以 # 开头的行）
    text = re.sub(
        r"^#\s+(.+)$", r"[bold magenta]\1[/bold magenta]", text, flags=re.MULTILINE
    )

    # 处理数字列表项的加粗标题
    text = re.sub(
        r"^(\d+\.)\s+\*\*([^*]+)\*\*",
        r"\1 [bold cyan]\2[/bold cyan]",
        text,
        flags=re.MULTILINE,
    )

    # 处理其他加粗文本
    text = re.sub(r"\*\*([^*]+)\*\*", r"[bold cyan]\1[/bold cyan]", text)

    # 处理列表项（以 - 或 • 开头的行）
    text = re.sub(r"^\s*[-•]\s*(.+)$", r"  [cyan]•[/cyan] \1", text, flags=re.MULTILINE)

    # 处理子列表项（缩进的列表项）
    text = re.sub(
        r"^\s{4,}[-•]\s*(.+)$",
        r"    [dim cyan]○[/dim cyan] \1",
        text,
        flags=re.MULTILINE,
    )

    # 处理引用文本
    text = re.sub(
        r"^\s*>\s+(.+)$", r"[dim italic]\1[/dim italic]", text, flags=re.MULTILINE
    )

    # 处理行内代码
    text = re.sub(r"`([^`]+)`", r"[bold yellow]\1[/bold yellow]", text)

    # 处理斜体文本
    text = re.sub(r"\*([^*]+)\*", r"[italic]\1[/italic]", text)

    # 处理长句子的自动换行和对齐
    lines = text.split("\n")
    formatted_lines = []
    for line in lines:
        if len(line.strip()) > 80:  # 如果行长度超过80个字符
            # 保持缩进，将文本按照标点符号分割成多行
            indent = len(line) - len(line.lstrip())
            indent = " " * indent
            content = line.strip()
            parts = re.split(r"([。，；：])", content)
            new_line = indent
            for i in range(0, len(parts) - 1, 2):
                new_line += parts[i] + parts[i + 1] + "\n" + indent
            if len(parts) % 2 == 1:
                new_line += parts[-1]
            formatted_lines.append(new_line.rstrip())
        else:
            formatted_lines.append(line)

    return "\n".join(formatted_lines)
