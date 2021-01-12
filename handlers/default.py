from aiogram.types import ReplyKeyboardMarkup


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


# ^-^
