# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: EditAdmin
@Author  : sky
@Date    : 2023/2/8 11:08
@Desc    : 修改用户界面设计与功能实现

"""
import sql_table

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt, QRect
from ComboCheckBox import QComboCheckBox
from db import DBSESSION


class EditAdmin(object):
    # 界面设计
    def setup_ui(self, Form, adminId):
        Form.setObjectName("Form")
        Form.resize(360, 279)
        self.label = QLabel(Form)
        self.label.setGeometry(QRect(40, 40, 54, 12))
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                Qt.AlignmentFlag.AlignVCenter)
        self.label.setObjectName("label")

        admin = DBSESSION.query(sql_table.TAdmin).filter(sql_table.TAdmin.a_id == adminId).first()
        self.textEdit = QLineEdit(Form)
        self.textEdit.setGeometry(QRect(100, 30, 181, 31))
        self.textEdit.setText(admin.a_username)
        self.textEdit.setObjectName("textEdit")

        self.textEdit_2 = QLineEdit(Form)
        self.textEdit_2.setGeometry(QRect(100, 80, 181, 31))
        self.textEdit_2.setText(admin.a_mark)
        self.textEdit_2.setObjectName("textEdit_2")

        self.label_2 = QLabel(Form)
        self.label_2.setGeometry(QRect(40, 90, 54, 12))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing |
                                  Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")

        self.textEdit_3 = QComboCheckBox(Form)

        class_list = []
        try:
            if admin.a_classid != '0':
                for data in admin.a_classid.split(','):
                    class_list.append(data)
        except Exception as e:
            pass

        # 获取班级列表（供老师选择来管理）
        temp_class_list = DBSESSION.query(sql_table.TClass).all()
        for item in temp_class_list:
            self.textEdit_3.add_item(f"{item.c_id}.{item.c_name}",
                                     flag=admin.a_classid == '0' or str(item.c_id) in class_list)
        self.textEdit_3.setGeometry(QRect(100, 130, 181, 31))
        self.textEdit_3.setObjectName("textEdit_3")

        self.label_3 = QLabel(Form)
        self.label_3.setGeometry(QRect(23, 140, 71, 20))
        self.label_3.setObjectName("label_3")


if __name__ == "__main__":
    pass
