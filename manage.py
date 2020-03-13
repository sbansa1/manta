from flask.cli import FlaskGroup
from app import create_app
from app.extensions import db
from app.api.event.models import Event
import json

app = create_app()

cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    """Seed the Database"""
    db.session.add(Event(noun='bill',userid=178765,ts="20170315 134850",latlong="19.07,72.87",verb="pay",
                         timespent=72,
                         properties={"bank": "hdfc", "merchantid": 234, "value": 10000, "mode": "netbank"}))
    db.session.add(Event( noun='bill', userid=178765, ts="20170315 134850", latlong="19.07,72.87", verb="pay",
                           timespent=72,
                           properties={"bank": "hdfc", "merchantid": 234, "value": 10000, "mode": "netbank"} ) )
    db.session.add(Event( noun='fdbk', userid=178765, ts="20170315 134850", latlong="19.07,72.87", verb="post",
                           timespent=0,
                           properties={"text": "the bank page took too long to load"}))
    db.session.commit()



if __name__=="__main__":
    cli()