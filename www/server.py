import os, ConfigParser, random, requests, json, datetime
from flask.ext.cors import CORS, cross_origin
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask,render_template,request, redirect
from pymongo import MongoClient
from mongohandlerstories import MongoHandlerStories
from mongohandlerorganizations import MongoHandlerOrganizations
from date import Date
from analytics import Analytics
from story import Story
from organization import Organization
from PIL import Image
from StringIO import StringIO
from auth import check_auth,authenticate,requires_auth

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
	r"/get_next_story/*": {"origins": "*"},
	r"/get_previous_story/*": {"origins": "*"},
	r"/register_click/*": {"origins": "*"}
}

cors = CORS(app)
mongo_handler_stories = MongoHandlerStories(
	config.get('db','host'), 
	config.get('db','port'), 
	config.get('db', 'db'), 
	config.get('db', 'collection_stories')
)
mongo_handler_organizations = MongoHandlerOrganizations(
	config.get('db','host'), 
	config.get('db','port'), 
	config.get('db', 'db'), 
	config.get('db', 'collection_organizations')
)

date_handler = Date()


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

@app.route('/organizations', methods=['GET', 'POST'])
def admin_organizations():
	if request.method == 'POST':
		organization = Organization(
			request.form.get('name', None),
			request.form.get('loginUsername'),
			request.form.get('loginPassword', None),
			request.form.get('url', None),
			request.form.get('logoURL', None)
		)
		mongo_handler_organizations.save_organization(organization)
	return render_organizations_panel()

@app.route('/admin', methods=['GET', 'POST'])
@requires_auth
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
			0,
			mongo_handler_stories.get_story_count ())
		mongo_handler_stories.save_story(story)
		
	return render_admin_panel()

@app.route('/analytics', methods=['GET', 'POST'])
@requires_auth
def analytics_page():
	analytics = Analytics(mongo_handler_stories)
	all_stories = mongo_handler_stories.get_all_stories()
	print analytics.clickthrough
	return render_template('analytics.html', stories=all_stories, analytics=analytics)

@app.route('/random_story', methods=['GET', 'POST'])
def random_story():
	stories = mongo_handler_stories.get_active_stories(date_handler.today)
	if not stories:
		return "no stories"
	else:
		random_index = random.randint(0, len(stories)-1)
		result = stories[random_index].get_story_object()
		mongo_handler_stories.register_load(result['_id'])
		return json.dumps(result, default=json_util.default)

@app.route('/get_previous_story/<storyID>', methods=['GET', 'POST'])
def get_previous_story(storyID):
	result = mongo_handler_stories.get_active_story(storyID,False)
	handleNextOrPrevious(result)
	return json.dumps(result, default=json_util.default)

@app.route('/get_next_story/<storyID>', methods=['GET', 'POST'])
def get_next_story(storyID):
	result = mongo_handler_stories.get_active_story(storyID,True)
	handleNextOrPrevious(result)
	return json.dumps(result, default=json_util.default)

def handleNextOrPrevious(result):
	if result is None:
		return "no stories"
	else:
		result["isLandscape"] = 0
		mongo_handler_stories.register_load(result['_id'])
		imageURL = result.get('image')
		if imageURL is not None:
			result["isLandscape"] = int(isLandscape(imageURL))
	return result
		

@app.route('/delete_story/<storyID>', methods=['GET', 'POST'])
def delete_story(storyID):
	mongo_handler_stories.remove_story(storyID)
	return redirect("/admin")

@app.route('/delete_organization/<organizationID>', methods=['GET', 'POST'])
def delete_organization(organizationID):
	mongo_handler_organizations.remove_organization(organizationID)
	return redirect("/organizations")

@app.route('/register_click/<storyID>', methods=['GET', 'POST'])
def register_click(storyID):
	mongo_handler_stories.register_click(storyID)
	return render_template('register_click.html')

def render_admin_panel():
	today = date_handler.format_date(date_handler.today)
	tomorrow = date_handler.format_date(date_handler.tomorrow)
	upcoming_stories = mongo_handler_stories.get_stories_after_date(date_handler.today)
	active_stories = mongo_handler_stories.get_active_stories(date_handler.today)
	return render_template('admin.html', tomorrows_stories=upcoming_stories, todays_stories=active_stories, todays_date=today, tomorrows_date=tomorrow)

def render_organizations_panel():
	organizations = mongo_handler_organizations.get_all_organizations()
	return render_template('organizations.html', organizations=organizations)

def isLandscape(url):
	print url
	response = requests.get(url)
	img = Image.open(StringIO(response.content))
	width = img.size[0]
	height = img.size[1]
	return width > height

if __name__ == '__main__':
	app.debug = True
	app.run(host='127.0.0.1')
	print "Started Server"
	






