import asyncio
import logging
import configparser

from aiogram import Bot, Dispatcher
from aiogram.client import bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import master_router
from database.data import init_db, end_all_users_ended_timers

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(
    token=config.get('default', 'BOT_TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


async def main():
    dp = Dispatcher()
    dp.include_router(master_router)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


async def database_changes():
    while True:
        ended_timer_users_ids = await end_all_users_ended_timers()
        for user_id in ended_timer_users_ids:
            await bot.send_message(user_id, "Timer ended✅")
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    init_db()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(main(), database_changes()))
    finally:
        loop.close()
