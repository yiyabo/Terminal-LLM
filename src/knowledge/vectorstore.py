"""向量存储模块

提供文本向量化和向量检索功能。
"""

import os
import json
import numpy as np
import faiss
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from sentence_transformers import SentenceTransformer
from rich.console import Console
import torch

from .document import TextChunk

# 创建控制台对象
console = Console()

@dataclass
class SearchResult:
    """搜索结果数据类"""
    content: str
    metadata: dict
    score: float

class VectorStore:
    """向量存储类"""

    MODEL_NAME = 'all-MiniLM-L6-v2'

    def __init__(self, dimension: int = 384):  # all-MiniLM-L6-v2 模型的维度是 384
        """初始化向量存储

        Args:
            dimension: 向量维度
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # 使用 L2 距离的 FAISS 索引
        self.chunks: List[TextChunk] = []
        self.embeddings: List[np.ndarray] = []
        self._model = None  # 延迟初始化模型

    def _is_model_downloaded(self) -> bool:
        """检查模型是否已下载"""
        try:
            # 尝试加载模型配置，这不会下载模型
            SentenceTransformer(self.MODEL_NAME, device='cpu')
            return True
        except Exception:
            return False

    @property
    def model(self):
        """延迟加载模型"""
        if self._model is None:
            # 检查模型是否需要下载
            if not self._is_model_downloaded():
                console.print("\n[yellow]首次使用知识库功能，正在下载必要的 AI 模型（约 100MB），请稍候...[/yellow]")
                self._model = SentenceTransformer(self.MODEL_NAME)
                console.print("[green]模型下载完成！[/green]\n")
            else:
                # 模型已存在，直接加载
                self._model = SentenceTransformer(self.MODEL_NAME)
                
            # 设置设备
            if torch.backends.mps.is_available():
                self._model = self._model.to('mps')
            elif torch.cuda.is_available():
                self._model = self._model.to('cuda')
                
        return self._model

    async def get_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """获取文本的 embedding 向量

        Args:
            texts: 文本列表

        Returns:
            embedding 向量列表，如果失败则返回 None
        """
        try:
            # 使用 sentence-transformers 生成 embeddings，禁用进度条
            embeddings = self.model.encode(texts, show_progress_bar=False)
            return embeddings.tolist()
        except Exception as e:
            console.print(f"[red]Error getting embeddings: {e}[/red]")
            return None

    async def add_texts(self, chunks: List[TextChunk]) -> bool:
        """添加文本块到向量存储

        Args:
            chunks: 文本块列表

        Returns:
            是否成功添加
        """
        # 获取 embeddings
        texts = [chunk.content for chunk in chunks]
        embeddings = await self.get_embeddings(texts)
        if embeddings is None:
            return False

        # 添加到 FAISS 索引
        vectors = np.array(embeddings).astype('float32')
        self.index.add(vectors)

        # 保存文本块
        self.chunks.extend(chunks)
        self.embeddings.extend(vectors)

        return True

    async def search(self, query: str, top_k: int = 3) -> Optional[List[SearchResult]]:
        """搜索相似文本

        Args:
            query: 查询文本
            top_k: 返回结果数量

        Returns:
            搜索结果列表，如果失败则返回 None
        """
        # 获取查询文本的 embedding
        query_embedding = await self.get_embeddings([query])
        if query_embedding is None:
            return None

        # 搜索最相似的向量
        vector = np.array(query_embedding[0]).astype('float32').reshape(1, -1)
        distances, indices = self.index.search(vector, min(top_k, len(self.chunks)))

        # 构建结果
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx < len(self.chunks):  # 确保索引有效
                chunk = self.chunks[idx]
                results.append(SearchResult(
                    content=chunk.content,
                    metadata=chunk.metadata,
                    score=float(1 / (1 + distance))  # 将距离转换为相似度分数
                ))

        return results

    def save(self, directory: str):
        """保存向量存储到文件

        Args:
            directory: 保存目录
        """
        os.makedirs(directory, exist_ok=True)

        # 保存 FAISS 索引
        faiss.write_index(self.index, os.path.join(directory, "index.faiss"))

        # 保存文本块
        chunks_data = [asdict(chunk) for chunk in self.chunks]
        with open(os.path.join(directory, "chunks.json"), "w") as f:
            json.dump(chunks_data, f)

    def load(self, directory: str) -> bool:
        """从文件加载向量存储

        Args:
            directory: 加载目录

        Returns:
            是否成功加载
        """
        try:
            # 加载 FAISS 索引
            index_path = os.path.join(directory, "index.faiss")
            if os.path.exists(index_path):
                self.index = faiss.read_index(index_path)

            # 加载文本块
            chunks_path = os.path.join(directory, "chunks.json")
            if os.path.exists(chunks_path):
                with open(chunks_path, "r") as f:
                    chunks_data = json.load(f)
                self.chunks = [TextChunk(**data) for data in chunks_data]

            return True
        except Exception as e:
            console.print(f"[red]Error loading vector store: {e}[/red]")
            return False

    def clear(self):
        """清空向量存储"""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunks = []
        self.embeddings = []
