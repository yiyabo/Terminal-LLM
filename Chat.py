"""ChatGLM 终端应用程序测试模块。

此模块是 ChatGLM 终端应用程序的测试版本，用于验证和测试核心功能：
1. 异步通信：测试与 ChatGLM API 的异步交互
2. 缓存机制：验证响应缓存的正确性
3. 历史记录：测试聊天历史的保存和加载
4. 错误处理：测试各种错误情况的处理逻辑
5. 用户界面：验证终端界面的交互体验

主要特点：
- 使用配置模块管理所有配置项
- 使用工具模块提供的功能类
- 完整的日志记录，包括文件和控制台输出
- 独立的测试环境，避免影响生产环境

依赖：
- asyncio：异步 IO 支持
- aiohttp：异步 HTTP 客户端
- rich：终端美化
- prompt_toolkit：命令行交互
- logging：日志记录
- config：配置模块
- utils：工具模块

使用方法：
    >>> python test.py

注意：
    此测试版本会创建独立的日志文件，不会影响主程序的运行。

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
import logging
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory

from config import *
from utils import ChatHistory, ResponseCache, format_bold_text
from typing import Optional

# 初始化日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chat.log'),
        logging.StreamHandler()
    ]
)

# 初始化组件
console = Console()
current_language = LANGUAGES["zh"]
command_completer = WordCompleter(list(COMMANDS.keys()), ignore_case=True)
prompt_session = PromptSession(history=InMemoryHistory())
chat_history = ChatHistory(HISTORY_FILE)
response_cache = ResponseCache(CACHE_FILE)

def print_welcome_message() -> None:
    """打印欢迎信息。

    使用 Rich 库创建一个居中的面板显示欢迎信息。
    测试终端界面的格式化和样式。
    """
    welcome_panel = Panel(Align.center(f"[bold cyan]{current_language['welcome']}[/bold cyan]"))
    console.print(welcome_panel)

def change_language(lang: str) -> None:
    """切换界面语言。

    测试多语言支持功能。

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

    测试命令系统和帮助文档显示。
    """
    console.print("\n[bold cyan]可用命令:[/bold cyan]")
    for cmd, desc in COMMANDS.items():
        console.print(f"[yellow]{cmd:10}[/yellow] - {desc}")
    console.print()

def handle_user_input(user_input: str) -> Optional[bool]:
    """处理用户输入的命令。

    测试命令处理系统，包括：
    - 退出命令
    - 清屏功能
    - 历史记录显示
    - 语言切换
    - 帮助系统

    参数：
        user_input (str): 用户输入的命令

    返回：
        Optional[bool]: 
        - False: 用户要求退出程序
        - True: 命令已处理完成（如清屏、显示历史等）
        - None: 输入的是普通文本，需要发送到 API 处理
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
        history = chat_history.get_recent_history()
        history_text = "\n".join([f"User: {h['user']}\nLLM: {h['assistant']}" for h in history])
        console.print(Panel(history_text, title=current_language['history_title'], expand=False))
        return True
    elif user_input.lower().startswith('lang '):
        _, lang_code = user_input.split(' ', 1)
        change_language(lang_code)
        return True
    elif user_input.lower() == 'help':
        print_help()
        return True
    return None

async def get_response(session: aiohttp.ClientSession, prompt: str) -> str:
    """异步获取 API 响应。

    测试 API 调用功能，包括：
    - 缓存机制
    - 错误处理
    - 重试逻辑
    - 响应解析

    参数：
        session (aiohttp.ClientSession): aiohttp 会话对象
        prompt (str): 用户输入的提示文本

    返回：
        str: API 的响应文本或缓存的响应

    异常：
        aiohttp.ClientError: HTTP 客户端错误
        asyncio.TimeoutError: 请求超时
    """
    # 检查缓存
    if CACHE_ENABLED:
        cached_response = response_cache.get_cached_response(prompt)
        if cached_response:
            logging.info("Using cached response")
            return cached_response

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    retries = 0
    while retries < MAX_RETRIES:
        try:
            async with session.post(API_URL, headers=headers, json=payload, timeout=REQUEST_TIMEOUT) as response:
                if response.status == 200:
                    response_data = await response.json()
                    response_text = response_data['choices'][0]['message']['content']
                    formatted_response = format_bold_text(response_text)
                    
                    # 缓存响应
                    if CACHE_ENABLED:
                        response_cache.cache_response(prompt, formatted_response)
                    
                    return formatted_response
                else:
                    error_message = current_language['error_message'].format(response.status)
                    console.print(f"[red]{error_message}[/red]")
                    logging.error(f"Received unexpected status code: {response.status}")
                    return "抱歉，服务器返回了错误状态码。"
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            retry_message = current_language['retry_message'].format(error=e, retry=retries + 1, max_retries=MAX_RETRIES)
            console.print(retry_message)
            logging.warning(retry_message)
            retries += 1
            if retries < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY)

    error_message = "抱歉，连接失败，请稍后再试。"
    console.print(f"[red]{error_message}[/red]")
    logging.error(error_message)
    return error_message

def print_response(response: str, elapsed_time: float) -> None:
    """打印 AI 的响应。

    测试响应格式化和显示功能，包括：
    - 文本格式化
    - 空行处理
    - 响应时间显示
    - 分隔线渲染

    参数：
        response (str): AI 的响应文本
        elapsed_time (float): 响应耗时（秒）
    """
    console.print("[bold blue]🤖 LLM: [/bold blue]")
    formatted_response = format_bold_text(response)
    
    # 处理多行响应，优化显示效果
    lines = [line.strip() for line in formatted_response.split('\n')]
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
    console.print("[dim]" + "─" * 50 + "[/dim]")

async def main() -> None:
    """主函数。

    测试整体功能的集成，包括：
    1. 组件初始化
    2. 用户输入处理
    3. API 调用流程
    4. 异常处理
    5. 程序退出逻辑

    异常：
        KeyboardInterrupt: 用户中断
        Exception: 其他未预期的错误
    """
    print_welcome_message()
    print_help()
    
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                # 获取用户输入
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: prompt_session.prompt(
                        "\n🔎 User: ",
                        completer=command_completer,
                        complete_while_typing=True
                    )
                )
                
                # 处理空输入
                if not user_input.strip():
                    continue
                
                # 处理特殊命令
                result = handle_user_input(user_input)
                if result is False:
                    break
                elif result is True:
                    continue

                # 记录开始时间
                start_time = perf_counter()

                # 获取响应
                with Live(Spinner('dots', text=current_language['thinking']), console=console, refresh_per_second=10):
                    response = await get_response(session, user_input)
                
                # 计算响应时间
                elapsed_time = perf_counter() - start_time
                
                # 保存对话记录
                chat_history.add_interaction(user_input, response)
                
                # 显示响应
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