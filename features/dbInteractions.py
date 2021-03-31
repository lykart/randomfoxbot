from misc import bot, adminUserID, connection as conn

from asyncio import get_event_loop
from datetime import date as Date

import functools


def autoCommit(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		foo = func(*args, **kwargs)
		conn.commit()

		return foo
	return wrapper


photoReceivedPossible = ["nothing", "demotivator", "QRdecode", "randomDemotivator"]


class UsersSet:

	def get(self):
		with conn.cursor() as cursor:
			cursor.execute("SELECT \"userID\" FROM \"user\";")
			return {i[0] for i in cursor}

	def inUsers(self, userID: int) -> bool:
		if userID in self.users:
			return True
		else:
			return False

	def update(self):
		self.users = self.get()

	def __init__(self):
		self.users = self.get()


usersSet = UsersSet()


# async def dbStatsSync():
# 	with conn.cursor() as cursor:
# 		while True:
# 			await sleep(600)
# TODO: синхронизация базы данных каждые 10 минут по статистике


@autoCommit
def addUser(userID) -> bool:
	if usersSet.inUsers(userID):
		return False

	with conn.cursor() as cursor:
		cursor.execute(
			"INSERT INTO \"user\" (\"userID\", \"signUpDate\") VALUES (%(userID)s, %(date)s);"
			"INSERT INTO \"stats\" (\"userID\") VALUES (%(userID)s);"
			"INSERT INTO \"settings\" (\"userID\") VALUES (%(userID)s);",

			{'userID': userID, 'date': Date.today()}
		)

	loop = get_event_loop()
	loop.create_task(bot.send_message(adminUserID, f"User {userID} added"))

	usersSet.update()
	return True


@autoCommit
def updateUserSettings(userID: int, **settings):
	item, option = list(settings.items())[0]

	with conn.cursor() as cursor:
		cursor.execute(
			f"UPDATE \"settings\" SET \"{item}\" = %s WHERE \"userID\" = %s",
			(option, userID)
		)


def getPhotoReceivedUserSettings(userID: int) -> str:
	with conn.cursor() as cursor:
		cursor.execute(
			"SELECT * FROM \"settings\" WHERE \"userID\" = %s;",
			(userID,)
		)
		result = [i for i in cursor][0] # tuple из всех настроек, где tuple[0] - userID, tuple[1] - photoReceived итд (как в бд)

	photoReceived = result[1]

	return photoReceived


#### Statistics interactions ####


@autoCommit
def incrementStatistics(field: str, userID: int):
	addUser(userID)

	with conn.cursor() as cursor:
		cursor.execute(
			f"UPDATE \"stats\" SET \"{field}\" = \"{field}\" + 1 WHERE \"userID\" = %s",
			(userID,)
		)


def getUserStats(userID: int):
	with conn.cursor() as cursor:
		cursor.execute(
			f"SELECT * FROM \"stats\" WHERE \"userID\" = %s;",
			(userID, )
		)
		result = [i for i in cursor][0]

	possibleStats = ["demoCreated", "inlineAnswered"]
	stats = {possibleStats[i]: result[i + 1] for i in range(len(possibleStats))}

	return stats


#### Statistics interactions ####


# ^_^
