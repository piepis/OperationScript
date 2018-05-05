#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author:piepis
@file:fileutil.py
@time:2017-12-19 9:32
@desc: request 请求类型重构
'''
import requests
import json
from OperationUtil.http.sslAdapter import Ssl3Adapter

class HttpClient:
    '''发送http请求'''

    def __init__(self, timeout=60):
        self.requests = requests
        self.timeout = timeout
        self.requests.session().mount('https://',Ssl3Adapter())

    def get(self, url, header_dict=None, param_dict=None):
        response = requests.get(url, headers=header_dict, params=param_dict, timeout=self.timeout, verify=False)
        return response

    def post_form(self, url, body_dict=None, header_dict=None, param_dict=None):
        response = requests.post(url, data=body_dict, headers=header_dict, params=param_dict, timeout=self.timeout, verify=False)
        return response

    def post_json(self, url, body_dict=None, header_dict=None, param_dict=None):
        header_dict['content-type'] = 'application/json'
        response = requests.post(url, data=json.dumps(body_dict), headers=header_dict, params=param_dict, timeout=self.timeout, verify=False)
        return response

    def post_multipart(self, url, files=None, header_dict=None):
        response = requests.post(url, files=files, headers=header_dict, verify=False)
        return response

    def post_multipart_file(self, url, file_path, header_dict=None):
        files = {'file': (open(file_path, 'rb'))}
        response = requests.post(url, files=files, headers=header_dict, verify=False)
        return response

if __name__ == '__main__':

    URL = "http://106.75.61.116:8080/oa/api/oa/dingtalk/sendDing"
    body_dict = {"mobile":["15855126862"],"company":"K","msg":"运维管理系统异常测试","msg_type":"text","source":"monitorNodeJs"}
    header_dict = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "accept-encoding": "gzip, deflate",
        "Connection": "keep-alive",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    #钉钉接口测试
    response = HttpClient().post_json(URL,body_dict,header_dict)

    print(response.text)