import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_path=os.getcwd(), instance_relative_config=True)
app.config.from_object('settings')
app.config.from_pyfile('settings.py', silent=True)
db = SQLAlchemy(app)

from marklog import posts
from marklog import views

try:
    db.create_all()
except Exception:
    # Already exists
    print("Tried to create database")
    pass
