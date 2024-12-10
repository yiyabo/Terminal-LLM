"""Shell AI 自然语言命令转换器。

此模块实现了一个基于自然语言的 Shell 命令助手，主要功能包括：
1. 自然语言转换：将用户的自然语言描述转换为对应的 Shell 命令
2. 命令确认：在执行前让用户确认或编辑生成的命令
3. 命令执行：安全地执行确认后的命令并显示结果
4. 历史记录：保存用户的操作历史
5. 错误处理：优雅地处理各种异常情况

主要特点：
- 使用 ChatGLM API 进行自然语言处理
- 支持命令编辑和确认机制
- 保存命令历史到用户主目录
- 美化的终端界面
- 完整的错误处理

依赖：
- os：系统操作
- sys：系统功能
- asyncio：异步 IO 支持
- aiohttp：异步 HTTP 客户端
- prompt_toolkit：命令行交互
- rich：终端美化

使用方法：
    >>> python shell_ai.py
    🤖 > 帮我找出最大的文件
    Suggested command: ls -lhS | head -n 5
    Execute this command? (y/n/edit):

注意：
    1. 需要设置正确的 API 密钥
    2. 某些命令可能需要特定的权限
    3. 使用 Ctrl+C 取消当前操作
    4. 使用 Ctrl+D 或输入 'exit' 退出程序

作者：Yiyabo!
日期：2024-12-10
"""

#!/usr/bin/env python
import os
import sys
import asyncio
import aiohttp
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.panel import Panel
from typing import Optional
from config import API_KEY, API_URL, MODEL_NAME, REQUEST_TIMEOUT

console = Console()

