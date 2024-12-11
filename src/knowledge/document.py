"""文档处理模块

提供文档加载、分割等基本功能。
"""

import os
from typing import List, Optional
from dataclasses import dataclass
import tiktoken

@dataclass
class TextChunk:
    """文本块数据类"""
    content: str
    metadata: dict

class DocumentProcessor:
    """文档处理器类"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """初始化文档处理器

        Args:
            chunk_size: 文本块大小（以 token 为单位）
            chunk_overlap: 文本块重叠大小（以 token 为单位）
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")  # 使用 GPT-4 的分词器

    def load_text(self, file_path: str) -> Optional[str]:
        """加载文本文件

        Args:
            file_path: 文件路径

        Returns:
            文件内容，如果文件不存在或不可读则返回 None
        """
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def split_text(self, text: str, metadata: dict = None) -> List[TextChunk]:
        """将文本分割成块

        Args:
            text: 要分割的文本
            metadata: 元数据字典

        Returns:
            文本块列表
        """
        if metadata is None:
            metadata = {}

        # 使用 tiktoken 进行分词
        tokens = self.encoding.encode(text)
        chunks = []
        
        # 分块
        i = 0
        while i < len(tokens):
            # 计算当前块的结束位置
            end = min(i + self.chunk_size, len(tokens))
            
            # 解码当前块
            chunk_tokens = tokens[i:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            # 创建文本块
            chunks.append(TextChunk(
                content=chunk_text,
                metadata=metadata.copy()
            ))
            
            # 移动到下一个位置，考虑重叠
            i += self.chunk_size - self.chunk_overlap
        
        return chunks

    def process_file(self, file_path: str) -> Optional[List[TextChunk]]:
        """处理单个文件

        Args:
            file_path: 文件路径

        Returns:
            文本块列表，如果处理失败则返回 None
        """
        # 加载文本
        text = self.load_text(file_path)
        if text is None:
            return None

        # 准备元数据
        metadata = {
            'source': file_path,
            'filename': os.path.basename(file_path)
        }

        # 分割文本
        chunks = self.split_text(text, metadata)
        return chunks
