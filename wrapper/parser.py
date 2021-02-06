import json

class Parser(object):
	""" Parser class for twitter api V2.0
		takes a json object from twitter
		parses it into a valid json format
		used for this Project :

			{
			"data" : 
				[
					"author_id": "author_id",
					"id": "tweet_id",
					"text" : "actual tweet message",
					"geo" : "geo coord, geo coord" or "NULL",
					"place" : "string name of location based on annotations with related probabilities",
					"place_user" : "string name of location defined by user",
					"valid" : "true if tweet is valid : \
								containing keywords about a natural disaster \
								referencing to a location -> geo not NULL\
								AND verified for the data set
								False otherwise",
					"real" : "true if the tweet was scrapped from twitter and False\
							if it was made with our data fixtures algorithm"
				]
			}

			# To do :
			 - regex hashtags ?
	"""
	def __init__(self ):
		""" Instantiates a Parser Object"""

	def parse(self, tweets):
		""" Parse the tweet into a proper json format with added information 
			Takes a tweet as Json dict and return the parsed tweet as json
		"""
		dict_tweets = {}
		list_tweets = []

		tweets_json =  tweets.json()

		for tweet in tweets_json['data']:
			parsed_tweet = {}
			parsed_tweet['place'] = {}
			if 'geo' not in tweet : 
				parsed_tweet['geo'] = "NULL"
				parsed_tweet['valid'] = "False"
				parsed_tweet['place_user'] = "NULL"
				# If there is no geo tag for the tweet we look for informations in annotations
				if 'entities' in tweet:
					if 'annotations' in tweet['entities']:
						for annotation in tweet['entities']['annotations']:
							if 'Place' in annotation['type']:
								parsed_tweet['place'][annotation['normalized_text']] = annotation['probability']
				
			else:
				if 'place_id' in tweet['geo']:
					# If there is a place_id it should have a includes->places
					for place in tweets_json['includes']['places']:
						if tweet['geo']['place_id'] == place['id']:
							parsed_tweet['place_user'] = place['full_name']
				if 'coordinates' not in tweet['geo']:
					parsed_tweet['geo'] = "NULL"
				else :
					parsed_tweet['geo'] = tweet['geo']['coordinates']['coordinates']
				parsed_tweet['valid'] = "True"
				
			# Tweet comes directly from the twitter API so always True
			parsed_tweet['real'] = "True"
			# Place is empty so -> NULL
			if not parsed_tweet['place']:
				parsed_tweet['place'] = "NULL"
			parsed_tweet['text'] = tweet['text']
			parsed_tweet['id'] = tweet['id']
			parsed_tweet['author_id'] = tweet['author_id']
			
			list_tweets.append(parsed_tweet)
			dict_tweets['tweets'] = list_tweets

			if 'meta' in tweets_json:
				dict_tweets['meta'] = tweets_json['meta']

		return dict_tweets