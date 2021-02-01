from misc import dp, bot
from features.mainFunctions import \
	createQR, uploadInputFileToTelegram,\
	escapeMarkdown  #

from aiogram.types import \
	InlineQuery, inline_keyboard, \
	InlineQueryResultPhoto, ChosenInlineResult, \
	InputMediaPhoto  #

from aiogram.utils import markdown

from os import remove
from time import time

import re


@dp.inline_handler(regexp=r'(?i)^qr\b.+$')
async def qrInlineHandler(inline_query: InlineQuery):
	awaitingButton = inline_keyboard.InlineKeyboardButton(
		'Ожидайте...',
		callback_data='awaiting'
	)

	awaitingKeyboard = inline_keyboard.InlineKeyboardMarkup(row_width=1).insert(awaitingButton)
	items = [
		InlineQueryResultPhoto(
			id=str(time() + 1),
			photo_url="https://i.ibb.co/n16zcs0/rnfoxbot-QR.jpg",
			thumb_url='https://i.ibb.co/KsbFqjG/rnfoxbot-QR.jpg',
			photo_width=200,
			photo_height=200,

			caption=markdown.italic("QR—code генерируется..."),
			reply_markup=awaitingKeyboard,
			parse_mode='MarkdownV2'
		)
	]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


@dp.chosen_inline_handler(lambda chosen_inline_query: re.search(r"(?i)^qr\b.+$", chosen_inline_query.query))
async def some_chosen_inline_handler(chosen_inline_query: ChosenInlineResult):
	queryTxt = chosen_inline_query.query
	txt = re.search(r"(?i)qr\b\s+(.+)", queryTxt).group(1)

	voidInlineKeyboard = inline_keyboard.InlineKeyboardMarkup()

	qrCodePath = createQR(txt)
	imgID = await uploadInputFileToTelegram(qrCodePath, bot=bot)

	await bot.edit_message_reply_markup(
		reply_markup=voidInlineKeyboard,
		inline_message_id=chosen_inline_query.inline_message_id
	)

	await bot.edit_message_media(
		media=InputMediaPhoto(media=imgID),
		inline_message_id=chosen_inline_query.inline_message_id
	)

	remove(qrCodePath)
