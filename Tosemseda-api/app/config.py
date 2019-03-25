#  -*- coding: utf-8 -*-
"""
Config File for enviroment variables
"""
from __future__ import unicode_literals
import os
from importlib import import_module


class Config(object):
    """
    Base class for all config variables
    """
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    AMBIENTE = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        if self.AMBIENTE is None:
            raise TypeError('You should use one of the specialized config class')
        self.SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
        self.SMTP_SERVER = os.environ['SMTP_SERVER']
        self.APP_URL = os.environ['APP_URL']


class ProductionConfig(Config):
    """
    Production Config... this is the real thing
    """
    AMBIENTE = 'production'


class StagingConfig(Config):
    """
    Staging Config is for... staging things
    """
    AMBIENTE = 'staging'
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development Config... this is your home developer!
    """
    AMBIENTE = 'development'
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_RECORD_QUERIES = True


class TestingConfig(DevelopmentConfig):
    """
    Test Config... You should be testing right now instead reading docs!!!
    """
    AMBIENTE = 'test'
    TESTING = True
    KEY_ON_TEST = 'KEY ON TEST'


class ConfigClassNotFound(Exception):
    """
    Raises when the APP_SETTINGS environment variable have a value which does not point to an uninstantiable class.
    """
    pass


def get_config():
    """
    Get the Config Class instance defined in APP_SETTINGS environment variable
    :return The config class instance
    :rtype: Config
    """
    config_imports = os.environ['APP_SETTINGS'].split('.')
    config_class_name = config_imports[-1]
    config_module = import_module('.'.join(config_imports[:-1]))
    config_class = getattr(config_module, config_class_name, None)
    if not config_class:
        raise ConfigClassNotFound('Unable to find a config class in {}'.format(os.environ['APP_SETTINGS']))
    return config_class()