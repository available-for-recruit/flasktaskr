import sqlite3
from _config import DATABASE_PATH

def create_db():
    with sqlite3.connect(DATABASE_PATH) as connection:
        c = connection.cursor()

        c.execute(
            """
            CREATE TABLE tasks(
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                due_date TEXT NOT NULL,
                priority INTEGER NOT NULL,
                status INTEGER NOT NULL
            )
            """
            )

def create_dummy_data():
    with sqlite3.connect(DATABASE_PATH) as connection:
        c = connection.cursor()
        dummy_data = [
            ("Finish this tutorial", "03/25/2015", 10, 1),
            ("Finish Real Python Course 2", "03/25/2015", 10, 1)
            ]

        c.executemany("INSERT INTO tasks (name, due_date, priority, status)"
                      "VALUES(?,?,?,?)",
                      dummy_data
                      )

create_db()
create_dummy_data()
