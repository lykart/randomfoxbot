from misc import dp, bot

from features.dbInteractions import \
	addUser,                        \
	updateUserSettings,             \
	getPhotoReceivedUserSettings,   \
	getUserStats                    #


from aiogram.utils import exceptions
from aiogram.types import       \
	Message, inline_keyboard,   \
	CallbackQuery               #
from aiogram.dispatcher import      \
	filters                         #
from aiogram.utils import markdown


async def systemAnswer(message: Message, text: str = "Ошибка", markup=None):
	"""Возвращающая текст, форматированный как СИСТЕМНОЕ СООБЩЕНИЕ (кастомный тип форматирования в этом проекте)"""
	if markup:
		await message.answer(
			markdown.code(text),
			reply_markup=markup,
			parse_mode='MarkdownV2'
		)
	else:
		await message.answer(
			markdown.code(text),
			parse_mode='MarkdownV2'
		)


def buttonsList(*args, rowWidth: int = 2):
	buttons = list(
			inline_keyboard.InlineKeyboardButton(text=text,	callback_data=data)
			for text, data in args[0]
	)

	length = len(buttons)
	lastRowWidth = length % rowWidth

	formattedButtons = [buttons[i:i + rowWidth] for i in range(0, length - lastRowWidth, rowWidth)]
	formattedButtons.append(buttons[length - lastRowWidth: length])

	return formattedButtons


def photoReceivedOptionConversion(option: str) -> str:
	optionsList = [
		["Демотиватор", "demotivator"],
		["Случайный демотиватор", "randomDemotivator"],
		["Распознавание QR-кода", "QRdecode"],
		["Ничего", "nothing"]
	]

	translated = [options[(options.index(option) + 1) % 2] for options in optionsList if option in options]

	return translated[0]


# ----------- HANDLERS -------------------------------------------------------------------------------------------------


@dp.message_handler(filters.Text(equals="Настρойки"), state=None)
@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=[r'(?i)settings|parameters|настройки']), state="*")
async def settingsCallingHandler(message: Message, isBack: bool = False, userID: int = None):
	"""Основное меню настроек"""
	if not isBack:
		addUser(message.from_user.id)
	if not userID:
		userID = message.chat.id

	buttonsData = [
		["Отправлено фото", "photoReceivedChanging"],
		["Статистика", "statistics"]
	]

	buttons = buttonsList(buttonsData, rowWidth=2)
	reply_markup = inline_keyboard.InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons)

	username = ''
	if userID == 1865815:
		username = "карович"
	elif userID == 953337533:
		username = "жура)0"

	text = \
		"Что вы хотите изменить" + \
		(', ' + username if username else '') + \
		"?"

	if not isBack:		# Создаёт сообщение, если пользователь вызвал настройки
		await message.answer(text=text, reply_markup=reply_markup)
	else:				# Изменяет сообщение, если пользователь нажал "back"
		await bot.edit_message_text(
			text=text,
			reply_markup=reply_markup,
			chat_id=message.chat.id,
			message_id=message.message_id
		)


@dp.callback_query_handler(filters.Text(equals="statistics"))
async def statisticsCallingCallbackHandler(callback_query: CallbackQuery, isUpdate: bool = False):
	message = callback_query.message

	buttonsData = [
		["Обновить", "update"],
		["←Назад", "back"]
	]

	buttons = buttonsList(buttonsData, rowWidth=2)
	reply_markup = inline_keyboard.InlineKeyboardMarkup(row_width=2, inline_keyboard=buttons)

	userStats = getUserStats(userID=callback_query.from_user.id)

	text = markdown.bold("Ваша статистика:\n\n") + \
	       "Создано демотиваторов — " + markdown.italic(f"{userStats['demoCreated']}\n") + \
	       "Выполнено inline\-комманд — " + markdown.italic(f"{userStats['inlineAnswered']}\n")

	try:
		await bot.edit_message_text(
			text=text,
			reply_markup=reply_markup,
			parse_mode='MarkdownV2',
			chat_id=message.chat.id,
			message_id=message.message_id
		)

		if isUpdate:
			await callback_query.answer(text="Статистика обновлена")
	except exceptions.MessageNotModified:
		await callback_query.answer(text="Статистика не поменялась")


@dp.callback_query_handler(filters.Text(equals="update"))
async def updateStatisticsCallbackHandler(callback_query: CallbackQuery):
	await statisticsCallingCallbackHandler(callback_query, isUpdate=True)


@dp.callback_query_handler(filters.Text(equals="photoReceivedChanging"))
async def photoReceivedCallingCallbackHandler(callback_query: CallbackQuery):
	message = callback_query.message
	userID = callback_query.from_user.id

	buttonsData = [
		["Демотиватор", "demotivator"],
		["Случайный демотиватор", "randomDemotivator"],
		["Распознавание QR-кода", "QRdecode"],
		["Ничего", "nothing"],
		["←Назад", "back"]
	]

	buttons = buttonsList(buttonsData, rowWidth=2)
	reply_markup = inline_keyboard.InlineKeyboardMarkup(row_width=2, inline_keyboard=buttons)

	currentOption = photoReceivedOptionConversion(getPhotoReceivedUserSettings(userID))

	text = "Текущая опция — " + markdown.bold(f"{currentOption}") + "\n\n"  \
	       "Что должно происходить при отправке фотографии по умолчанию?"

	await bot.edit_message_text(
		text=text,
		reply_markup=reply_markup,
		parse_mode='MarkdownV2',
		chat_id=message.chat.id,
		message_id=message.message_id
	)


@dp.callback_query_handler(regexp=r"back")
async def backCallbackHandler(callback_query: CallbackQuery):
	message = callback_query.message
	user_id = callback_query.from_user.id
	await settingsCallingHandler(message, isBack=True, userID=user_id)


@dp.callback_query_handler(regexp=r"demotivator|randomDemotivator|QRdecode|nothing|back")
async def photoReceivedChangingCallbackHandler(callback_query: CallbackQuery):
	data = callback_query.data
	userID = callback_query.from_user.id

	currentOption = getPhotoReceivedUserSettings(userID)

	if data == currentOption:
		await bot.answer_callback_query(callback_query.id, text="")
		return

	updateUserSettings(userID, photoReceived=data)

	await photoReceivedCallingCallbackHandler(callback_query)
	await bot.answer_callback_query(callback_query.id, text="Successful!")


# ^-^
