# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: dialog
@Author  : sky
@Date    : 2023/1/10 15:24
@Desc    :

"""
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QApplication, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit, QTextEdit, QDialog, QMenu, QMessageBox, QComboBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal, Slot

# 表格初始行数和列数
TABLE_ROW = 0
TABLE_COLUMN = 5

class ManagerCenterWidget(QWidget):
    def __init__(self):
        super(ManagerCenterWidget, self).__init__()
        # 1. 初始化界面
        self.init_ui()
        # 2. 读取数据库数据，并更新到表格
        self._read_data_from_db()

    def _read_data_from_db(self):
        """
        从数据库读取数据
        :return:
        """
        from utils.threads import SqlSelectTaskThread
        sql = f"SELECT account,name,gender,phone FROM t_student_info;"
        newTask = SqlSelectTaskThread(sql, self)
        newTask.sig_finished.connect(self.event_receive_data)
        newTask.start()

    @Slot(list)
    def event_receive_data(self, data_list:list):
        """
        接收数据库数据并更新到表格
        :param data_list: 数据列表
        :return:
        """
        self.init_table_data(data_list)


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
            {"text":"账号", "width":120},
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
        btn_add.clicked.connect(self.event_add_click)
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

        # 5. 设置右键菜单功能
        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.event_table_right_mouse_menu)

    def insert_table_row(self, row_index:int):
        """
        表格插入一行
        :param row_index:
        :return:
        """
        self.table_widget.insertRow(row_index)
        # 添加操作单元格按钮（修改、删除）
        self.add_tableItem_pushButton(row_index, TABLE_COLUMN - 1)

    def insert_table_row_data(self, row:int, column:int, content:str):
        """
        插入单元格数据
        :param row:
        :param column:
        :param data_list:
        :return:
        """
        cell = QTableWidgetItem(content)
        self.table_widget.setItem(row, column, cell)
        # 设置的单元格不可更改
        cell.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)


    def init_table_data(self, data_list):
        """
        初始化表格数据
        :param data_list: 数据列表
        :return:
        """
        current_row_count = self.table_widget.rowCount()
        for item_list in data_list:
            self.insert_table_row(current_row_count)
            for index , ele in enumerate(item_list):
                if index == 2:
                    ele = "男" if ele == 1 else "女"
                self.insert_table_row_data(current_row_count, index, ele)

            current_row_count += 1

    def add_tableItem_pushButton(self, row:int, column:int):
        """
        添加表格单元格中按钮
        :param row: 行
        :param column: 列
        :return:
        """
        btn_modify = QPushButton("修改")
        btn_modify.clicked.connect(self.event_table_modify_click)
        btn_modify.setStyleSheet("""text-align: center;
        background-color: NavajoWhite;
        height:30px;
        font:13px
        """)

        btn_delete = QPushButton("删除")
        btn_delete.clicked.connect(self.event_table_delete_click)
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

    def event_table_delete_click(self):
        button = self.sender()
        if button:
            # 获取按钮所在的行号
            row = self.table_widget.indexAt(button.parent().pos()).row()
            self.table_widget.removeRow(row)
            self.table_widget.selectRow(row)

    def event_table_modify_click(self):
        button = self.sender()
        if button:
            # 获取按钮所在的行号
            row = self.table_widget.indexAt(button.parent().pos()).row()
            self.table_widget.selectRow(row)

            dialog = ModifyDialog(self, row)
            dialog.sig_update.connect(self.event_start_update)
            dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
            dialog.exec()

    def event_add_click(self):
        """
        添加事件响应函数
        :return:
        """
        # 获取表格的所有行
        row_count = self.table_widget.rowCount()
        dialog = AddDialog(self, row_count)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.exec()

    def event_table_right_mouse_menu(self, pos):
        """
        右键菜单显示事件
        :param pos:
        :return:
        """
        # 1. 获取所有选中的行和所有选中的单元格
        selected_row_list = self.table_widget.selectionModel().selectedRows()
        selected_row_list.reverse()  # 删除操作时要对行数组进行反转，否则序号会出问题
        selected_item_list = self.table_widget.selectedItems()
        if len(selected_item_list) == 0:  # 未选中任何内容则不执行操作
            return

        # 2. 创建右键菜单
        menu = QMenu()
        copy_action = QAction("复制")
        delete_action = QAction("删除")
        # 根据是否有选中行来设置删除菜单的是否可用
        delete_action.setEnabled(False) if len(selected_row_list) <= 0 else delete_action.setEnabled(True)
        menu.addAction(copy_action)
        menu.addAction(delete_action)

        # 3. 选中了哪个操作
        action = menu.exec(self.table_widget.mapToGlobal(pos))

        if action == copy_action:
            # 将选中的单元格内容复制到剪贴板
            clipboard = QApplication.clipboard()

            # 选择范围
            selected_count = len(self.table_widget.selectedRanges())
            top_row = -1
            bottom_row = -1
            left_col = -1
            right_col = -1
            for i in range(0, selected_count):
                top_row = self.table_widget.selectedRanges()[i].topRow()
                bottom_row = self.table_widget.selectedRanges()[i].bottomRow()
                left_col = self.table_widget.selectedRanges()[i].leftColumn()
                right_col = self.table_widget.selectedRanges()[i].rightColumn()


            # 组装数据格式
            tmp_str = ''
            for i in range(top_row, bottom_row+1):
                for j in range(left_col, right_col+1):
                    if self.table_widget.item(i, j):
                        txt = self.table_widget.item(i,j).text()
                        tmp_str += txt
                        tmp_str += '\t'
                tmp_str = tmp_str[:len(tmp_str)-1]  # 去除最后一个字符
                tmp_str += '\n'
            clipboard.setText(tmp_str)



        if action == delete_action:
            # 删除选中的行
            ret = QMessageBox.question(self, "提示", "确认删除?", QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            if ret == QMessageBox.StandardButton.Ok: # 确认删除
                for rowItem in selected_row_list:
                    self.table_widget.removeRow(rowItem.row())

    @Slot(str, str, str, int, str)
    def event_start_update(self, old_account:str, account:str, name:str, gender:int, contact:str):
        """
        接收线程执行消息
        :param status:
        :return:
        """
        from utils.threads import SqlUpdateTaskThread
        sql = f"UPDATE t_student_info SET account='{account}',name='{name}',gender={gender},phone='{contact}' WHERE account='{old_account}';"
        newTask = SqlUpdateTaskThread(sql, self)
        newTask.sig_finished.connect(self.message_callback)
        newTask.start()

    @Slot(str)
    def message_callback(self, message:str):
        """
        显示操作反馈信息
        :param message:
        :return:
        """
        self.status_label.setText(message)

class DataCenterWidget(QWidget):
    def __init__(self):
        super(DataCenterWidget, self).__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.txt_edit = QTextEdit()
        layout.addWidget(self.txt_edit)

        self.setLayout(layout)
        
        
class ModifyDialog(QDialog):
    # 信号
    sig_update = Signal(str, str, str, int, str)

    def __init__(self, window:ManagerCenterWidget, row_index:int, *args, **kwargs):
        super(ModifyDialog, self).__init__(*args, **kwargs)
        self.window = window
        self.row_index = row_index

        self._account = ""
        self._name = ""
        self._gender = -1
        self._contact = ""

        self.setWindowTitle("信息更改")
        self.resize(300, 270)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        table_layout = QVBoxLayout()
        account_label = QLabel("账号:")
        self.account_line_edit = QLineEdit()
        name_label = QLabel("姓名:")
        self.name_line_edit = QLineEdit()
        gender_label = QLabel("性别:")
        self.gender_combox = QComboBox()
        self.gender_combox.addItems(["男","女"])
        contact_label = QLabel("联系方式：")
        self.contact_line_edit = QLineEdit()
        table_layout.addWidget(account_label)
        table_layout.addWidget(self.account_line_edit)
        table_layout.addWidget(name_label)
        table_layout.addWidget(self.name_line_edit)
        table_layout.addWidget(gender_label)
        table_layout.addWidget(self.gender_combox)
        table_layout.addWidget(contact_label)
        table_layout.addWidget(self.contact_line_edit)

        footer_layout = QHBoxLayout()
        btn_close = QPushButton("关闭")
        btn_close.clicked.connect(self.event_close_click)
        btn_save = QPushButton("保存")
        btn_save.clicked.connect(self.event_save_click)
        footer_layout.addStretch()
        footer_layout.addWidget(btn_close)
        footer_layout.addWidget(btn_save)

        layout.addLayout(table_layout)
        layout.addLayout(footer_layout)

        self.setLayout(layout)

        self.init_selected_data()

    def init_selected_data(self):
        """
        初始化对话框数据
        :return:
        """
        self._account = self.window.table_widget.item(self.row_index, 0).text().strip()
        self.account_line_edit.setText(self._account)
        self._name = self.window.table_widget.item(self.row_index, 1).text().strip()
        self.name_line_edit.setText(self._name)
        self._gender = self.window.table_widget.item(self.row_index, 2).text().strip()
        if self._gender == "男":
            self.gender_combox.setCurrentIndex(0)
        else:
            self.gender_combox.setCurrentIndex(1)
        self._contact = self.window.table_widget.item(self.row_index, 3).text().strip()
        self.contact_line_edit.setText(self._contact)

    def event_close_click(self):
        """
        关闭窗口
        :return:
        """
        self.close()

    def event_save_click(self):
        account = self.account_line_edit.text().strip()
        name = self.name_line_edit.text().strip()
        gender = 1 if self.gender_combox.currentText() == "男" else 0
        contact = self.contact_line_edit.text().strip()

        # 有数据改动才写入更新数据
        if account != self._account or name != self._name or self.gender_combox.currentText().strip() != self._gender or contact != self._contact:
            # 更新表格数据
            self.window.table_widget.item(self.row_index, 0).setText(account)
            self.window.table_widget.item(self.row_index, 1).setText(name)
            self.window.table_widget.item(self.row_index, 2).setText(self.gender_combox.currentText().strip())
            self.window.table_widget.item(self.row_index, 3).setText(contact)

            self.sig_update.emit(self._account, account, name, gender, contact)

        self.close()


class AddDialog(QDialog):
    def __init__(self, window:ManagerCenterWidget, row_index:int, *args, **kwargs):
        super(AddDialog, self).__init__(*args, **kwargs)
        self._window = window
        self._row_index = row_index

        self.setWindowTitle("添加人员")
        self.resize(300, 270)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        table_layout = QVBoxLayout()
        account_label = QLabel("账号:")
        self.account_line_edit = QLineEdit()
        name_label = QLabel("姓名:")
        self.name_line_edit = QLineEdit()
        gender_label = QLabel("性别:")
        self.gender_combox = QComboBox()
        self.gender_combox.addItems(["男","女"])
        contact_label = QLabel("联系方式：")
        self.contact_line_edit = QLineEdit()
        table_layout.addWidget(account_label)
        table_layout.addWidget(self.account_line_edit)
        table_layout.addWidget(name_label)
        table_layout.addWidget(self.name_line_edit)
        table_layout.addWidget(gender_label)
        table_layout.addWidget(self.gender_combox)
        table_layout.addWidget(contact_label)
        table_layout.addWidget(self.contact_line_edit)

        footer_layout = QHBoxLayout()
        self._status_label = QLabel("状态")
        btn_close = QPushButton("关闭")
        btn_close.clicked.connect(self.event_close_click)
        btn_save = QPushButton("保存")
        btn_save.clicked.connect(self.event_save_click)
        footer_layout.addWidget(self._status_label)
        footer_layout.addStretch()
        footer_layout.addWidget(btn_close)
        footer_layout.addWidget(btn_save)

        layout.addLayout(table_layout)
        layout.addLayout(footer_layout)

        self.setLayout(layout)

    def event_close_click(self):
        """
        关闭且不保存
        :return:
        """
        self.close()

    def event_save_click(self):
        """
        保存数据
        :return:
        """
        account = self.account_line_edit.text().strip()
        name = self.name_line_edit.text().strip()
        gender = 1 if self.gender_combox.currentText() == "男" else 0
        contact = self.contact_line_edit.text().strip()

        if account != "" and name != "" and gender != None and contact != "":
            self._window.insert_table_row(self._row_index)
            self._window.insert_table_row_data(self._row_index, 0, account)
            self._window.insert_table_row_data(self._row_index, 1, name)
            self._window.insert_table_row_data(self._row_index, 2, self.gender_combox.currentText().strip())
            self._window.insert_table_row_data(self._row_index, 3, contact)

            from utils.threads import SqlUpdateTaskThread
            sql = f"INSERT INTO t_student_info (account,name,gender,phone) VALUES('{account}','{name}',{gender},'{contact}');"
            newTask = SqlUpdateTaskThread(sql, self)
            newTask.sig_finished.connect(self.message_callback)
            newTask.start()

            self.account_line_edit.clear()
            self.name_line_edit.clear()
            self.contact_line_edit.clear()

        else:
            QMessageBox.warning(self, "警告", "输入内容不能为空!")


    @Slot(str)
    def message_callback(self, message:str):
        self._status_label.setText(message.strip())
        self._window.status_label.setText(message.strip())


if __name__ == "__main__":
    pass
