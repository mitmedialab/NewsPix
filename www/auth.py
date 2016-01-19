from functools import wraps
from flask import request, Response
import os,ConfigParser
from mongohandlerorganizations import MongoHandlerOrganizations


CONFIG_FILENAME = 'app.config'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser.SafeConfigParser()
config.read(os.path.join(BASE_DIR, CONFIG_FILENAME))



def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """

    return (username == config.get('app', 'admin_username')) and (password == config.get('app', 'admin_password'))

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