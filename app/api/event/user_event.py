from flask import current_app
import time

from app.api.event.models import Event
from app.extensions import db, client


def create_message(body=None):
    """Create Message"""
    message = client.messages.create(
        from_="+18478659454", body=body, to="+919826376555"
    )
    return message


"""
def create_binding():
    binding = client.notify.services(os.environ.get("SERVICE_INSTANCE_SID"))\
        .bindings.create(identity='00000001',
                        binding_type='sms',
                        address='+18478659454')
    print(binding.fetch())
    return (binding.fetch())
"""


def event_first_bill_pay(event_type, data):
    """Triggers the Notification when the user pays the bill for the first time"""

    data_parse = {}
    if event_type == "bill payment":
        for i in range(0, len(data)):
            user = Event.query.filter(Event.userid == data[i].userid).first()
            if data[i].noun == "bill" and data[i].verb == "pay" and user is None:
                "trigger push notification"
                current_app.logger.debug("Push Notification sent")
                data_parse["userid"] = data[i].userid
                data_parse["ts"] = data[i].ts
                data_parse["latlong"] = data[i].latlong
                data_parse["noun"] = data[i].noun
                data_parse["verb"] = data[i].verb
                data_parse["timespent"] = data[i].timespent
                data_parse["properties"] = data[i].properties

                event = Event(**data_parse)
                db.session.add(event)
                db.session.commit()
        message = create_message(body="The payment has been processed")
        status_notification(message)
        return {"Message": "Notification sent"}, 200
    return {"Message": "The event has been inserted"}, 201


def event_notify_user(event_type, data):

    """The end point will notify the user by SMS!Although in production I would probably like to use RabbitMQ
    for establishing an event store"""

    count = 0
    totalVal = 0
    eventStartTime = 0
    eventEndTime = 0
    totalTime = 0

    for data_val in data:
        totalVal = totalVal + int(data_val.properties["value"])
        count = count + 1
    totalTime += int((eventStartTime - eventEndTime) % 3600 // 60)
    if count >= 5 and totalVal >= 20000 and totalTime <= 5:
        """Notify user Through email or sms"""
        message = create_message(
            body="Alert! Are you Sure it was you! A total amount of {} payment "
            "has been initiated within 5 minutes".format(str(totalVal))
        )
        status_notification(message)
        return True
    return {"message": "The User has been notified"}, 200


def event_notify_operator(event_type, data):
    """Notify operator after 15 mins if the feedback has not been sent to the user"""
    if event_type == "Notify operator":
        """"""


def event_post_feedback(event_type):
    start_time = time.time()
    elapsed_time = 0
    if event_type == "Post Feeback" and status_notification:
        return {"Message": "Message has been succssefully delivered"}

    else:
        while elapsed_time != 15 and status_notification is not True:
            elapsed_time = time.time() - start_time
            elapsed_time = int(elapsed_time % 3600 // 60)
        create_message(body="Re-sending the message")
        return {"Message": "Operator has been re-notified"}


def status_notification(message=None):
    """Check if the notification has been received"""

    if message.Status.DELIVERED == "delivered":
        return True
    elif message.Status.FAILED == "failed":
        return False
    elif message.Status.UNDELIVERED == "undelivered":
        return False
    elif message.Status.QUEUED == "queued":
        return False
