#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import logging

import requests
import sys

__python_version__ = sys.version[0]

logging.basicConfig(level=logging.INFO,
                    format='%(filename)s[%(lineno)d]%(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    stream=sys.stdout)

class WechatUtil(object):
    @staticmethod
    def get_access_token(app_id, app_secret):
        # request_url = """https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxf104b38e82ba98c6&secret=192074e2c481608a843e8e9b8145601f"""

        request_url = """https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%(app_id)s&secret=%(app_secret)s""" % dict(
            app_id=app_id, app_secret=app_secret)
        response = requests.get(request_url)
        """
200	OK
Connection: keep-alive
Date: Thu, 24 Sep 2015 14:56:11 GMT
Server: nginx/1.8.0
Content-Type: application/json; encoding=utf-8
Content-Length: 144
{
    "access_token": "_P1cVPM_-03c7yOoe_iJhQa_d5kR4Dcp_xjArp4-Oom_YWeb5FqYunP_7Xa4f8yuIX2JiG3soeiN3MjacbIQD1_cF8dFJz0FQdehK_CDeiU",
    "expires_in": 7200
}
        """
        body = response.json()
        access_token = body["access_token"]
        return access_token

    @staticmethod
    def add_single_news(access_token="",
                        title="",
                        thumb_media_id="",
                        author="",
                        digest="",
                        show_cover_pic=True,
                        content="",
                        content_source_url=""):
        """
        参数	是否必须	说明
        title	是	标题
        thumb_media_id	是	图文消息的封面图片素材id（必须是永久mediaID）
        author	是	作者
        digest	是	图文消息的摘要，仅有单图文消息才有摘要，多图文此处为空
        show_cover_pic	是	是否显示封面，0为false，即不显示，1为true，即显示
        content	是	图文消息的具体内容，支持HTML标签，必须少于2万字符，小于1M，且此处会去除JS
        content_source_url	是	图文消息的原文地址，即点击“阅读原文”后的URL
        """
        request_url = "https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=%s" % access_token
        data = {
            'articles': [{
                "title": title,
                "thumb_media_id": thumb_media_id,
                "author": author,
                "digest": digest,
                "show_cover_pic": show_cover_pic and 1 or 0,
                "content": content,
                "content_source_url": content_source_url,
            }],
        }
        logging.info(data)
        response = requests.post(request_url, data=json.dumps(data), headers={'content-type': 'application/json'})
        logging.info(response.json())

    @staticmethod
    def add_multi_news(access_token="", articles={}):
        request_url = "https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=%s" % access_token
        data = {
            'articles': articles,
        }
        logging.info(data)
        response = requests.post(request_url, data=json.dumps(data, ensure_ascii=False),
                                 headers={'content-type': 'application/json'})
        logging.info(response.json())

    @staticmethod
    def add_media(access_token, media_file):
        """
        参数	是否必须	说明
        access_token	是	调用接口凭证
        type	是	媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        media	是	form-data中媒体文件标识，有filename、filelength、content-type等信息

        :param access_token:
        :param media_file:
        :return:
        """
        request_url = 'https://api.weixin.qq.com/cgi-bin/material/add_material'
        data = {
            'access_token': access_token,
            'type': 'image',
        }
        files = {'media': ('upload_file.jpeg', open(media_file, 'rb'), 'image/jpeg')}
        response = requests.post(url=request_url, params=data, files=files)
        result_json = response.json()
        logging.info(result_json)
        media_id = result_json["media_id"]

        return media_id

    @staticmethod
    def get_material_list(access_token, material_type='image', offset=0, count=10):
        request_url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s" % access_token
        data = {
            "type": material_type,
            "offset": offset,
            "count": count,
        }
        logging.info(data)
        response = requests.post(request_url, data=json.dumps(data, ensure_ascii=False),
                                 headers={'content-type': 'application/json'})
        logging.info(response.content)
        res_json = json.loads(response.content)
        return res_json

    @staticmethod
    def create_menu(access_token, menu):
        request_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
        return WechatUtil.post_json(request_url, menu)

    @staticmethod
    def post_json(request_url, data):
        logging.info(data)
        data_json = json.dumps(data, ensure_ascii=False)
        if __python_version__ == "3":
            data_json = data_json.encode("utf-8")
        response = requests.post(request_url, data=data_json,
                                 headers={'content-type': 'application/json; charset=UTF-8',
                                          "Encoding": "UTF-8"})
        logging.info(response.content)
        res_json = response.json()
        return res_json

    @staticmethod
    def send_text_message(access_token, open_id, text):
        logging.info(text)
        request_url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % access_token
        data = {
            "touser": open_id,
            "msgtype": "text",
            "text": {
                "content": text
            }
        }
        res_json = WechatUtil.post_json(request_url, data)
        return res_json

    @staticmethod
    def send_news_message(access_token, open_id, articles):
        logging.info(articles)
        request_url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % access_token
        data = {
            "touser": open_id,
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        }
        res_json = WechatUtil.post_json(request_url, data)
        return res_json

    @staticmethod
    def get_jsapi_ticket(app_no):
        access_token = WechatUtil.get_access_token(app_no)

        request_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=" + access_token + "&type=jsapi"
        response = requests.get(request_url)
        body = response.json()
        ticket = body["ticket"]
        return ticket


if __name__ == "__main__":
    import os
    from local_config import env

    access_token = WechatUtil.get_access_token(env.get("WECHAT_APP_ID"), env.get("WECHAT_APP_SECRET"))
    menu = {
        "button": [
            {
                "name": "商品列表",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "所有商品",
                        "key": "VIEW_ALL_PRODUCT_LIST",
                    },
                    {
                        "type": "click",
                        "name": "特惠商品",
                        "key": "VIEW_DISCOUNT_PRODUCT_LIST",
                    },
                ]
            },
            {
                "name": "我的订单",
                "type": "view",
                "url": "http://yangyongli.com"
            },
            {
                "name": "任务管理",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "我的任务",
                        "url": "http://yangyongli.com"
                    },
                    {
                        "type": "view",
                        "name": "等待抢单",
                        "url": "http://yangyongli.com"
                    },
                    {
                        "name": "发送位置",
                        "type": "location_select",
                        "key": "SHARE_SENDER_LOCATION"
                    },
                ]
            }]
    }

    result = WechatUtil.create_menu(access_token, menu)
    print(result)
