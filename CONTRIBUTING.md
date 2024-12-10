# Contributing to Terminal-LLM

[中文](CONTRIBUTING_CN.md) | English

Thank you for your interest in contributing to Terminal-LLM! This document provides guidelines and workflows for development.

## Development Environment

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Setup
1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/Terminal-LLM.git
cd Terminal-LLM
```

2. Install in development mode:
```bash
pip install -e .
```

3. Create and configure `.env`:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Development Workflow

### 1. Branching Strategy
- `main`: Stable production code
- `feature/*`: New features (e.g., `feature/auto-complete`)
- `fix/*`: Bug fixes (e.g., `fix/connection-timeout`)
- `refactor/*`: Code refactoring
- `docs/*`: Documentation updates

Example:
```bash
# Create a new feature branch
git checkout -b feature/my-feature main

# After development
git checkout main
git merge feature/my-feature
git branch -d feature/my-feature
```

### 2. Commit Guidelines
Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `style:` Code style changes
- `chore:` Maintenance tasks

Example:
```bash
git commit -m "feat: add command auto-completion

- Implement tab completion for commands
- Add tests for completion logic
- Update documentation"
```

### 3. Code Style
- Use [Black](https://github.com/psf/black) for code formatting
- Follow [PEP 8](https://pep8.org/) guidelines
- Maximum line length: 88 characters
- Use meaningful variable and function names
- Add docstrings to all functions and classes

### 4. Project Structure
```
Terminal-LLM/
├── src/                    # Source code
│   ├── core/              # Core functionality
│   ├── config/            # Configuration
│   ├── data/              # Data handling
│   └── ui/                # User interface
├── tests/                 # Test files
└── docs/                  # Documentation
```

### 5. Testing
- Write tests for new features
- Update existing tests when modifying code
- Ensure all tests pass before committing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src
```

### 6. Documentation
- Update README.md and README_EN.md
- Add docstrings to new code
- Update CHANGELOG.md for significant changes

### 7. Pull Request Process
1. Create a new branch for your feature
2. Develop and test your changes
3. Update documentation
4. Submit a pull request with:
   - Clear description of changes
   - Any related issues
   - Screenshots (if UI changes)
   - Test results

### 8. Version Control
Follow [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

## Module Development Guidelines

### Core Module
- Place core functionality in `src/core/`
- Keep business logic separate from UI
- Use async/await for API calls
- Handle exceptions appropriately

### Config Module
- Store configuration in `src/config/`
- Use environment variables for sensitive data
- Provide clear configuration documentation
- Include validation for config values

### Data Module
- Implement data handling in `src/data/`
- Use appropriate caching strategies
- Handle file operations safely
- Implement proper error handling

### UI Module
- Keep UI code in `src/ui/`
- Use Rich library components
- Maintain consistent styling
- Support both English and Chinese

## Security Guidelines

1. API Keys
- Never commit API keys
- Use environment variables
- Document required keys

2. Dependencies
- Keep dependencies updated
- Check for security vulnerabilities
- Use specific version numbers

## Support

If you need help:
- Create an issue
- Join discussions
- Read the documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
