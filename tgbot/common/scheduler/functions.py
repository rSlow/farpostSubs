from typing import Sequence

from .base import AbstractScheduler


async def init_schedulers(schedulers: dict[str, AbstractScheduler],
                          **kwargs):
    for scheduler in schedulers.values():
        scheduler.start()
        await scheduler.init(**kwargs)
