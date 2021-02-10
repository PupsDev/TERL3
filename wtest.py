from wrapper import Api
import json
import os

BEARER_TOKEN = ""
api = Api(BEARER_TOKEN)
ids=[1278747501642657792,1255542774432063488]

tweet_fields = "tweet.fields=lang,author_id"
max_results = 10
max_pages = 0
search = "%23twitter"
query = search+"&max_results="+str(max_results)


# json_response = api.get_tweet(ids,tweet_fields)

# api.print(json_response['data'])
# for r in json_response['data']:
# 	for key,value in r.items():
# 		print(value)

# response = api.get_recent_search(query,tweet_fields,max_pages)

# print("Get recent search : ")
# tweets_list = []

# # for tweets in response:
# # 	api.print(tweets)


# path = os.getcwd()
# path += '/testdata'

# method = "get_recent_search"
# test_result = method+".json"

# with open(path+'/'+test_result, "w") as outfile:
# 	for tweets in response:
# 		json.dump(tweets, outfile)

json_response = api.get_sample_stream()
print(json_response)

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

