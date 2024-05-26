from typing import Annotated

from aiogram import Bot, Dispatcher
from faststream import Context

AnnotatedBot = Annotated[Bot, Context("bot")]
AnnotatedDispatcher = Annotated[Dispatcher, Context("dispatcher")]
