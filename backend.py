from wrapper import Api
import json
import os
import sys

##
# use :
# backend.py BEARER_TOKEN max_pages keyword
##

if sys.argc > 3:

	api = Api(sys.argv[1], True)
	tweet_fields = "expansions=geo.place_id&tweet.fields=geo,entities,author_id"
	max_results = 50
	max_pages = sys.argv[2]

	search = sys.argv[3]

	query = search+"&max_results="+str(max_results)
	response = api.get_yielded_recent_search(query,tweet_fields,max_pages)
	for tweets in response:
		with open("search.json", "w", encoding='utf-8') as outfile:
				json.dump(tweets, outfile)
