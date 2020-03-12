from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client
import os


db = SQLAlchemy()
client = Client(os.environ.get("ACCOUNT_SID"), os.environ.get("AUTH_TOKEN"))
