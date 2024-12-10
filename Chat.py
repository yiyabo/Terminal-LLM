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

作者：Yiyabo!
日期：2024-12-10
"""

#!/usr/bin/env python
import asyncio
import aiohttp
import time
import logging
from typing import Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import HTML

from config import (
    LANGUAGES,
    COMMANDS,
    API_KEY,
    API_URL,
    MODEL_NAME,
    MAX_RETRIES,
    RETRY_DELAY,
    REQUEST_TIMEOUT,
    CACHE_ENABLED,
    CACHE_FILE,
    HISTORY_FILE,
    get_current_language,
    set_current_language
)
from utils import ChatHistory, ResponseCache
from commands import (
    CommandFactory,
    LangCommand,
    ExitCommand,
    ClearCommand,
    HistoryCommand,
    HelpCommand
)
from ui import (
    console,
    thinking_spinner,
    print_welcome,
    print_response,
    print_error,
    print_retry,
    print_help
)

# 初始化全局变量
chat_history = ChatHistory(HISTORY_FILE)
response_cache = ResponseCache(CACHE_FILE)

# 初始化日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chat.log'),
        logging.StreamHandler()
    ]
)

command_completer = WordCompleter(list(COMMANDS.keys()), ignore_case=True)
prompt_session = PromptSession(history=InMemoryHistory())

def print_welcome_message() -> None:
    """打印欢迎信息。"""
    print_welcome()

def change_language(lang: str) -> None:
    """切换界面语言。

    测试多语言支持功能。

    参数：
        lang (str): 语言代码，支持 'en' 和 'zh'
        
    异常：
        KeyError: 当语言代码不受支持时抛出
    """
    set_current_language(lang)
    console.print(get_current_language()['language_changed'])

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
    # 获取命令对象
    command = CommandFactory.get_command(user_input)
    if command is None:
        return None
        
    # 如果是语言切换命令，需要提取语言代码
    if isinstance(command, LangCommand):
        _, lang_code = user_input.split(' ', 1)
        return command.execute(lang_code)
        
    return command.execute()

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
            return cached_response

    retry_count = 0

    while retry_count < MAX_RETRIES:
        try:
            with thinking_spinner():
                # 发送请求
                async with session.post(
                    API_URL,
                    json={
                        "model": MODEL_NAME,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    timeout=REQUEST_TIMEOUT
                ) as response:
                    # 检查响应状态
                    if response.status != 200:
                        error_msg = f"API returned {response.status}"
                        print_error(error_msg)
                        retry_count += 1
                        if retry_count < MAX_RETRIES:
                            print_retry(error_msg, retry_count, MAX_RETRIES)
                            await asyncio.sleep(RETRY_DELAY)
                        continue

                    # 解析响应
                    data = await response.json()
                    result = data['choices'][0]['message']['content']

                    # 缓存响应
                    if CACHE_ENABLED:
                        response_cache.cache_response(prompt, result)

                    return result

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            error_msg = str(e)
            print_error(error_msg)
            retry_count += 1
            if retry_count < MAX_RETRIES:
                print_retry(error_msg, retry_count, MAX_RETRIES)
                await asyncio.sleep(RETRY_DELAY)
            continue

    raise Exception(get_current_language()['timeout'])

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
                        HTML('\n<ansgreen><b>🔎 User: </b></ansgreen>'),
                        completer=command_completer,
                        complete_while_typing=True
                    )
                )
                
                # 处理空输入
                if not user_input.strip():
                    continue
                
                # 处理命令
                result = handle_user_input(user_input)
                if result is False:
                    break
                elif result is True:
                    continue

                # 记录开始时间
                start_time = time.perf_counter()

                # 获取 AI 响应
                response = await get_response(session, user_input)
                
                # 计算耗时
                elapsed_time = time.perf_counter() - start_time
                
                # 添加到历史记录
                chat_history.add_interaction(user_input, response)
                
                # 打印响应
                print_response(response, elapsed_time)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]按 Ctrl+C 再次退出程序[/yellow]")
                try:
                    await asyncio.sleep(1)
                except KeyboardInterrupt:
                    console.print(f"\n[bold yellow]{get_current_language()['exit_message']}[/bold yellow]")
                    break
            except Exception as e:
                logging.error(f"发生错误: {str(e)}")
                print_error(str(e))

if __name__ == "__main__":
    asyncio.run(main())