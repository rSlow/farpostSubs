from config.scheduler import NotificationSchedulerfrom aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from config import settings

redis_storage = RedisStorage.from_url(
    settings.REDIS_URL,
    key_builder=DefaultKeyBuilder(with_destiny=True)
)
