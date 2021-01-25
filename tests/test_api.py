import unittest
import wrapper
import responses
import json

DEFAULT_URL = "https://api.twitter.com/2/"
class ApiTest(unittest.TestCase):

	def setUp(self):
		self.api = wrapper.Api()
	@responses.activate
	@responses.activate

	def test_get_tweet(self):
		with open ("testdata/get_tweet.json", "r") as f:
			resp_data = json.load(f)

		ids = 1278747501642657792
		tweet_fields=""
		responses.add(responses.GET, DEFAULT_URL, body=resp_data)
		resp = self.api.get_tweet(ids,tweet_fields)
		for r in resp:
			for key,value in r.items():
				assertEqual(value, resp_data[key])
		

	@responses.activate
	def test_get_tweet_with_fields(self):
		with open ("testdata/get_tweets_with_fields.json", "r") as f:
			resp_data = json.load(f)

		ids = 1278747501642657792
		tweet_fields = "tweet.fields=lang,author_id"
		responses.add(responses.GET, DEFAULT_URL, body=resp_data)
		resp = self.api.get_tweet(ids,tweet_fields)
		for r in resp:
			for key,value in r.items():
				assertEqual(value, resp_data[key])

	@responses.activate
	def test_get_tweets_with_fields(self):
		with open ("testdata/get_tweets_with_fields.json", "r") as f:
			resp_data = json.load(f)

		ids = [1278747501642657792,1255542774432063488]
		tweet_fields = "tweet.fields=lang,author_id"
		responses.add(responses.GET, DEFAULT_URL, body=resp_data)
		resp = self.api.get_tweet(ids,tweet_fields)
		for r in resp:
			for key,value in r.items():
				assertEqual(value, resp_data[key])

	#TO DO get_recent_search


