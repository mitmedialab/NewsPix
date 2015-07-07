from pymongo import MongoClient
from story import Story

class MongoHandler:

	def __init__(self):
		self.client = MongoClient("localhost", 27017)
		self.db = self.client.stories
		self.collection = self.db.collection

	def save_story(self, story):
		self.collection.save(story.get_story_object())
		print "SAVE STORY"

	def get_stories(self, cursor):
		stories = []
		if cursor.count() == 0:
			return stories
		for story in cursor:
			stories.append(Story(story.get('headline'), story.get('url'), story.get('image'), story.get('date'), story.get('to_date'), story.get('_id'), story.get('load_count'), story.get('click_count')))
		return stories

	def get_all_stories(self):
		return self.get_stories(self.collection.find().sort("date", -1))

	def get_stories_on_date(self, date):
		cursor = self.collection.find({"date": date})
		return self.get_stories(cursor)

	def get_stories_before_date(self, date):
		cursor = self.collection.find({"date": {"$lte": date}})
		return self.get_stories(cursor)

	def get_stories_after_date(self, date):
		cursor = self.collection.find({"date": {"$gt": date}})
		return self.get_stories(cursor)

	def get_active_stories(self, date):
		cursor = self.collection.find({"date": {"$lte": date}, "to_date": {"$gte": date}})
		return self.get_stories(cursor)

	def get_next_active_story(self, storyID):
		
		active_stories = self.get_active_stories(date_handler.today)
		if not active_stories:
			return None

		last_index = len(active_stories)-1
		
		if storyID is None or storyID == "0":
			return active_stories[last_index].get_story_object()

		position = last_index
		while position > 0:
			if active_stories[position].get_story_object()['_id'] == ObjectId(storyID):
				return active_stories[position-1].get_story_object()
			else:
				position -= 1

		return active_stories[last_index].get_story_object()

	def remove_story(self, storyID):
		self.collection.remove({"_id": ObjectId(storyID)})
		print "REMOVE STORY"

	def register_load(self, storyID):
		self.collection.update({"_id": ObjectId(storyID)}, {"$inc": {"load_count": 1}})

	def register_click(self, storyID):
		self.collection.update({"_id": ObjectId(storyID)}, {"$inc": {"click_count": 1}})