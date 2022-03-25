def addMovie(db):
	tconst = input("Enter title id: ")
	title = input("Enter a title: ")
	sYear = input("Enter start year: ")
	runningTime = input("Enter running time: ")
	genres = input("Enter a list of space separated genres: ").split()

	title_basics = db["title_basics"]

	# still need to check valid input

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

	print("inserted")