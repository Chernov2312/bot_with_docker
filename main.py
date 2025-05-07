import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import logging
from dotenv import find_dotenv, load_dotenv

from database.db import DataBaseSession

load_dotenv(find_dotenv())

from database.engine import drop_db, create_db, session_maker
from commands import private
from handlers.privite_user_handler import user_router
bot = Bot(token=os.environ.get('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.include_router(user_router)
logging.basicConfig(level=logging.INFO)



async def on_startup(bot):
    logging.info("Бот запущен")
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    logging.info("Бот лёг")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())

