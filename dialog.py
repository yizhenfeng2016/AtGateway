# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Sun Oct 29 16:18:34 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
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

class MultiInPutDialog(QtGui.QDialog):

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.resize(450, 300)
        self.setWindowTitle(_translate("Dialog", "问题反馈", None))
        app_path=""
        if getattr(sys,'frozen',False):
            app_path=os.path.dirname(sys.executable) #sys.executable：python.exe所在目录
        else:
            app_path=os.path.abspath('.')
        self.setWindowIcon(QtGui.QIcon(os.path.join(app_path,'icons/dialog.ico')))
        grid = QtGui.QGridLayout()
        self.label_1 = QtGui.QLabel(_translate("Dialog", "请选择您要反馈的问题类型：（单选）", None),parent=self)
        self.label_1.setGeometry(QtCore.QRect(10, 10, 211, 31))
        grid.addWidget(self.label_1, 0, 0, 1, 0)

        self.radioButton_1 = QtGui.QRadioButton(_translate("Dialog", "功能建议", None),parent=self)
        self.radioButton_2= QtGui.QRadioButton(_translate("Dialog", "功能异常", None),parent=self)
        self.radioButton_3 = QtGui.QRadioButton(_translate("Dialog", "其他问题", None),parent=self)
        self.radioButton_1.setGeometry(QtCore.QRect(30, 50, 89, 31))
        self.radioButton_2.setGeometry(QtCore.QRect(150, 50, 89, 31))
        self.radioButton_3.setGeometry(QtCore.QRect(280, 50, 89, 31))
        grid.addWidget(self.radioButton_1,1, 0, 1, 1)
        grid.addWidget(self.radioButton_2,1, 1, 1, 1)
        grid.addWidget(self.radioButton_3,1, 2, 1, 1)

        self.label_2 = QtGui.QLabel(_translate("Dialog", "您的意见：", None),parent=self)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 61, 21))
        grid.addWidget(self.label_2, 3, 0, 1, 0)

        self.textEdit = QtGui.QTextEdit(parent=self)
        self.textEdit.setGeometry(QtCore.QRect(30, 120, 391, 191))
        grid.addWidget(self.textEdit, 4, 0, 1, 0)

        self.checkBox = QtGui.QCheckBox(_translate("Dialog", "上传错误日记", None),parent=self)
        self.checkBox.setGeometry(QtCore.QRect(20, 330, 121, 41))
        grid.addWidget(self.checkBox, 5, 0, 1, 0)

        buttonBox = QtGui.QDialogButtonBox(parent=self)
        buttonBox.setOrientation(QtCore.Qt.Horizontal) # 设置为水平方向
        buttonBox.addButton(_translate("Dialog", "提交", None),buttonBox.AcceptRole)
        buttonBox.addButton(_translate("Dialog", "取消", None),buttonBox.RejectRole)
        # buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |QtGui.QDialogButtonBox.Ok) # 确定和取消两个按钮
        buttonBox.accepted.connect(self.accept) # 确定
        buttonBox.rejected.connect(self.reject) # 取消

        # self.pushButton_1 = QtGui.QPushButton(parent=self)
        # self.pushButton_1.setGeometry(QtCore.QRect(210, 400, 75, 23))
        # self.pushButton_1.setText(_translate("Dialog", "提交", None))
        #
        # self.pushButton_2 = QtGui.QPushButton(parent=self)
        # self.pushButton_2.setGeometry(QtCore.QRect(330, 400, 75, 23))
        # self.pushButton_2.setText(_translate("Dialog", "取消", None))
        # grid.addWidget(self.pushButton_1,8,2,1,1)
        # grid.addWidget(self.pushButton_2,8,3,1,1)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(grid)
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout.addItem(spacerItem)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    # -------------------Close Event Method----------------------

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Close Message',
                      "Are you sure to quit?", QtGui.QMessageBox.Yes |
                       QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
          event.accept()
        else:
          event.ignore()
