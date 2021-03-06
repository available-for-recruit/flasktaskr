import os
import test_base

from project import app, db
from project.models import Task, User

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
    self.assertIn(b"The task is complete. Nice.", response.data)

  def test_users_can_delete_tasks(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks", follow_redirects = True)
    self.create_task()
    # delete first task
    response = self.app.get("delete/1/", follow_redirects = True)
    self.assertIn(b"The task was deleted.", response.data)

  def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks", follow_redirects = True)
    self.create_task()
    self.logout()
    self.register("Fletcher", "fletcher@realpython.com", "python101", "python101")
    self.login("Fletcher", "python101")
    self.app.get("tasks/")
    response = self.app.get("delete/1/", follow_redirects = True)
    self.assertNotIn(b"The task was deleted.", response.data)
    self.assertIn(b"You can only delete tasks that belong to you.", response.data)

  def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks/", follow_redirects = True)
    self.create_task()
    self.logout()
    self.register("Fletcher", "fletcher@realpython.com", "python101", "python101")
    self.login("Fletcher", "python101")
    self.app.get("tasks/", follow_redirects = True)
    # complete first task
    response = self.app.get("complete/1/", follow_redirects = True)
    self.assertNotIn(b"The task was marked as complete.", response.data)
    self.assertIn(b"You can only update tasks that belong to you.", response.data)

  def test_admin_users_can_complete_tasks_that_are_not_created_by_them(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks/", follow_redirects = True)
    self.create_task()
    self.logout()
    self.create_admin_user()
    self.login("Superman", "allpowerful")
    self.app.get("tasks/", follow_redirects = True)
    response = self.app.get("complete/1/", follow_redirects = True)
    self.assertNotIn(b"You can only update tasks that belong to you.", response.data)

  def test_admin_users_can_delete_tasks_that_are_not_created_by_them(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks/", follow_redirects = True)
    self.create_task()
    self.logout()
    self.create_admin_user()
    self.login("Superman", "allpowerful")
    self.app.get("tasks/", follow_redirects = True)
    response = self.app.get("delete/1/", follow_redirects = True)
    self.assertNotIn(b"You can only delete tasks that belong to you.", response.data)

  def test_template_displays_logged_in_user_name(self):
    self.register("Fletcher", "fletcher@realpython.com", "python101", "python101")
    self.login("Fletcher", "python101")
    response = self.app.get("tasks/", follow_redirects = True)
    self.assertIn(b"Fletcher", response.data)

  def test_users_cannot_see_task_modify_links_for_tasks_not_created_by_them(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks/", follow_redirects = True)
    self.create_task()
    self.logout()
    self.register("Fletcher", "fletcher@realpython.com", "python101", "python101")
    self.login("Fletcher", "python101")
    response = self.app.get("tasks/", follow_redirects = True)
    self.assertNotIn(b"Mark as complete", response.data)
    self.assertNotIn(b"Delete", response.data)

  def test_users_can_see_task_modify_links_for_tasks_created_by_them(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks/", follow_redirects = True)
    self.create_task()
    self.logout()
    self.register("Fletcher", "fletcher@realpython.com", "python101", "python101")
    self.login("Fletcher", "python101")
    self.app.get("tasks/", follow_redirects = True)
    response = self.create_task()
    self.assertNotIn(b"complete/1/", response.data)
    self.assertIn(b"complete/2/", response.data)

  def test_admin_users_can_see_task_modify_links_for_all_tasks(self):
    self.register("Michael", "michael@realpython.com", "python", "python")
    self.login("Michael", "python")
    self.app.get("tasks/", follow_redirects = True)
    self.create_task()
    self.logout()
    self.create_admin_user()
    self.login("Superman", "allpowerful")
    self.app.get("tasks/", follow_redirects = True)
    response = self.create_task()
    self.assertIn(b"complete/1/", response.data)
    self.assertIn(b"delete/1/", response.data)
    self.assertIn(b"complete/2/", response.data)
    self.assertIn(b"delete/2/", response.data)



if __name__ == "__main__":
  test_base.unittest.main()

