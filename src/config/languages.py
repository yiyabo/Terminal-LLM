"""语言配置文件。

此模块定义了应用程序中使用的所有文本字符串的多语言版本。
目前支持中文和英文。
"""

LANGUAGES = {
    "zh": {
        "welcome": "✨ 欢迎使用终端版本 ChatGLM ✨",
        "help": """
可用命令:
/exit, exit   - 退出程序
/clear, clear - 清屏
/lang         - 切换语言 (/lang en/zh)
/help, help   - 显示帮助信息
""",
        "invalid_command": "无效的命令",
        "error": "抱歉，出现了一个错误：",
        "timeout": "请求超时，请稍后重试",
        "exit_message": "感谢使用，再见！",
        "language_changed": "已切换到中文",
        "clear_message": "屏幕已清空",
        "thinking": "思考中..."
    },
    "en": {
        "welcome": "✨ Welcome to Terminal ChatGLM ✨",
        "help": """
Available commands:
/exit, exit   - Exit program
/clear, clear - Clear screen
/lang         - Switch language (/lang en/zh)
/help, help   - Show help message
""",
        "invalid_command": "Invalid command",
        "error": "Sorry, an error occurred: ",
        "timeout": "Request timed out, please try again later",
        "exit_message": "Thanks for using! Goodbye!",
        "language_changed": "Switched to English",
        "clear_message": "Screen cleared",
        "thinking": "Thinking..."
    }
}
