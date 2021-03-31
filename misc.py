from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import environ
from psycopg2 import connect


bot_token = environ["bot_token"]
ytApiKey = environ["ytApiKey"]
adminUserID = environ["adminUserID"]

connection = connect(
	dbname=environ["dbName"],
	user=environ["dbUser"],
	password=environ["dbPassword"],
	host=environ["dbUrl"]
)

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
