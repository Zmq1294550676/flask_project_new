#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KET') or 'hard to guess thing'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    MONGODB_SETTINGS = {
        'db': 'weighting',
        'host': '127.0.0.1',
        'port': 27017,
        'username': 'siemens',
        'password': 'siemens',
        'connect': False
    }

    ### APNS推送服务的配置项
    # APNS_CERTIFICATE = '/var/www/weightingsystem/apns/apns_pro_nokey.pem'
    # APNS_ENABLED = True
    # APNS_SANDBOX = False    
    # APNS_DEFAULT_ERROR_TIMEOUT = 10
    # APNS_DEFAULT_EXPIRATION_OFFSET = 2592000
    
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
