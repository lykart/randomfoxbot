from misc import dp, bot

from features.demotivatorCreator import         \
	txtPicCreator,      demotivatorCreator      #

from features.mainFunctions import \
	fsCreator,          randomPhrase


from aiogram.types import   \
	Message,                \
	ReplyKeyboardMarkup     #
from aiogram.dispatcher import      \
	FSMContext,                     \
	filters                         #
from aiogram.dispatcher.filters.state import    \
	State,                                      \
	StatesGroup                                 #


from os import remove
from time import time


# Стандартная reply-keyboard:
def getDefaultReplyKeyboard():
	markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
	markup.add("Демотиватор")
	markup.insert("Пρопустить подзаголовок")
	markup.insert("Случɑйная подпись")
	markup.add("Распознать QR")
	markup.insert("ʘтмена")

	return markup



############################ FSM для генерации демотиваторов #################################


# Класс Машины Состояний
class DemoFSM(StatesGroup):
	pic = State()
	header = State()
	subtitle = State()
	generationDemo = State()
	headerChanging = State()
	subtitleChanging = State()


# Хэндлер отмены
@dp.message_handler(state=DemoFSM, regexp=r'(?i)/отмена|/cancel|ʘтмена')
async def cancelHandler(message: Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return

	async with state.proxy() as data:
		try:
			if data['pic']:
				remove(data['pic'])
		except:
			pass

	await state.finish()
	await message.answer('Отменено.')


@dp.message_handler(filters.Text(equals="Демотиватор"), state="*")
@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=[r'(?i)demotivator|demo|демо|демотиватор$']), state="*")
async def demoCallingHandler(message: Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is not None:
		return

	markup = getDefaultReplyKeyboard()

	await DemoFSM.pic.set()
	await message.answer("Отправь картинку, которую хотел бы видеть в демотиваторе", reply_markup=markup)


@dp.message_handler(content_types=['photo'], state=DemoFSM.pic)
async def picDemoHandler(message: Message, state: FSMContext):
	async with state.proxy() as data:
		photoName = str(time()) + ".jpg"
		data['pic'] = photoName
		await message.photo[-1].download(photoName)

	await DemoFSM.header.set()
	await message.answer("Что будет в заголовке демотиватора?")


@dp.message_handler(state=DemoFSM.header)
async def headerDemoHandler(message: Message, state: FSMContext):
	if message.text:
		if message.text == 'Случɑйная подпись':
			header, subtitle = randomPhrase()

			async with state.proxy() as data:
				data['header'] = {"text": header, "message": message}
				data['subtitle'] = {"text": subtitle, "message": message}

			await DemoFSM.generationDemo.set()
			await demoFinisher(message, state)

		else:
			await state.update_data(header={"text": message.text, "message": message})

			await DemoFSM.subtitle.set()
			await message.answer("А в подзаголовке?")
	else:
		await message.reply("Не похоже на текст...")


@dp.message_handler(state=DemoFSM.headerChanging)
async def headerChangingDemoHandler(message: Message, state: FSMContext):
	if message.text:
		await state.update_data(header={"text": message.text, "message": message})

		await DemoFSM.generationDemo.set()
		await demoFinisher(message, state)
	else:
		await message.reply("Не похоже на текст...")


@dp.message_handler(state=DemoFSM.subtitle)
async def subtitleDemoHandler(message: Message, state: FSMContext):
	if message.text:
		if message.text == "Пρопустить подзаголовок":
			async with state.proxy() as data:
				data['subtitle'] = None
		else:
			async with state.proxy() as data:
				data['subtitle'] = {"text": message.text, "message": message}

		await DemoFSM.generationDemo.set()
		await demoFinisher(message, state)
	else:
		await message.reply("Не похоже на текст...")


@dp.message_handler(state=DemoFSM.subtitleChanging)
async def subtitleChangingDemoHandler(message: Message, state: FSMContext):
	if message.text:
		if message.text == "Пρопустить подзаголовок":
			async with state.proxy() as data:
				data['subtitle'] = None
		else:
			async with state.proxy() as data:
				data['subtitle'] = {"text": message.text, "message": message}

		await DemoFSM.generationDemo.set()
		await demoFinisher(message, state)
	else:
		await message.reply("Не похоже на текст...")


@dp.message_handler(state=DemoFSM.generationDemo)
async def demoFinisher(message: Message, state: FSMContext):
	async with state.proxy() as data:
		try:
			subTxt = data['subtitle']['text']
		except:
			subTxt = None

		try:
			hTxt = data['header']['text']
			txtPic = txtPicCreator(hTxt, subTxt=subTxt, picPath=data['pic'])

		except ValueError as exception:
			messageToUser = exception.args[0]
			exceptionIn = exception.args[1]

			if exceptionIn == "subtitle":
				messageWhichContainsTooLongText = data['subtitle']['message']
				await DemoFSM.subtitleChanging.set()

			elif exceptionIn == "header":
				messageWhichContainsTooLongText = data['header']['message']
				await DemoFSM.headerChanging.set()

			await messageWhichContainsTooLongText.reply(messageToUser + "\n" + "Повторите ввод:")

			raise

	demPath = demotivatorCreator(picPath=data['pic'], txtPic=txtPic)

	# Проверка: сгенерировался ли демотиватор
	if '.' not in demPath:
		await message.answer(demPath)
	else:
		with open(demPath, 'rb') as photo:
			await bot.send_photo(message.chat.id, photo, caption='Демотиватор готов!')
		remove(demPath)

	remove(data['pic'])

	await state.finish()


########################## FSM для генерации демотиваторов #############################


class sfdFSM(StatesGroup):
	check = State()
	text = State()
	generating = State()


@dp.message_handler(filters.Text(equals="sfd"), state="*")
async def demoCallingHandler(message: Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is not None:
		return

	await sfdFSM.check.set()


@dp.message_handler(state=sfdFSM.check)
async def demoCallingHandler(message: Message, state: FSMContext):
	if message.text == "Cr":
		await sfdFSM.text.set()
	else:
		await state.finish()


@dp.message_handler(state=sfdFSM.text)
async def subtitleDemoHandler(message: Message, state: FSMContext):
	if message.text:
		print("nott")
		try:
			_time, _price, _name = message.text.split('\n')
			IMGpath = fsCreator(_time, _price, _name)

			chatID = message.chat.id
			with open(IMGpath, 'rb') as doc:
				await bot.send_document(chatID, doc)
			remove(IMGpath)
		finally:
			await state.finish()
# ^-^