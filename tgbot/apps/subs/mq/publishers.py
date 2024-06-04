from datetime import datetime, timedelta

from faststream.rabbit import RabbitBroker

from common.utils.functions import get_now
from .routing import ads_queue, ads_main_exchange
from ..ORM.schemas import SubscriptionModel
from config import settings as common_settings


async def publish_ad_message(broker: RabbitBroker,
                             sub: SubscriptionModel):
    timestamp = int(get_now().timestamp())
    scheduled_time = datetime.fromtimestamp(timestamp, tz=common_settings.TIMEZONE) + timedelta(seconds=10)
    await broker.publish(
        message=sub,
        exchange=ads_main_exchange,
        queue=ads_queue,
        timestamp=timestamp,
        headers={
            "scheduled_time": scheduled_time,
            "x-delay": 5000
        },
    )
