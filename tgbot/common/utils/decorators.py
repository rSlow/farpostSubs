import asyncio
from functools import wraps
from typing import TypeVar, Callable, ParamSpec, Awaitable

T = TypeVar('T', covariant=True)
P = ParamSpec("P")


def to_async_thread(func: Callable[P, T]) -> Callable[P, Awaitable[T]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper
