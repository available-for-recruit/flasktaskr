from project import db
from project.models import Task, User
from datetime import date


def create_dummy_data():
  db.session.add(User("admin", "ad@min.com", "admin", "admin"))
  db.session.add(Task("Finish this tutorial", date(2018, 10, 25), 10, date(2018, 9, 25), 1, 1))
  db.session.add(Task("Finish Real Python", date(2018, 11, 25), 10, date(2018, 10, 25), 1, 1))

db.create_all()
create_dummy_data()
db.session.commit()
