"""知识库相关命令"""

import os
from typing import Optional
from rich.panel import Panel
from rich.text import Text

from src.ui import console
from src.knowledge import DocumentProcessor, VectorStore
from src.core.commands import Command

# 全局向量存储实例
vector_store = VectorStore()

class LoadCommand(Command):
    """加载文档命令"""

    async def execute(self, *args, **kwargs) -> Optional[bool]:
        """执行加载文档命令

        用法: /load [文件路径]
        """
        if not args:
            console.print("[red]请指定文件路径[/red]")
            return True

        file_path = args[0]
        processor = DocumentProcessor()
        chunks = processor.process_file(file_path)

        if chunks is None:
            console.print(f"[red]无法加载文件, 请检查文件路径: {file_path}[/red]")
            return True

        # 将文本块添加到向量存储
        success = await vector_store.add_texts(chunks)
        if not success:
            console.print("[red]无法将文档添加到向量存储[/red]")
            return True

        # 显示处理结果
        text = Text()
        text.append(f"成功加载文件: {file_path}\n")
        text.append(f"分割为 {len(chunks)} 个文本块\n\n")
        text.append("预览前3个文本块:\n")
        
        for i, chunk in enumerate(chunks[:3], 1):
            text.append(f"\n[bold]块 {i}:[/bold]\n")
            text.append(chunk.content[:200] + "...\n")

        panel = Panel(
            text,
            title="文档加载结果",
            border_style="green"
        )
        console.print(panel)

        # 保存向量存储
        vector_store.save("data/vectorstore")
        return True


class ClearCommand(Command):
    """清空知识库命令"""

    def execute(self, *args, **kwargs) -> Optional[bool]:
        """执行清空知识库命令

        用法: /clear
        """
        vector_store.clear()
        vector_store.save("data/vectorstore")
        console.print("[green]已清空知识库[/green]")
        return True
