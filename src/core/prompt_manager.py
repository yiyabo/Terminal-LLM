"""提示词管理模块。

此模块负责管理和加载分层提示词，包括：
1. 基础层提示词：系统基本行为
2. 场景层提示词：特定场景的专业指令
3. 上下文层提示词：当前对话相关的临时指令

作者：Yiyabo!
日期：2024-12-10
"""

import os
from pathlib import Path
from typing import List, Optional


class PromptManager:
    """提示词管理器类"""

    def __init__(self, prompts_dir: str = "data/prompts"):
        """初始化提示词管理器。

        参数：
            prompts_dir (str): 提示词目录的路径
        """
        self.prompts_dir = Path(prompts_dir)
        self.base_dir = self.prompts_dir / "base"
        self.scene_dir = self.prompts_dir / "scene"
        self.context_dir = self.prompts_dir / "context"

    def load_prompt(self, file_path: Path) -> str:
        """加载单个提示词文件。

        参数：
            file_path (Path): 提示词文件路径

        返回：
            str: 提示词内容
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return ""

    def get_base_prompt(self) -> str:
        """获取基础系统提示词。

        返回：
            str: 基础系统提示词
        """
        return self.load_prompt(self.base_dir / "system.txt")

    def get_scene_prompt(self, scene: str) -> str:
        """获取特定场景的提示词。

        参数：
            scene (str): 场景名称（如 'coding', 'analysis' 等）

        返回：
            str: 场景提示词
        """
        return self.load_prompt(self.scene_dir / f"{scene}.txt")

    def detect_scene(self, user_input: str) -> Optional[str]:
        """检测用户输入属于哪个场景。

        参数：
            user_input (str): 用户输入

        返回：
            Optional[str]: 检测到的场景名称，如果没有检测到则返回 None
        """
        # 编程相关关键词
        coding_keywords = {
            "代码",
            "程序",
            "bug",
            "调试",
            "函数",
            "类",
            "变量",
            "报错",
            "python",
            "java",
            "javascript",
            "代码审查",
            "重构",
            "优化",
        }

        # 将用户输入转换为小写并分词
        words = set(user_input.lower().split())

        # 检测是否包含编程关键词
        if any(keyword in user_input.lower() for keyword in coding_keywords):
            return "coding"

        # 后续可以添加其他场景的检测逻辑
        return None

    def get_combined_prompt(self, user_input: str) -> str:
        """获取组合后的提示词。

        根据用户输入自动检测场景，并组合相应的提示词。

        参数：
            user_input (str): 用户输入

        返回：
            str: 组合后的提示词
        """
        prompts = []

        # 1. 添加基础提示词
        base_prompt = self.get_base_prompt()
        if base_prompt:
            prompts.append(base_prompt)

        # 2. 检测并添加场景提示词
        scene = self.detect_scene(user_input)
        if scene:
            scene_prompt = self.get_scene_prompt(scene)
            if scene_prompt:
                prompts.append(f"\n# 场景特定指令\n{scene_prompt}")

        # 3. 组合所有提示词
        return "\n\n".join(prompts)

    def test_prompt_effectiveness(self, test_inputs: List[str]) -> None:
        """测试提示词的效果。

        参数：
            test_inputs (List[str]): 测试输入列表
        """
        print("=== 提示词效果测试 ===\n")

        for test_input in test_inputs:
            print(f"测试输入: {test_input}")
            print("-" * 50)

            # 检测场景
            scene = self.detect_scene(test_input)
            print(f"检测到的场景: {scene if scene else '无特定场景'}")

            # 获取组合提示词
            combined_prompt = self.get_combined_prompt(test_input)
            print("\n组合后的提示词:")
            print("=" * 50)
            print(combined_prompt)
            print("=" * 50)
            print("\n" + "-" * 80 + "\n")
