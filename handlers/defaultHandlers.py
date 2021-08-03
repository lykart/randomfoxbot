from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, BotCommand

from aiogram import filters

from misc import dp, adminUserID, bot
from features.dbInteractions import incrementStatistics, getWholeDb


@dp.message_handler(filters.Text(equals="Статистика"), filters.IDFilter(user_id=adminUserID))
async def getStatsHandler(message: Message):
    stats = getWholeDb()
    await message.answer(text=stats)


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super(CounterMiddleware, self).__init__()

    async def on_pre_process_chosen_inline_result(self, message: Message, data: dict):
        incrementStatistics(userID=message.from_user.id, field="inlineAnswered")


async def set_default_commands():
    commands = [
        {
            'command': 'demotivator',
            'description': '🌄 Создание демотиватора',
        }, {
            'command': 'qr',
            'description': '📊 Генерация QR-кода',
        }, {
            'command': 'settings',
            'description': '🔧 Настройки',
        }, {
            'command': 'get_keyboard',
            'description': '🟩 Вкл. клавиатуру ответов',
        }, {
            'command': 'rm_keyboard',
            'description': '🟥 Выкл. клавиатуру ответов',
        },
    ]

    commands = [
        BotCommand(command['command'], command['description'])
        for command in commands
    ]

    return commands


# ^-^
