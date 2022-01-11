'''
@Author：洪建
@Date：2021/12/31 16:20
加载配置文件
'''
import yaml
import os

# 获取配置文件路径
CONFIG_PATH = os.path.join(os.path.dirname(__file__) + '/../config/config.yaml')
# 读取配置文件
with open(CONFIG_PATH, encoding='utf-8') as f:
    cv = yaml.safe_load(f)


# 数据库配置
def database_config():
    # 返回数据库名
    return cv['DATABASE']['db']


# 可测试设备操作能力列表
def feature_list_config():
    # 返回能力列表
    return cv['FEATURE']['featurelist']


#  ip地址
def host_config():
    # 返回ip地址
    return cv['HOST']['host']


if __name__ == '__main__':
    print(type(feature_list_config()))
