# -*- encoding: utf-8 -*-
"""
@File    : faker_data.py
@Date    : 2021/3/11 16:40
@Author  : 洪建
"""
import datetime
import random
import time
import uuid

import pytz
from common.basic_data import Basic_data


class Faker_Data:

    def __init__(self):

        pass

    def facility_status(self):

        '''设施状态,只设置正常状态'''
        status = random.choice(["01"])

        return status

    def equip_state(self):

        '''
        全景运维中设备管理状态
        设备状态 1:启用 2:停用 3:维修 4:迁出 5:报废 6:关机
        '''
        rand = random.randint(1,100)

        #启用比例85%，其他状态合计15%
        if rand >=15 :

            return 1

        else:

            return random.choice([2,3,4,5,6])

    def software_state(self):

        '''
        全景运维中软件管理状态
        软件状态 1:启用 2:停用
        '''

        rand = random.randint(1,100)

        #启用比例100%，其他状态10%
        if rand >= 10 :

            return 1

        else:

            return 2

    def mftype(self):

        '''设施分类,01:固定站;02:移动站;05:管制设备'''

        # mftype = random.choice(["01", "02", "05"])

        #去除管制设备
        mftype = random.choice(range(1,101))

        if mftype <= 10:

            return '02'

        # elif mftype > 10 and mftype <= 15:
        #
        #     return '05'

        else :

            return '01'

    def equtype(self):

        '''监测设备分类，目前只考虑监测设备，测向设备'''

        return random.choice(["01", "02"])

    def fmskind(self, mftype):

        '''监测执行站类型'''
        if mftype == "01":

            #固定站
            return random.choice(["01", "02", "03" ,"04"])

        elif mftype == "02":

            #移动站
            return random.choice(["01", "02", "03", "04", "05"])

        elif mftype == "05":

            #管制设备
            return random.choice(["01", "02", "03" ,"04"])

    def subMfid(self):

        """监测站流水号"""

        return str("%04d" % random.randint(1,9999))

    def mfname(self, ):

        '''监测站名'''

        return "测试监测站" + "%05d" % random.randint(1,99999)

    def equip_name(self, equtype):

        '''设备名'''

        #监测设备
        if equtype == "01":

            return "监测设备" + "%05d" % random.randint(1,99999)

        elif equtype == "02":

            return "测向设备" + "%05d" % random.randint(1,99999)

    def IPC_name(self):

        '''工控机名'''

        return "工控机" + "%05d" % random.randint(1,99999)

    def software_name(self):

        '''软件名称'''

        return "测试软件" + "%05d" % random.randint(1,99999)

    def equmodel(self, equtype):

        '''设备型号'''

        #监测设备型号
        if equtype == "01":

            return random.choice(['DG-R2209A', 'ESMD', 'MultiReceiver', 'R2601', 'EB200'])

        if equtype == "02":

            return random.choice(['DDF550', 'DDF255', 'DGR2026', 'DDF205', 'DGDF'])

    def time_tamp(self):

        '''获取当前时间戳'''

        return int(time.time() * 1000)

    def longitude_random(self):

        '''经度，随机值'''

        longitude_list = Basic_data().longitude()

        return "%.6f" % random.uniform(longitude_list[0],longitude_list[1])

    def latitude_random(self):

        '''纬度，随机值'''

        latitude_list = Basic_data().latitude()

        return "%.6f" % random.uniform(latitude_list[0], latitude_list[1])

    def fmaddrtype(self):

        '''站址类型'''

        return random.choice(["01", "02", "03", "04", "05"])

    def integratedco(self):

        '''集成厂商'''

        integratedco = ['成都华日通讯技术股份有限公司','北京德辰科技股份有限公司','成都大公博创信息技术有限公司',
                        '北京波尔通信技术股份有限公司','浙江原初数据科技有限公司','成都点阵科技有限公司','北京中星世通电子科技有限公司']

        return random.choice(integratedco)

    def integratedco_qjyw(self):

        '''集成厂商，全景运维专用，返回的是厂商编码'''

        integratedco = ['PROVIDER_HUARI','PROVIDER_DIANZHEN','PROVIDER_DECHENG','PROVIDER_ZHONGXINGSHITONG',
                        'PROVIDER_BOER','PROVIDER_HANDE','PROVIDER_LINGDIAN','PROVIDER_YUANCHU','PROVIDER_DGBC',
                        'PROVIDER_CETC54','PROVIDER_RONGXING','PROVIDER_RS']

        return random.choice(integratedco)

    def remocontip(self):

        '''生成11段的随机ip'''

        return "192.168.11." + str(random.randint(2,100))

    def uuid(self):

        '''生成uuid'''

        return str(uuid.uuid4())

    def equsn(self):

        '''设备序列号'''

        return str("%04d" % random.randint(1,9999)) + "-" + str("%04d" % random.randint(1,9999)) + "-" + str("%04d" % random.randint(1,9999)) + \
               "-" + str("%04d" % random.randint(1,9999)) + "-" + str("%04d" % random.randint(1,9999))

    def IPC_model(self):

        '''工控机型号'''

        return random.choice(['华硕EBE-4U-H110A', '研华EPC-P3086', '威沃J1900', '众研IPC-610L', '五四工控IPC-710', '研祥MN50-H'])

    def feature_function(self):

        '''设备能力和能力名'''

        return random.choice([('B_QueryFaciDevStat','监测站/设备状态查询')])

    def serviceCode(self):

        '''BSCode和PSCode'''

        random_code = "-" + Basic_data().areacode() + "-" + "01" + "-" + str("%04d" % random.randint(1,9999)) + "-" + str("%04d" % random.randint(1,9999))

        return "BS" + random_code, "PS" + random_code

    def random_port(self):

        '''随机端口号'''

        random_port = random.choice(range(1,65535))

        return random_port

    def random_mac(self):

        '''随机生成mac地址'''

        Maclist = []

        for i in range(1,7):

            randstr = "".join(random.sample('0123456789abcdefABCDEF', 2))

            Maclist.append(randstr)

        return ':'.join(Maclist)

    #随机移动车的编号
    def mobile_bizcode(self):

        mobile_list = ['b3570742-eb61-4324-aa28-db002c0f7e22', '685a8e12-1f20-45fd-8278-a984b200ef89',
                       'b7d3e2a0-7d0d-4cbd-87b6-38a39a40fae5','b21effef-d2f9-4b43-82e0-0f711915dcfd',
                       '7bd9a4b6-a02d-48c0-bd2f-7732eca5d7fd','1b60a681-4d02-4ad2-980a-2e07a1dcee8e']

        return random.choice(mobile_list)

    #生成国际标准时间格式
    def utc_date_time(self):

        random_int = random.choice([-1,0,-6,-12,-30,-88,-2.-3])

        utc_format = "%Y-%m-%dT%H:%M:%SZ"              #定义format

        # time_str = (datetime.datetime.now() + relativedelta(days= random_int)).strftime(utc_format)

        # return time_str                #返回世界时间格式



if __name__ == '__main__':

    print(Faker_Data().subMfid())