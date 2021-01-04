from tinydb import Query

from misc import db


photoReceivedPossible = ["nothing", "demotivator", "QRdecode", "randomDemotivator"]
User = Query()


def insertUserSettings(
		userID: int = 0,

		photoReceived: str = "nothing",
		skipSubtitle: bool = False,
) -> bool:

	if (photoReceived not in photoReceivedPossible) or (userID == 0):
		return False

	if db.contains(User.userID == userID):
		db.update({
				'photoReceived': photoReceived,
				'skipSubtitle': skipSubtitle
			},
			User.userID == userID
		)
	else:
		db.insert({
			'userID': userID,

			'photoReceived': photoReceived,
			'skipSubtitle': skipSubtitle
		})

	return True


def getUserSettings(userID: int = 0) -> dict or bool:
	if userID == 0:
		return False

	return db.search(User.userID == userID)

# ^_^
