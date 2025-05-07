from aiogram.types import BotCommand


private = [
    BotCommand(command='start', description='Запуск бота'),
    BotCommand(command='plans_get', description='Планы вывести'),
    BotCommand(command='plans_set', description='Планы установить'),
    BotCommand(command='plans_set_apply', description='подтвердить планы'),
    BotCommand(command='plans_id_clear', description='Очистить по номеру'),
    BotCommand(command='plans_all_clear', description='Очистить все'),
]
