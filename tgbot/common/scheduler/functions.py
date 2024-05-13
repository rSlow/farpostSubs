from typing import Sequence

from .base import AbstractScheduler


async def init_schedulers(schedulers: Sequence[AbstractScheduler]):
    for scheduler in schedulers:
        scheduler.start()
        await scheduler.init()
