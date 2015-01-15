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

@app.route('/hello', methods=['GET', 'POST'])
def hello():
	name = "Forrest"
	if request.method == 'POST':
		name = request.form['enterName']
	return render_template('hello.html', name=name)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	
	date = Date().get_date()
	jsonHandler = JSONHandler()

	# stories that get shown in a list
	stories = jsonHandler.get_stories(date)
	noStories = len(stories) == 0
	
	# adding a new story
	story = Story()
	if request.method == 'POST':
		story.headline = request.form['headline']
		story.storyURL = request.form['storyURL']
		story.imageURL = request.form['imageURL']
		story.date = request.form['date']
		jsonHandler.add_story(story)

		# update story list
		stories = jsonHandler.get_stories(date)
		noStories = len(stories) == 0

	return render_template('admin.html', noStories=noStories, stories=stories, date=date)

class Story:

	def __init__(self, headline="", storyURL="", imageURL=""):
		self.headline = headline
		self.storyURL = storyURL
		self.imageURL = imageURL
		self.date = ""

	def format_for_json(self):
		d = {}
		d['headline'] = self.headline
		d['url'] = self.storyURL
		d['image'] = self.imageURL
		return d;

class JSONHandler:

	def __init__(self):
		self.stories_file = open('stories.json', 'r')
		self.stories = json.load(self.stories_file)

	def add_story(self, story):
		date = self.get_date(story.date)
		if date is None:
			date = self.add_date(story)
		date['stories'].append(story.format_for_json())
		self.write_new_data()

	def get_date(self, story_date):
		for date in self.stories['dates']:
			if date['date'] == story_date:
				return date
		return None

	def add_date(self, story):
		new_date = {}
		new_date['date'] = story.date
		new_date['stories'] = []
		self.stories['dates'].append(new_date)
		return self.get_date(story.date)

	def write_new_data(self):
		self.stories_file.close()
		with(open('stories.json', 'w')) as f:
			json.dump(self.stories, f, ensure_ascii=False, indent=4)

	def get_date_index(self, date):
		dates = self.stories['dates']
		for i in range(len(dates)):
			if (dates[i]['date'] == date):
				return i
		return None

	def get_stories(self, date):
		stories = []
		index = self.get_date_index(date)
		if index is None:
			return stories
		for story in self.stories['dates'][index]['stories']:
			stories.append(Story(story['headline'], story['url'], story['image']))
		return stories

class Date:

	def __init__(self):
		self.date = datetime.datetime.now()

	def get_date(self):
		month = self.date.month
		if month < 10:
			month = "0" + str(month)
		day = self.date.day
		if day < 10:
			day = "0" + str(day)
		year = self.date.year
		return str(month) + "/" + str(day) + "/" + str(year)

if __name__ == '__main__':
    app.run()





















