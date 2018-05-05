#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author:piepis
@file:HtmlMouldOne.py
@time:2018-01-1919:59
@desc:  邮件发送html的第一个模板
'''

from xml.sax import saxutils
import datetime
from OperationUtil.file.readyaml import ReadYaml
from OperationUtil.file.fileutil import FileUtil
from OperationUtil.log.log import Log
import os.path


__version__ = u"0.0.0.1"
__author__ = u"piepis"

class HtmlMould(object) :
    generator = 'HTMLRunner %s' % __version__
    DEFAULT_TITLE = u'运维系统告警'
    DEFAULT_TESTER = u'运维小凯'
    DEFAULT_DESCRIPTION = u'22233'

    HTML_TMPL = u"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>%(title)s</title>
        <meta name="generator" content="%(generator)s"/>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
        <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
        <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
        %(stylesheet)s
    </head>
    <body >
    <script language="javascript" type="text/javascript">
    output_list = Array();

    /*level 调整增加只显示通过用例的分类 --Findyou
    0:Summary //all hiddenRow
    1:Failed  //pt hiddenRow, ft none
    2:Pass    //pt none, ft hiddenRow
    3:All     //pt none, ft none
    */
    function showCase(level) {
        trs = document.getElementsByTagName("tr");
        for (var i = 0; i < trs.length; i++) {
            tr = trs[i];
            id = tr.id;
            if (id.substr(0,2) == 'ft') {
                if (level == 2 || level == 0 ) {
                    tr.className = 'hiddenRow';
                }
                else {
                    tr.className = '';
                }
            }
            if (id.substr(0,2) == 'pt') {
                if (level < 2) {
                    tr.className = 'hiddenRow';
                }
                else {
                    tr.className = '';
                }
            }
        }

        //加入【详细】切换文字变化 --Findyou
        detail_class=document.getElementsByClassName('detail');
        //console.log(detail_class.length)
        if (level == 3) {
            for (var i = 0; i < detail_class.length; i++){
                detail_class[i].innerHTML="关闭明细"
            }
        }
        else{
                for (var i = 0; i < detail_class.length; i++){
                detail_class[i].innerHTML="展开明细"
            }
        }
    }

    function showClassDetail(cid, count) {
        var id_list = Array(count);
        var toHide = 1;
        for (var i = 0; i < count; i++) {
            //ID修改点为下划线 -Findyou
            tid0 = 't' + cid.substr(1) + '_' + (i+1);
            tid = 'f' + tid0;
            tr = document.getElementById(tid);
            if (!tr) {
                tid = 'p' + tid0;
                tr = document.getElementById(tid);
            }
            id_list[i] = tid;
            if (tr.className) {
                toHide = 0;
            }
        }
        for (var i = 0; i < count; i++) {
            tid = id_list[i];
            //修改点击无法收起的BUG，加入【详细】切换文字变化 --Findyou
            if (toHide) {
                document.getElementById(tid).className = 'hiddenRow';
                document.getElementById(cid).innerText = "展开明细"
            }
            else {
                document.getElementById(tid).className = '';
                document.getElementById(cid).innerText = "关闭明细"
            }
        }
    }

    function html_escape(s) {
        s = s.replace(/&/g,'&amp;');
        s = s.replace(/</g,'&lt;');
        s = s.replace(/>/g,'&gt;');
        return s;
    }
    </script>
    %(heading)s

    %(txtwenben)s
    %(ending)s
    </body>
    </html>
    """

    HEADING_ATTRIBUTE_TMPL = u"""<p class='attribute'><strong>%(name)s : </strong> %(value)s</p>
    """ # variables: (name, value)

    STYLESHEET_TMPL = u"""
    <style type="text/css" media="screen">
    body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 16px; }
    table       { font-size: 100%; }

    /* -- heading ---------------------------------------------------------------------- */
    .heading {
        margin-top: 0ex;
        margin-bottom: 1ex;
    }

    .heading .description {
        margin-top: 4ex;
        margin-bottom: 6ex;
    }

    /* -- report ------------------------------------------------------------------------ */
    #total_row  { font-weight: bold; }
    .passCase   { color: #5cb85c; }
    .failCase   { color: #d9534f; font-weight: bold; }
    .errorCase  { color: #f0ad4e; font-weight: bold; }
    .hiddenRow  { display: none; }
    .testcase   { font-size :14px; }
    </style>
    """
    # 增加返回顶部按钮
    ENDING_TMPL = u"""<div id='ending'>&nbsp;</div>
    <div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
    <a href="#"><span class="glyphicon glyphicon-eject" style = "font-size:30px;" aria-hidden="true">
    </span></a></div>
    """
    HEADING_TMPL = u"""<div class='heading'>
    <h2>%(title)s</h2>
    <hr style="height:1px;border:none;border-top:1px solid #555555;"/>
    %(parameters)s
    <hr style="height:1px;border:none;border-top:1px solid #555555;"/>
    </div>

    """

    def __init__(self, verbosity=1,title=None,description=None,tester=None):
        self.logging = Log()
        try:
            self.config = ReadYaml(FileUtil.getProjectObsPath() + u'/OperationConfig/config.yaml').getValue()
        except:
            self.logging.exception(u'存放html的config路径有问题，请查看',False)
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description
        if tester is None:
            self.tester = self.DEFAULT_TESTER
        else:
            self.tester = tester
        self.startTime = datetime.datetime.now()
    def _generate_heading(self,report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=saxutils.escape(name),
                value=saxutils.escape(value),
            )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title=saxutils.escape(self.title),
            parameters=''.join(a_lines),
            description=saxutils.escape(self.description),
            tester=saxutils.escape(self.tester),
        )
        self.logging.info(u'html文件标题生成成功')
        return heading
    def HTMLRun(self,HtmlContent):
        title = self.DEFAULT_TITLE
        stylesheet = self.STYLESHEET_TMPL
        ending = self.ENDING_TMPL

        startTime = str(self.startTime)[:19]
        result = [
            (u'发送方 ', self.tester),
            (u'发送时间 ', startTime),
        ]
        heading = self._generate_heading(result)
        output = self.HTML_TMPL % dict(
            title=saxutils.escape(title),
            generator=self.generator,
            stylesheet=stylesheet,
            heading=heading,
            txtwenben=HtmlContent,
            ending=ending,
        )
        self.logging.info(u'Html文件已经生成')
        return output
    #report_path : 导出路径，content： 内容
    def OutputHtml(self,content,report_path =None):
        if report_path is None:
            if self.config.get('report_path'):
                report_path = self.config['report_path']
        else:
            report_path = report_path

        output = self.HTMLRun(content)
        htmlmould = output.encode('utf8')  # 生成的html 模板
        try :
            if report_path :
                f, ext = os.path.split(report_path);
                report_path= f+self.startTime.strftime('%Y%m%d%H%M%S')+ext
                report_file = open(report_path, 'wb')
                stream = report_file
                stream.write(output.encode('utf8'))
                self.logging.info(u'HTML已经写入'+report_path)
        except :
            self.logging.exception(u'html存放路径错误',False)
        return htmlmould

