from wrapper import Api
import json
import os
import sys
from database import Database

##
# use :
# backend.py BEARER_TOKEN DB_URL max_pages keyword
##


if sys.argc > 4:
	db = Database(sys.argv[1])

	db.select_database("disastweet")

	db.select_collection("spacetweets") #select or create a collection

	api = Api(sys.argv[2], True)
	tweet_fields = "expansions=geo.place_id&tweet.fields=geo,entities,author_id"
	max_results = 50
	max_pages = sys.argv[3]

	search = sys.argv[4]

	query = search+"&max_results="+str(max_results)
	response = api.get_yielded_recent_search(query,tweet_fields,max_pages)
	for tweets in response:
		db._insert("", tweets)
