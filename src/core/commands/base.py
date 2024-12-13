"""命令基类模块"""

from abc import ABC, abstractmethod
from typing import Optional


# pylint: disable=too-few-public-methods
class Command(ABC):
    """命令基类"""

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Optional[bool]:
        """执行命令""" 