from misc import dp, bot, connection as conn

from features.dbInteractions import \
	addUser,                        \
	updateUserSettings,             \
	getPhotoReceivedUserSettings,   \
	getUserStats, change_nickname,  \
	get_nick_by_id                  #

from aiogram.utils import exceptions
from aiogram.types import       \
	Message, inline_keyboard,   \
	CallbackQuery               #
from aiogram.dispatcher import      \
	filters, FSMContext             #
from aiogram.utils import markdown
from aiogram.dispatcher.filters.state import    \
	State,                                      \
	StatesGroup                                 #

from typing import Optional


class SettingsFSM(StatesGroup):
	changingNickname = State()


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
@dp.message_handler(commands=["settings"])
async def settingsCallingHandler(message: Message, isBack: bool = False, userID: int = None):
	"""Основное меню настроек"""
	if not isBack:
		addUser(message.from_user.id)
	if not userID:
		userID = message.chat.id

	buttonsData = [
		["Отправлено фото", "photoReceivedChanging"],
		["Статистика", "statistics"],
		["Изменить ник", "changeNickname"],
	]

	buttons = buttonsList(buttonsData, rowWidth=2)
	reply_markup = inline_keyboard.InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons)

	username = get_nick_by_id(userID)

	text = f"Что вы хотите изменить, {username}?"

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


@dp.callback_query_handler(filters.Text(equals="changeNickname"))
async def NicknameChangingCallbackHandler(callback_query: CallbackQuery = None, state: FSMContext = None,
										  isUpdate: bool = False):
	if callback_query:
		await SettingsFSM.changingNickname.set()
		async with state.proxy() as data:
			data['callback_query'] = callback_query

	async with state.proxy() as data:
		callback_query = data['callback_query']
		message = callback_query.message

	buttonsData = [
		["Обновить", "updateNickname"],
		["←Назад", "back"]
	]

	buttons = buttonsList(buttonsData, rowWidth=2)
	reply_markup = inline_keyboard.InlineKeyboardMarkup(row_width=2, inline_keyboard=buttons)

	nickname = get_nick_by_id(callback_query.from_user.id)

	text = "Здравствуйте, " + markdown.bold(f"{nickname}!\n\n") + \
	       markdown.italic("Хотите изменить никнейм?\nОтправьте его мне (до 20-ти символов)")

	try:
		await bot.edit_message_text(
			text=text,
			reply_markup=reply_markup,
			parse_mode='MarkdownV2',
			chat_id=message.chat.id,
			message_id=message.message_id
		)

		if isUpdate:
			await callback_query.answer(text="Никнейм успешно обновлён.")
	except exceptions.MessageNotModified:
		await callback_query.answer(text="Не обманывай лисёнка 🥺")


@dp.callback_query_handler(filters.Text(equals="updateNickname"), state="*")
async def updateNicknameCallbackHandler(callback_query: CallbackQuery, state: FSMContext):
	await SettingsFSM.changingNickname.set()
	await NicknameChangingCallbackHandler(callback_query=callback_query, isUpdate=True, state=state)


@dp.message_handler(state=SettingsFSM.changingNickname)
async def updateNickname(message: Message, state: FSMContext):
	if len(message.text) <= 20:
		userID = message.from_user.id
		new_nickname = message.text

		change_nickname(userID, new_nickname)
		await message.answer(
			markdown.italic('Никнейм изменён на ') +
			markdown.bold(f'{new_nickname}') + '.',
			parse_mode='markdown')

		async with state.proxy() as data:
			callback_query = data['callback_query']
			message = callback_query.message

		await settingsCallingHandler(message, isBack=True, userID=userID)
	else:
		await message.answer("Можно покороче?")


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


@dp.callback_query_handler(regexp=r"back", state='*')
async def backCallbackHandler(callback_query: CallbackQuery, state: FSMContext):
	await state.finish()

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
