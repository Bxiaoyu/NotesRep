# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: threads
@Author  : sky
@Date    : 2023/1/5 15:12
@Desc    :

"""
import requests
from bs4 import BeautifulSoup
import time
from PySide6.QtCore import QThread, Signal, QObject

HOST = "https://www.amazon.com/"
HOST_ASIN_TPL = f"{HOST}{'gp/product/'}"
HOST_TASK_LIST_TPL = f"{HOST}{'gp/offer-listing'}"


class NewTaskThread(QThread):
    # 创建信号，更新窗体数据
    sig_success = Signal(int, str, str, str)
    sig_error = Signal(int, str, str, str)

    def __init__(self, row_index, asin):
        super().__init__()
        self.row_index = row_index
        self.asin = asin

    def run(self) -> None:
        """
        执行具体任务
        :return:
        """
        try:
            res = requests.get(
                url= f"{HOST_ASIN_TPL}{self.asin}/",
                headers={
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
                    "pragma":"no-cache",
                    "upgrade-insecure-requests":"1",
                    "cache-control":"no-cache",
                    "accept-language":"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    "accept-encoding":"gzip, deflate, br",
                    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
                }
            )
            if res.status_code != 200:
                raise Exception("初始化失败")

            soup = BeautifulSoup(res.text, 'lxml')
            title = soup.find(id="productTitle").text.strip()
            tpl = "https://www.amazon.com/gp/product/ajax/ref=dp_aod_pn?asin={}&m=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=&pc=dp&experienceId=aodAjaxMain"
            url = tpl.format(self.asin)

            # 获取到title和url，将此信息填写到表格上 & 写入文件中
            self.sig_success.emit(self.row_index, self.asin, title, url)
        except Exception as e:
            title = f"监控项 {self.asin} 添加失败。"
            self.sig_error.emit(self.row_index, self.asin, title, str(e))


class NewTaskThreads(QObject):
    # 创建信号，更新窗体数据
    sig_success = Signal(int, str, str, str)
    sig_error = Signal(int, str, str, str)

    def __init__(self, row_index, asin, thread, parent=None):
        super(NewTaskThreads, self).__init__(parent)
        self.row_index = row_index
        self.asin = asin
        self.work_thread = thread

    def start_task(self) -> None:
        """
        执行具体任务
        :return:
        """
        try:
            res = requests.get(
                url= f"{HOST_ASIN_TPL}{self.asin}/",
                headers={
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
                    "pragma":"no-cache",
                    "upgrade-insecure-requests":"1",
                    "cache-control":"no-cache",
                    "accept-language":"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    "accept-encoding":"gzip, deflate, br",
                    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
                }
            )
            print(res)
            if res.status_code != 200:
                raise Exception("初始化失败")

            soup = BeautifulSoup(res.text, 'lxml')
            title = soup.find(id="productTitle").text.strip()
            tpl = "https://www.amazon.com/gp/product/ajax/ref=dp_aod_ALL_mbc?asin={}&m=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=&pc=dp&experienceId=aodAjaxMain"
            url = tpl.format(self.asin)

            # 获取到title和url，将此信息填写到表格上 & 写入文件中
            self.sig_success.emit(self.row_index, self.asin, title, url)
            self.work_thread.quit()

        except Exception as e:
            title = f"监控项 {self.asin} 添加失败。"
            self.sig_error.emit(self.row_index, self.asin, title, str(e))
            self.work_thread.quit()


class TaskThread(QObject):
    # 创建信号
    sig_start = Signal(int)
    sig_stop = Signal(int)
    sig_counter = Signal(int)
    sig_error_counter = Signal(int)

    def __init__(self, row_index, asin, log_file_path, scheduler, thread, parent=None):
        super(TaskThread, self).__init__(parent)
        self.row_index = row_index
        self.asin = asin
        self.log_file_path = log_file_path
        self.scheduler = scheduler
        self.thread = thread

    def start_task(self):
        # 触发sig_start信号
        self.sig_start.emit(self.row_index)

        import time
        import random
        while True:
            if self.scheduler.terminate:
                self.sig_stop.emit(self.row_index)
                # 自己的线程在thread_list中移除
                self.scheduler.destroy_thread(self.thread)
                return

            try:
                time.sleep(random.randint(1, 3))
                self.sig_counter.emit(self.row_index)

                with open(self.log_file_path, mode='a', encoding='utf-8') as f:
                    f.write("日志\n")

                # 监控动作
                # 1. 根据型号访问，通过bs4获取数据
                # 2. 获取到数据，价格是否小于预期
                # 3. 发送报警邮件

                time.sleep(5)
            except Exception as e:
                self.sig_error_counter.emit(self.row_index)


class StopThread(QObject):
    # 信号
    sig_update = Signal(str)

    def __init__(self, scheduler, parent=None):
        super(StopThread, self).__init__(parent)
        self.scheduler = scheduler

    def run(self):
        # 1. 检测线程数量
        while True:
            running_count = len(self.scheduler.thread_list)
            self.sig_update.emit(f"正在终止({running_count})")

            if running_count == 0:
                break

            time.sleep(1)


if __name__ == "__main__":
    pass
