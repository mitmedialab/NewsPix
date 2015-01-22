import os
import ConfigParser
import requests
import json
import datetime
from bson.json_util import dumps
from flask import Flask,render_template,request
from pymongo import MongoClient 

app = Flask(__name__)
app.debug = True

# constants
CONFIG_FILENAME = 'app.config'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# read in app config
config = ConfigParser.ConfigParser()
config.read(os.path.join(BASE_DIR,CONFIG_FILENAME))

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
	date = dateHandler.get_todays_date()
	mongoHandler = MongoHandler()

	# stories that get shown in a list
	stories = mongoHandler.get_stories()
		
	story = Story()
	if request.method == 'POST':

		# get new story
		story.headline = request.form['headline']
		story.storyURL = request.form['storyURL']
		story.imageURL = request.form['imageURL']
		story.date = dateHandler.date_to_datetime(request.form['date'])
		mongoHandler.save_story(story)

		# update story list
		stories = mongoHandler.get_stories()

	return render_template('admin.html', noStories=len(stories) == 0, stories=stories, date=date)

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
		self.date = datetime.datetime.now()

	def get_todays_date(self):
		month = self.date.month
		if month < 10:
			month = "0" + str(month)
		day = self.date.day
		if day < 10:
			day = "0" + str(day)
		year = self.date.year
		return str(month) + "/" + str(day) + "/" + str(year)

	def date_to_datetime(self, date):
		month = int(date[:2])
		day = int(date[3:5])
		year = int(date[6:])
		return datetime.datetime(year, month, day, 0, 0)

class MongoHandler:

	def __init__(self):
		self.client = MongoClient("localhost", 27017)
		self.db = self.client.stories
		self.collection = self.db.collection

	def save_story(self, story):
		self.collection.save(story.get_story_object())

	def get_stories(self):
		stories = []
		cursor = self.collection.find()
		for story in cursor:
			stories.append(Story(story['headline'], story['url'], story['image'], story['date']))
		return stories

if __name__ == '__main__':
    app.run()





















