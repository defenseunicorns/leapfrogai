import os
from functools import wraps

from leapfrogai_api.utils.logging_tools import logger


def dev_only(func):
    """Decorator to conditionally register a FastAPI route only when the env var 'DEV' is set."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if os.environ.get("DEV") == "true":
            return func(*args, **kwargs)
        else:
            logger.warning(f"Route '{func.__name__}' is only available in dev mode.")
            return None

    return wrapper
