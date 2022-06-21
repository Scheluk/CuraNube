import sqlite3

import click
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

def init_db():
    db = get_db()

    with current_app.open_resource("curanube.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """"Clear the existing data and create new tables"""
    init_db()
    click.echo("Initialized the database")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def print_users():
    db = get_db()

    db.row_factory = sqlite3.Row

    result = db.execute("SELECT * FROM user").fetchall()

    list_accumulator = []
    for item in result:
        list_accumulator.append({k: item[k] for k in item.keys()})
    print(list_accumulator)

    return list_accumulator