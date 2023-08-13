import asyncio
import os

from aiogram import Bot, Dispatcher
import logging

from db import async_connection_db, create_async_engine_db
from bot.middlewares import ThrottlingMiddleware, SessionMiddleware, RegisteredMiddleware
import bot.user_handlers_fsm as user_handlers_fsm
from bot.config import load_config, Config
from bot.main_menu import set_main_menu


async def main():
    logging.basicConfig(level=logging.INFO, filename="bot_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    configfile = os.environ.get("CONFIG", "bot/bot.ini")
    config: Config = load_config(configfile)
    bot = Bot(token=config.tg_bot.token,
              parse_mode=config.settings.default_parse_mode,)
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers_fsm.router)

    db_session = await async_connection_db(
        engine=await create_async_engine_db(
            config=config.db,
            echo=config.settings.sqlalchemy_echo,
        ),
        expire_on_commit=config.settings.sqlalchemy_expire_on_commit,
    )

    dp.message.outer_middleware(ThrottlingMiddleware())

    dp.update.middleware(SessionMiddleware(sessionmaker=db_session))
    dp.update.middleware(RegisteredMiddleware())

    logging.info('Запуск бота')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)