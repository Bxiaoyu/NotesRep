# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: db
@Author  : sky
@Date    : 2023/2/7 15:57
@Desc    :

"""
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config as cf

class DBManager:
    def __init__(self, host, user, password, db_name):
        self._host = host
        self._user = user
        self._password = password
        self._db_name = db_name

    def conn(self):
        try:
            # 1.初始化数据库连接
            # engine = create_engine("mysql+pymysql://root:root@localhost/db_studentms", encoding="utf-8", future=True)
            engine = create_engine(f"mysql+pymysql://{self._user}:{self._password}@{self._host}/{self._db_name}",
                                   encoding="utf-8", future=True)
            # 2.创建session类型
            dbsession = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
            # 3.创建session对象
            self.session = dbsession()

            return self.session
        except Exception as e:
            print(e)
            return None


# 获取MD5加密结果
def md5(text):
    text = bytes(text, encoding="utf-8")
    return hashlib.md5(text).hexdigest()


DBSESSION = DBManager(cf.DB_HOST, cf.DB_USER, cf.DB_PASSWORD, cf.DB_NAME).conn()


if __name__ == "__main__":
    pass
