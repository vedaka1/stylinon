import os
from typing import Any, Callable


def cache_async_result(func: Callable[[], Any]) -> Any:
    cache: dict[str, Any] = {}

    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = func.__name__
        if key in cache:
            return cache[key]
        result: Any = await func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


def get_env_var(key: str, to_cast: Any, default: Any | None = None) -> Any:
    """
    Converting environment variable types
    Args:
        key (str): environment variable
        to_cast (Any): type to convert
        default (Any, optional): default value
    Raises:
        RuntimeError: occurs if such a variable is not found in .env
    Returns:
        Any: an environment variable with a converted type
    """
    value = os.getenv(key)

    if not value and not default:
        raise RuntimeError(f"{key} environment variable not set")
    if not value:
        return default
    return to_cast(value)
