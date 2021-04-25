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
		self._rate_limit["sample_stream"] = EndpointRateLimit(50,50,0)
		self._rate_limit["search_stream"] = EndpointRateLimit(50,50,0)
		self._rate_limit["rules"] = EndpointRateLimit(450,450,0)
		self._rate_limit["post_rules"] = EndpointRateLimit(450,450,0)
		
	def get_remaining_calls(self):
		""" get remaining calls of the api as a dict"""

		return self._rate_limit
	def get_limit(self, endpoint):
		""" get limit of the endpoint as a named tuple"""
		
		return self._rate_limit[endpoint]


	def set_limit(self,remaining, reset, endpoint):
		""" Set the remaining and reset of the endpoint
			Create a new endpoint with default limit and update remaining and reset
		"""
		updated_endpoint = EndpointRateLimit(self._rate_limit[endpoint].limit,int(remaining),int(reset))
		self._rate_limit.update({endpoint: updated_endpoint})

		return self.get_limit(endpoint)

		
	


	
