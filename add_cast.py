from Utils import *
from pymongo import MongoClient

def addCast(db):

	# Intialization

	titleExists = False
	nameExists = False

	name_basics = db["name_basics"]
	title_basics = db["title_basics"]
	title_principals = db["title_principals"]

	# https://stackoverflow.com/questions/25163658/mongodb-return-true-if-document-exists
	while True:
		shellClear()
		header = "\t\t\tAdd cast\t\t\t"
		printPrompt(header, "")
		nconst = input("Enter cast/crew member ID: ").strip()
		tconst = input("Enter title id: ").strip()
		category = input("Enter category: ").strip()

		if title_basics.count_documents({ "tconst": tconst }, limit = 1) != 0:
			titleExists = True
			print("Title found")
		else:
			print("Title not found")

		if name_basics.count_documents({"nconst" : nconst }, limit = 1) != 0:
			nameExists = True
			print("Name found")
		else:
			print("Name not found")

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

			print("Success!")
			break
		else:
			print("Invalid input")
			print("1. Try again")
			print("2. Exit")
			again = False
			while True:
				choice = takeOption(2)
				if choice == 1:
					again = True
					break
				elif choice == 2:
					break
					
			if again:
				continue
			else:
				break		
if __name__ == "__main__":
    client = MongoClient('localhost', 27012)
    db = client["291db"]
    addCast(db)
