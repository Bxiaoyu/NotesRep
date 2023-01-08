#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
=================================================
@Project -> File   ：xxSystem -> scheduler
@IDE    ：PyCharm
@Author ：sky
@Date   ：2023/1/8 12:52
@Desc   ：
==================================================
'''

class Scheduler(object):
    def __init__(self):
        self.thread_list = []
        self.window = None
        self.terminate = False  # 是否点击了停止

    def start(self, window, base_dir, fn_start, fn_stop, fn_counter, fn_error_counter):
        """
        开始线程
        :return:
        """
        self.window = window
        self.terminate = False

        # 1. 获取表格中的所有数据，每一行创建一个线程去执行监控
        for row_index in range(self.window.table_widget.rowCount()):
            asin = self.window.table_widget.item(row_index, 0).text().strip()
            status_text = self.window.table_widget.item(row_index, 6).text().strip()

            # 只有是待执行时，才创建线程去执行
            if status_text != "待执行":
                continue

            import os
            log_folder = os.path.join(base_dir, 'log')
            if not os.path.exists(log_folder):
                os.makedirs(log_folder)
            log_file_path = os.path.join(log_folder, f"{asin}.log")

            # 2. 每个线程 执行 & 状态实时的显示在表格中
            from PySide6.QtCore import QThread
            from utils.threads import TaskThread
            self.new_thread = QThread()
            self.task_work = TaskThread(row_index, asin, log_file_path, self, self.new_thread)
            self.task_work.moveToThread(self.new_thread)
            self.task_work.sig_start.connect(fn_start)
            self.task_work.sig_counter.connect(fn_counter)
            self.task_work.sig_error_counter.connect(fn_error_counter)
            self.task_work.sig_stop.connect(fn_stop)
            self.new_thread.started.connect(self.task_work.start_task)

            self.new_thread.finished.connect(self.task_work.deleteLater)
            self.new_thread.finished.connect(self.new_thread.deleteLater)

            self.new_thread.start()

            self.thread_list.append(self.new_thread)


    def stop(self):
        self.terminate = True

        # 创建线程，去监测 thread_list 中的数量，实时更新窗体label
        from utils.threads import StopThread
        from PySide6.QtCore import QThread
        self.monitor_thread = QThread()
        self.monitor_task = StopThread(self)
        self.monitor_task.moveToThread(self.monitor_thread)
        self.monitor_task.sig_update.connect(self.window.update_status_message)
        self.monitor_thread.started.connect(self.monitor_task.run)
        self.monitor_thread.finished.connect(self.monitor_task.deleteLater)
        self.monitor_thread.finished.connect(self.monitor_thread.deleteLater)
        self.monitor_thread.start()

    def destroy_thread(self, thread):
        thread.quit()
        self.thread_list.remove(thread)


# 单例模式
SCHEDULER = Scheduler()