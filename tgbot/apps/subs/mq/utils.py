from datetime import timedelta

from common.utils.functions import get_now
from ..ORM.schemas import SubscriptionModel, MessageSubscription
from .tasks import check_new_notes


def get_query_timestamp(sub: SubscriptionModel):
    query_dt = get_now() - timedelta(seconds=sub.frequency)
    query_ts = int(query_dt.timestamp())
    return query_ts


async def check_new_notes_preloader(sub: SubscriptionModel):
    sub_message = MessageSubscription(
        **sub.model_dump(),
        timestamp=int(get_now().timestamp())
    )
    await check_new_notes.kiq(sub_message)
