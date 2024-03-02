from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database.data import add_user, get_language
from keyboards.keyboards import *

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    await add_user(user_id)

    answer = {
        "eng": "Hi, I'm here to help you stay focused on your important tasks.\n"
               "/language to change language, if you want\n"
               "/help to see how bot work",
        "ukr": "Привіт! Я тут, щоб допомогти тобі зосередитися на важливих завданнях.\n"
               "/language щоб змінити мову\n"
               "/help щоб побачити, як працює бот"
    }
    language = await get_language(user_id)
    await message.answer(answer[language], reply_markup=build_menu_markup())


@router.message(Command("help"))
async def bot_help(message: Message):
    answer = {
        "eng": "Send me number of minutes (from 5 to 120) to set the timer " 
               "or press one of the buttons below.\n"
               "/stop to stop timer\n"
               "/repeat to repeat the last timer\n\n"
               "Steps of Pomodoro Technique:\n"
               "1. Choose the task\n"
               "2. Start the timer\n"
               "3. Work on the task until the timer rings\n"
               "4. Take a short break (3-5 minutes)\n"
               "5. After four pomodoro, take a longer break (15-30 minutes)",
        "ukr": "Надішліть мені кількісь хвилин (від 5 до 120) для встановлення таймера "
               "або натисніть одну з кнопок нижче.\n"
               "/stop щоб зупинити таймер\n"
               "/repeat щоб повторити останній таймер\n\n"
               "Техніка Pomodoro складається з 5 кроків:\n"
               "1. Виберіть завдання\n"
               "2. Запустіть таймер\n"
               "3. Працюйте над завданням, доки не закінчиться таймер\n"
               "4. Зробіть коротку перерву (3-5 хвилин)\n"
               "5. Після чотирьох pomodoros зробіть більшу перерву (15-30 хвилин)"
    }
    user_id = message.from_user.id
    language = await get_language(user_id)
    await message.answer(answer[language])


@router.message(Command("language"))
async def set_language(message: Message):
    answer = {
        "eng": "Choose your language 👇",
        "ukr": "Оберіть вашу мову👇"
    }
    user_id = message.from_user.id
    language = await get_language(user_id)
    await message.answer(answer[language], reply_markup=build_language_markup())
