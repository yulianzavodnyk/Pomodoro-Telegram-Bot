__all__ = ("build_menu_markup", )

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def build_menu_markup() -> ReplyKeyboardMarkup:
    # markup that allows user to use basic bot commands
    text = ["/5", "/10", "/15", "/20", "/25", "/30", "/45", "/60", "/help", "/repeat", "/stop"]
    builder = ReplyKeyboardBuilder()
    for i in text:
        builder.add(KeyboardButton(text=i))
    builder.adjust(4, 4, 3)
    return builder.as_markup(resize_keyboard=True)
