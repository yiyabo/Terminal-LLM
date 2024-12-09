"""ChatGLM 终端交互模块。

此模块实现了一个基于终端的 ChatGLM 交互界面，提供以下功能：
1. 异步 API 调用：使用 aiohttp 进行异步 HTTP 请求
2. 交互式命令行：支持命令补全和历史记录
3. 多语言支持：支持中英文界面切换
4. 错误处理：包含重试机制和友好的错误提示
5. 美化输出：使用 Rich 库实现终端美化

主要功能：
- 异步 API 调用和响应处理
- 用户输入处理和命令解析
- 聊天历史记录管理
- 终端界面渲染

依赖：
- asyncio：异步 IO 支持
- aiohttp：异步 HTTP 客户端
- rich：终端美化
- prompt_toolkit：命令行交互
- logging：日志记录

使用方法：
    >>> python Chat.py

作者：ChatGLM Team
日期：2024-12-10
"""

#!/usr/bin/env python
import asyncio
import aiohttp
import time
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.spinner import Spinner
from time import perf_counter
import re
import logging
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory

# 初始化日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 初始化 Rich 控制台
console = Console()

# 多语言支持配置
LANGUAGES = {
    "en": {
        "welcome": "✨ Welcome to the ChatGLM Terminal Version ✨",
        "user_prompt": "🔎 User: ",
        "exit_message": "🌟🌟 Exiting 🌟🌟",
        "thinking": "Thinking, please wait...",
        "response_time": "Response time: {time:.2f} seconds",
        "error_message": "Error: Received unexpected status code",
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
        "error_message": "错误: 接收到意外的状态码",
        "retry_message": "请求失败: {error}. 重试 {retry}/{max_retries}...",
        "clear_message": "屏幕已清除。",
        "history_title": "聊天记录",
        "language_changed": "语言已切换为中文。",
    },
}

# 默认语言
current_language = LANGUAGES["zh"]

# 命令补全器
COMMANDS = {
    'exit': '退出程序',
    'clear': '清除屏幕',
    'history': '显示聊天历史',
    'lang': '切换语言 (lang en/zh)',
    'help': '显示帮助信息'
}

command_completer = WordCompleter(list(COMMANDS.keys()), ignore_case=True)
prompt_session = PromptSession(history=InMemoryHistory())

# API 配置
api_key = "9c70867a71f29253e978f053863d4f1f.cayZWvePGcRF2U5C"
api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
max_retries = 3  # 最大重试次数
retry_delay = 2  # 重试延迟时间（秒）

# 用于存储聊天记录
chat_history = []

def format_bold_text(text: str) -> str:
    """格式化文本，支持 Markdown 风格的加粗和列表。

    将 Markdown 风格的加粗语法（**文本**）转换为 Rich 库支持的样式，
    并将破折号列表转换为圆点列表。

    参数：
        text (str): 要格式化的文本

    返回：
        str: 格式化后的文本

    示例：
        >>> print(format_bold_text("**重要提示**"))
        [bold cyan]重要提示[/bold cyan]
        >>> print(format_bold_text("- 第一项"))
        • 第一项
    """
    # 首先处理加粗文本
    text = re.sub(r'\*\*(.*?)\*\*', lambda m: f'[bold cyan]{m.group(1)}[/bold cyan]', text)
    # 将行首的破折号转换为圆点
    text = re.sub(r'^\s*-\s*', '• ', text, flags=re.MULTILINE)
    return text

