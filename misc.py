from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tinydb import TinyDB

from resources.links import pathToDB

from os import environ


bot_token = environ["bot_token"]
ytApiKey = environ["ytApiKey"]

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = TinyDB(pathToDB)
