"""对话测试脚本"""

import asyncio
import aiohttp
from src.core.chat import get_response
from src.core.prompt_manager import PromptManager

async def test_conversation():
    """测试连续对话场景"""
    
    # 测试对话序列
    conversation = [
        # 测试思考过程和初始理解
        "我想开发一个Python程序来监控系统性能，你能帮我吗？",
        
        # 测试上下文连贯性
        "这个程序需要哪些主要功能？",
        
        # 测试场景深度调整
        "具体怎么实现CPU使用率的监控？",
        
        # 测试错误处理和专业性
        "如果监控数据异常该怎么处理？",
        
        # 测试知识整合
        "你能总结一下我们刚才讨论的要点吗？"
    ]
    
    print("=== 连续对话测试 ===\n")
    
    async with aiohttp.ClientSession() as session:
        for i, user_input in enumerate(conversation, 1):
            print(f"\n=== 对话轮次 {i} ===")
            print(f"用户: {user_input}")
            print("-" * 50)
            
            try:
                response = await get_response(session, user_input)
                print(f"AI: {response}")
                print("=" * 80)
                
                # 等待一下，模拟真实对话节奏
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"错误: {str(e)}")
                break

async def main():
    """主函数"""
    await test_conversation()

if __name__ == "__main__":
    asyncio.run(main()) 