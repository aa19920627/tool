# -*- encoding: utf-8 -*-
"""
@File    : test_readyDataTasks.py
@Time    : 2020/12 11:41
@Author  : 胡元腾
@Software: PyCharm
"""
import pymysql
import sys
import os
import requests
from tkinter import *
#打包方式
#0、在cmd界面安装 pip install pyinstaller
#1、在cmd界面进入test_readyDataTasks.py脚本所在路径
#2、执行命令 pyi-makespec -F test_readyDataTasks.py
#3、修改生成的spec文件并指定与exe文件同级的用于读写数据的文件夹目录datas=[('data','data')]
#4、执行 pyinstaller -F test_readyDataTasks.spec生成exe文件
#另：很好的客户端前端包 PyQt5
LOG_LINE_NUM = 0
#生成资源文件目录访问路径
def resource_path(relative_path):
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#访问res文件夹下ConfessionBallon.MP3的内容
Devicespath = resource_path(os.path.join("data","Devices"))
Taskspath = resource_path(os.path.join("data","Tasks"))
serverpath = resource_path(os.path.join("data","server"))
DevicesXmlpath = resource_path(os.path.join("data","Devices.xml"))
TasksXmlpath = resource_path(os.path.join("data","Tasks.xml"))

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("批量注册工具")                             #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('550x450+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签&文本框
        self.startNum = Label(self.init_window_name, text="设备开始编号")
        self.startNum.grid(row=1, column=5,rowspan=2)
        self.startNum_Text = Text(self.init_window_name, width=30, height=1)  # 原始数据录入框
        self.startNum_Text.grid(row=1, column=10, rowspan=1, columnspan=2)

        self.numOfEqu = Label(self.init_window_name, text="设备总数")
        self.numOfEqu.grid(row=3, column=5,rowspan=2)
        self.numOfEqu_Text = Text(self.init_window_name, width=30, height=1)  #原始数据录入框
        self.numOfEqu_Text.grid(row=3, column=10, rowspan=1, columnspan=2)

        self.equName = Label(self.init_window_name, text="设备前缀")
        self.equName.grid(row=5, column=5, rowspan=2)
        self.equName_Text = Text(self.init_window_name, width=30, height=1)  # 原始数据录入框
        self.equName_Text.grid(row=5, column=10, rowspan=1, columnspan=2)

        self.controlIP = Label(self.init_window_name, text="管控地址")
        self.controlIP.grid(row=7, column=5, rowspan=2)
        self.controlIP_Text = Text(self.init_window_name, width=30, height=1)  # 原始数据录入框
        self.controlIP_Text.grid(row=7, column=10, rowspan=1, columnspan=2)

        self.atomIP = Label(self.init_window_name, text="原子服务地址")
        self.atomIP.grid(row=9, column=5, rowspan=2)
        self.atomIP_Text = Text(self.init_window_name, width=30, height=1)  # 原始数据录入框
        self.atomIP_Text.grid(row=9, column=10, rowspan=1, columnspan=2)

        self.mfidList = Label(self.init_window_name, text="监测站idList")
        self.mfidList.grid(row=13, column=5, rowspan=2)
        self.mfidList_Text = Text(self.init_window_name, width=30, height=5)  # 原始数据录入框
        self.mfidList_Text.grid(row=13, column=10, rowspan=1, columnspan=2)

        self.logs = Label(self.init_window_name, text="消息")
        self.logs.grid(row=15, column=20, rowspan=2)
        self.logs_Text = Text(self.init_window_name, width=30, height=10)  # 原始数据录入框
        self.logs_Text.grid(row=17, column=20, rowspan=1, columnspan=2)

        self.mfName = Label(self.init_window_name, text="监测站nameList")
        self.mfName.grid(row=15, column=5, rowspan=2)
        self.mfName_Text = Text(self.init_window_name, width=30, height=5)  # 原始数据录入框
        self.mfName_Text.grid(row=15, column=10, rowspan=1, columnspan=2)

        self.equNumPerStation = Label(self.init_window_name, text="每个站的设备个数")
        self.equNumPerStation.grid(row=11, column=5, rowspan=2)
        self.equNumPerStation_Text = Text(self.init_window_name, width=30, height=1)  # 原始数据录入框
        self.equNumPerStation_Text.grid(row=11, column=10, rowspan=1, columnspan=2)

        self.abilityList = Label(self.init_window_name, text="设备能力list")
        self.abilityList.grid(row=17, column=5, rowspan=2)
        self.abilityList_Text = Text(self.init_window_name, width=30, height=5)  # 原始数据录入框
        self.abilityList_Text.grid(row=17, column=10, rowspan=1, columnspan=2)

        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="开始", bg="lightblue", width=10,command=self.GreenDevices)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=20, column=11)


    def GreenDevices(self):
