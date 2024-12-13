"""
Terminal-LLM 的自定义异常类模块。

这个模块包含了系统中使用的所有自定义异常类。
"""

class APIError(Exception):
    """API 调用相关的异常"""

class NetworkError(Exception):
    """网络相关的异常"""

class RequestTimeoutError(Exception):
    """请求超时异常"""

class ChatError(Exception):
    """聊天系统通用异常""" 