from misc import dp, bot
from features.mainFunctions import getCurrentTime
from resources.links import foxLogoPreview


from aiogram.types import                               \
	InlineQuery,                inline_keyboard,        \
	InlineQueryResultArticle,   ChosenInlineResult,     \
	InputTextMessageContent                             #


from asyncio import sleep
from time import time

import re


def evalSecondsCount(query: str):
	secCount = query.strip() \
		.replace("timer", "") \
		.replace("s", "+") \
		.replace("m", "*60+") \
		.replace("h", "*60*60+") \
		.replace(" ", "")

	try:
		secCount = secCount[secCount.find(")")+1:]
	except:
		None

	if secCount[-1] == '+':
		secCount = secCount[::-1].replace("+", "", 1)[::-1]

	return eval(secCount)


@dp.inline_handler(regexp=r'(?i)timer\s+\(.+\)\s+(\d+[smh]){1,3}')
async def timerInlineHandler(inline_query: InlineQuery):
	secCount = evalSecondsCount(inline_query.query)

	if secCount > 7200 or secCount < 1:
		articleTitle = "Таймер не будет запущен"
		isWrong = True
	else:
		articleTitle = 'Запускает таймер'
		isWrong = False

	awaitingButton = inline_keyboard.InlineKeyboardButton(
		'Запускаю...',
		callback_data='awaiting'
	)

	awaitingKeyboard = inline_keyboard.InlineKeyboardMarkup(row_width=1). \
		insert(awaitingButton)

	items = [
		InlineQueryResultArticle(
			id=str(time()),
			title=articleTitle,
			description=f"на {secCount} секунд",
			reply_markup=awaitingKeyboard,
			thumb_url=foxLogoPreview,
			input_message_content=InputTextMessageContent(f"Таймер на {secCount} сек."))
	]
	if not isWrong:
		await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


doingTimersFrom = []
doingTimersFrom.clear()
@dp.inline_handler(lambda inline_query: re.search(r'(?i)stop\s+timer', inline_query.query))
async def some_callback_handler(inline_query: InlineQuery):
	userId = inline_query.from_user.id

	if userId in doingTimersFrom:
		doingTimersFrom.remove(userId)

		items = [
			InlineQueryResultArticle(
				id=str(time()),
				title="Завершаю таймер...",
				thumb_url=foxLogoPreview,
				input_message_content=InputTextMessageContent("ну и что ты тут ожидаешь увидеть?"))
		]
	else:
		items = [
			InlineQueryResultArticle(
				id=str(time()),
				title="Не могу найти таймер",
				description="возможно, ни одного не запущено вами",
				thumb_url=foxLogoPreview,
				input_message_content=InputTextMessageContent("Вы можете запустить таймер, выполнив запрос \"timer\""))
		]

	await bot.answer_inline_query(inline_query.id, results=items, cache_time=0)


@dp.chosen_inline_handler(lambda chosen_inline_query: re.search(r'(?i)timer\s+\(.+\)\s+(\d+[smh]){1,3}', chosen_inline_query.query))
async def timerChangingHandler(chosen_inline_query: ChosenInlineResult):
	secCount = evalSecondsCount(chosen_inline_query.query)
	queryText = chosen_inline_query.query
	try:
		text = queryText[queryText.find("(") + 1:queryText.find(")")]
	except:
		text = f"Таймер на {secCount} сек."

	userId = chosen_inline_query.from_user.id
	inlineMessageId = chosen_inline_query.inline_message_id

	if userId in doingTimersFrom:
		await bot.edit_message_text(
			text=f"Вы же уже запустили таймер?\nПодождите, пока он закончится...",
			inline_message_id=inlineMessageId
		)
		raise BlockingIOError("Таймер уже запущен этим пользователем")

	doingTimersFrom.append(userId)

	print(text)
	startTime = time()
	while secCount > 0:
		currTime = time()
		secCount -= int(currTime - startTime)
		startTime = time()

		button = inline_keyboard.InlineKeyboardButton(text=f"{secCount}", callback_data='awaiting')
		inlineKeyboard = inline_keyboard.InlineKeyboardMarkup(row_width=1, inline_keyboard=[[button]])

		await sleep(1)
		await bot.edit_message_text(text=text, inline_message_id=inlineMessageId, reply_markup=inlineKeyboard)

		if userId not in doingTimersFrom:
			break
	else:
		doingTimersFrom.remove(userId)

		currTime = getCurrentTime()
		doneButton = inline_keyboard.InlineKeyboardButton(
			'Закончен в ' + currTime,
			callback_data=f'something'
		)

		inlineKeyboard = inline_keyboard.InlineKeyboardMarkup(row_width=1).insert(doneButton)
		await bot.edit_message_text(text=f"Время истекло!",	inline_message_id=inlineMessageId)
		await bot.edit_message_reply_markup(reply_markup=inlineKeyboard,	inline_message_id=inlineMessageId)
		await bot.send_message(chosen_inline_query.from_user.id, text=f"({text}) был завершен.\nЗакончен в {currTime}")
		return

	await bot.edit_message_text(text=f"Таймер завершён досрочно", inline_message_id=inlineMessageId)
