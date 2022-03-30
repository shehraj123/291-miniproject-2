import pprint
from pymongo import MongoClient
from Utils import *

def searchGenre(db):
    shellClear()
    header = "\t\t\tSearch genres\t\t\t"
    printPrompt(header, "")    
    
    genre = input("Enter genre which you would like to search: ").strip().lower()
    min_vote = input("Enter a minimum vote count: ")
    
    

    name_basics = db["name_basics"]
    title_basics = db["title_basics"]
    title_principals = db["title_principals"]

    
    

    stage1 = [
        {
            "$unwind" : "$genres"  
        },
        
        {
            "$project": {
                "primaryName": {"$toLower": "$primaryTitle"},
                "genres": {"$toLower": "$genres"},
                "tconst" : "$tconst"
            }
        }, 

        {
            "$match" : {  
                
                "genres" : genre
            }
        },

    ]
    
    
    
    movies = db.title_basics.aggregate(stage1)
    
    all_results = [movie for movie in movies]
    movies = all_results


    if len(movies) == 0:
        print("No Movies Found.")
    
    printInfo(movies, min_vote, db)
    
"""
"""
def printInfo(movies, min_vote, db):

    for movie in movies:
        min_vote = int(min_vote)
        movie_name = movie["primaryName"]
        genre = movie["genres"]
        movie_id = movie["tconst"]
        
        
        rating, votes = match_score(movies, min_vote, db)
        
        print('''
        Movie Name: {} || Number Of Votes: {} || Score: {}
        '''.format(movie_name, votes, rating))
        

"""
"""

def match_score(movie_id, min_vote, db):
    stage2 = [
        {
            "$match" : {"$and":[
            {"tconst" : { "$in" : movie_id }},
            {"numVotes" : { "$gte" : min_vote }}
        ]}},

        {
            "$project" : {
                "rating" : "$averageRating",
                "votes " : "$numVotes"
            }
        }
    ]

    titles = db.title_ratings.aggregate(stage2)
    
    return [title["rating"] for title in titles], [title["votes"] for title in titles]



if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client["291db"]
    searchGenre(db)