from tinydb import Query
from typing import Dict
from misc import db


photoReceivedPossible = ["nothing", "demotivator", "QRdecode", "randomDemotivator"]
User = Query()


def defaultBlueprint(userID):
	return {
		'userID': userID,
		'photoReceived': "nothing",

		"statistics": defaultStatsField()
	}


def addUser(userID):
	if db.contains(User.userID == userID):
		return False
	else:
		userDocument = defaultBlueprint(userID=userID)
		db.insert(userDocument)

	return userDocument


def updateUserSettings(userID: int, **settings) -> bool:
#   for key in settings:
#   	if key == "photoReceived" and settings[key] not in photoReceivedPossible:
#   		print("Not correct \"photoReceived\" option")
#   		return False

	db.update(
		settings,
		User.userID == userID
	)

	return True


def getPhotoReceivedUserSettings(userID: int) -> str:
	try:
		userDocument = db.search(User.userID == userID)[0]
	except IndexError:
		print("Error in searching in DB")
		return ""

	return userDocument.get("photoReceived")


#### Statistics interactions ####


def defaultStatsField(demoCreated: int = 0, inlineAnswered: int = 0) -> Dict:
	return {
			"demoCreated": demoCreated,
			"inlineAnswered": inlineAnswered
	}


def incrementStatistics(field: str, userID: int):
	addUser(userID=userID)
	db.update(statsIncrementor(field), User.userID == userID)


def statsIncrementor(field: str):
	def transform(doc):
		doc["statistics"][field] += 1
	return transform


def getUserStats(userID: int):
	try:
		return db.search(User.userID == userID)[0]['statistics']
	except IndexError:
		addUser(userID=userID)
		return db.search(User.userID == userID)[0]['statistics']


#### Statistics interactions ####


# ^_^
