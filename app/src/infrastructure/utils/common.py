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
