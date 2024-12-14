"""终端 LLM 聊天模块。

此模块实现了终端 LLM 的核心聊天功能，包括：
1. 命令处理：处理用户输入的各种命令
2. API 调用：与 LLM API 的异步交互
3. 流式响应：实现流式文本生成
4. 错误处理：处理网络、API 等各类错误
5. 历史记录：管理聊天历史

作者：Yiyabo!
日期：2024-12-10
"""

import asyncio
import logging
import time
from typing import Optional

import aiohttp
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import Style

from src.config import (
    API_KEY,
    API_URL,
    CACHE_FILE,
    CHUNK_SIZE,
    COMMANDS,
    HISTORY_FILE,
    LOG_FILE,
    MODEL_TYPE,
    REQUEST_TIMEOUT,
    STREAM_BUFFER_SIZE,
    get_current_language,
    set_current_language,
)
from src.core.commands import CommandFactory, vector_store
from src.core.exceptions import APIError, ChatError, NetworkError, RequestTimeoutError
from src.core.model_adapter import Message, get_model_adapter
from src.core.prompt_manager import PromptManager
from src.core.utils import ChatHistory, ResponseCache
from src.ui import StreamingPanel, console, print_error, print_help, print_welcome

# 定义样式
style = Style.from_dict(
    {
        "command": "#ansiyellow bold",
        "bottom-toolbar": "#ansibrightblack",
        "bottom-toolbar.text": "#ansiwhite",
        "bottom-toolbar.key": "#ansiyellow",
        "completion-menu.completion": "bg:#008888 #ffffff",
        "completion-menu.completion.current": "bg:#00aaaa #000000",
        "completion-menu.meta.completion": "bg:#444444 #ffffff",
        "completion-menu.meta.completion.current": "bg:#666666 #ffffff",
    }
)

# 初始化全局变量
chat_history = ChatHistory(HISTORY_FILE)
response_cache = ResponseCache(CACHE_FILE)
prompt_manager = PromptManager()

# 初始化日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)


class CommandCompleter(Completer):
    """自定义命令补全器"""

    def __init__(self, commands):
        """初始化命令补全器。

        参数:
            commands: 命令字典，键为命令名，值为命令描述
        """
        self.commands = commands

    def get_completions(self, document: Document, complete_event):
        """获取补全建议。

        参数:
            document: 当前文档对象
            complete_event: 补全事件对象

        返回:
            生成器，产生 Completion 对象
        """
        # 只在输入 / 后触发
        if document.text.startswith("/"):
            word = document.text[1:]  # 去掉 / 前缀
            for command, description in self.commands.items():
                if command[1:].startswith(word.lower()):  # 不区分大小写的比较
                    yield Completion(
                        text=command,  # 使用完整命令（包含/）
                        start_position=-len(document.text),  # 从开头替换整个输入
                        display=command,
                        display_meta=description,
                        style="class:command",
                    )


# 创建自定义补全器
command_completer = CommandCompleter(COMMANDS)

# 创建按键绑定
kb = KeyBindings()


@kb.add("tab")
def _(event):
    """处理 Tab 键。

    参数:
        event: 按键事件对象
    """
    buff = event.current_buffer
    # 如果当前有补全菜单
    if buff.complete_state:
        buff.complete_next()
    else:
        buff.start_completion(select_first=False)


@kb.add("enter")
def _(event):
    """处理 Enter 键。

    参数:
        event: 按键事件对象
    """
    buff = event.current_buffer
    # 如果有补全菜单打开，就接受补全但不提交
    if buff.complete_state:
        buff.complete_state = None
    # 否则正常提交
    else:
        buff.validate_and_handle()


# 创建 prompt session
prompt_session = PromptSession(
    history=InMemoryHistory(),
    completer=command_completer,
    enable_history_search=True,
    complete_style=CompleteStyle.COLUMN,  # 改为垂直列表
    mouse_support=False,  # 禁用鼠标支持以保持文本选择功能
    bottom_toolbar=HTML("<b>提示：</b> 输入 / 后按 Tab 显示命令列表，使用 ↑↓ 键选择"),
    style=style,
    complete_in_thread=True,  # 在线程中运行补全，避免阻塞
    auto_suggest=None,  # 禁用自动建议
    enable_system_prompt=False,  # 禁用系统提示
    enable_suspend=True,  # 启用挂起功能
    reserve_space_for_menu=4,  # 为菜单保留空间
    complete_while_typing=False,  # 禁用输入时的补全
    key_bindings=kb,  # 使用自定义按键绑定
)


def print_welcome_message() -> None:
    """打印欢迎信息。"""
    print_welcome()


def change_language(lang: str) -> None:
    """切换界面语言。

    参数：
        lang (str): 语言代码，支持 'en' 和 'zh'

    异常：
        KeyError: 当语言代码不受支持时抛出
    """
    set_current_language(lang)
    console.print(get_current_language()["language_changed"])


