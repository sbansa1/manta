import time
import os
from flask import current_app
from app.api.event.models import Event
from app.extensions import db, client
from twilio.rest import TwilioException
from collections import deque


def logger(msg):
    from app import create_app

    app = create_app()
    with app.app_context():
        app.logger.debug(msg)


def create_message(body=None):
    """Create Message"""
    try:
        message = client.messages.create(
            from_=(os.environ.get("SENDER_PHONE_NUMBER")),
            body=body,
            to=(os.environ.get("RECEIVER_PHONE_NUMBER")),
        )
    except TwilioException.with_traceback() as e:
        print(e)
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
    event = []
    if event_type == "bill payment":

        for i in range(0, len(data)):
            user = Event.query.filter(Event.userid == data[i].userid).first()
            if data[i].noun == "bill" and data[i].verb == "pay" and user is None:
                "trigger push notification"
                logger("Push Notification sent")
                message = create_message(body="The payment has been processed")
                status_notification(message)
                logger("Push Notification sent")
    event = Event(**parse_data(data))
    event.save()
    return {"Message": "The event has been inserted"}, 201


def parse_data(data):
    """trigger insert event"""
    data_parse = {}
    for i in range(len(data)):
        data_parse["userid"] = data[i].userid
        data_parse["ts"] = data[i].ts
        data_parse["latlong"] = data[i].latlong
        data_parse["noun"] = data[i].noun
        data_parse["verb"] = data[i].verb
        data_parse["timespent"] = data[i].timespent
        data_parse["properties"] = data[i].properties
        return data_parse


def event_notify_user(event_type, data):

    """The end point will notify the user by SMS!Although in production I would probably like to use RabbitMQ
    for establishing an event store"""

    count = 0
    totalVal = 0
    eventStartTime = 0
    eventEndTime = 0
    totalTime = 0

    for data_val in data:
        if data_val.verb == "pay":
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
        logger("The User has been notified")

        return True
    return {"message": "The User has been notified"}, 200


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
        # current_app.logger.warning("The operator has been informed")
        return {"Message": "Operator has been re-notified"}


def status_notification(message=None):
    """Check if the notification has been received"""
    try:
        if message.Status.DELIVERED == "delivered":
            return True
        elif message.Status.FAILED == "failed":
            return False
        elif message.Status.UNDELIVERED == "undelivered":
            return False
        elif message.Status.QUEUED == "queued":
            return False
    except TwilioException as e:
        print(e.with_traceback())
