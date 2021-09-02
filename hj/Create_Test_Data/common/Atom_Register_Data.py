# -*- encoding: utf-8 -*-
"""
@File    : Atom_Register_Data.py
@Date    : 2021/8/17 11:25
@Author  : 洪建
"""

#构建原子服务批量注册监测站的模拟数据
import random
import uuid

from common.faker_data import Faker_Data


class Atom_Register_Data:

    def __init__(self,area,longitude_latitude):

        #地区编码和地区名称
        self.area = area

        #地市经纬度
        self.longitude_latitude = longitude_latitude


    #随机选取监测站的类型
    def mftype_random(self):

        ran_int = random.randint(1,10)

        if ran_int >=4 :

            return random.choice(['11','12','13','14']),'固定站'

        else:

            return random.choice(['21','22','23']),'移动站'


    #在各个地市随机生成mfid和mfidname
    def mfid_random(self):

        '''
        :param area: 地市区域码和地市名称
        '''

        #生成mfid
        code, name = random.choice(self.area)
        mftype_random,mftype = self.mftype_random()

        mfid = code + '01' + mftype_random + Faker_Data().subMfid()

        #生成监测站名称
        mfname = name + mftype + Faker_Data().subMfid()

        return code,mfid,mfname

    #生成各地市区域范围的经纬度，确保监测站地理位置处于市内区域
    def longitude_latitude_random(self,areacode):

        maxlongitude,minlongitude,maxlatitude,minlatitude = self.longitude_latitude[areacode]

        longitude = "%.3f" % random.uniform(minlongitude,maxlongitude)

        latitude = "%.3f" % random.uniform(minlatitude,maxlatitude)

        return str(longitude),str(latitude)

    #生成设备编号，uuid
    def equipment_random(self):

        return str(uuid.uuid4())



if __name__ == '__main__':





    area_list = [('150100','呼和浩特市'), ('150200','包头市'), ('150300','乌海市'), ('150400','赤峰市'), ('150500','通辽市'),
                     ('150600','鄂尔多斯市'), ('150700','呼伦贝尔市'), ('152200','兴安盟'), ('152500','锡林郭勒盟'),
                     ('152600','乌兰察布市'), ('152800','巴彦淖尔市'), ('152900','阿拉善盟')]
    longitude_latitude = {'150100':(111.813,111.242,40.868,40.359),
                          '150200':(110.641,109.778,42.161,41.531),
                          '150300':(106.918,106.802,39.611,39.312),
                          '150400':(119.960,117.960,43.827,42.691),
                          '150500':(122.910,121.262,44.115,43.105),
                          '150600':(109.462,107.353,40.275,39.168),
                          '150700':(124.025,120.223,51.007,49.031),
                          '152200':(122.569,120.207,47.006,46.138),
                          '152500':(116.010,112.429,44.453,42.517),
                          '152600':(113.593,112.264,41.849,40.726),
                          '152800':(109.045,106.287,41.964,41.067),
                          '152900':(104.936,100.904,41.430,39.661)}

    ard = Atom_Register_Data(area_list,longitude_latitude)

    code,mfid,mfname = ard.mfid_random()

    ard.longitude_latitude_random(code)

    print(ard.equipment_random())