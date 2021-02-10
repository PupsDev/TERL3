from wrapper import Api
import json
import os

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADAyLgEAAAAAc4eGilNnzVuxnuvfEZjxh%2BU7P74%3D4GbSIUdOdwOLnZ8ClQU8dtEGy6nz8ijBZs0sxZioTCskVyxNjY"
api = Api(BEARER_TOKEN, True)


tweet_fields = "expansions=geo.place_id&tweet.fields=geo,entities,author_id"
max_results = 50
max_pages = 2


search_list = []
f = open("keyWord.txt", "r")
for x in f:
	search_list.append(x)

cwd_path = os.getcwd()
cwd_path+='/training_data'


try:
    os.mkdir(cwd_path)
except OSError:
    print ("Creation of the directory %s failed" % cwd_path)
else:
    print ("Successfully created the directory %s " % cwd_path)

for search in search_list:
	search = search.rstrip()
	path= cwd_path+'/'+search
	try:
	    os.mkdir(path)
	except OSError:
	    print ("Creation of the directory %s failed" % path)
	else:
	    print ("Successfully created the directory %s " % path)
	print("Get recent search for '%s' : " % search)	 
	tweets_list = []
	query = search+"&max_results="+str(max_results)
	response = api.get_recent_search(query,tweet_fields,max_pages)
	i=1
	for tweets in response:
		tweets_list.append(tweets)
		with open(path+'/'+search+str(i)+".json", "w", encoding='utf-8') as outfile:
			json.dump(tweets, outfile)
		i+=1