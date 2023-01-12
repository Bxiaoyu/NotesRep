#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
=================================================
@Project -> File   ：testDemo -> main
@IDE    ：PyCharm
@Author ：sky
@Date   ：2023/1/9 22:31
@Desc   ：
==================================================
'''
import sys
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QApplication, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QPushButton, QStackedWidget, QListWidget
from PySide6.QtCore import Qt

# 表格初始行数和列数
TABLE_ROW = 0
TABLE_COLUMN = 5

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("XXXDemo")
        self.resize(700, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 创建表格，设置列数，设置表头
        self.table_widget = QTableWidget(TABLE_ROW, TABLE_COLUMN)
        table_header = [
            {"text":"学号", "width":120},
            {"text":"姓名", "width":120},
            {"text":"性别", "width":60},
            {"text":"联系方式", "width":180},
            {"text":"操作", "width":120}
        ]

        for index, info in enumerate(table_header):
            item = QTableWidgetItem()
            item.setText(info['text'])
            self.table_widget.setHorizontalHeaderItem(index, item)
            self.table_widget.setColumnWidth(index, info['width'])

        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        self.init_table_data()

    def init_table_data(self):
        table_data = [
            ["1001", "张三", "男", "18317881856"],
            ["1002", "韩梅梅", "女", "15980537345"],
            ["1003", "李明", "男", "13988037865"],
            ["1004", "苏小雨", "女", "17888679542"],
        ]

        current_row_count = self.table_widget.rowCount()
        for item_list in table_data:
            self.table_widget.insertRow(current_row_count)
            for index , ele in enumerate(item_list):
                cell = QTableWidgetItem(str(ele))
                self.table_widget.setItem(current_row_count, index, cell)
                # 设置单元格不可更改
                cell.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            # 添加操作单元格按钮（修改、删除）
            self.add_tableItem_pushButton(current_row_count, TABLE_COLUMN-1)

            current_row_count += 1


    def add_tableItem_pushButton(self, row:int, column:int):
        """
        添加表格单元格中按钮
        :param row: 行
        :param column: 列
        :return:
        """
        btn_modify = QPushButton("修改")
        btn_modify.clicked.connect(self.event_modify_click)
        btn_modify.setStyleSheet("""text-align: center;
        background-color: NavajoWhite;
        height:30px;
        font:13px
        """)

        btn_delete = QPushButton("删除")
        btn_delete.clicked.connect(self.event_delete_click)
        btn_delete.setStyleSheet("""text-align: center;
        background-color: LightCoral;
        height:30px;
        font:13px
        """)

        cell_widget = QWidget()
        opt_layout = QHBoxLayout()
        opt_layout.addWidget(btn_modify)
        opt_layout.addWidget(btn_delete)
        opt_layout.setContentsMargins(5, 2, 5, 2)
        cell_widget.setLayout(opt_layout)
        self.table_widget.setCellWidget(row, column, cell_widget)

    def event_delete_click(self):
        button = self.sender()
        if button:
            # 获取按钮所在的行号
            row = self.table_widget.indexAt(button.parent().pos()).row()
            self.table_widget.removeRow(row)
            self.table_widget.selectRow(row)

    def event_modify_click(self):
        button = self.sender()
        if button:
            # 获取按钮所在的行号
            row = self.table_widget.indexAt(button.parent().pos()).row()
            self.table_widget.selectRow(row)
            print(row)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

def main_2():
    import sqlite3
    import os
    conn = sqlite3.connect(os.path.join('db', 'testdb.db'))

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM t_student_info WHERE id={2};")
    res = cursor.fetchall()
    for item in res:
        print(item)
    conn.close()


if __name__ == "__main__":
    main_2()