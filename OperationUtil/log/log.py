#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author:piepis
@file:fileutil.py
@time:2017-12-19 9:32
@desc: 代码的log日志代码
'''

import logging
import os
import time
import sys
from OperationUtil.file.readyaml import ReadYaml
from OperationUtil.file.fileutil import FileUtil
from OperationUtil.file.ExceptionSendDingding import ExceptionSend
class Log:
    '''打印日志'''

    def __init__(self,config=None):

        if config is None:
            self.config = ReadYaml(FileUtil.getProjectObsPath() + '/OperationConfig/config.yaml').getValue()
        else:
            self.config = config
        self.logpath = os.path.join(FileUtil.getProjectObsPath(), 'log')  # log文件夹
        self.logpatherror = os.path.join(self.logpath, 'error')  # error 文件夹
        if self.config.get('log_path_info') and config.get('log_path_error'):
            if os.path.isdir(self.config.get('log_path_info')) and os.path.isdir(self.config.get('log_path_error')) :
                pass
        elif os.path.isdir(self.logpath) and os.path.isdir(self.logpatherror):
            self.config['log_path_info'] = self.logpath
            self.config['log_path_error'] = self.logpatherror
        elif os.path.isdir(self.logpath):
            self.config['log_path_info'] = self.logpath
            os.makedirs(self.logpatherror)
            self.config['log_path_error'] = self.logpatherror
        else:
            os.makedirs(self.logpatherror)
            self.config['log_path_info'] = self.logpath
            self.config['log_path_error'] = self.logpatherror

    def _print_console(self,level,message,log_path):
        try:
            self.logname = os.path.join(log_path, '{0}.log'.format(time.strftime("%Y-%m-%d")))
            # 创建一个logger
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            # 创建一个handler ,用于写入日志文件
            fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            # 创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            # 定义handler的输出格式
            formatter = logging.Formatter('%(asctime)s -  %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            # 给logger添加handler
            logger.addHandler(fh)
            logger.addHandler(ch)
            # 记录一条记录
            if level == 'info':
                logger.info(message)
            elif level == 'debug':
                logger.debug(message)
            elif level == 'warning':
                logger.warning(message)
            elif level == 'error':
                logger.error(message)
            elif level == 'exception':
                logger.exception(u'Exception Logged')
            logger.removeHandler(ch)
            logger.removeHandler(fh)
            # 关闭打开的文件
            fh.close()
        except Exception as e:
            print(e)

    def info(self,message):
        invokefileName = sys._getframe().f_back.f_code.co_filename # 获取调用脚本
        invokefuncName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
        invokdelineNumber = sys._getframe().f_back.f_lineno  # 获取行号
        message = invokefileName + ' - ' +  invokefuncName + '[' + str(invokdelineNumber)+ ']' + ' - '+ message
        log_path = self.config['log_path_info']
        self._print_console('info',message,log_path)

    def debug(self,message):
        invokefileName = sys._getframe().f_back.f_code.co_filename # 获取调用脚本
        invokefuncName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
        invokdelineNumber = sys._getframe().f_back.f_lineno  # 获取行号
        message = invokefileName + ' - ' +  invokefuncName + '[' + str(invokdelineNumber)+ ']' + ' - '+ message
        log_path = self.config['log_path_info']
        self._print_console('debug',message,log_path)

    def warning(self,message):
        invokefileName = sys._getframe().f_back.f_code.co_filename # 获取调用脚本
        invokefuncName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
        invokdelineNumber = sys._getframe().f_back.f_lineno  # 获取行号
        message = invokefileName + ' - ' +  invokefuncName + '[' + str(invokdelineNumber)+ ']' + ' - '+ message
        log_path = self.config['log_path_error']
        self._print_console('warning',message,log_path)

    def error(self,message):
        # invokefuncName = sys._getframe().f_code.co_name  # 获取执行函数名
        # invokdelineNumber = sys._getframe().f_lineno  # 获取行号
        invokefileName = sys._getframe().f_back.f_code.co_filename # 获取调用脚本
        invokefuncName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
        invokdelineNumber = sys._getframe().f_back.f_lineno  # 获取行号
        message = invokefileName + ' - ' +  invokefuncName + '[' + str(invokdelineNumber)+ ']' + ' - '+ message
        log_path = self.config['log_path_error'] #错误log日志路径
        Operationmobile = self.config['OperationMobile'] #错误log日志路径
        self._print_console('error',message,log_path)
        ExceptionSend().SendDingding(Operationmobile, message)
    def exception(self,message,whetherSent) :
        log_path = self.config['log_path_error'] #错误log日志路径
        Operationmobile = self.config['OperationMobile'] #错误log日志路径
        message = time.strftime("%Y-%m-%d %H:%M:%S ") +'\n' +message
        self._print_console('exception',message,log_path)
        if whetherSent :
            ExceptionSend().SendDingding(Operationmobile, message)
if __name__ == '__main__':
    config = {"log_path_info": "E:\git_lib\log",
    "log_path_error": "E:\git_lib\log\error"}
    if os.path.isdir(config['log_path_info']):
        print('111')


