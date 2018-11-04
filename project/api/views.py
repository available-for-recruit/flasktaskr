# project/api/views.py

import datetime
from functools import wraps
from flask import flash, redirect, jsonify, session, url_for, Blueprint, make_response, g
from flask_restful import reqparse, Resource, Api, fields, marshal
from flask_httpauth import HTTPBasicAuth

from project import db, bcrypt
from project.models import Task, User

################
#### config ####
################

api_blueprint = Blueprint('api', __name__)


##########################
#### helper functions ####
##########################

task_fields = {
  'name': fields.String,
  'due_date': fields.String,
  'priority': fields.Integer,
  'status': fields.Integer,
  'user_id': fields.String,
  'uri': fields.Url('tasks')
}

auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
  if not (username and password):
    return False
  user = User.query.filter_by(name=username).first()
  if user is not None and bcrypt.check_password_hash(user.password, password):
    g.user = user
    return True

################
#### routes ####
################

# List tasks
@api_blueprint.route('/api/v1/tasks/')
def api_tasks():
  results = db.session.query(Task).limit(10).offset(0).all()
  json_results = []
  for result in results:
    data = {
      'task_id': result.task_id,
      'task name': result.name,
      'due date': str(result.due_date),
      'priority': result.priority,
      'posted date': str(result.posted_date),
      'status': result.status,
      'user id': result.user_id
    }
    json_results.append(data)
  return jsonify(items=json_results)

@api_blueprint.route('/api/v1/tasks/<int:task_id>')
def task(task_id):
  result = db.session.query(Task).filter_by(task_id = task_id).first()
  if result:
    result = {
      'task_id': result.task_id,
      'task name': result.name,
      'due date': str(result.due_date),
      'priority': result.priority,
      'posted date': str(result.posted_date),
      'status': result.status,
      'user id': result.user_id
    }
    code = 200
  else:
    result = {"error": "Element does not exist"}
    code = 404
  return make_response(jsonify(result),code)

# flask_restful way of doing the api

#pyimagesearch@pyimagesearch:~$ curl --user crabble:crabblecrabble -i -H "Content-Type: application/json" localhost:5000/api/v1.0/tasks -X GET

# pyimagesearch@pyimagesearch:~$ curl --user crabble:crabblecrabble -i -H "Content-Type: application/json" localhost:5000/api/v1.0/tasks -X POST -d '{"name":"hello3", "due_date":"10/20/2018", "priority":5, "status":1}'

class api_tasks(Resource):
  def __init__(self):
    # api parser
    self.parser = reqparse.RequestParser()
    self.parser.add_argument('name', required = True, location= 'json')
    self.parser.add_argument('due_date', required = True, location= 'json')
    self.parser.add_argument('priority', required = True, location= 'json')
    super(api_tasks, self).__init__()

  @auth.login_required
  def get(self):
    results = db.session.query(Task).limit(10).offset(0).all()
    json_results = []
    for result in results:
      data = {
        'task_id': result.task_id,
        'task name': result.name,
        'due date': str(result.due_date),
        'priority': result.priority,
        'posted date': str(result.posted_date),
        'status': result.status,
        'user id': result.user_id
      }
      json_results.append(data)
    return jsonify(items=json_results)

  @auth.login_required
  def post(self):
      args = self.parser.parse_args()
      new_task = Task(
          args['name'],
          datetime.datetime.strptime(args['due_date'], "%m/%d/%Y" ),
          args['priority'],
          datetime.datetime.utcnow(),
          '1',
          g.user.id
      )
      db.session.add(new_task)
      db.session.commit()
      task = db.session.query(Task).filter_by(name = args['name']).first()
      return {'tasks': marshal(task, task_fields)}, 201

class api_single_task(Resource):
  def __init__(self):
    # api parser
    self.parser = reqparse.RequestParser()
    self.parser.add_argument('name', required = False, location= 'json')
    self.parser.add_argument('due_date', required = False, location= 'json')
    self.parser.add_argument('priority', required = False, location= 'json')
    super(api_single_task, self).__init__()

  @auth.login_required
  def get(self, id):
    result = db.session.query(Task).filter_by(task_id = id).first()
    if result:
      result = {
        'task_id': result.task_id,
        'task name': result.name,
        'due date': str(result.due_date),
        'priority': result.priority,
        'posted date': str(result.posted_date),
        'status': result.status,
        'user id': result.user_id
      }
      code = 200
    else:
      result = {"error": "Element does not exist"}
      code = 404
    return make_response(jsonify(result),code)

  @auth.login_required
  def put(self, id):
    task = db.session.query(Task).filter_by(task_id = id)
    if task[0].user_id == g.user.id or g.user.role == "admin":
      args = self.parser.parse_args()
      for k, v in args.items():
          if v is not None:
              task.update({k: v})
      db.session.commit()
      return {'tasks': marshal(task[0], task_fields)}
    else:
      result = {"error": "Not authorized to modify task"}
      code = 404
      return make_response(jsonify(result),code)

  @auth.login_required
  def delete(self, id):
    task = db.session.query(Task).filter_by(task_id = id)
    task.delete()
    db.session.commit()
    return {'tasks': {}}
