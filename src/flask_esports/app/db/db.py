import os
import sqlite3

from dotenv import load_dotenv
from flask import g, has_app_context, current_app

load_dotenv()
db_handle: sqlite3.Connection | None = None


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    if has_app_context():
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(
                current_app.config.get("SQL_DATABASE_URI", "sqlite:///app.db")
            )
            regenerate_db()
            db.row_factory = dict_factory
        return db
    else:
        from flask_esports.config import Config

        global db_handle
        if db_handle is None:
            db_handle = sqlite3.connect(Config.SQL_DATABASE_URI)
            db_handle.row_factory = dict_factory
        return db_handle


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def update_db(query, args=()):
    cur = get_db().execute(query, args)
    get_db().commit()
    cur.close()


def regenerate_db():
    with open(
        os.path.join(
            current_app.config.get("MODULE_BASE_DIR", ""), "app", "db", "schema.sql"
        ),
        "r",
    ) as f:
        schema = f.read()
    get_db().executescript(schema)
