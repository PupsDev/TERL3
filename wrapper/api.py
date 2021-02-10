"""This module is the api wrapper"""

import os
import json
import requests
import requests_cache
import time

from wrapper.exceptions import (
    TwitterError,
    RequestError,
    AuthentificationError)

from wrapper.rate_limit import RateLimit
from wrapper.parser import Parser

requests_cache.install_cache('wrapper_cache')

class Api(object):
    """ Wrapper class for twitter api V2.0

        Basic usage :
        import wrapper

        api = new Api("BEARER_TOKEN")
        
        list of methods:

        >>> api.get_recent_search(query,fields)
        >>> api.get_tweet(ids,fields)
        >>> api.get_filtered_stream(fields)
        >>> api.get_sample_stream(fields)

        The results are cached by default for 10mn

    """

    # Base url for twitter api  V2.0
    # We will concatenate useful endpoints for the requests to it
    BASE_URL = "https://api.twitter.com/2/"

    # A singleton representing a lazily instantiated FileCache.
    # We delay the creation of the cache object before it's useful so we save memory if we don't need it

    def __init__(self,bearer_token=None, parse = False):
        """Instantiates a wrapper.Api object"""

        self.rate_limit = RateLimit()
        self._parse = parse
        if parse:
            self._parser = Parser()

        if bearer_token:
            self.headers = self._create_headers(bearer_token)
        else:
            raise AuthentificationError("The wrapper.Api instance must be authenticated.")

    def get_recent_search(self,query , fields, max_pages=0):
        """Get recent search 
        Args:
            query:
                argument to filter the search
                example: query="from:twitterdev -is:retweet"
            fields:
                fields of the tweet we want to retrieve
                example :tweet.fields="lang,author_id"
        Returns:
            A generator
        """
        url = self.BASE_URL+ "tweets/search/recent?query={}&{}".format(query, fields)

        response = self._request(url,"recent_search")

        i=0
        # -> needs review maybe different if parse or not parse 
        # otherwise yield only the first page

        if max_pages and self._parse:
            list_tweets = {}
            list_tweets['tweets'] = response['tweets']
            meta = response['meta']
            print("Fetching {} pages ..".format(max_pages))

            while 'next_token' in meta and i < max_pages:
                url = self.BASE_URL+ "tweets/search/recent?query={}&{}&next_token={}".format(query, fields,response['meta']['next_token'])
                response = self._request(url,"recent_search")
                meta = response['meta']
                list_tweets['tweets'].extend(response['tweets'])
                i+=1
                yield response['tweets']


        else :
            yield response

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
        # NOT AN INT FOR IDS
        if isinstance(ids, list): 
            string_id = ','.join(map(str, ids))
            url = self.BASE_URL + "tweets?ids={}&{}".format(string_id,fields)
        elif type(ids)== int:
            url = self.BASE_URL + "tweets/{}?&{}".format(str(ids),fields)

        else :
            raise ValueError("get_tweet function requires ids as a list of integers or a single integer.")


        return self._request(url,"tweet").json()


    def get_filtered_stream(self, fields=""):
        """ Get a filtered stream by the query"""

        url = self.BASE_URL+ "tweets/search/stream?{}".format(fields)
        return self._request(url,"filtered_stream")

    def get_sample_stream(self, fields=""):
        """ Get a sample stream representing the trends in the sample"""

        url = self.BASE_URL+ "tweets/sample/stream?{}".format(fields)
        return self._request(url,"sample_stream")
    def get_stream_rules(self, ids):
        """ Get the list of the rules active for the filtered stream"""

        url = self.BASE_URL+ "tweets/search/stream/rules?ids={}".format(ids)
        return self._request(url,"rules")

    def post_stream_rules(self, rules):
        """ Get the list of the rules active for the filtered stream"""

        url = self.BASE_URL+ "tweets/search/stream/rules"
        return self._request(url,"post_rules", rules) 

    def _create_headers(self,bearer_token):
        """ create the header of the request from the bearer token returns a header"""

        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    def _connect_to_endpoint(self,url, headers,endpoint, rules=""):
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


        if "post" in endpoint:
            payload = {"add": rules}
            response = requests.request("POST", url, headers=self.headers,  json=payload)

        elif "stream" in endpoint:
            with requests_cache.disabled():
                response = requests.request("GET", url, headers=self.headers, stream=True)


        else:
            response = requests.request("GET", url, headers=self.headers)
 
        self.rate_limit.set_limit(response.headers["x-rate-limit-remaining"],
                                            response.headers["x-rate-limit-reset"], endpoint)
        if response.status_code != 200:
            raise RequestError({"message":"Request returned an error: {} {}".format(
                    response.status_code, response.text
                ), "code": response.status_code}
                
            )

       
        return response

    def _request(self, url, endpoint, rules=""):
        """ Request function using cache
        Args:
            url:
                url of our call
            endpoint:
               endpoint specific to our call
        Returns:
            A JSON object
        """
        # We check if we have at least one call remaining for the endpoint


        remaining = int(self.rate_limit.get_limit(endpoint).remaining)
        if remaining > 0:
            try:
                response = self._connect_to_endpoint(url, self.headers,endpoint)
               
            except Exception as err:
                #print(err)
                return
        else:
            time_sleep = (float(self.rate_limit.get_limit(endpoint).reset)-time.time())+ 1
            print("Too many request for "+endpoint+" endpoint, waiting "+str(int(time_sleep)) + " second(s)...")
            time.sleep(time_sleep)


        

        if (self._parse):
            tweet = self._parser.parse(response)
            return tweet
        else:
            return response


    #Utilitary functions
    def get_remaining_calls(self):
        """ Get the remaining calls as a dict"""
        return self.rate_limit.get_remaining_calls()
    def print(self, data):
        """ Print data with a nice indented json format"""
        print(json.dumps(data,sort_keys=True, indent=4))


