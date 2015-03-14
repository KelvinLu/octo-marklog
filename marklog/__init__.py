from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

from marklog import posts
from marklog import views

try:
    db.create_all()
except Exception:
    # Already exists
    print("Tried to create database")
    pass