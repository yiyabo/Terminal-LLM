from pathlib import Path

def load_prompt(file_path: Path) -> str:
    """加载提示词文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def main():
    """测试提示词效果"""
    # 测试基础提示词
    base_prompt = load_prompt(Path("data/prompts/base/system.txt"))
    print("=== 基础提示词 ===")
    print(base_prompt)
    print("\n" + "=" * 80 + "\n")
    
    # 测试编程场景提示词
    coding_prompt = load_prompt(Path("data/prompts/scene/coding.txt"))
    print("=== 编程场景提示词 ===")
    print(coding_prompt)
    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    main() 