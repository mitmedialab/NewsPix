import os, ConfigParser, random, requests, json, datetime
import flask.ext.login as flask_login
from flask.ext.cors import CORS, cross_origin
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask,render_template,request,redirect, flash
from pymongo import MongoClient
from mongohandlerstories import MongoHandlerStories
from mongohandlerorganizations import MongoHandlerOrganizations
from mongohandler_timestamps import MongoHandlerTimestamps
from date import Date
from analytics import Analytics
from story import Story
from organization import Organization
from event_timestamp import EventTimestamp
from PIL import Image
from StringIO import StringIO
from auth import check_auth,authenticate,requires_auth
from user import User

# constants
CONFIG_FILENAME = 'app.config'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(BASE_DIR, CONFIG_FILENAME))

app = Flask(__name__)
app.secret_key = '?76GC0uSEGJ3J8t02511ghkk60^j9s'
app.debug = True
app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {
	r"/random_story/*": {"origins": "*"},
	r"/get_next_story/*": {"origins": "*"},
	r"/get_previous_story/*": {"origins": "*"},
	r"/register_click/*": {"origins": "*"},
	r"/news_organizations/*": {"origins": "*"}
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

mongo_handler_installations = MongoHandlerTimestamps(
	config.get('db','host'), 
	config.get('db','port'), 
	config.get('db', 'db'), 
	config.get('db', 'collection_installations')
)

mongo_handler_clicks = MongoHandlerTimestamps(
	config.get('db','host'), 
	config.get('db','port'), 
	config.get('db', 'db'), 
	config.get('db', 'collection_clicks')
)

date_handler = Date()

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(username):
	if not mongo_handler_organizations.is_valid_organization(username):
		return
	user = User()
	user.id = username
	return user

@login_manager.request_loader
def request_loader(request):
	username = request.form.get('username', None)
	password = request.form.get('password', None)
	if not mongo_handler_organizations.is_valid_organization(username):
		return
	user = User()
	user.id = username
	user.is_authenticated = mongo_handler_organizations.is_authorized(username, password)
	return user

@login_manager.unauthorized_handler
def unauthorized_handler():
	return redirect('/login')

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

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get('username', None)
		password = request.form.get('password', None)
		if mongo_handler_organizations.is_authorized(username, password):
			user = User()
			user.id = username
			flask_login.login_user(user)
			return redirect('/admin')
		else:
			flash("Login failed!")

	return app.send_static_file('login.html')

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return redirect('/login')


@app.route('/oninstall')
def oninstall():
	return render_template('oninstall.html')

@app.route('/organizations', methods=['GET', 'POST'])
@requires_auth
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

@app.route('/news_organizations', methods=['GET'])
def all_news_organizations():
	all_news_organizations = mongo_handler_organizations.get_all_organizations()
	result = []
	for organization in all_news_organizations:
		result.append(organization.get_organization_object())
	
	return json.dumps(result, default=json_util.default)

@app.route('/admin', methods=['GET', 'POST'])
@flask_login.login_required
def admin():
	signed_in_organization = flask_login.current_user.id
	if request.method == 'POST':
		# get new story
		story = Story (
			signed_in_organization,
			request.form.get('headline', None),
			request.form.get('storyURL', None),
			request.form.get('imageURL', None),
			date_handler.date_to_datetime(request.form.get('date', None)),
			date_handler.date_to_datetime(request.form.get('to_date', None)),
			None,
			0,
			0,
			mongo_handler_stories.get_story_count(signed_in_organization))
		mongo_handler_stories.save_story(story)
	return render_admin_panel(signed_in_organization)

@app.route('/analytics', methods=['GET', 'POST'])
@flask_login.login_required
def analytics_page():
	signed_in_organization = flask_login.current_user.id
	installations = mongo_handler_installations.get_organization_events(signed_in_organization)
	clicks = mongo_handler_clicks.get_organization_events(signed_in_organization)
	analytics = Analytics(mongo_handler_stories, signed_in_organization, installations, clicks)
	all_stories = mongo_handler_stories.get_all_stories(signed_in_organization)
	print analytics.clickthrough
	return render_template('analytics.html', stories=all_stories, analytics=analytics)

@app.route('/analytics/events', methods=['GET'])
def events():
	signed_in_organization = flask_login.current_user.id
	installations = mongo_handler_installations.get_organization_events(signed_in_organization)
	clicks = mongo_handler_clicks.get_organization_events(signed_in_organization)
	analytics = Analytics(mongo_handler_stories, signed_in_organization, installations, clicks)
	return json.dumps({'installations': analytics.installation_events, 'clicks': analytics.click_events}, default=json_util.default)

@app.route('/random_story', methods=['GET', 'POST'])
def random_story_old():
	stories = mongo_handler_stories.get_active_stories(date_handler.today, "keene_sentinel")
	if not stories:
		return "no stories"
	else:
		random_index = random.randint(0, len(stories)-1)
		result = stories[random_index].get_story_object()
		mongo_handler_stories.register_load(result['_id'])
		return json.dumps(result, default=json_util.default)

@app.route('/random_story/<organizationID>', methods=['GET', 'POST'])
def random_story(organizationID):
	stories = mongo_handler_stories.get_active_stories(date_handler.today, organizationID)
	if not stories:
		return "no stories"
	else:
		random_index = random.randint(0, len(stories)-1)
		result = stories[random_index].get_story_object()
		mongo_handler_stories.register_load(result['_id'])
		return json.dumps(result, default=json_util.default)

@app.route('/get_previous_story/<storyID>', methods=['GET', 'POST'])
def get_previous_story_old(storyID):
	result = mongo_handler_stories.get_active_story(storyID, "keene_sentinel", False)
	handleNextOrPrevious(result)
	return json.dumps(result, default=json_util.default)

@app.route('/get_previous_story/<organizationID>/<storyID>', methods=['GET', 'POST'])
def get_previous_story(organizationID, storyID):	
	result = mongo_handler_stories.get_active_story(storyID, organizationID, False)
	handleNextOrPrevious(result)
	return json.dumps(result, default=json_util.default)

@app.route('/get_next_story/<storyID>', methods=['GET', 'POST'])
def get_next_story_old(storyID):
	result = mongo_handler_stories.get_active_story(storyID, "keene_sentinel", True)
	handleNextOrPrevious(result)
	return json.dumps(result, default=json_util.default)

@app.route('/get_next_story/<organizationID>/<storyID>', methods=['GET', 'POST'])
def get_next_story(organizationID, storyID):
	result = mongo_handler_stories.get_active_story(storyID, organizationID, True)
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
def register_click_old(storyID):
	mongo_handler_stories.register_click(storyID)
	click = EventTimestamp('keene_sentinel', date_handler.format_date_for_chart(date_handler.today))
	mongo_handler_clicks.register_event(click)
	return render_template('register_click.html')

@app.route('/register_click/<organizationID>/<storyID>', methods=['GET', 'POST'])
def register_click(organizationID, storyID):
	mongo_handler_stories.register_click(storyID)
	click = EventTimestamp(organizationID, date_handler.format_date_for_chart(date_handler.today))
	mongo_handler_clicks.register_event(click)
	return render_template('register_click.html')

@app.route('/register_install/<organizationID>', methods=['POST'])
def register_install(organizationID):
	installation = EventTimestamp(organizationID, date_handler.format_date_for_chart(date_handler.today))
	mongo_handler_installations.register_event(installation)

def render_admin_panel(signed_in_organization):
	organization_logo = mongo_handler_organizations.get_organization(signed_in_organization)['logo_url']
	today = date_handler.format_date(date_handler.today)
	tomorrow = date_handler.format_date(date_handler.tomorrow)
	upcoming_stories = mongo_handler_stories.get_stories_after_date(date_handler.today, signed_in_organization)
	active_stories = mongo_handler_stories.get_active_stories(date_handler.today, signed_in_organization)

	return render_template('admin.html', tomorrows_stories=upcoming_stories, todays_stories=active_stories, todays_date=today, tomorrows_date=tomorrow, organization_logo=organization_logo)

def render_organizations_panel():
	organizations = mongo_handler_organizations.get_all_organizations()
	return render_template('organizations.html', organizations=organizations)

def isLandscape(url):
	#print url
	response = requests.get(url)
	img = Image.open(StringIO(response.content))
	width = img.size[0]
	height = img.size[1]
	return width > height

if __name__ == '__main__':
	app.debug = True
	app.run(host='127.0.0.1')
	print "Started Server"
	






