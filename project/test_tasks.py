import os
import test_base

from views import app, db
from models import User

class AllTestsTasks(test_base.AllTests):

  def test_logged_in_users_can_acces_tasks_page(self):
    self.register("Fletcher", "fletcher@realpython.com", "python101", "python101")
    self.login("Fletcher", "python101")
    response = self.app.get("tasks/")
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Add a new task:", response.data)
    self.logout()
    response = self.app.get("tasks/", follow_redirects = True)
    self.assertIn(b"You need to login first.", response.data)

  def test_users_can_add_tasks(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks/", follow_redirects = True)
    response = self.create_task()
    self.assertIn(
                  b"New entry was successfully posted. Thanks.",
                  response.data)

  def test_users_cannot_add_tasks_when_error(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks/", follow_redirects = True)
    response = self.create_bad_task()
    self.assertIn(b"This field is required.", response.data)

  def test_users_can_complete_tasks(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks", follow_redirects = True)
    self.create_task()
    # complete first task
    response = self.app.get("complete/1/", follow_redirects = True)
    self.assertIn(b"The task was marked as complete.", response.data)

  def test_users_can_delete_tasks(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks", follow_redirects = True)
    self.create_task()
    # delete first task
    response = self.app.get("delete/1/", follow_redirects = True)
    self.assertIn(b"The task was deleted.", response.data)

  def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks", follow_redirects = True)
    self.create_task()
    self.logout()
    self.register("Fletcher", "fletcher@realpython.com", "python101", "python101")
    self.login("Fletcher", "python101")
    self.app.get("tasks/")
    # complete first task
    response = self.app.get("complete/1/", follow_redirects = True)
    self.assertNotIn(b"The task was marked as complete.", response.data)


if __name__ == "__main__":
  test_base.unittest.main()

