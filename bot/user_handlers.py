'''from aiogram import F, Dispatcher, Router
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Window, Dialog, DialogManager, StartMode, setup_dialogs
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Column, SwitchTo
from aiogram_dialog.widgets.text import Const

from texts import text_for_response
from trying_selenium import get_stat

storage = MemoryStorage()
router = Router()


class BotStates(StatesGroup):
    dont_know_where = State()
    default = State()
    wait_for_city_name = State()
    result = State()


async def city_name_handler(message: Message, message_input: MessageInput,
                       manager: DialogManager):
    if message.text.isdigit() or len(message.text)>20:
        return
    manager.dialog_data["city"] = message.text
    await message.answer(f"Производится поиск погоды в {message.text}")
    await manager.switch_to(BotStates.result)


async def other_city_name_handler(message: Message, message_input: MessageInput,
                             manager: DialogManager):
    await message.answer("Введённое название некорректно")


dialogs = Dialog(
    Window(
        Const(text_for_response['menu']),
        Column(
            SwitchTo(Const("Поиск по населённому пункту"), id="weather_city_search", state=BotStates.wait_for_city_name),
            Button(Const("Повторить последний поиск"), id="weather_last_city_search")),
            state=BotStates.default),
    Window(Const('Введите название населённого пункта:'),
            MessageInput(city_name_handler, content_types=[ContentType.TEXT]),
            MessageInput(other_city_name_handler),
            state=BotStates.wait_for_city_name),
    Window(Const(text_for_response['no_filters']),
            SwitchTo(Const("Вернуться в меню"), id="sec", state=BotStates.default),
            state=BotStates.dont_know_where),
    Window(Const('На этом пока всё'),
                SwitchTo(Const("Вернуться в меню"), id="sec", state=BotStates.default),
                state=BotStates.result)
)

router.include_router(dialogs)
setup_dialogs(router)


@router.message(Command('menu'))
async def menu_command_response(message : Message, dialog_manager: DialogManager):
    # keyboard = from_menu_kb_generation()
    # await message.answer(text=text_for_response['menu'], reply_markup=keyboard)
    await dialog_manager.start(BotStates.default, mode=StartMode.RESET_STACK)


@router.message(Command('help'))
async def help_command_response(message : Message):
    await message.answer(text=text_for_response['help'])


@router.message(Command('contacts'))
async def contacts_command_response(message: Message):
    await message.answer(text=text_for_response['contacts'])


# @router.callback_query(lambda callback: callback.data =='go_to_menu')
# async def callback_to_menu(callback: CallbackQuery):
#     keyboard = from_menu_kb_generation()
#     await callback.message.edit_text(
#         text=text_for_response['menu'],
#         reply_markup=keyboard)
#
#
# @router.callback_query()
# async def process_category_press(callback):
#     await callback.message.answer(text=callback.data)
#     await callback.answer()


@router.message(F.text=='zxc')
async def any_message_response(message: Message, dialog_manager: DialogManager):
    print(StateFilter(default_state))
    # keyboard = return_to_menu()
    # await message.answer(text=text_for_response['no_filters'], reply_markup=keyboard)
    await dialog_manager.start(BotStates.dont_know_where, mode=StartMode.RESET_STACK)'''



