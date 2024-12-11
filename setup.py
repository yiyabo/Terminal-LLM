from setuptools import setup, find_packages

setup(
    name="terminal-llm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "prompt_toolkit",
        "rich",
        "python-dotenv"
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'terminal-llm=src.cli:cli'
        ],
    },
)