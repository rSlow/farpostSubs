from aiogram import Bot, Dispatcher
from apscheduler.job import Job
from loguru import logger

from common.scheduler import AbstractScheduler
from config import settings
from .ORM.schemas import SubscriptionModel
from .ORM.subs import Subscription
from .utils.tasks import check_new_notes


class SubsScheduler(AbstractScheduler):
    def __init__(self,
                 bot: Bot,
                 dispatcher: Dispatcher):
        super().__init__(timezone=settings.TIMEZONE)
        self.bot = bot
        self.dispatcher = dispatcher

    async def init(self) -> None:
        subs = await Subscription.get_all_active()
        for sub in subs:
            self.create_sub(sub)
        logger.info("INITED SUBSCRIPTION SCHEDULER")

    @staticmethod
    def get_job_id(obj: SubscriptionModel):
        return str(obj.id)

    def create_sub(self,
                   obj: SubscriptionModel,
                   **kwargs):
        kwargs.update({
            "sub": obj,
            "bot": self.bot
        })
        return self.add_job(
            func=check_new_notes,
            id=self.get_job_id(obj),
            trigger="interval",
            seconds=obj.frequency,
            kwargs=kwargs,
        )

    def delete_sub(self, obj: SubscriptionModel) -> None:
        job_id = self.get_job_id(obj)
        self.remove_job(job_id)

    def update_sub(self,
                   obj: SubscriptionModel) -> Job:
        self.delete_sub(obj)
        return self.create_sub(obj)
