from collections import namedtuple

EndpointRateLimit = namedtuple('EndpointRateLimit',
								['limit', 'remaining', 'reset'])
class RateLimit(object):
	"""RateLimit class for twitter api V2.0"""

	def __init__(self):
		""" Instantiates a RateLimit Object"""
		self._rate_limit = {}
		self._rate_limit["recent_search"] = EndpointRateLimit(180,180,0)
		self._rate_limit["tweet"] = EndpointRateLimit(300,300,0)
	def get_remaining_calls(self):
		""" get remaining calls of the api as a dict"""

		return {"recent_search" : self._rate_limit["recent_search"].remaining,
				 "tweet" : self._rate_limit["tweet"].remaining}

	def get_limit(self, endpoint):
		""" get limit of the endpoint as a named tuple"""
		return self._rate_limit[endpoint]


	def set_limit(self,remaining, reset, endpoint):
		""" Set the remaining and reset of the endpoint
			Create a new endpoint with default limit and update remaining and reset
		"""
		updated_endpoint = EndpointRateLimit(self._rate_limit[endpoint],remaining,reset)
		self._rate_limit.update({endpoint: updated_endpoint})

		return self.get_limit(endpoint)

		
	


	
