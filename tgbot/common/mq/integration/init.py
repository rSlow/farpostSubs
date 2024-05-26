from typing import Any, Awaitable, Callable

from aiogram import Bot, Dispatcher
from faststream import FastStream, ContextRepo
from loguru import logger

from .annotations import DISPATCHER_KEY, BOT_KEY
from .utils import import_object


def startup_event_generator(dispatcher_path: str,
                            bot_path: str,
                            **kwargs: str) -> Callable[[ContextRepo], Awaitable[None]]:
    """
    Generate startup event for broker.

    :param dispatcher_path: python-path to the dispatcher object.
    :param bot_path: python-path to bot object.
    :param kwargs: random key-word arguments.

    :returns: startup event handler.
    """

    async def startup(context: ContextRepo) -> None:
        # if not broker.is_worker_process:
        #     return

        dispatcher = import_object(dispatcher_path)
        if not isinstance(dispatcher, Dispatcher):
            raise ValueError("Dispatcher should be an instance of dispatcher.")
        bot = import_object(bot_path)
        if not isinstance(bot, Bot):
            raise ValueError("Bots should be instances of Bot class.")

        workflow_data = {
            "dispatcher": dispatcher,
            "bot": bot,
            **dispatcher.workflow_data,
            **kwargs,
        }

        try:
            await dispatcher.emit_startup(**workflow_data)
        except Exception as exc:
            logger.warning(f"Error found while starting up:")
            logger.exception(exc)

        context.set_global(DISPATCHER_KEY, dispatcher)
        context.set_global(BOT_KEY, bot)

    return startup


def shutdown_event_generator() -> Callable[[ContextRepo], Awaitable[None]]:
    """
    Generate shutdown event for broker.

    This function doesn't take any parameters,
    except broker,
    because all needed information for shutdown
    can be obtained from the state.

    :returns: shutdown event handler.
    """

    async def shutdown(context: ContextRepo) -> None:
        # if not broker.is_worker_process:
        #     return

        bot: Bot = context.get(BOT_KEY)
        dispatcher: Dispatcher = context.get(DISPATCHER_KEY)

        workflow_data = {
            "dispatcher": dispatcher,
            "bot": bot,
            **dispatcher.workflow_data,
        }

        try:
            await dispatcher.emit_shutdown(**workflow_data)
        except Exception as exc:
            logger.warning(f"Error found while shutting down:")
            logger.exception(exc)

    return shutdown


def aiogram_init(app: FastStream,
                 dispatcher: str,
                 bot: str,
                 **kwargs: Any) -> None:
    """
    Initialize faststream broker.

    This function creates startup
    and shutdown events handlers,
    that trigger executor's startup and shutdown events.

    After this function is called, dispatcher and bot
    are going to be available in your tasks,
    using faststream 'Depends()'.

    :param app: current faststream app.
    :param dispatcher: python-path to the dispatcher.
    :param bot: bot to use.
    :param kwargs: random key-word arguments for shutdown and startup events.
    """
    app.on_startup(
        startup_event_generator(
            dispatcher,
            bot,
            **kwargs,
        ),
    )
    app.on_shutdown(
        shutdown_event_generator(),
    )
