'''
#!/usr/bin/env python
# encoding: utf-8
@author: piepis
@contact: wangkai@keking.cn
@file: myThread.py
@time: 2018/3/11 21:12
@desc:线程Thread子类
'''
import threading
from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor(128)
from time import ctime
class MyThread(threading.Thread):
    def __init__(self,func,args,name = ''):
        threading.Thread.__init__(self)
        self.func = func#传进来函数
        self.args = args#传进来参数
        self.name = name#传进来函数名字
    def getResult(self):
        return self.res
    def run(self):
        #可以传递初始化函数参数的特殊方法
        print('starting {0} at:{1}'.format(self.name,ctime()))
        self.res = self.func(*self.args)
        print('{0} finished at: {1}'.format(self.name,ctime()))

    # for j, plate in enumerate(images):  # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中
    #     thread.append ( MyThread(_SimpleRecognizePlate,(j,plate),_SimpleRecognizePlate.__name__))#开启线程#返回 预测的图片，车牌，以及置信度
    # for i in range(j+1) :
    #     thread[i].start()
    # for i in range(j + 1):
    #     thread[i].join()
    #     for image_gray_alone ,str_alone,Confidence_alone in thread[i].getResult():
    #         image_gray.append(image_gray_alone )
    #         str.append(str_alone)
    #         Confidence.append(Confidence_alone)

