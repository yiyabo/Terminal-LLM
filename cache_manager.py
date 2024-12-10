"""简单的内存缓存管理器。

提供基本的缓存功能：
1. 设置缓存项
2. 获取缓存项
3. 删除缓存项
"""

import time
from typing import Dict, Any, Optional

class CacheManager:
    """简单的内存缓存管理器。
    
    使用字典存储缓存项，提供基本的缓存操作。
    每个缓存项包含值和过期时间。
    """
    
    def __init__(self, ttl: int = 3600):
        """初始化缓存管理器。
        
        Args:
            ttl: 缓存项的存活时间（秒），默认1小时
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
    
    def set(self, key: str, value: Any) -> None:
        """设置缓存项。
        
        Args:
            key: 缓存键
            value: 要缓存的值
        """
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string")
        
        if value is None:
            raise ValueError("Cache value cannot be None")
            
        self._cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存项。
        
        如果键不存在或已过期，返回 None。
        
        Args:
            key: 缓存键
            
        Returns:
            缓存的值或 None（如果不存在或已过期）
        """
        if not isinstance(key, str):
            raise TypeError("Cache key must be a string")
            
        item = self._cache.get(key)
        if not item:
            return None
            
        # 检查是否过期
        if time.time() - item['timestamp'] > self.ttl:
            del self._cache[key]
            return None
            
        return item['value']
    
    def remove(self, key: str) -> None:
        """删除缓存项。
        
        Args:
            key: 要删除的缓存键
        """
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """清空所有缓存项。"""
        self._cache.clear()
    
    def get_stats(self) -> Dict[str, int]:
        """获取缓存统计信息。
        
        Returns:
            包含统计信息的字典：
            - total_items: 总缓存项数
            - expired_items: 已过期的缓存项数
        """
        current_time = time.time()
        return {
            'total_items': len(self._cache),
            'expired_items': sum(
                1 for item in self._cache.values()
                if current_time - item['timestamp'] > self.ttl
            )
        }
