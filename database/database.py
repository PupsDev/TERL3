# -*- coding:utf8 -*-

from pymongo import MongoClient
import json

class Database(object):
	CLIENT = None
	DATABASE = None
	COLLECTION = None

	def __init__(self, uri):
		"""Constructor
		Args:
			uri:
				example:
					"mongodb://localhost:27017"
		Returns:
			None
		"""
		try:
			self.CLIENT = MongoClient(uri)
		except Exception as e:
			raise e

	def select_database(self, db_name):
		"""Select a database
		Args:
			db_name:
				name of the wished database
		Returns:
			None
		"""

		self.DATABASE = self.CLIENT[db_name]

	def select_collection(self, collection_name):
		"""Select a collection from the DATABASE
		Args:
			collection_name:
				name of the wished collection
		Returns:
			None
		"""

		self.COLLECTION = self.DATABASE[collection_name]

	def _insert(self, json_file="", data=[]):
		"""Insert data into the current COLLECTION
		Args:
			json_file:
				json file to load
			data:
				data to insert if json_file is not specified
		Returns:
			None
		"""

		try:
			if json_file != "":
				with open(json_file) as f:
					data = json.load(f)

			if isinstance(data, list):
				self.COLLECTION.insert_many(data) 
			else:
				self.COLLECTION.insert_one(data)
		except Exception as e:
			raise e
			

	def _delete(self, rules={}, many=True):
		"""Delete from the COLLECTION one or many data
		Args:
			rules:
				elements which respect the rules will be treat
				WARNING:
					if rules={} (are not specified), many will be consider like true all data will be delete
			many:
				if many is true, many data will be delete, else just one
		Returns:
			None
		"""

		if many == True:
			self.COLLECTION.delete_many(rules)
		else:
			self.COLLECTION.delete_one(rules)

	def find_from_collection(self, rules={}):
		"""Find from the COLLECTION data which respect the rules
		Args:
			rules:
				elements which respect the rules will be treat
		Returns:
			data which respect the rules from the COLLECITON
		"""

		found = self.COLLECTION.find(rules)
		return found

	def print_found(self, found):
		"""Print found element from the collection"""
		for x in found:
			print(x)