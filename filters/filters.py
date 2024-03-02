__all__ = ("NumbersFilter",)

from aiogram.filters import Filter
from aiogram.types import Message


class NumbersFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.text.isnumeric()
