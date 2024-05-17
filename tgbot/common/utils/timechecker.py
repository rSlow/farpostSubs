import time
from functools import wraps
from typing import ParamSpec, TypeVar, Awaitable, Callable

from loguru import logger

P = ParamSpec("P")
T = TypeVar("T")


def asynctimechecker(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.time()
        result = await func(*args, **kwargs)
        execution_time = time.time() - start
        logger.info(f"Execution time: {execution_time:.2f}")
        return result

    return wrapper


def timechecker(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start
        logger.info(f"Execution time: {execution_time:.2f}")
        return result

    return wrapper
