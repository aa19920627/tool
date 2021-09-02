# -*- encoding: utf-8 -*-
"""
@File    : simulation_control.py
@Date    : 2021/8/18 15:40
@Author  : 洪建
"""
from xml.dom import minidom

import requests

from common.faker_data import Faker_Data
from common.get_token import Get_Token

#因为管控没有提供注册监测站的M接口，原子服务批量在管控中注册设备时，需要先在管控注册对应的监测站



class Simulation_Control:

    def __init__(self):

        pass

    def __init__(self):

        self.session = requests.session()
        self.token = Get_Token().get_token()

    def request_api(self, url, data, headers):

        res = self.session.post(url=url, json=data, headers=headers)

        return res

    def build_facility_data(self,mfid,mfname,longitude,latitude):

        '''注册监测站，API参数'''

        mftype = '0' + mfid[8]
        fmskind = '0' + mfid[9]
        areacode = mfid[0:6]
        subMfid = mfid[-4:-1]


        data = {"areacode":areacode,
                "status":'01',
                "mftype":mftype,
                "fmskind":fmskind,
                "subMfid":subMfid,
                "mfname":mfname,
                "runningdate":"20210311161414",
                "repealdate":"20230325161243",
                "longitude":longitude,
                "latitude":latitude,
                "fmaddrtype":Faker_Data().fmaddrtype(),
                "integratedco":Faker_Data().integratedco(),
                "islink":"00",
                "remocontip":'192.168.11.119',
                "remocontport":8010,
                "stopusing":False,
                "mfid":mfid}


        return data

    def register_facility(self,mfid,mfname,longitude,latitude,url):

        '''注册监测站，传参：注册数量'''


        data = self.build_facility_data(mfid,mfname,longitude,latitude)

        res = self.request_api(url, data, self.token)

        if res.status_code == 200:

            print("监测站创建成功" )

        else:

            print("监测站创建失败" )
            print(res.json())

    #读取xml文件中的监测设备信息
    def read_xml(self,filename):

        dom = minidom.parse('../../data/DeviceRegister/%s'%filename)

        root = dom.documentElement

        names = root.geElementsByTagName('Mfids')

        for name in names:

            mfid_node =


if __name__ == '__main__':

    mfid = '15020001142143'
    mftype = mfid[8]
    fmskind = mfid[9]
    subMfid = mfid[-4:]
    areacode = mfid[0:6]
    print(mftype,fmskind,subMfid,areacode)