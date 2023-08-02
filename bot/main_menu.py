from aiogram.types import BotCommand


async def set_main_menu(bot):
    commands = {'/menu' : 'Перейти к меню',
    '/help': 'Справка по работе бота',
    '/contacts' : 'Контакты создателя бота'}
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
        description in commands.items()]
    await bot.set_my_commands(main_menu_commands)