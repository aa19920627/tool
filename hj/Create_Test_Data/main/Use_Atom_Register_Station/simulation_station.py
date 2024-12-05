# -*- encoding: utf-8 -*-
"""
@File    : simulation_station.py
@Date    : 2021/8/17 11:22
@Author  : 洪建
"""
from random import randint

from common.Atom_Register_Data import Atom_Register_Data
from main.Use_Atom_Register_Station.structure_xml import Structure_Xml


# 模拟监测站数据，批量生成原子服务注册文件

# Structure_Xml类提供xml文件写入的方法，Atom_Register_Data提供模拟数据的生成，以下代码控制生成数量和一些基本逻辑


class simulation_station:

    def __init__(self):
        # 定义一些基本配置

        # 每个监测站下设备的数量
        self.equ_num = 3

        # DeviceIp和TcpServerIp，绿色serverIP和tcp连接的ip
        self.DeviceIp = '127.0.0.1'
        self.TcpServerIp = '192.168.0.72'

        # 绿色server连接端口
        self.DevicePort = '20010'

        # 原子服务端口
        self.BServerPort = '8010'

        # 定义是否需要严格控制监测站的经纬度位于对应的市范围内，True表示严格控制，False标识在省内就可以
        self.is_control_longitude_latitude = True

        # 原子服务配置中TcpServerPort的初始值，每次新增一个站点加1
        self.TcpServerPort = 30115
        # 设备能力列表
        self.task_ability = 'FIXFQ;FSCAN;MSCAN;WDDF;SCANDF;FIXDF'
        # 设备编号后缀的初始值
        self.equip_num = 1

        # 设备名称的基础名
        self.equip_name_base = 'demo'

        # 区域码和区域名称
        self.area_list = [('510100', '成都市')]

        # 区域内的经纬度(定义的地市所属监测站生成地理位置的范围，避免监测站建立到区域外)
        self.longitude_latitude = {'510100': (103.8131, 104.2421, 30.8681, 31.3591)}

        # 初始化Atom_Register_Data类
        self.ard = Atom_Register_Data(self.area_list, self.longitude_latitude)

        # 初始化Structure_Xml类
        self.sx = Structure_Xml()

    # 获取注册的元数据
    def generate_data(self):

        code, mfid, mfname = self.ard.mfid_random()

        longitude, latitude = self.ard.longitude_latitude_random(code)

        return mfid, mfname, longitude, latitude

    # 生成原子服务批量注册的xml文件
    def generate_xml(self, num):
        for i in range(num):
            mfid, mfname, longitude, latitude = self.generate_data()

            self.sx.create_Mfids()

            self.sx.create_Mfid(mfid)
            self.sx.create_MfidName(mfname)
            self.sx.create_Longitude(longitude)
            self.sx.create_Latitude(latitude)
            self.sx.create_DeviceIp(self.DeviceIp)
            self.sx.create_DevicePort(self.DevicePort)
            self.sx.create_TcpServerIp(self.TcpServerIp)
            self.sx.create_TcpServerPort(str(self.TcpServerPort))
            self.sx.create_EmDeviceId(self.ard.equipment_random())
            self.sx.create_TaskAbility(self.task_ability)

            # 随机监测站下的设备数量
            for eqnum in range(self.equ_num):
                equip_uuid = self.ard.equipment_random()
                equip_name = self.equip_name_base + str(eqnum+1)
                self.sx.create_DeviceItems(equip_uuid, equip_name, self.BServerPort)


            self.sx.append_Mfids()

            #tcp端口自增长
            self.TcpServerPort += 1

            # 打印注册信息
            print('已生成第%s个监测站信息' % (i + 1) + ':    ' + mfid + '   ' + mfname + '   ' + longitude + '    '
                  + latitude + '    ' + equip_uuid + '    ' + equip_name)

        self.sx.write_to_file()


if __name__ == '__main__':
    ss = simulation_station()

    ss.generate_xml(50)
