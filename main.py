from primaryFunctions import \
	getRandomWikiArticle, orDecider, toBold, toItalic, toMonospace, yesOrNot, randomRating, randomPopGenerator, \
	getRandomYoutubeVideo, \
	wikiArticlesQueue, ytVideosQueue
import asyncio, os
from telethon import TelegramClient, events
from random import choice, randint

# from flask import Flask
#
# randomFoxBotWeb = Flask(__name__)
#
#
# @randomFoxBotWeb.route('/')
# def hello_world():
# 	return 'Hello World!'
#
#
# if __name__ == '__main__':
#     randomFoxBotWeb.run()


# Инициализация работы бота

api_id = int(os.environ['api_id'])
api_hash = os.environ["api_hash"]
bot_token = os.environ["bot_token"]
ytApiKey = os.environ["ytApiKey"]

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
loop = asyncio.get_event_loop()



# Генератор очереди всего рандомного
async def queueGenerator():
	# if wikiArticlesQueue.maxsize / (wikiArticlesQueue.qsize() + 1) >= 3:
	# 	num = wikiArticlesQueue.maxsize - wikiArticlesQueue.qsize()
	# 	print(wikiArticlesQueue.qsize())
	#
	# 	bot.loop.create_task(getRandomWikiArticle())
	#
	# if ytVideosQueue.maxsize / (ytVideosQueue.qsize() + 1) >= 3:
	# 	num = ytVideosQueue.maxsize - ytVideosQueue.qsize()
	# 	print(ytVideosQueue.qsize())
	#
	# 	bot.loop.create_task(getRandomYoutubeVideo())

	global wikiArticlesQueue

	randomWikiArticle = await getRandomWikiArticle()
	print(randomWikiArticle)

	wikiArticlesQueue.put(randomWikiArticle)


# # Обработчик исключений inline query
# @bot.on(events.InlineQuery)
# async def otherInlineQueryHandler(event):
# 	builder = event.builder
# 	print("inline: ", event.text)
#
# 	await event.answer([
# 		builder.article(event.text,
# 		                text="A"),
# 	])


# Обработчик запроса "Who am I?" Inline Query
@bot.on(events.InlineQuery(pattern=r'(?i)who\s*am\s*i'))
async def whoAmIInlineQueryHandler(event):
	builder = event.builder

	LGBTQKAplus = [
		"Гей", "Пидорас", "Лесбиян04ка", "FTM трансгендер", "MTF трансгендер",
		"Трансформер", "Мороженое \"Радуга\"", "Би", "Квирчик", "Апельсин", "Вертолёт АПАЧИ", "Big Poppa",
		"Small Joppa", "Агендер", "Асексуал", "Ким 5+", "Лох", "Валя Беляев", "Голубой", "Фанат зелёного гей флага",
		"забанены в твиттере"
	]

	await event.answer([
		builder.article('Кто я из суперсемейки?', text=f"Я {choice(LGBTQKAplus)}!")
	])


# Обработчик запроса "Who am I?" Inline Query
@bot.on(events.InlineQuery(pattern=r'(?i)^\s*gay$'))
async def howMuchInlineQueryHandler(event):
	builder = event.builder

	await event.answer([
		builder.article('Насколько я гей?', text=f"Я Гей на {randint(0, 100)}%")
	])


# Обработчик меню help inline query
@bot.on(events.InlineQuery(pattern=r'(?i)^help$|^\s*$'))
async def helpInlineQueryHandler(event):
	builder = event.builder

	await event.answer({
		builder.article('Введите математическое выражение, оканчивающееся на \"=\"',
		                text="Введите математическое выражение, состоящее из чисел и простейших операций "
		                     "(Лис ещё только учится!!) типа \"*\", \"/\", \"+\", \"-\", оканчивающееся на знак \"=\" "
		                     "и Лис посчитает в столбик результат вычислений"),
		builder.article('Введите \"wiki\" для получения случайной статьи',
		                text="Введите \"wiki\" или \"wikipedia\" в любом регистре, и Лис быстро сбегает до Вики и "
		                     "принесёт ссылку на случайную статью из русскоязычной Википедии"),
		builder.article('Введите вопрос, и бот ответит Да\Нет',
		                text="Введите любой вопрос, не содержащий \"или\" (желательно, на который можно ответить "
		                     "односложно, Лис ещё плохо понимает человечий и не может изъяснятся без переводчика, "
		                     "для большего погружения О_о), и бот ответит на него Да или Нет"),
		builder.article('Введите список слов через \"или\", и бот выберет одно',
		                text="Введите любое количество слов через \"или\" и Лис, обнюхав, выберет одно из них"),
		builder.article('Введите \"rate\" и после то, что должен оценить бот',
		                text="Введите \"rate\" в любом регистре и через пробел то, что хотите отдать на оценку Лису. "
		                     "Он ответит вам в десятибальной шкале с небольшим милым пояснением"),
		builder.article('Введите \"yt\" для получения случайного видео',
		                text="Введите \"yt\" или \"youtube\", чтобы получить случайное видео с ютуба, которое в данный "
		                     "момент просматривает Лис"),
	})


