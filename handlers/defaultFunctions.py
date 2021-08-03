from aiogram.types import ReplyKeyboardMarkup, Message, ReplyKeyboardRemove

from misc import dp


# Стандартная reply-keyboard:
def getDefaultReplyKeyboard():
	markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
	markup.add("Демотиватор")
	markup.insert("Пρопустить подзаголовок")
	markup.insert("Случɑйная подпись")
	markup.add("Распознать QR")
	markup.insert("Настρойки")
	markup.insert("ʘтмена")

	return markup


@dp.message_handler(commands=["get_keyboard"])
async def set_default_keyboard(message: Message):
	await message.answer("Готово!", reply_markup=getDefaultReplyKeyboard())


@dp.message_handler(commands=["rm_keyboard"])
async def remove_default_keyboard(message: Message):
	await message.answer("Готово!", reply_markup=ReplyKeyboardRemove())


# ^-^