class ShellAI:
    """Shell AI 命令转换器类。

    此类负责将自然语言转换为 Shell 命令，并提供命令执行环境。
    包含命令转换、确认、执行和历史记录等功能。

    属性：
        history_file (str): 历史记录文件的路径
        session (PromptSession): prompt_toolkit 会话对象

    示例：
        >>> shell_ai = ShellAI()
        >>> await shell_ai.run()
    """

    def __init__(self):
        """初始化 Shell AI。

        设置历史文件路径和创建 prompt_toolkit 会话。
        历史文件保存在用户主目录下。
        """
        self.history_file = os.path.expanduser('~/.shell_ai_history')
        self.session = PromptSession(
            history=FileHistory(self.history_file)
        )
        
    async def get_llm_response(self, prompt: str) -> str:
        """获取 LLM API 响应。

        向 ChatGLM API 发送请求并获取响应。

        参数：
            prompt (str): 要发送给 API 的提示文本

        返回：
            str: API 的响应文本

        异常：
            Exception: API 调用失败时抛出
        """
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
        
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, 
                                headers=headers, 
                                json=payload,
                                timeout=REQUEST_TIMEOUT) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data['choices'][0]['message']['content']
                else:
                    raise Exception(f"API error: {response.status}")

    async def process_natural_language(self, user_input: str) -> Optional[str]:
        """处理自然语言输入并转换为命令。

        将用户的自然语言描述转换为可执行的 Shell 命令。
        包含详细的转换规则和安全检查。

        参数：
            user_input (str): 用户的自然语言输入

        返回：
            Optional[str]: 转换后的 Shell 命令，如果转换失败则返回 None
        """
        prompt = f"""
        请将以下自然语言请求转换为对应的shell命令：
        '{user_input}'
        
        要求：
        1. 只返回具体的命令，不要包含任何解释或其他文字
        2. 确保命令是安全的
        3. 如果需要多个命令，用分号分隔
        4. 如果无法转换或不确定，返回 'UNABLE_TO_CONVERT'
        5. 对于查找最大文件的需求，使用 ls -lhS 或 du -sh * 等命令
        6. 对于查找特定类型文件的需求，结合 find 和 grep 命令
        7. 优先使用通用的 Unix/Linux 命令
        8. 如果涉及到目录切换，确保使用正确的相对或绝对路径
        
        示例输入和输出：
        输入：'帮我找出最大的文件'
        输出：'ls -lhS | head -n 5'
        
        输入：'显示所有的 Python 文件'
        输出：'find . -name "*.py"'
        """
        
        try:
            command = await self.get_llm_response(prompt)
            return command.strip()
        except Exception as e:
            console.print(f"[red]Error converting to command: {e}[/red]")
            return None

    async def prompt_for_confirmation(self, command: str) -> Optional[str]:
        """提示用户确认命令。

        显示生成的命令并让用户选择确认、编辑或取消。

        参数：
            command (str): 要确认的命令

        返回：
            Optional[str]: 确认后的命令（可能被编辑），如果用户取消则返回 None
        """
        console.print(Panel(f"[yellow]Suggested command:[/yellow] {command}"))
        response = await self.session.prompt_async("Execute this command? (y/n/edit): ")
        
        if response.lower() == 'y':
            return command
        elif response.lower() == 'edit':
            edited_command = await self.session.prompt_async("Edit command: ", default=command)
            return edited_command
        return None

    async def execute_command(self, command: str) -> Optional[int]:
        """执行 Shell 命令。

        安全地执行 Shell 命令并处理其输出。
        支持特殊命令（如 clear）的处理。

        参数：
            command (str): 要执行的 Shell 命令

        返回：
            Optional[int]: 命令的返回码（0 表示成功），如果执行失败则返回 None

        异常：
            Exception: 命令执行失败时抛出
        """
        try:
            # 对特殊命令进行处理
            if command.strip() == 'clear':
                console.clear()
                return 0
                
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True,  # 确保在shell环境中执行
                executable='/bin/bash'  # 使用bash作为shell
            )
            stdout, stderr = await process.communicate()
            
            if stdout:
                # 处理输出中的控制字符
                output = stdout.decode()
                if not any(control in output for control in ['[H', '[2J', '[3J']):
                    console.print(output.rstrip())
            if stderr:
                console.print(f"[red]{stderr.decode().rstrip()}[/red]")
                
            return process.returncode
        except Exception as e:
            console.print(f"[red]Error executing command: {e}[/red]")
            return None

    async def run(self) -> None:
        """运行主循环。

        实现主要的交互循环：
        1. 显示欢迎信息
        2. 获取用户输入
        3. 处理特殊命令（exit、clear）
        4. 转换自然语言为命令
        5. 确认和执行命令
        6. 错误处理

        异常：
            KeyboardInterrupt: 用户中断（Ctrl+C）
            EOFError: 用户退出（Ctrl+D）
            Exception: 其他未预期的错误
        """
        console.print("[bold cyan]✨ Welcome to Shell AI - Your Natural Language Shell Assistant ✨[/bold cyan]")
        console.print("[green]Type 'exit' to quit, 'clear' to clear screen[/green]")
        
        while True:
            try:
                # 获取用户输入
                user_input = await self.session.prompt_async("🤖 > ")
                
                # 处理退出命令
                if user_input.lower() in ['exit', 'quit']:
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break
                elif user_input.lower() == 'clear':
                    console.clear()
                    continue
                
                # 处理自然语言输入
                command = await self.process_natural_language(user_input)
                if command and command != 'UNABLE_TO_CONVERT':
                    confirmed_command = await self.prompt_for_confirmation(command)
                    if confirmed_command:
                        await self.execute_command(confirmed_command)
                else:
                    console.print("[red]Sorry, I couldn't convert that to a command.[/red]")
                    
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

def main() -> None:
    """程序入口函数。

    创建 Shell AI 实例并运行主循环。
    处理顶级异常并确保优雅退出。

    异常：
        Exception: 捕获所有未处理的异常
    """
    try:
        shell_ai = ShellAI()
        asyncio.run(shell_ai.run())
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
