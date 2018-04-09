#-*- coding:utf-8 -*-
__author__ = 'Administrator'

from mygui import MyMainWindow
from PyQt4 import QtGui
import sys

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    win=MyMainWindow()
    win.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     MainWindow = QtGui.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())

# from share import user
# from business.local import SendRecvManage
# from manage.msg import ResultOnCallBack
# import threading
# import time
#
# def getrecv(sock):
#     while True:
#         sock.recv_all()
#
# def getresult(res):
#     while True:
#         res.result_deal()
#
# if __name__=="__main__":
#     ip="192.168.1.103"
#     port=9102
#     # connect_flag=user.create_tcp_socket(ip,port)#创建socket
#     # if connect_flag:
#     print("connect success")
#     sock=SendRecvManage()
#     res=ResultOnCallBack()
#
#     print("get")
#     send=threading.Thread(target=getrecv,args=(sock,))
#     send.start()
#
#     result=threading.Thread(target=getresult,args=(res,))
#     result.start()
#     print("result")
#
#     r=sock.login()  #登录
#     print(r)
#
#     send.join()
#     result.join()
#
#     print(time.time())
#     print("jiesu")