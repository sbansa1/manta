from app.extensions import db
from sqlalchemy.dialects.postgresql import JSON


class Event(db.Model):

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userid = db.Column(db.Integer, nullable=False)
    ts = db.Column(db.String(128), nullable=False)
    latlong = db.Column(db.String(128))
    noun = db.Column(db.String(10), default="bill")
    verb = db.Column(db.String(10), default="pay")
    timespent = db.Column(db.Integer)
    properties = db.Column(JSON)

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
