# -*- encoding: utf-8 -*-
"""
@File    : make_data.py
@Date    : 2021/3/11 15:59
@Author  : 洪建
"""
import random

import requests

from common.basic_data import Basic_data
from common.faker_data import Faker_Data
from common.get_token import Get_Token


class  Make_Data:

    '''构建管控数据，监测站，监测设备，能力'''

    def __init__(self):

        self.session = requests.session()
        self.token = Get_Token().get_token()

    def request_api(self, url, data, headers):

        res = self.session.post(url=url, json=data, headers=headers)

        return res

    def build_facility_data(self):

        '''注册监测站，API参数'''

        mftype = Faker_Data().mftype()
        fmskind = Faker_Data().fmskind(mftype)
        areacode = Basic_data().areacode()
        subMfid = Faker_Data().subMfid()
        mfid = areacode + "01" + str(int(mftype)) + str(int(fmskind)) + subMfid

        data = {"areacode":areacode,
                "status":Faker_Data().facility_status(),
                "mftype":mftype,
                "fmskind":fmskind,
                "subMfid":subMfid,
                "mfname":Faker_Data().mfname(),
                "runningdate":"20210311161414",
                "repealdate":"20230325161243",
                "longitude":str(Faker_Data().longitude_random()),
                "latitude":str(Faker_Data().latitude_random()),
                "fmaddrtype":Faker_Data().fmaddrtype(),
                "integratedco":Faker_Data().integratedco(),
                "islink":"00",
                "remocontip":Faker_Data().remocontip(),
                "remocontport":8010,
                "stopusing":False,
                "mfid":mfid}

        url = Basic_data().facility_add_url()

        return url, data

    def build_equip_data(self):

        '''注册监测设备，API参数'''

        equtype = Faker_Data().equtype()

        data = {"equid":Faker_Data().uuid(),
                "equname":Faker_Data().equip_name(equtype),
                "mfid":"",
                "mfname":"",
                "equtype":equtype,
                "equimanu":Faker_Data().integratedco(),
                "equmodel":Faker_Data().equmodel(equtype),
                "equsn":Faker_Data().equsn(),
                "host":Faker_Data().remocontip(),
                "port":"8010",
                "multitask":"false",
                "tasknum":1,
                "stopusing":False,
                "equstatusput":False,
                "currentuserid":Basic_data().currentuserid(),
                "currentusername":Basic_data().currentusername()}

        url = Basic_data().equip_add_url()

        return url, data

    def build_fuction_data(self):

        '''注册设备能力API参数构建,设备能力url写死，有需求另做设计'''

        feature, displayname = Faker_Data().feature_function()
        serviceCode, psServiceCode = Faker_Data().serviceCode()

        data = {"mfid":"",
                "equid":"",
                "feature":feature,
                "displayname":displayname,
                "serviceCode":serviceCode,
                "psServiceCode":psServiceCode,
                "baseserviceurl":"http://192.168.11.114:8010/B_QueryFaciDevStat",
                "baseserviceproxyurl":"http://192.168.11.114:8010/B_QueryFaciDevStat"}

        url = Basic_data().function_add_url()

        return url, data

    def get_mfid_and_mfname(self):

        '''获取注册监测设备，所属的监测站mfid列表'''

        url = Basic_data().facility_list_url()
        data = {"integratedco":"","centerIds":[],"deleted":False,"mfname":"","pagenumber":1,"pagesize":1000}

        res = self.request_api(url, data, self.token)

        return res.json()['object']['data']

    def get_equip_monitor(self):

        '''获取带monitor的监测站所有设备的id'''

        url = Basic_data().equip_list_url()
        data = {"mfid":Basic_data().monitor_facility_id(),"pagenumber":1,"pagesize":500,"deleted":False}

        res = self.request_api(url, data, self.token)

        equip_list = []

        for i in res.json()['object']['data']:

            equip_list.append(i['equid'])

        return equip_list

    def judge_B_QueryFaciDevStat(self):

        '''判断设备是否有QueryFaciDevStat能力'''

        url = Basic_data().equip_list_url()
        data = {"mfid":"","pagenumber":1,"pagesize":1000,"deleted":False}

        res = self.request_api(url, data, self.token)

        #设备列表，没有监测站/设备状态查询能力，加入列表
        equip_list = []

        #判断设备有监测站/设备状态查询能力？
        for i in res.json()['object']['data']:

            try:
                if '监测站/设备状态查询' not in str(i):

                    equip_list.append((i['mfid'],i['equid']))

            except:

                continue

        #返回mfid和equid
        return equip_list

    def register_facility(self, n):

        '''注册监测站，传参：注册数量'''

        for i in range(n):

            url, data = self.build_facility_data()

            res = self.request_api(url, data, self.token)

            if res.status_code == 200:

                print("第%s个监测站创建成功" % (i+1))

            else:

                print("第%s个监测站创建失败" % (i+1))
                print(res.json())

    def register_equip(self, n):

        '''监测测向设备注册'''

        mfidinfo_list = self.get_mfid_and_mfname()


        for i in range(n):

            url, data = self.build_equip_data()

            #随机选择mfid,mfname
            random_mfinfo = random.choice(mfidinfo_list)
            data['mfid'] = random_mfinfo['mfid']
            data['mfname'] = random_mfinfo['mfname']

            res = self.request_api(url, data, self.token)

            if res.status_code == 200:

                print("第%s个监测设备创建成功" % (i + 1))

            else:

                print("第%s个监测设备创建失败" % (i + 1))
                print(res.json())

    def register_function(self):

        '''注册设备能力，目前默认注册监测站/设备状态查询'''

        #获取需要注册能力的设备列表
        equip_list = self.judge_B_QueryFaciDevStat()

        for i in equip_list:

            url, data = self.build_fuction_data()
            mfid, equid = i

            data['mfid'] = mfid
            data['equid'] = equid

            res = self.request_api(url, data, self.token)

            if res.status_code == 200:

                print("注册成功")

            else:

                print("注册失败")
                print(res.json())

    def register_monitor_function(self):

        '''注册monitor监测站的设备能力'''

        equip_list = self.get_equip_monitor()

        for i in equip_list:

            url, data = self.build_fuction_data()

            mfid = Basic_data().monitor_facility_id()
            equip = i

            data['mfid'] = mfid
            data['equid'] = equip

            res = self.request_api(url, data, self.token)

            if res.status_code == 200:

                print("注册成功")

            else:

                print("注册失败")
                print(res.json())

    def register_monitor_facility(self):

        '''注册安装了monitor的监测站'''

        url, data = self.build_facility_data()

        #参数特殊构建，写死
        data['mftype'] = '01'
        data['fmskind'] = '01'
        data['subMfid'] = '0001'
        data['mfname'] = Basic_data().mfname_monitor()
        data['remocontip'] = Basic_data().monitor_facility_ip()
        data['mfid'] = Basic_data().monitor_facility_id()

        self.request_api(url, data, self.token)

    def register_monitor_equip(self, n):

        '''特殊注册：为安装了monitor的监测站，注册设备'''

        mfid = Basic_data().monitor_facility_id()
        mfname_monitor = Basic_data().mfname_monitor()

        for i in range(n):

            url, data = self.build_equip_data()
            data['mfid'] = mfid
            data['mfname'] = mfname_monitor

            res = self.request_api(url, data, self.token)

            if res.status_code == 200 :

                print('%s的设备注册成功' % mfid)

            else:

                print('%s的设备注册失败' % mfid)
                print(res.json())



if __name__ == '__main__':

    #注册监测站，传参：个数
    # Make_Data().register_facility(20)
    #
    # #注册监测测向设备，传参，个数
    # Make_Data().register_equip(55)

    # #注册设备能力
    # Make_Data().register_function()


    # Make_Data().register_monitor_facility()   #注册带monitor的监测站
    # Make_Data().register_monitor_equip(3)      #带monitor的监测站注册设备
    # Make_Data().register_monitor_function()      #注册待monitor的监测站的设备能力