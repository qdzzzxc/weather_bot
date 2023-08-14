from aiogram import F, Router, MagicFilter, types, Bot
from aiogram.client import bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from datetime import datetime, timedelta

from bot.weather_parsing import get_stat
from db.models import Users

from bot.keyboards import from_menu_kb_generation, return_to_menu, kb_result, kb_result_10_d
from bot.texts import text_for_response

storage = MemoryStorage()
router = Router()


class BotStates(StatesGroup):
    wait_for_city_name = State()


@router.message(Command('start'))
async def help_command_response(message: Message):
    await message.answer(text=text_for_response['start'])


@router.message(Command('menu'))
async def menu_command_response(message: Message, last_val=None):
    keyboard = from_menu_kb_generation(last_val=bool(last_val))
    await message.answer(text=text_for_response['menu'], reply_markup=keyboard)


@router.message(Command('help'))
async def help_command_response(message: Message):
    await message.answer(text=text_for_response['help'])


@router.message(Command('contacts'))
async def contacts_command_response(message: Message):
    await message.answer(text=text_for_response['contacts'])


@router.callback_query(F.data == 'weather_city_search')
async def enter_city_name(callback: CallbackQuery, state: FSMContext):
    text = 'Введите название населённого пункта:'
    await callback.message.edit_text(text=text)
    await state.set_state(BotStates.wait_for_city_name)


result_weather_default = ["{}\n", "{}\n", "{} °C\n", "Ощущается как {} °C\n", "Вероятность дождя: {} %"]

td = datetime.today()
result_weather_10_days = "{}\n" \
                         "Сейчас: {}°C\n" \
                         "Завтра: {}°C\n" \
                         f"{(td+timedelta(days=2)).strftime('%d-%m')}  {{}}°C\n" \
                         f"{(td+timedelta(days=3)).strftime('%d-%m')}  {{}}°C\n"\
                         f"{(td+timedelta(days=4)).strftime('%d-%m')}  {{}}°C\n"\
                         f"{(td+timedelta(days=5)).strftime('%d-%m')}  {{}}°C\n"\
                         f"{(td+timedelta(days=6)).strftime('%d-%m')}  {{}}°C\n"\
                         f"{(td+timedelta(days=7)).strftime('%d-%m')}  {{}}°C\n"\
                         f"{(td+timedelta(days=8)).strftime('%d-%m')}  {{}}°C\n"\
                         f"{(td+timedelta(days=9)).strftime('%d-%m')}  {{}}°C\n"\
                         f"{(td+timedelta(days=10)).strftime('%d-%m')}  {{}}°C\n"


@router.callback_query(F.data == 'show_10_days')
async def result_10_days(callback: CallbackQuery, last_val, dao):
    weather = await get_stat(last_val, dao, mode='10_d')
    if weather[1] == 'Нет данных':
        text = f'{last_val}\nСейчас: {weather[0]}°C\nИзвините, но мы не смогли получить прогноз погоды на 10 дней :('
    else:
        text = result_weather_10_days.format(last_val, *weather)
    await callback.message.edit_text(text=text, reply_markup=kb_result_10_d())


@router.callback_query(F.data == 'return_to_search_result')
async def result_10_days(callback: CallbackQuery, last_val, dao):
    weather = await get_stat(last_val, dao)
    text = [string.format(atr) for string, atr in zip(result_weather_default, [last_val] + list(weather)) if
            atr != 'Нет данных']
    text = ''.join(text)
    await callback.message.edit_text(text=text, reply_markup=kb_result())


@router.callback_query(F.data == 'weather_last_city_search')
async def last_city_result(callback: CallbackQuery, last_val, dao):
    await callback.message.edit_text(text=f'Поиск погоды в {last_val}')

    weather = await get_stat(last_val, dao)

    text = [string.format(atr) for string, atr in zip(result_weather_default, [last_val] + list(weather)) if
            atr != 'Нет данных']
    text = ''.join(text)
    await callback.message.edit_text(text=text, reply_markup=kb_result())


@router.message(BotStates.wait_for_city_name, F.text.len() < 30)
async def searching_process(message: Message, bot: Bot, state: FSMContext, dao):
    resp = await message.answer(text=f'Поиск погоды в {message.text}')
    await state.clear()
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    city_name = message.text.capitalize()
    weather = await get_stat(city_name, dao)
    if weather:
        await dao.upd_col_val(Users, 'user_id', message.from_user.id, vals_to_update={'last_city': city_name})
        text = [string.format(atr) for string, atr in zip(result_weather_default, [city_name] + list(weather)) if
                atr != 'Нет данных']
        text = ''.join(text)
        await resp.edit_text(text=text, reply_markup=kb_result())
    else:
        await resp.edit_text(text='Не найдено населённого пункта с таким названием')


@router.message(BotStates.wait_for_city_name)
async def city_name_error(message: Message):
    text = 'Введённое название некорректно, попробуйте снова'
    await message.answer(text=text)


@router.callback_query(F.data == 'go_to_menu')
async def callback_to_menu(callback: CallbackQuery, last_val):
    keyboard = from_menu_kb_generation(last_val=bool(last_val))
    await callback.message.edit_text(
        text=text_for_response['menu'],
        reply_markup=keyboard)


@router.message()
async def any_message_response(message: Message, state: FSMContext):
    keyboard = return_to_menu()
    await message.answer(text=text_for_response['no_filters'], reply_markup=keyboard)
    await state.clear()
