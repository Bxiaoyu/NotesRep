# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: ComboCheckBox
@Author  : sky
@Date    : 2023/2/7 15:09
@Desc    : 用户添加与修改选择框设置类

"""
from PySide6.QtWidgets import QWidget, QComboBox, QLineEdit, QListView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QMouseEvent
from PySide6.QtCore import Qt

global classIds
classIds = ''

# 全选与单选的绑定（没有这个会导致勾选数据错乱）,装饰器
def show_text(function):
    def wrapped(self, *args, **kwargs):
        global classIds
        if self.vars["showTextLock"]:
            self.vars["showTextLock"] = False
            result = function(self, *args, **kwargs)
            items = self.get_selected()
            l = len(items)
            l_ = self.vars["listViewModel"].rowCount() - 1
            self.vars["listViewModel"].item(0).setCheckState(
                Qt.CheckState.Checked if l == l_ else Qt.CheckState.Unchecked if l == 0 else Qt.CheckState.PartiallyChecked
            )
            self.vars["lineEdit"].setText(
                "(全选)" if l == l_ else "(无选择)" if l == 0 else ";".join((item.text() for item in items))
            )
            self.vars["showTextLock"] = True

            classIds = "" if l == 0 else ",".join((item.text().split('.')[0] for item in items))
        else:
            result = function(self, *args, **kwargs)
        return result
    return wrapped


# 选项的渲染和选择后的显示
class QComboCheckBox(QComboBox):
    class MyListView(QListView):
        def __init__(self, parent: QWidget=None, vars=None):
            super().__init__(parent)
            self.vars = vars

        def mousePressEvent(self, event:QMouseEvent):
            self.vars["lock"] = False
            super().mousePressEvent(event)

        def mouseDoubleClickEvent(self, event:QMouseEvent):
            self.vars["lock"] = False
            super().mouseDoubleClickEvent(event)

    def __init__(self, parent:QWidget=None):
        super(QComboCheckBox, self).__init__(parent)
        self.vars = dict()
        self.vars["lock"] = True
        self.vars["showTextLock"] = True
        # 装饰器锁，避免批量操作时重复改变lineEdit的显示
        self.vars["lineEdit"] = QLineEdit(self)
        self.vars["lineEdit"].setReadOnly(True)
        self.vars["listView"] = self.MyListView(self, self.vars)
        self.vars["listViewModel"] = QStandardItemModel(self)
        self.setModel(self.vars["listViewModel"])
        self.setView(self.vars["listView"])
        self.setLineEdit(self.vars["lineEdit"])

        self.activated.connect(self.__show_selected)

        self.add_item("(全选)")

    @show_text
    def add_item(self, text:"str", flag=False):
        # 根据文本添加子项
        item = QStandardItem()
        item.setText(text)
        item.setCheckable(True)
        if flag:
            item.setCheckState(Qt.CheckState.Checked)
        self.vars["listViewModel"].appendRow(item)

    # 根据文本查找子项
    def find_text(self, text:"str"):
        tempList = self.vars["listViewModel"].findItems(text)
        tempList.pop(0) if tempList and tempList[0].row() == 0 else tempList
        return tempList

    # 获取班级ids
    def get_class_text(self):
        return classIds

    # 全选
    @show_text
    def select_all(self):
        for row in range(0, self.vars["listViewModel"].rowCount()):
            self.vars["listViewModel"].item(row).setCheckState(Qt.CheckState.Checked)

    # 全不选
    @show_text
    def select_clear(self):
        for row in range(0, self.vars["listViewModel"].rowCount()):
            self.vars["listViewModel"].item(row).setCheckState(Qt.CheckState.Unchecked)

    # 获取当前选择的子项
    def get_selected(self):
        items = []
        for row in range(1, self.vars["listViewModel"].rowCount()):
            item = self.vars["listViewModel"].item(row)
            if item.checkState() == Qt.CheckState.Checked:
                items.append(item)
        return items

    # 显示选中的选项
    @show_text
    def __show_selected(self, index):
        # 未被选中
        if not self.vars["lock"]:
            # 选中全选
            if index == 0:
                if self.vars["listViewModel"].item(0).checkState() == Qt.CheckState.Checked:
                    self.select_clear()
                else:
                    self.select_all()
            # 选中其它
            else:
                self.__select_reverse(index)

            self.vars['lock'] = True

    # 选中一个项
    def __select_reverse(self, row:"int"):
        item = self.vars["listViewModel"].item(row)
        item.setCheckState(Qt.CheckState.Unchecked if item.checkState() == Qt.CheckState.Checked else Qt.CheckState.Checked)

if __name__ == "__main__":
    pass
