import asyncio
from contextlib import asynccontextmanager
from typing import Callable, Any, Awaitable

from faststream import FastStream, BaseMiddleware
from faststream.annotations import (FastStream as AnnotatedFastStream,
                                    Logger as AnnotatedLogger)
from faststream.broker.message import StreamMessage
from faststream.rabbit import RabbitBroker, RabbitQueue, RabbitExchange, ExchangeType
from faststream.rabbit.annotations import RabbitMessage

from common.mq.integration import aiogram_init
from config import settings as common_settings


@asynccontextmanager
async def faststream_lifespan(app: AnnotatedFastStream):
    aiogram_init(
        app,
        "config.dispatcher:dp",
        "config.bot:bot"
    )

    yield

    ...


class RetryError(RuntimeError):
    pass


class RetryMiddleware(BaseMiddleware):
    async def consume_scope(
            self,
            call_next: Callable[[Any], Awaitable[Any]],
            msg: StreamMessage[Any],
    ) -> Any:
        headers = msg.headers
        retries = headers.get("x-retry-count", 0)
        if retries < 3:
            try:
                return await call_next(msg)
            except RetryError:
                ...


rabbit_broker = RabbitBroker(
    url=common_settings.RABBITMQ_URL,
    middlewares=[RetryMiddleware]
)

rabbit_app = FastStream(
    broker=rabbit_broker,
    lifespan=faststream_lifespan
)

queue = RabbitQueue(name="test")
main_exchange = RabbitExchange(name="test")
delay_exchange = RabbitExchange(
    name="test_delay",
    type=ExchangeType.X_DELAYED_MESSAGE,
    arguments={"x-delayed-type": ExchangeType.DIRECT}
)


@rabbit_broker.subscriber(queue, delay_exchange)
# @rabbit_broker.publisher(queue, delay_exchange)
@rabbit_broker.subscriber(queue, main_exchange)
async def task(msg: str,
               message: RabbitMessage,
               broker: RabbitBroker,
               logger: AnnotatedLogger):
    logger.info(f"Received message: {msg}")
    headers = message.headers
    retries = headers.get("x-retry-count", 0)
    if retries < 3:
        headers.setdefault("x-retry-count", retries + 1)
        await broker.publish(
            message,
            queue=queue,
            exchange=delay_exchange,
            headers={"x-delay": 1000}
        )


async def __main__():
    await rabbit_app.run()


if __name__ == '__main__':
    asyncio.run(__main__())
