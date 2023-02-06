# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: sql_table
@Author  : sky
@Date    : 2023/2/6 17:28
@Desc    : 数据库表

"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# 创建对象的基类
Base = declarative_base()

# 定义Admin对象
class Admin(Base):
    # 表名
    __tablename__ = 'admin'

    # 表结构
    a_id = Column(Integer, primary_key=True, auto_increment=True, comment='1.超级管理员 其他.班级管理员'),
    a_username = Column(String(10))

if __name__ == "__main__":
    pass
