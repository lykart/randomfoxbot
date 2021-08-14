from aiogram.types import ReplyKeyboardMarkup, BotCommand


# Стандартная reply-keyboard:
def getDefaultReplyKeyboard():
	markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
	markup.add("Демотиватор")
	markup.insert("Пρопустить подзаголовок")
	markup.insert("Случɑйная подпись")
	markup.add("Распознать QR")
	markup.insert("Настρойки")
	markup.insert("ʘтмена")

	return markup


async def get_default_commands():
	commands = [
        {
            'command': 'demotivator',
            'description': '🌄 Создание демотиватора',
        }, {
            'command': 'qr',
            'description': '📊 Разпознать QR-код',
        }, {
            'command': 'settings',
            'description': '🔧 Настройки',
        }, {
            'command': 'get_keyboard',
            'description': '🟩 Вкл. клавиатуру ответов',
        }, {
            'command': 'rm_keyboard',
            'description': '🟥 Выкл. клавиатуру ответов',
        },
    ]

	commands = [
        BotCommand(command['command'], command['description'])
        for command in commands
    ]

	return commands


# ^-^
