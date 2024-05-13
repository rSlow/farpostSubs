from abc import ABC, abstractmethod
from typing import Any

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
