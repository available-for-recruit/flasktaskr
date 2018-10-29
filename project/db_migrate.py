from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as connection:
  c = connection.cursor()

  # temporarily change the target of the migrations (tasks)
  c.execute(
            """
            ALTER TABLE tasks RENAME TO old_tasks
            """
            )

  # recreate a new tasks table with the updated schema
  db.create_all()

  # retrieve data from the old_tasks table
  c.execute(
            """
            SELECT name, due_date, priority, status
            FROM old_tasks
            ORDER BY task_id ASC
            """)

  """
   save all the rows as a list of tuples and set the posted_date to now and user_id to 1
  """
  data = [(row[0], row[1], row[2], row[3], datetime.now(), 1) for row in c.fetchall()]

  c.executemany(
                 """
                 INSERT INTO tasks (name, due_date, priority, status, posted_date, user_id) VALUES (?, ?, ?, ?, ?, ?)
                 """ ,
                 data
                 )

  # delete old_tasks table
  c.execute("DROP TABLE old_tasks")


