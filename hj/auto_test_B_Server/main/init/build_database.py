'''
@Author：洪建
@Date：2021/12/31 14:02

初始化数据库
'''
from component.loading_config import database_config
from component.sqlite_method import ManageSqlite

# 数据库名
DATABASE_NAME = database_config()


def build_database():
    # 初始化数据库连接类
    _ms = ManageSqlite(DATABASE_NAME)

    # 创建station表，存放监测站基本信息
    sql_station = '''CREATE TABLE IF NOT EXISTS station
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                mfid VARCHAR (14),
                mfname VARCHAR (50),
                area VARCHAR (6))
    '''
    # 创建device表，存放设备信息
    sql_device = '''CREATE TABLE IF NOT EXISTS device
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                mfid VARCHAR(14),
                mfname VARCHAR (50),
                equid VARCHAR (50),
                equname VARCHAR (50),
                type VARCHAR (1),
                ip VARCHAR (50),
                port VARCHAR (50)
                )
    '''
    # 创建function表，存放设备能力
    sql_function = '''CREATE TABLE IF NOT EXISTS function
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                mfid VARCHAR(14),
                mfname VARCHAR (50),
                equid VARCHAR (50),
                equname VARCHAR (50),
                fuc_name VARCHAR (50),
                fuc_en_name VARCHAR (50),
                url VARCHAR (255),
                request_message VARCHAR (10000)
                )
    '''
    # 创建function_base_info表，存放设备基础能力对照表
    sql_base_function = '''CREATE TABLE IF NOT EXISTS function_base_info
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fuc_en_name VARCHAR (50), 
                    fuc_name VARCHAR (50)   
                    )
    '''
    # 执行sql
    _ms.operation_sqlite(sql_station,sql_device,sql_function,sql_base_function)
    # 关闭连接
    _ms.close_cur_conn()


def build_base_data():
    # 初始化sqlite操作类
    _ms = ManageSqlite(DATABASE_NAME)

    # 创建设备能力的基本数据，往function_base_info中插入数据
    data_list = [
        ('B_SglFreqMeas', '单频测量'),
        ('B_WBFFTMon', '宽带FFT频谱观测'),
        ('B_FScan', '频率扫描频谱观测'),
        ('B_PScan', '全景扫描频谱观测'),
        ('B_MScan', '存储频率列表扫描'),
        ('B_SglFreqDF', '单频测向'),
        ('B_WBDF', '宽带FFT测向'),
        ('B_FScanDF', '扫频测向'),
        ('B_MScanDF', '频率表扫描测向'),
        ('B_StopMeas', '停止测量任务'),
        ('B_QueryFaciDevStat', '监测站/设备状态查询'),
        ('B_QueryDeviceInfo', '监测设备信息查询')
    ]

    # 批量插入的通用sql
    sql = 'INSERT INTO function_base_info (fuc_en_name,fuc_name) VALUES (?,?)'

    _ms.insert_many(sql, data_list)
    _ms.close_cur_conn()


if __name__ == '__main__':
    build_database()
    build_base_data()
