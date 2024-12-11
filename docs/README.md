# Terminal-LLM

[中文](README.md) | English

An elegant terminal-based LLM client that provides a beautiful interface and smooth user experience.

## Features

- 🎨 Beautiful Terminal Interface
  - Colored animations and icons
  - Elegant panels and borders
  - Formatted text display
  - Auto-wrapping and alignment

- 🚀 Powerful Functionality
  - Intelligent caching mechanism
  - History management
  - Multi-language support (Chinese & English)
  - Command-line completion

- ⌨️ Useful Commands
  - `/help` - Display help information
  - `/clear` - Clear screen
  - `/history` - View chat history
  - `/lang` - Switch language
  - `/exit` or `/quit` - Exit program

## Quick Start

### Requirements
- Python 3.8 or higher
- pip package manager

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
touch .env
```

2. Add the following to your `.env` file:
```env
CHATGLM_API_KEY=your-api-key-here
CHATGLM_API_URL=your-api-url-here  # Optional
CHATGLM_MODEL=your-model-name      # Optional
```

## Project Structure

```
Terminal-LLM/
├── src/                    # Source code directory
│   ├── core/              # Core functionality
│   │   ├── chat.py       # Chat functionality
│   │   ├── commands.py   # Command handling
│   │   └── shell_ai.py   # Shell AI
│   ├── config/           # Configuration management
│   │   └── config.py     # Configuration definitions
│   ├── data/             # Data processing
│   │   └── cache.py      # Cache management
│   └── ui/               # User interface
│       └── ui.py         # UI components
├── data/                  # Data files
│   ├── cache/            # Cache directory
│   ├── history/          # History records
│   └── chat.log          # Log file
├── .env                   # Environment variables
├── .gitignore            # Git ignore file
├── README.md             # Documentation (Chinese)
├── README_EN.md          # Documentation (English)
├── pytest.ini            # Test configuration
└── run.py                # Entry point
```

## Development

### Testing
```bash
pytest
```

### Code Style
The project uses Black for code formatting:
```bash
black src/
```

## Contributing

Pull requests and issues are welcome!

## License

[MIT License](LICENSE)
