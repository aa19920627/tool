# -*- coding: utf-8 -*-
"""
@Time ： 2024/8/14 16:30
@Auth ： 洪建
"""
import configparser

from component.runtime_environment import Frozen_Path

'''
配置文件读取
'''
config_path = Frozen_Path().app_path() + '/config/config.ini'

config = configparser.ConfigParser()
# 指定文件编码为 utf-8
with open(config_path, 'r', encoding='utf-8') as file:
    config.read_file(file)


# 读取默认配置
def read_default_config():
    return config['DEFAULT']


# 读取设备能力参数
def read_equip_config():
    return config['DEVICE']


if __name__ == '__main__':
    demo = read_equip_config()
    print(demo)
