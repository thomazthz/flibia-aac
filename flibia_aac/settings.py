# -*- coding: utf-8 -*-
"""Application configuration."""

import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = '=!=!=!= PLEASE,CHANGE THIS SECRET KEY, OK?... =!=!=!='
    TOKEN_SALT = '=!=!=!= TOKEN-SALT-KEY (do not forget to change it) =!=!=!='
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    THEME_NAME = 'classic'
    FULL_DATETIME_FORMAT = 'MMM DD YYYY, HH:mm:ss ZZZ'  # Oct 02 2018, 14:12:15 (format https://arrow.readthedocs.io/en/latest/#tokens)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIME_ZONE = 'UTC'

    MAIL_DEFAULT_SENDER = 'no-reply@flibia.com'

    ACTIVE_WIDGETS = (
        'flibia_aac.widgets.widgets.TopExperienceWidget',
        'flibia_aac.widgets.widgets.PlayersOnlineWidget',
    )


class ProductionConfig(Config):
    """Production configuration."""

    ENV = 'production'
    DB_NAME = 'flibia_prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI',
                                             'mysql://user:pass@localhost/{}'.format(DB_NAME))

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # MAIL_USERNAME=your@email.address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # MAIL_PASSWORD=your_password
    MAIL_PORT = 465
    MAIL_USE_SSL = True


class DevelopmentConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'flibia_dev'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flibia:password@localhost/{}'.format(DB_NAME)
    SQLALCHEMY_ECHO = True

    MAIL_PORT = 1025
    MAIL_SERVER = 'localhost'


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = False
    DB_NAME = 'flibia_test'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flibia:password@localhost/{}'.format(DB_NAME)
    WTF_CSRF_ENABLED = False


def get_config_object(env):
    return dict(
        development=DevelopmentConfig,
        production=ProductionConfig,
        testing=TestConfig
    ).get(env)