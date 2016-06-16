#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from ..ext import wechat
from ..flask_wechat import filters
from ..ext import db
from ..models import WechatTextMessage


# http://flask-wechat.readthedocs.io/zh_CN/latest/docs/getting_started.html
# 微信回调URI为: /wechat/callbacks/<identity>/
wechat_identity = os.environ.get("WECHAT_CALLBACK_IDENTITY", "")


@wechat.account
def get_config(id):
    return dict(
        appid=os.environ.get("WECHAT_APP_ID", ""),
        appsecret=os.environ.get("WECHAT_APP_SECRET", ""),
        token=os.environ.get("WECHAT_APP_TOKEN", "")
    ) if id == wechat_identity else dict()


@wechat.handler(wechat_identity, filters.event.subscribe)
def subscribe(message):
    return message.reply_text("Thank you for subscribe!")


@wechat.handler(wechat_identity)
def all(message):
    return message.reply_text("I'm confused...")


@wechat.handler(wechat_identity, filters.message.startswith("hello"))
def hello(message):
    return message.reply_text("world")


@wechat.handler(wechat_identity, filters.message.startswith("codingpy"))
def codingpy(message):
    article1 = dict(
        title="CodingPy网站初始化",
        description="下了它的代码,在本地跑一下",
        picurl="http://yangyongli.com/static/images/python-favico.ico",
        url="http://yangyongli.com/article/initial_site/"
    )

    article2 = dict(
        title="试试别的东西",
        description="下了它的代码,在本地跑一下",
        picurl="http://yangyongli.com/static/images/flask.png",
        url="http://yangyongli.com/article/initial_site/"
    )
    return message.reply_article([article1, article2])


def database_filter():
    def decorated_func(message):
        if message.content == "hi":
            return True
        return False
    return decorated_func

def database_find(message):
    # if message.content == "hi":
    #     return True
    try:
        text = message.content
        text_message = WechatTextMessage.query.filter(WechatTextMessage.request == text).first()
        if text_message:
            return True
    except Exception as e:
        pass

    return False

@wechat.handler(wechat_identity, database_find)
def database_handler(message):
    text = message.content
    try:
        text_message = WechatTextMessage.query.filter(WechatTextMessage.request == text).first()
        if text_message:
            return message.reply_text(text_message.response)
    except Exception as e:
        pass
    return message.reply_text("不知道怎么回应: " + text)

