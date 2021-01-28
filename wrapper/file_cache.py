import os
from hashlib import md5

class _FileCacheError(Exception):
	"""Base exception class for FileCache related errors"""


class _FileCache(object):
	""" Instantiates a FileCache Object"""