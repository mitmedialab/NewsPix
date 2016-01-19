import os, ConfigParser
from pymongo import MongoClient
from organization import Organization
from date import Date
from bson.objectid import ObjectId

class MongoHandlerOrganizations:

	def __init__(self, host, port, db, collection):
		self.client = MongoClient(host, int(port))
		self.db = self.client[db]
		self.collection = self.db[collection]

	def save_organization(self, organization):
		result = self.collection.find_one({"login_username": organization.login_username})
		if not result:
			self.collection.save(organization.get_organization_object())
		return False

	def get_organizations(self, cursor):
		organizations = []
		idx = cursor.count()
		if cursor.count() == 0:
			return organizations
		for organization in cursor:
			organizations.append(Organization(
				organization.get('name'),
				organization.get('login_username'),
				organization.get('login_password'),
				organization.get('url'),
				organization.get('logo_url'),
				organization.get('_id')
			))
			idx-=1
		return organizations

	def get_all_organizations(self):
		return self.get_organizations(self.collection.find())

	def get_organization(self, username):
		return self.collection.find_one({"login_username": username})

	def remove_organization(self, organizationID):
		result = self.collection.find_one({"_id": ObjectId(organizationID)})
		if result:
			self.collection.remove({"_id": ObjectId(organizationID)})

	def is_valid_organization(self, username):
		result = self.collection.find_one({"login_username": username})
		if not result:
			return False
		return True

	def is_authorized(self, username, password):
		result = self.collection.find_one({"login_username": username})
		if not result:
			return False
		if result['login_password'] == password:
			return True
		return False


	
