import asyncio
from functools import wraps
from typing import Callable, Awaitable


def to_async_thread[** P, T](func: Callable[P, T]) -> Callable[P, Awaitable[T]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper
