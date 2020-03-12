from flask_restplus import Namespace

user_event_namespace = Namespace("user_namespace")

from app.api.event import views
