# -*- encoding: utf-8 -*-
"""
@File    : structure_xml.py
@Date    : 2021/8/16 16:43
@Author  : 洪建
"""
import time
import xml.dom.minidom as minidom

#构建原子服务自动注册标准xml的结构


class Structure_Xml:

    def __init__(self):

        pass

        #创建文档
        self.dom = minidom.getDOMImplementation().createDocument(None, 'DeviceRegister', None)
        #获得根节点
        self.root = self.dom.documentElement


    #创建节点Mfids
    def create_Mfids(self):

        self.Mfids = self.dom.createElement('Mfids')


    #创建节点Mfid-监测站编号
    #传入参数mfid
    def create_Mfid(self,mfid):

        self.Mfid = self.dom.createElement('Mfid')
        self.Mfid_value = self.dom.createTextNode(mfid)

        #给Mfid添加内容
        self.Mfid.appendChild(self.Mfid_value)

        #将Mfid添加到Mfids的子节点
        self.Mfids.appendChild(self.Mfid)

    #创建节点MfidName-监测站名称
    #传入监测站名称mfidName
    def create_MfidName(self,mfidName):

        self.MfidName = self.dom.createElement('MfidName')
        self.MfidName_value = self.dom.createTextNode(mfidName)

        self.MfidName.appendChild(self.MfidName_value)

        self.Mfids.appendChild(self.MfidName)

    #创建节点Longitude-经度
    #传入经度
    def create_Longitude(self,longitude):

        self.Longitude = self.dom.createElement('Longitude')
        self.Longitude_value = self.dom.createTextNode(longitude)

        self.Longitude.appendChild(self.Longitude_value)

        self.Mfids.appendChild(self.Longitude)

    # 创建节点Latitude-纬度
    # 传入纬度
    def create_Latitude(self, latitude):

        self.Latitude = self.dom.createElement('Latitude')
        self.Latitude_value = self.dom.createTextNode(latitude)

        self.Latitude.appendChild(self.Latitude_value)

        self.Mfids.appendChild(self.Latitude)

    #创建节点DeviceIp-绿色server的ip
    #传入ip
    def create_DeviceIp(self, deviceIp):

        self.DeviceIp = self.dom.createElement('DeviceIp')
        self.DeviceIp_value = self.dom.createTextNode(deviceIp)

        self.DeviceIp.appendChild(self.DeviceIp_value)

        self.Mfids.appendChild(self.DeviceIp)

    #创建节点DevicePort-绿色server的端口
    #传入端口
    def create_DevicePort(self, devicePort):

        self.DevicePort = self.dom.createElement('DevicePort')
        self.DevicePort_value = self.dom.createTextNode(devicePort)

        self.DevicePort.appendChild(self.DevicePort_value)

        self.Mfids.appendChild(self.DevicePort)

    #创建节点TcpServerIp-tcp连接ip
    #传入ip
    def create_TcpServerIp(self, tcpServerIp):

        self.TcpServerIp = self.dom.createElement('TcpServerIp')
        self.TcpServerIp_value = self.dom.createTextNode(tcpServerIp)

        self.TcpServerIp.appendChild(self.TcpServerIp_value)

        self.Mfids.appendChild(self.TcpServerIp)

    #创建节点TcpServerPort-tcp连接端口
    #传入端口
    def create_TcpServerPort(self, tcpServerPort):

        self.TcpServerPort = self.dom.createElement('TcpServerPort')
        self.TcpServerPort_value = self.dom.createTextNode(tcpServerPort)

        self.TcpServerPort.appendChild(self.TcpServerPort_value)

        self.Mfids.appendChild(self.TcpServerPort)

    #循环节点
    #创建DeviceItems-设备信息
    #传入设备id，名称，原子服务端口号
    def create_DeviceItems(self, deviceId, deviceName, bServerPort):

        self.DeviceItems = self.dom.createElement('DeviceItems')

        #创建节点DeviceId-设备id
        self.DeviceId = self.dom.createElement('DeviceId')
        self.DeviceId_value = self.dom.createTextNode(deviceId)

        self.DeviceId.appendChild(self.DeviceId_value)
        self.DeviceItems.appendChild(self.DeviceId)

        #创建节点DeviceName-设备名称
        self.DeviceName = self.dom.createElement('DeviceName')
        self.DeviceName_value = self.dom.createTextNode(deviceName)

        self.DeviceName.appendChild(self.DeviceName_value)
        self.DeviceItems.appendChild(self.DeviceName)

        #创建节点BServerPort-原子服务端口
        self.BServerPort = self.dom.createElement('BServerPort')
        self.BServerPort_value = self.dom.createTextNode(bServerPort)

        self.BServerPort.appendChild(self.BServerPort_value)
        self.DeviceItems.appendChild(self.BServerPort)

        #将DeviceItems加入到Mfids节点中
        self.Mfids.appendChild(self.DeviceItems)


    #将Mfids节点加入根节点
    def append_Mfids(self):

        self.root.appendChild(self.Mfids)


    #将xml内容保存到文件中
    def write_to_file(self):

        file_name = time.strftime("%Y%M%d%H%M%S", time.localtime()) + '_DeviceRegister.xml'

        with open('../../data/DeviceRegister/%s' % file_name , 'w' , encoding='utf -8' ) as f :

            self.dom.writexml(f, addindent='\t', newl='\n', encoding='utf-8')

if __name__ == '__main__':

    sx = Structure_Xml()

    sx.create_Mfids()
    sx.create_Mfid('15000000240002')
    sx.create_MfidName('测试监测站')
    sx.create_Longitude('131.89026083978371')
    sx.create_Latitude('31.890260839783707')
    sx.create_DeviceIp('127.0.0.1')
    sx.create_DevicePort('20010')
    sx.create_TcpServerIp('127.0.0.1')
    sx.create_TcpServerPort('30016')

    for i in range(3):
        sx.create_DeviceItems('7794d32f-82cd-488c-abf6-ad77ece6798e', 'demo1', '8010')

    sx.append_Mfids()
    sx.write_to_file()


