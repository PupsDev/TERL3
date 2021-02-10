import unittest
import wrapper
import responses
import json
import types

DEFAULT_URL = "https://api.twitter.com/2/"
BEARER_TOKEN = ""

''' 
	To do :
			- Test exceptions
			- Test Streams
'''
class ApiTest(unittest.TestCase):

	def setUp(self):
		self.api = wrapper.Api(BEARER_TOKEN)

	#Tests Get_tweet
	''' We test if our method can return exactly what we
		expect it to return by checking with already saved data.
		We test for one tweet, multiples tweets and with
		fields parameters
	'''
	@responses.activate
	def test_get_tweet(self):
		with open ("testdata/get_tweet.json", "r") as f:
			resp_data = json.load(f)

		ids = 1278747501642657792

		responses.add(responses.GET, DEFAULT_URL, body=resp_data)
		resp = self.api.get_tweet(ids)
		for key,value in resp['data'].items():
			self.assertEqual(value, resp_data['data'][0][key])
		

	@responses.activate
	def test_get_tweet_with_fields(self):
		with open ("testdata/get_tweets_with_fields.json", "r") as f:
			resp_data = json.load(f)

		ids = 1278747501642657792
		tweet_fields = "tweet.fields=lang,author_id"
		responses.add(responses.GET, DEFAULT_URL, body=resp_data)
		resp = self.api.get_tweet(ids,tweet_fields)

		for key,value in resp['data'].items():
			self.assertEqual(value, resp_data['data'][0][key])
	@responses.activate
	def test_get_tweets_with_fields(self):
		with open ("testdata/get_tweets_with_fields.json", "r") as f:
			resp_data = json.load(f)

		ids = [1278747501642657792,1255542774432063488]
		tweet_fields = "tweet.fields=lang,author_id"
		responses.add(responses.GET, DEFAULT_URL, body=resp_data)
		resp = self.api.get_tweet(ids,tweet_fields)

		for r,v in enumerate(resp['data']):
			for key,value in resp['data'][r].items():
				self.assertEqual(value, resp_data['data'][r][key])

	#Tests Get_recent_search
	''' We test the generator of the get_recent_search method.
	'''
	@responses.activate
	def test_get_recent_search(self):
		with open ("testdata/get_recent_search.json", "r") as f:
			resp_data = json.load(f)

		# hashtags must be encoded as %23
		search = "%23twitter" 

		# Max result fixed at 10
		query = search+"&max_results=10"
		tweet_fields = "expansions=geo.place_id&tweet.fields=geo,entities,author_id"
		responses.add(responses.GET, DEFAULT_URL, body=resp_data)
		resp = self.api.get_recent_search(query,tweet_fields,max_pages=0)

		# We convert the generator in a list
		tweet = list(resp)

		# We take only the first item of the list because max_pages = 0
		tweet = tweet[0].json()

		# We only test if twitter is in the text of each tweets
		for r,v in enumerate(tweet['data']):
			self.assertTrue(['twitter' in tweet['data'][r]['text']])


	'''
		Streams weirdly return none, might be because of unittest.TestCase
	'''
	#Tests Get_sample_stream
	@responses.activate
	def test_get_sample_stream(self):
		resp = self.api.get_sample_stream()
		pass
		
	#Tests Get_filtered_stream
	@responses.activate
	def test_get_filtered_stream(self):
		pass




