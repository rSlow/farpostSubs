from abc import abstractmethod
from asyncio import Protocol
from datetime import datetime
from decimal import Decimal

from aio_pika.abc import AbstractIncomingMessage

Jsonable = bool | bytes | bytearray | Decimal | list | float | int | None | str | datetime


class ConsumeFunction(Protocol):
    @abstractmethod
    async def __call__(self, message: AbstractIncomingMessage):
        ...
