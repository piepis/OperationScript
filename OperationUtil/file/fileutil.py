#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author:piepis
@file:fileutil.py
@time:2017-12-199:32
@desc: 返回代码的绝对路径
'''

import os
class FileUtil(object):

    @classmethod
    def getProjectObsPath(self):
        projectObsPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return projectObsPath

if __name__ == '__main__':
    print(FileUtil.getProjectObsPath())