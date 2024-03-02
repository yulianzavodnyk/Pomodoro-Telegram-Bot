from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database.data import add_user
from keyboards.keyboards import *

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    await add_user(user_id)
    await message.answer(
        text="Hi, I'm here to help you stay focused on your important tasks.\n"
             "/help to see how bot work",
        reply_markup=build_menu_markup()
    )


@router.message(Command("help"))
async def bot_help(message: Message):
    await message.answer(
        text="Send me number of minutes (from 5 to 120) to set the timer "
        "or press one of the buttons below.\n\n"
        "/stop to stop timer\n"
        "/repeat to repeat the last timer\n\n"
        "Steps of Pomodoro Technique:\n"
        "1. Choose the task\n"
        "2. Start the timer\n"
        "3. Work on the task until the timer rings\n"
        "4. Take a short break (3-5 minutes)\n"
        "5. After four pomodoro, take a longer break (15-30 minutes)",
        reply_markup=build_menu_markup()
    )
