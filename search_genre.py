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
    
    

    name_basics = db["name_basics"]
    title_basics = db["title_basics"]
    title_principals = db["title_principals"]

    
    

    # stage1 = [
    #     {
    #         "$unwind" : "$genres"  
    #     },
    #     {
    #         "$project": {
    #             "primaryName": {"$toLower": "$primaryTitle"},
    #             "genres": {"$toLower": "$genres"},
    #             "tconst" : "$tconst"
    #         }
    #     },
    #     {
    #         "$match" : {  
                
    #             "genres" : {
    #                 "$eq": genre
    #             }
    #         }
    #     }
    # ]
    
    
    
    # movies = db.title_basics.aggregate(stage1)
    
    # all_results = [movie for movie in movies]
    # movies = all_results


    # if len(movies) == 0:
    #     print("No Movies Found.")
    
    # tconsts = [movie["tconst"] for movie in movies]
    printInfo(min_vote, genre, db)

    x = input("Press any key to exit...")
    return

    
"""
"""
def printInfo(min_vote, genre, db):
  
    stage = [
        
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
                "primaryTitle": {"$toLower": "$primaryTitle"},
                "genres": {"$toLower": "$genres"},
                "tconst" : "$tconst",
                "avgRating" : "$avgRating",
                "numVotes" : "$numVotes"
            }
        },

        {
            "$match" : {
                "$and": [{"numVotes" : {"$gte": min_vote}}, {"genres" : {"$eq" : genre}}] #
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