from aiogram import types
from aiogram.types import User
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiohttp import ClientSession
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from common.buttons import CANCEL_BUTTON, BACK_BUTTON
from common.dialogs.factory.functions import OnInvalidInput, OnValidInput
from common.utils.functions import edit_dialog_message, get_now_strftime
from config import settings as common_settings
from ..ORM.schemas import SubscriptionCreateModel, frequency_validator
from ..ORM.subs import Subscription
from ..api.parser import is_valid_url
from ..api.saver import save_page
from ..api.url import get_headers
from ..scheduler import AdsScheduler
from ..settings import TEMP_DIR
from ..states import CreateSub
from ..types import farpost_url_factory


async def on_url_success(message: types.Message,
                         _: ManagedTextInput,
                         dialog_manager: DialogManager,
                         data: str):
    check_message = await message.answer("Проверка...")
    await message.delete()
    try:
        async with ClientSession(headers=get_headers()) as session:
            await session.get("https://www.farpost.ru/")  # get cookies
            async with session.get(data) as response:
                real_url = response.real_url
                page_data = await response.content.read()
        is_valid = is_valid_url(page_data)
        if is_valid:
            dialog_manager.dialog_data["url"] = str(real_url.parent) + "?" + real_url.query_string
            await dialog_manager.next()
        else:
            if common_settings.DEBUG:
                await save_page(
                    path=TEMP_DIR / "pages" / f"error_page {get_now_strftime()}.html",
                    data=page_data
                )
            await message.answer(f"<a href='{data}'>Ссылка</a> ведет на сайт FarPost, но при этом страница не содержит "
                                 f"списка элементов. Проверьте правильность введенной ссылки.")
    except Exception as ex:
        logger.warning(ex.args[0])
        await message.answer("Во время проверки ссылки возникла неизвестная ошибка. "
                             "Пожалуйста, попробуйте добавить ссылку через некоторое время.")
    finally:
        await check_message.delete()


url_window = Window(
    Const("Ожидаю ссылку подписки в формате:"),
    Const("https://www.farpost.ru/..."),
    Const("Введенный запрос будет проверен на правильность автоматически."),
    TextInput(
        id="url",
        type_factory=farpost_url_factory,
        on_success=on_url_success,
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
    Const("Ссылка прошла проверку!"),
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
    ads_scheduler: AdsScheduler = manager.middleware_data["ads_scheduler"]
    ads_scheduler.create_sub(sub)

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
