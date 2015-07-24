from pymongo import MongoClient
from story import Story
from date import Date
from bson.objectid import ObjectId

class MongoHandler:

	def __init__(self, host, port, db, collection):
		self.client = MongoClient(host, int(port))
		self.db = self.client[db]
		self.collection = self.db[collection]
		self.date_handler = Date()

	def save_story(self, story):
		self.collection.save(story.get_story_object())
		print "SAVE STORY"

	def get_stories(self, cursor):
		stories = []
		if cursor.count() == 0:
			return stories
		for story in cursor:
			stories.append(Story(
				story.get('headline'), 
				story.get('url'), 
				story.get('image'), 
				story.get('date'), 
				story.get('to_date'), 
				story.get('_id'), 
				story.get('load_count'), 
				story.get('click_count'),
				story.get('position')))
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
		return self.get_stories(cursor.sort("position", -1))

	def get_active_stories(self, date):
		cursor = self.collection.find({"date": {"$lte": date}, "to_date": {"$gte": date}})
		return self.get_stories(cursor.sort("position", -1))

	def get_active_story(self, storyID, isNextStory=True):
		
		active_stories = self.get_active_stories(self.date_handler.today)
		if not active_stories:
			return None

		if storyID is None or storyID == "0":
			return active_stories[len(active_stories)-1].get_story_object()

		current_position = self.get_story_position(storyID, active_stories)
		return self.get_next_story_from_position(current_position, active_stories, isNextStory)

	def get_story_position(self, storyID, active_stories):
		for story in active_stories:
			if story._id == ObjectId(storyID):
				return story.position
		return 0

	def get_next_story_from_position(self, position, active_stories, isNextStory):
		print "Current position: " + str(position)
		print "isNextStory: " + str(isNextStory)
		
		position_changed = False
		
		if position == 0 and isNextStory:
			return self.get_story_at_position(self.get_highest_position(active_stories), active_stories)

		position_to_get = 0
		
		for story in active_stories:

			story_position = story.position
			print "Current iterating position: " + str(story_position)

			#we want the next story
			if isNextStory:
				if story_position > position_to_get and story_position < position:
					position_to_get = story_position
					position_changed = True
					
			#we want the previous story
			else:
				if story_position > position:
					position_to_get = story_position
					position_changed = True
					print "Position changed"
		
		if isNextStory == False and position_changed == False:
			return self.get_story_at_position(self.get_lowest_position(active_stories), active_stories)
					
		return self.get_story_at_position(position_to_get, active_stories)

	def get_story_at_position(self, position, active_stories):
		for story in active_stories:
			if story.position == position:
				return story.get_story_object()
		return active_stories[0].get_story_object()

	def get_highest_position(self, active_stories):
		highest_position = 0
		for story in active_stories:
			if story.position > highest_position:
				story.position = highest_position
		return highest_position

	def get_lowest_position(self, active_stories):
		lowest_position = None
		for story in active_stories:
			if lowest_position == None:
				lowest_position = story.position 
			elif story.position < lowest_position:
				lowest_position = story.position
		print "lowest position is " + str(lowest_position)
		return lowest_position

	def remove_story(self, storyID):
		self.collection.remove({"_id": ObjectId(storyID)})
		print "REMOVE STORY"

	def register_load(self, storyID):
		self.collection.update({"_id": ObjectId(storyID)}, {"$inc": {"load_count": 1}})

	def register_click(self, storyID):
		self.collection.update({"_id": ObjectId(storyID)}, {"$inc": {"click_count": 1}})

	def get_story_count(self):
		#NOTE FROM CATHERINE - server using Mongo 2.0.4 so doesn't support the aggregate command
		#cursor = self.collection.aggregate([{"$group": { "_id": None, "count": { "$sum": 1 }}}])
		#if len(cursor["result"]) == 0:
		#	return 0
		#return cursor["result"][0]["count"]
		active_stories = self.get_active_stories(self.date_handler.today)
		if not active_stories:
			return 0
		else:	
			return len(active_stories)

		