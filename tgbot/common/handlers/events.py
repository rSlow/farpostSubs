from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, KICKED
from aiogram.types import ChatMemberUpdated
from aiogram_dialog import DialogManager

common_events_router = Router(name="common_events")


@common_events_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated,
                           dialog_manager: DialogManager):
    ...
