#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author:piepis
@file:ToolFuction.py
@time:2018-1-2310:51
@desc: 工具函数
'''
import re

tt = u"【 正  文 】近年来受到进口微机严重冲击的国产微机，１９９５年打了个翻身仗，总销售额达６１５亿元，销量首次突破百万台大关，达１１５万台，从而以微弱优势重新获得了我国微机市场的主要份额———５０·４％的市场占有率。这是由电子部计算机与微电子发展研究中心（ＣＣＩＤ）近日发布的。"
# dd = re.search(r'[\uFF10-\uFFFF．·％]*',tt)
def strQ2B(ustring):
	"""全角转半角"""
	rstring = ""
	for uchar in ustring:
		inside_code = ord(uchar)
		if inside_code == 12288:  # 全角空格直接转换
			inside_code = 32
		elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
			inside_code -= 65248

		rstring += unichr(inside_code)
	return rstring
cc =strQ2B(tt)

#日期转换
def Data(data):
    month = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "June": "06", "July": "07", "Aug": "08",
             "Sept": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    hh4=re.match(r'(.*)/(.*)/(.*):(.*:.*:.*)',data)
    h1 =hh4.group(1)
    h2 = hh4.group(2)
    h3 =hh4.group(3)
    h4 =hh4.group(4)
    h5 = month[h2]
    request_time = h3+'-'+h5+'-'+h1+' '+h4
    return request_time

def gettext(filePath):
    row_list = {}
    with open(filePath,'r') as file_to_read:
        lines = file_to_read.readlines() # 整行读取数据
    for line in lines:
        temp = line.split()
        if temp[1] =='-':
            row_list[temp[0]] =0
        else:
            row_list[temp[0]] =temp[1]
    return row_list