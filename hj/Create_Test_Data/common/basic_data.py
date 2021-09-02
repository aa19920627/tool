# -*- encoding: utf-8 -*-
"""
@File    : basic_data.py
@Date    : 2021/3/11 16:16
@Author  : 洪建
"""
import os

import yaml

from common.frozen_path import Frozen_Path


class Basic_data:

    '''全景运维，管控系统数据使用'''

    def __init__(self):

        self.path = Frozen_Path().app_path() + "/config/config.yaml"

        f = open(self.path, encoding='utf-8').read()

        self.file = yaml.load(f, Loader=yaml.FullLoader)

    def areacode(self):

        '''区域码'''

        return str(self.file["config"]["areacode"])

    def longitude(self):

        '''经度'''

        return [self.file["config"]["longitudemin"], self.file["config"]["longitudemax"]]

    def latitude(self):

        '''纬度'''

        return [self.file["config"]["latitudemin"], self.file["config"]["latitudemax"]]

    def facility_add_url(self):

        '''监测站新增api'''

        return self.file["config"]["facility_add"]

    def equip_add_url(self):

        '''监测设备新增api'''

        return self.file["config"]["equip_add"]

    def facility_list_url(self):

        '''监测站列表接口api'''

        return self.file["config"]["facility_list"]

    def equip_list_url(self):

        '''监测设备列表接口api'''

        return self.file["config"]["equip_list"]

    def function_add_url(self):

        '''设备能力注册接口api'''

        return self.file["config"]["function_add"]

    def machine_add_url(self):

        '''全景运维-注册设备API地址'''

        return self.file["config"]["machine_add"]

    def machie_list_url(self):

        '''全景运维-监测设施列表查询API地址'''

        return self.file["config"]["machie_list"]

    def software_add_url(self):

        '''全景运维-设备注册API地址'''

        return self.file["config"]["software_add"]

    def cluster_list_url(self):

        '''全景运维-监测应用列表API地址'''

        return self.file["config"]["cluster_list"]

    def serversoftware_monitor_url(self):

        '''全景运维-配置设备和软件关联关系API地址'''

        return self.file["config"]["serversoftware_monitor"]

    def software_list_url(self):

        '''全景运维-软件列表API地址'''

        return self.file["config"]["software_list"]

    def machine_list_url(self):

        '''全景运维-设备列表API地址'''

        return self.file["config"]["machine_list"]

    #全景运维-监测车轨迹新增API地址
    def mobile_add_url(self):

        return self.file["config"]["mobile_add"]

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

    def mfname_monitor(self):

        '''安装了monitor的监测站的mfname'''

        return self.file["config"]["mfname_monitor"]

    def monitor_facility_ip(self):

        '''安装monitor的监测站的ip地址'''

        return self.file["config"]["monitor_facility_ip"]

    def monitor_facility_id(self):

        '''安装monitor的监测站的mfid'''

        return self.file["config"]["monitor_facility_id"]

if __name__ == '__main__':

    print(Basic_data().machine_list_url())