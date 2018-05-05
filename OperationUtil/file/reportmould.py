#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author:piepis
@file:reportmould.py
@time:2018-01-1915:24
@desc:  html 报告模板
'''
from xml.sax import saxutils
import datetime
__version__ = u"0.0.0.1"
__author__ = u"piepis"


def html(senttxt):
    #title
    DEFAULT_TITLE = 'Unit Test Report'
    #版本

    HTML_TMPL = ur"""<?xml version="1.0" encoding="UTF-8"?>
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
    ENDING_TMPL = """<div id='ending'>&nbsp;</div>
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
    generator = 'HTMLTestRunner %s' % __version__
    DEFAULT_TESTER=u'运维小凯'
    DEFAULT_DESCRIPTION = '22233'
    description = DEFAULT_DESCRIPTION
    tester = DEFAULT_TESTER

    startTime = datetime.datetime.now()
    startTime = str(startTime)[:19]
    result =  [
        (u'发送方 ', tester),
        (u'发送时间 ', startTime),
    ]

    def _generate_heading(report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = HEADING_ATTRIBUTE_TMPL % dict(
                name=saxutils.escape(name),
                value=saxutils.escape(value),
            )
            a_lines.append(line)
        heading = HEADING_TMPL % dict(
            title=saxutils.escape(title),
            parameters=''.join(a_lines),
            description=saxutils.escape(description),
            tester=saxutils.escape(tester),
        )
        return heading


    title = DEFAULT_TITLE
    stylesheet = STYLESHEET_TMPL
    ending = ENDING_TMPL
    heading = _generate_heading(result)
    output = HTML_TMPL % dict(
        title=saxutils.escape(title),
        generator=generator,
        stylesheet=stylesheet,
        heading = heading,
        ending=ending,
        txtwenben = senttxt,
    )

    report_path = r'E:\git_lib\api_testing\report\report1.html'
    report_file = open(report_path, 'wb')
    stream = report_file
    hh =output.encode('utf8')
    stream.write(output.encode('utf8'))
    return hh
