import asyncio
import os

from aiogram import Bot, Dispatcher
from sqlalchemy import URL

from middlewares import ThrottlingMiddleware
import user_handlers_fsm
from config import load_config
from main_menu import set_main_menu

#from db import BaseModel, create_async_engine, get_session_maker, proceed_schemas

async def main():
    config = load_config()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers_fsm.router)

    dp.message.outer_middleware(ThrottlingMiddleware())

    #dp.include_router(other_handlers.router)

    # postgres_url = URL.create(
    #     "postgresql+asyncpg",
    #     username=os.getenv('db_user'),
    #     host='localhost',
    #     password='nyaaa8008',
    #     database=os.getenv('db_name'),
    #     port=os.getenv('db_port')
    # )
    #
    # async_engine = create_async_engine()
    # session_maker = get_session_maker(async_engine)
    # with session_maker() as session:
    #     proceed_schemas(session, BaseModel.metadata)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())