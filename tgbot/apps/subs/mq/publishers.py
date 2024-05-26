from faststream.rabbit import RabbitBroker

from common.utils.functions import get_now
from .routing import ads_main_queue, ads_main_exchange
from ..ORM.schemas import SubscriptionModel


async def publish_ad_message(broker: RabbitBroker,
                             sub: SubscriptionModel):
    await broker.publish(
        message=sub,
        queue=ads_main_queue,
        exchange=ads_main_exchange,
        timestamp=int(get_now().timestamp()),
    )
