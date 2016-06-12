#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from ..ext import wechat
from ..flask_wechat import filters


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
        Title="CodingPy网站初始化",
        Description="下了它的代码,在本地跑一下",
        PicUrl="http://yangyongli.com/static/images/python-favico.ico",
        Url="http://yangyongli.com/article/initial_site/"
    )

    article2 = dict(
        Title="试试别的东西",
        Description="下了它的代码,在本地跑一下",
        PicUrl="http://yangyongli.com/static/images/flask.png",
        Url="http://yangyongli.com/article/initial_site/"
    )
    return message.reply_article([article1, article2])
