from datetime import timedelta

from common.utils.functions import get_now
from ..ORM.schemas import SubscriptionModel


def get_query_timestamp(sub: SubscriptionModel):
    query_dt = get_now() - timedelta(seconds=sub.frequency)
    query_ts = int(query_dt.timestamp())
    return query_ts
