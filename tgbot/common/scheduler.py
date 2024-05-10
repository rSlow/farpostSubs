from abc import ABC, abstractmethod
from typing import Sequence, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class AbstractScheduler(AsyncIOScheduler, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    async def init(self) -> None:
        ...

    @staticmethod
    @abstractmethod
    def get_job_id(obj: Any) -> str:
        ...


async def init_schedulers(schedulers: Sequence[AbstractScheduler]):
    for scheduler in schedulers:
        scheduler.start()
        await scheduler.init()
