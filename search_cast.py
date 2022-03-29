# https://stackoverflow.com/questions/6502541/mongodb-query-multiple-collections-at-once
import pprint

def searchCast(db):
    name = input("Enter cast/crew member name: ").strip().lower()

    name_basics = db["name_basics"]
    title_basics = db["title_basics"]
    title_principals = db["title_principals"]

    stage1 = [
        {
            "$project": {
                "primaryName": {"$toLower": "$primaryName"},
                "primaryProfession": "$primaryProfession",
                "nconst" : "$nconst",
                "knownForTitles" : "$knownForTitles"
            }
        }, 

        {
            "$match" : {
                "primaryName" : name
            }
        },

    ]
    casts = db.name_basics.aggregate(stage1)
    results = [cast for cast in casts]
    casts = results

    if len(casts) == 0:
        print("No cast/crew found.")
    
    showInfo(casts, db)

"""
"""
def showInfo(casts, db):

    for cast in casts:
        name = cast["primaryName"]
        professions = cast["primaryProfession"]
        nconst = cast["nconst"]
        title_consts = cast["knownForTitles"]
        titles = getTitleInfo(title_consts, db)
        job_characters = [] # list of jobs and characters with corresponding indices in titles
        
        for tconst in title_consts:
            job_characters.append(getJobChar(tconst, nconst, db))

        print('''
        Name: {}
        Professions: {}
        Known for Titles: {}
        '''.format(name, ", ".join(professions), printTitles(titles, job_characters)))
        

"""
"""
def printTitles(titles, job_characters):
    res = ""
    i = 1
    for title in titles:  
        res += "\n\t{}. {}, jobs : {}, characters: {}".format(i, title, job_characters[i-1][0], ", ".join(job_characters[i-1][1]))
        i += 1

    return res    

def getTitleInfo(title_consts, db):
    stage2 = [
        {
            "$match" : {
                "tconst" : {
                    "$in" : title_consts
                }
            }
        },

        {
            "$project" : {
                "title" : "$primaryTitle"
            }
        }
    ]

    titles = db.title_basics.aggregate(stage2)
    
    return [title["title"] for title in titles]


def getJobChar(tconst, nconst, db):
    stage3 = [
        {
            "$match" : {
                "$and" : [
                    {"tconst" : tconst},
                    {"nconst" : nconst}
                ]              
            }
        },

        {
            "$project" : {
                "job" : "$job",
                "characters" : "$characters"
            }
        }
    ]

    res = db.title_principals.aggregate(stage3)
    res = [(r["job"], r["characters"]) for r in res]
    toret = tuple()
    if len(res) >= 1:
        toret = res[0]
    return toret

if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('localhost', 27248)
    db = client["291db"]
    searchCast(db)