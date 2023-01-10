# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: dialog
@Author  : sky
@Date    : 2023/1/10 15:24
@Desc    :

"""
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QApplication, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit, QTextEdit
from PySide6.QtCore import Qt, Slot

# 表格初始行数和列数
TABLE_ROW = 0
TABLE_COLUMN = 5

class ManagerCenterWidget(QWidget):
    def __init__(self):
        super(ManagerCenterWidget, self).__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 1. 创建头部搜索框
        search_layout = QHBoxLayout()
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("请输入搜索内容")
        btn_search = QPushButton("搜索")
        search_layout.addWidget(self.search_line_edit)
        search_layout.addWidget(btn_search)

        # 2. 创建中间表格
        table_layout = QVBoxLayout()
        # 创建表格，设置列数，设置表头
        self.table_widget = QTableWidget(TABLE_ROW, TABLE_COLUMN)
        table_layout.addWidget(self.table_widget)
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

        self.init_table_data()

        # 3. 创建翻页框
        next_layout = QHBoxLayout()
        btn_header_page = QPushButton("首页")
        btn_previous_page = QPushButton("上一页")
        btn_next_page = QPushButton("下一页")
        btn_last_page = QPushButton("尾页")
        self.number_label = QLabel("0/0")
        self.page_number_line_edit = QLineEdit()
        self.page_number_line_edit.setPlaceholderText("页数")
        btn_skip = QPushButton("跳转")
        next_layout.addStretch()
        next_layout.addWidget(btn_header_page)
        next_layout.addWidget(btn_previous_page)
        next_layout.addWidget(self.number_label)
        next_layout.addWidget(btn_next_page)
        next_layout.addWidget(btn_last_page)
        next_layout.addWidget(self.page_number_line_edit)
        next_layout.addWidget(btn_skip)
        # next_layout.addStretch()

        # 4. 创建底部菜单栏
        footer_layout = QHBoxLayout()
        self.status_label = QLabel("状态")
        btn_add = QPushButton("添加")
        btn_import = QPushButton("导入")
        btn_export = QPushButton("导出")
        footer_layout.addWidget(self.status_label)
        footer_layout.addStretch()
        footer_layout.addWidget(btn_add)
        footer_layout.addWidget(btn_import)
        footer_layout.addWidget(btn_export)

        layout.addLayout(search_layout)
        layout.addLayout(table_layout)
        layout.addLayout(next_layout)
        layout.addLayout(footer_layout)

        self.setLayout(layout)

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

class DataCenterWidget(QWidget):
    def __init__(self):
        super(DataCenterWidget, self).__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.txt_edit = QTextEdit()
        layout.addWidget(self.txt_edit)

        self.setLayout(layout)

if __name__ == "__main__":
    pass
