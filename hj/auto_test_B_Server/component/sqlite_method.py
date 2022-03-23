'''
@Author：洪建
@Date：2021/12/30 14:25

说明
ManageSqlite类存放sqlite数据库的通用操作方法
'''
import os.path
import sqlite3

# db文件存放路径
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/db/')


class ManageSqlite(object):

    def __init__(self, database_name):
        # 建立sqlite连接
        # 建立连接
        self._conn = sqlite3.connect(DB_PATH + database_name)
        # 创建游标
        self._cur = self._conn.cursor()

    # 建表，增删改
    def operation_sqlite(self, *sql):
        # 执行语句
        for i in sql:
            self._cur.execute(i)
        self._conn.commit()

    # 添加多条数据
    def insert_many(self, sql, data):
        # 执行语句
        self._cur.executemany(sql, data)
        self._conn.commit()

    # 传入一个脚本，执行多条sql语句，所有sql语句应该用；隔开
    def execute_script(self, sql_script):
        # 执行语句
        self._cur.executescript(sql_script)

    # 获取查询结果的第1条数据
    def get_fetchone(self, sql):
        self._cur.execute(sql)
        return self._cur.fetchone()

    # 获取查询结果所有数据，返回一个列表
    def get_fetchall(self, sql):
        self._cur.execute(sql)
        return self._cur.fetchall()

    # 断开连接
    def close_cur_conn(self):
        # 关闭游标
        self._cur.close()
        # 关闭连接
        self._conn.close()


if __name__ == '__main__':
    print(os.path.join(os.path.dirname(__file__), '../data/db/'))
    _ms = ManageSqlite('auto_b_server')

    # _sql_one = '''CREATE TABLE table_test
    #             (监测站名称 TEXT,Mfid TEXT) '''
    # _ms.operation_sqlite(_sql_one)

    # print(_ms.get_fetchone("SELECT * from device where equid = 'a6590676-f5a7-4220-b105-a6ea4edbd77b'"))
    list_old = _ms.get_fetchall("SELECT province FROM area ")
    area_list = []
    for i in list_old:
        area_list.append(i[0])
    list_new = list(set(area_list))
    list_new.sort(key=area_list.index)
    print(list_new)
    _ms.close_cur_conn()
