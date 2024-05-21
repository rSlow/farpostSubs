from apscheduler.job import Job
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import AsyncBroker, BrokerMessage

from common.scheduler import AbstractScheduler
from config import settings
from .ORM.schemas import SubscriptionModel
from .ORM.subs import Subscription


class AdsScheduler(AbstractScheduler):
    def __init__(self, broker: AsyncBroker):
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

    def create_sub(self,
                   obj: SubscriptionModel,
                   **kwargs):
        message = BrokerMessage(
            task_name="check_notes",
            message=obj.model_dump_json().encode(),
        )
        return self.add_job(
            func=self.broker.kick(message),
            id=self.get_job_id(obj),
            trigger="interval",
            seconds=obj.frequency
        )

    def delete_sub(self, obj: SubscriptionModel) -> None:
        job_id = self.get_job_id(obj)
        self.remove_job(job_id)

    def update_sub(self,
                   obj: SubscriptionModel) -> Job:
        self.delete_sub(obj)
        return self.create_sub(obj)
