from misc import dp, bot, ytApiKey

from resources.links import                         \
	foxLogoPreview,         helpImages              #

from features.mainFunctions import                  \
	yesOrNot,               orDecider,              \
	getRandomWikiArticle,   getRandomYoutubeVideo,  \
	randomPopGenerator,     randomRating            #


from aiogram.types import InlineQueryResultArticle
from aiogram.types import InputTextMessageContent
from aiogram.types import InlineQuery

from aiogram.utils import markdown


from random import choice, randint
from time import time

import re


helpList = \
	[
		[
		'Введите один из запросов ниже:',

		'',

		'',

		'Основная функциональность бота заключена в inline-командах. '
		'Команды можно вводить как строчными, так и заглавными буквами. '
		'Некоторые из них описаны здесь'
		], [
		'Решение примеров:',

		'Математическое выражение c \"=\" на конце',

		'',

		"Введите математическое выражение, состоящее из чисел и простейших операций "
		"(Лис ещё только учится!!) типа \"*\", \"/\", \"+\", \"-\", оканчивающееся на знак \"=\" "
		"и Лис посчитает в столбик результат вычислений"
	], [
		'Случайная статья из Wikipedia:',

		'\"Wiki\"',

		'https://i.ibb.co/S6mcw2F/1200px-Wikipedia-logo-svg-svg.png',

		"Введите \"wiki\" или \"wikipedia\" в любом регистре, и Лис быстро сбегает до Вики и "
		"принесёт ссылку на случайную статью из русскоязычной Википедии"
	], [
		'Ответ на вопрос - \"Да\Нет\":',

		'Вопрос, заканчивающийся на \"?\"',

		'',

		"Введите любой вопрос, не содержащий \"или\" (желательно, на который можно ответить "
		"односложно, Лис ещё плохо понимает человечий и не может изъяснятся без переводчика, "
		"для большего погружения О_о), и бот ответит на него Да или Нет"
	], [
		'Выбор одного из вариантов:',

		'Список слов через \"или\"',

		'',

		"Введите любое количество слов через \"или\" и Лис, обнюхав, выберет одно из них"
	], [
		'Оценка чего-либо:',

		'\"rate\" и после то, что должен оценить бот',

		'',

		"Введите \"rate\" в любом регистре и через пробел то, что хотите отдать на оценку Лису. "
		"Он ответит вам в десятибальной шкале с небольшим милым пояснением"
	], [
		'Случайного видео из YouTube:',

		'\"yt\" или \"youtube\"',

		'https://i.ibb.co/RDttyBT/youtube-logo-png-2069.png',

		"Введите \"yt\" или \"youtube\", чтобы получить случайное видео с ютуба, которое в данный "
		"момент просматривает Лис"
	], [
		'QR-код:',

		'\"qr\" и после то, что вы хотите зашифровать',

		'',

		'Введите \"qr\" и то, что вы хотите видеть контентом qr-кода. Бот быстро и со вкусом создаст его'
	], [
		'Или в диалоге с ботом:',

		'',

		'',

		'Напишите в личные сообщения боту по тэгу @rnfoxbot или по ссылке t.me/rnfoxbot и введите одну '
		'из следующих команд'
	], [
		'Создание демотиватора',

		'\\демотиватор или \\демо, или \\demotivator',

		'',

		'Бот создаст демотиватор из картинки и двух строк текста, которые вы ему отправите. '
		'Все взаимодействия с ботом сопровождаются подсказками, так, что вы не потеряетесь'
	],
		# [
		# 	'Или в диалоге с ботом:',
		#
		# 	'',
		#
		# 	'',
		#
		# 	''
		# ], [
		# 	'Или в диалоге с ботом:',
		#
		# 	'',
		#
		# 	'',
		#
		# 	''
		# ]
	]

# TODO: Сделать информативный и красивый /start

@dp.inline_handler(regexp=r'(?i)^help$|^\s*$')
async def helpInlineHandler(inline_query: InlineQuery):
	items = [
		InlineQueryResultArticle(
			id=str(i),
			title=helpList[i][0],
			description=helpList[i][1],
			thumb_url=helpImages[i % 5],
			input_message_content=InputTextMessageContent(helpList[i][-1]))
		for i in range(len(helpList))
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=60)


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
			description=answer,
			thumb_url='https://i.ibb.co/PmrJZxc/1280px-Gay-Pride-Flag-svg.png',
			input_message_content=InputTextMessageContent(f"Вы {answer}!"))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик ответа Да\Нет на вопрос Inline Query
