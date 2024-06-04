from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, KICKED
from aiogram.types import ChatMemberUpdated
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from apps.subs.ORM.subs import Subscription
from apps.subs.scheduler import AdsScheduler

common_events_router = Router(name="common_events")


@common_events_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated,
                           dialog_manager: DialogManager):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    ads_scheduler: AdsScheduler = dialog_manager.middleware_data["ads_scheduler"]

    subs = await Subscription.get_all_user_subscriptions(
        telegram_id=event.from_user.id,
        session=session
    )
    for sub in subs:
        ads_scheduler.delete_sub(sub)

    await Subscription.deactivate_user(
        telegram_id=event.from_user.id,
        session=session
    )
