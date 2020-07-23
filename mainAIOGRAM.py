from primaryFunctions import getRandomWikiArticle, orDecider, \
	yesOrNot, randomRating, randomPopGenerator, getRandomYoutubeVideo, \
	createQR, uploadInputFileToTelegram
from demotivatorCreator import demotivatorCreator

from random import choice, randint

from aiogram import Bot, Dispatcher, types
from aiogram.types.input_media import InputMediaPhoto
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultPhoto, inline_keyboard
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor, markdown

from time import time

import os
import logging
import re


# Инициализация работы бота
bot_token = os.environ["bot_token"]
ytApiKey = os.environ["ytApiKey"]

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


helpList = [
	[
		'Введите математическое выражение, оканчивающееся на \"=\"',

		"Введите математическое выражение, состоящее из чисел и простейших операций "
		"(Лис ещё только учится!!) типа \"*\", \"/\", \"+\", \"-\", оканчивающееся на знак \"=\" "
		"и Лис посчитает в столбик результат вычислений"
	], [
		'Введите \"wiki\" для получения случайной статьи',

		"Введите \"wiki\" или \"wikipedia\" в любом регистре, и Лис быстро сбегает до Вики и "
		"принесёт ссылку на случайную статью из русскоязычной Википедии"
	], [
		'Введите вопрос, и бот ответит Да\Нет',

		"Введите любой вопрос, не содержащий \"или\" (желательно, на который можно ответить "
		"односложно, Лис ещё плохо понимает человечий и не может изъяснятся без переводчика, "
		"для большего погружения О_о), и бот ответит на него Да или Нет"
	], [
		'Введите список слов через \"или\", и бот выберет одно',

		"Введите любое количество слов через \"или\" и Лис, обнюхав, выберет одно из них"
	], [
		'Введите \"rate\" и после то, что должен оценить бот',

		"Введите \"rate\" в любом регистре и через пробел то, что хотите отдать на оценку Лису. "
		"Он ответит вам в десятибальной шкале с небольшим милым пояснением"
	], [
		'Введите \"yt\" для получения случайного видео'

		"Введите \"yt\" или \"youtube\", чтобы получить случайное видео с ютуба, которое в данный "
		"момент просматривает Лис"
	]]


@dp.inline_handler(regexp=r'(?i)^help$|^\s*$')
async def helpInlineHandler(inline_query: InlineQuery):
	items = [
		InlineQueryResultArticle(
			id=str(i),
			title=helpList[i][0],
			input_message_content=InputTextMessageContent(helpList[i][1]))
		for i in range(len(helpList) - 1)
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=300)


qrQueue = []


@dp.inline_handler(regexp=r'(?i)^qr\b.+$')
async def qrInlineHandler(inline_query: InlineQuery):
	txt = re.search(r"(?i)qr\b\s+(.+)", inline_query.query).group(1)

	awaitingButton = inline_keyboard.InlineKeyboardButton(
		'Ожидайте...',
		callback_data='awaiting'
	)

	awaitingKeyboard = inline_keyboard.InlineKeyboardMarkup(row_width=1).\
									   insert(awaitingButton)

	items = [
		InlineQueryResultPhoto(
			id=str(time()+1),
			photo_url="https://i.ibb.co/n16zcs0/rnfoxbot-QR.jpg",
			thumb_url='https://i.ibb.co/KsbFqjG/rnfoxbot-QR.jpg',
			photo_width=200,
			photo_height=200,
			caption=
				markdown.italic("QR code с текстом") + '\n' +
			    markdown.bold  (f"\"{txt}\"") + '\n'
			,
			reply_markup=awaitingKeyboard,
			parse_mode='MarkdownV2'
		)
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=500)

	if inline_query.from_user.id not in qrQueue:
		qrQueue.append(inline_query.from_user.id)
		print(qrQueue)


@dp.chosen_inline_handler(lambda chosen_inline_query: chosen_inline_query.from_user.id in qrQueue)
async def some_chosen_inline_handler(chosen_inline_query: types.ChosenInlineResult):
	queryTxt = chosen_inline_query.query
	txt = re.search(r"(?i)qr\b\s+(.+)", queryTxt).group(1)

	voidInlineKeyboard = inline_keyboard.InlineKeyboardMarkup()

	qrCodePath = createQR(txt)
	imgID = await uploadInputFileToTelegram(qrCodePath, botToken=bot_token, bot=bot)


	await bot.edit_message_reply_markup(
		reply_markup=voidInlineKeyboard,
		inline_message_id=chosen_inline_query.inline_message_id
	)

	await bot.edit_message_media(
		media=InputMediaPhoto(media=imgID),
		inline_message_id=chosen_inline_query.inline_message_id
	)

	qrQueue.remove(chosen_inline_query.from_user.id)
	os.remove(qrCodePath)


# Обработчик запроса "Who am I?" Inline Query
@dp.inline_handler(regexp=r'(?i)who\s*am\s*i')
async def whoIAmInlineHandler(inline_query: InlineQuery):
	LGBTQKAplus = [
		"Гей", "Пидорас", "Лесбиян04ка", "FTM трансгендер", "MTF трансгендер",
		"Трансформер", "Мороженое \"Радуга\"", "Би", "Квирчик", "Апельсин", "Вертолёт АПАЧИ", "Big Poppa",
		"Small Joppa", "Агендер", "Асексуал", "Ким 5+", "Лох", "Валя Беляев", "Голубой", "Фанат зелёного гей флага",
		"забанены в твиттере"
	]

	answer = choice(LGBTQKAplus)
	print(answer)

	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Кто я из суперсемейки?',
			input_message_content=InputTextMessageContent(f"Вы {answer}!"))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик ответа Да\Нет на вопрос Inline Query
