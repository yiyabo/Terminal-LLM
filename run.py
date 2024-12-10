#!/usr/bin/env python
"""Terminal LLM 入口脚本"""

import asyncio
from src.core.chat import main

if __name__ == "__main__":
    asyncio.run(main())