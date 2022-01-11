'''
@Author：洪建
@Date：2021/12/31 17:28
1.通过B_QueryDeviceInfo生成其他设备能力
2.将能力写入数据库function表
'''
import os
import random
from component.loading_config import database_config, feature_list_config, host_config
from component.manage_xml import ManageXml
from component.sqlite_method import ManageSqlite
from main.base_component.request_interface import RequestInterface
from main.function_module.register_center.register import RegisterStationDevice

DATABASE_NAME = database_config()
HOST_ADDRESS = host_config()


# 设备能力生成类
class GenerateFunction(object):

    def __init__(self):
        # 初始化sqlite操作类
        self.ms = ManageSqlite(DATABASE_NAME)

    # 获取注册设备能力url的基本信息，包括ip,port,mfid,equname
    # 返回原子服务url
    def get_function_base_info(self, equid, b_feature):
        # 获取设备基本信息
        mfid, equname, ip, port = self.ms.get_fetchone(
            "SELECT mfid,equname,ip,port FROM device WHERE equid = '%s'" % equid)
        # 组装原子服务url
        url = 'http://%s:%s/%s/%s/%s' % (ip, port, mfid, equname, b_feature)

        return url, mfid

    # 生成设备操作服务的请求报文,返回设备能力基本信息列表
    # 返回列表中字典示例{'mfid': mfid, 'euqid': equid, 'url': url, 're_message': request_xml_string,
    #                      'SoapAction': feature_soapaction}
    def generate_equip_operation_xml(self, equid):

        # 获取B_QueryDeviceInfo接口的mfid,equid,url
        url, mfid = self.get_function_base_info(equid, 'B_QueryDeviceInfo')
        # 调用B_QueryDeviceInfo的响应报文
        b_query_device_info_respose = RequestInterface().get_B_QueryDeviceInfo(mfid, equid, url)
        # 解析报文feature的,生成feature列表
        # 实例化xml操作类
        mx = ManageXml(xml_string=b_query_device_info_respose)
        # 获取featurelist对象
        featurelist = mx.root.find('.//srrc:featurelist', mx.ns)

        '''
        下面请求报文的组装
        '''
        # 定义一个设备能力基本信息列表
        feature_base_info_list = []
        # 获取feature对象,暂时只支持常见能力
        for i in featurelist.findall('.//srrc:feature', mx.ns):
            # print(featurelist.findall('.//srrc:feature', mx.ns))
            # 判断支持的能力
            if i.find('.//srrc:code', mx.ns).text in feature_list_config():
                # 实例化设备操作服务报文的操作类
                mx_feature = ManageXml(xml_file_name='feature_common.xml')
                # 添加节点srrc:equpara
                equpara_node = mx_feature.append_code(mx_feature.root.find('.//srrc:requestbody', mx_feature.ns),
                                                      'srrc:equpara')
                # B_FScan和B_PScan请求报文中参数列表比较特殊,需要特殊处理
                feature_soapaction = i.find('.//srrc:code', mx.ns).text
                if feature_soapaction in ('B_FScan', 'B_FScan'):
                    # 添加节点srrc:groupitems,srrc:groupitem,srrc:groupid,srrc:items
                    groupitems_node = mx_feature.append_code(equpara_node, 'srrc:groupitems')
                    groupitem_node = mx_feature.append_code(groupitems_node, 'srrc:groupitem')
                    groupid_node = mx_feature.append_code(groupitem_node, 'srrc:groupid')
                    groupid_node.text = '1'
                    items_node = mx_feature.append_code(groupitem_node, 'srrc:items')
                else:
                    # FSCAN和PSCAN之外,都没有groupitems节点,直接添加items节点
                    items_node = mx_feature.append_code(equpara_node, 'srrc:items')

                '''
                下面是item节点，存放参数，循环节点
                '''
                # 定义一个列表,用来接收item
                item_list = []
                # 循环获取响应报文中srrc:parameter节点,作为item节点中paraname和paravalue的输入
                for parameter in i.findall('.//srrc:parameter', mx.ns):
                    # 获取srrc:parameter中displayname和defaultvalue节点的值,作为请求报文中paraname,paravalue的输入
                    name = parameter.find('.//srrc:displayname', mx.ns).text
                    defaultvalue = parameter.find('.//srrc:defaultvalue', mx.ns).text

                    # 添加srrc:item节点
                    item_node = mx_feature.append_code(items_node, 'srrc:item')
                    # 添加srrc:paraname和srrc:paravalue节点和对应的值,paravalue为提取的默认值
                    paraname_node = mx_feature.append_code(item_node, 'srrc:paraname')
                    paraname_node.text = name
                    paravalue_node = mx_feature.append_code(item_node, 'srrc:paravalue')
                    paravalue_node.text = defaultvalue
                    item_list.append(item_node)
                # 添加多个item节点
                items_node.extend(item_list)
                # 添加outputchannel节点,定义数据传输方式
                outputchannel_node = mx_feature.append_code(mx_feature.root.find('.//srrc:requestbody', mx_feature.ns),
                                                            'srrc:outputchannel')
                # 添加mode节点，设置sink模式
                mode_node = mx_feature.append_code(outputchannel_node, 'srrc:mode')
                mode_node.text = 'sink'
                # 添加datachannel节点，设置为stream方式
                datachannel_node = mx_feature.append_code(outputchannel_node, 'srrc:datachannel')
                datachannel_node.text = 'stream'
                # 添加host节点，设置值为配置的ip地址
                host_node = mx_feature.append_code(outputchannel_node, 'srrc:host')
                host_node.text = HOST_ADDRESS
                # 添加port节点，接收数据的端口
                port_node = mx_feature.append_code(outputchannel_node, 'srrc:port')
                port_node.text = str(random.randint(60000, 65000))
                # 添加stc节点,stream唯一标志
                stc_node = mx_feature.append_code(outputchannel_node, 'srrc:stc')
                stc_node.text = 'test'
                # 保存报文
                mx_feature.write_xml()

                # 再读取文件，返回字符串
                path = os.path.join(os.path.dirname(__file__), '../../../data/xml/temp.xml')
                request_xml_string = mx.get_xml_string(path)
                # 获取url
                url, mfid = self.get_function_base_info(equid, feature_soapaction)

                # 将装有设备能力基本信息的字典添加到列表中
                feature_base_info_list.append(
                    {'mfid': mfid, 'equid': equid, 'url': url, 're_message': request_xml_string,
                     'SoapAction': feature_soapaction})

        return feature_base_info_list

    # 将设备能力写入数据库
    def register_equip_operation(self, equid):

        # 获取设备服务基本信息
        feature_base_info_list = self.generate_equip_operation_xml(equid)

        # 写入数据库
        RegisterStationDevice().insert_function_info(feature_base_info_list)


if __name__ == '__main__':
    gf = GenerateFunction().register_equip_operation('a6590676-f5a7-4220-b105-a6ea4edbd77b')
