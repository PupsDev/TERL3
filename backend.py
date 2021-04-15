from wrapper import Api
import json
import os
import sys
import pymongo

##
# use :
# backend.py DB_URL BEARER_TOKEN max_pages keyword
##

if len(sys.argv) > 4:
	client = pymongo.MongoClient(sys.argv[1]) #connexion

	db = client["disastweet"] #selection de la bdd

	collection = db.spacetweets #selection de la collection

	api = Api(sys.argv[2], True)
	tweet_fields = "expansions=geo.place_id&tweet.fields=geo,entities,author_id"
	max_results = 50
	max_pages = int(sys.argv[3])

	search = sys.argv[4]

	query = search+"&max_results="+str(max_results)
	response = api.get_yielded_recent_search(query,tweet_fields,max_pages)
	for tweets in response:
		for tweet in tweets:
			tweet["valid"] = "?"

	collection.insert_many(tweets) #insertion multiple