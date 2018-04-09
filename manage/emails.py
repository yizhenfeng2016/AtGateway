#-*- coding:utf-8 -*-
__author__ = 'Administrator'

import smtplib
import email
from email.header import Header
from email import MIMEMultipart,MIMEText,MIMEBase
import os
import sys

def send_email(msg_text,attachment_flag):
    fromaddr = "13592895405@163.com"
    toaddrs  = "1029568690@qq.com"
    subject="SmartHome App问题反馈"
    smtpserver='smtp.163.com'
    username='13592895405@163.com'
    password='mztkzpljrqyviuhm'

    # 构造MIMEMultipart对象做为根容器
    msg =MIMEMultipart.MIMEMultipart()
    # 构造MIMEText对象做为邮件显示内容并附加到根容器
    text_msg = MIMEText.MIMEText(msg_text,'plain','utf-8')
    msg.attach(text_msg)

    if attachment_flag:#带有附件
        # 构造MIMEBase对象做为文件附件内容并附加到根容器
        contype = 'application/octet-stream'
        maintype, subtype = contype.split('/', 1)
        app_path=""
        if getattr(sys,'frozen',False):
            app_path=os.path.dirname(sys.executable) #sys.executable：python.exe所在目录
        else:
            app_path=os.path.abspath('.')
        file="temp"
        log_filepath=os.path.join(app_path,file)
        log_files=os.listdir(log_filepath)
        for file in log_files:
            file_name=os.path.join(log_filepath,file)
            ## 读入文件内容并格式化
            data = open(file_name, 'rb')
            file_msg = MIMEBase.MIMEBase(maintype, subtype)
            file_msg.set_payload(data.read())
            data.close()
            email.Encoders.encode_base64(file_msg)
            ## 设置附件头
            basename = os.path.basename(file_name)
            file_msg.add_header('Content-Disposition',
             'attachment', filename = basename)
            msg.attach(file_msg)
    # else: #没有附件
    #     msg=email.mime.text.MIMEText(msg_text,'plain','utf-8')#中文需参数‘utf-8’，单字节字符不需要

    # 设置根容器属性
    msg['Subject']=Header(subject,'utf-8')
    msg['From']='用户<13592895405@163.com>'
    msg['To']='1029568690@qq.com'
    msg['Date'] = email.Utils.formatdate()

    # 用smtp发送邮件
    smtp=smtplib.SMTP()
    flag=True
    try:
        smtp.connect(smtpserver)
        smtp.login(username,password)
        smtp.sendmail(fromaddr,toaddrs,msg.as_string())
        flag=True
    except Exception as e:
        # print(e.message)
        flag=False
        smtp.quit()
    finally:
        return flag
