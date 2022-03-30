import importlib
import load_json
import tsv_2_json
from pymongo import MongoClient
import pymongo
import add_cast
import add_movie
import search_cast
import search_genre
import search_titles
import time
from Utils import *


def main():
    """
    """
    # Getting port number
    done = False
    while not done:
        try:
            port = input("Make sure mongo server is running. Enter Mongo Port #: ")
            if len(port) != 5 or not port.isnumeric():
                raise
            port = int(port)
            done = True
        except KeyboardInterrupt:
            break
        except:
            print("Enter valid port")

    # Starting Client
    client = MongoClient('localhost', port)
    files = ("title.basics", "title.principals", "title.ratings", "name.basics")
    print("Please wait while database is being loaded...")
    start = time.time()
    tsv_2_json.convert(files)
    
    db = load_json.load(client)
    db.name_basics.create_index([("nconst", pymongo.ASCENDING)])
    db.title_basics.create_index([("tconst", pymongo.ASCENDING), ("primaryTitle", pymongo.ASCENDING)])
    db.title_principals.create_index([("tconst", pymongo.ASCENDING)])
    db.title_ratings.create_index([("numVotes", pymongo.ASCENDING)])
    db.title_ratings.create_index([("tconst", pymongo.ASCENDING)])

    end = time.time()
    time_taken = (end - start) 
    print("Time taken: {:.1f} m {:.1f} s".format(time_taken//60, time_taken%60))
    time.sleep(2)

    while True:
        shellClear()
        header = "\t\t\tWelcome\t\t\t"
        prompt = """
            1. Add cast
            2. Add movie
            3. Search cast/crew member
            4. Search genres
            5. Search titles
            6. Exit
        """
        printPrompt(header, prompt)

        choice = takeOption(6)

        if choice == 1:
            add_cast.addCast(db)
        elif choice == 2:
            add_movie.addMovie(db)

        elif choice == 3:
            search_cast.searchCast(db)

        elif choice == 4:
            search_genre.searchGenre(db)

        elif choice == 5:
            search_titles.searchTitles(db)

        elif choice == 6:
            break


            
if __name__ == "__main__":
    main()    