from flask import Flask
import os
from app.extensions import db, client
from app.api import api
import logging
from logging.handlers import RotatingFileHandler


def create_app(script_info=None):
    """Creates the flask app"""

    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)
    extensions(app)
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    )
    handler = RotatingFileHandler("logs.log", maxBytes=100000, backupCount=5)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    return app


def extensions(app):
    """"""
    db.init_app(app)
    api.init_app(app)
