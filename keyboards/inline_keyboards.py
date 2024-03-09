__all__ = ("build_timer_markup",)

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_timer_markup() -> InlineKeyboardMarkup:
    # markup that shows to user show how much time is left till the end of the timer
    builder = InlineKeyboardBuilder()
    builder.button(text="⏳", callback_data="show_time_left")
    return builder.as_markup()

