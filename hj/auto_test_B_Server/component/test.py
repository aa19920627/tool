import xml.etree.ElementTree as ET
import xmltodict
import json

tree = ET.parse('../data/xml/your_data.xml')
root = tree.getroot()
# here you can change the encoding type to be able to set it to the one you need

root_new = root[1][0]
print(root_new.tag)
root_new.find('{http://www.srrc.org.cn}mfid').text = '37020001120014'
new_node = ET.Element('srrc:new')
new_node.text = '新增'
root[1][0].append(new_node)
ET.register_namespace('soapenv', 'http://schemas.xmlsoap.org/soap/envelope/')
ET.register_namespace('srrc', 'http://www.srrc.org.cn')
tree.write('your_data.xml', 'utf-8', 'xml')

str_list = ET.tostring(root)
