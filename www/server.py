import os, ConfigParser, random, requests, json, datetime
from flask.ext.cors import CORS, cross_origin
from bson import json_util
from bson.json_util import dumps
from flask import Flask,render_template,request
from pymongo import MongoClient 

app = Flask(__name__)
app.debug = True
app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/random_story/*": {"origins": "*"}}

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	
	dateHandler = Date()
	today = dateHandler.format_date(dateHandler.today)
	tomorrow = dateHandler.format_date(dateHandler.tomorrow)
	mongoHandler = MongoHandler()

	# stories that get shown in the lists
	tomorrows_stories = mongoHandler.get_stories(dateHandler.tomorrow)
	todays_stories = mongoHandler.get_stories(dateHandler.today)
		
	story = Story()
	if request.method == 'POST':
		# get new story
		story.headline = request.form.get('headline', None)
		story.storyURL = request.form.get('storyURL', None)
		story.imageURL = request.form.get('imageURL', None)

		story.date = dateHandler.date_to_datetime(request.form.get('date', None))
		

		mongoHandler.save_story(story)
		
		# update story lists
		tomorrows_stories = mongoHandler.get_stories(dateHandler.tomorrow)
		todays_stories = mongoHandler.get_stories(dateHandler.today)
		

	return render_template('admin.html', tomorrows_stories=tomorrows_stories, todays_stories=todays_stories, todays_date=today, tomorrows_date=tomorrow)

@app.route('/random_story', methods=['GET', 'POST'])
def random_story():
	stories = MongoHandler().get_stories(Date().today)
	if len(stories) >  0:
		random_index = random.randint(0, len(stories)-1)
		result = stories[random_index].get_story_object()
	else:
		result = "no stories"

	print "HEAAAY"
	return json.dumps(result, default=json_util.default)

class Story:

	def __init__(self, headline="", storyURL="", imageURL="", date=None):
		self.headline = headline
		self.storyURL = storyURL
		self.imageURL = imageURL
		self.date = date

	def get_story_object(self):
		return {
			'headline': self.headline,
			'url': self.storyURL,
			'image': self.imageURL,
			'date': self.date
		}

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
		print "SAVE STORY"
		self.collection.save(story.get_story_object())

	def get_stories(self, date):
		stories = []
		cursor = self.collection.find({"date": date})
		for story in cursor:
			stories.append(Story(story['headline'], story['url'], story['image'], story['date']))
		return stories

if __name__ == '__main__':
    app.run()






