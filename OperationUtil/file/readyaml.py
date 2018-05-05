#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author:piepis
@file:readyaml.py
@time:2018-01-14 10:41
@desc: 读取yaml配置文件
'''

import yaml
import sys
class ReadYaml:
    """专门读取配置文件的，.yaml文件格式"""
    def __init__(self,filename):
        version = sys.version  # 获取版本
        if u'2.' in version[0:2]:
            self.stream = open(filename)
        else:
            self.stream = open(filename, encoding='utf-8')
    def getValue(self):
        dict = yaml.load(self.stream)
        self.stream.close()
        return dict