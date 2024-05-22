from datetime import timedelta

from common.utils.functions import get_now
from ..ORM.schemas import SubscriptionModel, MessageSubscription
from .tasks import check_new_notes_aiohttp


def get_query_timestamp(sub: SubscriptionModel):
    query_dt = get_now() - timedelta(seconds=sub.frequency)
    query_ts = int(query_dt.timestamp())
    return query_ts


async def kiq_sub_message(sub: SubscriptionModel):
    sub_message = MessageSubscription(
        **sub.model_dump(),
        timestamp=int(get_now().timestamp())
    )
    await check_new_notes_aiohttp.kiq(sub_message)
    # sub_message = MessageSubscription(
    #     **sub.model_dump(),
    #     timestamp=int(get_now().timestamp())
    # )
    # await check_new_notes_aiohttp.kiq(sub_message)
