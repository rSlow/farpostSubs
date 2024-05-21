from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class SQLProvider(Provider):
    component = "sql"

    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncIterable[AsyncSession]:
        async with Session() as session:
            yield session
