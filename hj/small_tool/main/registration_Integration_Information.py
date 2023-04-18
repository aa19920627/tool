'''
@Author: 洪建
@Date 2023/4/18 11:41
'''
import requests
from openpyxl.reader.excel import load_workbook

from hj.small_tool.common.basic_data import Basic_data
from hj.small_tool.common.frozen_path import Frozen_Path
from hj.small_tool.common.get_token import Get_Token


#该工具用于将一体化注册服务的PSCode和总线地址批量导入大公的管控中

class  Make_Data:

    '''构建管控数据，监测站，监测设备，能力'''

    def __init__(self):

        self.session = requests.session()
        self.token = Get_Token().get_token()
        self.file = Frozen_Path().app_path() + "\data\安徽系统服务417.xlsx"    #读取一体化平台导出的服务信息表位置

    def read_excel(self):

        '''读取一体化信息表，获取服务的PScode，BScode'''

        wb = load_workbook(self.file)    #获取工作簿对象
        # ws = wb.active      #获取工作表

        # for row in ws.values:
        #     print(row)



    def request_api(self, url, data, headers):

        res = self.session.put(url=url, json=data, headers=headers)

        return res

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


if __name__ == '__main__':

    mk = Make_Data()
    print(mk.file)
    mk.read_excel()