from typing import Annotated

from aiogram import Bot, Dispatcher
from faststream import Context

BOT_KEY = "aiogram_bot"
DISPATCHER_KEY = "aiogram_dispatcher"

AnnotatedBot = Annotated[Bot, Context(BOT_KEY)]
AnnotatedDispatcher = Annotated[Dispatcher, Context(DISPATCHER_KEY)]
