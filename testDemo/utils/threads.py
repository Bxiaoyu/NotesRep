# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: threads
@Author  : sky
@Date    : 2023/1/10 14:18
@Desc    :

"""
from PySide6.QtCore import QThread, Signal


class SqlUpdateTaskThread(QThread):
    # 信号
    sig_finished = Signal(str)

    def __init__(self, sql:str, parent=None):
        super(SqlUpdateTaskThread, self).__init__(parent)
        self._sql = sql

    def run(self) -> None:
        self._run_task()
        self.quit()
        self.deleteLater()

    def _run_task(self):
        from utils.statustype import ResponseStatus
        from utils.sqlmanager import DATABASE_MANAGER
        res = DATABASE_MANAGER.update(self._sql)
        if res == ResponseStatus.SUCCESS:
            status_txt = "操作成功"
        else:
            status_txt = "操作失败"
        self.sig_finished.emit(status_txt)


class SqlSelectTaskThread(QThread):
    # 信号
    sig_finished = Signal(list)

    def __init__(self, sql:str, parent=None):
        super(SqlSelectTaskThread, self).__init__(parent)
        self._sql = sql

    def run(self) -> None:
        self._run_task()
        self.quit()
        self.deleteLater()

    def _run_task(self):
        from utils.sqlmanager import DATABASE_MANAGER
        res = DATABASE_MANAGER.select(self._sql)
        self.sig_finished.emit(res)

if __name__ == "__main__":
    pass
