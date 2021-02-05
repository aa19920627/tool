# -*- encoding: utf-8 -*-
"""
@File    : read_config.py
@Date    : 2021/1/25 13:17
@Author  : 洪建
"""
import os

import yaml

from equipment_restart.common.frozen_path import Frozen_Path

'''
读取配置文件
'''


class Read_config :


    '''
    读取系统参数
    '''
    def __init__(self):

        self.config_dir = Frozen_Path().app_path() + "/config/config.yaml"

        self.data = yaml.load(open(self.config_dir), Loader=yaml.FullLoader)

    def interval_time(self):

        return self.data["Config"]["interval"]


    def restart_time(self):

        return self.data["Config"]["restart_time"]

class Basis_config:

    '''
    读取动环服务的基本信息
    '''
    def __init__(self):

        self.basis_dir = Frozen_Path().app_path() + "/config/basis_config.yaml"
        self.data = yaml.load(open(self.basis_dir), Loader=yaml.FullLoader)

    def basis_ip(self):

        return str(self.data["Basis"]["ip"])

    def basis_url(self):

        return str(self.data["Basis"]["url"])

    def basis_mfid(self):

        return str(self.data["Basis"]["mfid"])

    def basis_equid(self):

        return str(self.data["Basis"]["equid"])

# if __name__ == '__main__':
#     print(type(Basis_config().basis_mfid()))