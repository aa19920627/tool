#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 洪建
# @File : ocr_recognition.py
# @Time : 2025/12/2 14:55

"""ocr技术识别验证码"""
import os
import re
import time
from io import BytesIO
import numpy
import tesserocr
from PIL import Image
from retrying import retry
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# 处理图片，让识别更准确
def preprces(image):
    image = image.convert('L')  # 将图片二值化
    array = numpy.array(image)
    # numpy的where方法对数组进行筛选和处理，将灰度值大于阈值的图片像素设置为255，表示白色，否则设置为0，表示黑色
    array = numpy.where(array > 90, 255, 0)
    image = Image.fromarray(array.astype('uint8'))
    return image


# 通过retry来指定重试条件和重试次数
@retry(stop_max_attempt_number=10, retry_on_result=lambda x: x is False)
def login():
    browser.get(url='https://captcha7.scrape.center/')
    browser.find_element(By.CSS_SELECTOR, '.username input[type="text"]').send_keys('admin')
    browser.find_element(By.CSS_SELECTOR, '.password input[type="password"]').send_keys('admin')
    captcha = browser.find_element(By.CSS_SELECTOR, '#captcha')
    image = Image.open(BytesIO(captcha.screenshot_as_png))
    image = preprces(image)
    # OCR识别验证码，若无法获取到tessdata的路径，需手动指定
    captcha = tesserocr.image_to_text(image, path=r'D:\Tesseract-OCR\tessdata')
    captcha = re.sub('[^A-Za-z0-9]', '', captcha)
    browser.find_element(By.CSS_SELECTOR, '.captcha input[type="text"]').send_keys(captcha)
    browser.find_element(By.CSS_SELECTOR, '.login').click()

    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//h2[contains(.,"登录成功")]')))
        time.sleep(10)
        browser.close()
        return True
    except TimeoutException:
        return False

if __name__ == '__main__':
    browser = webdriver.Chrome()
    login()
