from Utils import *
from pymongo import MongoClient
from pymongo.collation import Collation

# References:
	# https://stackoverflow.com/questions/25163658/mongodb-return-true-if-document-exists
	# https://www.statology.org/mongodb-max-value/
	# https://stackoverflow.com/questions/28968660/how-to-convert-a-pymongo-cursor-cursor-into-a-dict
	# https://stackoverflow.com/questions/39815265/mongo-sort-by-string-value-that-is-actually-number
	# https://pymongo.readthedocs.io/en/stable/examples/collations.html

def addCast(db):
	name_basics = db["name_basics"]
	title_basics = db["title_basics"]
	title_principals = db["title_principals"]

	while True:
		# Clear the screen and print the header
		shellClear()
		header = "\t\t\tAdd cast\t\t\t"
		printPrompt(header, "")

		# ask for input
		nconst = input("Enter cast/crew member ID: ").strip()
		tconst = input("Enter title id: ").strip()
		category = input("Enter category: ").strip()

		titleExists = False
		nameExists = False

		# title id needs to exist in title_basics
		if title_basics.count_documents({ "tconst": tconst }, limit = 1) != 0:
			titleExists = True
			print("Title found")
		else:
			print("Title not found")

		# cast/crew member id needs to exist in title_basics
		if name_basics.count_documents({"nconst" : nconst }, limit = 1) != 0:
			nameExists = True
			print("Name found")
		else:
			print("Name not found")

		# If input is valid, insert the movie
		if nameExists and titleExists:
			# this finds the maximum ordering for the given title
			cursor = title_principals.find({"tconst": tconst}).sort("ordering", -1).collation(Collation(locale="en_US", numericOrdering=True)).limit(1)

			l = []
			for doc in cursor:
				l.append(doc)

			# if l is empty, it means there is no entry for the title 
			# in title_principals, so the ordering is set to 1
			try:
				d = l[0]
				ordering = int(d["ordering"])
				ordering = str(ordering + 1)
			except IndexError:
				ordering = "1"

			# Inserting the movie into the collection
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
		# Ask for input again
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