@dp.inline_handler(regexp=r'(?i)^(?=.*?\?)((?!или|or).)*$')
async def questionInlineQueryHandler(inline_query: InlineQuery):
	answer = yesOrNot()
	messToUser = markdown.bold(inline_query.query) + '\n' + markdown.italic(answer)
	print(messToUser)

	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Ответ',
			thumb_url=foxLogoPreview,
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


@dp.inline_handler(regexp=r'(?i)(.+\bили|or\b.+)+')
async def OrInlineQueryHandler(inline_query: InlineQuery):
	answer = orDecider(inline_query.query).capitalize()
	messToUser = markdown.bold(inline_query.query) + '\n' + markdown.italic(answer)

	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Лис выбрал слово...',
			thumb_url=foxLogoPreview,
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик запроса случайной роры Inline Query
@dp.inline_handler(regexp=r'(?i)^\s*popa|попа\s+\d+')
async def popaInlineQueryHandler(inline_query: InlineQuery):
	_str = inline_query.query
	_str = re.sub(r'(?i)popa|попа', '', _str)
	num = int(_str.strip())

	answer = randomPopGenerator(num).strip().capitalize()
	messToUser = markdown.bold(answer)

	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Ророчка:',
			thumb_url=foxLogoPreview,
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик запроса случайной роры Inline Query
@dp.inline_handler(regexp=r'(?i)num\s+-*\d+\s+-*\d+')
async def randNumInlineQueryHandler(inline_query: InlineQuery):
	num = [int(i) for i in inline_query.query.lower().replace("num", "").split()]

	randomNumber = str(randint(num[0], num[1]))
	messToUser = markdown.italic(f"Случайное число от {num[0]} до {num[1]}:") + '\n' + \
	             markdown.bold(f'{randomNumber}')
	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title=f'Случайное число от {num[0]} до {num[1]}:',
			description=randomNumber,
			thumb_url=foxLogoPreview,
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик простейших математических выражений Inline Query
@dp.inline_handler(regexp=r'[\s\d\.\,\/\*\-\+\(\)]+=$')
async def calculationInlineQueryHandler(inline_query: InlineQuery):
	answer = str(eval(inline_query.query.replace("=", "").replace(",", ".")))
	messToUser = markdown.code(inline_query.query.replace(" ", "")) + markdown.code(answer)

	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Результат вычислений:',
			thumb_url='https://i.ibb.co/QmWSC1N/Untitled-2.png',
			description=answer,
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=50000000)


@dp.inline_handler(regexp=r'(?i)^\s*gay\b.+')
async def howMuchInlineQueryHandler(inline_query: InlineQuery):
	answer = randint(0, 100)

	_str = inline_query.query
	_str = re.sub(r'(?i)\s*gay\b\s+', '', _str)

	messToUser = markdown.italic(f"{_str} гей на {answer}%")

	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title=f'Насколько {_str} гей?',
			description="нажми, если любишь маму",
			thumb_url='https://i.ibb.co/PmrJZxc/1280px-Gay-Pride-Flag-svg.png',
			input_message_content=InputTextMessageContent(message_text=messToUser, parse_mode='MarkdownV2'))
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=9999999999)


# Обработчик запроса оценки Inline Query
@dp.inline_handler(regexp=r'(?i)rate\b\b.*')
async def RateInlineQueryHandler(inline_query: InlineQuery):
	item = inline_query.query.lower().replace("rate", '').strip()
	messToUser = randomRating(item)

	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Оценка от Лиса',
			description='Лисик вынес окончательный вердикт!',
			thumb_url=foxLogoPreview,
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
			description='Рекомендация от Лиса',
			thumb_url='https://i.ibb.co/RDttyBT/youtube-logo-png-2069.png',
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
			description='Рекомендация от Лиса',
			thumb_url='https://i.ibb.co/S6mcw2F/1200px-Wikipedia-logo-svg-svg.png',
			input_message_content=InputTextMessageContent(randomWikiArticle))
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)
