#https://www.youtube.com/watch?v=9N6a-VLBa2I

from pymongo import MongoClient
import pymongo
import json

def load(port):
	client = MongoClient("localhost", port)

	db = client["291db"]

	name_basics = db["name_basics"]
	title_basics = db["title_basics"]
	title_principals = db["title_principals"]
	title_ratings = db["title_ratings"]

	name_basics.drop()
	title_basics.drop()
	title_principals.drop()
	title_ratings.drop()

	with open("name.basics.json") as f:
		data = json.load(f)

	name_basics.insert_many(data)

	with open("title.basics.json") as f:
		data = json.load(f)

	title_basics.insert_many(data)

	with open("title.principals.json") as f:
		data = json.load(f)

	title_principals.insert_many(data)

	with open("title.ratings.json") as f:
		data = json.load(f)

	title_ratings.insert_many(data)

	return db