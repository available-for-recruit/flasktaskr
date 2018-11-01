import os

# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True # cross-site request forgery protection
SECRET_KEY = 'jabble' # should be very complex

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

# database URL
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE_PATH
