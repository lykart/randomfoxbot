import aiohttp, re, json, string, queue
import urllib.request
from random import choice, random


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


ratingList = [
	"**0/10!**\n__Лис хочет разорвать это на куски, пожертвовав собой. Мир не должен это увидеть, да и Лис не должен был"
	"...__",
	"**1/10!**\n__Кажется, Лису стало плохо. Рыжее сердечко не выдержало такого убожества__",
	"**2/10!**\n__Лис нервно царапает это и кусает, бегая вокруг. Один Бог знает, что хорошее может быть в его худшем "
	"творении__",
	"**3/10!**\n__После ежегодной лисячей вечеринки неделю назад осталось молоко. Оно уже давно скисло, но выглядит до "
	"сих пор лучше, чем это__",
	"**4/10!**\n__Лис посмотрел на это и отрыгнул вчерашнюю куриную косточку. Почему? Он и сам не знает__",
	"**5/10!**\n__Лис просто пробежал мимо по своим рыжим делам__",
	"**6/10!**\n__Лис заинтересованно смотрит на это, но боится подойти. Возможно, он увидел что-то рыжее внутри__",
	"**7/10!**\n__Лис радостно бегает вокруг и принюхивается, пытаясь определить, можно ли это съесть__",
	"**8/10!**\n__Лис быстро подбежал, схватил кусочек, и убежал. Ему определённо понравилось__",
	"**9/10!**\n__Вау! Лис стал какать радугой при виде этого!!!__",
	"**10/10!**\n__Все Лисы мира сбежались к этому. Кажется, это лучшая в мире вещь в глазал лисячьего сообщества__",
]


def randomRating():
	return choice(ratingList)


popList = [
	" ", "п", "по", "пи", "па", "пь", "по", "пa", "поо", "паа", " ", " ", "a", "и", " ", " "
]


def randomPopGenerator(n):
	_str = ''

	for i in range(n):
		_str += choice(popList)

	_str = _str.strip().replace("  ", " ")

	return _str
