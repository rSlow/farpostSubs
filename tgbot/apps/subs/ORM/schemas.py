from typing import Annotated

from pydantic import BaseModel, HttpUrl, AfterValidator


def url_validator(url: HttpUrl):
    if url.host != "farpost.ru":
        raise ValueError(f"wrong host: {url.host}")
    return url


class SubscriptionCreateModel(BaseModel):
    telegram_id: int
    url: Annotated[HttpUrl, AfterValidator(url_validator)]
    frequency: int


class SubscriptionModel(SubscriptionCreateModel):
    id: int
    is_active: bool
