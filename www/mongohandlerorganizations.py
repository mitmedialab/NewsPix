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
		self.collection.save(organization.get_organization_object())

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

	def remove_organization(self, organizationID):
		self.collection.remove({"_id": ObjectId(organizationID)})