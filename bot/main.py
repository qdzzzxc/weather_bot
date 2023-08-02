import asyncio

from aiogram import Bot, Dispatcher

import user_handlers_fsm
from config import load_config
from main_menu import set_main_menu

async def main():
    config = load_config()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers_fsm.router)
    #dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())