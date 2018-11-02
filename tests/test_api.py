import os
import test_base

from project import app, db
from project.models import Task, User

class AllTestsAPI(test_base.AllTests):

  def test_invalid_resource_endpoint_returns_error(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.create_tasks_for_api()
    response = self.app.get('api/v1/tasks/209', follow_redirects=True)
    self.assertEquals(response.status_code, 404)
    self.assertEquals(response.mimetype, "application/json")
    self.assertIn(b"Element does not exist", response.data)

  def test_collection_endpoint_returns_correct_data(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.create_tasks_for_api()
    response = self.app.get('api/v1/tasks/', follow_redirects=True)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.mimetype, 'application/json')
    self.assertIn(b'Run around in circles', response.data)
    self.assertIn(b'Purchase Real Python', response.data)

  def test_resource_endpoint_returns_correct_data(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.create_tasks_for_api()
    response = self.app.get('api/v1/tasks/2', follow_redirects=True)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.mimetype, "application/json")
    self.assertIn(b"Purchase Real Python", response.data)
    self.assertNotIn(b"Run around in circles", response.data)

if __name__ == "__main__":
  test_base.unittest.main()
