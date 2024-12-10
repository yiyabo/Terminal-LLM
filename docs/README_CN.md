# Terminal-LLM

中文 | [English](README.md)

一个优雅的终端版 LLM 客户端，提供美观的界面和流畅的用户体验。

## 特性

- 🎨 精美的终端界面
  - 彩色动画和图标
  - 优雅的面板和边框
  - 格式化的文本显示
  - 自动换行和对齐

- 🚀 强大的功能
  - 智能缓存机制
  - 历史记录管理
  - 多语言支持（中英文）
  - 命令行补全

- ⌨️ 实用的命令
  - `/help` - 显示帮助信息
  - `/clear` - 清屏
  - `/history` - 查看历史记录
  - `/lang` - 切换语言
  - `/exit` 或 `/quit` - 退出程序

## 快速开始

### 环境要求
- Python 3.8 或更高版本
- pip 包管理器

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/Terminal-LLM.git
cd Terminal-LLM
```

2. 安装依赖：
```bash
pip install -e .
```

### 配置

1. 在项目根目录创建 `.env` 文件：
```bash
touch .env
```

2. 在 `.env` 文件中添加以下配置：
```env
CHATGLM_API_KEY=your-api-key-here
CHATGLM_API_URL=your-api-url-here  # 可选
CHATGLM_MODEL=your-model-name      # 可选
```

### 运行

```bash
python run.py
```

## 项目结构

```
Terminal-LLM/
├── src/                    # 源代码目录
│   ├── core/              # 核心功能
│   │   ├── chat.py       # 聊天功能
│   │   ├── commands.py   # 命令处理
│   │   └── shell_ai.py   # Shell AI
│   ├── config/           # 配置管理
│   │   └── config.py     # 配置定义
│   ├── data/             # 数据处理
│   │   └── cache.py      # 缓存管理
│   └── ui/               # 用户界面
│       └── ui.py         # UI 组件
├── data/                  # 数据文件
│   ├── cache/            # 缓存目录
│   ├── history/          # 历史记录
│   └── chat.log          # 日志文件
├── .env                   # 环境变量
├── .gitignore            # Git 忽略文件
├── README.md             # 说明文档
├── README_EN.md          # 英文说明
├── pytest.ini            # 测试配置
└── run.py                # 入口文件
```

## 开发

### 测试
```bash
pytest
```

### 代码风格
项目使用 Black 进行代码格式化：
```bash
black src/
```

## 贡献

欢迎提交 Pull Request 或创建 Issue！

## 许可证

[MIT License](LICENSE)