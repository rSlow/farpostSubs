from aiogram_dialog import DialogManager


async def dialog_data_getter(dialog_manager: DialogManager, **__):
    return dialog_manager.dialog_data


async def start_data_getter(dialog_manager: DialogManager, **__):
    return dialog_manager.start_data
