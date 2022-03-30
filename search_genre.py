import pprint
from pymongo import MongoClient
from Utils import *
'''
            Search Genre is the intial function call which leads the user to input thier information and then calls the 
            secounds printInfo function to perform a search with the given information
'''
def searchGenre(db):
    # Clearing 
    shellClear()
    header = "\t\t\tSearch genres\t\t\t"
    printPrompt(header, "")    
    
    # Asking for user input
    genre = input("Enter genre which you would like to search: ").strip().lower()
    
    # Creating a loop for valid user input
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
    
    # Calling the secound function with the given user input
    printInfo(min_vote, genre, db)

    x = input("Press any key to exit...")
    return

    
"""
              printInfo takes the given user information and does a search within mangoDB with the given information
              this function also is responsible for the printing of the information which the query returns
"""
def printInfo(min_vote, genre, db):
    
    # Matching numVotes when its greater then or equal to user min vote input
    # Lookup is used to join the two needed tables based on the given attributes
    # Unwinding - Replacing the merges
    # Unwinding genre
    # Getting the nessisary infomration out of the created table
    # Matching based on genre
    # Sorting as needed
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
    
    # Taking titles as the list of all the titiles from the search
    titles = db.title_ratings.aggregate(stage)
    
    # Itterating through all the titles
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

    client = MongoClient('localhost', 27017)
    db = client["291db"]
    searchGenre(db)