from aiogram import Bot, Dispatcher
from apscheduler.job import Job
from loguru import logger

from common.scheduler.base import AbstractScheduler
from config import settings
from .ORM.schemas import SubscriptionModel
from .ORM.subs import Subscription
from .mq.manager import SubsMQConnectionManager


class SubsScheduler(AbstractScheduler):
    def __init__(self,
                 bot: Bot,
                 dispatcher: Dispatcher,
                 rabbit: SubsMQConnectionManager):
        super().__init__(timezone=settings.TIMEZONE)
        self.bot = bot
        self.dispatcher = dispatcher
        self.rabbit = rabbit

    async def init(self) -> None:
        subs = await Subscription.get_all_active()
        for sub in subs:
            self.create_sub(sub)
        logger.info("INITED SUBSCRIPTION SCHEDULER")

    @staticmethod
    def get_job_id(obj: SubscriptionModel):
        return str(obj.id)

    def create_sub(self, sub: SubscriptionModel):
        return self.add_job(
            func=self.rabbit.send_sub,
            id=self.get_job_id(sub),
            trigger="interval",
            seconds=sub.frequency,
            kwargs={"sub": sub},
        )

    def delete_sub(self, sub: SubscriptionModel) -> None:
        job_id = self.get_job_id(sub)
        self.remove_job(job_id)

    def update_sub(self, sub: SubscriptionModel) -> Job:
        self.delete_sub(sub)
        return self.create_sub(sub)
