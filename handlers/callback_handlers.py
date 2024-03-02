from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.data import get_language, show_time_left, check_activate_user_timer

router = Router(name=__name__)


@router.callback_query(F.data == "show_pomodoro_time_left")
async def cancel_pomodoro(call: CallbackQuery):
    user_id = call.from_user.id
    language = await get_language(user_id)
    if await check_activate_user_timer(user_id):
        hours, minutes, seconds = await show_time_left(user_id)
        answer = {
            "eng": f"Time left: {f'{hours} hr ' if hours else ''}{f'{minutes} min ' if minutes else ''}{seconds} sec",
            "ukr": f"Лишилося: {f'{hours} год ' if hours else ''}{f'{minutes} хв ' if minutes else ''}{seconds} сек"
        }
        await call.answer(text=answer[language], show_alert=True)
    else:
        answer = {
            "eng": f"No timer running!",
            "ukr": f"Нічого не запущено!"
        }
        await call.answer(text=answer[language], show_alert=True)
