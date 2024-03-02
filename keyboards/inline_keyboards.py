__all__ = ("build_pomodoro_markup", )

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_pomodoro_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⏳", callback_data="show_pomodoro_time_left")
    return builder.as_markup()

