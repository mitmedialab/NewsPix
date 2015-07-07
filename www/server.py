import os, ConfigParser, random, requests, json, datetime
from flask.ext.cors import CORS, cross_origin
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask,render_template,request
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True
app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {
	r"/random_story/*": {"origins": "*"},
	r"/get_story/*": {"origins": "*"},
	r"/register_click/*": {"origins": "*"}
}

cors = CORS(app)

# constants
CONFIG_FILENAME = 'app.config'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MongoDB & links to each collection
'''uri = "mongodb://"+ config.get('db','user')+ ":"+ config.get('db','pass')+"@" +config.get('db','host') + ":" + config.get('db','port')+"/?authSource="+config.get('db','auth_db')
print uri
db_client = MongoClient(uri)
app.db = db_client[config.get('db','name')]
app.db_weather_collection = app.db[config.get('db','weather_collection')]
app.db_jokes_collection = app.db[config.get('db','jokes_collection')]
'''
@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/oninstall')
def oninstall():
	return render_template('oninstall.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	
	active_stories = None
	upcoming_stories = None
	tomorrows_stories = None
	todays_stories = None
	
	if request.method == 'POST':
		# get new story
		story = Story (
			request.form.get('headline', None),
			request.form.get('storyURL', None),
			request.form.get('imageURL', None),
			date_handler.date_to_datetime(request.form.get('date', None)),
			date_handler.date_to_datetime(request.form.get('to_date', None)),
			None,
			0,
			0)
		mongo_handler.save_story(story)
		
	return render_admin_panel()

@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
	all_stories = mongo_handler.get_all_stories()
	return render_template('analytics.html', stories=all_stories, analytics=analytics)

@app.route('/random_story', methods=['GET', 'POST'])
def random_story():

	stories = mongo_handler.get_active_stories(date_handler.today)
	
	if not stories:
		return "no stories"
	else:
		random_index = random.randint(0, len(stories)-1)
		result = stories[random_index].get_story_object()
		mongo_handler.register_load(result['_id'])
		return json.dumps(result, default=json_util.default)

@app.route('/get_story/<storyID>', methods=['GET', 'POST'])
def get_story(storyID):
	result = mongo_handler.get_next_active_story(storyID)
	if result is None:
		return "no stories"
	else:
		mongo_handler.register_load(result['_id'])
		return json.dumps(result, default=json_util.default)

@app.route('/delete_story/<storyID>', methods=['GET', 'POST'])
def delete_story(storyID):
	mongo_handler.remove_story(storyID)
	return render_admin_panel()

@app.route('/register_click/<storyID>', methods=['GET', 'POST'])
def register_click(storyID):
	mongo_handler.register_click(storyID)
	return render_template('register_click.html')

def render_admin_panel():
	today = date_handler.format_date(date_handler.today)
	tomorrow = date_handler.format_date(date_handler.tomorrow)
	upcoming_stories = mongo_handler.get_stories_after_date(date_handler.today)
	active_stories = mongo_handler.get_active_stories(date_handler.today)
	return render_template('admin.html', tomorrows_stories=upcoming_stories, todays_stories=active_stories, todays_date=today, tomorrows_date=tomorrow)

class Story:

	def __init__(self, headline, storyURL, imageURL, fromDate, toDate, _id, loadCount, clickCount):
		self.headline = headline
		self.storyURL = storyURL
		self.imageURL = imageURL
		self.fromDate = fromDate
		self.toDate = toDate
		self._id = _id
		if fromDate is not None:
			self.formatedFromDate = date_handler.format_date(fromDate)
		if toDate is not None:
			self.formatedToDate = date_handler.format_date(toDate)
		self.loadCount = loadCount
		self.clickCount = clickCount
		if loadCount == 0 or loadCount == None or clickCount == 0 or clickCount == None:
			self.clickthrough = 0
		else:
			self.clickthrough = loadCount / clickCount

	def get_story_object(self):
		story = {}
		story['headline'] = self.headline
		story['url'] = self.storyURL
		story['image'] = self.imageURL
		story['date'] = self.fromDate
		story['to_date'] = self.toDate
		story['load_count'] = self.loadCount
		story['click_count'] = self.clickCount
		story['clickthrough'] = self.clickthrough
		if not self._id:
			return story
		else:
			story['_id'] = self._id
			return story

class Date:

	def __init__(self):
		now = datetime.datetime.now()
		self.today = datetime.datetime(now.year, now.month, now.day)
		self.tomorrow = self.today + datetime.timedelta(days=1)

	def format_date(self, date):
		month = date.month
		if month < 10:
			month = "0" + str(month)
		day = date.day
		if day < 10:
			day = "0" + str(day)
		year = date.year
		return str(month) + "/" + str(day) + "/" + str(year)

	def date_to_datetime(self, date):
		month = int(date[:2])
		day = int(date[3:5])
		year = int(date[6:])
		return datetime.datetime(year, month, day)

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

class Analytics:

	def __init__(self):
		self.stories = mongo_handler.get_all_stories()
		self.loads = self.get_aggregate_load_count()
		self.clicks = self.get_aggregate_click_count()
		self.clickthrough = self.get_average_clickthrough_rate()

	def get_aggregate_load_count(self):
		load_count = 0
		for story in self.stories:
			if story.loadCount is not None:
				load_count += story.loadCount
		return load_count

	def get_aggregate_click_count(self):
		click_count = 0
		for story in self.stories:
			if story.clickCount is not None:
				click_count += story.clickCount
		return click_count;

	def get_average_clickthrough_rate(self):
		if self.loads == 0 or self.clicks == 0:
			return 0
		else:
			return self.loads / self.clicks


if __name__ == '__main__':
	mongo_handler = MongoHandler()
	date_handler = Date()
	analytics = Analytics()
	app.run()
	






