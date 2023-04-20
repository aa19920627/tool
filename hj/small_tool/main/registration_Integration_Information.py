'''
@Author: 洪建
@Date 2023/4/18 11:41
'''
import json
import time

import requests
from openpyxl.reader.excel import load_workbook

from hj.small_tool.common.basic_data import Basic_data
from hj.small_tool.common.frozen_path import Frozen_Path
from hj.small_tool.common.get_token import Get_Token


# 该工具用于将一体化注册服务的PSCode和总线地址批量导入大公的管控中

class Make_Data:
    '''构建管控数据，监测站，监测设备，能力'''

    def __init__(self):

        self.session = requests.session()
        self.token = Get_Token().get_token()
        self.file = Frozen_Path().app_path() + "\data\安徽一体化服务信息.xlsx"  # 读取一体化平台导出的服务信息表位置
        self.log_path = Frozen_Path().app_path() + "\log\/registration_Integration_Information.log"
        self.baseserviceproxyurl = Basic_data().baseserviceproxy_url()  # 获取一体化平台的总线地址

    def read_excel(self):

        '''读取一体化信息表，获取服务的PScode，BScode'''

        wb = load_workbook(self.file)  # 获取工作簿对象
        ws = wb.get_sheet_by_name(u'服务')  # 获取服务工作簿
        ws_app = wb.get_sheet_by_name(u'系统')  # 获取系统工作簿

        for row in ws.values:

            if row[0] != None and row[0] != 'EQUIPID':
                # print(row[0],row[1],row[3],row[4])

                # 获取服务表中需要的信息
                equip = row[0]
                PScode = row[1]
                BScode = row[1].replace("P", "B")
                soapaction = row[3].split("/")[5]
                appcode = row[4]
                baseurl = row[3]

                # 获取系统表中的mfid
                for row_app in ws_app.values:
                    if row_app[0] == appcode and len(row_app[2]) == 14:
                        mfid = row_app[2]

                        # print(len(mfid))

                        # 用mfid来获取设备能力的源服务地址
                        # baseurl = self.get_baseserviceurl(mfid, soapaction)
                        soapaction_name = self.features_search(soapaction)
                        # print(baseurl,soapaction_name)
                        # 验证是否获取到正确的服务源地址和服务中文名
                        if baseurl != None and soapaction_name != None:

                            # 调用更新接口更新设备能力的信息
                            self.update_function(mfid, equip, soapaction, soapaction_name, BScode, PScode, baseurl)
                            print("注册成功" + "   " + mfid + "    " + soapaction)
                        else:
                            # print('注册失败' + mfid + str(baseurl) + '    ' + str(soapaction))
                            # 将注册失败的日志写入文件
                            with open(self.log_path, 'a', encoding='utf-8') as f:
                                f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "      " +
                                        mfid + "/" + equip + "/" + soapaction + "/" + PScode + "   " + "未查询到对应的设备能力或未查询到对应的服务中文名" + "\n")
                            continue

    def get_baseserviceurl(self, query_mfid, soapaction):

        '''获取服务的源服务地址'''
        url = Basic_data().function_query_rul()
        data = {"mfid": query_mfid,
                "pagenumber": 1,
                "pagesize": 100,
                "deleted": "false"}

        res = self.session.post(url, json=data, headers=self.token)

        # 获取对应设备能力的baserul

        try:
            for i in res.json()['object']['data'][0]['devicefunctions']:
                # print(i['feature'],soapaction)
                if i['feature'] == soapaction:
                    return i['baseserviceurl']
        except:
            return None
        return None

    def features_search(self, soapaction):

        '''获取设备能力的中文名称'''
        url = Basic_data().features_search_url()

        res = self.session.get(url=url, headers=self.token)

        # print(res.json()['object']['functioncodes'])

        # 根据soapaction来获取设备能力的中文名称
        for i in res.json()['object']['functioncodes']:

            if soapaction == i['code_ID']:
                return i['code_NANE']

        return None

    def update_function(self, mfid, equip, feature, displayname, serviceCode, psServiceCode, baseserviceurl):

        url = Basic_data().function_add_url()
        data = {"mfid": mfid,
                "equid": equip,
                "feature": feature,
                "displayname": displayname,
                "serviceCode": serviceCode,
                "psServiceCode": psServiceCode,
                "baseserviceurl": baseserviceurl,
                "baseserviceproxyurl": self.baseserviceproxyurl}

        res = self.session.put(url=url, json=data, headers=self.token)


if __name__ == '__main__':
    mk = Make_Data()
    print(mk.file)
    # mk.read_excel()
    # mk.get_baseserviceurl("51010000110055", 'B_FScan')
    mk.read_excel()
    # print(mk.features_search('B_MScan'))
