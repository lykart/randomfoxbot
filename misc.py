from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from os import environ

bot_token = "1391499519:AAFLDXNgo4S7eh6-WLzEb9r8iRNn09ATOAo"
ytApiKey = 'AIzaSyBRIXPn-RsGxpbsXtoK9ZVd16mQxFWAmLY'

# bot_token = environ["bot_token"]
# ytApiKey = environ["ytApiKey"]

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
