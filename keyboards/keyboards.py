__all__ = ("build_language_markup", "build_menu_markup")

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def build_language_markup() -> ReplyKeyboardMarkup:
    languages = ["🇺🇦 Українська", "🇬🇧 English"]
    builder = ReplyKeyboardBuilder()
    for language in languages:
        builder.add(KeyboardButton(text=language))
    return builder.as_markup(resize_keyboard=True)


def build_menu_markup() -> ReplyKeyboardMarkup:
    text = ["/15", "/20", "/25", "/30", "/45", "/60", "/help", "/repeat", "/stop"]
    builder = ReplyKeyboardBuilder()
    for i in text:
        builder.add(KeyboardButton(text=i))
    builder.adjust(3, 3, 3)
    return builder.as_markup(resize_keyboard=True)

