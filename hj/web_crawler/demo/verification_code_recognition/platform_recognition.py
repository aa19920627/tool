#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : platform_recognition.py
# @Time : 2025/12/4 17:05

'''使用打码平台识别验证码'''
import io
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from web_crawler.demo.verification_code_recognition.captcha_platform.chaojiying import Chaojiying

USERNAME = 'hongjian829'
PASSWORD = 'i821jhde'
SOFT_ID = 975697  # 软件编号，超级鹰后台生成

# 数字英文验证码
CAPTCHA_KIND = '1006'
FILE_NAME = r'./captcha_platform/captcha1.png'
client = Chaojiying(USERNAME, PASSWORD, SOFT_ID)
result = client.post_pic(open(FILE_NAME, 'rb').read(),CAPTCHA_KIND)
print(result)

# 点选验证码
CAPTCHA_KIND = '9004'
FILE_NAME = r'./captcha_platform/captcha2.png'
client = Chaojiying(USERNAME, PASSWORD, SOFT_ID)
result = client.post_pic(open(FILE_NAME, 'rb').read(),CAPTCHA_KIND)
print(result)

# 滑动验证码
# 使用opencv添加自定义文字，提醒标注人员需要标注的位置
CAPTCHA_KIND = '9101'
FILE_NAME = r'./captcha_platform/captcha3.png'

def cv2_add_text(image, text, left, top, textColor=(255, 0, 0), text_size=20):
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font='./captcha_platform/simsun.ttc', size=text_size, encoding="utf-8")
    draw.text((left, top), text, textColor, font=font)
    return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)

image = cv2.imread(FILE_NAME)
image = cv2_add_text(image, '请点击目标缺口的左上角', int(image.shape[1] / 10), int(image.shape[0] / 2), (255, 0, 0),
                     40)
client = Chaojiying(USERNAME, PASSWORD, SOFT_ID)
#cv2.imencode('.png', image)将 OpenCV 图像编码为 PNG 格式的字节数据,[1]取元组的第二个元素，即编码后的字节缓冲区
#io.BytesIO(...)将 NumPy 数组转换为字节流对象
#.getvalue()从 BytesIO 对象中获取完整的字节数据
result = client.post_pic(io.BytesIO(cv2.imencode('.png', image)[1]).getvalue(), CAPTCHA_KIND)
print(result)

# 标记返回的坐标，验证一下
image = cv2.imread(FILE_NAME)
image = cv2.circle(image, (192, 92), radius=10, color=(255, 0, 0), thickness=1)
cv2.imwrite(FILE_NAME, image)

# 问答验证码
CAPTCHA_KIND = '6004'
FILE_NAME = r'./captcha_platform/captcha4.png'
client = Chaojiying(USERNAME, PASSWORD, SOFT_ID)
result = client.post_pic(open(FILE_NAME, 'rb').read(),CAPTCHA_KIND)
print(result)
