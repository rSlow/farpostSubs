from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka
from faststream.annotations import FastStream

from apps.subs.di.provider import AdsProvider
from .integration.init import aiogram_init
from config.logger import init_logging


@asynccontextmanager
async def faststream_lifespan(app: FastStream):
    init_logging()

    container = make_async_container(AdsProvider())
    setup_dishka(container, app)

    aiogram_init(
        app,
        "config.dispatcher:dp",
        "config.bot:bot"
    )

    yield

    ...
