from Utils import *
import pprint
import search_cast

def searchTitles(db):
    
    # Intialization
    shellClear()
    header = "\t\t\tSearch titles\t\t\t"
    printPrompt(header, "")

    keywords = input("Enter keywords to search for: ").strip().lower().split(" ")
    regex = ".*{}.*".format(".*".join(keywords))
    title_basics = db["title_basics"]
    title_principals = db["title_principals"]
    title_ratings = db["title_ratings"]

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

    done= False
    index = -1
    while not done:
        try:
            index = int(input("Select the movie using the index: "))
            if index <= 0 or index > len(res):
                raise ValueError
            done = True    
        except KeyboardInterrupt:
            break
        except ValueError:
            print("Enter valid index")    
    title = res[index - 1]
    tconst = title["tconst"]

    # Printing rating and votes
    rating, votes = getRatingVotes(tconst, db)  
    print("\n\tYou selected {}".format(title["primaryTitle"]))  
    print("\tavgRating: {}\n\tVotes: {}".format(rating, votes))

    # Printing cast crew members
    crew = getCastCrew(tconst, db) # list of dictionaries

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
"""
def getCastCrew(tconst, db):
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