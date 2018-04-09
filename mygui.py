#-*- coding:utf-8 -*-
__author__ = 'Administrator'

import gui
from PyQt4 import QtCore, QtGui

from business.remote import LoginManage
from business.remote import GetAesKey
from business.local import SendRecvManage
from business.search import SearchDevice
from manage import msg,function,emails
from query.query import QueryMsg
from control.control import Control
from share import user,queue

import time
import Queue
import webbrowser
import sys
import os
import dialog
import socket

control_q=Queue.Queue()

HostName="server.atsmartlife.com"

try:
    _fromUtf8 = QtCore.QString.fromUtf8
    _toUtf8=QtCore.QString.toUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class MyMainWindow(QtGui.QMainWindow,gui.Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)#将自己MyMainWindow作为对象，调用父类的setupUi的方法，从而获取组件
        self.initialize()

    def initialize(self):
        self.addMenu()
        self.addStatus("status_show")
        username_re=QtCore.QRegExp(r"[0-9]+")
        password_re=QtCore.QRegExp(r"[A-Za-z0-9]{6,16}")

        self.usernameEdit.setValidator(QtGui.QRegExpValidator(username_re,self))
        self.username2lineEdit.setValidator(QtGui.QRegExpValidator(username_re,self))
        self.passwordEdit.setValidator(QtGui.QRegExpValidator(password_re,self))
        self.pidcomboBox.addItem("gateway")
        self.pidcomboBox.addItem("mirror")
        self.pidcomboBox.addItem("coordin_zigbee")
        # self.pidcomboBox.addItem("icool")
        # self.pidcomboBox.addItem("aqms")

        self.classcomboBox.addItem("gateway")
        self.classcomboBox.addItem("coordin_zigbee")
        self.classcomboBox.addItem("mirror")
        self.logcat_thread=""
        self.control_thread=""
        self.key_thread_p=""
        self.get_thread_p=""
        self.getResult_thread=""
        self.getRecvall_thread_l=""

        self.loginButton.clicked.connect(self.login)
        self.logoutButton.clicked.connect(self.logout)
        self.netloginpushButton.clicked.connect(self.login)
        self.netlogoutpushButton.clicked.connect(self.logout)

        self.logcat_thread=logcatThread() #打印线程
        self.logcat_thread.start()
        self.control_thread=controlThread()#向服务器发送控制cmd线程
        self.control_thread.start()
        self.getResult_thread=getResultThread() #处理返回信息线程
        self.getResult_thread.start()

        self.getlogout_thread=getLogoutTheard()#退出线程
        self.getlogout_thread.start()

        self.status_thread=statusThread()#状态栏显示线程
        self.status_thread.start()

        self.connect(self.status_thread,QtCore.SIGNAL("status_show(QString)"),self.addStatus)

        self.sendButton.clicked.connect(self.send_control_cmd)
        self.connect(self.logcat_thread,QtCore.SIGNAL("getprint(QString)"),self.update_textBrowser)
        self.connect(self.getlogout_thread,QtCore.SIGNAL("getlogout(QString)"),self.logout_manage)
        self.connect(self.classcomboBox,QtCore.SIGNAL('activated(int)'),self.update_device_type)
        self.connect(self.ipcomboBox,QtCore.SIGNAL('activated(int)'),self.update_device_info)
        self.update_device_type(0) #设置默认值
        self.connect(self.control_thread,QtCore.SIGNAL("getcounts(QString)"),self.update_lineEdit)
        self.clearpushButton.clicked.connect(self.clear_textEdit)
        self.cleartextBrowsepushButton.clicked.connect(self.clear_textBrowser)

        self.gundongpushButton.clicked.connect(self.logcatgundong)
        self.gundongflag=False

        self.logcatstoppushButton.clicked.connect(self.logcatstop)
        self.cmdstoppushButton.clicked.connect(self.cmdstop)
        self.controlstoppushButton.clicked.connect(self.controlstop)
        self.searchpushButton.clicked.connect(self.search_devices)
        self.freshpushButton.clicked.connect(self.fresh_devices_or_combs)

    def addMenu(self):
        app_path=""
        if getattr(sys,'frozen',False):
            app_path=os.path.dirname(sys.executable) #sys.executable：python.exe所在目录
        else:
            app_path=os.path.abspath('.')
        # 设置行为栏目图标，显示字符
        openfile=QtGui.QAction(QtGui.QIcon(os.path.join(app_path,'icons/openfile.ico')), _translate("MainWindow", "打开", None), self)
        openfile.setShortcut('Ctrl+O') # 设置对应的快捷键
        # openfile.setStatusTip('openfile')# 设置状态栏提示
        newfile=QtGui.QAction(QtGui.QIcon(os.path.join(app_path,'icons/newfile.ico')), _translate("MainWindow", "新建", None), self)
        newfile.setShortcut('Ctrl+N') # 设置对应的快捷键

        savefile=QtGui.QAction(QtGui.QIcon(os.path.join(app_path,'icons/savefile.ico')), _translate("MainWindow", "保存", None), self)
        savefile.setShortcut('Ctrl+S') # 设置对应的快捷键

        setting=QtGui.QAction(QtGui.QIcon(os.path.join(app_path,'icons/setting.ico')), _translate("MainWindow", "设置", None), self)
        setting.setShortcut('Ctrl+T') # 设置对应的快捷键

        exitapp= QtGui.QAction(QtGui.QIcon(os.path.join(app_path,'icons/exit.ico')), _translate("MainWindow", "退出", None), self)
        exitapp.setShortcut('Ctrl+Q') # 设置对应的快捷键
        # exit.setStatusTip('Exit application')# 设置状态栏提示
        self.connect(exitapp, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()')) # 设置点击exit设置栏目行为：以点击为信号，触发退出的操作
        self.fileMenu = self.menuBar().addMenu("&"+_translate("MainWindow", "文件", None))# 初始化一级栏目和名称
        #创建子菜单
        self.fileMenu.addAction(newfile)
        self.fileMenu.addAction(openfile)
        self.fileMenu.addAction(savefile)
        self.fileMenu.addAction(setting)
        self.fileMenu.addAction(exitapp)

        helpdoc=QtGui.QAction(QtGui.QIcon(os.path.join(app_path,'icons/helpdoc.ico')), _translate("MainWindow", "使用操作", None), self,triggered=self.helpdoc)
        helpdoc.setShortcut('Ctrl+H')
        email=QtGui.QAction(QtGui.QIcon(os.path.join(app_path,'icons/email.ico')), _translate("MainWindow", "提交反馈", None), self,triggered=self.sendemail)
        email.setShortcut('Ctrl+E')
        self.helpMenu = self.menuBar().addMenu("&"+_translate("MainWindow", "帮助", None))
        self.helpMenu.addAction(helpdoc)
        self.helpMenu.addAction(email)

    def helpdoc(self):
        app_path=""
        if getattr(sys,'frozen',False):
            app_path=os.path.dirname(sys.executable) #sys.executable：python.exe所在目录
        else:
            app_path=os.path.abspath('.')
        path="file:///"+app_path+"/html/helpdoc.html"
        webbrowser.open(path,new=0)

    def sendemail(self):
        types={
            0:"功能建议",
            1:"功能异常",
            2:"其他问题"
        }
        input_dialog=dialog.MultiInPutDialog()
        if input_dialog.exec_():
            question_type=types[2]
            if input_dialog.radioButton_1.isChecked():
                question_type=types[0]
            if input_dialog.radioButton_2.isChecked():
                question_type=types[1]
            if input_dialog.radioButton_3.isChecked():
                question_type=types[2]

            text=input_dialog.textEdit.toPlainText()
            text=str(_toUtf8(text))
            email_text="问题类型："+question_type+"\n"+"反馈意见："+text
            # attachment_flag=True
            if input_dialog.checkBox.isChecked():
                attachment_flag=True
            else:
                attachment_flag=False
            self.send_email_thread=sendEmailThread(email_text,attachment_flag)
            self.send_email_thread.start()#如果send_email_thread是局部变量，当sendemail函数结束时，他的生命也结束
                                          #所以send_email_thread不能为局部变量
            self.connect(self.send_email_thread,QtCore.SIGNAL("status_show(QString)"),self.addStatus)

    def addStatus(self,status_msg):
        # 设置状态栏，并显示指定的消息
        # print(status_msg)
        if status_msg=="status_show":
            space=" "*90
            self.statusBar().showMessage(space+'Copyright (C) 1999-2015 YiZhenFeng All Rights Reserved')

        if status_msg=="email_send_success":
            QtGui.QMessageBox.about(self,"info",_translate("Dialog", "您的宝贵意见已收到，谢谢您的反馈！", None))

        if status_msg=="email_send_failure":
            QtGui.QMessageBox.about(self,"info",_translate("Dialog","邮件发送失败，请重新发送！",None))
    
    def logout_manage(self,msg):
        if msg=="someone_login":
            #有人抢登,停止有关线程
            LoginManage().loginout()
            if self.get_thread_p:
                # print("stop get_thread_p thread")
                self.get_thread_p.stop()
            if self.key_thread_p:
                # print("stop key_thread_p thread")
                self.key_thread_p.stop()
            self.sipaddrcomboBox.clear()
            self.combstextBrowser.clear()
            self.devlisttextBrowser.clear()
            QtGui.QMessageBox.about(self,"Info",_fromUtf8("someone login,please login again"))

        if msg=="forced_exit":
            # print("come in loginout================")
            #停止有关线程
            if self.getRecvall_thread_l:
                # print("stop getRecvall_thread_l thread")
                self.getRecvall_thread_l.stop()
                # time.sleep(5) #等待线程接受完数据
            self.combstextBrowser.clear()
            self.devlisttextBrowser.clear()
            QtGui.QMessageBox.about(self,"Info",_fromUtf8("someone login,please loginout on other place and login again"))

        if msg=="someone_login_zigbee":
            #停止有关线程
            if self.getRecvall_thread_l:
                # print("stop getRecvall_thread_l thread")
                self.getRecvall_thread_l.stop()
                # time.sleep(5) #等待线程接受完数据
            self.combstextBrowser.clear()
            self.devlisttextBrowser.clear()
            QtGui.QMessageBox.about(self,"Info",_fromUtf8("someone login,please login again"))

        if msg=="login_failure":
            QtGui.QMessageBox.about(self,"Info","login failure")


    def login(self):
        """
        Net_flag=0 #走内网
        Net_flag=1 #走公网
        默认 Net_flag=1
        """
        if self.publicradioButton.isChecked() or self.netradioButton.isChecked():
            if self.publicradioButton.isChecked():
                # print("choose public network")
                # user.Net_flag=1
                user.set_info_dict("Net_flag",1)
            elif self.netradioButton.isChecked():
                # print("choose local network")
                # user.Net_flag=0 #走内网
                user.set_info_dict("Net_flag",0)

            # print(user.Net_flag)
            # print(user.get_info_dict("Net_flag"))
            if user.get_info_dict("Net_flag")==1: #走公网
                try:
                    Server_IP=socket.gethostbyname(HostName)
                except Exception as e:
                    Server_IP="139.159.224.188"
                # POST_SECUREPORT_URL="http://112.74.28.12/secureport"
                # POST_MSG_URL="http://112.74.28.12/postmsg"
                # GET_URL="http://112.74.28.12/getmsg"
                finally:
                    user.set_info_dict("POST_SECUREPORT_URL","http://{0}/secureport".format(Server_IP))
                    user.set_info_dict("POST_MSG_URL","http://{0}/postmsg".format(Server_IP))
                    user.set_info_dict("GET_URL","http://{0}/getmsg".format(Server_IP))
                    user.set_info_dict("USERNAME",str(self.usernameEdit.text()))
                    password=str(self.passwordEdit.text())
                    user.set_info_dict("PASSWORD",password)
                    if len(password)>=6 and len(password)<=16:
                        msg=LoginManage().login()
                        if msg=="Login success":
                            #停止内网线程
                            if self.getRecvall_thread_l:
                                # print("stop getRecvall_thread_l thread")
                                self.getRecvall_thread_l.stop()

                            self.key_thread_p=getAesKeyThread()
                            self.key_thread_p.start() #动态获取密钥线程
                            time.sleep(0.1)
                            self.get_thread_p=getMsgThread()
                            self.get_thread_p.start() #向服务器get请求线程

                            QueryMsg().get_all_friends() #向服务器get_friends
                            self.connect(self.pidcomboBox,QtCore.SIGNAL('activated(int)'),self.update_addrs)
                            self.update_addrs(0) #设置默认值
                            self.okButton.clicked.connect(self.okbutton_updataUI)
                            self.logoutButton.clicked.connect(self.logout)
                        QtGui.QMessageBox.about(self,"Info",_fromUtf8(msg))
                    else:
                        QtGui.QMessageBox.about(self,"Info",_fromUtf8(str("password length is 6 to 16")))

            else:  #走内网
                connect_flag=1
                if user.get_info_dict("SERVER_PORT")==9101: #室内机通讯---tcp socket；网关通讯---http(get,post)
                    connect_flag=user.create_tcp_socket(user.get_info_dict("SERVER_IP"),user.get_info_dict("SERVER_PORT"))
                    # print(connect_flag)
                if connect_flag:
                    self.getRecvall_thread_l=getRecvallThread() #接受服务器信息线程
                    self.getRecvall_thread_l.start()
                    login_flag=SendRecvManage().login()
                    if login_flag:
                        QtGui.QMessageBox.about(self,"Info","login success")
                        #停止公网有关线程
                        if self.get_thread_p:
                            # print("stop get_thread_p thread")
                            self.get_thread_p.stop()
                        if self.key_thread_p:
                            # print("stop key_thread_p thread")
                            self.key_thread_p.stop()
                        query_manage=QueryMsg()
                        query_manage.combination_control_query()
                        query_manage.room_query()
                        query_manage.devices_query()
                        time.sleep(2)
                        self.devlisttextBrowser.clear()
                        self.combstextBrowser.clear()
                        self.display_combs()
                        self.display_devices()
                    else:
                        queue.logout_Q.put("login_failure")
                        self.getRecvall_thread_l.stop()
                        self.getResult_thread.stop()
                else:
                    QtGui.QMessageBox.about(self,"Info","tcp connect failure")
        else:
            QtGui.QMessageBox.about(self,"Info","please choose login mode")

    def logout(self):
        #退出登录，关闭有关线程
        # print("come in logout")
        """
        Net_flag=0 #走内网
        Net_flag=1 #走公网
        默认 Net_flag=1
        """
        if self.publicradioButton.isChecked() or self.netradioButton.isChecked():
            if user.get_info_dict("Net_flag")==1: #走公网
                msg=LoginManage().loginout()
                # print(msg)
                if msg!="":
                    dict_msg=dict(eval(msg))
                    if dict_msg.get("result",None)=="success":
                        # print("come in stop thread")
                        #停止公网有关线程
                        if self.get_thread_p:
                            # print("stop get_thread_p thread")
                            self.get_thread_p.stop()
                        if self.key_thread_p:
                            # print("stop key_thread_p thread")
                            self.key_thread_p.stop()
                        QtGui.QMessageBox.about(self,"Info",_fromUtf8(str(msg)))
                        self.sipaddrcomboBox.clear()
                        self.combstextBrowser.clear()
                        self.devlisttextBrowser.clear()
                else:
                    # print("check in the network")
                    msg="check in the network"
                    QtGui.QMessageBox.about(self,"Info",_fromUtf8(str(msg)))

            elif user.get_info_dict("Net_flag")==0: #走局域网
                #停止局域网有关线程
                if self.getRecvall_thread_l:
                    # print("stop getRecvall_thread_l thread")
                    self.getRecvall_thread_l.stop()
                    time.sleep(3) #等待线程接受完数据
                    QtGui.QMessageBox.about(self,"Info",_fromUtf8(str("logout success")))
                    self.combstextBrowser.clear()
                    self.devlisttextBrowser.clear()
                else:
                    QtGui.QMessageBox.about(self,"Info",_fromUtf8(str("not login")))
        else:
            QtGui.QMessageBox.about(self,"Info","please choose login mode")

    def fresh_devices_or_combs(self):
        query_devs=QueryMsg()
        query_devs.room_query()
        query_devs.devices_query()
        query_devs.combination_control_query()
        time.sleep(2)
        self.display_combs()
        self.display_devices()

    def logcatgundong(self):
        if self.gundongflag:
            self.gundongflag=False
            self.gundongpushButton.setText(_translate("MainWindow", "自动滚动", None))
        else:
            self.gundongflag=True
            self.gundongpushButton.setText(_translate("MainWindow", "停止滚动", None))

    def logcatstop(self):
        if self.logcat_thread:
            if self.logcat_thread.flag:
                self.logcat_thread.pause()
                self.logcatstoppushButton.setText(_translate("MainWindow", "恢复", None))
            else:
                self.logcat_thread.resume()
                self.logcatstoppushButton.setText(_translate("MainWindow", "暂停", None))

    def cmdstop(self):
         if self.control_thread:
            if self.control_thread.flag:
                self.control_thread.pause()
                self.cmdstoppushButton.setText(_translate("MainWindow", "恢复", None))
            else:
                self.control_thread.resume()
                self.cmdstoppushButton.setText(_translate("MainWindow", "暂停", None))

    def controlstop(self):
        if self.control_thread:
            if self.control_thread.running:
                self.control_thread.stop()
                self.controlstoppushButton.setText(_translate("MainWindow", "开始", None))
            else:
                self.control_thread.resume()
                self.control_thread.start() #线程重新开始
                self.controlstoppushButton.setText(_translate("MainWindow", "停止", None))

    def clear_textEdit(self):
        self.sendtextEdit.clear()

    def clear_textBrowser(self):
        self.logcattextBrowser.clear()

    def update_lineEdit(self,txt):
        self.countslineEdit.clear()
        self.countslineEdit.setText(txt)

    def update_textBrowser(self,txt):
        now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        log=now_time+"----------"+txt
        self.logcattextBrowser.append(log)
        self.logcattextBrowser.append("")
        #自动滚行:在程序执行过程中去翻看前面的 信息，如果不把光标（虽然光标看不见）
        #定位到最后一行，就会从翻看的位置打印信息，增加这三行代码，无论什么时候都能
        #自动定位到最后一行
        if self.gundongflag:
            cursor = self.logcattextBrowser.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            self.logcattextBrowser.setTextCursor(cursor)

    def display_combs(self):
        # print("come in display_combs")
        # combs_list=user.data_dict.get("combs",None)
        combs_list=user.get_data_dict("combs")
        self.combstextBrowser.clear()
        if combs_list:
            for cl in combs_list:
                control_name=cl.get("control_name")
                item=control_name
                if item:
                    self.combstextBrowser.append(_fromUtf8(item))

    def display_devices(self):
        # print("come in display_devices")
        # device_list=user.data_dict.get("devices",None)
        device_list=user.get_data_dict("devices")
        # print(device_list)
        self.devlisttextBrowser.clear()
        if device_list:
            dev_list_by_type,class_types=function.dev_by_classtype(device_list)
            # print(dev_list_by_type)
            # print(class_types)
            if class_types:
                for c in class_types:
                    for d in dev_list_by_type:
                        if d.get(c,None):
                            cm=c+"："
                            self.devlisttextBrowser.append(_fromUtf8(cm))
                            temp_list=d.get(c)
                            for tl in temp_list:
                                if tl:
                                    item='，'.join(tl)
                                    item="    "+item
                                    self.devlisttextBrowser.append(_fromUtf8(item))

    def send_control_cmd(self):
        # print("send control cmd")
        cmd_all_list=[]
        loop_times=1
        if self.loopcheckBox.isChecked():
            loop_times=self.loopspinBox.value()
            # print(loop_times)
        cmd_all_list.append(loop_times)
        cmds=str(_toUtf8(self.sendtextEdit.toPlainText()))
        # cmd=unicode(cmds,'utf-8','ignore')
        # print(cmds)
        if cmds:
            cmds_list=function.split_cmd(cmds)
            # print(len(cmds_list))
            for cl in cmds_list:
                dev_class_type,cmd_list=function.cmd_by_deviceorcombs_data(cl)
                if dev_class_type:
                    msg_list=[dev_class_type,cmd_list]
                    cmd_all_list.append(msg_list)
                else:
                    QtGui.QMessageBox.about(self,"Info","dataset has not this device")
            # print("send control cmd to control thread",cmd_all_list)
            control_q.put(cmd_all_list)
        else:
            QtGui.QMessageBox.about(self,"Info","Please input cmd")

    def update_addrs(self,index):
        # print("come in update_addrs")
        self.sipaddrcomboBox.clear()
        # friend_l=user.data_dict.get("usr",None)
        friend_l=user.get_data_dict("usr")
        if friend_l:
            if index==0:
                user.set_info_dict("PID","0002")
                for l in friend_l:
                    if l.get("type",None)=="gateway":
                        self.sipaddrcomboBox.addItem(l.get("friend"))

            elif index==1:
                user.set_info_dict("PID","0008")
                for l in friend_l:
                    if l.get("type",None)=="mirror":
                        self.sipaddrcomboBox.addItem(l.get("friend"))
            elif index==2:
                user.set_info_dict("PID","0003")
                for l in friend_l:
                    if l.get("type",None)=="coordin_zigbee":
                        self.sipaddrcomboBox.addItem(l.get("friend"))
            elif index==3:
                user.set_info_dict("PID","0001")
                for l in friend_l:
                    if l.get("type",None)=="icool":
                        self.sipaddrcomboBox.addItem(l.get("friend"))
            elif index==4:
                user.set_info_dict("PID","0004")
                for l in friend_l:
                    if l.get("type",None)=="aqms":
                        self.sipaddrcomboBox.addItem(l.get("friend"))
        else:
            QtGui.QMessageBox.about(self,"Info","no friends")

    def okbutton_updataUI(self):
        # print("come in set_sipaddr")
        sipaddr=self.sipaddrcomboBox.currentText()
        user.set_info_dict("SIPADDR",str(sipaddr))
        if sipaddr=="":
            QtGui.QMessageBox.about(self,"Info",_fromUtf8("please choose sipaddr"))
        else:
            self.devlisttextBrowser.clear()
            query_instance=QueryMsg()# 初始化QueryMsg实例
            query_instance.get_dev_status()
            self.display_combs()
            self.display_devices()
            self.control_thread=controlThread()
            self.control_thread.start()#向服务器发送控制cmd线程
            self.sendButton.clicked.connect(self.send_control_cmd)

    def update_device_type(self,index):
        # print("come in update_port")
        if index==0: #gateway
            user.set_info_dict("PID","0002")
        elif index==1: #zigbee
            user.set_info_dict("PID","0003")
        elif index==2: #mirror
            user.set_info_dict("PID","0008")

    def search_devices(self):
        self.ipcomboBox.clear()
        if self.username2lineEdit.text():
            user.set_info_dict("USERNAME",str(self.username2lineEdit.text()))
            SearchDevice().search()
            devices_list=user.get_data_dict("search")
            if devices_list:
                dev_list=function.search_devices_by_type(devices_list)
                if dev_list:
                    for l in dev_list:
                        self.ipcomboBox.addItem(l.get("server_ip"))
                    self.update_device_info(0)
        else:
            QtGui.QMessageBox.about(self,"Info",_fromUtf8("please filling in username"))

    def update_device_info(self,index):
        # print("come in update device info")
        SERVER_IP=str(self.ipcomboBox.currentText())
        user.set_info_dict("SERVER_IP",SERVER_IP)
        # print("server_ip===",user.get_info_dict("SERVER_IP"))
        user.set_info_dict("getHttp","http://{0}/lua/getall".format(SERVER_IP))
        user.set_info_dict("postHttp","http://{0}/lua".format(SERVER_IP))
        devices_list=user.get_data_dict("search")
        if devices_list:
            dev_list=function.search_devices_by_type(devices_list)
            device=dev_list[index]
            SERVER_PORT=device.get("server_port",None)
            if SERVER_PORT:
                user.set_info_dict("SERVER_PORT",SERVER_PORT)
            # print("server_port===", SERVER_PORT)
            data_length=device.get("data_length",None)
            if data_length:
                user.set_info_dict("data_length",data_length)
            # print("data_length===",data_length)
            SIPADDR=device.get("sip_addr",None)
            if SIPADDR:
                user.set_info_dict("SIPADDR",SIPADDR)

class controlThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.control_instance=Control()
        self.running=True #用于停止线程
        self.flag=True  #用于暂停线程
        self.runed_times=0 #用于记录暂停前的执行的次数
        self.runed_looptimes=1 #用于记录暂停前要循环执行的次数
        self.loopflag=True #用于循环暂停

    def run(self):
        # print("start controlThread")
        while self.running:
            if not control_q.empty():
                # print("got cmd windows data")
                cmd_all_list=control_q.get()
                self.runed_looptimes=cmd_all_list[0]
                self.loopflag=True
                while self.loopflag:
                    for t in range(self.runed_times,self.runed_looptimes): #循环次数
                        # print(self.flag)
                        if self.flag:
                            if self.running:
                                counts=t+1
                                self.emit(QtCore.SIGNAL("getcounts(QString)"),_fromUtf8(str(counts)))
                                for i in range(1,(len(cmd_all_list))):
                                    msg_list=cmd_all_list[i]
                                    dev_class_type=msg_list[0]
                                    cmd_list=msg_list[1]
                                    self.control_instance.devices_c(dev_class_type,cmd_list)
                                    # print("send control cmd to server")
                            else:
                                break
                        else:
                            self.runed_times=t
                            break
                    if self.flag:
                        self.loopflag=False
                    else:
                        self.loopflag=True

    def pause(self):
        self.flag=False

    def resume(self):
        self.running=True
        self.loopflag=True #用于循环暂停
        self.flag=True


    def stop(self):
        self.loopflag=True #用于循环暂停
        self.flag=True # 将线程从暂停状态恢复, 如何已经暂停的话
        self.running=False
        self.runed_times=0 #用于记录暂停前的执行的次数
        self.runed_looptimes=1 #用于记录暂停前要循环执行的次数

class logcatThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.running=True
        self.flag=True

    def run(self):
        # print("start logcatThread")
        while self.running:
            try:
                data=msg.OnDataCallback()
                if data:
                    if self.flag:
                        self.emit(QtCore.SIGNAL("getprint(QString)"),_fromUtf8(data))
            except:
                break

    def pause(self):
        self.flag=False

    def resume(self):
        self.flag=True

    def stop(self):
        self.flag=True # 将线程从暂停状态恢复, 如何已经暂停的话
        self.running=False

class getMsgThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.GetMsg=msg.GetMsg()
        self.running=True
        self.flag=True

    def run(self):
        # print("start getMsgThread")
        while self.running:
            if self.flag:
                # print("get_msg")
                self.GetMsg.get_msg()

    def pause(self):
        self.flag=False

    def resume(self):
        self.flag=True

    def stop(self):
        self.flag=True # 将线程从暂停状态恢复, 如何已经暂停的话
        self.running=False

class getAesKeyThread(QtCore.QThread):
    '''QT中子线程内不能操作GUI界面，切记切记'''
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.GetAesKey=GetAesKey()
        self.running=True
        self.flag=True

    def run(self):
        # print("start getAesKeyThread")
        timer_interval=self.GetAesKey.get_aes()
        while self.running:
            time.sleep(timer_interval)
            if self.flag:
                timer_interval=self.GetAesKey.get_aes()

    def pause(self):
        self.flag=False

    def resume(self):
        self.flag=True

    def stop(self):
        self.flag=True # 将线程从暂停状态恢复, 如何已经暂停的话
        self.running=False

class getRecvallThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.GetRecvall=SendRecvManage()
        self.running=True
        self.flag=True

    def run(self):
        # print("start getRecvallThread")
        while self.running:
            if self.flag:
                self.GetRecvall.recv_all()

    def pause(self):
        self.flag=False

    def resume(self):
        self.flag=True

    def stop(self):
        self.flag=True # 将线程从暂停状态恢复, 如何已经暂停的话
        self.running=False

class getResultThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.GetResult=msg.ResultOnCallBack()
        self.running=True
        self.flag=True

    def run(self):
        # print("start getResultThread")
        while self.running:
            if self.flag:
                self.GetResult.result_deal()

    def pause(self):
        self.flag=False

    def resume(self):
        self.flag=True

    def stop(self):
        self.flag=True # 将线程从暂停状态恢复, 如何已经暂停的话
        self.running=False

class getLogoutTheard(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        # print("start getlogoutThread")
        while True:
            if not queue.logout_Q.empty():
                # print("come in get logout queue")
                logout_msg=queue.logout_Q.get()
                self.emit(QtCore.SIGNAL("getlogout(QString)"),_fromUtf8(logout_msg))


class statusThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while True:
            self.emit(QtCore.SIGNAL("status_show(QString)"),_fromUtf8("status_show"))
            time.sleep(3)

class sendEmailThread(QtCore.QThread):
    def __init__(self,msg_text,attachment_flag):
        QtCore.QThread.__init__(self)
        self.text=msg_text
        self.flag=attachment_flag

    def run(self):
        flag=emails.send_email(self.text,self.flag)
        if flag:
            self.emit(QtCore.SIGNAL("status_show(QString)"),_fromUtf8("email_send_success"))
        else:
            self.emit(QtCore.SIGNAL("status_show(QString)"),_fromUtf8("email_send_failure"))