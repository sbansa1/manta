from flask import Flask
import os
from app.extensions import db, client
from app.api import api


def create_app(script_info=None):
    """Creates the flask app"""

    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)
    extensions(app)

    return app


def extensions(app):
    """"""
    db.init_app(app)
    api.init_app(app)
