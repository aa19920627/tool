# -*- encoding: utf-8 -*-
"""
@File    : simulation_station.py
@Date    : 2021/8/17 11:22
@Author  : 洪建
"""
from common.Atom_Register_Data import Atom_Register_Data
from main.Use_Atom_Register_Station.structure_xml import Structure_Xml



#模拟监测站数据，批量生成原子服务注册文件

#Structure_Xml类提供xml文件写入的方法，Atom_Register_Data提供模拟数据的生成，以下代码控制生成数量和一些基本逻辑



class simulation_station:

    def __init__(self):

        #定义一些基本配置

        #每个监测站下设备的数量范围
        self.equ_max_num = 1
        self.equ_min_num = 1

        #DeviceIp和TcpServerIp，绿色serverIP和tcp连接的ip
        self.DeviceIp = '127.0.0.1'
        self.TcpServerIp = '127.0.0.1'

        #绿色server连接端口
        self.DevicePort = '20010'

        #原子服务端口
        self.BServerPort = '8010'

        #定义是否需要严格控制监测站的经纬度位于对应的市范围内，True表示严格控制，False标识在省内就可以
        self.is_control_longitude_latitude = True

        #原子服务配置中TcpServerPort的初始值，每次新增一个站点加1
        self.TcpServerPort = 30015

        #设备编号后缀的初始值
        self.equip_num = 1

        #设备名称的基础名
        self.equip_name_base = 'Demo'

        #区域码和区域名称
        self.area_list = [('150100', '呼和浩特市'), ('150200', '包头市'), ('150300', '乌海市'), ('150400', '赤峰市'), ('150500', '通辽市'),
                     ('150600', '鄂尔多斯市'), ('150700', '呼伦贝尔市'), ('152200', '兴安盟'), ('152500', '锡林郭勒盟'),
                     ('152600', '乌兰察布市'), ('152800', '巴彦淖尔市'), ('152900', '阿拉善盟')]

        #区域内的经纬度(定义的地市所属监测站生成地理位置的范围，避免监测站建立到区域外)
        self.longitude_latitude = {'150100': (111.813, 111.242, 40.868, 40.359),
                              '150200': (110.641, 109.778, 42.161, 41.531),
                              '150300': (106.918, 106.802, 39.611, 39.312),
                              '150400': (119.960, 117.960, 43.827, 42.691),
                              '150500': (122.910, 121.262, 44.115, 43.105),
                              '150600': (109.462, 107.353, 40.275, 39.168),
                              '150700': (124.025, 120.223, 51.007, 49.031),
                              '152200': (122.569, 120.207, 47.006, 46.138),
                              '152500': (116.010, 112.429, 44.453, 42.517),
                              '152600': (113.593, 112.264, 41.849, 40.726),
                              '152800': (109.045, 106.287, 41.964, 41.067),
                              '152900': (104.936, 100.904, 41.430, 39.661)}

        #初始化Atom_Register_Data类
        self.ard = Atom_Register_Data(self.area_list,self.longitude_latitude)

        #初始化Structure_Xml类
        self.sx = Structure_Xml()


    #获取注册的元数据
    def generate_data(self):

        #

        code, mfid, mfname = self.ard.mfid_random()

        longitude,latitude = self.ard.longitude_latitude_random(code)

        equip_uuid = self.ard.equipment_random()

        return mfid,mfname,longitude,latitude,equip_uuid

    #生成原子服务批量注册的xml文件
    def generate_xml(self,num):

        for i in range(num):

            mfid, mfname, longitude, latitude, equip_uuid = self.generate_data()

            self.sx.create_Mfids()

            self.sx.create_Mfid(mfid)
            self.sx.create_MfidName(mfname)
            self.sx.create_Longitude(longitude)
            self.sx.create_Latitude(latitude)
            self.sx.create_DeviceIp(self.DeviceIp)
            self.sx.create_DevicePort(self.DevicePort)
            self.sx.create_TcpServerIp(self.TcpServerIp)
            self.sx.create_TcpServerPort(str(self.TcpServerPort))

            equip_name = self.equip_name_base + str(self.equip_num)
            self.sx.create_DeviceItems(equip_uuid, equip_name, self.BServerPort)

            self.sx.append_Mfids()

            #设备名称的序号和tcp端口自增长
            self.equip_num +=1
            self.TcpServerPort+=1

            #打印注册信息
            print('已生成第%s个监测站信息'% (i+1) + ':    ' + mfid + '   ' + mfname + '   ' + longitude + '    '
                  +latitude+ '    '+equip_uuid+'    '+equip_name)

        self.sx.write_to_file()



if __name__ == '__main__':


    ss = simulation_station()

    ss.generate_xml(40)