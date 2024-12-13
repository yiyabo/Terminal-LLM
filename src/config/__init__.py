"""配置模块

导出所有配置项供其他模块使用。
"""

from .config import (
    API_KEY,
    API_URL,
    CACHE_ENABLED,
    CACHE_FILE,
    COMMANDS,
    HISTORY_FILE,
    LOG_FILE,
    MAX_HISTORY_ITEMS,
    MAX_RETRIES,
    MODEL_NAME,
    MODEL_TYPE,
    REQUEST_TIMEOUT,
    RETRY_DELAY,
    CHUNK_SIZE,
    STREAM_BUFFER_SIZE,
    REFRESH_RATE,
    get_current_language,
    set_current_language,
)
