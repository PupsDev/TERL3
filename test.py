# from wrapper import Api
# import json

# BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADAyLgEAAAAAc4eGilNnzVuxnuvfEZjxh%2BU7P74%3D4GbSIUdOdwOLnZ8ClQU8dtEGy6nz8ijBZs0sxZioTCskVyxNjY"
# api = Api(BEARER_TOKEN)
# ids = [1278747501642657792,255542774432063488]
# tweet_fields = ""
# json_response = api.get_tweet(ids,tweet_fields)
# api.print(json_response)

# for i in range(1,302):
# 	print(i)
# 	json_response = api.get_tweet(ids,tweet_fields)

# print(api.get_remaining_calls())
# with open ("testdata/get_tweet.json", "w") as f:
# 	json.dump(json_response, f, indent=4)
# f.close()

from database import Database

# with data
db = Database("mongodb://127.0.0.1:27017")

# db.select_database("test_db1")

# db.select_collection("test_coll1")

# data0 = {"_id" : 0, "name" : "name0", "surname" : "surname0", "age" : 50}
# data1 = {"_id" : 1, "name" : "name1", "surname" : "surname1", "age" : 25}
# data2 = {"_id" : 2, "name" : "name2", "surname" : "surname2", "age" : 52}
# data3 = {"_id" : 3, "name" : "name3", "surname" : "surname3", "age" : 23}
# data4 = {           "name" : "name4", "surname" : "surname4", "age" : 44}

# db._insert("", [data0, data1, data2, data3])

# db._insert("", data4)

# found = db.find_from_collection()

# db.print_found(found)

# with json file
db.select_database("test_db2")

db.select_collection("test_coll2")

db._insert("test.json")

found = db.find_from_collection()

db.print_found(found)