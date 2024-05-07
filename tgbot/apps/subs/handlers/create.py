from aiogram import types
from aiogram.types import User
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from common.buttons import CANCEL_BUTTON, BACK_BUTTON
from common.dialogs.factory.functions import on_valid_input, on_invalid_input
from ..ORM.schemas import SubscriptionModel, SubscriptionCreateModel
from ..ORM.subs import Subscription
from ..states import CreateSub

url_window = Window(
    Const("Ожидаю ссылку подписки в формате:"),
    Const("https://www.farpost.ru/saved_search/.../.../show/restored"),
    TextInput(
        id="url",
        type_factory=SubscriptionCreateModel.url,
        on_success=on_valid_input("url"),
        on_error=on_invalid_input("Ошибка валидации ссылки: {error.args[0]}")
    ),
    CANCEL_BUTTON,
    state=CreateSub.url
)


async def on_valid_frequency(_: types.Message,
                             __: ManagedTextInput,
                             dialog_manager: DialogManager,
                             data: int):
    dialog_manager.dialog_data["frequency"] = data
    await finish_form(dialog_manager)


async def on_default_frequency(_: types.CallbackQuery,
                               __: Button,
                               manager: DialogManager):
    await finish_form(manager)


async def finish_form(manager: DialogManager):
    session: AsyncSession = manager.middleware_data["session"]
    user: User = manager.middleware_data["event_from_user"]
    data = manager.dialog_data
    url: HttpUrl = data["url"]
    frequency: int = data.get("frequency", 60)
    sub_model = SubscriptionCreateModel(
        url=url,
        frequency=frequency,
        telegram_id=user.id
    )
    await Subscription.add(sub_model, session)
    await manager.done()


frequency_window = Window(
    Const("Укажите периодичность проверки в секундах (цифрой):"),
    TextInput(
        id="url",
        type_factory=int,
        on_success=on_valid_frequency,
        on_error=on_invalid_input("Ошибка валидации значения периодичности: {message.text}")
    ),
    Button(
        text=Const("Значение по умолчанию (60 секунд)"),
        id="default_frequency",
        on_click=on_default_frequency
    ),
    BACK_BUTTON,
    state=CreateSub.frequency
)

create_sub_dialog = Dialog(
    url_window,
    frequency_window
)
