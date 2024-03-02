from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.data import get_language, get_last_timer_duration, check_activate_user_timer, set_timer
from filters.filters import NumbersFilter
from keyboards.inline_keyboards import build_pomodoro_markup

router = Router(name=__name__)

other_timer_running_answer = {
    "eng": "There is other timer running!",
    "ukr": "Інший таймер запущено!"
}
timer_success_set_answer = {
    "eng": "Timer successfully started!",
    "ukr": "Таймер запущено!"
}


@router.message(NumbersFilter())
async def numbers_handle(message: Message):
    number_not_in_range_answer = {
        "eng": "Timer must be set at least 5 minutes and maximum 120 minutes (2 hours)",
        "ukr": "Таймер має бути від 5 до 120 хвилин (2 годин)"
    }
    user_id = message.from_user.id
    language = await get_language(user_id)
    duration = int(message.text)
    if duration not in range(5, 121):
        await message.answer(number_not_in_range_answer[language])
    elif await check_activate_user_timer(user_id):
        await message.answer(other_timer_running_answer[language])
    else:
        await set_timer(user_id, time=duration, activation=True)
        await message.reply(
            text=timer_success_set_answer[language]+f" ({duration} "+{'eng': 'min', 'ukr': 'хв'}[language]+')',
            reply_markup=build_pomodoro_markup()
        )


@router.message(Command("15", "20", "25", "30", "45", "60"))
async def build_in_timers(message: Message):
    user_id = message.from_user.id
    language = await get_language(user_id)
    duration = int(message.text[1:])
    if await check_activate_user_timer(user_id):
        await message.answer(other_timer_running_answer[language])
    else:
        await set_timer(user_id, time=duration, activation=True)
        await message.reply(
            text=timer_success_set_answer[language] + f" ({duration} " + {'eng': 'min', 'ukr': 'хв'}[language] + ')',
            reply_markup=build_pomodoro_markup()
        )


@router.message(Command("repeat"))
async def repeat(message: Message):
    never_started_timer_answer = {
        "eng": "You've never started timer before!",
        "ukr": "Ви ще ніколи не запускали таймер!"
    }
    user_id = message.from_user.id
    language = await get_language(user_id)
    duration = await get_last_timer_duration(user_id)
    if await check_activate_user_timer(user_id):
        await message.answer(other_timer_running_answer[language])
    elif duration:
        await set_timer(user_id, activation=True, time=duration)
        await message.reply(
            text=timer_success_set_answer[language] + f" ({duration} " + {'eng': 'min', 'ukr': 'хв'}[language] + ')',
            reply_markup=build_pomodoro_markup()
        )
    else:
        await message.answer(never_started_timer_answer[language])


@router.message(Command("stop"))
async def stop(message: Message):
    success_stop_answer = {
        "eng": "Ok. Done!",
        "ukr": "Зроблено!"
    }
    no_timer_running_answer = {
        "eng": "There is no timer running!",
        "ukr": "Таймер не запущено!"
    }
    user_id = message.from_user.id
    language = await get_language(user_id)
    if await check_activate_user_timer(user_id):
        await set_timer(user_id, activation=False)
        await message.answer(success_stop_answer[language])
    else:
        await message.answer(no_timer_running_answer[language])
