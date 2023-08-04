from aiogram import F, Dispatcher, Router, MagicFilter
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from db.data_access_object import DataAccessObject
from db.models import Users

from keyboards import from_menu_kb_generation, return_to_menu
from texts import text_for_response
from trying_selenium import get_stat

storage = MemoryStorage()
router = Router()


class BotStates(StatesGroup):
    wait_for_city_name = State()
    result = State()


@router.message(Command('menu'))
async def menu_command_response(message : Message):
    keyboard = from_menu_kb_generation()
    await message.answer(text=text_for_response['menu'], reply_markup=keyboard)


@router.message(Command('help'))
async def help_command_response(message : Message):
    await message.answer(text=text_for_response['help'])


@router.message(Command('contacts'))
async def contacts_command_response(message: Message):
    await message.answer(text=text_for_response['contacts'])


@router.callback_query(F.data =='weather_city_search')
async def enter_city_name(callback: CallbackQuery, state: FSMContext):
    text = 'Введите название населённого пункта:'
    await callback.message.edit_text(text=text)
    await state.set_state(BotStates.wait_for_city_name)


@router.message(StateFilter(BotStates.wait_for_city_name), MagicFilter.len(F.text)<30)
async def searching_process(message: Message, state: FSMContext, dao):
    await state.update_data(city=message.text)
    await dao.add_last_city(Users, message.from_user.id, message.text)
    await message.answer(text=f'Поиск погоды в {message.text}')
    await state.clear()


@router.message(StateFilter(BotStates.wait_for_city_name))
async def city_name_error(message: Message, state: FSMContext):
    text = 'Введённое название некорректно ('
    await message.answer(text=text)


@router.callback_query(F.data =='go_to_menu')
async def callback_to_menu(callback: CallbackQuery):
    keyboard = from_menu_kb_generation()
    await callback.message.edit_text(
        text=text_for_response['menu'],
        reply_markup=keyboard)


# @router.callback_query()
# async def process_category_press(callback):
#     await callback.message.answer(text=callback.data)
#     await callback.answer()


@router.message()
async def any_message_response(message: Message):
    keyboard = return_to_menu()
    await message.answer(text=text_for_response['no_filters'], reply_markup=keyboard)



