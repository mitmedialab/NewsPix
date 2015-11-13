import os, ConfigParser
from pymongo import MongoClient
from installation import Installation
from date import Date
from bson.objectid import ObjectId

class MongoHandlerInstallations:

	def __init__(self, host, port, db, collection):
		self.client = MongoClient(host, int(port))
		self.db = self.client[db]
		self.collection = self.db[collection]

	def register_installation(self, installation):
		self.collection.save(installation.get_installation_object())

	def get_installations(self, cursor):
		installations = []
		idx = cursor.count()
		if cursor.count() == 0:
			return installations
		for installation in cursor:
			installations.append(Installation(
				installation.get('organization'),
				installation.get('date')
			))
			idx-=1
		return installations

	def get_all_installations(self):
		return self.get_installations(self.collection.find().sort("date", -1))

	def get_organization_installations(self, organization):
		return self.get_installations(self.collection.find({'organization': organization}).sort("date", -1))