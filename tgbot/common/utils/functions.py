from datetime import datetime
from typing import Optional

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Chat
from aiogram_dialog import DialogManager

from config import settings


def get_now():
    return datetime.now().astimezone(tz=settings.TIMEZONE)


async def edit_dialog_message(manager: DialogManager,
                              text: str,
                              reply_markup: Optional[InlineKeyboardMarkup] = None):
    dialog_message_id: int = manager.current_stack().last_message_id
    bot: Bot = manager.middleware_data["bot"]
    chat: Chat = manager.middleware_data["event_chat"]
    return await bot.edit_message_text(
        chat_id=chat.id,
        message_id=dialog_message_id,
        text=text,
        reply_markup=reply_markup
    )
