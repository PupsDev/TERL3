from wrapper import Api

api = Api()
ids = [1278747501642657792,1255542774432063488]
tweet_fields = "tweet.fields=lang,author_id"

json_response = api.get_tweet(ids, tweet_fields)
api.print(json_response)