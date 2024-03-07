from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.database.data import calculate_time_left, check_activate_user_timer

router = Router(name=__name__)


@router.callback_query(F.data == "show_time_left")
async def show_alert_time_left(call: CallbackQuery):
    user_id = call.from_user.id
    if await check_activate_user_timer(user_id):
        hours, minutes, seconds = await calculate_time_left(user_id)
        await call.answer(
            text=f"Time left: {f'{hours} hr ' if hours else ''}{f'{minutes} min ' if minutes else ''}{seconds} sec",
            show_alert=True
        )
    else:
        await call.answer(
            text="No timer running!",
            show_alert=True
        )
