#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author:piepis
@file:SendEmail.py
@time:2017-12-2210:41
@desc: 发送邮件
'''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os
from OperationUtil.log.log import Log
class SendMail:
    '''邮件发送'''
    def __init__(self):
        self.loging = Log()
    def send_mail(self, receiver, sender, sender_pwd, email_host, title, content, attachments=None):
        try:
            msg = MIMEMultipart()
            msg['Subject'] = title
            msg['Form'] =  sender
            msg['To'] = COMMASPACE.join(receiver)
            msg['Date'] = formatdate(localtime=True)
            msg.attach(MIMEText(content, _subtype='html', _charset='utf-8'))
            if attachments :
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(open(attachment, 'rb').read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
                    msg.attach(part)
            smtp = smtplib.SMTP()
            smtp.connect(email_host)
            smtp.login(sender, sender_pwd)
            smtp.sendmail(sender, receiver, msg.as_string())
            smtp.quit()
            self.loging.info('邮件发送成功')
            return True
        except Exception:
            self.loging.exception('本次邮件发送失败',False)
            raise
if __name__ == '__main__':
    from OperationUtil.file.readyaml import ReadYaml
    from OperationUtil.file.fileutil import FileUtil
    config = ReadYaml(FileUtil.getProjectObsPath() + '/OperationConfig/config.yaml').getValue()
    receiver = config['email_receiver']
    sender = config['email_sender']
    sender_pwd = config['email_sender_pwd']
    email_host = config['email_host']
    title = config['email_title']
    content = '测试邮件'
    attachments = [r"F:\2018-01-16\report.html"]
    SendMail().send_mail(receiver, sender, sender_pwd, email_host, title, content, attachments)
    print('sendMail')
