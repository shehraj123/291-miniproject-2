from pymongo import MongoClient
from pymongo.collation import Collation

client = MongoClient('localhost', 27012)
db = client["291db"]

name_basics = db["name_basics"]
title_basics = db["title_basics"]
title_principals = db["title_principals"]

tconst = input("tconst")

cursor = title_principals.find({"tconst": tconst}).sort("ordering", -1).collation(Collation(locale="en_US", numericOrdering=True)).limit(1)

l = []
for doc in cursor:
    l.append(doc)
d = l[0]

ordering = int(d["ordering"])
print(ordering)
ordering = str(ordering + 1)
print(ordering)