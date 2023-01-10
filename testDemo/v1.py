# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: v1
@Author  : sky
@Date    : 2023/1/10 13:56
@Desc    :

"""
import sys
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QApplication, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QPushButton, QStackedWidget, QListWidget, QListWidgetItem, QListView
from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtGui import QIcon
from utils.windows import ManagerCenterWidget, DataCenterWidget


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("xxx系统")
        self.resize(750, 500)

        self.contentWidget = QListWidget()
        self.contentWidget.setStyleSheet("background-color: NavajoWhite")
        self.contentWidget.setViewMode(QListView.ViewMode.IconMode)
        self.contentWidget.setIconSize(QSize(51, 51))
        self.contentWidget.setCurrentRow(0)
        self.contentWidget.setMovement(QListView.Movement.Static)
        self.contentWidget.setMaximumWidth(128)
        self.contentWidget.setSpacing(12)

        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget(ManagerCenterWidget())
        self.pagesWidget.addWidget(DataCenterWidget())

        # self.set_lists()

        self.create_icons()

        navigation_layout = QHBoxLayout()
        navigation_layout.addWidget(self.contentWidget)
        navigation_layout.addWidget(self.pagesWidget)
        navigation_layout.setStretchFactor(self.contentWidget, 1)  # 设置显示列表和窗口的比例1:10
        navigation_layout.setStretchFactor(self.pagesWidget, 10)
        self.setLayout(navigation_layout)

    def create_icons(self):
        """
        创建图标式的菜单栏
        :return:
        """
        manager_button = QListWidgetItem(self.contentWidget)
        manager_button.setIcon(QIcon("./images/management_center.png"))
        manager_button.setText("管理中心")
        manager_button.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        manager_button.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

        data_button = QListWidgetItem(self.contentWidget)
        data_button.setIcon(QIcon("./images/data_analysis_center.png"))
        data_button.setText("数据中心")
        data_button.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        data_button.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

        self.contentWidget.currentItemChanged.connect(self.event_page_index_changed)

    def set_lists(self):
        """
        创建文字式的菜单栏
        :return:
        """
        # logo_page = QListWidgetItem(self.contentWidget)
        # logo_page.setText("LOGO")
        # logo_page.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        # logo_page.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

        manager_page = QListWidgetItem(self.contentWidget)
        manager_page.setText("管理中心")
        manager_page.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        manager_page.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

        data_page = QListWidgetItem(self.contentWidget)
        data_page.setText("数据中心")
        data_page.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        data_page.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

        self.contentWidget.currentItemChanged.connect(self.event_page_index_changed)

    @Slot(QListWidgetItem, QListWidgetItem)
    def event_page_index_changed(self, current, previous):
        """
        更新页面索引
        :param current:
        :param previous:
        :return:
        """
        if not current:
            current = previous

        self.pagesWidget.setCurrentIndex(self.contentWidget.row(current))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
