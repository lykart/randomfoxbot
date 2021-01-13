from tinydb import Query


from misc import db


photoReceivedPossible = ["nothing", "demotivator", "QRdecode", "randomDemotivator"]
User = Query()


def defaultBlueprint(userID, defaultAction="nothing"):
	return {
		'userID': userID,
	    'photoReceived': defaultAction
	}


def addUser(userID):
	if db.contains(User.userID == userID):
		return False
	else:
		userDocument = defaultBlueprint(userID=userID)
		db.insert(userDocument)

	return userDocument


def updateUserSettings(userID: int, photoReceived: str = None) -> bool:
	if photoReceived not in photoReceivedPossible:
		return False

	updatedSettings = {}
	if photoReceived:
		updatedSettings.update({"photoReceived": photoReceived})

	if updatedSettings:
		db.update(
			updatedSettings,
			User.userID == userID
		)
	else:
		print(f"Error in {userID} settings update (не передано аргументов для изменения)")
		return False

	return True


def getPhotoReceivedUserSettings(userID: int) -> str:
	try:
		userDocument = db.search(User.userID == userID)[0]
	except:
		print("Error in searching in DB")
		return None

	return userDocument.get("photoReceived")


### something ###


def statsBlueprint(demoCreated, inlineAnswered):
	return {'demoCreated': 0, 'inlineAnswered': 0}

# ^_^
