from operator import itemgetter

from aiogram import types
from aiogram.types import User
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Format, Const, Case
from sqlalchemy.ext.asyncio import AsyncSession

from common.buttons import CANCEL_BUTTON
from common.whens import WhenGetterKey
from ..ORM.subs import Subscription
from ..states import CurrentSubsFSM, CreateSub, SubMenu


async def current_subs_getter(event_from_user: User,
                              dialog_manager: DialogManager,
                              **__):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    subs = await Subscription.get_all_user_subscriptions(
        session=session,
        telegram_id=event_from_user.id
    )
    subs_buttons = [(sub.id, sub.name, sub.is_active) for sub in subs]
    return {
        "subs": subs_buttons,
        "subs_count": len(subs),
        "active_subs_count": len([*filter(lambda x: x.is_active, subs)])
    }


async def on_sub_click(_: types.CallbackQuery,
                       __: Select,
                       dialog_manager: DialogManager,
                       data: str):
    await dialog_manager.start(
        state=SubMenu.main,
        data={"sub_id": data}
    )


when_subs = WhenGetterKey("subs")


def item_data_selector(pos: int):
    def inner(data: dict,
              _: Case,
              __: DialogManager):
        return data["item"][pos]

    return inner


current_subs_dialog = Dialog(
    Window(
        Format("Текущих подписок: {subs_count}"),
        Format("Активных подписок: {active_subs_count}"),
        ScrollingGroup(
            Select(
                text=Case(
                    texts={
                        True: Format('✅ {item[1]}'),
                        False: Format('❌ {item[1]}'),
                    },
                    selector=item_data_selector(2)
                ),
                item_id_getter=itemgetter(0),
                id="subs",
                items="subs",
                on_click=on_sub_click,
            ),
            id="subs_scroll",
            width=1,
            height=4,
            hide_on_single_page=True,
            when=when_subs
        ),
        Start(
            text=Const("Добавить подписку"),
            id="add_sub",
            state=CreateSub.url,
            when=~when_subs
        ),
        CANCEL_BUTTON,
        state=CurrentSubsFSM.state,
        getter=current_subs_getter
    )
)
