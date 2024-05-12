import html

from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Group, Button
from aiogram_dialog.widgets.text import Const, Format
from sqlalchemy.ext.asyncio import AsyncSession

from common.buttons import CANCEL_BUTTON
from common.dialogs.factory.dialog_data import dialog_data_getter
from common.dialogs.factory.functions import OnInvalidInput
from common.dialogs.factory.yes_no import yes_no_window
from common.dialogs.widgets.data_checkbox import DataCheckbox
from common.whens import WhenGetterKey
from ..ORM.schemas import frequency_validator
from ..ORM.subs import Subscription
from ..buttons import ON_MAIN_BUTTON
from ..scheduler import SubsScheduler
from ..states import SubMenu


async def sub_main_getter(dialog_manager: DialogManager, **__):
    sub_id = dialog_manager.start_data["sub_id"]
    session: AsyncSession = dialog_manager.middleware_data["session"]
    sub = await Subscription.get(int(sub_id), session)
    # escape HTML characters
    sub.name = html.escape(sub.name)
    json_sub = sub.model_dump(mode="json")
    dialog_manager.dialog_data.update(json_sub)
    return json_sub


async def toggle_is_active(_: types.CallbackQuery,
                           checkbox: DataCheckbox,
                           manager: DialogManager):
    sub_id: int = manager.dialog_data["id"]
    subs_scheduler: SubsScheduler = manager.middleware_data["subs_scheduler"]
    is_active: bool = checkbox.is_checked(manager)
    session: AsyncSession = manager.middleware_data["session"]
    await Subscription.set_is_active(
        session=session,
        sub_id=sub_id,
        is_active=is_active
    )
    sub = await Subscription.get(sub_id, session)
    if is_active:
        subs_scheduler.create_sub(sub)
    else:
        subs_scheduler.delete_sub(sub)
    await manager.update({}, ShowMode.EDIT)


when_is_active = WhenGetterKey("is_active")

sub_main_window = Window(
    Format("Подписка <u>{name}</u>"),
    Format("- <a href='{url}'>ссылка</a>"),
    Const("- активна ✅", when_is_active),
    Const("- не активна ❌", ~when_is_active),
    Format("- раз в {frequency} секунд"),
    Group(
        SwitchTo(
            Const("Название"),
            id="name",
            state=SubMenu.name
        ),
        SwitchTo(
            Const("Частота обновления ⏳"),
            id="frequency",
            state=SubMenu.frequency
        ),
        DataCheckbox(
            checked_text=Const("Активна ✅"),
            unchecked_text=Const("Не активна ❌"),
            id="is_active",
            data_getter="is_active",
            on_state_changed=toggle_is_active
        ),
        SwitchTo(
            Const("Удалить 🗑"),
            id="delete",
            state=SubMenu.delete
        ),
        width=2
    ),
    CANCEL_BUTTON,
    state=SubMenu.main,
    getter=sub_main_getter
)


async def set_name(message: types.Message,
                   _: ManagedTextInput,
                   manager: DialogManager,
                   name: str):
    if name != manager.dialog_data["name"]:
        session: AsyncSession = manager.middleware_data["session"]
        sub_id: int = manager.dialog_data["id"]
        await Subscription.update_name(
            session=session,
            sub_id=sub_id,
            name=name
        )
    await message.delete()
    manager.show_mode = ShowMode.EDIT
    await manager.switch_to(SubMenu.main)


sub_name_window = Window(
    Format("Текущее название: <code>{name}</code>"),
    Const("\nВведите новое название:"),
    TextInput(
        id="name",
        on_success=set_name
    ),
    ON_MAIN_BUTTON,
    state=SubMenu.name,
    getter=dialog_data_getter,
)


async def set_frequency(message: types.Message,
                        _: ManagedTextInput,
                        manager: DialogManager,
                        frequency: int):
    if frequency != manager.dialog_data["frequency"]:
        session: AsyncSession = manager.middleware_data["session"]
        subs_scheduler: SubsScheduler = manager.middleware_data["subs_scheduler"]
        sub_id: int = manager.dialog_data["id"]

        await Subscription.update_frequency(
            session=session,
            sub_id=sub_id,
            frequency=frequency
        )
        sub = await Subscription.get(sub_id, session)
        subs_scheduler.update_sub(sub)

    await message.delete()
    manager.show_mode = ShowMode.EDIT
    await manager.switch_to(SubMenu.main)


sub_frequency_window = Window(
    Format("Текущее значение частоты обновления: {frequency} секунд"),
    Const("\nЗначение частоты обновления должно быть больше или равно 30 секундам."),
    Const("Введите новую частоту обновления (в секундах):"),
    TextInput(
        id="frequency",
        type_factory=frequency_validator,
        on_success=set_frequency,
        on_error=OnInvalidInput(
            error_message="{error.args[0]}",
            delete_input=True
        )
    ),
    ON_MAIN_BUTTON,
    state=SubMenu.frequency,
    getter=dialog_data_getter
)


async def delete_sub(callback: types.CallbackQuery,
                     _: Button,
                     manager: DialogManager):
    await callback.message.edit_text("Удаление...")

    session: AsyncSession = manager.middleware_data["session"]
    subs_scheduler: SubsScheduler = manager.middleware_data["subs_scheduler"]
    sub_id: int = manager.dialog_data["id"]

    sub = await Subscription.get(sub_id, session)
    subs_scheduler.delete_sub(sub)
    await Subscription.delete(
        sub_id=sub_id,
        session=session
    )

    await callback.message.edit_text("Удаление завершено!")
    manager.show_mode = ShowMode.SEND
    await manager.done()


delete_sub_window = yes_no_window(
    Format("Удалить подписку <u>{name}</u>?"),
    state=SubMenu.delete,
    back_state=SubMenu.main,
    on_click=delete_sub,
    getter=dialog_data_getter
)

sub_edit_dialog = Dialog(
    sub_main_window,
    sub_name_window,
    sub_frequency_window,
    delete_sub_window,
)
