from json import dumps


from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import filters
from aiogram.types import Message


from misc import dp, db, adminUserID
from features.dbInteractions import incrementStatistics


# @dp.message_handler(filters.Text(equals="Статистика"), filters.IDFilter(user_id=adminUserID))
# async def getStatsHandler(message: Message):
#     database = dumps(db.all()).replace("{", "\n").replace("}", "\n").replace(",", "\n").replace("\n\n\n", "\n\n")
#     await message.answer(text=database, parse_mode='MarkdownV2')


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super(CounterMiddleware, self).__init__()

    async def on_pre_process_chosen_inline_result(self, message: Message, data: dict):
        incrementStatistics(userID=message.from_user.id, field="inlineAnswered")


# ^-^
