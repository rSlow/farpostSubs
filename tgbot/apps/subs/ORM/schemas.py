from typing import Annotated

from pydantic import HttpUrl, BeforeValidator, BaseModel

from ..types import farpost_url_factory


def _url_regexp_validator(url: HttpUrl | str):
    if isinstance(url, str):
        url = HttpUrl(url)
    str_url = str(url)
    return farpost_url_factory(str_url)


class SubscriptionCreateModel(BaseModel):
    telegram_id: int
    url: Annotated[HttpUrl, BeforeValidator(_url_regexp_validator)]
    frequency: int
    name: str


class SubscriptionModel(SubscriptionCreateModel):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
