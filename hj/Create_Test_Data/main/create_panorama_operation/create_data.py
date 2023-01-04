# -*- encoding: utf-8 -*-
"""
@File    : create_data.py
@Date    : 2021/3/15 11:15
@Author  : 洪建
"""
import random
import time

import requests

from common.basic_data import Basic_data
from common.faker_data import Faker_Data
from common.get_token import Get_Token


class Create_Data:

    '''构建全景运维的测试数据'''

    def __init__(self):

        self.session = requests.session()
        self.token = Get_Token().get_token()

    def request_api(self, url, data, headers):

        res = self.session.post(url=url, json=data, headers=headers)

        return res

    def build_IPC_data(self):

        '''构建工控机注册的api参数
           网关默认
        '''

        machinecode = Faker_Data().uuid()

        data = {"machinePropValueList":
                    [{"machinePropCode":"PROP_7_2_IS_MONITORABLE",
                      "propValue":"1",
                      "machineCode":machinecode},
                     {"machinePropCode":"PROP_7_2_PORT",
                      "propValue":str(Faker_Data().random_port()),
                      "machineCode":machinecode},
                     {"machinePropCode":"PROP_7_2_IP",
                      "propValue":Faker_Data().remocontip(),
                      "machineCode":machinecode},
                     {"machinePropCode":"PROP_7_2_GATEWAY",
                      "propValue":Basic_data().gateway_ip(),
                      "machineCode":machinecode},
                     {"machinePropCode":"PROP_7_2_IS_AGENT",
                      "propValue":"1",
                      "machineCode":machinecode},
                     {"machinePropCode":"PROP_7_2_MAC",
                      "propValue":Faker_Data().random_mac(),
                      "machineCode":machinecode},
                     {"machinePropCode":"PROP_7_2_MOTHER_BOARD_SN",
                      "propValue":Faker_Data().uuid(),
                      "machineCode":machinecode}],
                     "machine":{"name":Faker_Data().IPC_name(),
                                "machineType":2,
                                "machineCode":Faker_Data().uuid(),
                                "roomCode":"",
                                "state":Faker_Data().equip_state(),
                                "onlineTime":Faker_Data().time_tamp(),
                                "offlineTime":"",
                                "brand":"",
                                "model":Faker_Data().IPC_model(),
                                "serialNumber":Faker_Data().uuid(),
                                "manufacturer":Faker_Data().integratedco_qjyw(),
                                "provider":Faker_Data().integratedco_qjyw(),
                                "providerPhone":'',
                                "accessRouter":'',
                                "description":''}}


        url = Basic_data().machine_add_url()

        return url, data

    def build_software_data(self):

        '''注册软件'''

        data = {"software":
                    {"softwareCode":Faker_Data().uuid(),
                     "state":Faker_Data().software_state(),
                     "provider":Faker_Data().integratedco_qjyw(),
                     "clusterId":"",
                     "onlineTime":Faker_Data().time_tamp(),
                     "name":Faker_Data().software_name(),
                     "ports":Faker_Data().random_port()}}

        url = Basic_data().software_add_url()

        return url,data

    def build_software_equip_monitor(self):

        '''配置软件和设备的关联关系'''

        data = [{"machineCode":"",
                 "softwareCode":""}]
        url = Basic_data().serversoftware_monitor_url()

        return url, data

    def get_cluster_list(self):

        '''获取监测应用列表'''

        url = Basic_data().cluster_list_url()
        data = {"pageNum":1,"pageSize":1000}

        res = self.request_api(url, data, self.token)

        cluster_list = []

        for i in res.json()['data']['records'] :

            cluster_list.append(i['clusterCode'])

        return cluster_list

    def get_MachieCode(self):

        '''获取设备编号'''

        url = Basic_data().machie_list_url()
        data = {"pageNum":1,"pageSize":500}

        res = self.request_api(url,data,self.token)

        machiecode_list = []

        for i in res.json()['data']['records']:

            machiecode_list.append(i['roomCode'])

        return machiecode_list

    def get_monitor_equiplist(self):

        '''获取安装了monitor的监测站下设备列表'''

        url = Basic_data().machine_list_url()
        data = {"pageNum":1,"pageSize":500,"roomCode":Basic_data().monitor_facility_id()}

        res = self.request_api(url,data,self.token)

        machiecode_list = []

        for i in res.json()['data']['records']:

            machiecode_list.append(i['machineCode'])

        return machiecode_list

    def get_software_list(self):

        '''获取软件列表'''

        url = Basic_data().software_list_url()
        data = {"pageNum":1,"pageSize":10000}

        res = self.request_api(url, data, self.token)

        software_list = []

        for i in res.json()['data']['records']:

            software_list.append(i['softwareCode'])

        return software_list

    def register_IPC(self, n):

        '''
        注册工控机
        n表示每个监测设施增加几个工控机
        '''

        machiecode_list = self.get_MachieCode()

        for i in range(2):

            for i in machiecode_list:

                url, data = self.build_IPC_data()   #注册工控机的api信息
                data['machine']['roomCode'] = i

                res = self.request_api(url, data, self.token)

                if res.status_code == 200 :

                    print('%s的工控机注册成功' %i)

                else:

                    print("%s的工控机注册失败" %i)

    def register_software(self, n):

        '''注册软件，n代表注册的个数'''

        cluster_list = self.get_cluster_list()

        for i in range(n):

            url, data = self.build_software_data()
            data['software']['clusterId'] = random.choice(cluster_list)

            res = self.request_api(url, data, self.token)

            if res.status_code == 200 :

                print("第%s个软件注册成功" % (i+1))

            else:

                print("第%s个软件注册失败" % (i+1))
                print(res.json())

    def relevance_software_equip(self, n):

        '''设备和软件建立关联关系，该方法仅针对带monitor的站点下的设备
           n代表每个设备关联多少软件
        '''

        equip_list = self.get_monitor_equiplist()
        software_list = self.get_software_list()
        url, data = self.build_software_equip_monitor()

        for i in range(n):

            for j in equip_list:

                data[0]['machineCode'] = j
                data[0]['softwareCode'] = random.choice(software_list)

                res = self.request_api(url, data, self.token)

                if res.status_code == 200:

                    print('%s和软件关联成功' %j)

                else:

                    print('%s和软件关联失败' % j)
                    print(res.json())

    #增加移动车轨迹请求数据
    def add_mobile_car_running_data(self, bizCode):

        data = {
                 "bizCode": bizCode,
                 "bizType": 100,
                 "equipId": "",
                 "createTime": Faker_Data().utc_date_time(),
                 "latitude": Faker_Data().longitude_random(),
                 "longitude": Faker_Data().latitude_random()
                }

        url = Basic_data().mobile_add_url()

        return data,url

    #增加移动车轨迹
    def add_mobile_car_running(self, n, bizCode):


        for i in range(n):

            data, url = self.add_mobile_car_running_data(bizCode)

            time.sleep(random.randint(1,4))     #休眠，增加数据的随机性

            res = self.request_api(url, data, self.token)
            # print(url)
            if res.status_code == 200:

                print('增加移动车轨迹成功')

            else:

                print('增加移动车轨迹失败')
                print(res.json())


if __name__ == '__main__':

    # Create_Data().register_IPC(1)   #注册工控机，传参为每个监测站建几个工控机
    Create_Data().register_software(1000)   #注册软件，传参为注册的软件总量
    # Create_Data().relevance_software_equip(1)   #设置设备和软件的关联关系，传参为每个设备关联的软件数量，该接口仅用于关联指定监测站(部署monitor)的设备
    # Create_Data().add_mobile_car_running(200, '7bd9a4b6-a02d-48c0-bd2f-7732eca5d7fd')