import re
from time import time

from PIL import Image, ImageDraw, ImageFont

pathToFont = 'times.ttf'


def intBox(x, y):
	return (int(x), int(y))


# Обрезает с каждой стороны изображения *padding* пикселей
def cropImage(image, padding):
	return image.copy().crop((int(padding), int(padding), int(image.width - padding), int(image.height - padding)))


# Подгоняет отношение сторон и размер изображения под приемлимые значения
def picExeption(pic):
	height = pic.height
	width = pic.width

	# TODO: Сделать ограничение по максимальному
	#  размеру изображения для экономии ресурсов

	minSizeOfSidePix = 300  # Минимальный размер картинки внутри демотиватора в пикселях
	if height < minSizeOfSidePix and width < minSizeOfSidePix:
		resizeCoeff = minSizeOfSidePix / min(width, height)

		width = int(resizeCoeff * width)
		height = int(resizeCoeff * height)
		pic = pic.resize((width, height), resample=Image.BICUBIC)

	# print(pic.size, "minPxCount")

	maxAspectRatio = 4 / 3
	if width / height > maxAspectRatio or height / width > maxAspectRatio:
		if width == max(width, height):
			height = int(width / maxAspectRatio)
		else:
			width = int(height / maxAspectRatio)

		pic = pic.resize((width, height), resample=Image.BICUBIC)

	return pic


# Переносит с n-ного слова с конца на новую строку
def textLineBreak(text, n):
	temp = text[::-1].replace('\n', ' ').replace(' ', '\n', n).replace('\n', ' ', n - 1)
	return temp[::-1]


# Удаление лишних пробелов
def textPreparation(text):
	text = re.sub('\s+', ' ', text)
	return text.strip()


# Проверка, является ли изображением, обрабатываемым PIL
def isPic(pic):
	try:
		pic.copy()
	except:
		return False
	return True


def tryToMatchTextWidthByFontSize(txt, targetFontSize, txtFieldWidth, howMuchCanFontChange):
	_font = ImageFont.truetype(pathToFont, targetFontSize)

	txtDrawer = ImageDraw.Draw(
		Image.new('RGB', (1, 1), (0, 0, 0))
	)
	txtWidth = txtDrawer.multiline_textsize(txt, font=_font)[0]

	fontSize = targetFontSize
	n = 2
	while txtWidth > txtFieldWidth:
		if n <= howMuchCanFontChange:
			fontSize -= 2
			n += 2

			if fontSize <= 5:
				raise ValueError("Нечитаемый размер шрифта после попытки "
				                 "вставить в границы демотиватора")

			_font = ImageFont.truetype(pathToFont, fontSize)
			txtWidth = txtDrawer.multiline_textsize(txt, font=_font)[0]

			# print(txtWidth, txtFieldWidth, fontSize)
		else:
			raise ValueError("Слишком длинный текст: невозможно "
			                 "вставить в границы демотиватора")

	return fontSize


def minimizingTextWidthByLiningChange(txt: str, fontSize: int, txtFieldWidth: int, wordsCount: int) -> str:
	_font = ImageFont.truetype(pathToFont, fontSize)

	txtDrawer = ImageDraw.Draw(
		Image.new('RGB', (1, 1), (0, 0, 0))
	)

	txtWidth = txtDrawer.multiline_textsize(txt, font=_font)[0]
	minSubTxtWidth = txtWidth

	n = int(wordsCount / 2)
	breakedWords = n

	for i in range(-2, 2):

		if n + i > wordsCount:
			break
		elif not n + i >= 0:
			continue

		txt = textLineBreak(txt, n + i)
		txtWidth = txtDrawer.multiline_textsize(txt, font=_font)[0]

		if txtWidth < minSubTxtWidth:
			minSubTxtWidth = txtWidth
			breakedWords = n + i

	txt = textLineBreak(txt, breakedWords)

	return txt


# Обрабатывает текст так, чтобы он влез в картинку
def textException(txtDrawer, txt, txtFieldWidth, targetFontSize: int,
                  canLiningChange: bool, howMuchCanFontChange: int = 0):
	fontSize = targetFontSize
	_font = ImageFont.truetype(pathToFont, fontSize)
	txtWidth = txtDrawer.multiline_textsize(txt, font=_font)[0]

	if howMuchCanFontChange:
		try:
			fontSize = tryToMatchTextWidthByFontSize(txt, targetFontSize, txtFieldWidth, howMuchCanFontChange)
			return txt, fontSize
		except:
			pass

	wordsCount = len(textPreparation(txt).split())
	if canLiningChange and wordsCount > 1:
		txt = minimizingTextWidthByLiningChange(txt, targetFontSize, txtFieldWidth, wordsCount)

		txtWidth = txtDrawer.multiline_textsize(txt, font=_font)[0]
		if txtWidth < txtFieldWidth:
			return txt, fontSize

	if howMuchCanFontChange and canLiningChange:
		try:
			fontSize = tryToMatchTextWidthByFontSize(txt, targetFontSize, txtFieldWidth, howMuchCanFontChange)
			return txt, fontSize
		except:
			pass

	if txtWidth > txtFieldWidth:
		raise ValueError("Слишком длинный текст")


def zeroIfNone(x):
	return x if x else 0


def getBackWidthFromPicWidth(picWidth):
	padding = 1 / 9  # от размера изображения по каждой из сторон
	paddingXPx = int(picWidth * padding)

	return picWidth + paddingXPx * 2


