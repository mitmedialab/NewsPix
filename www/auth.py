from functools import wraps
from flask import request, Response
import os,ConfigParser
from mongohandlerorganizations import MongoHandlerOrganizations


CONFIG_FILENAME = 'organizations.config'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(BASE_DIR, CONFIG_FILENAME))

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    stored_password = config.get('organizations', username)
    if stored_password and (stored_password == password):
        config.set('signed_in', 'signed_in_organization', username)
        with open(os.path.join(BASE_DIR, CONFIG_FILENAME), 'w') as config_file:
            config.write(config_file)
        return True
    return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated