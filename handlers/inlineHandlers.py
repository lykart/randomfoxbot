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
			'Введи один из запросов ниже:',

			'Я тебе помогу 😊',

			'',

			'Основная функциональность Лиса заключена в inline\\-командах\\. '
			'Команды можно вводить как строчными, так и заглавными буквами\\. '
			'Некоторые из них описаны здесь\\. Кликнув на конкретную, можно получить полное описание С ПРИМЕРОМ\\!'
	], [
		'Решение примеров 🤓',

		'Математическое выражение c \"=\" на конце',

		'2+2*2=',

		"Введите математический пример из чисел и простейших операций, "
		"вроде 2\\+2\\*2, ну, или 8/2; Вообще какое хотите\\! Главное, оканчивающийся на знак \"\\=\"\\. "
		"Лис посчитает в столбик результат вычислений \\(Я ещё только учусь, не ругайтесь 😣\\!\\!\\)"
	], [
		'Случайную статью из вики? 😳',

		'Тогда напиши \"wiki\"',

		'wiki',

		"Введи в чат \"wiki\" или \"wikipedia\", и Лисёнок быстро сбегает до Вики и "
		"принесёт ссылку на случайную статью из её русскоязыного раздела\\. \\(И еще немного пыли на лапках\\)"
	], [
		'Придумаю рандомное число 😎',

		'\"num\" и два числа-границы',

		'num 1 10',

		'Введи \"num\", а после — два числа через пробел\\. Они задают границы в которых должно быть получившееся число'
	], [
		'Отвечу на односложный вопрос 😏',

		'Вопрос, заканчивающийся на \"?\"',

		'Хочешь резвиться, Лисёнок?',

		"Задай мне вопрос, не содержащий \"или\" \\(желательно, на который можно ответить "
		"односложно, а то я пока ещё плохо понимаю человечий и не могу разговаривать без переводчика 😖\\)"
	], [
		'Поиграю в советчика 🤠',

		'Отправь мне список слов через \"или\"',

		'Рыжий или Огненно-красный?',

		"Не можешь выбрать что\\-то? Напиши мне список вариантов, разделяя их словом \"или\", и я, обнюхав и взвесив все за и против, выберу одно из них\\!"
	], [
		'Буду твоим личным таймером 🤗',

		'Напиши \"timer\" и время по шаблону 00h00m0s',

		'timer (Лис варит борщ) 1h5m',

		'Введи для начала команду \"timer\", затем любой текст в скобках, который будет отображаться в таймере: \\(текст 😳\\) '
		'и после время по шаблону: \"' + markdown.code("A") + 'h' + markdown.code("B") +
		'm' + markdown.code("C") + 's\" , где А \\- целое число часов, В \\- целое число минут, С \\- целое число '
		'секунд\\. Необязательно присутствие всех блоков одновременно: можно написать \"20m5s\" или \"100s\"\\.'
		'\n\nК сожалению, я не многозадачный, поэтому один пользователь может запускать только один таймер одновременно\\! 😯'
		'\n\nЧтобы остановить текущий таймер введи inline\\-команду \"stop timer\"\\ или просто нажми на кнопку под ним'
	], [
		'Стану оценщиком чего-либо 🤩',

		'\"rate\" и то, что я должен оценить ',

		'rate шефбургер',

		"Напиши \"rate\" в любом регистре и через пробел то, что хочешь отдать на оценку \\(~растерзание~\\)\\.😶 "
	], [
		'Скину интересное видео из YT 😋',

		'\"yt\" или \"youtube\"',

		'yt',

		"Введи \"yt\" или \"youtube\", чтобы я принёс тебе случайное видео с ютуба, которое я недавно посмотрел"

	], [
		'QR-код 🤫',

		'\"qr\" и то, что хочешь зашифровать',

		r'qr @rnfoxbot — самый умный и милый Лисёнок во всём Телеграме!',

		'Напиши \"qr\" и затем то, что ты хочешь зашифровать в qr\\-код\\. Я быстро создам вкусную картинку\\-код и отправлю тебе'
	], [
		'Или у Лисёнка в ЛС:',

		'',

		'',

		'Напиши мне в личные сообщения по тэгу @rnfoxbot или по ссылке t\\.me/rnfoxbot и понажимай на кнопки \\(для начала \\start\\)'
		''
	], [
		'Создание демотиватора',

		'/демотиватор',

		'',

		'Лисёнок нарисует демотиватор из картинки и двух строк текста, которые вы ему отправите\\. '
		'Все взаимодействия с Лисёнком сопровождаются подсказками, так, что ты не потеряешься'
	], [
		'Генерация QR-кода',

		'/qr',

		'',

		'Лисёнок закодирует всю информацию, которую вы ему отправите \\(учтите, что вместительность QR\\-кодов очень невелика\\)'
	],
		# [
		#   'Или в диалоге с ботом:',
		#
		#   '',
		#
		#   '',
		#
		#   ''
		# ], [
		#   'Или в диалоге с ботом:',
		#
		#   '',
		#
		#   '',
		#
		#   ''
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

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=999999)


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
