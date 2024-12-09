# 更新日志

本文档记录 Terminal-LLM 的所有重要更新。

本更新日志格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增
- 精美的终端界面，包含彩色动画和图标
- 智能缓存机制，提升性能表现
- 多语言支持（中文和英文）
- 命令行自动补全功能
- 基础命令集（/help、/clear、/history、/lang、/exit）
- 开发工具配置：
  - EditorConfig 统一代码风格
  - Pre-commit 钩子进行代码质量检查
  - 代码格式化和检查工具集成
- 添加了 terminal-llm 命令的 CLI 入口点
- 添加了 src/cli.py 作为应用程序的主入口点

### 变更
- 优化项目结构，将配置、核心功能、数据和UI分离为独立模块
- 完善中英文文档
- 迁移到 Poetry 进行依赖管理
  - 添加 pyproject.toml 实现现代化的 Python 打包
  - 分离开发依赖和运行依赖
  - 移除 requirements.txt，改用 Poetry

### 修复
- 初始化设置和配置相关问题
- 包依赖管理问题

## [0.1.0] - 2024-12-11

### 新增
- Terminal-LLM 首次发布
- 核心 LLM 集成功能
- 基础终端用户界面
- 配置管理系统
- 命令历史记录功能
- 多语言支持框架
- 项目文档结构

### 安全性
- 安全的环境变量处理
- 基础输入验证

[未发布]: https://github.com/yourusername/Terminal-LLM/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/Terminal-LLM/releases/tag/v0.1.0
