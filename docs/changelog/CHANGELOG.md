# Changelog

All notable changes to Terminal-LLM will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Beautiful terminal interface with colored animations and icons
- Smart caching mechanism for improved performance
- Multi-language support (English and Chinese)
- Command line auto-completion
- Basic command set (/help, /clear, /history, /lang, /exit)
- Development tool configurations:
  - EditorConfig for consistent coding styles
  - Pre-commit hooks for code quality checks
  - Code formatting and linting tools integration
- Added CLI entry point for terminal-llm command
- Added src/cli.py as the main entry point for the application

### Changed
- Optimized project structure with separate modules for config, core, data, and UI
- Enhanced documentation in both English and Chinese
- Migrated to Poetry for dependency management
  - Added pyproject.toml for modern Python packaging
  - Separated development and runtime dependencies
  - Removed requirements.txt in favor of Poetry

### Fixed
- Initial setup and configuration issues
- Package dependency management

## [0.1.0] - 2024-12-11

### Added
- Initial release of Terminal-LLM
- Core LLM integration functionality
- Basic terminal UI implementation
- Configuration management system
- Command history feature
- Multi-language support framework
- Project documentation structure

### Security
- Secure environment variable handling
- Basic input validation

[Unreleased]: https://github.com/yourusername/Terminal-LLM/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/Terminal-LLM/releases/tag/v0.1.0
