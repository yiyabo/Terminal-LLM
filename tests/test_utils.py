"""测试 utils 模块的功能。

测试以下组件：
1. ChatHistory：对话历史管理
2. ResponseCache：响应缓存管理
3. format_bold_text：文本格式化
"""

import pytest
import os
import json
from utils import ChatHistory, ResponseCache, format_bold_text

# ChatHistory 测试
def test_chat_history():
    """测试对话历史管理功能。"""
    # 设置测试文件
    test_file = "test_history.json"
    
    # 确保测试开始时文件不存在
    if os.path.exists(test_file):
        os.remove(test_file)
    
    try:
        # 创建新的历史管理器
        history = ChatHistory(test_file)
        
        # 测试添加对话
        history.add_interaction("你好", "你好！很高兴见到你。")
        history.add_interaction("今天天气如何？", "今天是晴天。")
        
        # 测试获取最近历史
        recent = history.get_recent_history(1)
        assert len(recent) == 1
        assert recent[0]["user"] == "今天天气如何？"
        assert recent[0]["assistant"] == "今天是晴天。"
        
        # 测试获取所有历史
        all_history = history.get_recent_history(10)
        assert len(all_history) == 2
        
        # 测试清空历史
        history.clear_history()
        assert len(history.get_recent_history(10)) == 0
        
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

# ResponseCache 测试
def test_response_cache():
    """测试响应缓存管理功能。"""
    # 设置测试文件
    test_file = "test_cache.json"
    
    # 确保测试开始时文件不存在
    if os.path.exists(test_file):
        os.remove(test_file)
    
    try:
        # 创建新的缓存管理器
        cache = ResponseCache(test_file)
        
        # 测试缓存新响应
        test_prompt = "你好"
        test_response = "你好！很高兴见到你。"
        cache.cache_response(test_prompt, test_response)
        
        # 测试获取缓存的响应
        cached = cache.get_cached_response(test_prompt)
        assert cached == test_response
        
        # 测试获取不存在的缓存
        assert cache.get_cached_response("不存在的提示") is None
        
        # 测试缓存持久化
        cache2 = ResponseCache(test_file)
        assert cache2.get_cached_response(test_prompt) == test_response
        
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

# format_bold_text 测试
def test_format_bold_text():
    """测试文本格式化功能。"""
    # 测试加粗格式
    assert format_bold_text("**重要提示**") == "[bold cyan]重要提示[/bold cyan]"
    
    # 测试列表格式
    assert format_bold_text("- 第一项") == "• 第一项"
    assert format_bold_text("- 第一项\n- 第二项") == "• 第一项\n• 第二项"
    
    # 测试混合格式
    mixed_text = "**标题**\n- 第一项\n- 第二项"
    expected = "[bold cyan]标题[/bold cyan]\n• 第一项\n• 第二项"
    assert format_bold_text(mixed_text) == expected
    
    # 测试普通文本
    normal_text = "这是普通文本"
    assert format_bold_text(normal_text) == normal_text
