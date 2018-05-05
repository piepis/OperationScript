'''
#!/usr/bin/env python
# encoding: utf-8
@author: piepis
@contact: wangkai@keking.cn
@file: Logconfig.py
@time: 2018/3/17 16:05
@desc:全局性log配置文件
'''
from OperationUtil.log.log import Log
from OperationUtil.file.readyaml import ReadYaml
from OperationUtil.file.fileutil import FileUtil

#--------------人脸识别 和 车牌号识别的 log配置文件
FacePlateconfig = ReadYaml(FileUtil.getProjectObsPath() + '/OperationConfig/FacePlateRecognitionMain.yaml').getValue()
FacePlateloging = Log(FacePlateconfig)  # 配置log文件