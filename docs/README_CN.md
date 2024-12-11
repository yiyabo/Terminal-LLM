# Terminal-LLM

中文 | [English](README.md)

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-package-blue.svg)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

一个优雅的终端 LLM 客户端，提供美观的界面和流畅的用户体验。

## ✨ 特性亮点

### 🎨 精美的终端界面
- **动态反馈**：优雅的加载动画，让等待不再枯燥
- **智能排版**：自动格式化代码、链接和重要信息
- **丰富图标**：使用 Unicode 图标增强视觉体验
- **自适应布局**：完美适配不同终端窗口大小

### 🧠 智能对话
- **本地向量存储**：基于 FAISS 的高性能向量数据库
- **文档智能处理**：自动分块和向量化，支持长文本理解
- **上下文感知**：智能管理对话历史
- **多语言支持**：中英文无缝切换

### ⚡ 强大功能
- **命令自动补全**：智能提示可用命令和参数
- **历史记录管理**：便捷访问对话历史
- **异步处理**：高效处理并发请求
- **错误恢复**：智能处理异常情况

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Poetry 包管理器

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/Terminal-LLM.git
cd Terminal-LLM
```

2. 安装 Poetry（如果尚未安装）：
```bash
pip install poetry
```

3. 使用 Poetry 安装项目：
```bash
poetry install
```

### 使用方法

安装完成后，你可以通过以下两种方式启动应用：

1. 使用 Poetry：
   ```bash
   poetry run terminal-llm
   ```

2. 先激活虚拟环境：
   ```bash
   poetry shell
   terminal-llm
   ```

### 配置

1. 在项目根目录创建 `.env` 文件：
```bash
cp .env.example .env
```

2. 在 `.env` 文件中添加配置：
```env
CHATGLM_API_KEY=你的API密钥
CHATGLM_API_URL=你的API地址  # 可选
CHATGLM_MODEL=模型名称      # 可选
```

## 🎯 核心命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `/help` | 显示帮助信息 | `/help` |
| `/load` | 加载知识文档 | `/load docs/example.txt` |
| `/clear` | 清空对话历史 | `/clear` |
| `/history` | 查看历史记录 | `/history` |
| `/lang` | 切换界面语言 | `/lang en` |
| `/exit` | 退出程序 | `/exit` |

## 📚 项目结构

```
Terminal-LLM/
├── src/                    # 源代码目录
│   ├── core/              # 核心功能
│   │   ├── chat.py       # 对话功能
│   │   └── commands/     # 命令处理
│   ├── knowledge/        # 知识处理
│   │   ├── document.py   # 文档处理
│   │   └── vectorstore.py# 向量存储
│   └── ui/               # 用户界面
│       └── ui.py         # UI 组件
└── docs/                  # 文档
    ├── README.md         # 英文文档
    └── README_CN.md      # 中文文档
```

## 🤝 参与贡献

我们欢迎各种形式的贡献！请参阅我们的[贡献指南](contribution/CONTRIBUTING_CN.md)。

## 📄 开源协议

本项目采用 MIT 协议开源 - 查看 [LICENSE](../LICENSE) 文件了解详情。