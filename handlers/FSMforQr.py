from misc import dp

from features.mainFunctions import \
	decodeQr,   escapeMarkdown

from .defaultFunctions import getDefaultReplyKeyboard

from aiogram.utils import markdown
from aiogram.types import Message

from aiogram.dispatcher import      \
	FSMContext,                     \
	filters                         #
from aiogram.dispatcher.filters.state import    \
	State,                                      \
	StatesGroup                                 #

from validators import url as isURL

from os import remove
from time import time


############################ FSM для распознования QR-кодов #################################


# Класс Машины Состояний
class QrFSM(StatesGroup):
	qrInput = State()
	qrRead = State()


# Хэндлер отмены
@dp.message_handler(state='*', regexp=r'(?i)/отмена|/cancel|ʘтмена')
async def cancelQrHandler(message: Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return

	async with state.proxy() as data:
		try:
			if data['qr']:
				remove(data['qr'])
		except:
			pass

	await state.finish()
	await message.answer('Отменено.')


@dp.message_handler(filters.Text(equals="Распознать QR"), state="*")
@dp.message_handler(commands=["qr"])
async def qrCallingHandler(message: Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is not None:
		return

	markup = getDefaultReplyKeyboard()

	await QrFSM.qrInput.set()
	await message.answer("Отправьте QR-код, который хотите распознать", reply_markup=markup)


@dp.message_handler(content_types=['photo'], state=QrFSM.qrInput)
async def qrCodeAcceptor(message: Message, state: FSMContext):
	async with state.proxy() as data:
		photoPath = str(time()) + ".jpg"
		data['qr'] = photoPath
		await message.photo[-1].download(photoPath)

	await QrFSM.qrRead.set()

	qrData = decodeQr(photoPath)
	remove(data['qr'])

	if qrData:
		messageToUser = "Содержание QR—кода:\n" + f'{qrData}'
	else:
		messageToUser = markdown.bold("Не удалось считать QR—код")

	await message.reply(
		text=messageToUser,
		disable_web_page_preview=False,
	)

	await state.finish()


if __name__ == '__main__':
	txt = decodeQr('C:\\Users\\User\\PycharmProjects\\untitled\\handlers\\img.png')
	pass


# ^-^
