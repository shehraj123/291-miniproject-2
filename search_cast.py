# References
# https://stackoverflow.com/questions/6502541/mongodb-query-multiple-collections-at-once
import pprint
from Utils import *

def searchCast(db):
    """
    This function is for searching the cast/crew members based on name. Matches the
    given name and filters out those unmatched.
    Arguments:
        db - pymongo database
    Returns:
        N/A    
    """
    # Intialization
    shellClear()
    header = "\t\t\tSearch cast/crew member\t\t\t"
    printPrompt(header, "")

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
                "knownForTitles" : "$knownForTitles",
                "birthYear" : "$birthYear",
                "deathYear" : "$deathYear"
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

    x = input("\nPress any key to go back to menu...")

def showInfo(casts, db):
    """
    Display information such as name, birth year, death year and professions. Also 
    displays the title the cast/crew worked in and their characters.
    Arguments:
        db - pymongo database
        casts - list of all cast/crew members with the given name
    Returns:
        N/A
    """
    for cast in casts:
        name = cast["primaryName"]
        professions = cast["primaryProfession"]
        nconst = cast["nconst"]
        title_consts = cast["knownForTitles"]
        bYear = cast["birthYear"]
        dYear = cast["deathYear"]
        titles = getTitleInfo(title_consts, db)
        job_characters = [] # list of jobs and characters with corresponding indices in titles
        
        for tconst in title_consts:
            job_char = getJobChar(tconst, nconst, db)
            if job_char:
                job_characters.append(job_char)
            else:
                job_characters.append(["", ""])

        print('''
        Name: {}
        Born: {}
        Died: {}
        Professions: {}
        Known for Titles: {}
        '''.format(name, bYear, dYear, ", ".join(professions), printTitles(titles, job_characters)))
        
def printTitles(titles, job_characters):
    """
    Helper function for printing the titles and jobs in correct format.
    Arguments: 
        titles - list of tconst(title ids) the member worked in.
        job_characters - corresponding list of jobs/characters enacted.
    Returns:
        res - Formatted string
    """
    res = ""
    i = 1
    for title in titles:  
        res += "\n\t{}. {}, jobs : {}, characters: {}".format(i, title, job_characters[i-1][0], ", ".join(job_characters[i-1][1]))
        i += 1

    return res    

def getTitleInfo(title_consts, db):
    """
    Get title names based on list of tconsts.
    Arguments: 
        title_consts - list of tconst(title ids)
        db - pymongo database
    Returns:
        list of titles corresponding to tconsts
    """
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
    """
    Get job and characters enacted by the member.
    Arguments: 
        tconst - title id of the title the member worked in
        nconst - member id of the person
        db - pymongo database
    Returns:
        tuple of jobs and characters array if exists. otherwise None.    
    """
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
    if len(res) >= 1:
        return res[0]
    else:
        return None

if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('localhost', 27248)
    db = client["291db"]
    searchCast(db)