import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'