#获取输入变量值
        startNum = self.startNum_Text.get(1.0, END).strip().replace("\n", "").encode()
        numOfEqu = self.numOfEqu_Text.get(1.0, END).strip().replace("\n", "").encode()
        equName = self.equName_Text.get(1.0, END).strip().replace("\n", "").encode()
        controlIP = self.controlIP_Text.get(1.0, END).strip().replace("\n", "").encode()
        atomIP = self.atomIP_Text.get(1.0, END).strip().replace("\n", "").encode()
        srcmfidList = self.mfidList_Text.get(1.0, END).strip().replace("\n", "").encode()
        mfName = self.mfName_Text.get(1.0, END).strip().replace("\n", "").encode()
        equNumPerSation = self.equNumPerStation_Text.get(1.0, END).strip().replace("\n", "").encode()
        abilityList = self.abilityList_Text.get(1.0, END).strip().replace("\n", "").encode()
#变量类型处理
        endNum = int(startNum) + int(numOfEqu)
        startN = int(startNum)
        equNumPerStation = int(equNumPerSation)
        equName = str(equName,encoding="utf8")
        atomIP =  str(atomIP,encoding="utf8")
        numOfEqu = int(numOfEqu)
        controlIP = str(controlIP,encoding="utf8")
        mfidList = str(srcmfidList,encoding="utf8")
        mfidList = mfidList.split(",")
        mfName = str(mfName,encoding="utf8")
        mfName = mfName.split(",")
        abilityList = str(abilityList, encoding="utf8")
        abilityList = abilityList.split(",")

        #self.logs_Text.insert(1.0, os.path.abspath("."))

###########生成绿server文件####################################
    #执行完后将Devices.xml,Tasks.xml文件替换到绿server路径D:\Program Files (x86)\DeviceManagerBJ\Server\Config\
###########################################
    ##def GreenDevices(self):生成绿server文件Devices.xml
        try:
            with open(DevicesXmlpath,"w+") as f:
                f.write("<Devices>")

            for num in range(startN,endNum):
                name = equName + str(num)
            #self.logs_Text.insert(1.0, name)
                with open(Devicespath, "r", encoding="utf-8") as f1,open(DevicesXmlpath,"a",encoding="utf-8") as f2:
                    for line in f1:
                        if "%s" in line:
                            line = line.replace("%s", name)
                        f2.write(line)

            with open(DevicesXmlpath,"a",encoding="utf-8") as f2:
                f2.write("</Devices>")
            self.logs_Text.insert(1.0, "绿server,Devices.xml文件生成成功\n")

##########################################
    ##def GreenTasks(self):生成绿server文件Tasks.xml
            with open(TasksXmlpath,"w+") as f:
                f.write("<Tasks>")

            for num in range(startN,endNum):
                name = equName + str(num)
                with open(Taskspath, "r", encoding="utf-8") as f1,open(TasksXmlpath,"a",encoding="utf-8") as f2:
                    for line in f1:
                        if "%s" in line:
                            line = line.replace("%s", name)
                        f2.write(line)

            with open(TasksXmlpath,"a",encoding="utf-8") as f2:
                f2.write("</Tasks>")
            self.logs_Text.insert(1.0, "绿server,Tasks.xml文件生成成功\n")
        except Exception as e:
            self.logs_Text.insert(1.0, "文件操作失败\n")

##########生成原子服务数据#####################################
# 执行前手动添加站，执行后重启原子服务
        try:
            conn = pymysql.connect(database='dgbc_rmbt_v2',user='root',password='root',host=atomIP,port=3306,charset='utf8',autocommit=True)#
            cur = conn.cursor()
            #self.logs_Text.insert(1.0, "原子服务数据生成成功\n")

            for mfid in mfidList:
                endNum = startN + equNumPerStation
                while startN < endNum:
                    sql = "INSERT INTO `dgbc_rmbt_v2`.`rmbt_facility_equipment` (`EQUID`, `MFID`, `DEVICEID`, `EQUMODEL`, `EQUNAME`, `EQUIMANU`, `TASKNUM`, `EQUSN`, `IFBAND`, `DFBAND`, `EQUIP`, `EQUPORT`, `STARTFREQ`, `ENDFREQ`, `PROTOCOLADDRESS`, `TASKABILITY`, `ExtendFields`, `EQUTYPE`, `EQUWORKMODE`, `EQUSTATUS`) VALUES ('62491398-7275-4297-b42b-1b799ff1d%s', '%s', '5e2e339b-bf64-4845-a23e-8600b5676%s', '%s%s', '%s%s', '大公博创', '1', '00000000', NULL, NULL, '%s', '8010', '87.0000000', '108.0000000', 'D:\\\Program Files (x86)\\\DeviceManager\\\Server\\\DeviceTasks\\\Receiverdemo.xml', 'MultiMeasure,BroadMeasure,WDDF,SCANDF,FIXFQ,FSCAN,MSCAN,FIXDF,TDOA,VID,智能采集,通道', null, '01', '0', '01');"% (startN,mfid,startN,equName,startN,equName,startN,atomIP)
                    cur.execute(sql)
                    startN = startN + 1
                    #self.logs_Text.insert(1.0, "原子服务数据生成成功\n")

            startN = int(startNum)
            endNum = startN + int(numOfEqu)
            for num in range(startN, endNum):
                with open(serverpath, "r") as f1:
                    for line in f1:
                        sql = line%(num,num)
                        cur.execute(sql)
            self.logs_Text.insert(1.0, "原子服务数据生成成功\n")
            cur.close()
            conn.close()
        except Exception as e :
            self.logs_Text.insert(1.0, "原子服务数据库连接错误\n")

