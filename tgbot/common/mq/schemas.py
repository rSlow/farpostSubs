from abc import ABC
from asyncio import AbstractEventLoop
from datetime import datetime, timedelta
from ssl import SSLContext
from typing import Optional, Any

from aio_pika import RobustConnection, Message, DeliveryMode
from aio_pika.abc import AbstractRobustConnection, ExchangeType, SSLOptions
from pydantic import BaseModel, Field
from yarl import URL

from .types import Jsonable


class BaseConfig(BaseModel, ABC):
    class Config:
        arbitrary_types_allowed = True


class MQConnectionConfig(BaseConfig):
    url: Optional[str | URL] = None
    host: str = "localhost"
    port: int = 5672
    login: str = "guest"
    password: str = "guest"
    virtualhost: str = "/"
    ssl: bool = False
    loop: Optional[AbstractEventLoop] = None
    ssl_options: Optional[SSLOptions] = None
    ssl_context: Optional[SSLContext] = None
    timeout: Optional[int | float] = None
    client_properties: Optional[dict[str, Jsonable]] = None
    connection_class: type[AbstractRobustConnection] = RobustConnection
    kwargs: dict[str, Any] = Field(default_factory=dict)


class MQChannelConfig(BaseConfig):
    channel_number: Optional[int] = None
    publisher_confirms: bool = True
    on_return_raises: bool = False


class MQExchangeConfig(BaseConfig):
    name: str
    type: ExchangeType | str = ExchangeType.DIRECT
    durable: bool = False
    auto_delete: bool = False
    internal: bool = False
    passive: bool = False
    arguments: Optional[dict[str, Jsonable]] = None
    timeout: Optional[int | float] = None
    robust: bool = True


class MQQueueConfig(BaseConfig):
    name: Optional[str] = None
    durable: bool = False
    exclusive: bool = False
    passive: bool = False
    auto_delete: bool = False
    arguments: Optional[dict] = None
    timeout: int | float | None = None
    robust: bool = True


class MQMessage(BaseModel):
    body: str | BaseModel | bytes
    headers: Optional[dict] = None
    content_type: Optional[str] = None,
    content_encoding: Optional[str] = None,
    delivery_mode: Optional[DeliveryMode | int] = None,
    priority: Optional[int] = None,
    correlation_id: Optional[str] = None,
    reply_to: Optional[str] = None,
    expiration: Optional[int | datetime | float | timedelta] = None,
    message_id: Optional[str] = None,
    timestamp: Optional[int | datetime | float | timedelta] = None,
    type: Optional[str] = None,
    user_id: Optional[str] = None,
    app_id: Optional[str] = None

    def as_sendable(self):
        if isinstance(self.body, BaseModel):
            str_body = self.body.model_dump_json()
            self.body = str_body.encode()
        if isinstance(self.body, str):
            self.body = self.body.encode()
            return Message(**self.model_dump(mode="json"))
