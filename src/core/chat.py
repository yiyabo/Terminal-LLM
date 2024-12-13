"""终端应用程序测试模块。

此模块是 Terminal-LLM 终端应用程序的测试版本，用于验证和测试核心功能：
1. 异步通信：测试与 API 的异步交互
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
import logging
import time
from typing import Optional

import aiohttp
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory

from src.config import (
    API_KEY,
    API_URL,
    CACHE_FILE,
    COMMANDS,
    HISTORY_FILE,
    LOG_FILE,
    MODEL_NAME,
    get_current_language,
    set_current_language,
)
from src.core.commands import (
    CommandFactory,
)
from src.core.commands import vector_store  # 单独导入 vector_store
from src.core.utils import ChatHistory, ResponseCache
from src.ui import (
    console,
    print_error,
    print_help,
    print_response,
    print_welcome,
    thinking_spinner,
)
from src.core.exceptions import (
    APIError,
    NetworkError,
    RequestTimeoutError,
    ChatError,
)

# 初始化全局变量
chat_history = ChatHistory(HISTORY_FILE)
response_cache = ResponseCache(CACHE_FILE)

# 初始化日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

command_completer = WordCompleter(list(COMMANDS.keys()), ignore_case=True)
prompt_session = PromptSession(history=InMemoryHistory())


def print_welcome_message() -> None:
    """打印欢迎信息。"""
    print_welcome()


def change_language(lang: str) -> None:
    """切换界面语言。

    测试多语支持功能。

    参数：
        lang (str): 语言代码，支持 'en' 和 'zh'

    异常：
        KeyError: 当语言代码不受支持时抛出
    """
    set_current_language(lang)
    console.print(get_current_language()["language_changed"])


async def handle_user_input(user_input: str) -> Optional[bool]:
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

    # 获取命令参数
    command_parts = user_input[1:].split()
    args = command_parts[1:] if len(command_parts) > 1 else []

    # 执行命令
    return await command.execute(*args)


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
    async with thinking_spinner():
        # 从向量存储中检索相关文本
        relevant_texts = []
        if vector_store.index.ntotal > 0:  # 如果向量存储不为空
            results = await vector_store.search(prompt)
            if results:
                relevant_texts = [result.content for result in results]

        # 构建系统提示
        system_prompt = "你是一个有帮助的 AI 助手。"
        if relevant_texts:
            system_prompt += "\n\n相关上下文：\n" + "\n---\n".join(relevant_texts)

        # 构建请求数据
        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }

        # 发送请求
        try:
            async with session.post(
                API_URL, headers={"Authorization": f"Bearer {API_KEY}"}, json=data
            ) as response:
                if response.status != 200:
                    error_data = await response.json()
                    error_message = error_data.get("error", {}).get("message", "未知错误")
                    raise APIError(f"API 错误 ({response.status}): {error_message}")

                result = await response.json()
                return result["choices"][0]["message"]["content"]

        except aiohttp.ClientError as e:
            raise NetworkError(f"网络错误: {str(e)}") from e
        except asyncio.TimeoutError as e:
            raise RequestTimeoutError(f"请求超时: {str(e)}") from e
        except Exception as e:
            raise ChatError(f"发生错误: {str(e)}") from e


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
                        HTML("\n<ansgreen><b>🔎 User: </b></ansgreen>"),
                        completer=command_completer,
                        complete_while_typing=True,
                    ),
                )

                # 处理空输入
                if not user_input.strip():
                    continue

                # 如果是命令（以 / 开头），处理命令
                if user_input.startswith("/"):
                    result = await handle_user_input(user_input)
                    if result is False:
                        return  # 退出程序
                    continue  # 继续下次循环

                # 如果不是命令，发送给 AI
                start_time = time.perf_counter()
                response = await get_response(session, user_input)
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
                    console.print(
                        f"\n[bold yellow]{get_current_language()['exit_message']}[/bold yellow]"
                    )
                    return  # 退出程序
            except (NetworkError, RequestTimeoutError, APIError, ChatError) as e:
                logging.error("发生错误: %s", str(e))
                print_error(str(e))


if __name__ == "__main__":
    asyncio.run(main())
