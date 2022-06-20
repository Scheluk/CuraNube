import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext

database = [
    {"username":"admin","email":"admin@gmail.com","id":1,"pw":"admin","verified":True},
    {"username":"temp1","email":"t1@gmail.com","id":2,"pw":"admin","verified":False},
    {"username":"temp2","email":"t2@gmail.com","id":4,"pw":"admin","verified":True}
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()