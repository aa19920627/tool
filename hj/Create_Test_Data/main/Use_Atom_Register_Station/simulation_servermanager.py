# -*- encoding: utf-8 -*-
"""
@File    : simulation_servermanager.py
@Date    : 2021/8/18 11:50
@Author  : 洪建
"""
import os
from xml.dom import minidom

#模拟在绿色server中创建Demo设备



#创建Devices.xml
class Simulation_Servermanager:

    def writer_Devices(self):


        filepath = '../../data/DeviceRegister/Devices.xml'

        domTree = minidom.getDOMImplementation().createDocument(None, 'Devices', None)
        rootNode = domTree.documentElement


        for num in range(1,41):

            name = "Demo" + str(num)
            customer_node = domTree.createElement("Devices")  # 创建子节点，
            customer_node.setAttribute("Assemble", "Devices\Receiver\ReceiverDemo.dll")
            customer_node.setAttribute("Name", name)
            customer_node.setAttribute("Load", "-1")
            customer_node.setAttribute("Catalog", "Receiver")
            rootNode.appendChild(customer_node)  # 将他们挂在跟节点上


            key = domTree.createElement('AudioDataSize')# 创建子节点，
            key_text = domTree.createTextNode('0')  # 元素内容写入
            key.appendChild(key_text)
            customer_node.appendChild(key)# 将他们挂在Devices节点上

            key = domTree.createElement('AudioFilePath')  # 创建子节点，
            customer_node.appendChild(key)

            key = domTree.createElement('AudioSampleRate')  # 创建子节点，
            key_text = domTree.createTextNode('22050')  # 元素内容写入
            key.appendChild(key_text)
            customer_node.appendChild(key)# 将他们挂在Devices节点上

            key = domTree.createElement('DataDir')  # 创建子节点，
            customer_node.appendChild(key)

            key = domTree.createElement('DataFileRelated')  # 创建子节点，
            key_text = domTree.createTextNode('FALSE')  # 元素内容写入
            key.appendChild(key_text)
            customer_node.appendChild(key)

            key = domTree.createElement('DataFolderPath')  # 创建子节点，
            customer_node.appendChild(key)

            key = domTree.createElement('FramesPerSec')  # 创建子节点，
            key_text = domTree.createTextNode('0.000000')  # 元素内容写入
            key.appendChild(key_text)
            customer_node.appendChild(key)

            key = domTree.createElement('IP')  # 创建子节点，
            key_text = domTree.createTextNode('127.0.0.1')  # 元素内容写入
            key.appendChild(key_text)
            customer_node.appendChild(key)

            key = domTree.createElement('Port')  # 创建子节点，
            key_text = domTree.createTextNode('5555')  # 元素内容写入
            key.appendChild(key_text)
            customer_node.appendChild(key)

            key = domTree.createElement('ReadCirclely')  # 创建子节点，
            key_text = domTree.createTextNode('FALSE')  # 元素内容写入
            key.appendChild(key_text)
            customer_node.appendChild(key)

            key = domTree.createElement('recorder')  # 创建子节点，
            key_text = domTree.createTextNode('0')  # 元素内容写入
            key.appendChild(key_text)
            customer_node.appendChild(key)

        with open(filepath, 'w', encoding='utf-8') as f:
            domTree.writexml(f, addindent='  ')


#创建文件Tasks.xml
class Write_Data_Tasks:

    def write_Tasks(self):

        for num in range(1,41):

            name = "Demo" + str(num)

            with open('../../data/DeviceRegister/Tasks_Demo.xml', "r", encoding="utf-8") as f1,\
                    open("../../data/DeviceRegister/Tasks.xml","a",encoding="utf-8") as f2:

                for line in f1:
                    if "%s" in line:
                        line = line.replace("%s", name)
                    f2.write(line)


if __name__ == '__main__':


    Simulation_Servermanager().writer_Devices()
    # Write_Data_Tasks().write_Tasks()