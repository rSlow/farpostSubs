from os import PathLike
from typing import Any, Callable, Awaitable, Iterable, Sequence

from aiogram.types import TelegramObject

UserIDType = str | Iterable[str]
HandlerType = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]
PathType = str | PathLike[str] | Sequence[str | PathLike[str]]
