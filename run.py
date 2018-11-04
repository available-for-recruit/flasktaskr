import os
from project import app
from flask_restful import Resource, Api
from project import app
from project.api.views import api_tasks, api_single_task

myapi = Api(app)
port = int(os.environ.get("PORT", 5000))
myapi.add_resource(api_tasks, '/api/v1.0/tasks', endpoint = 'tasks')
myapi.add_resource(api_single_task, '/api/v1.0/tasks/<int:id>')

app.run(host="0.0.0.0", port = port)
