import os, ConfigParser
from pymongo import MongoClient
from organization import Organization
from date import Date
from bson.objectid import ObjectId

CONFIG_FILENAME = 'organizations.config'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser.ConfigParser()
safe_config = ConfigParser.SafeConfigParser();

config.read(os.path.join(BASE_DIR, CONFIG_FILENAME))
safe_config.read(os.path.join(BASE_DIR, CONFIG_FILENAME))

class MongoHandlerOrganizations:

	def __init__(self, host, port, db, collection):
		self.client = MongoClient(host, int(port))
		self.db = self.client[db]
		self.collection = self.db[collection]

	def save_organization(self, organization):
		result = self.collection.find_one({"login_username": organization.login_username})
		if not result:
			self.collection.save(organization.get_organization_object())
			config.read(os.path.join(BASE_DIR, CONFIG_FILENAME))
			config.set('organizations', organization.login_username, organization.login_password)
			with open(os.path.join(BASE_DIR, CONFIG_FILENAME), 'w') as config_file:
				config.write(config_file)
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
				organization.get('_id'),
				organization.get('number_of_installations')
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
			safe_config.remove_option("organizations", result['login_username'])
			config.read(os.path.join(BASE_DIR, CONFIG_FILENAME))

	def login(self, username, password):
		result = self.collection.find_one({"login_username": username})
		if not result:
			return False
		if result['login_password'] == password:
			return True
		return False

	
