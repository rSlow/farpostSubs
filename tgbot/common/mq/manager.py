from abc import ABC, abstractmethod
from functools import wraps
from typing import Optional, Awaitable, Callable, ParamSpec, TypeVar

from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, AbstractRobustExchange, AbstractRobustQueue

from .exceptions import NotCreatedError
from .schemas import MQConnectionConfig, MQExchangeConfig, MQQueueConfig, MQChannelConfig, MQMessage
from .types import ConsumeFunction, Jsonable

P = ParamSpec("P")
T = TypeVar("T")


def check_created_connection(func: Callable[P, Awaitable[T]]):
    @wraps(func)
    async def _inner(self: "BaseMQConnectionManager",
                     *args: P.args, **kwargs: P.kwargs) -> T:
        if not isinstance(self, BaseMQConnectionManager):
            raise TypeError(f"{self.__class__.__name__} is not a RabbitConnectionManager")
        if not self._created:
            raise NotCreatedError
        return await func(self, *args, **kwargs)

    return _inner


class BaseMQConnectionManager(ABC):
    _connection: Optional[AbstractRobustConnection] = None
    _channel: Optional[AbstractRobustChannel] = None
    _exchange: Optional[AbstractRobustExchange] = None
    _queue: Optional[AbstractRobustQueue] = None

    _created: bool = False

    def __init__(self, *,
                 connection_config: MQConnectionConfig = MQConnectionConfig(),
                 channel_config: MQChannelConfig = MQChannelConfig(),
                 exchange_config: MQExchangeConfig = MQExchangeConfig(name="default"),
                 queue_config: MQQueueConfig = MQQueueConfig(name="default")):
        self._connection_config = connection_config
        self._channel_config = channel_config
        self._exchange_config = exchange_config
        self._queue_config = queue_config

    @property
    def queue_key(self):
        return self._queue.name

    async def create(self):
        self._connection = await connect_robust(
            **self._connection_config.model_dump(exclude={"kwargs"}),
            **self._connection_config.kwargs
        )
        self._channel = await self._connection.channel(**self._channel_config.model_dump())
        self._exchange = await self._channel.declare_exchange(**self._exchange_config.model_dump())
        self._queue = await self._channel.declare_queue(**self._queue_config.model_dump())

        await self._queue.bind(self._exchange, self._queue_config.name)

        self._created = True

    @check_created_connection
    async def send_message(self,
                           message: MQMessage | str,
                           routing_key: str,
                           mandatory: bool = True,
                           immediate: bool = False,
                           timeout: Optional[int | float] = None):
        if not isinstance(message, (MQMessage, str)):
            raise TypeError(f"message is type {message.__class__.__name__}, not 'MQMessage' or 'str'")
        if isinstance(message, str):
            message = MQMessage(body=message)
        publish_message = message.as_sendable()
        await self._exchange.publish(
            message=publish_message,
            routing_key=routing_key,
            mandatory=mandatory,
            immediate=immediate,
            timeout=timeout
        )

    @check_created_connection
    async def consume(self,
                      callback: ConsumeFunction,
                      *,
                      no_ack: bool = False,
                      exclusive: bool = False,
                      arguments: Optional[dict[str, Jsonable]] = None,
                      consumer_tag: Optional[str] = None,
                      timeout: Optional[int | float] = None,
                      robust: bool = True):
        consumer_tag = await self._queue.consume(
            callback=callback,
            no_ack=no_ack,
            exclusive=exclusive,
            arguments=arguments,
            consumer_tag=consumer_tag,
            timeout=timeout,
            robust=robust
        )
        return consumer_tag

    @abstractmethod
    def form_message(self, **kwargs) -> MQMessage:
        ...
