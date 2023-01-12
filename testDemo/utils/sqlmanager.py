# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: sqlmanager
@Author  : sky
@Date    : 2023/1/10 14:19
@Desc    :

"""
import os
import sqlite3
from utils.statustype import ResponseStatus

class SqlManager(object):
    def __init__(self, database:str):
        super(SqlManager, self).__init__()
        self._database = database
        self._conn = None

        # 建立连接
        self._connect()

    def _connect(self):
        try:
            self._conn = sqlite3.connect(database=self._database, check_same_thread=False)
            print("数据库连接成功")
            return ResponseStatus.SUCCESS
        except Exception as e:
            print(e)
            return ResponseStatus.ERROR

    def update(self, sql:str):
        """
        数据的增删改操作
        :param sql: sql语句
        :return:
        """
        assert self._conn != None
        try:
            curOjb = self._conn.cursor()
            curOjb.execute(sql)
            self._conn.commit()
            print("数据插入成功")
            return ResponseStatus.SUCCESS
        except Exception as e:
            self._conn.rollback()
            print(e)
            return ResponseStatus.ERROR

    def select(self, sql:str):
        """
        数据查询
        :param sql: sql语句
        :return:
        """
        assert self._conn != None
        try:
            curObj = self._conn.cursor()
            curObj.execute(sql)
            self._conn.commit()
            return curObj.fetchall()
        except Exception as e:
            return []

    def close(self):
        if self._conn != None:
            self._conn.close()
            print("数据库关闭")

    def __del__(self):
        self.close()



DATABASE_MANAGER = SqlManager(os.path.join('db', 'testdb.db'))

if __name__ == "__main__":
    pass
