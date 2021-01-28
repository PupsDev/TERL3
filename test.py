from wrapper import Api
import json

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADAyLgEAAAAAc4eGilNnzVuxnuvfEZjxh%2BU7P74%3D4GbSIUdOdwOLnZ8ClQU8dtEGy6nz8ijBZs0sxZioTCskVyxNjY"
api = Api(BEARER_TOKEN)
ids = [1278747501642657792,255542774432063488]
tweet_fields = ""
json_response = api.get_tweet(ids,tweet_fields)
api.print(json_response)

for i in range(1,302):
	print(i)
	json_response = api.get_tweet(ids,tweet_fields)

print(api.get_remaining_calls())
with open ("testdata/get_tweet.json", "w") as f:
	json.dump(json_response, f, indent=4)
f.close()
