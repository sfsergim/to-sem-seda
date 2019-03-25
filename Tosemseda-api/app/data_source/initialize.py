# -*- coding: utf-8 -*-
import os
import struct
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from app.data_source import database
from app import config as config_module
from app.presentation import api

config = config_module.get_config()
async_mode = None

web_app = Flask(__name__)
web_app.config.from_object(config)

database.AppRepository.db = SQLAlchemy(web_app)
api.create_api(web_app)


@web_app.route('/api')
def api_root():
    return Response('{"result": "Porra Weiss <3 <3"}', 200, content_type='application/json')


def run():
    """
    Run the flask app in a develpment enviroment
    """
    web_app.run(host='0.0.0.0', port=int(os.environ.get('PORTA', 10999)), debug=True)
