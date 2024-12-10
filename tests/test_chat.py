"""测试 Chat 模块的功能。

测试以下功能：
1. 命令处理
2. API 调用
3. 响应格式化
4. 错误处理
"""

import pytest
import asyncio
import aiohttp
import os
from unittest.mock import Mock, AsyncMock, patch
from Chat import (
    handle_user_input,
    get_response,
    print_response,
    format_bold_text,
    current_language,
    print_welcome_message,
    change_language,
    print_help,
    CACHE_ENABLED,
    LANGUAGES
)

# 禁用缓存
os.environ["ENABLE_CACHE"] = "false"

# 在每个测试开始前重置 current_language
@pytest.fixture(autouse=True)
def setup_language():
    global current_language
    current_language = LANGUAGES["zh"]
    yield

# 创建异步上下文管理器
class AsyncContextManager:
    def __init__(self, response):
        self.response = response

    async def __aenter__(self):
        return self.response

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

@pytest.mark.asyncio
async def test_handle_user_input():
    """测试用户输入处理功能。"""
    # 确保使用中文
    change_language("zh")
    
    # 测试退出命令
    assert handle_user_input("/quit") is False
    assert handle_user_input("/exit") is False
    assert handle_user_input("quit") is False
    assert handle_user_input("exit") is False
    
    # 测试清屏命令
    assert handle_user_input("/clear") is True
    assert handle_user_input("clear") is True
    
    # 测试帮助命令
    assert handle_user_input("/help") is True
    assert handle_user_input("help") is True
    
    # 测试语言切换命令
    assert handle_user_input("/lang en") is True
    assert handle_user_input("/lang zh") is True
    assert handle_user_input("lang en") is True
    assert handle_user_input("lang zh") is True
    
    # 测试无效命令
    assert handle_user_input("/invalid") is True
    
    # 测试普通文本输入
    assert handle_user_input("你好") is None

@pytest.mark.asyncio
async def test_get_response_success():
    """测试正常响应。"""
    # 确保使用中文
    change_language("zh")

    # 测试正常响应
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={
        "choices": [{"message": {"content": "你好👋！有什么可以帮助你的吗？"}}]
    })
    mock_session = AsyncMock()
    mock_session.post = AsyncMock(return_value=mock_response)
    response = await get_response(mock_session, "你好")
    assert "你好👋！" in response

@pytest.mark.asyncio
async def test_get_response_error():
    """测试错误响应。"""
    # 确保使用中文
    change_language("zh")

    # 测试错误状态码
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_response.json = AsyncMock(return_value={"error": "Internal Server Error"})
    mock_session = AsyncMock()
    mock_session.post = AsyncMock(side_effect=aiohttp.ClientError("Internal Server Error"))
    response = await get_response(mock_session, "你好")
    assert current_language["error_message"].format(error="Internal Server Error") in response

@pytest.mark.asyncio
async def test_error_handling():
    """测试错误处理功能。"""
    # 确保使用中文
    change_language("zh")

    # 测试网络超时
    mock_session = AsyncMock()
    mock_session.post.side_effect = asyncio.TimeoutError()
    response = await get_response(mock_session, "测试")
    assert current_language["timeout"] in response

    # 测试 HTTP 错误
    mock_session = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value={"error": "Not Found"})
    mock_session.post = AsyncMock(return_value=mock_response)
    response = await get_response(mock_session, "测试")
    assert current_language["error_message"].format(error="Not Found") in response

    # 测试 JSON 解析错误
    mock_session = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_session.post = AsyncMock(return_value=mock_response)
    response = await get_response(mock_session, "测试")
    assert current_language["error_message"].format(error="Invalid JSON response") in response

def test_print_response(capsys):
    """测试响应打印功能。"""
    # 确保使用中文
    change_language("zh")
    
    # 测试普通响应
    print_response("测试响应", 1.5)
    captured = capsys.readouterr()
    assert "测试响应" in captured.out
    assert "1.5" in captured.out
    
    # 测试带格式的响应
    print_response("**重要提示**", 0.5)
    captured = capsys.readouterr()
    assert "重要提示" in captured.out
    assert "0.5" in captured.out

def test_language_switching():
    """测试语言切换功能。"""
    # 测试切换到英文
    change_language("en")
    assert LANGUAGES["en"]["welcome"] == current_language["welcome"]

    # 测试切换到中文
    change_language("zh")
    assert LANGUAGES["zh"]["welcome"] == current_language["welcome"]

    # 测试无效语言
    with pytest.raises(KeyError):
        change_language("fr")

def test_welcome_message(capsys):
    """测试欢迎信息显示功能。"""
    change_language("zh")  # 确保使用中文
    print_welcome_message()
    captured = capsys.readouterr()
    assert LANGUAGES["zh"]["welcome"] in captured.out

def test_help_message(capsys):
    """测试帮助信息显示功能。"""
    change_language("zh")  # 确保使用中文
    print_help()
    captured = capsys.readouterr()
    assert "退出程序" in captured.out
    assert "清除屏幕" in captured.out
    assert "切换语言" in captured.out
    assert "显示帮助信息" in captured.out
    print_help()
    captured = capsys.readouterr()
    assert "退出程序" in captured.out
    assert "清除屏幕" in captured.out
    assert "切换语言" in captured.out
    assert "显示帮助信息" in captured.out
