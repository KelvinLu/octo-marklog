from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)
cache = SimpleCache()

from marklog import posts
from marklog import views

try:
    db.create_all()
except Exception:
    # Already exists
    print("Tried to create database")
    pass