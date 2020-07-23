from PIL import Image, ImageDraw, ImageFont
import re
from time import time


def intBox(x, y):
	return (int(x), int(y))


def cropImage(image, padding):
	return image.copy().crop((int(padding), int(padding), int(image.width - padding), int(image.height - padding)))


def picExeption(pic):
	height = pic.height
	width = pic.width

	minSizeOfSidePix = 100
	if height < minSizeOfSidePix and width < minSizeOfSidePix:
		resizeCoeff = 110 / min(width, height)

		width = int(resizeCoeff * width)
		height = int(resizeCoeff * height)
		pic = pic.resize((width, height), resample=Image.BICUBIC)

		# print(pic.size, "minPxCount")

	maxAspectRatio = 5 / 4
	if width / height > maxAspectRatio or height / width > maxAspectRatio:
		if width == max(width, height):
			height = int(width / maxAspectRatio)
		else:
			width = int(height / maxAspectRatio)

		pic = pic.resize((width, height), resample=Image.BICUBIC)

		# print(pic.size, "AR")

	# print(width, height)

	return pic


def textLineBreak(text, n):
	temp = text[::-1].replace('\n', ' ').replace(' ', '\n', n).replace('\n', ' ', n-1)
	return temp[::-1]


def textPreparation(text):
	text = re.sub('\s+', ' ', text)
	return text.strip()

def isPic(pic):
	try:
		pic.copy()
	except:
		return False
	return True


def textExeption(txtDrawer, txt, txtFieldBox, pathToFont, fontSize, canFontChange, howMuchCanFontChange, canLiningChange):
	txtFieldWidth, txtFieldHeight = txtFieldBox

	_font = ImageFont.truetype(pathToFont, fontSize)
	txtWidth = txtDrawer.multiline_textsize(txt, font=_font)[0]

	if txtWidth > txtFieldWidth:
		if canLiningChange:
			minSubTxtWidth = txtDrawer.multiline_textsize(txt, font=_font)[0]
			n = int((txt.count(" ") + 1) / 2)
			breakedWords = 0

			for i in range(-2, 2):
				if not (n + 1 >= 0):
					continue

				subTxt = textLineBreak(txt, n + i)
				txtWidth = txtDrawer.multiline_textsize(subTxt, font=_font)[0]

				if txtWidth < minSubTxtWidth:
					minSubTxtWidth = txtWidth
					breakedWords = n + i

			txt = textLineBreak(txt, breakedWords)

	m = 2
	while txtWidth > txtFieldWidth and m <= howMuchCanFontChange and canFontChange:
		fontSize -= 2
		m += 2

		if fontSize <= 0:
			break

		_font = ImageFont.truetype(pathToFont, fontSize)
		txtWidth = txtDrawer.multiline_textsize(txt, font=_font)[0]

		print(txtWidth, txtFieldWidth, fontSize, m)

	if txtWidth > txtFieldWidth:
		return "Error"

	return (txt, fontSize)


def txtPicCreator(hTxt, subTxt, txtFieldSize, txtFieldPos, picSize):
	txtFieldWidth = txtFieldSize[0]
	txtFieldHeight = txtFieldSize[1]

	pathToFont = 'times.ttf'

	txtPic = Image.new('RGBA', picSize, (0, 0, 0, 0))
	txtDrawer = ImageDraw.Draw(txtPic)
	textColor = (255, 255, 255, 230)


	fontSize = int(min(txtFieldWidth / 3.5, txtFieldHeight) / 1.9)
	temp = textExeption(txtDrawer, hTxt, txtFieldSize, pathToFont, fontSize,
		canFontChange=True, howMuchCanFontChange=45, canLiningChange=False)

	if temp == "Error":
		return "Too long header text"

	hTxt, fontSize = temp[0], temp[1]

	headerFont = ImageFont.truetype(pathToFont, fontSize)
	txtSize = txtDrawer.multiline_textsize(hTxt, font=headerFont)
	headerWidth, headerHeight = txtSize[0], txtSize[1]

	headerBox = intBox(txtFieldPos[0] + txtFieldWidth / 2 - headerWidth / 2, txtFieldPos[1])
	txtDrawer.multiline_text(headerBox, hTxt, font=headerFont, fill=textColor, align='center')

	# int(min(txtFieldWidth / 3.5, txtFieldHeight) / 3.9)
	fontSize = int(fontSize * 0.6)
	temp = textExeption(txtDrawer, subTxt, txtFieldSize, pathToFont, fontSize,
	    canFontChange=True, howMuchCanFontChange=16, canLiningChange=True)

	if temp == "Error":
		return "Too long subtitle text"

	subTxt, fontSize = temp[0], temp[1]
	subFont = ImageFont.truetype(pathToFont, fontSize)
	subTxtWidth = txtDrawer.multiline_textsize(subTxt, font=subFont)[0]

	subtitleBox = intBox(txtFieldPos[0] + txtFieldWidth / 2 - subTxtWidth / 2, txtFieldPos[1] + headerHeight * 1.15)
	txtDrawer.multiline_text(subtitleBox, subTxt, font=subFont, fill=textColor, align='center')

	return txtPic


def frameCreator(picSize, frameSize):
	picWidth, picHeight = picSize

	frameSizeBox = intBox(picWidth + frameSize * 8, picHeight + frameSize * 8)
	frame = Image.new('RGB', frameSizeBox, (255, 255, 255))

	blackSizeBox = intBox(picWidth + frameSize * 6, picHeight + frameSize * 6)
	black = Image.new('RGB', blackSizeBox, (0, 0, 0))

	frame.paste(black, (frameSize, frameSize, frameSize + blackSizeBox[0], frameSize + blackSizeBox[1]))

	return frame


def demotivatorCreator(picPath, headerTxt, subtitleTxt):
	pic = Image.open(picPath)

	headerTxt = textPreparation(headerTxt)
	subtitleTxt = textPreparation(subtitleTxt)

	pic = picExeption(pic)
	picWidth, picHeight = pic.size

	padding = 1/9  # от размера изображения по каждой из сторон
	paddingXPx = int(picWidth * padding)
	paddingYPx = int(picHeight * padding)

	textHeightPx = int(picHeight / 3.7)
	textFieldHeightPx = int(textHeightPx * 1.3)

	backSize = intBox(picWidth + paddingXPx * 2, picHeight + textFieldHeightPx + paddingYPx)
	background = Image.new('RGBA', backSize, (0, 0, 0, 255))

	frameSize = int(min(background.width, background.height) / 250)
	frame = frameCreator(pic.size, frameSize)
	frameBox = (paddingXPx - frameSize * 4, paddingYPx - frameSize * 4,
	            paddingXPx - frameSize * 4 + frame.size[0], paddingYPx - frameSize * 4 + frame.size[1])

	background.paste(frame, frameBox)

	txtPadding = 1/14 # от размера самого демотиватора
	txtPaddingPx = int(background.width * txtPadding / 2)

	txtPic = txtPicCreator(headerTxt, subtitleTxt, intBox(background.width - txtPaddingPx * 2, textHeightPx),
	                       intBox(txtPaddingPx, paddingYPx + picHeight + txtPaddingPx / 2.5), background.size)

	if not isPic(txtPic):
		return txtPic

	background.paste(pic, (paddingXPx, paddingYPx, paddingXPx + picWidth, paddingYPx + picHeight))
	demotivatorPic = Image.alpha_composite(background, txtPic)

	photoPath = str(time()) + ".png"
	demotivatorPic.save(photoPath)
	return photoPath
