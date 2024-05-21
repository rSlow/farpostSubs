from taskiq_aio_pika import AioPikaBroker

from config import settings as common_settings

ads_broker = AioPikaBroker(
    url=common_settings.RABBITMQ_URL,
    exchange_name="ads",
    queue_name="ads",
)
