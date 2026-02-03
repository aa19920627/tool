from urllib.parse import urljoin
from selenium import webdriver
import requests
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = 'https://login2.scrape.center/'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

# 配置chrome程序的路径
chrom_path = r"D:\Selenium\chrome-win64\chrome-win64\chrome.exe"
options = Options()
options.binary_location = chrom_path

# 启动浏览器并自动登录
browser = webdriver.Chrome(options=options)
browser.get(BASE_URL)
browser.find_element(By.CSS_SELECTOR,'input[name="username"]').send_keys(USERNAME)
browser.find_element(By.CSS_SELECTOR,'input[name="password"]').send_keys(PASSWORD)
browser.find_element(By.CSS_SELECTOR,'input[type="submit"]').click()
time.sleep(10)  # 等待登录跳转

# 提取登录态 Cookie
cookies = browser.get_cookies()
browser.close()

# 携带 Cookie 请求目标页面
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

response = session.get(INDEX_URL)
print('状态码:', response.status_code)
print('最终URL:', response.url)
