from datetime import datetime
from typing import Optional

from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup, Chat, ReplyKeyboardMarkup
from aiogram_dialog import DialogManager

from config import settings


def get_now(timezone: Optional[str] = None):
    tz = timezone if timezone is not None else settings.TIMEZONE
    return datetime.now().astimezone(tz=tz)


def get_now_strftime(timezone: Optional[str] = None):
    return get_now(timezone).strftime("%d-%m-%Y %H:%M:%S")


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


async def send_message(manager: DialogManager,
                       text: str,
                       reply_markup: Optional[ReplyKeyboardMarkup | InlineKeyboardMarkup] = None):
    bot: Bot = manager.middleware_data["bot"]
    chat: Chat = manager.middleware_data["event_chat"]
    return await bot.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=reply_markup
    )


def get_message(event: types.ErrorEvent):
    if message := event.update.message:
        return message
    if callback_message := event.update.callback_query.message:
        return callback_message
    raise RuntimeError(f"no message exists in error {event.exception}")
