import sqlite3
from flask import g
import os

# path to user database
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db")

#to connect to database
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db
# to close database
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()