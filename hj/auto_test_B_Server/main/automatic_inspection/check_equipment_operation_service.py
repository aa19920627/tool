'''
@Author：洪建
@Date：2022/1/11 13:38
该包用于检查设备操作服务的调用情况，检查步骤
1.调用结果
2.数据返回结果
其他要求：
1.重试n（可配置）次，间隔n（可配置）秒
'''

from main.base_component.request_interface import RequestInterface


class CheckRequest(object):
    '''
    检查调用的返回结果
    '''

    def __init__(self):
        # 实例化通用接口类
        self.ri = RequestInterface()

    def check_request_respose(self, equid, soapaction):
        # 检查调用设备操作服务后的响应结果
        res = self.ri.call_equipment_operation_service(equid,soapaction)
        print(res.text)

if __name__ == '__main__':

    cr = CheckRequest()
    cr.check_request_respose('a6590676-f5a7-4220-b105-a6ea4edbd77b', 'B_FScan')
