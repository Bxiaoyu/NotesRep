# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: AddAdmin
@Author  : sky
@Date    : 2023/2/7 15:55
@Desc    : 添加用户界面设计与功能实现

"""
import sys

import sql_table
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ComboCheckBox import QComboCheckBox
from db import DBSESSION, md5


class AddAdmin(object):
    def setup_ui(self, Form):
        Form.setObjectName("Form")
        Form.resize(360, 279)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 40, 54, 12))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing |
                                QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label.setObjectName("label")

        self.textEdit = QtWidgets.QLineEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(100, 30, 181, 31))
        self.textEdit.setObjectName("textEdit")

        self.label0 = QtWidgets.QLabel(Form)
        self.label0.setGeometry(QtCore.QRect(40, 90, 54, 12))
        self.label0.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing |
                                 QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label0.setObjectName("label")

        self.textEdit0 = QtWidgets.QLineEdit(Form)
        self.textEdit0.setGeometry(QtCore.QRect(100, 80, 181, 31))
        self.textEdit0.setObjectName("textEdit")

        self.textEdit_2 = QtWidgets.QLineEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(100, 130, 181, 31))
        self.textEdit_2.setObjectName("textEdit_2")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 140, 54, 12))
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing |
                                 QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")

        class_list = DBSESSION.query(sql_table.TClass).all()
        self.textEdit_3 = QComboCheckBox(Form)
        for item in class_list:
            self.textEdit_3.add_item(f"{item.c_id}.{item.c_name}", flag=False)
        self.textEdit_3.setGeometry(QtCore.QRect(100, 180, 181, 31))
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(23, 190, 71, 20))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(110, 240, 75, 23))
        self.pushButton.setObjectName("pushButton")

        # 提交按钮
        self.pushButton.clicked.connect(lambda : self.addAdmin(Form))

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 240, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        # 取消按钮
        self.pushButton_2.clicked.connect(lambda: Form.close())

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "新增角色"))
        self.label.setText(_translate("Form", "用户名："))
        self.label0.setText(_translate("Form", "密码："))
        self.label_2.setText(_translate("Form", "备注："))
        self.label_3.setText(_translate("Form", "可管理班级："))
        self.pushButton.setText(_translate("Form", "提交"))
        self.pushButton_2.setText(_translate("Form", "取消"))

    # 功能实现
    def addAdmin(self, Form):
        username = self.textEdit.text().strip()
        password = self.textEdit0.text().strip()
        mark = self.textEdit_2.text().strip()
        classids = self.textEdit_3.get_class_text()
        try:
            DBSESSION.add(sql_table.TAdmin(username, md5(password), mark, classids))
            DBSESSION.commit()
            QMessageBox.about(Form, "成功", "添加成功！请刷新列表数据。")
        except Exception as e:
            DBSESSION.rollback()
            print(e)
            QMessageBox.about(Form, "失败", "添加失败!")
        Form.close()

# 测试
def main():
    app = QApplication(sys.argv)
    aw = AddAdmin()
    window = QMainWindow()
    aw.setup_ui(window)
    window.show()
    window.setWindowTitle("学生管理系统-新增用户")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
