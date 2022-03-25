import importlib
import load_json
import tsv_2_json
from pymongo import MongoClient
import pymongo
import add_cast
import add_movie


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

    # print("add cast")
    # add_cast.addCast(db)
    
    print("add movie")
    add_movie.addMovie(db)

main()    