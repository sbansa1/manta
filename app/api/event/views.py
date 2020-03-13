from app.api.event import user_event_namespace
from flask_restplus import Resource, fields
from app.api.event.models import Event
import threading

from app.api.event.user_event import (
    event_notify_user,
    event_first_bill_pay,
    event_post_feedback,
)

event_model = user_event_namespace.model(
    "Event",
    {
        "userid": fields.Integer,
        "ts": fields.String,
        "latlong": fields.String,
        "noun": fields.String,
        "verb": fields.String,
        "timespent": fields.Integer,
        "properties": fields.String,
    },
)


class UserEvent(Resource):
    """User Event Trial"""

    @user_event_namespace.marshal_with(event_model, as_list=True)
    def get(self):
        """This is just for testing I would obviously get the URL and Consume the url and data"""
        # req = requests.get("")
        # data = req.json()
        # print(data)
        query = Event.query.all()
        event_first_bill_pay(data=query, event_type="bill payment")
        threading.Thread(target=event_notify_user, args=("Notify User", query,)).start()
        threading.Thread(target=event_post_feedback, args=("Post Feeback",)).start()
        return query


user_event_namespace.add_resource(UserEvent, "")
