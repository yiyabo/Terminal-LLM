"""测试命令模块。

测试命令模块的各个功能：
1. 命令工厂
2. 各种命令的执行
3. 语言切换
"""

import pytest
from unittest.mock import patch, MagicMock
from commands import (
    Command,
    ExitCommand,
    ClearCommand,
    HistoryCommand,
    LangCommand,
    HelpCommand,
    CommandFactory
)
from config import get_current_language, set_current_language, LANGUAGES

# 在每个测试开始前重置语言
@pytest.fixture(autouse=True)
def setup_language():
    set_current_language("zh")
    yield

def test_command_factory():
    """测试命令工厂。"""
    # 测试退出命令
    assert isinstance(CommandFactory.get_command("/quit"), ExitCommand)
    assert isinstance(CommandFactory.get_command("exit"), ExitCommand)
    
    # 测试清屏命令
    assert isinstance(CommandFactory.get_command("/clear"), ClearCommand)
    assert isinstance(CommandFactory.get_command("clear"), ClearCommand)
    
    # 测试历史记录命令
    assert isinstance(CommandFactory.get_command("/history"), HistoryCommand)
    assert isinstance(CommandFactory.get_command("history"), HistoryCommand)
    
    # 测试帮助命令
    assert isinstance(CommandFactory.get_command("/help"), HelpCommand)
    assert isinstance(CommandFactory.get_command("help"), HelpCommand)
    
    # 测试语言切换命令
    assert isinstance(CommandFactory.get_command("/lang en"), LangCommand)
    assert isinstance(CommandFactory.get_command("lang zh"), LangCommand)
    
    # 测试无效命令
    assert CommandFactory.get_command("invalid") is None

def test_exit_command():
    """测试退出命令。"""
    command = ExitCommand()
    assert command.execute() is False

def test_clear_command():
    """测试清屏命令。"""
    with patch('commands.console.clear') as mock_clear, \
         patch('commands.print_welcome') as mock_welcome:
        command = ClearCommand()
        assert command.execute() is True
        mock_clear.assert_called_once()
        mock_welcome.assert_called_once()

def test_history_command():
    """测试历史记录命令。"""
    mock_history = [
        {"user": "hello", "assistant": "hi"}
    ]
    with patch('commands.chat_history') as mock_chat_history:
        mock_chat_history.get_recent_history.return_value = mock_history
        command = HistoryCommand()
        assert command.execute() is True
        mock_chat_history.get_recent_history.assert_called_once()

def test_lang_command():
    """测试语言切换命令。"""
    command = LangCommand()
    
    # 测试切换到英文
    assert command.execute("en") is True
    assert get_current_language() == LANGUAGES["en"]
    
    # 测试切换到中文
    assert command.execute("zh") is True
    assert get_current_language() == LANGUAGES["zh"]
    
    # 测试无效语言
    assert command.execute("invalid") is True  # 命令执行成功，但语言未改变
    assert get_current_language() == LANGUAGES["zh"]

def test_help_command():
    """测试帮助命令。"""
    with patch('commands.print_help') as mock_help:
        command = HelpCommand()
        assert command.execute() is True
        mock_help.assert_called_once()
