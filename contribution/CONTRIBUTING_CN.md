# Terminal-LLM 贡献指南

中文 | [English](CONTRIBUTING.md)

感谢你对 Terminal-LLM 项目的关注！本文档提供了参与项目开发的指南和工作流程。

## 开发环境

### 环境要求
- Python 3.8 或更高版本
- pip 包管理器
- Git

### 环境搭建
1. Fork 并克隆仓库：
```bash
git clone https://github.com/你的用户名/Terminal-LLM.git
cd Terminal-LLM
```

2. 以开发模式安装：
```bash
pip install -e .
```

3. 创建并配置 `.env`：
```bash
cp .env.example .env
# 编辑 .env 文件，添加你的 API 密钥
```

## 开发工作流

### 1. 分支策略
- `main`：稳定的生产代码
- `feature/*`：新功能（如 `feature/auto-complete`）
- `fix/*`：Bug 修复（如 `fix/connection-timeout`）
- `refactor/*`：代码重构
- `docs/*`：文档更新

示例：
```bash
# 创建新功能分支
git checkout -b feature/my-feature main

# 开发完成后
git checkout main
git merge feature/my-feature
git branch -d feature/my-feature
```

### 2. 提交规范
遵循 [约定式提交](https://www.conventionalcommits.org/zh-hans/) 规范：

- `feat:`：新功能
- `fix:`：Bug 修复
- `docs:`：文档变更
- `refactor:`：代码重构
- `test:`：添加或修改测试
- `style:`：代码格式调整
- `chore:`：维护任务

示例：
```bash
git commit -m "feat: 添加命令自动补全功能

- 实现命令的 Tab 补全
- 添加补全逻辑的测试
- 更新相关文档"
```

### 3. 代码风格
- 使用 [Black](https://github.com/psf/black) 进行代码格式化
- 遵循 [PEP 8](https://pep8.org/) 规范
- 最大行长度：88 字符
- 使用有意义的变量和函数名
- 为所有函数和类添加文档字符串

### 4. 项目结构
```
Terminal-LLM/
├── src/                    # 源代码
│   ├── core/              # 核心功能
│   ├── config/            # 配置管理
│   ├── data/              # 数据处理
│   └── ui/                # 用户界面
├── tests/                 # 测试文件
└── docs/                  # 文档
```

### 5. 测试
- 为新功能编写测试
- 修改代码时更新相关测试
- 提交前确保所有测试通过

```bash
# 运行测试
pytest

# 运行测试并显示覆盖率
pytest --cov=src
```

### 6. 文档
- 更新 README.md 和 README_EN.md
- 为新代码添加文档字符串
- 重要更改更新 CHANGELOG.md

### 7. Pull Request 流程
1. 创建新分支
2. 开发并测试更改
3. 更新文档
4. 提交 PR，包含：
   - 清晰的更改描述
   - 相关的 Issue
   - UI 更改的截图（如果有）
   - 测试结果

### 8. 版本控制
遵循 [语义化版本](https://semver.org/lang/zh-CN/)：
- 主版本.次版本.修订号
- 主版本：不兼容的 API 变更
- 次版本：新功能
- 修订号：Bug 修复

## 模块开发指南

### Core 模块
- 核心功能放在 `src/core/`
- 业务逻辑与 UI 分离
- API 调用使用 async/await
- 适当的异常处理

### Config 模块
- 配置存储在 `src/config/`
- 敏感数据使用环境变量
- 提供清晰的配置文档
- 包含配置值的验证

### Data 模块
- 数据处理实现在 `src/data/`
- 使用适当的缓存策略
- 安全的文件操作
- 实现proper错误处理

### UI 模块
- UI 代码保存在 `src/ui/`
- 使用 Rich 库组件
- 保持一致的样式
- 支持中英文

## 安全指南

1. API 密钥
- 永远不要提交 API 密钥
- 使用环境变量
- 文档说明所需的密钥

2. 依赖管理
- 保持依赖更新
- 检查安全漏洞
- 使用特定的版本号

## 支持

如果需要帮助：
- 创建 Issue
- 参与讨论
- 阅读文档

## 许可证

通过贡献，你同意你的贡献将在 MIT 许可证下发布。
