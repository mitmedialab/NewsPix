from flask import Flask, Response, redirect, session, render_template, json, jsonify, request, make_response, url_for
from pymongo import MongoClient

import ConfigParser
import json
import pymongo
from bson import json_util
from bson.objectid import ObjectId

# CONFIG_FILENAME = 'app.config'
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# LOG_DIR = os.path.join(BASE_DIR,'logs')

# config = ConfigParser.ConfigParser()
# config.read=('config.cfg')

app = Flask(__name__)

app.debug = True
# uri = "mongodb://"+ config.get('db','user')+ ":"+ config.get('db','pass')+"@" +config.get('db','host') + ":" + config.get('db','port')
db_client = MongoClient('localhost', 27017)
app.db = db_client['dbase']

@app.route('/')
def home_page():
    users = app.db.users.find({})
    if users is not None:	
	    return render_template('home.html',
	        users=users)

@app.route('/user/<username>')
def user_profile(username):
    users = app.db.users.find({'name': username})
    if users is not None:
	    return render_template('user.html',
	        users=users)


@app.route('/news')
def welcome():
	return render_template('news.html')

@app.route('/hello')
def hello():
	return render_template('hello.html')


@app.route("/log", methods=['GET', 'POST'])
def log():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			app.db.users.find({'name': request.form['username'], 'password': request.form['password'] })
			print "Successfully logged"
			return redirect(url_for('hello'))
		else:
			return redirect(url_for('log'))
	return render_template('log.html', error=error)

@app.route("/new", methods=['GET', 'POST'])
def new():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			app.db.users.insert({'name': request.form['username'], 'password': request.form['password'] })
			print "Successfully signed up"
			return redirect(url_for('hello'))
		else:
			return redirect(url_for('new'))
	return render_template('new.html', error=error)

if __name__ == '__main__':
	app.run()
	print "Started Server"



