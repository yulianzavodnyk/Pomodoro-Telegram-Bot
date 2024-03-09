import asyncio
import configparser
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import master_router  # router that handles all operations
from database.data import init_db, end_all_users_ended_timers  # database methods

config = configparser.ConfigParser()
config.read('config.ini')  # reading configuration file with value BOT_TOKEN

if not config.get('default', 'BOT_TOKEN'):  # checking if BOT_TOKEN filled out, if not log error
    logging.basicConfig(level=logging.ERROR, format='%(levelname)s - %(message)s')
    logging.error("config.ini: BOT_TOKEN is None, please write it")
    sys.exit(1)

bot = Bot(  # creating telegram bot entity
    token=config.get('default', 'BOT_TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


async def main():
    """ Start bot polling """
    try:
        dp = Dispatcher()  # creating dispatcher entity, adding master_router
        dp.include_router(master_router)
        logging.basicConfig(  # setting log settings
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
    """
        calling end_all_users_ended_timers()
        to get list with all users that have currently ended timer,
        then send to them alert that their timers ended
    """
    while True:
        ended_timer_users_ids = await end_all_users_ended_timers()
        for user_id in ended_timer_users_ids:
            await bot.send_message(user_id, "Timer ended✅")
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    init_db()  # initialization database
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
