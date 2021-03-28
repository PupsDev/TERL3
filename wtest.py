from wrapper import Api
import json
import os

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADAyLgEAAAAAc4eGilNnzVuxnuvfEZjxh%2BU7P74%3D4GbSIUdOdwOLnZ8ClQU8dtEGy6nz8ijBZs0sxZioTCskVyxNjY"
api = Api(BEARER_TOKEN, True)
ids=[1278747501642657792,1255542774432063488]

tweet_fields = "expansions=geo.place_id&tweet.fields=lang,author_id,geo,entities"
max_results = 30
max_pages = 20


search_list = ["Doublepups"]


for search in search_list :
	query = "from:"+search+"&max_results="+str(max_results)

	response = api.get_recent_search(query,tweet_fields,max_pages)

	print(search)

	api.print(response)
	with open(search+".json", "w", encoding='utf-8') as outfile:
		json.dump(response, outfile)