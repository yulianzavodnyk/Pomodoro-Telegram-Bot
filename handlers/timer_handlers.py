from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.data import get_last_timer_duration, check_activate_user_timer, set_timer, add_user
from keyboards.inline_keyboards import build_timer_markup

router = Router(name=__name__)


@router.message(lambda message: message.text.isnumeric())
async def numbers_handle(message: Message):
    user_id = message.from_user.id
    await add_user(user_id)
    duration = int(message.text)
    if duration not in range(5, 121):
        await message.answer("Timer must be set at least 5 minutes and maximum 120 minutes (2 hours)")
    elif await check_activate_user_timer(user_id):
        await message.answer("There is other timer running!")
    else:
        await set_timer(user_id, time=duration, activation=True)
        await message.reply(
            text=f"Timer successfully started! ({duration} min)",
            reply_markup=build_timer_markup()
        )


@router.message(Command("5", "10", "15", "20", "25", "30", "45", "60"))
async def build_in_timers(message: Message):
    user_id = message.from_user.id
    await add_user(user_id)
    duration = int(message.text[1:])
    if await check_activate_user_timer(user_id):
        await message.answer("There is other timer running!")
    else:
        await set_timer(user_id, time=duration, activation=True)
        await message.reply(
            text=f"Timer successfully started! ({duration} min)",
            reply_markup=build_timer_markup()
        )


@router.message(Command("repeat"))
async def repeat(message: Message):
    user_id = message.from_user.id
    await add_user(user_id)
    duration = await get_last_timer_duration(user_id)
    if await check_activate_user_timer(user_id):
        await message.answer("There is other timer running!")
    elif duration:
        await set_timer(user_id, activation=True, time=duration)
        await message.reply(
            text=f"Timer successfully started! ({duration} min)",
            reply_markup=build_timer_markup()
        )
    else:
        await message.answer("You've never started timer before!")


@router.message(Command("stop"))
async def stop(message: Message):
    user_id = message.from_user.id
    await add_user(user_id)
    if await check_activate_user_timer(user_id):
        await set_timer(user_id, activation=False)
        await message.answer("Ok. Done!")
    else:
        await message.answer("There is no timer running!")
