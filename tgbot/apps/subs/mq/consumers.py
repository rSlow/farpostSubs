import asyncio

from aio_pika.abc import AbstractIncomingMessage
from loguru import logger

from common.mq.exceptions import RejectedError
from ..ORM.schemas import MessageSubscription
from ..utils.tasks import check_new_ads


async def handle_sub_message(message: AbstractIncomingMessage):
    sub = MessageSubscription.model_validate_json(message.body)
    try:
        await check_new_ads(sub)
        await message.ack()
    except RejectedError as ex:
        logger.error(ex.args[0])
    except Exception as ex:
        logger.exception(ex)
