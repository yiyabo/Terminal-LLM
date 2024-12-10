"""缓存管理器测试模块。

测试基本的缓存功能：
1. 设置和获取缓存项
2. 过期机制
3. 删除操作
4. 统计信息
"""

import pytest
import time
from cache_manager import CacheManager

def test_basic_operations():
    """测试基本的缓存操作。"""
    cache = CacheManager(ttl=1)  # 1秒后过期
    
    # 测试设置和获取
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"
    
    # 测试不存在的键
    assert cache.get("nonexistent_key") is None
    
    # 测试删除
    cache.remove("test_key")
    assert cache.get("test_key") is None

def test_expiration():
    """测试过期机制。"""
    cache = CacheManager(ttl=1)  # 1秒后过期
    
    # 设置测试数据
    cache.set("expire_key", "expire_value")
    
    # 立即获取应该存在
    assert cache.get("expire_key") == "expire_value"
    
    # 等待过期
    time.sleep(1.1)  # 稍微多等0.1秒确保过期
    
    # 再次获取应该为空
    assert cache.get("expire_key") is None

def test_error_handling():
    """测试错误处理。"""
    cache = CacheManager()
    
    # 测试设置 None 值
    with pytest.raises(ValueError):
        cache.set("error_key", None)
    
    # 测试设置非字符串键
    with pytest.raises(TypeError):
        cache.set(123, "value")  # type: ignore
    
    # 测试获取非字符串键
    with pytest.raises(TypeError):
        cache.get(123)  # type: ignore

def test_stats():
    """测试统计信息。"""
    cache = CacheManager(ttl=1)
    
    # 添加测试数据
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    
    # 检查总数
    stats = cache.get_stats()
    assert stats['total_items'] == 2
    assert stats['expired_items'] == 0
    
    # 等待过期
    time.sleep(1.1)
    
    # 检查过期数
    stats = cache.get_stats()
    assert stats['total_items'] == 2
    assert stats['expired_items'] == 2

def test_clear():
    """测试清空缓存。"""
    cache = CacheManager()
    
    # 添加测试数据
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    
    # 验证数据已添加
    stats = cache.get_stats()
    assert stats['total_items'] == 2
    
    # 清空缓存
    cache.clear()
    
    # 验证缓存已清空
    stats = cache.get_stats()
    assert stats['total_items'] == 0
