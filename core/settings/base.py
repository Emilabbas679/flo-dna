import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask_env import MetaFlaskEnv

project_name = "flocake-app"


class Config(metaclass=MetaFlaskEnv):
    """
    Base configuration class. Subclasses should include configurations for
    testing, development and production environments
    """

    DEBUG = True
    ASSETS_DEBUG = False  # not DEBUG
    CSRF_ENABLED = True

    SECRET_KEY = 'B85F4F52A619BA8E41F59188558A1'
    JWT_SECRET_KEY = "01234secret01234"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGGER_NAME = "%s_log" % project_name
    LOG_FILENAME = "/var/tmp/app.%s.log" % project_name

    LANGUAGES = ['en', 'az', 'ru']

    S3_REGION_NAME = 'fra1'
    S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'
    S3_ACCESS_KEY_ID = 'UKZLL2BAK4F7WCCXYIBD'
    S3_SECRET_ACCESS_KEY = 'jDqe3BIu9J7x+/i0XgRrcuw9+ZFEiWhTKo3J2Vsly1E'
