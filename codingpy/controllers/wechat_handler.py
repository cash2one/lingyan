#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ..ext import wechat
from ..flask_wechat import filters
import os

# http://flask-wechat.readthedocs.io/zh_CN/latest/docs/getting_started.html
#微信回调URI为: /wechat/callbacks/<identity>/
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


