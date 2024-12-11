# Terminal-LLM

[中文](README_CN.md) | English

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-package-blue.svg)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

An elegant terminal-based LLM client that provides a beautiful interface and smooth user experience.

## ✨ Features

### 🎨 Beautiful Terminal Interface
- **Dynamic Feedback**: Elegant loading animations make waiting a pleasure
- **Smart Formatting**: Auto-formatting for code, links, and important information
- **Rich Icons**: Enhanced visual experience with Unicode icons
- **Adaptive Layout**: Perfect fit for different terminal window sizes

### 🧠 Intelligent Conversation
- **Local Vector Store**: High-performance vector database based on FAISS
- **Document Processing**: Automatic chunking and vectorization for long text understanding
- **Context Awareness**: Smart conversation history management
- **Multi-language**: Seamless switching between English and Chinese

### ⚡ Powerful Features
- **Command Auto-completion**: Smart suggestions for commands and parameters
- **History Management**: Easy access to conversation history
- **Async Processing**: Efficient handling of concurrent requests
- **Error Recovery**: Smart handling of exceptions

## 🚀 Quick Start

### Requirements
- Python 3.8+
- Poetry package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Terminal-LLM.git
cd Terminal-LLM
```

2. Install Poetry (if not already installed):
```bash
pip install poetry
```

3. Install the project with Poetry:
```bash
poetry install
```

### Usage

After installation, you can start the application in two ways:

1. Using Poetry:
   ```bash
   poetry run terminal-llm
   ```

2. Activating the virtual environment first:
   ```bash
   poetry shell
   terminal-llm
   ```

### Configuration

1. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

2. Add your configuration to `.env`:
```env
CHATGLM_API_KEY=your-api-key-here
CHATGLM_API_URL=your-api-url-here  # Optional
CHATGLM_MODEL=your-model-name      # Optional
```

## 🎯 Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Display help information | `/help` |
| `/load` | Load knowledge documents | `/load docs/example.txt` |
| `/clear` | Clear conversation history | `/clear` |
| `/history` | View history | `/history` |
| `/lang` | Switch interface language | `/lang zh` |
| `/exit` | Exit program | `/exit` |

## 📚 Project Structure

```
Terminal-LLM/
├── src/                    # Source code directory
│   ├── core/              # Core functionality
│   │   ├── chat.py       # Chat functionality
│   │   └── commands/     # Command handling
│   ├── knowledge/        # Knowledge processing
│   │   ├── document.py   # Document processing
│   │   └── vectorstore.py# Vector storage
│   └── ui/               # User interface
│       └── ui.py         # UI components
└── docs/                  # Documentation
    ├── README.md         # English documentation
    └── README_CN.md      # Chinese documentation
```

## 🤝 Contributing

We welcome all forms of contributions! Please refer to our [Contributing Guidelines](contribution/CONTRIBUTING.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
