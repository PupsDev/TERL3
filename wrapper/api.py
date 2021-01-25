import requests
import os
import json
import time
from queue import PriorityQueue

# Wrapper class for twitter api V2.0

class Api(object):

	#Authentification dans une classe !
	BEARER_TOKEN = "BEARER_TOKEN"
	
	# Base url for twitter api  V2.0
	# We will concatenate useful endpoints for the requests to it
	BASE_URL = "https://api.twitter.com/2/"

	#Rate limit for 15 minutes window

	RATE_LIMIT_RECENT_SEARCH = 180
	RATE_LIMIT_TWEET = 300

	# 15 minutes = 900secondes
	INTERVAL = 15*60

	limit_queue = PriorityQueue()


	# A singleton representing a lazily instantiated FileCache.
	# We delay the creation of the cache object before it's useful so we save memory if we don't need it
	DEFAULT_CACHE = object()


	_cache = {}

	#Constructor
	def __init__(self, c = {}):
		self.cache = c

	def get_recent_search(query , fields):
		"""Get recent search 
		Args:
			query:
				argument to filter the search
				example: query="from:twitterdev -is:retweet"
			fields:
				fields of the tweet we want to retrieve
				example :tweet.fields="lang,author_id"
		Returns:
			A JSON object from the _request function
		"""
		url = self.BASE_URL+ "tweets/search/recent?query={}&{}".format(query, fields)
		return self._request(url,self.RATE_LIMIT_RECENT_SEARCH)

	def get_tweet(self,ids , fields):
		"""Get a specific tweet or a list of specific tweets by their ids
		Args:
			ids:
				must be a string
				unique id or list of tweets ids
			fields:
				fields of the tweet we want to retrieve
				example :tweet.fields="lang,author_id"
		Returns:
				A JSON object from the _request function
		"""

		#TO DO unique id or lists ids here only list of ids

		if isinstance(ids, list): 
			string_id = ','.join(map(str, ids))
			url = self.BASE_URL + "tweets?ids={}&{}".format(string_id, fields)
			print(url)
		else:
			url = self.BASE_URL + "tweets/{}&{}".format(str(ids), fields)

		return self._request(url,self.RATE_LIMIT_TWEET)

	#To implement
	def get_filtered_stream():
		return
	#To implement
	def get_sample_stream():
		return

	def _update_limit_queue(self,queue, interval, call_limit):
		"""Get a specific tweet or a list of specific tweets by their ids
        Args:
            queue:
                priority queue for storing the timestamps of the requests
            interval:
                time to wait before we can making more calls  
			call_limit:
				maximum calls we can make

        Returns:
           None
        """

        # While there is still timestamps in the queue, the first timestamp was made < interval secs

		while not queue.empty():
			timeSinceOldest = time.time()-queue.queue[0]

			# if it has been more than 15 min between first call and now we can pop the first call
			if timeSinceOldest > interval:
				queue.get()

			# if we reach the call limit we sleep the remaining time between the interval and the oldest call
			elif queue.qsize() >= call_limit :
				if timeSinceOldest < interval : 
					timesleep = int(interval - timeSinceOldest)
					print("Waiting "+ str(int((interval - timeSinceOldest)) + 1) + " second(s)..." )
					time.sleep(timesleep+1)
			else:
					break
		# we enqueue the new call timestamp
		queue.put(time.time())

	def _create_headers(self,bearer_token):
		# create the header of the request from the bearer token returns a header

		headers = {"Authorization": "Bearer {}".format(bearer_token)}
		return headers

	def _connect_to_endpoint(self,url, headers):
		""" Connect to the endpoint and check for error
        Args:
            url:
                url of our call
            headers:
               header from the bearer token
			 Raises:
          	 Exception: Exception if the return code is not 200 (invalid)

        Returns:
            A JSON object
        """
		response = requests.request("GET", url, headers=headers)
		#print(response.status_code)
		if response.status_code != 200:
			print("Request returned an error")
			raise Exception(
		        "Request returned an error: {} {}".format(
		            response.status_code, response.text
		        )
		    )
			
		return response

	def _request(self, url, rate_limit):
		""" Request function using cache
        Args:
            url:
                url of our call
            rate_limit:
               rate limit specific to our call
        Returns:
            A JSON object
        """

		# Basic cache checking
		if url in self.cache:
		   return self.cache[url]	    

		# We update limit queue before making our request 
		self._update_limit_queue(self.limit_queue, self.INTERVAL, rate_limit)

		headers = self._create_headers(self.BEARER_TOKEN)
		try:
  			response = self._connect_to_endpoint(url, headers)
		except Exception as err:
			return []
		
		return response.json()
	def print(self, data):
		print(json.dumps(data,sort_keys=True, indent=4))
    


###############

