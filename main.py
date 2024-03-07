import asyncio
import configparser
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import master_router
from database.data import init_db, end_all_users_ended_timers

config = configparser.ConfigParser()
config.read('config.ini')


async def main():
    try:
        bot = Bot(
            token=config.get('default', 'BOT_TOKEN'),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
    except Exception:
        logging.basicConfig(level=logging.ERROR, format='%(levelname)s - %(message)s')
        logging.error("config.ini: BOT_TOKEN is None, please write it")
        sys.exit(1)

    try:
        dp = Dispatcher()
        dp.include_router(master_router)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
        )
        await dp.start_polling(bot)
    except Exception:
        logging.basicConfig(level=logging.ERROR, format='%(levelname)s - %(message)s')
        logging.error("Cannot start polling, check value BOT_TOKEN in config.ini")
        sys.exit(1)


async def database_changes():
    bot = Bot(
        token=config.get('default', 'BOT_TOKEN'),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    while True:
        ended_timer_users_ids = await end_all_users_ended_timers()
        for user_id in ended_timer_users_ids:
            await bot.send_message(user_id, "Timer ended✅")
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    init_db()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                main(),
                database_changes()
            )
        )
    except Exception:
        loop.close()
        sys.exit(1)
