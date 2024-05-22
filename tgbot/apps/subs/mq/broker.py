from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker
import taskiq_aiogram

from apps.subs.di.provider import AdsProvider
from config import settings as common_settings
from config.logger import init_logging

ads_broker = AioPikaBroker(
    url=common_settings.RABBITMQ_URL,
    exchange_name="ads",
    queue_name="ads",
    qos=1
)

taskiq_aiogram.init(
    ads_broker,
    "config.dispatcher:dp",
    "config.bot:bot",
)


@ads_broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_startup(_: TaskiqState):
    init_logging()
    container = make_async_container(AdsProvider())
    setup_dishka(container, ads_broker)
