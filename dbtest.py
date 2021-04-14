from database import Database
import os
import json

db = Database("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

db.select_database("disastweet")

 db.select_collection("spacetweets") #select or create a collection

files = os.listdir("./spacetweets")
for file in files:
	rep = "./spacetweets/"+file
	with open(rep) as json_data:
	    data_dict = json.load(json_data)
	    db._insert("", data_dict["tweets"])

found = db.find_from_collection()

db.print_found(found)