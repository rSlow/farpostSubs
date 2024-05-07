from operator import itemgetter

from aiogram import types
from aiogram.types import User
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Format, Const
from sqlalchemy.ext.asyncio import AsyncSession

from common.buttons import CANCEL_BUTTON
from common.whens import WhenAble
from ..ORM.subs import Subscription
from ..states import CurrentSubsFSM


async def current_subs_getter(event_from_user: User,
                              dialog_manager: DialogManager,
                              **__):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    subs = await Subscription.get_from_user(
        session=session,
        telegram_id=event_from_user.id
    )
    subs_buttons = [(sub.id, sub.name) for sub in subs]
    return {
        "subs": subs_buttons,
        "subs_count": len(subs)
    }


async def on_sub_click(_: types.CallbackQuery,
                       __: Select,
                       dialog_manager: DialogManager,
                       data: str):
    ...


when_subs = WhenAble("subs")

current_subs_dialog = Dialog(
    Window(
        Format("Текущих подписок: {subs_count}"),
        ScrollingGroup(
            Select(
                text=Format("{item[1]}"),
                item_id_getter=itemgetter(0),
                id="subs",
                items="subs",
                on_click=on_sub_click
            ),
            id="subs_scroll",
            width=1,
            height=4,
            when=when_subs
        ),
        Start(
            text=Const("Добавить подписку"),
            id="add_sub",
            state=...,
            when=~when_subs
        ),
        CANCEL_BUTTON,
        state=CurrentSubsFSM.state,
        getter=current_subs_getter
    )
)
