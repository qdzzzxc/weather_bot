from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def from_menu_kb_generation(last_val):
    kb_builder = InlineKeyboardBuilder()
    button_names = ['Поиск по населённому пункту']
    if last_val: button_names.append('Повторить последний поиск')
    back_data = ['weather_city_search', 'weather_last_city_search']
    buttons = [InlineKeyboardButton(text=text, callback_data=data) for text, data in zip(button_names, back_data)]
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup(resize_keyboard=True)


def return_to_menu():
    button_name = 'Перейти в меню'
    button_data = 'go_to_menu'
    button: InlineKeyboardButton = InlineKeyboardButton(text=button_name, callback_data=button_data)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return keyboard


def kb_result():
    kb_builder = InlineKeyboardBuilder()
    button_names = ['Показать прогноз погоды на 10 дней', 'Поиск по населённому пункту']
    back_data = ['show_10_days', 'weather_city_search']
    buttons = [InlineKeyboardButton(text=text, callback_data=data) for text, data in zip(button_names, back_data)]
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup(resize_keyboard=True)


def kb_result_10_d():
    kb_builder = InlineKeyboardBuilder()
    button_names = ['Краткая сводка', 'Поиск по населённому пункту']
    back_data = ['return_to_search_result', 'weather_city_search']
    buttons = [InlineKeyboardButton(text=text, callback_data=data) for text, data in zip(button_names, back_data)]
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup(resize_keyboard=True)