# Функция создания картинки подписи
def txtPicCreator(hTxt, picWidth=None, subTxt=None, backWidth=None, picPath=None):
	if backWidth:
		pass
	elif picWidth:
		backWidth = getBackWidthFromPicWidth(picWidth)
	elif picPath:
		pic = Image.open(picPath)
		pic = picExeption(pic)

		backWidth = getBackWidthFromPicWidth(pic.width)
		pic.close()
	else:
		raise ValueError("Данных аргументов недостаточно")

	txtPaddingCoeff = 1 / 18  # от размера самого демотиватора
	txtPadding = int(backWidth * txtPaddingCoeff)

	txtFieldWidth = backWidth - (txtPadding * 2)

	txtPic = Image.new('RGB', (10, 10), (0, 0, 0))
	txtDrawer = ImageDraw.Draw(txtPic)
	textColor = (255, 255, 255)

	headerTargetFontSize = int(txtFieldWidth / 9)
	try:
		temp = textException(txtDrawer, hTxt, txtFieldWidth, headerTargetFontSize,
		                     howMuchCanFontChange=30, canLiningChange=True)
	except ValueError:
		# print(exc, ": Заголовок")
		raise ValueError("Слишком длинный заголовок", "header")

	hTxt, headerFontSize = temp[0], temp[1]

	headerFont = ImageFont.truetype(pathToFont, headerFontSize)
	txtSize = txtDrawer.multiline_textsize(hTxt, font=headerFont)
	headerWidth, headerHeight = txtSize[0], txtSize[1]

	headerBox = intBox((backWidth / 2) - (headerWidth / 2), txtPadding / 3)

	if subTxt:
		subTxtPadding = headerHeight * 0.15
		subFontSize = int(headerFontSize * 0.6)

		try:
			temp = textException(txtDrawer, subTxt, txtFieldWidth, subFontSize,
			                     howMuchCanFontChange=20, canLiningChange=True)
		except ValueError:
			# print(exc, ": Подзаголовок")
			raise ValueError("Слишком длинный подзаголовок", "subtitle")

		subTxt, fontSize = temp[0], temp[1]
		subFont = ImageFont.truetype(pathToFont, fontSize)
		subTxtWidth, subTxtHeight = txtDrawer.multiline_textsize(subTxt, font=subFont)

		subtitleBox = intBox(backWidth / 2 - subTxtWidth / 2, headerBox[1] + headerHeight + subTxtPadding)

		textHeight = headerHeight + subTxtHeight + subTxtPadding
	else:
		textHeight = headerHeight

	txtPic = txtPic.resize(intBox(backWidth, textHeight + txtPadding * 1.5))

	txtDrawer = ImageDraw.Draw(txtPic)
	txtDrawer.multiline_text(headerBox, hTxt, font=headerFont, fill=textColor, align='center')

	if subTxt:
		txtDrawer.multiline_text(subtitleBox, subTxt, font=subFont, fill=textColor, align='center')

	return txtPic


# Функция создания белой рамки
def frameCreator(picSize, frameSize):
	picWidth, picHeight = picSize

	frameSizeBox = intBox(picWidth + frameSize * 8, picHeight + frameSize * 8)
	frame = Image.new('RGB', frameSizeBox, (255, 255, 255))

	blackSizeBox = intBox(picWidth + frameSize * 6, picHeight + frameSize * 6)
	black = Image.new('RGB', blackSizeBox, (0, 0, 0))

	frame.paste(black, (frameSize, frameSize, frameSize + blackSizeBox[0], frameSize + blackSizeBox[1]))

	return frame


# Если Х меньше нуля, возвращает 1
def atLeastOne(x):
	return x if x > 0 else 1


# Основная функция создания демотиватора
def demotivatorCreator(picPath, headerTxt=None, subtitleTxt=None, txtPic=None):
	pic = Image.open(picPath)

	pic = picExeption(pic)
	picWidth, picHeight = pic.size

	backWidth = getBackWidthFromPicWidth(picWidth)
	paddingXPx = int((backWidth - picWidth) / 2)

	padding = paddingXPx / backWidth
	paddingYPx = int(picHeight * padding)

	if not txtPic:
		headerTxt = textPreparation(headerTxt)
		subtitleTxt = textPreparation(subtitleTxt)

		try:
			txtPic = txtPicCreator(hTxt=headerTxt, subTxt=subtitleTxt, picWidth=backWidth)
		except ValueError as exceptiopn:
			# print(exceptiopn)
			raise exceptiopn

	else:
		backWidth = txtPic.width

	backSize = intBox(backWidth, picHeight + paddingYPx + txtPic.height)
	background = Image.new('RGB', backSize, (0, 0, 0))
# print("back", backWidth)

	frameSize = atLeastOne(int(min(background.width, background.height) / 250))
	frame = frameCreator(pic.size, frameSize)

	frameBox = (paddingXPx - frameSize * 4, paddingYPx - frameSize * 4,
	            paddingXPx - frameSize * 4 + frame.size[0], paddingYPx - frameSize * 4 + frame.size[1])

	background.paste(txtPic, (0, picHeight + paddingYPx))
	background.paste(frame, frameBox)
	background.paste(pic, (paddingXPx, paddingYPx, paddingXPx + picWidth, paddingYPx + picHeight))

	photoPath = str(time()) + ".jpg"
	background.save(photoPath)

	return photoPath
