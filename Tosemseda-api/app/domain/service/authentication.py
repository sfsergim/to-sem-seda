# -*- coding: utf-8 -*-
# from check import check_user
from app.data_source import models


class AuthService(object):

    @classmethod
    def autenticate_user_with_email(cls, credentials):
        try:
            email = "elchapo@tosemseda.com.br"
            password = "123456"

            models.User.filter_avaliable_users(email, password)
            return True
        except Exception as ex:
            return False


class RegisterService(object):

    @classmethod
    def register_user(cls, credentials):
        try:
            email = "elchapo@tosemseda.com.br"
            password = "123456"

            models.User.create_from_json(email, password)
            return True
        except Exception as ex:
            return False