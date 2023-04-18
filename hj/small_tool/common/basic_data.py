# -*- encoding: utf-8 -*-
"""
@File    : basic_data.py
@Date    : 2021/3/11 16:16
@Author  : 洪建
"""
import yaml

from hj.small_tool.common.frozen_path import Frozen_Path


class Basic_data:

    '''全景运维，管控系统数据使用'''

    def __init__(self):

        self.path = Frozen_Path().app_path() + "/config/config.yaml"

        f = open(self.path, encoding='utf-8').read()

        self.file = yaml.load(f, Loader=yaml.FullLoader)

    def token(self):

        '''万能token'''

        return self.file["config"]["token"]

    def currentuserid(self):

        '''用户id'''

        return self.file["config"]["currentuserid"]

    def currentusername(self):

        '''用户名'''

        return self.file["config"]["currentusername"]

    def gateway_ip(self):

        '''默认网关'''

        return self.file["config"]["gateway_ip"]

    def function_add_url(self):

        '''设备能力注册接口api'''

        return self.file["config"]["function_add"]

if __name__ == '__main__':

    print(Basic_data().machine_list_url())