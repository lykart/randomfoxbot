from misc import bot, adminUserID, connection as conn

from asyncio import get_event_loop
from datetime import date as Date

from typing import List, Dict

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
	def get(self) -> List[Dict[str, str]]:
		with conn.cursor() as cursor:
			cursor.execute("SELECT \"userID\", \"nickname\" FROM \"user\";")
			return [{'id': i[0], 'nickname': i[1]} for i in cursor]

	def inUsers(self, userID: int) -> bool:
		if userID in self.users:
			return True
		else:
			return False

	def update(self):
		self.__init__()

	def __init__(self):
		self.nicknames = self.get()
		self.users = {entry['id'] for entry in self.nicknames}


usersSet = UsersSet()


# async def dbStatsSync():
# 	with conn.cursor() as cursor:
# 		while True:
# 			await sleep(600)
# TODO: синхронизация базы данных каждые 10 минут по статистике


def getWholeDb() -> str:
	with conn.cursor() as cursor:
		cursor.execute(f"SELECT * FROM \"user\";")
		users = cursor.fetchall()

		cursor.execute(f"SELECT * FROM \"stats\";")
		stats = cursor.fetchall()

		cursor.execute(f"SELECT * FROM \"settings\";")
		settings = cursor.fetchall()

	users = { user[0]: user[1:] for user in users }
	stats = { stat[0]: stat[1:] for stat in stats }
	settings = { setting[0]: setting[1:] for setting in settings }

	userStats = [
		f"\n\nUser -- {user}:\n\t"
		f"> demoCreated = {stats.get(user)[0]}, inlineAnswered = {stats.get(user)[1]}\n\t"
		f"> photoReceived = {settings.get(user)[0]}"

		for user in users
	]

	answer = ""

	for user in userStats:
		answer += user

	return answer


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


def get_nick_by_id(user_id: int) -> str:
	nickname, = [entry['nickname'] for entry in usersSet.nicknames if entry['id'] == user_id]
	return nickname


@autoCommit
def change_nickname(user_id: int, new_nickname: str):
	with conn.cursor() as cursor:
		cursor.execute(
			f"UPDATE \"user\" SET \"nickname\" = %s WHERE \"userID\" = %s",
			(new_nickname, user_id)
		)

	for i, entry in enumerate(usersSet.nicknames):
		if entry['id'] == user_id:
			usersSet.nicknames[i]['nickname'] = new_nickname
			break


#### Statistics interactions ####


# ^_^
