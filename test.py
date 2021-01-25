from wrapper import Api
import json

api = Api()
ids = [1278747501642657792,1255542774432063488]
tweet_fields = ""

json_response = api.get_tweet(ids, tweet_fields)
api.print(json_response)
with open ("testdata/get_tweet.json", "w") as f:
	json.dump(json_response, f, indent=4)
f.close()