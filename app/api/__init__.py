from flask_restplus import Api
from app.api.event import user_event_namespace

api = Api(version=1.0, title="Events API", doc="/")

api.add_namespace(user_event_namespace, path="/check")
