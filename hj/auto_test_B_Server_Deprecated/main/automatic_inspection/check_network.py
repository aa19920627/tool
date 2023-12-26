'''
@Author：洪建
@Date：2022/1/10 17:07
该类用于检查设备ip的连通性
'''
import os

from component.loading_config import database_config
from component.sqlite_method import ManageSqlite

DATABASE_NAME = database_config()


class CheckNetwork(object):

    def __init__(self, equid):
        self.equid = equid
        self.ms = ManageSqlite(DATABASE_NAME)

    # 测试设备对应的ip的连通性
    def test_ip_connection(self):
        # 查询ip地址
        ip_value = self.ms.get_fetchone("SELECT ip FROM device WHERE equid = '%s'" % self.equid)[0]

        # 测试ip连通性
        back_info = os.system('ping -w 1 %s' % ip_value)

        # 判断ping结果，通返回0，不通返回1
        if back_info == 0:
            return True
        else:
            return False


if __name__ == '__main__':
    cn = CheckNetwork('a6590676-f5a7-4220-b105-a6ea4edbd77b')
    print(cn.test_ip_connection())
