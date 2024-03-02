import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client import bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import master_router
from config import BOT_TOKEN
from database.data import init_db, end_all_users_active_timers, get_language

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


async def main():
    dp = Dispatcher()
    dp.include_router(master_router)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


async def database_changes():
    text = {
        "eng": "Timer ended",
        "ukr": "Таймер закінчився"
    }
    while True:
        ended_timer_users_id = await end_all_users_active_timers()
        for user_id in ended_timer_users_id:
            await bot.send_message(user_id, text[get_language(user_id)])
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    init_db()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(main(), database_changes()))
    finally:
        loop.close()
