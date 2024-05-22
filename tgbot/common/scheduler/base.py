from abc import ABC, abstractmethod
from typing import Any, Iterable

from apscheduler.schedulers.asyncio import AsyncIOScheduler


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
