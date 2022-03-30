from Utils import *

def addCast(db):

	# Intialization
	shellClear()
	header = "\t\t\tAdd cast\t\t\t"
	printPrompt(header, "")

	nconst = input("Enter cast/crew member ID: ").strip()
	tconst = input("Enter title id: ").strip()
	category = input("Enter category: ").strip()

	titleExists = False
	nameExists = False

	name_basics = db["name_basics"]
	title_basics = db["title_basics"]
	title_principals = db["title_principals"]

	# https://stackoverflow.com/questions/25163658/mongodb-return-true-if-document-exists

	if title_basics.count_documents({ "tconst": tconst }, limit = 1) != 0:
		titleExists = True
		print("title found")

	if name_basics.count_documents({"nconst" : nconst }, limit = 1) != 0:
		nameExists = True
		print("name found")

	if nameExists and titleExists:
		# https://www.statology.org/mongodb-max-value/
		# https://stackoverflow.com/questions/28968660/how-to-convert-a-pymongo-cursor-cursor-into-a-dict
		cursor = title_principals.find().sort("ordering", -1).limit(1)
		l = []
		for doc in cursor:
			l.append(doc)
		d = l[0]

		ordering = int(d["ordering"])
		ordering = str(ordering + 1)

		row = {
			"tconst": tconst,
			"ordering": ordering,
			"nconst": nconst,
			"category": category,
			"job": '\\N',
			"characters": '\\N'
		}

		title_principals.insert_one(row)

		print("inserted")

















