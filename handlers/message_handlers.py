from aiogram import Router, F
from aiogram.types import Message

from database.data import change_language
from keyboards.keyboards import *

router = Router(name=__name__)


@router.message(F.text.in_({"🇺🇦 Українська", "🇬🇧 English"}))
async def change_lang_callback_handler(message: Message):
    languages_with_answers = {
        "🇺🇦 Українська": ["ukr", "Мову успішно змінено"],
        "🇬🇧 English": ["eng", "Language changed"]
    }
    user_id = message.from_user.id
    await change_language(user_id, language=languages_with_answers[message.text][0])
    await message.reply(languages_with_answers[message.text][1], reply_markup=build_menu_markup())
