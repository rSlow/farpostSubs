from faststream import FastStream
from faststream.rabbit import RabbitBroker

from apps.subs.mq.tasks import ads_router
from .lifespan import faststream_lifespan
from config import settings as common_settings

broker = RabbitBroker(common_settings.RABBITMQ_URL)
app = FastStream(
    broker=broker,
    lifespan=faststream_lifespan
)

broker.include_routers(
    ads_router,
)
