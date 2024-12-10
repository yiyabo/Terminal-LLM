"""配置模块

导出所有配置项供其他模块使用。
"""

from .config import (
    API_KEY,
    API_URL,
    MODEL_NAME,
    MAX_RETRIES,
    RETRY_DELAY,
    REQUEST_TIMEOUT,
    CACHE_ENABLED,
    CACHE_FILE,
    HISTORY_FILE,
    LOG_FILE,
    get_current_language,
    set_current_language,
    COMMANDS
)

from .languages import LANGUAGES