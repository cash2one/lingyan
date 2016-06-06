#!usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import xmlrpc.client as xmlrpc_client
except:
    import xmlrpclib as xmlrpc_client
from flask import current_app, url_for, flash
import requests


def notify_baidu(url):
    baidu_api = "http://data.zz.baidu.com/urls?"
    token = "site=www.codingpy.com&token=flJTo2ma4A4ijZkU"

    resp = requests.post(baidu_api + token, data=url)

    if resp.status_code == 200:
        return True
    else:
        flash('An error occured. ')
        return False


def baidu_ping(url):
    """
    :ref: http://zhanzhang.baidu.com/tools/ping

    发送给百度Ping服务的XML-RPC客户请求需要包含如下元素：
    RPC端点： http://ping.baidu.com/ping/RPC2
    调用方法名： weblogUpdates.extendedPing
    参数： (应按照如下所列的相同顺序传送)
    博客名称
    博客首页地址
    新发文章地址
    博客rss地址
    """

    result = 1
    rpc_server = xmlrpc_client.ServerProxy('http://ping.baidu.com/ping/RPC2')

    try:
        # 返回0表示提交成功
        current_app.logger.info('begin to ping baidu: <%s>' % url)
        result = rpc_server.weblogUpdates.extendedPing(
            current_app.config.get('SITE_NAME'),
            url_for('site.index', _external=True),
            url,
            url_for('site.feed', _external=True)
        )
    except:
        pass

    if result != 0:
        current_app.logger.warning('<%s> ping to baidu failed' % url)

    return result == 0
