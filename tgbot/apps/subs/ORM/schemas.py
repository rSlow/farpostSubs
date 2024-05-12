from typing import Annotated

from pydantic import HttpUrl, BeforeValidator, BaseModel, Field

from ..utils.url import prepare_url


def url_regexp_validator(url: HttpUrl | str):
    if isinstance(url, str):
        url = HttpUrl(url)
    return prepare_url(str(url))


def frequency_validator(data: str):
    try:
        frequency = int(data)
    except ValueError:
        raise ValueError(f"Неверно указано значение частоты обновления - {data}")
    if frequency < 30:
        raise ValueError("Значение частоты обновления менее 30 секунд")
    return frequency


class SubscriptionCreateModel(BaseModel):
    telegram_id: int
    url: Annotated[HttpUrl, BeforeValidator(url_regexp_validator)]
    frequency: int = Field(ge=30)
    name: str


class SubscriptionModel(SubscriptionCreateModel):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
