import aiohttp, re, json, string, queue
import urllib.request
from random import choice, random
import pymorphy2


morph = pymorphy2.MorphAnalyzer()

# Очереди рандомного контента (для ускорения работы бота)
wikiArticlesQueue = queue.Queue(maxsize=30)
ytVideosQueue = queue.Queue(maxsize=30)


async def getRandomYoutubeVideo(ytApiKey):
	count = 1
	_random = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(3))

	urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(ytApiKey,count,_random)
	webURL = urllib.request.urlopen(urlData)
	data = webURL.read()
	encoding = webURL.info().get_content_charset('utf-8')
	results = json.loads(data.decode(encoding))

	# ytVideosQueue.put(f"https://www.youtube.com/watch?v={[i['id']['videoId'] for i in results['items']][0]}")

	return f"https://www.youtube.com/watch?v={[i['id']['videoId'] for i in results['items']][0]}"


# Возвращает ссылку на случайную статью из русской википедии
async def getRandomWikiArticle():
	wikiUrl = "https://ru.wikipedia.org/w/api.php?action=query&format=json&list=random&rnnamespace=0"

	async with aiohttp.ClientSession() as session:
		async with session.get(wikiUrl) as response:
			print("Wiki request is get")
			randomWikiArticle_json = await response.json()

			# wikiArticlesQueue.put(f"https://ru.wikipedia.org/wiki/?curid="
			#                       f"{randomWikiArticle_json['query']['random'][0]['id']}")

			return f"https://ru.wikipedia.org/wiki/?curid={randomWikiArticle_json['query']['random'][0]['id']}"


# Выбирает один ответ из n из сообщения пользователя (разделяет маркером "или")
def orDecider(userMessage):
	userMessage = userMessage.lower()

	# Парсинг строки по вариантам выбора
	listOfVariants = userMessage.split('или')
	fnd = re.compile(r'\b[\w \S-]+\b')

	for i in range(len(listOfVariants)):
		listOfVariants[i] = fnd.findall(listOfVariants[i])

	return choice(listOfVariants)[0]


# Случайно с равным шансов возвращает Да или Нет
def yesOrNot():
	return 'Да' if random() <= 0.5 else 'Нет'


# Перевод текста в жирный с помощью Markdown
def toBold(message):
	return '**' + message + '**'


# Перевод текста в курсив с помощью Markdown
def toItalic(message):
	return '__' + message + '__'


# Перевод текста в моноширинный с помощью Markdown
def toMonospace(message):
	return '`' + message + '`'


def randomRating(item):
	item = item if len(item) != 0 else 'это'

	if ' ' in item:
		item = item.split()
		if len(item) > 5:
			return "Слишком уж вы сложную вещь для оценивания выбрали. Лис не понимает :("
	else:
		item = [item]

	item = [morph.parse(i)[0] for i in item]

	ratingList = [
		[r"*0/10\!*" + '\n' + "_Лис хочет разорвать $$$ на куски, пожертвовав собой\. Мир не должен этого увидеть\.\.\._", 'accs'],
		[r"*1/10\!*" + '\n' + "_Кажется, Лису стало плохо\. Рыжее сердечко не выдержало такого убожества как $$$_", 'nomn'],
		[r"*2/10\!*" + '\n' + "_Лис нервно царапает $$$ и кусает, бегая вокруг\. Один Бог знает, что хорошее может быть в этой мерзости_", 'accs'],
		[r"*3/10\!*" + '\n' + "_После ежегодной лисячей вечеринки неделю назад осталось молоко\. Оно уже давно скисло, но выглядит до сих пор лучше, чем $$$_", 'nomn'],
		[r"*4/10\!*" + '\n' + "_Лис посмотрел на $$$ и отрыгнул вчерашнюю куриную косточку\. Почему? Он и сам не знает_", 'accs'],
		[r"*5/10\!*" + '\n' + "_Лис просто пробежал мимо по своим рыжим делам, не заметив $$$_", 'gent'],
		[r"*6/10\!*" + '\n' + "_Лис заинтересованно смотрит на $$$, но боится подойти\. Возможно, он почуял рыжую ауру_", 'accs'],
		[r"*7/10\!*" + '\n' + "_Лис радостно бегает вокруг $$$ и принюхивается, пытаясь определить, можно ли это съесть_", 'gent'],
		[r"*8/10\!*" + '\n' + "_Лис быстро подбежал, схватил кусочек $$$, и убежал\. Ему определённо понравилось_", 'gent'],
		[r"*9/10\!*" + '\n' + "_Вау\! Лис стал какать радугой при виде $$$\!\!\!_", 'gent'],
		[r"*10/10\!*" + '\n' + "_Все Лисы мира сбежались к $$$\. Кажется, лучше этого в глазах лисячьего сообщества нет ничего_", 'datv'],
	]
	_choice = choice(ratingList)
	print(_choice)
	print(item)

	inflectedItems = []
	for i in item:
		try:
			temp = i.inflect({f'{_choice[1]}'})[0]
		except:
			temp = i[0]
		print(temp)
		inflectedItems.append(temp)
		print(inflectedItems)

	print(inflectedItems)
	rating = _choice[0].replace('$$$', ' '.join(inflectedItems))
	print(rating)
	return rating


popList = [
	" ", "п", "по", "пи", "па", "пь", "по", "пa", "поо", "паа", " ", " ", "a", "и", " ", " "
]


def randomPopGenerator(n):
	_str = ''

	for i in range(n):
		_str += choice(popList)

	_str = _str.strip()
	re.sub(r'\s{2,}', ' ', _str)

	return _str