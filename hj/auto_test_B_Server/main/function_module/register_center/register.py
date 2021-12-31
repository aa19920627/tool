'''
@Author：洪建
@Date：2021/12/31 16:16
注册服务：
1.监测站
2.设备
3.设备能力
'''
from component.sqlite_method import ManageSqlite

# 数据库名
DATABASE_NAME = 'auto_b_server'

class Register(object):

    def __init__(self):

        #初始化sqlite操作类
        ms = ManageSqlite()
