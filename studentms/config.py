# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: config
@Author  : sky
@Date    : 2023/2/6 16:55
@Desc    : 配置文件,存放系统中需要多次使用的全局变量

"""

USER = (1, "admin", '0', '0', '0')

# 管理模块标识
FLAG_STUDENT = 1  # 学生管理
FLAG_CLASS = 2    # 班级管理
FLAG_ADMIN = 3    # 角色管理
FLAG_GRADE = 4    # 成绩管理
FLAG_INFO = 5     # 修改资料

# 登录窗口
LOGIN_WINDOW = None

# 数据库配置
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_NAME = 'db_studentms'

if __name__ == "__main__":
    pass
