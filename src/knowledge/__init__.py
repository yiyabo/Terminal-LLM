"""知识库管理模块

此模块提供文档处理和知识管理的核心功能。
"""

from .document import DocumentProcessor
from .vectorstore import VectorStore, SearchResult

__all__ = ['DocumentProcessor', 'VectorStore', 'SearchResult']
