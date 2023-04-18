'''
@Author: 洪建
@Date 2023/4/18 17:11
'''
from hj.small_tool.main.registration_Integration_Information import Make_Data

#读取一体化导出的服务信息表，批量更新PSCode和总线地址
Make_Data().read_excel()