import os, ConfigParser, random, requests, json, datetime
from flask.ext.cors import CORS, cross_origin
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask,render_template,request
from pymongo import MongoClient
from mongohandler import MongoHandler
from date import Date
from analytics import Analytics
from story import Story
from PIL import Image
from StringIO import StringIO

# constants
CONFIG_FILENAME = 'app.config'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(BASE_DIR, CONFIG_FILENAME))

app = Flask(__name__)
app.debug = True
app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {
	r"/random_story/*": {"origins": "*"},
	r"/get_story/*": {"origins": "*"},
	r"/register_click/*": {"origins": "*"}
}

cors = CORS(app)
mongo_handler = MongoHandler(
	config.get('db','host'), 
	config.get('db','port'), 
	config.get('db', 'db'), 
	config.get('db', 'collection'))
date_handler = Date()
analytics = Analytics(mongo_handler)

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
def analytics_page():
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
		result["isLandscape"] = 0
		mongo_handler.register_load(result['_id'])
		imageURL = result.get('image')
		if imageURL is not None:
			result["isLandscape"] = int(isLandscape(imageURL))
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

def isLandscape(url):
	response = requests.get(url)
	print url
	img = Image.open(StringIO(response.content))
	width = img.size[0]
	height = img.size[1]
	return width > height

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
	print "Started Server"
	






