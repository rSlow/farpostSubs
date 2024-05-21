from abc import ABC, abstractmethod
from typing import Sequence, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractScheduler[** P](AsyncIOScheduler, ABC):
    def __init__(self, **kwargs: P.kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    async def init(self, **kwargs) -> None:
        ...

    @staticmethod
    @abstractmethod
    def get_job_id(obj: Any) -> str:
        ...


async def init_schedulers(schedulers: Sequence[AbstractScheduler]):
    for scheduler in schedulers:
        scheduler.start()
        await scheduler.init()
