from aiogram import Bot, Dispatcher
from apscheduler.job import Job
from loguru import logger

from common.mq.manager import RabbitConnectionManager
from common.mq.schemas import MQMessage
from common.scheduler import AbstractScheduler
from config import settings
from .ORM.schemas import SubscriptionModel
from .ORM.subs import Subscription


class SubsScheduler(AbstractScheduler):
    def __init__(self,
                 bot: Bot,
                 dispatcher: Dispatcher,
                 rabbit: RabbitConnectionManager):
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

    def create_sub(self,
                   obj: SubscriptionModel,
                   **kwargs):
        message = MQMessage(body=obj)
        kwargs.update({
            "messages": [message],
            "routing_key": self.rabbit.queue_key
        })
        return self.add_job(
            func=self.rabbit.send_messages,
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
