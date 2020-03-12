import os


class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SECRET_KEY = "my_precious"
    ACCOUNT_SID = os.environ.get("TWILIO_SID")
    AUTH_TOKEN = os.environ.get(("TWILIO_AUTH_TOKEN"))
    SERVICE_INSTANCE_SID = os.environ.get(("SERVICE_INSTANCE_SID"))


class DevelopmentConfig(BaseConfig):
    """Development Config"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestingConfig(BaseConfig):
    """Testing Config"""

    SQLALCHEMY_TESTING_URI = os.environ.get("DATABASE_TESTING_URL")
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production Config"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
