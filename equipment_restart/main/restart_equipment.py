# -*- encoding: utf-8 -*-
"""
@File    : restart_equipment.py
@Date    : 2021/1/25 13:30
@Author  : 洪建
"""
import time

import requests

from common.component import Component_method
from common.read_xml import Read_Xml
from common.write_log import Write_Log

'''
重启设备，调用动环服务
'''


class Restart_equipment:

    def __init__(self, url, mfid, equid):

        self.session = requests.session()
        self.url = url
        self.mfid = mfid
        self.equid = equid


    def build_request(self, equipmentswitch):

        url = self.url
        data = Read_Xml().read_xml("E_RemoteControl") % (self.mfid, self.equid, equipmentswitch)

        headers = {"SoapAction":"E_RemoteControl", "Content-Type":"text/xml;charset=UTF-8"}

        try:
            res = self.session.post(url=url, json=data, headers=headers,timeout=5)

        except requests.exceptions.Timeout:

            Write_Log().write_log("%调用设备开关服务超时" % Component_method().get_log_time())

    def restart_equipment(self):

        self.build_request("off")   #关掉设备

        time.sleep(10)

        self.build_request("on")    #开启设备

