# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps
import re
import unicodedata
from copy import copy
from flask import request, g, Response
from flask_restful import Resource
from app import config as config_module
from app.domain.service.authentication import AuthService, RegisterService

config = config_module.get_config()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = getattr(g, 'authenticated', False)
        if not authenticated:
            return Response('{"result": "Not Authorized"}', 401, content_type='application/json')
        return f(*args, **kwargs)

    return decorated_function


def not_allowed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return Response('{"result": "Method not allowed"}', 405, content_type='application/json')
    return decorated_function


def slugify(value):
    value = unicode(value, 'utf-8')
    slug = unicodedata.normalize('NFKD', value)
    slug = slug.replace(' ', '-')
    slug = slug.encode('ascii', 'ignore')
    return slug


def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(name):
    result = []
    for index, part in enumerate(name.split('_')):
        if index == 0:
            result.append(part.lower())
        else:
            result.append(part.capitalize())
    return ''.join(result)


class ResourceBase(Resource):
    http_methods_allowed = ['GET', 'POST', 'PUT', 'DELETE']
    entity_class = None
    me_profile = None

    def __init__(self):
        if self.logged_user is None:
            return
        self.me_profile = "EFETUAR O LOGIN E RETORNAR REU OU FALSE "
        try:
            self.me = self._create_me()
        except Exception as ex:
            self.me = None

    def _create_me(self):
        return self.entity_class.create_with_logged(self.logged_user, self.cookies)

    @property
    def logged_user(self):
        return getattr(g, 'user', None)

    @staticmethod
    def camel_to_snake(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def transform_key(self, data, method):
        if isinstance(data, dict):
            return {method(key): self.transform_key(value, method) for key, value in data.items()}
        if isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, dict):
                    data[index] = {method(key): self.transform_key(value, method) for key, value in item.items()}
        return data

    @property
    def payload(self):
        payload = {}
        if request.json:
            payload.update(self.transform_key(request.json, self.camel_to_snake))
        if request.form:
            payload.update(self.transform_key(request.form, self.camel_to_snake))
        if request.args:
            payload.update(self.transform_key(request.args, self.camel_to_snake))
        return payload

    @property
    def payload_batch(self):
        payload = {}
        payload_list = []
        if request.method != 'GET' and request.json:
            if isinstance(request.json, list):
                for item in request.json:
                    payload.update(self.transform_key(item, self.camel_to_snake))
                    copy_json = copy(payload)
                    payload_list.append(copy_json)
                return payload_list
            payload.update(self.transform_key(request.json, self.camel_to_snake))
        if request.form:
            payload.update(self.transform_key(request.form, self.camel_to_snake))
        if request.args:
            payload.update(self.transform_key(request.args, self.camel_to_snake))
        return payload

    @property
    def cookies(self):
        username = request.cookies.get('inceresUserName', None)
        token = request.cookies.get('inceresUserToken', 'null')
        profile_key = request.cookies.get('inceresProfileKey', 'null')
        return {'inceresUserName': username, 'inceresUserToken': token, 'inceresProfileKey': profile_key}

    def options(self, *args, **kwargs):
        return {'result': True}

    def response(self, data_dict):
        return {snake_to_camel(key): value for key, value in data_dict.iteritems()}

    def return_ok(self, **extra):
        result = {'result': 'OK'}
        if extra is not None:
            result.update(extra)
        return result

    def return_not_found(self, exception=None):
        return {'result': 'error', 'error': 'Not Found', 'exception': str(exception)}, 404

    def return_unexpected_error(self, exception=None):
        return {'result': 'error', 'error': 'General Error', 'exception': str(exception)}, 500

    def return_bad_request(self, exception=None):
        return {'result': 'error', 'error': 'Bad Request', 'exception': str(exception)}, 400


class UserLoginResource(ResourceBase):

    def get(self):
        try:
            authenticated = AuthService.autenticate_user_with_email(self.payload)
            if authenticated:
                g.email = self.payload.get('email')
                return self.return_ok()
            return self.return_not_found()
        except Exception as ex:
            return self.return_unexpected_error(ex)


class UserRegister(ResourceBase):

    # TODO: Mudar para method POST para receber os dados por payload
    def get(self):
        try:
            authenticated = RegisterService.register_user(self.payload)
            if authenticated:
                g.email = self.payload.get('email')
                return self.return_ok()
            return self.return_not_found()
        except Exception as ex:
            return self.return_unexpected_error(ex)
