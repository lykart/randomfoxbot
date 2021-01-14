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
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

		'Основная функциональность бота заключена в inline\\-командах\\. '
		'Команды можно вводить как строчными, так и заглавными буквами\\. '
		'Некоторые из них описаны здесь'
		], [
		'Решение примеров:',

		'Математическое выражение c \"\\=\" на конце',

		'2\\+2\\*2\\=',

		"Введите математическое выражение, состоящее из чисел и простейших операций "
		"\\(Лис ещё только учится\\!\\!\\) типа \"\\*\", \"/\", \"\\+\", \"\\-\", оканчивающееся на знак \"\\=\" "
		"и Лис посчитает в столбик результат вычислений"
	], [
		'Случайная статья из Wikipedia:',

		'\"Wiki\"',

		'wiki',

		"Введите \"wiki\" или \"wikipedia\" в любом регистре, и Лис быстро сбегает до Вики и "
		"принесёт ссылку на случайную статью из русскоязычной Википедии"
	], [
			'Случайное целое число:',

			'\"num\" и число от какого, после до какого',

			'num 1 10',

			'Введите \"num\" и после числа через пробел \\- границы в которых должно быть получившееся число'
	], [
		'Ответ на вопрос \\- \"Да\Нет\":',

		'Вопрос, заканчивающийся на \"?\"',

		'Хочешь кушать, Лисёнок?',

		"Введите любой вопрос, не содержащий \"или\" \\(желательно, на который можно ответить "
		"односложно, Лис ещё плохо понимает человечий и не может изъяснятся без переводчика, "
		"для большего погружения О\\_о\\), и бот ответит на него Да или Нет"
	], [
		'Выбор одного из вариантов:',

		'Список слов через \"или\"',

		'Рыжий или Огненно—красный?',

		"Введите любое количество слов через \"или\" и Лис, обнюхав, выберет одно из них"
	], [
		'Таймер:',

		'\"timer\" \(some text\) время по шаблону: 1h20m3s',

		'timer (Лис делает планку) 1m',

		'Введите \"timer\" любой текст в скобках, который будет отображаться в таймере: \\(текст\\) '
		'и после время по шаблону \"' + markdown.code("A") + 'h' + markdown.code("B") +
		'm' + markdown.code("C") + 's\" , где А \\- целое число часов, В \\- целое число минут, С \\- целое число '
		'секунд\\. Не обязательно присутствие всех блоков одновременно: можно написать \"20m5s\" или \"100s\"'
		'\n\nМожно запускать только один таймер одновременно\\! Чтобы остановить предыдущий введите inline\\-команду'
		'\"stop timer\"\\.'
	], [
		'Оценка чего\\-либо:',

		'\"rate\" и после то, что должен оценить бот',

		'rate малиновый пирог',

		"Введите \"rate\" в любом регистре и через пробел то, что хотите отдать на оценку Лису\\. "
		"Он ответит вам в десятибальной шкале с небольшим милым пояснением"
	], [
		'Случайного видео из YouTube:',

		'\"yt\" или \"youtube\"',

		'yt',

		"Введите \"yt\" или \"youtube\", чтобы получить случайное видео с ютуба, которое в данный "
		"момент просматривает Лис"
	], [
		'QR\\-код:',

		'\"qr\" и после то, что вы хотите зашифровать',

		r'qr @rnfoxbot — самый милый Лисёнок в Телеграме\\!',

		'Введите \"qr\" и то, что вы хотите видеть контентом qr—кода\\. Бот быстро и со вкусом создаст его'
	], [
		'Или в диалоге с ботом:',

		'',

		'',

		'Напишите в личные сообщения боту по тэгу @rnfoxbot или по ссылке t\\.me/rnfoxbot и введите одну '
		'из следующих команд'
	], [
		'Создание демотиватора',

		'\\демотиватор или \\демо, или \\demotivator',

		'',

		'Бот создаст демотиватор из картинки и двух строк текста, которые вы ему отправите\\. '
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
			input_message_content=InputTextMessageContent(helpList[i][-1], parse_mode='MarkdownV2'),
			reply_markup= InlineKeyboardMarkup().
				insert(InlineKeyboardButton(
					'Попробуй!',
					switch_inline_query_current_chat=helpList[i][2]
					)
				) if helpList[i][2] else None,

		)
		for i in range(len(helpList))
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)


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
			description='*cохранение интриги*',
			thumb_url='https://i.ibb.co/PmrJZxc/1280px-Gay-Pride-Flag-svg.png',
			input_message_content=InputTextMessageContent(f"Вы {answer}!"))
	]
	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


@dp.inline_handler(regexp=r'(?i)me\s+.+')
async def meInlineQueryHandler(inline_query: InlineQuery):
	text = inline_query.query
	text = text.strip().replace("  ", " ").replace("me", "")
	messToUser = markdown.bold(f"Лисёнок{text}")

	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Лисёнок ',
			description=text,
			thumb_url=foxLogoPreview,
			input_message_content=InputTextMessageContent(messToUser, parse_mode='MarkdownV2'))
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


# Обработчик ответа Да\Нет на вопрос Inline Query
@dp.inline_handler(regexp=r'(?i)^(?=.*?\?)((?!или|or).)*$')
async def questionInlineQueryHandler(inline_query: InlineQuery):
	answer = yesOrNot()
	messToUser = markdown.bold(inline_query.query) + '\n' + markdown.italic(answer)

	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title='Лис сделал выбор...',
			description=inline_query.query,
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
			description=inline_query.query,
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
			title='Ророчка *flushed*',
			description=f"из {num} частей!!1",
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
			thumb_url=foxLogoPreview,
			description=f"{num[0]}, {num[1]}\n"
			            f"Что же он выберет?",
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

	# TODO: доделать уже наконец-то gay (для одного пользователя - одно значение)

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
			title='Лисик вынес вердикт!',
			description=f'что же он думает о {item}???',
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
