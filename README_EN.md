# Terminal ChatGLM 

[中文](README.md) | English

An elegant terminal-based ChatGLM client that provides a beautiful interface and smooth user experience.

## Features

- Beautiful Terminal Interface
  - Colored animations and icons
  - Elegant panels and borders
  - Formatted text display
  - Smooth thinking animation

- Powerful Functionality
  - Intelligent caching mechanism
  - History management
  - Multi-language support
  - Markdown-style formatting

- Useful Commands
  - `/help` - Display help information
  - `/clear` - Clear screen
  - `/history` - View chat history
  - `/exit` or `/quit` - Exit program

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root directory:
```env
CHATGLM_API_KEY=your_api_key_here
```

### Run

```bash
python Chat.py
```

## Project Structure

```
Terminal-LLM/
├── Chat.py         # Main entry
├── config.py       # Configuration
├── utils.py        # Utility module
└── commands.py     # Command system
```

## Usage Tips

1. **Command Completion**: Press Tab after typing `/` to view all available commands
2. **History**: Use `/history` to view recent chat history
3. **Clear Screen**: Use `/clear` to clean the screen and show welcome message again
4. **Exit**: Use `/exit` or `/quit` to exit the program

## Interface Preview

- Elegant welcome interface
- Smooth thinking animation
- Clear command help
- Beautiful error messages

## Tech Stack

- Python 3.8+
- Rich: Terminal beautification
- Prompt-toolkit: Command line interaction
- aiohttp: Async HTTP client
- ChatGLM API: AI conversation support

## Development Plan

- [ ] Add more formatting options
- [ ] Implement more useful commands
- [ ] Add configuration import/export
- [ ] Support more AI models

## Author

**Yiyabo!**

## License

MIT License

## Terminal Setup Guide

### Windows

1. **Using PowerShell**
```powershell
# 1. Open PowerShell configuration file
notepad $PROFILE

# 2. Add the following content
function chat {
    python "C:\path\to\Terminal-LLM\Chat.py"
}

# 3. Save and reload configuration
. $PROFILE
```

2. **Using Command Prompt (cmd)**
```batch
# 1. Create a batch file
echo @echo off > %USERPROFILE%\chat.bat
echo python "C:\path\to\Terminal-LLM\Chat.py" >> %USERPROFILE%\chat.bat

# 2. Add to system environment variables
setx PATH "%PATH%;%USERPROFILE%"
```

### macOS

1. **Using Bash**
```bash
# 1. Open bash configuration file
nano ~/.bashrc

# 2. Add the following content
alias chat='python /path/to/Terminal-LLM/Chat.py'

# 3. Save and reload configuration
source ~/.bashrc
```

2. **Using Zsh**
```zsh
# 1. Open zsh configuration file
nano ~/.zshrc

# 2. Add the following content
alias chat='python /path/to/Terminal-LLM/Chat.py'

# 3. Save and reload configuration
source ~/.zshrc
```

### Linux

1. **Using Bash**
```bash
# 1. Open bash configuration file
nano ~/.bashrc

# 2. Add the following content
alias chat='python /path/to/Terminal-LLM/Chat.py'

# 3. Save and reload configuration
source ~/.bashrc
```

2. **Using Zsh**
```zsh
# 1. Open zsh configuration file
nano ~/.zshrc

# 2. Add the following content
alias chat='python /path/to/Terminal-LLM/Chat.py'

# 3. Save and reload configuration
source ~/.zshrc
```

3. **Create System-level Command**
```bash
# 1. Create a symbolic link to /usr/local/bin
sudo ln -s /path/to/Terminal-LLM/Chat.py /usr/local/bin/chat

# 2. Add execution permission
sudo chmod +x /usr/local/bin/chat
```

After configuration, you can use the `chat` command from any directory to start the program.

### Verify Installation

In any terminal, type:
```bash
chat
```

If you see the following welcome message, the configuration is successful:
```
✨Welcome to Terminal ChatGLM✨
```

### Troubleshooting

1. **Command Not Found**
   - Verify configuration file path is correct
   - Check if configuration file has been reloaded
   - Verify Python is in environment variables

2. **Permission Issues**
   - Windows: Run terminal as administrator
   - Linux/macOS: Use `sudo` for configuration

3. **Python Path Issues**
   - Use `which python` or `where python` to confirm Python path
   - Consider using full Python path, e.g.:
     ```bash
     alias chat='/usr/local/bin/python3 /path/to/Terminal-LLM/Chat.py'
     ```

## Acknowledgments

Thanks to the following open-source projects:
- [Rich](https://github.com/Textualize/rich)
- [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)
- [aiohttp](https://github.com/aio-libs/aiohttp)
- [ChatGLM](https://github.com/THUDM/ChatGLM)
