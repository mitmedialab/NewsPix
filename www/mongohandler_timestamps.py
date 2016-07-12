import os, ConfigParser
from pymongo import MongoClient
from event_timestamp import EventTimestamp
from date import Date
from bson.objectid import ObjectId

class MongoHandlerTimestamps:

	def __init__(self, host, port, db, collection):
		self.client = MongoClient(host, int(port))
		self.db = self.client[db]
		self.collection = self.db[collection]

	def register_event(self, event):
		self.collection.save(event.get_installation_object())

	def get_organization_event_count(self, organization):
		result = self.get_organization_events(organization)
		return len(result)

	def get_events(self, cursor):
		events = []
		idx = cursor.count()
		if cursor.count() == 0:
			return events
		for event in cursor:
			events.append(EventTimestamp(
				event.get('organization'),
				event.get('date')
			))
			idx-=1
		return events

	def get_all_events(self):
		return self.get_events(self.collection.find().sort("date", 1))

	def get_organization_events(self, organization):
		return self.get_events(self.collection.find({'organization': organization}).sort("date", 1))