from typing import Any

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from common.types import HandlerType


def register_middlewares(middlewares: list[BaseMiddleware],
                         dispatcher: Dispatcher):
    for middleware in middlewares:
        dispatcher.update.middleware(middleware)
        dispatcher.error.middleware(middleware)


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: HandlerType,
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)


class ContextMiddleware(BaseMiddleware):
    def __init__(self, **context):
        super().__init__()
        self.context = context

    async def __call__(
            self,
            handler: HandlerType,
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        data.update(self.context)
        return await handler(event, data)
