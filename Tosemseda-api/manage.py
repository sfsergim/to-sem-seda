#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import sys

from app.data_source import initialize
manager = Manager(initialize.web_app)


def register_migrate(manager):
    from app.data_source.models import *
    migrate = Migrate(initialize.web_app, db)
    manager.add_command('db', MigrateCommand)
    return migrate


if __name__ == '__main__':
    if 'db' in sys.argv:
        migrate = register_migrate(manager)
    manager.run()
