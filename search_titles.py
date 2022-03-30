from Utils import *
import pprint
import search_cast

'''
                searchTitle is used to get the user input and search if valid
                this then calls the getCastCrew and getRatingVotes to get the needed information from for individual movies
'''
def searchTitles(db):
    
    # Intialization
    shellClear()
    header = "\t\t\tSearch titles\t\t\t"
    printPrompt(header, "")

    # User inputs
    keywords = input("Enter keywords to search for: ").strip().lower().split(" ")
    regex = ".*{}.*".format(".*".join(keywords))

    # Stage one is used to get all title which match
    stage1 = [
        {
            "$project": {
                "tconst": "$tconst",
                "titleType" : "$titleType",
                "primaryTitle": {"$toLower": "$primaryTitle"},
                "originalTitle" : "$originalTitle",
                "Year" : "$startYear",
                "endYear" : "$endYear",
                "isAdult": "$isAdult",
                "runtime" : "$runtimeMinutes",
                "genres": "$genres"
            }
        },

        {
            "$match" : {
                "$or" : 
                    [{"Year" : {
                        "$eq" : keywords[0]
                    }},

                    {"primaryTitle" : {
                        "$regex" : regex
                    }
                    }]
                
            }
        }
    ]

    
    res = db.title_basics.aggregate(stage1)
    res = [r for r in res]
    
    # Invalid / too many filters
    if len(res) == 0:
        x = input("No such title.. Press any key to go back to menu")
        return
    # Printing info and indexes for each title
    i = 1
    for item in res:
        print("""
        {}. "tconst": {},
            "titleType" : {},
            "primaryTitle": {},
            "originalTitle" : {},
            "Year" : {},
            "endYear" : {},
            "isAdult": {},
            "runtime" : {},
            "genres": {}\n\n
        """.format(i, item["tconst"], item["titleType"], item["primaryTitle"], item["originalTitle"], item["Year"], item["endYear"], item["isAdult"], item["runtime"], item["genres"]))
        i += 1

    # Variable initilization
    done= False
    index = -1
    
    # Asking user for movie select
    while not done:
        try:
            index = int(input("Select the movie using the index: "))
            if index <= 0 or index > len(res):
                raise ValueError
            done = True    
        except KeyboardInterrupt:
            exit()
        except ValueError:
            print("Enter valid index")    
    
    # Getting location of movie selected
    title = res[index - 1]
    tconst = title["tconst"]

    # Printing rating and votes
    
    # Getting information for the given movie
    rating, votes = getRatingVotes(tconst, db)  
    print("\n\tYou selected {}".format(title["primaryTitle"]))  
    print("\tavgRating: {}\n\tVotes: {}".format(rating, votes))

    # Printing cast crew members
    crew = getCastCrew(tconst, db) # list of dictionaries

    # Itterating through
    if crew:
        print("\t Crew/Cast: ")
        i = 1
        for mem in crew:
            print("\t{}. Name: {}, Characters played: {}".format(i, mem["Name"], mem["characters"]))
            i += 1

    else:
        print("no cast/crew...")

    x = input("Enter any key to go back")
    return            

"""
                   Based on the gived movieID find the crewlist
"""
def getCastCrew(tconst, db):
    # Matching movieID 
    # Lookup is used to join the two needed tables based on the given attributes
    # Unwinding 
    # Replace the merged
    # Projecting the needed information 
    stage = [
        {
            "$match" : {
                "tconst" : tconst
            }
        },

        {
            "$lookup" : {
                "from" : "name_basics",
                "localField" : "nconst",
                "foreignField": "nconst",
                "as": "primaryName"
            }
        },

        {
            "$unwind" : "$primaryName"
        },

        {
            "$replaceWith" : {
                "$mergeObjects" : [{"characters": "$characters"}, "$primaryName"]
            }
        },

        {
            "$project" : {
                "Name" : "$primaryName",
                "characters" : "$characters"
            }
        }
    ]

    res = db.title_principals.aggregate(stage)
    res = [r for r in res]
    if len(res) == 0:
        return None
    return res


"""
               Based on the gived movieID find the rating and the number of votes
"""
def getRatingVotes(tconst, db):
    stage = [
        {
            "$match": {
                "tconst" : tconst
            }
        }
    ]

    
    res = db.title_ratings.aggregate(stage)
    r = [x for x in res]
    if len(r) == 0:
        return ["", ""]
    else:
        r = r[0]
        return (r["averageRating"], r["numVotes"])    

if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('localhost', 27248)
    db = client["291db"]
    searchTitles(db)