async def get_response(session: aiohttp.ClientSession, prompt: str) -> str:
    """异步获取 API 响应。

    向 ChatGLM API 发送请求并获取响应，包含重试机制和错误处理。

    参数：
        session (aiohttp.ClientSession): aiohttp 会话对象
        prompt (str): 用户输入的提示文本

    返回：
        str: API 的响应文本，如果发生错误则返回错误信息

    异常：
        aiohttp.ClientError: HTTP 客户端错误
        asyncio.TimeoutError: 请求超时
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "glm-4-flash",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    retries = 0
    while retries < max_retries:
        try:
            async with session.post(api_url, headers=headers, json=payload) as response:
                if response.status == 200:
                    response_data = await response.json()
                    response_text = response_data['choices'][0]['message']['content']
                    return format_bold_text(response_text)
                else:
                    error_message = current_language['error_message'].format(response.status)
                    console.print(f"[red]{error_message}[/red]")
                    logging.error(f"Received unexpected status code: {response.status}")
                    return "抱歉，没有输入哦，请重新输入～🤩"
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            retry_message = current_language['retry_message'].format(error=e, retry=retries + 1, max_retries=max_retries)
            console.print(retry_message)
            logging.warning(retry_message)
            retries += 1
            await asyncio.sleep(retry_delay)

    error_message = "抱歉，连接失败，请稍后再试。"
    console.print(f"[red]{error_message}[/red]")
    logging.error(error_message)
    return error_message

def print_welcome_message() -> None:
    """打印欢迎信息。

    使用 Rich 库创建一个居中的面板显示欢迎信息。
    """
    welcome_panel = Panel(Align.center(f"[bold cyan]{current_language['welcome']}[/bold cyan]"))
    console.print(welcome_panel)

def change_language(lang: str) -> None:
    """切换界面语言。

    参数：
        lang (str): 语言代码，支持 'en' 和 'zh'
    """
    global current_language
    if lang in LANGUAGES:
        current_language = LANGUAGES[lang]
        console.print(current_language['language_changed'])
    else:
        console.print("[red]Language not supported.[/red]")

def print_help() -> None:
    """显示帮助信息。

    打印所有可用的命令及其描述。
    """
    console.print("\n[bold cyan]可用命令:[/bold cyan]")
    for cmd, desc in COMMANDS.items():
        console.print(f"[yellow]{cmd:10}[/yellow] - {desc}")
    console.print()

def handle_user_input(user_input: str) -> bool:
    """处理用户输入的命令。

    处理特殊命令，如退出、清屏、显示历史记录等。

    参数：
        user_input (str): 用户输入的命令

    返回：
        bool: 
        - False: 用户要求退出程序
        - True: 命令已处理
    """
    if user_input.lower() == 'exit':
        console.print(f"[bold yellow]{current_language['exit_message']}[/bold yellow]")
        return False
    elif user_input.lower() == 'clear':
        console.clear()
        print_welcome_message()
        console.print(current_language['clear_message'])
        return True
    elif user_input.lower() == 'history':
        console.print(Panel("\n".join(chat_history), title=current_language['history_title'], expand=False))
        return True
    elif user_input.lower().startswith('lang '):
        _, lang_code = user_input.split(' ', 1)
        change_language(lang_code)
        return True
    elif user_input.lower() == 'help':
        print_help()
        return True
    return True

def print_response(response: str, elapsed_time: float) -> None:
    """打印 AI 的响应。

    格式化并打印 AI 的响应，包括响应时间和分隔线。

    参数：
        response (str): AI 的响应文本
        elapsed_time (float): 响应耗时（秒）
    """
    console.print("[bold blue]🤖 LLM: [/bold blue]")
    formatted_response = format_bold_text(response)
    # 按行分割并打印，移除多余的空行
    lines = [line.strip() for line in formatted_response.split('\n')]
    # 移除连续的空行
    filtered_lines = []
    prev_empty = False
    for line in lines:
        if line or not prev_empty:
            filtered_lines.append(line)
        prev_empty = not line
    
    # 打印处理后的行
    for line in filtered_lines:
        if line:
            console.print(line)
        else:
            print()

    # 显示响应时间
    console.print(current_language['response_time'].format(time=elapsed_time))

    # 打印分隔线，只在每次机器人的响应后加
    console.print("[dim]" + "─" * 50 + "[/dim]")

async def main() -> None:
    """主函数。

    实现主要的交互循环：
    1. 显示欢迎信息和帮助
    2. 创建 aiohttp 会话
    3. 进入交互循环：
        - 获取用户输入
        - 处理特殊命令
        - 调用 API 获取响应
        - 显示响应和计时
    4. 处理键盘中断和其他异常
    """
    print_welcome_message()
    print_help()  # 启动时显示帮助信息
    
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                # 使用 prompt_toolkit 获取用户输入，支持命令补全和历史记录
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: prompt_session.prompt(
                        "\n🔎 User: ",  # 使用普通字符串，移除 Rich 格式化
                        completer=command_completer,
                        complete_while_typing=True
                    )
                )
                
                # 处理空输入
                if not user_input.strip():
                    continue
                
                # 处理自定义命令
                if not handle_user_input(user_input):
                    break

                # 开始计时
                start_time = perf_counter()

                # 显示加载动画并调用 API 获取响应
                with Live(Spinner('dots', text=current_language['thinking']), console=console, refresh_per_second=10):
                    response = await get_response(session, user_input)
                
                # 结束计时并计算响应时间
                end_time = perf_counter()
                elapsed_time = end_time - start_time
                chat_history.append(f"User: {user_input}\nLLM: {response}")

                # 打印机器人的响应
                print_response(response, elapsed_time)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]按 Ctrl+C 再次退出程序[/yellow]")
                try:
                    await asyncio.sleep(1)
                except KeyboardInterrupt:
                    console.print(f"\n[bold yellow]{current_language['exit_message']}[/bold yellow]")
                    break
            except Exception as e:
                logging.error(f"发生错误: {str(e)}")
                console.print(f"[red]发生错误: {str(e)}[/red]")

if __name__ == "__main__":
    asyncio.run(main())