# Обработчик запроса случайного видео с YouTube Inline Query
@bot.on(events.InlineQuery(pattern=r'(?i)yt|youtube'))
async def youtubeInlineQueryHandler(event):
	builder = event.builder

	randomYoutubeVideo = getRandomYoutubeVideo(ytApiKey)
	print(randomYoutubeVideo)
	await event.answer([
		builder.article('Случайное видео с YouTube', text=randomYoutubeVideo, link_preview=True)
	])


# Обработчик запроса случайной статьи Википедии Inline Query
@bot.on(events.InlineQuery(pattern=r'(?i)wiki|wikipedia'))
async def wikiInlineQueryHandler(event):
	builder = event.builder

	if wikiArticlesQueue.not_full:
		await queueGenerator()

	randomWikiArticle = wikiArticlesQueue.get()
	print("Inline request is processed")

	await event.answer([
		builder.article('Случайная статья из Википедии', text=randomWikiArticle, link_preview=True)
	])


# Обработчик запроса случайной роры Inline Query
@bot.on(events.InlineQuery(pattern=r'(?i)popa\s+\d+'))
async def popaInlineQueryHandler(event):
	builder = event.builder
	num = int(event.text.replace("popa", "").strip())

	messToUser = toBold(randomPopGenerator(num).strip().capitalize())

	await event.answer([
		builder.article('Ророчка', text=messToUser)
	])


# Обработчик запроса оценки Inline Query
@bot.on(events.InlineQuery(pattern=r'(?i)rate\b.*'))
async def RateInlineQueryHandler(event):
	builder = event.builder

	messToUser = toBold(event.text.replace("rate", '').strip().capitalize()) + '\n' + (randomRating())

	await event.answer([
		builder.article('Оценка от Лиса', text=messToUser)
	])


# Обработчик запроса случайной статьи Википедии Inline Query
@bot.on(events.InlineQuery(pattern=r'(?i)(.+\bили\b.+)+'))
async def OrInlineQueryHandler(event):
	builder = event.builder

	messToUser = toBold(event.text) + '\n' + toItalic(orDecider(event.text).capitalize())

	await event.answer([
		builder.article('Одно из слов', text=messToUser)
	])


# Обработчик ответа Да\Нет на вопрос Inline Query
@bot.on(events.InlineQuery(pattern=r'(?i)^(?=.*?\?)((?!или).)*$'))
async def questionInlineQueryHandler(event):
	builder = event.builder

	messToUser = toBold(event.text) + '\n' + toItalic(yesOrNot())
	await event.answer([
		builder.article('Да или Нет', text=messToUser)
	])


# Обработчик простейших математических выражений Inline Query
@bot.on(events.InlineQuery(pattern=r'[\s\d\.\,\/\*\-\+\(\)]+=$'))
async def calculationInlineQueryHandler(event):
	builder = event.builder

	print("evaluation")
	messToUser = toMonospace(event.text.replace(" ", "")) + toMonospace(
		str(eval(event.text.replace("=", "").replace(",", "."))))
	print(messToUser)

	await event.answer([
		builder.article('Результат вычислений', text=messToUser)
	])


# Обработчик на вопрос с вариантам (с "или")
@bot.on(events.NewMessage(pattern=r'(?i)(.+\bили\b.+)+'))
async def OrMessageArrivedHandler(event):
	print("Выбор из вариантов")

	choiceIs = orDecider(event.text).capitalize()

	# Отправка ответа
	await bot.send_message(event.from_id, choiceIs)


# Обработчик на вопрос (без "или")
@bot.on(events.NewMessage(pattern=r'(?i)^(?=.*?\?)((?!или).)*$'))
async def questionMessageArrivedHandler(event):
	await bot.send_message(event.from_id, yesOrNot())

# Обработчик на любое сообщение
@bot.on(events.NewMessage())
async def anyMessageArrivedHandler(event):
	messStr = event.text.lower()

	if messStr[-3:] == ' да' or messStr == 'да':
		reply = 'ПИЗДА!'
	elif messStr[-4:] == ' нет' or messStr == 'нет':
		reply = 'ПИДОРА ОТВЕТ!'
	else:
		return

	await bot.send_message(event.from_id, reply)


bot.run_until_disconnected()

# Передаю пламенный СПАСИБО Диме
