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
from PySide6.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from ComboCheckBox import QComboCheckBox
from db import DBSESSION, md5


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

        self.pushButton = QPushButton(Form)
        self.pushButton.setGeometry(QRect(150, 220, 75, 23))
        self.pushButton.setObjectName("pushButton")

        # 提交按钮
        self.pushButton.clicked.connect(lambda: self.updateAdmin(adminId, Form))

        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setGeometry(QRect(230, 220, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        # 取消按钮
        self.pushButton_2.clicked.connect(lambda: Form.hide())

        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setGeometry(QRect(10, 220, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")

        # 重置密码按钮
        self.pushButton_3.clicked.connect(lambda: self.resetPassw(adminId, Form))

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    # 重新翻译（针对性修改）
    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "编辑角色"))
        self.label.setText(_translate("Form", "用户名："))
        self.label_2.setText(_translate("Form", "备注："))
        self.label_3.setText(_translate("Form", "可管理班级："))
        self.pushButton.setText(_translate("Form", "提交"))
        self.pushButton_2.setText(_translate("Form", "取消"))
        self.pushButton_3.setText(_translate("Form", "重置密码"))

    # 修改用户名
    def updateAdmin(self, adminId, Form):
        username = self.textEdit.text()
        mark = self.textEdit_2.text()
        classids = self.textEdit_3.get_class_text()
        try:
            admin = DBSESSION.query(sql_table.TAdmin).filter(sql_table.TAdmin.a_id == adminId).update(
                {"a_username":f"{username}","a_mark":f"{mark}","a_classid":f"{classids}"})
            DBSESSION.commit()
            QMessageBox.about(Form, "成功", "编辑成功！请刷新数据列表。")
        except Exception as e:
            DBSESSION.rollback()
            QMessageBox.about(Form, "失败", "编辑失败!")
        Form.close()

    # 重置密码
    def resetPassw(self, adminId, Form):
        text, okPressed = QInputDialog.getText(Form, "重置密码", "新密码:", QLineEdit.EchoMode.Normal, '')
        if okPressed:
            try:
                DBSESSION.query(sql_table.TAdmin).filter(sql_table.TAdmin.a_id == adminId).update(
                    {"a_password":f"{md5(text)}"})
                DBSESSION.commit()
                QMessageBox.about(Form, "成功", "重置密码成功！")
            except Exception as  e:
                DBSESSION.rollback()
                QMessageBox.about(Form, "失败", "重置密码失败！")
            Form.close()


def main():
    import sys
    app = QApplication(sys.argv)
    aw = EditAdmin()
    window = QMainWindow()
    aw.setup_ui(window, 1)
    window.show()
    window.setWindowTitle("学生管理系统-修改用户")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()