import importlib
import load_json
import tsv_2_json
from pymongo import MongoClient
import pymongo
import add_cast
import add_movie
from Utils import *


def main():
    """
    """
    # Getting port number
    done = False
    while not done:
        try:
            port = input("Enter Mongo Port #: ")
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
    tsv_2_json.convert(files)

    db = load_json.load(client)

    while True:
        shellClear()
        header = "\t\t\tWelcome\t\t\t"
        prompt = """
            1. Add cast
            2. Add movie
            3. Exit
        """
        printPrompt(header, prompt)

        choice = takeOption(3)

        if choice == 1:
            shellClear()
            header = "\t\t\tAdd cast\t\t\t"
            add_cast.addCast(db)
        elif choice == 2:
            shellClear()
            header = "\t\t\tAdd movie\t\t\t"
            add_movie.addMovie(db)
        elif choice == 3:
            break
            
if __name__ == "__main__":
    main()    