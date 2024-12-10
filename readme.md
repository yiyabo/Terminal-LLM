# Terminal ChatGLM 

一个优雅的终端版 ChatGLM 客户端，提供美观的界面和流畅的用户体验。

## 特性

- 精美的终端界面
  - 彩色动画和图标
  - 优雅的面板和边框
  - 格式化的文本显示
  - 自动换行和对齐

- 强大的功能
  - 智能缓存机制
  - 历史记录管理
  - 多语言支持
  - 命令行补全

- 实用的命令
  - `/help` - 显示帮助信息
  - `/clear` - 清屏
  - `/history` - 查看历史记录
  - `/lang` - 切换语言 (支持中英文)
  - `/exit` 或 `/quit` - 退出程序

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

1. 复制配置文件模板：
```bash
cp config.example.py config.py
```

2. 编辑 `config.py`，设置你的 API 密钥：
```python
API_KEY = "your-api-key-here"
```

### 运行

```bash
python Chat.py
```

## 项目结构

```
Terminal-LLM/
├── Chat.py          # 主程序入口
├── commands.py      # 命令处理模块
├── config.py        # 配置文件
├── ui.py           # 用户界面模块
└── utils.py        # 工具模块
```

## 使用提示

1. **命令补全**：输入 `/` 后按 Tab 键可以查看所有可用命令
2. **历史记录**：使用 `/history` 查看最近的对话历史
3. **语言切换**：使用 `/lang zh` 或 `/lang en` 切换界面语言
4. **清屏**：使用 `/clear` 清理屏幕并重新显示欢迎信息

## 界面展示

- 优雅的欢迎界面
- 流畅的思考动画
- 美观的响应格式
- 清晰的错误提示
- 精美的命令帮助

## 技术栈

- Python 3.8+
- Rich：终端美化
- Prompt Toolkit：命令行交互
- aiohttp：异步 HTTP 客户端
- ChatGLM API：AI 对话支持

## 开发计划

- [ ] 添加更多的格式化选项
- [ ] 实现更多实用命令
- [ ] 优化缓存机制
- [ ] 添加配置文件导入/导出
- [ ] 支持更多的 AI 模型

## 作者

**Yiyabo!**

## 许可证

MIT License

## 致谢

感谢以下开源项目：
- [Rich](https://github.com/Textualize/rich)
- [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)
- [aiohttp](https://github.com/aio-libs/aiohttp)
- [ChatGLM](https://github.com/THUDM/ChatGLM)

## 终端配置教程

### Windows

1. **使用 PowerShell**
```powershell
# 1. 打开 PowerShell 配置文件
notepad $PROFILE

# 2. 添加以下内容
function chat {
    python "C:\path\to\Terminal-LLM\Chat.py"
}

# 3. 保存并重新加载配置
. $PROFILE
```

2. **使用 Command Prompt (cmd)**
```batch
# 1. 创建一个批处理文件
echo @echo off > %USERPROFILE%\chat.bat
echo python "C:\path\to\Terminal-LLM\Chat.py" >> %USERPROFILE%\chat.bat

# 2. 添加到系统环境变量
setx PATH "%PATH%;%USERPROFILE%"
```

### macOS

1. **使用 Bash**
```bash
# 1. 打开 bash 配置文件
nano ~/.bashrc

# 2. 添加以下内容
alias chat='python /path/to/Terminal-LLM/Chat.py'

# 3. 保存并重新加载配置
source ~/.bashrc
```

2. **使用 Zsh**
```zsh
# 1. 打开 zsh 配置文件
nano ~/.zshrc

# 2. 添加以下内容
alias chat='python /path/to/Terminal-LLM/Chat.py'

# 3. 保存并重新加载配置
source ~/.zshrc
```

### Linux

1. **使用 Bash**
```bash
# 1. 打开 bash 配置文件
nano ~/.bashrc

# 2. 添加以下内容
alias chat='python /path/to/Terminal-LLM/Chat.py'

# 3. 保存并重新加载配置
source ~/.bashrc
```

2. **使用 Zsh**
```zsh
# 1. 打开 zsh 配置文件
nano ~/.zshrc

# 2. 添加以下内容
alias chat='python /path/to/Terminal-LLM/Chat.py'

# 3. 保存并重新加载配置
source ~/.zshrc
```

3. **创建系统级命令**
```bash
# 1. 创建一个软链接到 /usr/local/bin
sudo ln -s /path/to/Terminal-LLM/Chat.py /usr/local/bin/chat

# 2. 添加执行权限
sudo chmod +x /usr/local/bin/chat
```

配置完成后，在任何目录下都可以直接使用 `chat` 命令启动程序。

### 验证安装

在任何终端中输入：
```bash
chat
```

如果看到以下欢迎信息，说明配置成功：
```
✨欢迎使用终端版本ChatGLM✨
```

### 故障排除

1. **命令未找到**
   - 确认配置文件路径是否正确
   - 检查是否已重新加载配置文件
   - 验证 Python 是否在环境变量中

2. **权限问题**
   - Windows：以管理员身份运行终端
   - Linux/macOS：使用 `sudo` 进行配置

3. **Python 路径问题**
   - 使用 `which python` 或 `where python` 确认 Python 路径
   - 考虑使用完整的 Python 路径，如：
     ```bash
     alias chat='/usr/local/bin/python3 /path/to/Terminal-LLM/Chat.py'
     ```