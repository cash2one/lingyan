#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from hashlib import md5
from logging.handlers import RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(__file__))
datadir = 'data'


class Config:
    SITE_NAME = 'LingYan | 凌言'
    SECRET_KEY = os.urandom(32)
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # 是否启用博客模式
    # BLOG_MODE = True

    # html or markdown
    BODY_FORMAT = os.getenv('BODY_FORMAT')  # or 'html'

    # mail setup
    # 服务器名称: smtp-mail.outlook.com
    # 端口: 587
    # 加密方法: TLS
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[凌言]'
    MAIL_SENDER = 'yangyongli@outlook.com'

    APP_ADMIN = os.environ.get('CODINGPY_ADMIN')

    # flask-cache configuration
    CACHE_KEY = 'view/%s'  # ?
    CACHE_DEFAULT_TIMEOUT = 30
    # 使用uwsgi_cache效果更好
    # Used only for RedisCache, MemcachedCache and GAEMemcachedCache
    CACHE_KEY_PREFIX = '%s_' % md5(SECRET_KEY).hexdigest()[7:15]

    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_URL = 'redis://localhost:6379'

    # QiNiu Cloud Storage
    QINIU_AK = os.getenv('QINIU_AK') or ''
    QINIU_SK = os.getenv('QINIU_SK') or ''
    QINIU_BUCKET = os.getenv('QINIU_BUCKET') or ''
    QINIU_DOMAIN = os.getenv('QINIU_DOMAIN') or '%s.qiniudn.com' % QINIU_BUCKET

    @staticmethod
    def init_app(app):
        _handler = RotatingFileHandler(
            'app.log', maxBytes=10000, backupCount=1)
        _handler.setLevel(logging.WARNING)
        app.logger.addHandler(_handler)

        # TODO
        # mail_handler = Config.get_mailhandler()
        # app.logger.addHandler(mail_handler)


class DevelopmentConfig(Config):
    DEBUG = True
    WECHAT_DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') \
        or "mysql+pymysql://codingpy:codingpy2016@108.61.182.93:3306/codingpy" or \
        'sqlite:///%s' % os.path.join(basedir, 'data_dev_sqlite.db')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductionConfig(Config):
    # CACHE_DIR = os.path.join(basedir, datadir, 'cache')
    DEBUG = False
    WECHAT_DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        "mysql+pymysql://codingpy:codingpy2016@108.61.182.93:3306/codingpy"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig,
}
