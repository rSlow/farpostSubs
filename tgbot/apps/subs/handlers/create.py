from aiogram import types
from aiogram.types import User
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from sqlalchemy.ext.asyncio import AsyncSession

from common.buttons import CANCEL_BUTTON, BACK_BUTTON
from common.dialogs.factory.functions import OnInvalidInput, OnValidInput
from common.utils.functions import edit_dialog_message
from ..ORM.schemas import SubscriptionCreateModel, frequency_validator
from ..ORM.subs import Subscription
from ..scheduler import SubsScheduler
from ..states import CreateSub
from ..types import farpost_url_factory

url_window = Window(
    Const("Ожидаю ссылку подписки в формате:"),
    Const("https://www.farpost.ru/saved_search/.../.../show"),
    Const("Прочие дополнительные параметры запроса уберутся автоматически."),
    TextInput(
        id="url",
        type_factory=farpost_url_factory,
        on_success=OnValidInput(pre_saver=lambda url: str(url)),
        on_error=OnInvalidInput("<b><u>Ошибка валидации ссылки</u></b>: {error.args[0]}")
    ),
    CANCEL_BUTTON,
    state=CreateSub.url
)


async def on_default_frequency(_: types.CallbackQuery,
                               __: Button,
                               manager: DialogManager):
    manager.dialog_data["frequency"] = 60
    await manager.next()


frequency_window = Window(
    Const("Укажите периодичность проверки в секундах (цифрой), не менее 30 секунд:"),
    TextInput(
        id="frequency",
        type_factory=frequency_validator,
        on_success=OnValidInput(),
        on_error=OnInvalidInput("Ошибка валидации значения периодичности: {message.text}")
    ),
    Button(
        text=Const("Значение по умолчанию (60 секунд)"),
        id="default_frequency",
        on_click=on_default_frequency
    ),
    BACK_BUTTON,
    state=CreateSub.frequency
)


async def finish_form_wrapper(_: types.Message,
                              dialog_manager: DialogManager,
                              __: int):
    await finish_form(dialog_manager)


async def finish_form(manager: DialogManager):
    await edit_dialog_message(
        manager=manager,
        text="Обработка..."
    )

    session: AsyncSession = manager.middleware_data["session"]
    user: User = manager.middleware_data["event_from_user"]
    data = manager.dialog_data
    url: str = data["url"]
    frequency: int = data["frequency"]
    name: str = data["name"]
    sub_model = SubscriptionCreateModel(
        url=url,
        frequency=frequency,
        telegram_id=user.id,
        name=name
    )
    sub = await Subscription.add(sub_model, session)
    subs_scheduler: SubsScheduler = manager.middleware_data["subs_scheduler"]
    subs_scheduler.create_sub(sub)

    await edit_dialog_message(
        manager=manager,
        text="Подписка добавлена."
    )
    manager.show_mode = ShowMode.SEND
    await manager.done()


name_window = Window(
    Const("Введите название подписки:"),
    TextInput(
        id="name",
        on_success=OnValidInput(handle_next=False, after_handler=finish_form_wrapper),
    ),
    BACK_BUTTON,
    state=CreateSub.name
)

create_sub_dialog = Dialog(
    url_window,
    frequency_window,
    name_window
)
