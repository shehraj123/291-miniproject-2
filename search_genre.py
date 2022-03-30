import pprint
from pymongo import MongoClient
from Utils import *

def searchGenre(db):
    shellClear()
    header = "\t\t\tSearch genres\t\t\t"
    printPrompt(header, "")    
    
    genre = input("Enter genre which you would like to search: ").strip().lower()
    
    done = False
    while not done:
        try:        
            min_vote = int(input("Enter a minimum vote count: "))
            if min_vote < 0:
                raise ValueError
            done = True    
        except KeyboardInterrupt:
            exit()
        except ValueError:
            print('Enter valid range for votes')    
    
    
    printInfo(min_vote, genre, db)

    x = input("Press any key to exit...")
    return

    
"""
"""
def printInfo(min_vote, genre, db):
  
    stage = [

        {
            "$match" : {
                "numVotes" : {
                    "$gte" : min_vote
                }
            }
        },
        
        {
            "$lookup" :{
                "from" : "title_basics",
                "localField" : "tconst",
                "foreignField": "tconst",
                "as" : "name"
            }
        },

        {
            "$unwind" : "$name"
        },


        {
            "$replaceWith" : {
                "$mergeObjects": [{"avgRating": "$averageRating", "numVotes": "$numVotes"}, "$name"]
            }
        },

        {
            "$unwind": "$genres"
        },

        {
            "$project": {
                "primaryTitle": 1,
                "genres": {"$toLower": "$genres"},
                # "tconst" : 1,
                "avgRating" : 1,
                "numVotes" : 1
            }
        },

        {
            "$match" : {
                "genres" : {"$eq" : genre} 
            }
        },

        {
            "$sort" : {"avgRating" : -1}
        }
    ]      
    
    titles = db.title_ratings.aggregate(stage)
    # titles = [title for title in titles]
    
    i = 1
    for title in titles:    
        print('''
        {}. Movie Name: {}
            Number Of Votes: {}
            Rating: {}\n\n
        '''.format(i, title["primaryTitle"], title["numVotes"], title["avgRating"]))
        i += 1
        


if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('localhost', 27248)
    db = client["291db"]
    searchGenre(db)