#!/usr/bin/env python
"""Terminal LLM CLI entry point"""

import asyncio
from src.core.chat import main

def cli():
    """Command line interface entry point"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
