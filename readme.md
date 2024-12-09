# ChatGLM 终端助手

基于 ChatGLM API 的智能终端助手，提供自然语言对话和 Shell 命令解释功能。项目采用异步编程模型，支持多语言切换，并具有完善的错误处理机制。

## ✨ 主要特性

### 🤖 聊天助手 (Chat.py)
- **多语言支持**：无缝切换中英文界面
- **异步处理**：基于 `asyncio` 的高性能异步通信
- **智能缓存**：减少重复请求，提升响应速度
- **优雅的界面**：使用 `rich` 库实现精美的终端展示
- **完整的错误处理**：自动重试、超时处理、友好的错误提示

### 🐚 Shell 智能助手 (shell_ai.py)
- **自然语言转换**：将自然语言描述智能转换为 Shell 命令
- **命令确认机制**：执行前可预览和编辑命令
- **本地历史记录**：自动保存命令历史，方便复用
- **安全执行环境**：内置安全检查机制
- **美化输出**：格式化展示命令结果

## 📋 系统要求

- Python 3.8+
- macOS/Linux（Windows 支持可能不完整）

## 📦 依赖说明

```bash
# 核心依赖
aiohttp>=3.8.0        # 异步 HTTP 客户端
rich>=10.0.0          # 终端美化
prompt_toolkit>=3.0.0  # 命令行交互
python-dotenv>=0.19.0 # 环境变量管理
```

## 🚀 快速开始

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/yiyabo/Terminal-LLM.git
cd Terminal-LLM
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥和其他配置
```

### 使用方法

#### 聊天助手
```bash
python Chat.py
```

**常用命令**：
- `/lang zh` - 切换到中文
- `/lang en` - 切换到英文
- `/clear` - 清屏
- `/exit` - 退出程序

#### Shell 助手
```bash
python shell_ai.py
```

**示例用法**：
```
🤖 > 帮我找出当前目录最大的5个文件
Suggested command: ls -lhS | head -n 5
Execute this command? (y/n/edit):
```

## ⚙️ 配置说明

### 环境变量
- `CHATGLM_API_KEY` - API 密钥
- `CHATGLM_API_URL` - API 端点
- `CHATGLM_MODEL` - 模型名称

### 配置文件
- `config.py` - 核心配置项
- `utils.py` - 工具类和辅助函数

## 🔒 安全说明

1. **API 密钥保护**
   - 使用环境变量管理敏感信息
   - 避免在代码中硬编码密钥

2. **Shell 命令安全**
   - 命令执行前进行确认
   - 内置安全检查机制
   - 支持命令编辑和取消

## 🔍 故障排除

### 常见问题
1. API 连接失败
   - 检查网络连接
   - 验证 API 密钥是否正确
   - 确认 API 端点是否可访问

2. 命令执行错误
   - 检查命令语法
   - 确认是否有足够权限
   - 查看错误日志获取详细信息

## 🤝 贡献指南

欢迎提交 Pull Request 或 Issue！

1. Fork 本仓库
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

## 📄 开源协议

本项目采用 MIT 协议开源。

## 👥 作者

- ChatGLM Team

## 📚 相关资源

- [ChatGLM 官方文档](https://open.bigmodel.cn/docs/api)
- [aiohttp 文档](https://docs.aiohttp.org/)
- [Rich 文档](https://rich.readthedocs.io/)