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
class TAdmin(Base):
    # 表名
    __tablename__ = 't_admin'

    # 表结构
    a_id = Column(Integer, primary_key=True, autoincrement=True, comment='1.超级管理员 其他.班级管理员', nullable=False)
    a_username = Column(String(10), nullable=False, comment='用户名')
    a_password = Column(String(32), nullable=False, comment='密码 长度6-18 (MD5加密)')
    a_mark = Column(String(20), comment='备注')
    a_classid = Column(String(30), comment='可管理班级（id）多个班级id可用,隔开')

    def __init__(self, name, password, mark, class_id):
        self.a_username = name
        self.a_password = password
        self.a_mark = mark
        self.a_classid = class_id

class TClass(Base):
    # 表名
    __tablename__ = 't_class'

    # 表结构
    c_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    c_name = Column(String(20), nullable=False, comment='班级名称')

    def __init__(self, name):
        self.c_name = name


class TStudent(Base):
    # 表名
    __tablename__ = 't_student'

    # 表结构
    s_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    s_realname = Column(String(13), nullable=False, comment='姓名')
    s_number = Column(Integer, comment='学号')
    s_sex = Column(Integer, nullable=False, default=0, comment='性别	1.男，2.女')
    s_class = Column(Integer, nullable=False, comment='所属班级id')
    s_chinese = Column(Integer, nullable=False, comment='语文成绩')
    s_math = Column(Integer, nullable=False, comment='数学成绩')
    s_english = Column(Integer, nullable=False, comment='外语成绩')

    def __init__(self, name, number, sex, class_, chinese, math, english):
        self.s_realname = name
        self.s_number = number
        self.s_sex = sex
        self.s_class = class_
        self.s_chinese = chinese
        self.s_math = math
        self.s_english = english


def main():
    # 1.初始化数据库连接
    engine = create_engine("mysql+pymysql://root:root@localhost/db_studentms", encoding="utf-8", future=True)
    # 2.创建session类型
    dbsession = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
    # 3.创建session对象
    session = dbsession()

    # 查询测试
    res = session.query(TStudent).filter(TStudent.s_id==3).first()
    print(f"{res.s_id} {res.s_realname} {res.s_number} {res.s_sex} {res.s_class} {res.s_chinese} {res.s_math} {res.s_english}")

    # session.add(TStudent('杨建',1005,1,1,0,0,0))
    # session.commit()
    # session.add(TStudent('孟钰',1006,2,1,0,0,0))
    # session.commit()
    res = session.query(TStudent).filter(TStudent.s_id==5).first()
    print(f"{res.s_id} {res.s_realname} {res.s_number} {res.s_sex} {res.s_class} {res.s_chinese} {res.s_math} {res.s_english}")


if __name__ == "__main__":
    pass
