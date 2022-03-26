run:
	python3 main.py

startDB:
	mongod --port 27012 --dbpath mongoDBDataFolder

checkDB:
	mongo --port 27012 