async def handle_user_input(user_input: str) -> Optional[bool]:
    """处理用户输入的命令。

    参数：
        user_input (str): 用户输入的命令

    返回：
        Optional[bool]:
        - False: 用户请求退出
        - True: 命令执行完成
        - None: 不是命令，需要发送到 API
    """
    command = CommandFactory.get_command(user_input)
    if command is None:
        return None

    command_parts = user_input[1:].split()
    args = command_parts[1:] if len(command_parts) > 1 else []

    return await command.execute(*args)


async def get_response(session: aiohttp.ClientSession, prompt: str) -> str:
    """获取 API 响应。

    参数��
        session (aiohttp.ClientSession): aiohttp 会话对象
        prompt (str): 用户输入的提示文本

    返回：
        str: API 的完整响应文本

    异常：
        NetworkError: 网络连接错误
        RequestTimeoutError: 请求超时
        APIError: API 调用错误
        ChatError: 其他错误
    """
    # 获取最近5次对话历史
    recent_history = chat_history.get_recent_history(5)

    # 检索相关文本
    relevant_texts = []
    if vector_store.index.ntotal > 0:
        results = await vector_store.search(prompt)
        if results:
            relevant_texts = [result.content for result in results]

    # 获取组合后的系统提示词
    system_prompt = prompt_manager.get_combined_prompt(prompt)
    if relevant_texts:
        system_prompt += "\n\n相关上下文：\n" + "\n---\n".join(relevant_texts)

    # 获取对应的模型适配器
    adapter = get_model_adapter(MODEL_TYPE, API_KEY, API_URL)

    # 构建消息列表
    messages = [Message(role="system", content=system_prompt)]

    # 添加历史对话
    for history_item in recent_history:
        messages.extend(
            [
                Message(role="user", content=history_item["user"]),
                Message(role="assistant", content=history_item["assistant"]),
            ]
        )

    # 添加当前用户输入
    messages.append(Message(role="user", content=prompt))

    # 构建请求数据
    data = adapter.format_request(messages, stream=True)

    try:
        async with session.post(
            adapter.api_url,
            headers=adapter.get_headers(),
            json=data,
            timeout=REQUEST_TIMEOUT,
            chunked=True,  # Enable chunked transfer
            read_bufsize=CHUNK_SIZE,  # Use optimized chunk size
        ) as response:
            if response.status != 200:
                error_data = await response.json()
                error_msg = error_data.get("error", {}).get("message", "未知错误")
                raise APIError(f"API 错误 ({response.status}): {error_msg}")

            # 使用流式响应面板
            with StreamingPanel() as panel:
                buffer = []
                async for line in response.content:
                    if line:
                        try:
                            line_text = line.decode("utf-8").strip()
                            content = await adapter.parse_stream_line(line_text)
                            if content:
                                buffer.append(content)
                                # 当缓冲区达到一定大小时才更新UI
                                if len(buffer) >= STREAM_BUFFER_SIZE:
                                    panel.update("".join(buffer))
                                    buffer = []
                        except UnicodeDecodeError:
                            continue

                # 确保最后的缓冲区内容也被显示
                if buffer:
                    panel.update("".join(buffer))

                return panel.get_response()

    except aiohttp.ClientError as e:
        raise NetworkError(f"网络错误: {str(e)}") from e
    except asyncio.TimeoutError as e:
        raise RequestTimeoutError(f"请求超时: {str(e)}") from e
    except Exception as e:
        raise ChatError(f"发生错误: {str(e)}") from e


async def main() -> None:
    """主程序入口。

    主要功能：
    1. 初始化环境
    2. 处理用户输入
    3. 调用 API
    4. 错误处理
    5. 优雅退出
    """
    print_welcome_message()
    print_help()

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                # 获取用户输入
                user_input = await prompt_session.prompt_async(
                    HTML("\n<ansgreen><b>🔎 User: </b></ansgreen>"),
                )

                # 处理空输入
                if not user_input.strip():
                    continue

                # 处理命令
                if user_input.startswith("/"):
                    result = await handle_user_input(user_input)
                    if result is False:
                        return
                    continue

                # 调用 API
                start_time = time.perf_counter()
                response = await get_response(session, user_input)
                elapsed_time = time.perf_counter() - start_time

                # 保存历史记录
                chat_history.add_interaction(user_input, response)

                # 显示响应时间
                console.print(f"\n[dim]响应时间: {elapsed_time:.2f} 秒[/dim]")

            except KeyboardInterrupt:
                console.print("\n[yellow]按 Ctrl+C 再次退出程序[/yellow]")
                try:
                    await asyncio.sleep(1)
                except KeyboardInterrupt:
                    msg = get_current_language()["exit_message"]
                    console.print(f"\n[bold yellow]{msg}[/bold yellow]")
                    return

            except (NetworkError, RequestTimeoutError, APIError, ChatError) as e:
                logging.error("发生错误: %s", str(e))
                print_error(str(e))


if __name__ == "__main__":
    asyncio.run(main())
