from misc import dp, bot

from features.dbInteractions import \
	addUser,                        \
	updateUserSettings,             \
	getPhotoReceivedUserSettings    #


from aiogram.types import       \
	Message, inline_keyboard,   \
	CallbackQuery               #
from aiogram.dispatcher import      \
	filters                         #
from aiogram.utils import markdown


# Функция, возвращающая текст, форматированный как СИСТЕМНОЕ СООБЩЕНИЕ
async def systemAnswer(message: Message, text: str = "Ошибка", markup=None):
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
	formattedButtons.append(buttons[length - lastRowWidth : length])

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


############# HANDLERS ############################


@dp.message_handler(filters.Text(equals="Настρойки"), state=None)
@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=[r'(?i)settings|parameters|демо|демотиватор$']), state="*")
async def settingsCallingHandler(message: Message, isBack: bool = False):
	if not isBack and addUser(message.from_user.id):
		print(f"User {message.from_user.id} added")

	buttonsData = [
		["Отправлено фото", "photoReceivedChanging"]
	]

	buttons = buttonsList(buttonsData, rowWidth=2)
	reply_markup = inline_keyboard.InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons)

	userID = message.from_user.id
	username = ", "

	if userID == 1865815:
		username += "кууууун"
	elif userID == 953337533:
		username += "Юрочка"
	else:
		username = ""

	text = "Что вы хотите изменить" + username + "?"

	if not isBack:
		await message.answer(text=text, reply_markup=reply_markup)
	else:
		await bot.edit_message_text(
			text=text,
			reply_markup=reply_markup,
			chat_id=message.chat.id,
			message_id=message.message_id
		)


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


@dp.callback_query_handler(regexp=r"demotivator|randomDemotivator|QRdecode|nothing|back")
async def photoReceivedChangingCallbackHandler(callback_query: CallbackQuery):
	data = callback_query.data
	message = callback_query.message
	userID = callback_query.from_user.id

	currentOption = getPhotoReceivedUserSettings(userID)
	if data == currentOption:
		await bot.answer_callback_query(callback_query.id, text="")
		return

	if data == "demotivator":
		updateUserSettings(userID, "demotivator")
	elif data == "randomDemotivator":
		updateUserSettings(userID, "randomDemotivator")
	elif data == "QRdecode":
		updateUserSettings(userID, "QRdecode")
	elif data == "nothing":
		updateUserSettings(userID, "nothing")
	elif data == "back":
		await settingsCallingHandler(message, isBack=True)
		return

	await photoReceivedCallingCallbackHandler(callback_query)
	await bot.answer_callback_query(callback_query.id, text="Successful!")


# ^-^
