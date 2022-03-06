from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
import os

db = SQLAlchemy()


def init_app(app: Flask):
    load_dotenv()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")

    db.init_app(app)
    app.db = db
