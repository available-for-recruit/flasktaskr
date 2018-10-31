import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):

  # setup and teardown

  # executed prior to each test
  def setUp(self):
    app.config["TESTING"] = True
    # VERY IMPORTANT TO DISABLE!!!
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, TEST_DB)
    self.app = app.test_client()
    db.create_all()

  # executed after each test
  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def login(self, name, password):
    return self.app.post("/",
                         data = dict (
                                      name = name,
                                      password = password,
                                      ),
                         follow_redirects = True
                         )

  def logout(self):
    return self.app.get("logout/", follow_redirects=True)

  def register(self, name, email, password, confirm):
    return self.app.post(
                         "register/",
                         data = dict(
                                     name = name,
                                     email = email,
                                     password  = password,
                                     confirm = confirm
                                     ),
                         follow_redirects = True
                         )

  def create_task(self):
    return self.app.post("add/",
                         data=dict(
                                   name = "Go to the bank",
                                   due_date = "10/08/2018",
                                   priority = "1",
                                   posted_date = "10/08/2018",
                                   status = "1"
                                   ),
                         follow_redirects = True
                         )

  def create_bad_task(self):
    return self.app.post("add/",
                         data=dict(
                                   name = "Go to the bank",
                                   due_date = "",
                                   priority = "1",
                                   posted_date = "10/08/2018",
                                   status = "1"
                                   ),
                         follow_redirects = True
                         )

if __name__ == "__main__":
  unittest.main()
