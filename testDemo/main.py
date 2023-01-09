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
from PySide6.QtWidgets import QPushButton, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("XXXDemo")
        self.resize(700, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 创建表格，设置列数，设置表头
        self.table_widget = QTableWidget(0, 5)
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
        current_row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(current_row_count)
        id_cell = QTableWidgetItem("1001")
        self.table_widget.setItem(current_row_count, 0, id_cell)

        name_cell = QTableWidgetItem("张三")
        self.table_widget.setItem(current_row_count, 1, name_cell)

        gender_cell = QTableWidgetItem("男")
        self.table_widget.setItem(current_row_count, 2, gender_cell)

        contact_cell = QTableWidgetItem("18317881856")
        self.table_widget.setItem(current_row_count, 3, contact_cell)

        btn_modify = QPushButton("修改")
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
        opt_layout.setContentsMargins(5,2,5,2)
        cell_widget.setLayout(opt_layout)
        self.table_widget.setCellWidget(current_row_count, 4, cell_widget)

        current_row_count += 1

    def event_delete_click(self):
        button = self.sender()
        if button:
            row = self.table_widget.indexAt(button.parent().pos()).row()
            self.table_widget.removeRow(row)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()