from common.mq.exceptions import NotCreatedError
from common.mq.manager import BaseMQConnectionManager
from common.mq.schemas import MQConnectionConfig, MQChannelConfig, MQExchangeConfig, MQQueueConfig, MQMessage
from config import settings
from .consumers import handle_sub_message
from .utils import get_query_timestamp
from ..ORM.schemas import SubscriptionModel, MessageSubscription


class SubsMQConnectionManager(BaseMQConnectionManager):
    async def send_sub(self, sub: SubscriptionModel):
        message = self.form_message(sub)
        await self.send_message(
            message=message,
            routing_key=self.queue_key,
        )

    def form_message(self, sub: SubscriptionModel) -> MQMessage:
        if self._queue is None:
            raise NotCreatedError

        query_ts = get_query_timestamp(sub)
        message_sub = MessageSubscription(
            **sub.model_dump(),
            timestamp=query_ts
        )
        message = MQMessage(body=message_sub)
        return message


async def init_subs_mq():
    subs_mq = SubsMQConnectionManager(
        connection_config=MQConnectionConfig(url=settings.RABBITMQ_URL),
        channel_config=MQChannelConfig(publisher_confirms=False),
        exchange_config=MQExchangeConfig(name="ads"),
        queue_config=MQQueueConfig(
            name="ads",
            timeout=30
        )
    )
    await subs_mq.create()
    await subs_mq.consume(handle_sub_message)
    return subs_mq
