from views import db
from models import Task
from datetime import date


def create_dummy_data():
    db.session.add(Task("Finish this tutorial", date(2018, 10, 25), 10, 1))
    db.session.add(Task("Finish Real Python", date(2018, 11, 25), 10, 1))

db.create_all()
# create_dummy_data()
db.session.commit()
