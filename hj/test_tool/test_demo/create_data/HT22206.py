# -*- coding: utf-8 -*-
"""
@Time ： 2024/9/12 11:01
@Auth ： 洪建
"""
import time
from symtable import Class

import requests
from PIL.ImImagePlugin import number
from faker import Faker
import random

from faker.providers import BaseProvider
from faker.providers.person.pl_PL import checksum_identity_card_number
from openpyxl.workbook import Workbook

'''重大活动保障补充测试，生成用户数据'''



# 模拟数据
class Faker_Data:
    def __init__(self):
        # 初始化 Faker 并指定语言为中文
        self.fake = Faker("zh_CN")


    def faker_name(self):
        # 生成一个中文名字
        # 100个常见姓氏
        surnames = [
            "张", "李", "王", "刘", "陈", "杨", "赵", "黄", "周", "吴",
            "徐", "孙", "马", "朱", "胡", "郭", "林", "贺", "何", "高",
            "梁", "郝", "尹", "龚", "方", "常", "许", "钟", "郑", "潘",
            "杜", "戴", "任", "罗", "蔡", "彭", "白", "姚", "吕", "邓",
            "曹", "邵", "陶", "龚", "龙", "汪", "邱", "顾", "方", "常",
            "段", "伍", "任", "谢", "苏", "马", "潘", "阮", "江", "余",
            "凌", "王", "蔡", "周", "黄", "邓", "唐", "林", "江", "冯"
        ]
        # 200个常见名字
        names = [
            "伟", "芳", "娜", "敏", "静", "洋", "强", "磊", "勇", "军",
            "丽", "红", "梅", "秀", "娟", "婷", "娟", "娟", "燕", "娟",
            "峰", "刚", "平", "亮", "杰", "磊", "俊", "良", "进", "东",
            "霞", "媛", "萍", "玉", "梅", "珊", "莉", "雪", "燕", "静",
            "超", "磊", "云", "涛", "浩", "鹏", "峰", "亮", "勇", "刚",
            "梅", "芳", "杰", "静", "婷", "娜", "霞", "丽", "玲", "萍",
            "宁", "杰", "峰", "阳", "斌", "俊", "华", "浩", "杰", "鑫",
            "欣", "怡", "姗", "雨", "露", "萌", "雪", "玲", "莉", "婷",
            "诚", "心", "阳", "光", "晨", "星", "辉", "宇", "龙", "宇",
            "宇", "凤", "玲", "艳", "琴", "静", "丽", "慧", "涵", "笑",
            "林", "云", "华", "星", "涛", "宇", "霞", "丽", "菲", "丽",
            "燕", "娜", "婷", "萍", "琪", "媛", "欢", "珍", "婷", "瑞",
            "芳", "花", "梅", "秀", "丽", "珍", "玲", "艳", "琴", "茜",
            "瑶", "蓉", "倩", "璇", "文", "伟", "俊", "祥", "胜", "超"
        ]
        faker_name = random.choice(surnames) + random.choice(names)
        return faker_name

    # 生成电话号码
    def faker_telephone(self):
        faker_telephone = self.fake.phone_number()
        return faker_telephone

    # 生成邮箱
    def faker_email(self):

        emai_addr = str(random.randint(100000000, 999999999)) + "@qq.com"
        return emai_addr
    # 生成用户id
    def user_id(self, number):

        # 定义初始id
        chegndu_id = 51015500
        sichuan_id = 51005500
        userid_list = []

        for num in range(number):

            if chegndu_id == 51019999:
                sichuan_id += 1
                user_id = sichuan_id
            else:
                chegndu_id += 1
                user_id = chegndu_id
            userid_list.append(user_id)
        return userid_list


class ADD_USER:
    def __init__(self):
        self.re = requests.session()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization":"Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6ImQyNzQwYjMwLTIwNTMtNDgxYS05NTUyLTQ1MWQ3YzMxNzJmZiJ9.er4hZ2VVp2VU4hb0XfEcNHgqaU4vuy3XKI2O4wRe3FglReyfG6MxvAkIemqxKHN7FCKsOx3Hkc_IdNfoMh2sYA"
        }
        self.fd = Faker_Data()

        # 创建一个新的工作簿和工作表
        self.wb = Workbook()
        self.ws = self.wb.active

    def add_user(self, number):
        userid_list = self.fd.user_id(number)
        row_number = 1
        for i in range(number):
            password = str(random.randint(10000000, 99999999))
            data = {
                "userCode":str(userid_list[i]),
                "password": str(password),
                "userName": self.fd.faker_name(),
                "mobile": str(self.fd.faker_telephone()),
                "invalidDate": "2025-09-28 00:00:00",
                "phone": "028-83919542",
                "sex": "0",
                "position": "0111",
                "birthday": "2024-09-12 00:00:00",
                "technical": "24552",
                "countryEmail": self.fd.faker_email(),
                "ethnicity": "0",
                "localEmail": self.fd.faker_email(),
                "politic": "01",
                "userType": "1",
                "education": "21",
                "status": "1",
                "orgId": 1,
                "areaCode": "510100",
                "priority": "9",
                "userOrder": str(random.randint(1, 9999)),
                "roleIds": []
            }

            self.ws.cell(row=row_number, column=1).value = data['userCode']
            self.ws.cell(row=row_number, column=2).value = password
            row_number +=1
            res = self.re.request(url="http://192.168.36.110/rbac/api/system/user/add",
                            json=data,
                            headers=self.headers,method="POST")
            print(data)
            print(res.text)
            print(f"添加用户成功，用户名：{userid_list[i]}，密码：{password}")
            time.sleep(0.3)
        self.wb.save("./user.xlsx")


if __name__ == '__main__':
    # fd = Faker_Data()
    # id_list = fd.user_id(10002)
    # for i in range(10002):
    #     print(id_list[i])

    ADD_USER().add_user(10100)