"""历史记录相关命令"""

from typing import Optional
from rich.panel import Panel
from rich.text import Text

from src.ui import console
from src.core.utils import ChatHistory
from src.core.commands import Command

class HistoryCommand(Command):
    """历史记录命令"""

    async def execute(self, *args, **kwargs) -> Optional[bool]:
        """执行历史记录命令

        用法: /history [数量]
        """
        # 获取历史记录
        history = ChatHistory()
        records = history.get_records()
        
        if not records:
            console.print("[yellow]暂无历史记录[/yellow]")
            return True

        # 确定要显示的记录数量
        try:
            limit = int(args[0]) if args else 10
        except (IndexError, ValueError):
            limit = 10

        # 准备显示文本
        text = Text()
        text.append(f"显示最近 {min(limit, len(records))} 条对话记录：\n\n")
        
        for i, record in enumerate(records[-limit:], 1):
            text.append(f"[bold blue]{i}. 用户:[/bold blue]\n")
            text.append(f"{record['user']}\n\n")
            text.append(f"[bold green]   回复:[/bold green]\n")
            text.append(f"{record['response']}\n\n")

        # 显示结果
        panel = Panel(
            text,
            title="历史记录",
            border_style="blue"
        )
        console.print(panel)
        return True
