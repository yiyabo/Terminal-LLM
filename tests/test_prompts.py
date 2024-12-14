"""提示词测试脚本"""

from src.core.prompt_manager import PromptManager

def main():
    """运行提示词测试"""
    
    # 创建测试用例
    test_cases = [
        # 编程场景测试
        "我的Python代码有一个bug，能帮我看看吗？",
        
        # 系统操作测试
        "如何在Linux系统中查看进程状态？",
        
        # 普通对话测试
        "今天天气真不错",
        
        # 错误处理测试
        "我的程序运行时报错了，怎么处理？",
        
        # 多场景混合测试
        "我在写一个Python程序来监控系统状态，遇到了一些问题"
    ]
    
    # 创建提示词管理器
    prompt_manager = PromptManager()
    
    # 运行测试
    prompt_manager.test_prompt_effectiveness(test_cases)

if __name__ == "__main__":
    main() 