###########生成管控设备能力数据#####################################
# 执行前手动添加站
        data = '''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:srrc="http://www.srrc.org.cn">
   <soapenv:Header>
      <srrc:MonitorHeader>
         <!--Optional:-->
         <srrc:TransId>?</srrc:TransId>
         <!--Optional:-->
         <srrc:BizKey>?</srrc:BizKey>
         <!--Optional:-->
         <srrc:PSCode>?</srrc:PSCode>
         <!--Optional:-->
         <srrc:BSCode>?</srrc:BSCode>
         <!--Optional:-->
         <srrc:appCode>?</srrc:appCode>
         <!--Optional:-->
         <srrc:appName>?</srrc:appName>
         <!--Optional:-->
         <srrc:platFormCode>?</srrc:platFormCode>
         <!--Optional:-->
         <srrc:platFormName>?</srrc:platFormName>
         <!--Optional:-->
         <srrc:resCode1>?</srrc:resCode1>
         <!--Optional:-->
         <srrc:resCode2>?</srrc:resCode2>
      </srrc:MonitorHeader>
   </soapenv:Header>
   <soapenv:Body>
      <srrc:requestbody>
         <!--监测站ID，先注册站:-->
         <srrc:mfid>%s</srrc:mfid>
         <!--监测站名称:-->
         <srrc:mfname>%s</srrc:mfname>
         <!--设备ID:-->
         <srrc:equid>%s</srrc:equid>
         <!--设备名称:-->
         <srrc:equname>%s</srrc:equname>
         <!--Optional:-->
         <srrc:baseserviceurl>%s</srrc:baseserviceurl>
         <!--Optional:-->
         <srrc:baseserviceproxyurl>127.0.0.1</srrc:baseserviceproxyurl>
         <!--能力，每次只能注册一条能力:-->
         <srrc:feature>%s</srrc:feature>
         <!--Optional:-->
         <srrc:exinfo>
            <!--扩展信息，BSCode&PSCode:-->
            <srrc:item>
               <srrc:paraname>bscode</srrc:paraname>
               <srrc:paravalue>1</srrc:paravalue>
            </srrc:item>
            <srrc:item>
               <srrc:paraname>pscode</srrc:paraname>
               <srrc:paravalue>1</srrc:paravalue>
            </srrc:item>
         </srrc:exinfo>
      </srrc:requestbody>
   </soapenv:Body>
</soapenv:Envelope>
'''

        url = 'http://' + controlIP + ':57000/Monitor/M_RegisterEquip'
        header = {'Content-Type': 'text/xml;charset=UTF-8', 'SOAPAction': 'M_RegisterEquip', 'Connection': 'keep-alive'}

        if abilityList[0]=='':
            abilityList=['B_QueryDeviceInfo', 'B_QueryFaciDevStat', 'B_SglFreqMeas', 'B_FScan', 'B_PScan', 'B_StopMeas','B_SglFreqDF', 'B_SelfTest', 'B_TaskModification']

        try:
            for index in range(len(mfidList)):
                endNum = startN + equNumPerStation
                mfname1 = mfName[index]
                for num in range(startN, endNum):
                    for ability in abilityList:
                        equNam = equName + str(num)
                        baseserviceurl = 'http://' + atomIP + ':8010/' + str(mfidList[index]) + '/' + equNam + '/' + ability
                        equid = '5e2e339b-bf64-4845-a23e-8600b5676' + str(num)
                        mfid = mfidList[index]

                        data1 = data % (mfid, mfname1, equid, equNam, baseserviceurl, ability)
                        data2 = data1.encode("UTF-8")
                        re = requests.post(url=url, data=data2, headers=header)
                        assert '调用成功' in re.text
                        assert re.status_code == 200
                startN = startN + equNumPerStation
            self.logs_Text.insert(1.0, "管控数据生成成功\n")
        except Exception as e:
            self.logs_Text.insert(1.0, "管控接口调用失败\n")

def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()