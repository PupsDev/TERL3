"""This module is the api wrapper"""

import os
import json
import requests
import time

from wrapper.file_cache import _FileCache
from wrapper.exceptions import (
    TwitterError,
    RequestError,
    AuthentificationError)

from wrapper.rate_limit import RateLimit

DEFAULT_CACHE = object()

class Api(object):
    """ Wrapper class for twitter api V2.0

        Basic usage :
        import wrapper

        api = new Api("BEARER_TOKEN")
        
        list of methods:

        >>> api.get_recent_search(query,fields)
        >>> api.get_tweet(ids , fields)
        >>> api.get_filtered_stream(query,fields)
        >>> api.get_sample_stream(query,fields)

        The results are cached by default for 10mn

    """

    # Base url for twitter api  V2.0
    # We will concatenate useful endpoints for the requests to it
    BASE_URL = "https://api.twitter.com/2/"

    # A singleton representing a lazily instantiated FileCache.
    # We delay the creation of the cache object before it's useful so we save memory if we don't need it

    DEFAULT_CACHE_TIMEOUT = 600


    _cache = {}

    def __init__(self,bearer_token=None,cache=DEFAULT_CACHE):
        """Instantiates a wrapper.Api object"""
        self._set_cache(cache)
        self.rate_limit = RateLimit()


        if bearer_token:
            self.headers = self._create_headers(bearer_token)
        else:
            raise AuthentificationError("The wrapper.Api instance must be authenticated.")

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
        return self._request(url,"recent_search")

    def get_tweet(self,ids , fields=""):
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
        elif isinstance(ids, int):
            url = self.BASE_URL + "tweets/{}&{}".format(str(ids), fields)
        else :
            raise ValueError("get_tweet function requires ids as a list of integers or a single integer.")

        return self._request(url,"tweet")

    #To implement
    def get_filtered_stream():
        """ Get a filtered stream by the query"""
        return
    #To implement
    def get_sample_stream():
        """ Get a sample stream representing the trends in the sample"""
        return

    def _create_headers(self,bearer_token):
        """ create the header of the request from the bearer token returns a header"""

        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    def _connect_to_endpoint(self,url, headers,endpoint):
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
        response = requests.request("GET", url, headers=self.headers)
        #print(response.status_code)
        self.rate_limit.set_limit(response.headers["x-rate-limit-remaining"],
                                            response.headers["x-rate-limit-reset"], endpoint)
        if response.status_code != 200:
            raise RequestError({"message":"Request returned an error: {} {}".format(
                    response.status_code, response.text
                ), "code": response.status_code}
                
            )

            
        return response

    def _request(self, url, endpoint):
        """ Request function using cache
        Args:
            url:
                url of our call
            endpoint:
               endpoint specific to our call
        Returns:
            A JSON object
        """

        # Basic cache checking
        #to do cache
        #if url in self.cache:
        #   return self.cache[url]       

        # We check if we have at least one call remaining for the endpoint
        remaining = int(self.rate_limit.get_limit(endpoint).remaining)
        if remaining > 0 :
            try:
                response = self._connect_to_endpoint(url, self.headers,endpoint)
               
            except Exception as err:
                print(err)
                return
        else :
            time_sleep = (float(self.rate_limit.get_limit(endpoint).reset)-time.time())+ 1
            print("Too many request for "+endpoint+" endpoint, waiting "+str(int(time_sleep)) + " second(s)...")
            time.sleep(time_sleep)
        
        return response.json()
    def _set_cache(self, cache):
        """Override the default cache.  Set to None to prevent caching.
        Args:
            cache:
                An instance that supports the same API as the twitter._FileCache
        """
        if cache == DEFAULT_CACHE:
            self._cache = _FileCache()
        else:
            self._cache = cache

    #Utilitary functions
    def get_remaining_calls(self):
        """ Get the remaining calls as a dict"""
        return self.rate_limit.get_remaining_calls()
    def print(self, data):
        """ Print data with a nice indented json format"""
        print(json.dumps(data,sort_keys=True, indent=4))


