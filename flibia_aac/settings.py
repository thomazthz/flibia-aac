# -*- coding: utf-8 -*-
"""Application configuration."""

import os

class Config(object):
    """Base configuration."""

    SECRET_KEY = '=!=!=!= PLEASE,CHANGE THIS SECRET KEY, OK?... =!=!=!='
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    THEME_NAME = 'classic'
    FULL_DATETIME_FORMAT = '%b %d %Y, %X'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production configuration."""

    ENV = 'production'
    DB_NAME = 'flibia_prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI',
                                             'mysql://user:pass@localhost/{}'.format(DB_NAME))


class DevelopmentConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'flibia_dev'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flibia:password@localhost/{}'.format(DB_NAME)
    SQLALCHEMY_ECHO = True


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'


def get_config_object(env):
    return dict(
        development=DevelopmentConfig,
        production=ProductionConfig,
    ).get(env)