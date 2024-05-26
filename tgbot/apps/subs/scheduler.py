from apscheduler.job import Job
from faststream.rabbit import RabbitBroker
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from common.scheduler.base import AbstractScheduler
from config import settings
from .ORM.schemas import SubscriptionModel
from .ORM.subs import Subscription
from .mq.publishers import publish_ad_message


class AdsScheduler(AbstractScheduler):
    def __init__(self, broker: RabbitBroker):
        super().__init__(timezone=settings.TIMEZONE)
        self.broker = broker

    async def init(self, session: AsyncSession) -> None:
        subs = await Subscription.get_all_active(session)
        for sub in subs:
            self.create_sub(sub)
        logger.info("INITED SUBSCRIPTION SCHEDULER")

    @staticmethod
    def get_job_id(obj: SubscriptionModel):
        return str(obj.id)

    def create_sub(self, sub: SubscriptionModel):
        return self.add_job(
            func=publish_ad_message,
            id=self.get_job_id(sub),
            trigger="interval",
            seconds=sub.frequency,
            kwargs={
                "broker": self.broker,
                "sub": sub
            }
        )

    def delete_sub(self, obj: SubscriptionModel) -> None:
        job_id = self.get_job_id(obj)
        self.remove_job(job_id)

    def update_sub(self,
                   obj: SubscriptionModel) -> Job:
        self.delete_sub(obj)
        return self.create_sub(obj)
