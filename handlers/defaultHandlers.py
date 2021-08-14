from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram import filters

from misc import dp, adminUserID
from features.dbInteractions import incrementStatistics, getWholeDb
from handlers.defaultFunctions import getDefaultReplyKeyboard


@dp.message_handler(filters.Text(equals="Статистика"), filters.IDFilter(user_id=adminUserID))
async def getStatsHandler(message: Message):
    stats = getWholeDb()
    stat_message = await message.answer(text=stats)

    from asyncio import sleep
    await sleep(10)     # удаление сообщения статистики после 10ти секунд (оно громоздкое)

    await dp.bot.delete_message(chat_id=message.chat.id, message_id=stat_message.message_id)
    await dp.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.message_handler(commands=["get_keyboard"])
async def set_default_keyboard(message: Message):
	await message.answer("Готово!", reply_markup=getDefaultReplyKeyboard())


@dp.message_handler(commands=["rm_keyboard"])
async def remove_default_keyboard(message: Message):
	await message.answer("Готово!", reply_markup=ReplyKeyboardRemove())


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super(CounterMiddleware, self).__init__()

    async def on_pre_process_chosen_inline_result(self, message: Message, data: dict):
        incrementStatistics(userID=message.from_user.id, field="inlineAnswered")


# ^-^
