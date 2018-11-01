import os
import test_base

from project import app, db
from project.models import Task, User

class AllTestsMain(test_base.AllTests):
  def test_404_error(self):
    response = self.app.get("/this-route-does-not-exist/")
    self.assertEquals(response.status_code, 404)
    self.assertIn(b"Sorry. There's nothing here.", response.data)

  def test_500_error(self):
    # Proper way to register, but we are testing direct db error
    #self.register("Jeremy", "jeremy@realpython.com", "django", "django")
    bad_user = User(
                    name = "Jeremy",
                    email = "jeremy@realpython.com",
                    password = "django"
                    )
    db.session.add(bad_user)
    db.session.commit()
    self.assertRaises(ValueError, self.login, "Jeremy", "django")
    try:
      response = self.login("Jeremy", "django")
      self.assertEquals(response.status_code, 500)
    except ValueError:
      pass

if __name__ == "__main__":
  test_base.unittest.main()
