'''
@Author：洪建
@Date：2022/1/4 17:07
处理xml的通用方法
'''
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom


class ManageXml(object):
    '''
    处理xml文件和数据的通用方法
    '''

    def __init__(self, xml_file_name=None, xml_string=None):
        # 定义xml文件的相对路径
        self.xml_path = os.path.join(os.path.dirname(__file__), '../data/xml/%s' % xml_file_name)
        print(self.xml_path)
        # 定义临时xml位置
        self.temp_path = os.path.join(os.path.dirname(__file__), '../data/xml/temp.xml')
        # 判断输入对象是文件还是字符串,实例化方法不一样，xml_file_name是文件
        if xml_file_name != None:
            self.tree = ET.parse(self.xml_path)
            self.root = self.tree.getroot()
        else:
            self.root = ET.fromstring(xml_string)
            self.tree = ET.ElementTree(self.root)
        # 搜索命名空间的XML,为前缀创造一个字典，在搜索函数中使用他
        self.ns = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
                   'srrc': 'http://www.srrc.org.cn'}
        # 注册命名空间，避免写入导致命名空间为ns0的现象
        ET.register_namespace('soapenv', 'http://schemas.xmlsoap.org/soap/envelope/')
        ET.register_namespace('srrc', 'http://www.srrc.org.cn')

    # 新增子节点,parent_node父节点对象,child_node_name子节点名称
    def append_code(self, parent_node, child_node_name):

        new_parent_node = ET.SubElement(parent_node, child_node_name)
        return new_parent_node

    # 读取xml文件，返回字符串
    def get_xml_string(self, path):

        with open(path, encoding='utf-8') as f:
            return f.read()

    # 将xml对象element转换为字符串
    def tosrting_xml(self, element):

        # tostring生成的是byte类型，需要decode转换一下

        return ET.tostring(element, encoding='unicode').encode('utf-8')

    # 保存xml修改函数到临时文件
    def write_xml(self):
        # self.tree = ET.ElementTree(self.root)
        # 保存修改，写入临时xml文件
        # self.tree.write(self.temp_path, encoding='utf-8', method='xml', xml_declaration=True)
        xml_string = ET.tostring(self.root)
        dom = minidom.parseString(xml_string)

        with open(self.temp_path, 'w', encoding='utf-8') as f:
            dom.writexml(f, addindent='  ', indent='\t', newl="\n", encoding='utf-8')

    # 回收临时文件
    def delete_xml(self):

        os.remove(self.temp_path)


if __name__ == '__main__':
    mx = ManageXml(xml_file_name='your_data.xml')
    # print(mx.root[1].find('.//srrc:mfid', mx.ns))
    # for i in mx.root.iter('{http://www.srrc.org.cn}mfid') :
    #     print(i)

    # str_list = ET.tostring(mx.root)
    # print(str_list)
    # print(mx.to_string_xml())
    # for i in mx.root.iter('{http://www.srrc.org.cn}feature') :
    #
    #     print(i.find('{http://www.srrc.org.cn}code').text)
    featurelist = mx.root.find('.//srrc:featurelist', mx.ns)
    for i in featurelist.findall('.//srrc:feature', mx.ns):
        if i.find('.//srrc:code', mx.ns).text in (
                'B_FScan', 'B_PScan', 'B_SglFreqMeas', 'B_SglFreqDF', 'B_WBDF', 'B_FScanDF'):
            print(i.find('.//srrc:code', mx.ns).text)
