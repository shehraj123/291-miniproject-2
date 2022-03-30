from Utils import *
from pymongo import MongoClient

'''
	This is the function that handles adding the movie to the database
	It asks for input, then validates it.
	If the input is valide, the movie is added to the database.
'''
def addMovie(db):

	while True:
		# Clear the screen and print the headers
		shellClear()
		header = "\t\t\tAdd movie\t\t\t"
		printPrompt(header, "")

		# Get the input
		tconst = input("Enter title id: ").strip()
		title = input("Enter a title: ").strip()
		sYear = input("Enter start year: ").strip()
		runningTime = input("Enter running time: ").strip()
		genres = input("Enter a list of space separated genres: ").strip().split()

		title_basics = db["title_basics"]

		# check valid input
		validID = True
		validYear = True
		validRunningTime = True

		# ID needs to be unique
		cursor = title_basics.find({"tconst": tconst})
		for doc in cursor:
			validID = False
			print("Invalid ID")
			break

		# Year needs to be numeric and a 4 digit number
		if (not sYear.isnumeric()) or (len(sYear) != 4):
			print("Invalid year")
			validYear = False

		# Running time needs to be numeric
		if (not runningTime.isnumeric()):
			print("Invalid running time")
			validRunningTime = False

		# If input is valid, insert the movie
		if validID and validYear and validRunningTime:
			row = {
				"tconst": tconst,
				"titleType": "movie",
				"primaryTitle": title,
				"originalTitle": title,
				"isAdult": '\\N',
				"startYear": sYear,
				"endYear": '\\N',
				"runtimeMinutes": runningTime,
				"genres": genres
			}

			title_basics.insert_one(row)

			print("Success!")
			break
		# Otherwise ask for input again
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
    addMovie(db)