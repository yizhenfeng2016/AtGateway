#coding:utf-8
__author__ = 'Administrator'
import re
from share import logfile
import os

jiemi_msg='''{"msg_type":{"someone_login":"login"},"from_role":"coordin_zigbee"}fffgddd'''
jiemi_msg=re.findall(r"{(.*)}",jiemi_msg)
for l in jiemi_msg:
    jiemi_msg='{'+l+'}'
    logfile.logger.info(jiemi_msg)
    d=dict(eval(jiemi_msg))
    logfile.logger.info(d)
    logfile.logger.info(type(d))

while True:
    try:
        i=4/0
    except Exception as e:
        logfile.logger.exception(e.message)
# finally:
#     print(i)


#!/usr/bin/python
# -*- coding: utf-8 -*-

# import sys
# from PyQt4 import QtGui, QtCore
# import webbrowser
#
#
# class MainWindow(QtGui.QMainWindow):
#
#     def __init__(self):
#
#         QtGui.QMainWindow.__init__(self)
#         self.resize(250, 150)
#         self.setWindowTitle('Mainwindow')
#
#         exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
#         # 设置行为栏目图标，显示字符
#         exit.setShortcut('Ctrl+Q')
#         # 设置对应的快捷键
#         exit.setStatusTip('Exit application')
#         # 设置状态栏提示
#         self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
#         # 设置点击exit设置栏目行为：以点击为信号，触发退出的操作
#
#         menubar = self.menuBar()
#         # 创建菜单栏
#         file = menubar.addMenu('&File')
#         # 初始化一级栏目和名称
#         file.addAction(exit)
#         # 在一级栏目下添加之前制定的行为栏目
#
#         self.statusBar().showMessage('Ready')
#         # 设置状态栏，并显示指定的消息
#
# app = QtGui.QApplication(sys.argv)
# main = MainWindow()
# main.show()
# sys.exit(app.exec_())

# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
#
# fromaddr = "13592895405@163.com"
# toaddrs  = "1029568690@qq.com"
#
# subject="python email test"
# smtpserver='smtp.163.com'
#
# username='13592895405@163.com'
# password='mztkzpljrqyviuhm'
#
# msg=MIMEText("你好",'plain','utf-8')#中文需参数‘utf-8’，单字节字符不需要
# msg['Subject']=Header(subject,'utf-8')
# msg['From']='fankui<13592895405@163.com>'
# msg['To']='1029568690@qq.com'
#
# smtp=smtplib.SMTP()
# smtp.connect(smtpserver)
# smtp.login(username,password)
# smtp.sendmail(fromaddr,toaddrs,msg.as_string())
# smtp.quit()

