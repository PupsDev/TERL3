from wrapper import Api
import json

BEARER_TOKEN = "BEARER_TOKEN"
api = Api(BEARER_TOKEN)
ids = [1358020945215127553]

tweet_fields = "expansions=geo.place_id&tweet.fields=geo,entities,author_id"
max_results = 50
max_pages = 5
search = "Earthquakes"
query = search+"&max_results="+str(max_results)


#json_response = api.get_tweet(ids,tweet_fields)

response = api.get_recent_search(query,tweet_fields,max_pages)

print("Get recent search : ")
tweets_list = []

for tweets in response:
	api.print(tweets)




# json_response = api.get_sample_stream()
# for response_line in json_response.iter_lines():
# 	if response_line:
# 		json_response = json.loads(response_line)
# 		print(json.dumps(json_response, indent=4, sort_keys=True))

# print("Get tweets : ")
# print(json.dumps(json_response,sort_keys=True, indent=2))


# json_response3 = api.get_sample_stream()
# for i in range(1,3):
	
# for response_line in json_response3.iter_lines(3):
# 	if response_line:
# 		json_response = json.loads(response_line)
# 		print(json.dumps(json_response, indent=4, sort_keys=True))

