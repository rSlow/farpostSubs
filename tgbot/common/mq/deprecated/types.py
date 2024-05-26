from datetime import datetime
from decimal import Decimal
from typing import Awaitable, Callable

from aio_pika.abc import AbstractIncomingMessage

Jsonable = bool | bytes | bytearray | Decimal | list | float | int | None | str | datetime
ConsumeFunction = Callable[[AbstractIncomingMessage], Awaitable]