@dp.inline_handler(regexp=r'(?i)^(?=.*?\?)((?!или|or).)*$')
async def questionInlineQueryHandler(inline_query: InlineQuery):
	messToUser = markdown.bold(inline_query.query) + '\n' + markdown.italic(yesOrNot())
	print(messToUser)
	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Да|Нет',
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


@dp.inline_handler(regexp=r'(?i)(.+\bили|or\b.+)+')
async def OrInlineQueryHandler(inline_query: InlineQuery):
	messToUser = markdown.bold(inline_query.query) + \
	             '\n' + markdown.italic(orDecider(inline_query.query).capitalize())

	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Одно из слов',
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик запроса случайной роры Inline Query
@dp.inline_handler(regexp=r'(?i)popa|попа\s+\d+')
async def popaInlineQueryHandler(inline_query: InlineQuery):
	num = int(inline_query.query.lower().replace("popa", "").strip())

	messToUser = markdown.bold(randomPopGenerator(num).strip().capitalize())
	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Ророчка',
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик запроса случайной роры Inline Query
@dp.inline_handler(regexp=r'(?i)num\s+-*\d+\s+-*\d+')
async def randNumInlineQueryHandler(inline_query: InlineQuery):
	num = [int(i) for i in inline_query.query.lower().replace("num", "").split()]

	messToUser = markdown.italic(f"Случайное число от {num[0]} до {num[1]}:") + '\n' + markdown.bold(f'{randint(num[0], num[1])}')
	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title=f'Случайное число от {num[0]} до {num[1]}',
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик простейших математических выражений Inline Query
@dp.inline_handler(regexp=r'[\s\d\.\,\/\*\-\+\(\)]+=$')
async def calculationInlineQueryHandler(inline_query: InlineQuery):
	messToUser = markdown.code(inline_query.query.replace(" ", "")) + markdown.code(
		str(eval(inline_query.query.replace("=", "").replace(",", "."))))
	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Результат вычислений',
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


@dp.inline_handler(regexp=r'(?i)^\s*gay$')
async def howMuchInlineQueryHandler(inline_query: InlineQuery):
	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Насколько я гей?',
			input_message_content=InputTextMessageContent(markdown.italic(f"Я Гей на {randint(0, 100)}%"),
			                                              parse_mode='MarkdownV2'))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик запроса оценки Inline Query
@dp.inline_handler(regexp=r'(?i)rate\b\b.*')
async def RateInlineQueryHandler(inline_query: InlineQuery):
	item = inline_query.query.lower().replace("rate", '').strip()
	print(item)
	messToUser = randomRating(item)
	print(messToUser)
	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Оценка от Лиса',
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик запроса случайного видео с YouTube Inline Query
@dp.inline_handler(regexp=r'(?i)yt|youtube')
async def youtubeInlineQueryHandler(inline_query: InlineQuery):
	randomYoutubeVideo = await getRandomYoutubeVideo(ytApiKey)
	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Случайное видео с YouTube',
			input_message_content=InputTextMessageContent(randomYoutubeVideo))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик запроса случайной статьи Википедии Inline Query
@dp.inline_handler(regexp=r'(?i)wiki|wikipedia')
async def wikiInlineQueryHandler(inline_query: InlineQuery):
	randomWikiArticle = await getRandomWikiArticle()
	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Случайная статья из Википедии',
			input_message_content=InputTextMessageContent(randomWikiArticle))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# @dp.message_handler(regexp='(?i)id')
# async def idMessageHandler(message: types.Message):
# 	print(message.chat.id)


############################ FSM для генерации демотиваторов #################################


# States
class Form(StatesGroup):
	pic = State()  # Will be represented in storage as 'Form:name'
	header = State()  # Will be represented in storage as 'Form:age'
	subtitle = State()  # Will be represented in storage as 'Form:gender'


@dp.message_handler(commands='demotivator|demo|демо|демотиватор')
async def DemotivatorInlineQueryHandler(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("Отмена")

	await Form.pic.set()
	await message.answer("Отправь картинку, которую хотел бы видеть в демотиваторе", reply_markup=markup)


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='отмена|cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return

	async with state.proxy() as data:
		if len(data['pic']) > 2:
			os.remove(data['pic'])

	logging.info('Cancelling state %r', current_state)
	await state.finish()
	await message.reply('Отменено.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(content_types=['photo'], state=Form.pic)
async def process_name(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		photoName = str(time()) + ".jpg"
		data['pic'] = photoName
		await message.photo[-1].download(photoName)

	await Form.next()
	await message.answer("Что будет в заголовке демотиватора?")


@dp.message_handler(state=Form.header)
async def process_age(message: types.Message, state: FSMContext):
	while True:
		if message.text:
			break
		else:
			await message.reply("Не похоже на текст...")

	await Form.next()
	await state.update_data(header=message.text)


	await message.answer("А в подзаголовке?")


@dp.message_handler(state=Form.subtitle)
async def process_gender_invalid(message: types.Message, state: FSMContext):
	while True:
		if message.text:
			break
		else:
			await message.reply("Не похоже на текст...")

	async with state.proxy() as data:
		data['subtitle'] = message.text

	demPath = demotivatorCreator(data['pic'], data['header'], data['subtitle'])

	if '.' not in demPath:
		await message.answer(demPath)
	else:
		print(demPath)
		with open(demPath, 'rb') as photo:
			await bot.send_photo(message.chat.id, photo, caption='Демотиватор готов!')
		os.remove(demPath)

	os.remove(data['pic'])

	await state.finish()


###################################################################################

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)

#############################################################################################