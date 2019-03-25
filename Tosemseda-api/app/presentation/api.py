# -*- coding: utf-8 -*-

"""
This module define all the api endpoints
"""
from flask_restful import Api


def create_api(app):
    """
    Used when creating a Flask App to register the REST API and its resources
    """
    from app.presentation import resources
    api = Api(app)

    api.add_resource(resources.UserLoginResource, '/api/user/login')
    api.add_resource(resources.UserRegister, '/api/user/register')

