#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author:piepis
@file:ExceptionSendDingding.py
@time:2018-01-1712:57
@desc: 将脚本出错的异常发送钉消息
'''
from OperationUtil.http.httpclient import HttpClient
class ExceptionSend(object):
    def __init__(self):
        self.url = "http://106.75.61.116:8080/oa/api/oa/dingtalk/sendDing"
        self.header_dict = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "Connection": "keep-alive",
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
    #钉钉接口
    def SendDingding(self,mobile_list,msg):
        body_dict = {"mobile": mobile_list, "company": "K", "msg": msg, "msg_type": "text",
                     "source": "monitorNodeJs"}
        HttpClient().post_json(self.url,body_dict,self.header_dict)

