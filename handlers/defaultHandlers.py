from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aiogram import filters

from misc import dp, adminUserID
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


# ^-^
