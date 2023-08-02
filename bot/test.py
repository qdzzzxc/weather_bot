import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Window, DialogManager, StartMode, setup_dialogs, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

storage = MemoryStorage()
bot = Bot(token='6451274123:AAFST_eFn89wEMz5H6Gd6HyTeIayYpjtMFs')
dp = Dispatcher(bot=bot, storage=storage)


class MySG(StatesGroup):
    main = State()

async def go_clicked(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.edit_text("Going on!")


main_window = Window(
    Const("Hello, unknown person"),
    Button(
        Const("Go"),
        id="go",  # id is used to detect which button is clicked
        on_click=go_clicked,
    )
    ,
    state=MySG.main,
)



@dp.message(CommandStart())
async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


async def main():
    dialog = Dialog(main_window)
    dp.include_router(dialog)

    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())