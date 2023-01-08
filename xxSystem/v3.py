# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: mainwindow
@Author  : sky
@Date    : 2023/1/5 11:15
@Desc    :

"""
import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMenu
from PySide6.QtWidgets import QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, Slot, QThread
from utils.dialog import LogDialog

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

STATUS_MAPPING = {
    0:"初始化中",
    1:"待执行",
    2:"正在执行",
    3:"完成并提醒",
    10:"异常并停止",
    11:"初始化失败",
}

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 需要调用的控件
        self.txt_asin:QLineEdit = None
        self.table_widget:QTableWidget = None

        # 窗体标题和尺寸
        self.setWindowTitle('NB的xx系统')

        # 窗体尺寸
        self.resize(1228, 450)

        # 窗体的位置
        cp = QGuiApplication.primaryScreen().size()
        size = self.geometry()
        self.move((cp.width() - size.width()) / 2,
                  (cp.height() - size.height()) / 2)

        # 创建主布局
        layout = QVBoxLayout()
        layout.addLayout(self.init_header())
        layout.addLayout(self.init_form())
        layout.addLayout(self.init_table())
        layout.addLayout(self.init_footer())

        # 增加底部弹簧
        # layout.addStretch()
        # 添加主布局到窗体
        self.setLayout(layout)

    def init_header(self):
        # 1. 创建顶部布局
        header_layout = QHBoxLayout()
        # 1.1 创建按钮，加入header_layout
        btn_start = QPushButton("开始")
        btn_start.clicked.connect(self.event_start_click)
        header_layout.addWidget(btn_start)

        btn_stop = QPushButton("停止")
        btn_stop.clicked.connect(self.event_stop_click)
        header_layout.addWidget(btn_stop)

        header_layout.addStretch()

        return header_layout

    def init_form(self):
        # 2. 创建搜索框布局
        form_layout = QHBoxLayout()

        # 2.1 添加输入框
        txt_asin = QLineEdit()
        txt_asin.setPlaceholderText("请输入商品ID和价格，例如：B0818JJQQ8=88")
        self.txt_asin = txt_asin
        form_layout.addWidget(txt_asin)

        # 2.2 添加按钮
        btn_add = QPushButton("添加")
        btn_add.clicked.connect(self.event_add_click)
        form_layout.addWidget(btn_add)

        return form_layout

    def init_table(self):
        # 3. 创建中间表格布局
        table_layout = QHBoxLayout()

        # 3.1 创建表格
        table_widget = QTableWidget(0, 8)
        table_header = [
            {"field":"asin", "text":"ASIN", "width":120},
            {"field":"title", "text":"标题", "width":150},
            {"field":"url", "text":"URL", "width":400},
            {"field":"price", "text":"底价", "width":100},
            {"field":"success", "text":"成功次数", "width":100},
            {"field":"error", "text":"503次数", "width":100},
            {"field":"status", "text":"状态", "width":100},
            {"field":"frequency", "text":"频率 (N秒/次)", "width":100},
        ]

        for id, info in enumerate(table_header):
            item = QTableWidgetItem()
            item.setText(info['text'])
            table_widget.setHorizontalHeaderItem(id, item)
            table_widget.setColumnWidth(id, info['width'])

        # 初始化数据
        self.init_table_data(table_widget)

        # 开启右键功能，在表格中点击右键时，自动触发相应函数
        table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        table_widget.customContextMenuRequested.connect(self.event_table_right_menu)

        table_layout.addWidget(table_widget)

        self.table_widget = table_widget

        return table_layout

    def init_footer(self):
        # 1. 创建底部菜单栏布局
        footer_layout = QHBoxLayout()

        self.label_status = QLabel("未检测", self)
        footer_layout.addWidget(self.label_status)

        footer_layout.addStretch()

        btn_reset = QPushButton("重新初始化")
        btn_reset.clicked.connect(self.event_reset_click)
        footer_layout.addWidget(btn_reset)

        btn_recheck = QPushButton("重新检测")
        footer_layout.addWidget(btn_recheck)

        btn_reset_count = QPushButton("次数清零")
        btn_reset_count.clicked.connect(self.event_reset_count_click)
        footer_layout.addWidget(btn_reset_count)

        btn_delete = QPushButton("删除检测项")
        btn_delete.clicked.connect(self.event_delete_click)
        footer_layout.addWidget(btn_delete)

        btn_alert = QPushButton("SMTP报警配置")
        btn_alert.clicked.connect(self.event_alert_click)
        footer_layout.addWidget(btn_alert)

        btn_proxy = QPushButton("代理IP")
        btn_proxy.clicked.connect(self.event_proxy_click)
        footer_layout.addWidget(btn_proxy)

        return footer_layout

    def init_table_data(self, tableWidget:QTableWidget):
        """
        初始化表格数据
        :return:
        """
        import json
        file_path = os.path.join(BASE_DIR, "db", "db.json")
        with open(file_path, mode='r', encoding='utf-8') as f:
            data = f.read()
        data_list = json.loads(data)

        current_row_count = tableWidget.rowCount()
        for row_list in data_list:
            tableWidget.insertRow(current_row_count)
            for index, ele in enumerate(row_list):
                ele = STATUS_MAPPING[ele] if index == 6 else ele
                cell = QTableWidgetItem(str(ele))
                if index in [0,4,5,6]:
                    # 设置这几列不可修改
                    cell.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                tableWidget.setItem(current_row_count, index, cell)
            current_row_count += 1

    # 事件响应函数
    def event_add_click(self):
        """
        添加事件响应函数
        :return:
        """
        # 1. 获取输入框内容
        text = self.txt_asin.text().strip()
        if not text:
            QMessageBox.warning(self, "错误", "商品的ASIN输入错误!")
            return

        asin, price = text.split("=")
        if not asin or not price:
            QMessageBox.warning(self, "错误", "商品ASIN或价格为空!")
            return
        price = float(price)

        # 2. 加入到表格中（型号，底价）
        new_row_list = [asin, "", "", price, 0, 0, 0, 5]

        current_row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(current_row_count)
        for index, ele in enumerate(new_row_list):
            ele = STATUS_MAPPING[ele] if index == 6 else ele
            cell = QTableWidgetItem(str(ele))
            if index in [0, 4, 5, 6]:
                # 不可修改
                cell.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.table_widget.setItem(current_row_count, index, cell)

        # 3. 发送请求自动获取标题（爬虫获取数据），另开一个线程执行此任务
        # from utils.threads import NewTaskThread
        # thread = NewTaskThread(self, current_row_count, asin)
        # thread.sig_success.connect(self.init_success_callback)
        # thread.sig_error.connect(self.init_error_callback)
        # thread.start()

        # 3. 发送请求自动获取标题（爬虫获取数据），另开一个线程执行此任务
        from utils.threads import NewTaskThreads
        self.newThread = QThread()
        self.task_work = NewTaskThreads(current_row_count, asin, self.newThread)
        self.task_work.moveToThread(self.newThread)
        self.task_work.sig_success.connect(self.init_success_callback)
        self.task_work.sig_error.connect(self.init_error_callback)
        self.newThread.started.connect(self.task_work.start_task)

        self.newThread.finished.connect(self.task_work.deleteLater)
        self.newThread.finished.connect(self.newThread.deleteLater)

        self.newThread.start()

    def event_reset_click(self):
        """
        重新初始化事件响应函数
        :return:
        """
        # 1. 获取已经选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "未选中任何内容!")
            return

        # 2. 获取每一行重新初始化
        for row_object in row_list:
            index = row_object.row()
            print("选中的行:", index)

            asin = self.table_widget.item(index, 0).text().strip()

            # 更新状态
            cell_status = QTableWidgetItem(STATUS_MAPPING[0])
            cell_status.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.table_widget.setItem(index, 6, cell_status)

            # 创建线程进行初始化
            from utils.threads import NewTaskThreads
            self.newThread = QThread()
            self.task_work = NewTaskThreads(index, asin, self.newThread)
            self.task_work.moveToThread(self.newThread)
            self.task_work.sig_success.connect(self.init_success_callback)
            self.task_work.sig_error.connect(self.init_error_callback)
            self.newThread.started.connect(self.task_work.start_task)

            self.newThread.finished.connect(self.task_work.deleteLater)
            self.newThread.finished.connect(self.newThread.deleteLater)

            self.newThread.start()

    def event_reset_count_click(self):
        """
        清零事件响应函数
        :return:
        """
        # 1. 获取已经选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择要操作的行")
            return

        # 2. 获取每一行重新初始化次数
        for row_object in row_list:
            index = row_object.row()

            # 更新状态
            cell_status = QTableWidgetItem(str(0))
            cell_status.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.table_widget.setItem(index, 4, cell_status)

            cell_status = QTableWidgetItem(str(0))
            cell_status.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.table_widget.setItem(index, 5, cell_status)

    def event_delete_click(self):
        """
        删除检测项响应函数
        :return:
        """
        # 1. 获取已经选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择要操作的行")
            return

        # 2. 反转数组，避免删除时表格序号出现问题
        row_list.reverse()

        # 3. 删除
        for row_object in row_list:
            index = row_object.row()
            self.table_widget.removeRow(index)

    def event_alert_click(self):
        """
        SMTP报警配置事件响应函数
        :return:
        """
        # 1. 创建弹窗并在弹窗中进行设置
        from utils.dialog import AlertDialog

        dialog = AlertDialog()
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.exec()

    def event_proxy_click(self):
        """
        代理IP设置事件响应函数
        :return:
        """
        # 1. 创建弹窗并在弹窗中进行设置
        from utils.dialog import ProxyDialog

        dialog = ProxyDialog()
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.exec()

    def event_table_right_menu(self, pos):
        """
        右键菜单事件响应函数
        :pos: 点击位置
        :return:
        """
        # 只有选中一行，才支持右键
        selected_item_list = self.table_widget.selectedItems()
        if len(selected_item_list) == 0:
            return

        menu = QMenu()
        item_copy = menu.addAction("复制")
        item_log = menu.addAction("查看日志")
        item_log_clear = menu.addAction("清除日志")

        # 选中了哪个操作?
        action = menu.exec(self.table_widget.mapToGlobal(pos))

        if action == item_copy:
            # 复制当前型号
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_item_list[0].text())

        if action == item_log:
            # 查看日志，显示一个对话框显示日志信息

            # 获取选中的行号
            row_index = selected_item_list[0].row()
            asin = self.table_widget.item(row_index, 0).text().strip()
            dialog = LogDialog(asin)
            dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
            dialog.exec()

        if action == item_log_clear:
            # 清空日志

            # 获取选中的行号
            row_index = selected_item_list[0].row()
            asin = self.table_widget.item(row_index, 0).text().strip()

            log_file_path = os.path.join("log", f"{asin}.log")
            if os.path.exists(log_file_path):
                os.remove(log_file_path)

    def event_start_click(self):
        """
        开始事件响应函数
        :return:
        """
        # 1. 为每一行创建一个线程去执行（所有线程的记录）
        from utils.scheduler import SCHEDULER

        SCHEDULER.start(
            self,
            BASE_DIR,
            self.task_start_callback,
            self.task_stop_callback,
            self.task_counter_callback,
            self.task_error_counter_callback,
        )
        # 2. 执行中
        self.update_status_message("执行中")

    def event_stop_click(self):
        """
        停止事件响应函数
        :return:
        """
        # 1. 执行中的线程逐一停止
        from utils.scheduler import SCHEDULER
        SCHEDULER.stop()
        # 2. 更新状态
        self.update_status_message("正在终止 1/100")

    def update_status_message(self, message):
        """
        更新状态
        :param message: 输入信息
        :return:
        """
        self.label_status.setText(message)
        self.label_status.repaint()

    def task_start_callback(self, row_index):
        # 对表格中的数据进行数据更新
        cell_status = QTableWidgetItem(STATUS_MAPPING[2])
        cell_status.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        self.table_widget.setItem(row_index, 6, cell_status)

    def task_stop_callback(self, row_index):
        # 对表格中的数据进行数据更新
        cell_status = QTableWidgetItem(STATUS_MAPPING[1])
        cell_status.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        self.table_widget.setItem(row_index, 6, cell_status)

    def task_counter_callback(self, row_index):
        # 原有次数+1
        old_count = self.table_widget.item(row_index, 4).text().strip()
        new_count = int(old_count) + 1

        # 对表格中的数据进行数据更新
        cell_status = QTableWidgetItem(str(new_count))
        cell_status.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        self.table_widget.setItem(row_index, 4, cell_status)

    def task_error_counter_callback(self, row_index):
        # 原有次数+1
        old_count = self.table_widget.item(row_index, 5).text().strip()
        new_count = int(old_count) + 1

        # 对表格中的数据进行数据更新
        cell_status = QTableWidgetItem(str(new_count))
        cell_status.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        self.table_widget.setItem(row_index, 5, cell_status)

    @Slot(int, str, str, str)
    def init_success_callback(self, row_index, asin, title, url):
        """
        更新窗体显示数据
        :param index:
        :param asin:
        :param title:
        :param utl:
        :return:
        """
        # print(row_index, asin, title, url)
        # 更新标题
        cell_title = QTableWidgetItem(title)
        self.table_widget.setItem(row_index, 1, cell_title)

        # 更新url
        cell_url = QTableWidgetItem(url)
        self.table_widget.setItem(row_index, 2, cell_url)

        # 更新状态
        cell_status = QTableWidgetItem(STATUS_MAPPING[1])
        cell_status.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.table_widget.setItem(row_index, 6, cell_status)

        # 清空输入框
        self.txt_asin.clear()

    @Slot(int, str, str, str)
    def init_error_callback(self, row_index, asin, title, url):
        """
        更新窗体显示数据
        :param index:
        :param asin:
        :param title:
        :param utl:
        :return:
        """
        # 更新标题
        cell_title = QTableWidgetItem(title)
        self.table_widget.setItem(row_index, 1, cell_title)

        # 更新url
        cell_url = QTableWidgetItem(url)
        self.table_widget.setItem(row_index, 2, cell_url)

        # 更新状态
        cell_status = QTableWidgetItem(STATUS_MAPPING[11])
        cell_status.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.table_widget.setItem(row_index, 6, cell_status)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
