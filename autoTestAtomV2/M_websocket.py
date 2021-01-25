# -*- encoding: utf-8 -*-
"""
@File    : test_readyDataTasks.py
@Time    : 2020/12 11:41
@Author  : 胡元腾
@Software: PyCharm
"""
#打包方式
#0、在cmd界面安装 pip install pyinstaller
#1、在cmd界面进入test_readyDataTasks.py脚本所在路径
#2、执行命令 pyi-makespec -F test_readyDataTasks.py
#3、修改生成的spec文件并指定与exe文件同级的用于读写数据的文件夹目录datas=[('data','data')]
#4、执行 pyinstaller -F test_readyDataTasks.spec生成exe文件
#另：很好的客户端前端包 PyQt5
import websocket
import json
import _thread
from websocket import create_connection
import time
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import xlrd
LOG_LINE_NUM = 0
#生成资源文件目录访问路径

url1 = '''ws://%s:54008/ws/monitor'''  # 接口地址
#wav_path = "D:/001M26_01_01_0001.pcm"  # 音频文件地址

global action
global file_path
def on_message(ws, message):
   print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("close connection")

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    #设置窗口
    def set_init_window(self):
        global action
        self.init_window_name.title("巡检设备能力工具")                             #窗口名
        #self.init_window_name.geometry('320x160+100+100')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('810x470+100+150')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签&文本框
        self.PortalIP = Label(self.init_window_name, text="PortalIP（必填）")
        self.PortalIP.grid(row=1, column=6, rowspan=2)
        self.PortalIP_Text = Text(self.init_window_name, width=30, height=1)  # 原始数据录入框
        self.PortalIP_Text.grid(row=1, column=7, rowspan=1, columnspan=2)

        self.userID = Label(self.init_window_name, text="userID（必填）")
        self.userID.grid(row=3, column=6,rowspan=2)
        self.userID_Text = Text(self.init_window_name, width=30, height=1)  # 原始数据录入框
        self.userID_Text.grid(row=3, column=7, rowspan=1, columnspan=2)

        self.userName = Label(self.init_window_name, text="userName（必填）")
        self.userName.grid(row=5, column=6,rowspan=2)
        self.userName_Text = Text(self.init_window_name, width=30, height=1)  #原始数据录入框
        self.userName_Text.grid(row=5, column=7, rowspan=1, columnspan=2)

        self.appid = Label(self.init_window_name, text="appid（必填）")
        self.appid.grid(row=7, column=6, rowspan=2)
        self.appid_Text = Text(self.init_window_name, width=30, height=1)  # 原始数据录入框
        self.appid_Text.grid(row=7, column=7, rowspan=1, columnspan=2)

        self.mfid = Label(self.init_window_name, text="mfid（批量检测时置为空）")
        self.mfid.grid(row=9, column=6, rowspan=2)
        self.mfid_Text = Text(self.init_window_name, width=30, height=1)  # 原始数据录入框
        self.mfid_Text.grid(row=9, column=7, rowspan=1, columnspan=2)

        self.equid = Label(self.init_window_name, text="equid（批量检测时置为空）")
        self.equid.grid(row=11, column=6, rowspan=2)
        self.equid_Text = Text(self.init_window_name, width=30, height=1)  # 原始数据录入框
        self.equid_Text.grid(row=11, column=7, rowspan=1, columnspan=2)

        #下拉框
        self.feature = Label(self.init_window_name, text="feature设备能力（批量检测时置为空）")
        self.feature.grid(row=13, column=6, rowspan=1)
        self.numberChosen = ttk.Combobox(self.init_window_name,width=27,state='readonly')
        self.numberChosen['values']=('','B_SglFreqMeas','B_SglFreqDF','B_FScan','B_PScan','B_MScan')
        self.numberChosen.grid(row=13, column=7, rowspan=1, columnspan=2)
        self.numberChosen.current(1)

        self.logs = Label(self.init_window_name, text="消息")
        self.logs.grid(row=15, column=5, rowspan=2)
        self.logs_Text = Text(self.init_window_name, width=65, height=20)  # 原始数据录入框
        #self.logs_Text.delete(1.0,'end')

        self.logs_Text.grid(row=15, column=6, rowspan=1, columnspan=2)

        self.result = Label(self.init_window_name, text="测试结果")
        self.result.grid(row=13, column=13, rowspan=1)
        self.result_Text = Text(self.init_window_name, width=29, height=20)  # 原始数据录入框
        self.result_Text.grid(row=15, column=13, rowspan=1, columnspan=2)
        #self.result_Text.delete(1.0,'end')


        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="开始", bg="lightblue", width=10,command=self.on_open)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=20, column=7)

        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="批量开始", bg="lightblue", width=10,command=self.on_Allopen)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=20, column=8)

        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="停止", bg="lightblue", width=10,command=self.stop)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=20, column=13)

        # 按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="批量检测导入", bg="lightblue", width=10,command=self.loadfile)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=1, column=13)

    def loadfile(self):
        global file_path
        file_path = filedialog.askopenfilename()
        self.logs_Text.delete(1.0, 'end')
        self.result_Text.delete(1.0, 'end')
        self.mfid_Text.delete(1.0, 'end')
        self.equid_Text.delete(1.0, 'end')
        self.numberChosen.current(0)

    def stop(self):
        global action
        action = action+1
        self.logs_Text.delete(1.0, 'end')
        self.result_Text.delete(1.0, 'end')

    def on_open(self):

#获取输入变量值
        global action
        global content
        action = 1
        PortalIP = self.PortalIP_Text.get(1.0, END).strip().replace("\n", "").encode()
        userID = self.userID_Text.get(1.0, END).strip().replace("\n", "").encode()
        userName = self.userName_Text.get(1.0, END).strip().replace("\n", "").encode()
        appid = self.appid_Text.get(1.0, END).strip().replace("\n", "").encode()
        mfid = self.mfid_Text.get(1.0, END).strip().replace("\n", "").encode()
        equid = self.equid_Text.get(1.0, END).strip().replace("\n", "").encode()
        feature = self.numberChosen.get()
        featureList = {"B_SglFreqMeas":"task-fixfq","B_FScan":"task-fscan","B_PScan":"task-pscan","B_MScan":"task-mscan","B_SglFreqDF":"task-fixdf"}
        typei = featureList[feature]
#变量类型处理
        PortalIP = str(PortalIP,encoding="utf8")
        userID = str(userID,encoding="utf8")
        userName = str(userName,encoding="utf8")
        appid = str(appid,encoding="utf8")
        mfid = str(mfid,encoding="utf8")
        equid = str(equid,encoding="utf8")
        url = url1 % (PortalIP)

        def run(*args):
            if feature == 'B_SglFreqMeas':
                global content
                content_fixfq = {"userName": "43000001", "cmdName": "GmsStart",
                           "param": "{\"userAccount\":\"{\\\"user\\\":\\\"43000001\\\",\\\"username\\\":\\\"自动化\\\",\\\"userrmpno\\\":\\\"43000001\\\"}\",\"type\":\"task-fixfq\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"43010000130011\",\"equid\":\"9bffc735-3bf9-448e-be3d-fe852c784a2f\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>000000-01-0004</srrc:appid><srrc:userid>43000001</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>43010000130011</srrc:mfid><srrc:equid>9bffc735-3bf9-448e-be3d-fe852c784a2f</srrc:equid><srrc:feature>B_SglFreqMeas</srrc:feature><srrc:equpara><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>span</srrc:paraname><srrc:paravalue>100000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfmode</srrc:paraname><srrc:paravalue>NORM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>squelchthreshold</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>afc</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfattenuation</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>mgc</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>bwmeasuremode</srrc:paraname><srrc:paravalue>xdb</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>antennaselect</srrc:paraname><srrc:paravalue>监测天线</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>audiotype</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>spectrumswitch</srrc:paraname><srrc:paravalue>ON</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ITUSwitch</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>IQSwitch</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item></srrc:items></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"B_SglFreqMeas\",\"taskType\":\"B_SglFreqMeas\",\"reserveParam\":\"{\\\"reserveParam\\\":\\\"null\\\",\\\"tdScheduleParam\\\":{\\\"squelchswitch\\\":1,\\\"aduidRecordThreshold\\\":0}}\"}],\"param\":\"\"}"}
                content_fixfq["userName"] = userID
                param = '''{\"userAccount\":\"{\\\"user\\\":\\\"%s\\\",\\\"username\\\":\\\"%s\\\",\\\"userrmpno\\\":\\\"%s\\\"}\",\"type\":\"%s\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"%s\",\"equid\":\"%s\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>%s</srrc:appid><srrc:userid>%s</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>%s</srrc:mfid><srrc:equid>%s</srrc:equid><srrc:feature>%s</srrc:feature><srrc:equpara><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>span</srrc:paraname><srrc:paravalue>100000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfmode</srrc:paraname><srrc:paravalue>NORM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>squelchthreshold</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>afc</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfattenuation</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>mgc</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>bwmeasuremode</srrc:paraname><srrc:paravalue>xdb</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>antennaselect</srrc:paraname><srrc:paravalue>监测天线</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>audiotype</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>spectrumswitch</srrc:paraname><srrc:paravalue>ON</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ITUSwitch</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>IQSwitch</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item></srrc:items></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"%s\",\"taskType\":\"%s\",\"reserveParam\":\"{\\\\"reserveParam\\\\":\\\\"null\\\\",\\\\"tdScheduleParam\\\\":{\\\\"squelchswitch\\\\":1,\\\\"aduidRecordThreshold\\\\":0}}\"}],\"param\":\"\"}'''
                paramNew = param % (
                userID, userName, userID, typei, mfid, equid, appid, userID, mfid, equid, feature, feature, feature)
                content_fixfq["userName"] = paramNew
                content = content_fixfq
            if feature == 'B_FScan':
                content_fscan = {"userName":"43000001","cmdName":"GmsStart","param":"{\"userAccount\":\"{\\\"user\\\":\\\"43000001\\\",\\\"username\\\":\\\"自动化\\\",\\\"userrmpno\\\":\\\"43000001\\\"}\",\"type\":\"task-fscan\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"43010000130011\",\"equid\":\"9bffc735-3bf9-448e-be3d-fe852c784a2f\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:userid>43000001</srrc:userid><srrc:appid>000000-01-0004</srrc:appid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:feature>B_FScan</srrc:feature><srrc:mfid>43010000130011</srrc:mfid><srrc:equid>9bffc735-3bf9-448e-be3d-fe852c784a2f</srrc:equid><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>startfreq</srrc:paraname><srrc:paravalue>87000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>stopfreq</srrc:paraname><srrc:paravalue>108000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>step</srrc:paraname><srrc:paravalue>25000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>scantype</srrc:paraname><srrc:paravalue>FSCAN</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"B_FScan\",\"taskType\":\"B_FScan\",\"reserveParam\":\"{\\\"roomid\\\":\\\"43010000130011\\\",\\\"abstractParam\\\":[{\\\"segmentId\\\":\\\"1\\\",\\\"thresholdType\\\":\\\"automatic\\\",\\\"threshold\\\":5,\\\"templateThreshold\\\":[],\\\"peakThreshold\\\":15}]}\"}]}"}
                content_fscan["userName"] = userID
                param = '''{\"userAccount\":\"{\\\"user\\\":\\\"%s\\\",\\\"username\\\":\\\"%s\\\",\\\"userrmpno\\\":\\\"%s\\\"}\",\"type\":\"%s\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"%s\",\"equid\":\"%s\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:userid>%s</srrc:userid><srrc:appid>%s</srrc:appid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:feature>%s</srrc:feature><srrc:mfid>%s</srrc:mfid><srrc:equid>%s</srrc:equid><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>startfreq</srrc:paraname><srrc:paravalue>87000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>stopfreq</srrc:paraname><srrc:paravalue>108000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>step</srrc:paraname><srrc:paravalue>25000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>scantype</srrc:paraname><srrc:paravalue>FSCAN</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"%s\",\"taskType\":\"%s\",\"reserveParam\":\"{\\\"roomid\\\":\\\"%s\\\",\\\"abstractParam\\\":[{\\\"segmentId\\\":\\\"1\\\",\\\"thresholdType\\\":\\\"automatic\\\",\\\"threshold\\\":5,\\\"templateThreshold\\\":[],\\\"peakThreshold\\\":15}]}\"}]}'''
                paramNew = param % (userID, userName, userID, typei, mfid, equid, userID, appid, feature, mfid, equid, feature, feature, mfid)
                content_fscan["userName"] = paramNew
                content = content_fscan
            if feature == 'B_PScan':
                content_pscan = {"userName":"43000001","cmdName":"GmsStart","param":"{\"userAccount\":\"{\\\"user\\\":\\\"43000001\\\",\\\"username\\\":\\\"自动化\\\",\\\"userrmpno\\\":\\\"43000001\\\"}\",\"type\":\"task-pscan\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"43010000130011\",\"equid\":\"9bffc735-3bf9-448e-be3d-fe852c784a2f\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:userid>43000001</srrc:userid><srrc:appid>000000-01-0004</srrc:appid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:feature>B_PScan</srrc:feature><srrc:mfid>43010000130011</srrc:mfid><srrc:equid>9bffc735-3bf9-448e-be3d-fe852c784a2f</srrc:equid><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>startfreq</srrc:paraname><srrc:paravalue>87000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>stopfreq</srrc:paraname><srrc:paravalue>108000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>step</srrc:paraname><srrc:paravalue>25000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>scantype</srrc:paraname><srrc:paravalue>PSCAN</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"B_PScan\",\"taskType\":\"B_PScan\",\"reserveParam\":\"{\\\"roomid\\\":\\\"43010000130011\\\",\\\"abstractParam\\\":[{\\\"segmentId\\\":\\\"1\\\",\\\"thresholdType\\\":\\\"automatic\\\",\\\"threshold\\\":5,\\\"templateThreshold\\\":[],\\\"peakThreshold\\\":15}]}\"}]}"}
                content_pscan["userName"] = userID
                param = '''{\"userAccount\":\"{\\\"user\\\":\\\"%s\\\",\\\"username\\\":\\\"%s\\\",\\\"userrmpno\\\":\\\"%s\\\"}\",\"type\":\"%s\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"%s\",\"equid\":\"%s\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:userid>%s</srrc:userid><srrc:appid>%s</srrc:appid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:feature>%s</srrc:feature><srrc:mfid>%s</srrc:mfid><srrc:equid>%s</srrc:equid><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>startfreq</srrc:paraname><srrc:paravalue>87000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>stopfreq</srrc:paraname><srrc:paravalue>108000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>step</srrc:paraname><srrc:paravalue>25000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>scantype</srrc:paraname><srrc:paravalue>PSCAN</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"%s\",\"taskType\":\"%s\",\"reserveParam\":\"{\\\"roomid\\\":\\\"%s\\\",\\\"abstractParam\\\":[{\\\"segmentId\\\":\\\"1\\\",\\\"thresholdType\\\":\\\"automatic\\\",\\\"threshold\\\":5,\\\"templateThreshold\\\":[],\\\"peakThreshold\\\":15}]}\"}]}'''
                paramNew = param % (userID, userName, userID, typei,mfid, equid, userID, appid, feature, mfid, equid, feature, feature, mfid)
                content_pscan["param"] = paramNew
                content = content_pscan
            if feature == 'B_MScan':
                content_mscan = {"userName":"43000001","cmdName":"GmsStart","param":"{\"userAccount\":\"{\\\"user\\\":\\\"43000001\\\",\\\"username\\\":\\\"自动化\\\",\\\"userrmpno\\\":\\\"43000001\\\"}\",\"type\":\"task-mscan\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"43010000130011\",\"equid\":\"9bffc735-3bf9-448e-be3d-fe852c784a2f\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>000000-01-0004</srrc:appid><srrc:userid>43000001</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>43010000130011</srrc:mfid><srrc:equid>9bffc735-3bf9-448e-be3d-fe852c784a2f</srrc:equid><srrc:feature>B_MScan</srrc:feature><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>antennaselect</srrc:paraname><srrc:paravalue>监测天线</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>key</srrc:paraname><srrc:paravalue>1</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"B_MScan\",\"taskType\":\"B_MScan\"}],\"param\":\"\"}"}
                content_mscan["userName"] = userID
                param = '''{\"userAccount\":\"{\\\"user\\\":\\\"%s\\\",\\\"username\\\":\\\"%s\\\",\\\"userrmpno\\\":\\\"%s\\\"}\",\"type\":\"%s\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"%s\",\"equid\":\"%s\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>%s</srrc:appid><srrc:userid>%s</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>%s</srrc:mfid><srrc:equid>%s</srrc:equid><srrc:feature>%s</srrc:feature><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>antennaselect</srrc:paraname><srrc:paravalue>监测天线</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>key</srrc:paraname><srrc:paravalue>1</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"%s\",\"taskType\":\"%s\"}],\"param\":\"\"}'''
                paramNew = param % (userID,userName,userID,typei,mfid,equid,appid,userID,mfid,equid,feature,feature,feature)
                content_mscan["param"] = paramNew
                content = content_mscan
                # websocket.enableTrace(True)                      #打开跟踪，查看日志
            # self.logs_Text.insert(1.0, '收到回复消息1:',self.numberChosen.get())
            if feature == 'B_SglFreqDF':
                content_fixdf = {"userName":"43000001","cmdName":"GmsStart","param":"{\"type\":\"task-fixdf\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"43010000130011\",\"equid\":\"9bffc735-3bf9-448e-be3d-fe852c784a2f\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>000000-01-0004</srrc:appid><srrc:userid>43000001</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>43010000130011</srrc:mfid><srrc:equid>9bffc735-3bf9-448e-be3d-fe852c784a2f</srrc:equid><srrc:feature>B_SglFreqDF</srrc:feature><srrc:equpara><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>span</srrc:paraname><srrc:paravalue>20000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfbw</srrc:paraname><srrc:paravalue>3750</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>blockaveragingcycles</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfampthreshold</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>0.1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>integrationtime</srrc:paraname><srrc:paravalue>0.1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>afc</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfattenuation</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfmode</srrc:paraname><srrc:paravalue>NORM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>mgc</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfmode</srrc:paraname><srrc:paravalue>CONT</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>horizontal</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>audiotype</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>spectrumswitch</srrc:paraname><srrc:paravalue>ON</srrc:paravalue></srrc:item></srrc:items></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"B_SglFreqDF\",\"taskType\":\"B_SglFreqDF\"}],\"param\":\"\",\"userAccount\":\"{\\\"user\\\":\\\"43000001\\\",\\\"username\\\":\\\"自动化\\\",\\\"userrmpno\\\":\\\"43000001\\\"}\"}"}
                content_fixdf["userName"] = userID
                param = '''{\"type\":\"%s\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"%s\",\"equid\":\"%s\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>%s</srrc:appid><srrc:userid>%s</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>%s</srrc:mfid><srrc:equid>%s</srrc:equid><srrc:feature>%s</srrc:feature><srrc:equpara><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>span</srrc:paraname><srrc:paravalue>20000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfbw</srrc:paraname><srrc:paravalue>3750</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>blockaveragingcycles</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfampthreshold</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>0.1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>integrationtime</srrc:paraname><srrc:paravalue>0.1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>afc</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfattenuation</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfmode</srrc:paraname><srrc:paravalue>NORM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>mgc</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfmode</srrc:paraname><srrc:paravalue>CONT</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>horizontal</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>audiotype</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>spectrumswitch</srrc:paraname><srrc:paravalue>ON</srrc:paravalue></srrc:item></srrc:items></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"%s\",\"taskType\":\"%s\"}],\"param\":\"\",\"userAccount\":\"{\\\"user\\\":\\\"%s\\\",\\\"username\\\":\\\"%s\\\",\\\"userrmpno\\\":\\\"%s\\\"}\"}'''
                paramNew = param % (typei,mfid,equid,appid,userID,mfid,equid,feature,feature,feature,userID,userName,userID)
                content_fixdf["param"] = paramNew
                content = content_fixdf


            while 1:
                ws = create_connection(url)  # 创建连接
                #self.logs_Text.insert(1.0, type(json.dumps(content)))
                ws.send(json.dumps(content))
                while 1:
                    recv = ws.recv()
                    if "true" in recv:
                        #print('收到回复消息1:', recv)  # 打印服务器响应数据
                        self.logs_Text.delete(1.0, 'end')
                        self.logs_Text.insert(1.0,'收到回复消息1:', recv,'\n')
                        content1 = {"cmdName": "CmdConfirm"}
                        recv1 = str(recv)
                        object = json.loads(recv1)

                        self.logs_Text.insert(1.0,'任务ID为:', object["data"]["object"])
                        ws.send(json.dumps(content1))
                        sendTime =  int(round(time.time()*1000))
                        a =1
                        while True:
                            if a==1:
                                #self.logs_Text.insert(1.0, '收到回复消息1:',a,ws.recv())
                                #self.result_Text.insert(1.0, '收到回复消息1:', a, ws.recv())
                                recvTime = int(round(time.time()*1000))

                                self.result_Text.insert(1.0, "收到监测数据，发送接收监测数据时差%s毫秒\n"%(recvTime-sendTime),a)
                                a = a + 1
                            if a==2:
                                self.logs_Text.insert(1.0, '收到监测数据2:',a, ws.recv(),'\n')

                                if action==2:
                                    content2 = {"userName":"43000001","cmdName":"GmsStop","param":"%s"}
                                    content2["param"] = object
                                    #stopContent1 = json.loads(stopContent)
                                    ws.send(json.dumps(content2))  # 发送停止请求

                                    #while True:
                                    #stoprecv = ws.recv()
                                        #print('收到回复消息stoprecv:', stoprecv)  # 打印服务器响应数据
                                        #if "停止任务成功" in stoprecv:
                                            #print('收到回复消息stoprecv:', stoprecv)  # 打印服务器响应数据
                                            #self.result_Text.insert(1.0, '停止任务成功')
                                    self.result_Text.insert(1.0, '停止任务成功 \n')
                                    ws.close()# 关闭连接
                                    a = a + 1

                                    break
                                    # except Exception as e:
                                    #         # self.logs_Text.insert(1.0, "文件操作失败\n")
                                    #     #print('停止任务无响应')  # 打印服务器响应数据
                                    #     self.logs_Text.insert(1.0, '停止任务无响应')
                                    #     ws.close()# 关闭连接
                                    #     break
                        break

                    else:
                        self.logs_Text.insert(1.0, '收到回复消息1:',recv,'\n')
                        continue

                break


                    # else:
                    #     print('收到回复消息4:', ws.recv())  # 打印服务器响应数据
                # except Exception as e:
                #     #self.logs_Text.insert(1.0, "文件操作失败\n")
                #     print('未接收到监测数据')  # 打印服务器响应数据


        _thread.start_new_thread(run, ())

    def on_Allopen(self):
        global action
        global file_path
        global content
        action = 1
        #输入框获取
        PortalIP = self.PortalIP_Text.get(1.0, END).strip().replace("\n", "").encode()
        userID = self.userID_Text.get(1.0, END).strip().replace("\n", "").encode()
        userName = self.userName_Text.get(1.0, END).strip().replace("\n", "").encode()
        appid = self.appid_Text.get(1.0, END).strip().replace("\n", "").encode()
        featureList = {"B_SglFreqMeas": "task-fixfq", "B_Fscan": "task-fscan", "B_Pscan": "task-pscan",
                       "B_Mscan": "task-mscan", "B_SglFreqDF": "task-fixdf"}
        # 变量类型处理
        PortalIP = str(PortalIP, encoding="utf8")
        userID = str(userID, encoding="utf8")
        userName = str(userName, encoding="utf8")
        appid = str(appid, encoding="utf8")
        url = url1 % (PortalIP)


        def getSource(sourceDir, sheetIndex=0):
            with xlrd.open_workbook(sourceDir) as workbook:
                table = workbook.sheets()[sheetIndex]
                for i in range(table.nrows):
                    yield table.row_values(i)

        def run1(*args):
            global content
            for rowList in getSource(file_path):
                time.sleep(1)
                mfid = rowList[0]
                equid = rowList[1]
                feature = rowList[2]
                typei = featureList[feature]

                if feature == 'B_SglFreqMeas':
                    #global content
                    content_fixfq = {"userName": "43000001", "cmdName": "GmsStart",
                                     "param": "{\"userAccount\":\"{\\\"user\\\":\\\"43000001\\\",\\\"username\\\":\\\"自动化\\\",\\\"userrmpno\\\":\\\"43000001\\\"}\",\"type\":\"task-fixfq\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"43010000130011\",\"equid\":\"9bffc735-3bf9-448e-be3d-fe852c784a2f\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>000000-01-0004</srrc:appid><srrc:userid>43000001</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>43010000130011</srrc:mfid><srrc:equid>9bffc735-3bf9-448e-be3d-fe852c784a2f</srrc:equid><srrc:feature>B_SglFreqMeas</srrc:feature><srrc:equpara><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>span</srrc:paraname><srrc:paravalue>100000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfmode</srrc:paraname><srrc:paravalue>NORM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>squelchthreshold</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>afc</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfattenuation</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>mgc</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>bwmeasuremode</srrc:paraname><srrc:paravalue>xdb</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>antennaselect</srrc:paraname><srrc:paravalue>监测天线</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>audiotype</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>spectrumswitch</srrc:paraname><srrc:paravalue>ON</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ITUSwitch</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>IQSwitch</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item></srrc:items></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"B_SglFreqMeas\",\"taskType\":\"B_SglFreqMeas\",\"reserveParam\":\"{\\\"reserveParam\\\":\\\"null\\\",\\\"tdScheduleParam\\\":{\\\"squelchswitch\\\":1,\\\"aduidRecordThreshold\\\":0}}\"}],\"param\":\"\"}"}
                    content_fixfq["userName"] = userID
                    param = '''{\"userAccount\":\"{\\\"user\\\":\\\"%s\\\",\\\"username\\\":\\\"%s\\\",\\\"userrmpno\\\":\\\"%s\\\"}\",\"type\":\"%s\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"%s\",\"equid\":\"%s\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>%s</srrc:appid><srrc:userid>%s</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>%s</srrc:mfid><srrc:equid>%s</srrc:equid><srrc:feature>%s</srrc:feature><srrc:equpara><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>span</srrc:paraname><srrc:paravalue>100000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfmode</srrc:paraname><srrc:paravalue>NORM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>squelchthreshold</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>afc</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfattenuation</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>mgc</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>bwmeasuremode</srrc:paraname><srrc:paravalue>xdb</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>antennaselect</srrc:paraname><srrc:paravalue>监测天线</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>audiotype</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>spectrumswitch</srrc:paraname><srrc:paravalue>ON</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ITUSwitch</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>IQSwitch</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item></srrc:items></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"%s\",\"taskType\":\"%s\",\"reserveParam\":\"{\\\\"reserveParam\\\\":\\\\"null\\\\",\\\\"tdScheduleParam\\\\":{\\\\"squelchswitch\\\\":1,\\\\"aduidRecordThreshold\\\\":0}}\"}],\"param\":\"\"}'''
                    paramNew = param % (
                        userID, userName, userID, typei, mfid, equid, appid, userID, mfid, equid, feature, feature,
                        feature)
                    content_fixfq["userName"] = paramNew
                    content = content_fixfq
                if feature == 'B_FScan':
                    content_fscan = {"userName": "43000001", "cmdName": "GmsStart",
                                     "param": "{\"userAccount\":\"{\\\"user\\\":\\\"43000001\\\",\\\"username\\\":\\\"自动化\\\",\\\"userrmpno\\\":\\\"43000001\\\"}\",\"type\":\"task-fscan\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"43010000130011\",\"equid\":\"9bffc735-3bf9-448e-be3d-fe852c784a2f\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:userid>43000001</srrc:userid><srrc:appid>000000-01-0004</srrc:appid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:feature>B_FScan</srrc:feature><srrc:mfid>43010000130011</srrc:mfid><srrc:equid>9bffc735-3bf9-448e-be3d-fe852c784a2f</srrc:equid><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>startfreq</srrc:paraname><srrc:paravalue>87000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>stopfreq</srrc:paraname><srrc:paravalue>108000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>step</srrc:paraname><srrc:paravalue>25000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>scantype</srrc:paraname><srrc:paravalue>FSCAN</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"B_FScan\",\"taskType\":\"B_FScan\",\"reserveParam\":\"{\\\"roomid\\\":\\\"43010000130011\\\",\\\"abstractParam\\\":[{\\\"segmentId\\\":\\\"1\\\",\\\"thresholdType\\\":\\\"automatic\\\",\\\"threshold\\\":5,\\\"templateThreshold\\\":[],\\\"peakThreshold\\\":15}]}\"}]}"}
                    content_fscan["userName"] = userID
                    param = '''{\"userAccount\":\"{\\\"user\\\":\\\"%s\\\",\\\"username\\\":\\\"%s\\\",\\\"userrmpno\\\":\\\"%s\\\"}\",\"type\":\"%s\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"%s\",\"equid\":\"%s\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:userid>%s</srrc:userid><srrc:appid>%s</srrc:appid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:feature>%s</srrc:feature><srrc:mfid>%s</srrc:mfid><srrc:equid>%s</srrc:equid><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>startfreq</srrc:paraname><srrc:paravalue>87000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>stopfreq</srrc:paraname><srrc:paravalue>108000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>step</srrc:paraname><srrc:paravalue>25000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>scantype</srrc:paraname><srrc:paravalue>FSCAN</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"%s\",\"taskType\":\"%s\",\"reserveParam\":\"{\\\"roomid\\\":\\\"%s\\\",\\\"abstractParam\\\":[{\\\"segmentId\\\":\\\"1\\\",\\\"thresholdType\\\":\\\"automatic\\\",\\\"threshold\\\":5,\\\"templateThreshold\\\":[],\\\"peakThreshold\\\":15}]}\"}]}'''
                    paramNew = param % (
                    userID, userName, userID, typei, mfid, equid, userID, appid, feature, mfid, equid, feature, feature,
                    mfid)
                    content_fscan["userName"] = paramNew
                    content = content_fscan
                if feature == 'B_PScan':
                    content_pscan = {"userName": "43000001", "cmdName": "GmsStart",
                                     "param": "{\"userAccount\":\"{\\\"user\\\":\\\"43000001\\\",\\\"username\\\":\\\"自动化\\\",\\\"userrmpno\\\":\\\"43000001\\\"}\",\"type\":\"task-pscan\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"43010000130011\",\"equid\":\"9bffc735-3bf9-448e-be3d-fe852c784a2f\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:userid>43000001</srrc:userid><srrc:appid>000000-01-0004</srrc:appid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:feature>B_PScan</srrc:feature><srrc:mfid>43010000130011</srrc:mfid><srrc:equid>9bffc735-3bf9-448e-be3d-fe852c784a2f</srrc:equid><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>startfreq</srrc:paraname><srrc:paravalue>87000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>stopfreq</srrc:paraname><srrc:paravalue>108000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>step</srrc:paraname><srrc:paravalue>25000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>scantype</srrc:paraname><srrc:paravalue>PSCAN</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"B_PScan\",\"taskType\":\"B_PScan\",\"reserveParam\":\"{\\\"roomid\\\":\\\"43010000130011\\\",\\\"abstractParam\\\":[{\\\"segmentId\\\":\\\"1\\\",\\\"thresholdType\\\":\\\"automatic\\\",\\\"threshold\\\":5,\\\"templateThreshold\\\":[],\\\"peakThreshold\\\":15}]}\"}]}"}
                    content_pscan["userName"] = userID
                    param = '''{\"userAccount\":\"{\\\"user\\\":\\\"%s\\\",\\\"username\\\":\\\"%s\\\",\\\"userrmpno\\\":\\\"%s\\\"}\",\"type\":\"%s\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"%s\",\"equid\":\"%s\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:userid>%s</srrc:userid><srrc:appid>%s</srrc:appid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:feature>%s</srrc:feature><srrc:mfid>%s</srrc:mfid><srrc:equid>%s</srrc:equid><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>startfreq</srrc:paraname><srrc:paravalue>87000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>stopfreq</srrc:paraname><srrc:paravalue>108000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>step</srrc:paraname><srrc:paravalue>25000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>detector</srrc:paraname><srrc:paravalue>AVG</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>DEF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>scantype</srrc:paraname><srrc:paravalue>PSCAN</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"%s\",\"taskType\":\"%s\",\"reserveParam\":\"{\\\"roomid\\\":\\\"%s\\\",\\\"abstractParam\\\":[{\\\"segmentId\\\":\\\"1\\\",\\\"thresholdType\\\":\\\"automatic\\\",\\\"threshold\\\":5,\\\"templateThreshold\\\":[],\\\"peakThreshold\\\":15}]}\"}]}'''
                    paramNew = param % (
                    userID, userName, userID, typei, mfid, equid, userID, appid, feature, mfid, equid, feature, feature,
                    mfid)
                    content_pscan["param"] = paramNew
                    content = content_pscan
                if feature == 'B_MScan':
                    content_mscan = {"userName": "43000001", "cmdName": "GmsStart",
                                     "param": "{\"userAccount\":\"{\\\"user\\\":\\\"43000001\\\",\\\"username\\\":\\\"自动化\\\",\\\"userrmpno\\\":\\\"43000001\\\"}\",\"type\":\"task-mscan\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"43010000130011\",\"equid\":\"9bffc735-3bf9-448e-be3d-fe852c784a2f\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>000000-01-0004</srrc:appid><srrc:userid>43000001</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>43010000130011</srrc:mfid><srrc:equid>9bffc735-3bf9-448e-be3d-fe852c784a2f</srrc:equid><srrc:feature>B_MScan</srrc:feature><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>antennaselect</srrc:paraname><srrc:paravalue>监测天线</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>key</srrc:paraname><srrc:paravalue>1</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"B_MScan\",\"taskType\":\"B_MScan\"}],\"param\":\"\"}"}
                    content_mscan["userName"] = userID
                    param = '''{\"userAccount\":\"{\\\"user\\\":\\\"%s\\\",\\\"username\\\":\\\"%s\\\",\\\"userrmpno\\\":\\\"%s\\\"}\",\"type\":\"%s\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"%s\",\"equid\":\"%s\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>%s</srrc:appid><srrc:userid>%s</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>%s</srrc:mfid><srrc:equid>%s</srrc:equid><srrc:feature>%s</srrc:feature><srrc:equpara><srrc:groupitems><srrc:groupitem><srrc:groupid>1</srrc:groupid><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>antennaselect</srrc:paraname><srrc:paravalue>监测天线</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>vertical</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>fieldstrength</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>Antennaselect</srrc:paraname><srrc:paravalue>E5E790CD-A456-44B0-B2F0-99DB632AFAC1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>key</srrc:paraname><srrc:paravalue>1</srrc:paravalue></srrc:item></srrc:items></srrc:groupitem></srrc:groupitems></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"%s\",\"taskType\":\"%s\"}],\"param\":\"\"}'''
                    paramNew = param % (
                    userID, userName, userID, typei, mfid, equid, appid, userID, mfid, equid, feature, feature, feature)
                    content_mscan["param"] = paramNew
                    content = content_mscan
                    # websocket.enableTrace(True)                      #打开跟踪，查看日志
                # self.logs_Text.insert(1.0, '收到回复消息1:',self.numberChosen.get())
                if feature == 'B_SglFreqDF':
                    content_fixdf = {"userName": "43000001", "cmdName": "GmsStart",
                                     "param": "{\"type\":\"task-fixdf\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"43010000130011\",\"equid\":\"9bffc735-3bf9-448e-be3d-fe852c784a2f\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>000000-01-0004</srrc:appid><srrc:userid>43000001</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>43010000130011</srrc:mfid><srrc:equid>9bffc735-3bf9-448e-be3d-fe852c784a2f</srrc:equid><srrc:feature>B_SglFreqDF</srrc:feature><srrc:equpara><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>span</srrc:paraname><srrc:paravalue>20000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfbw</srrc:paraname><srrc:paravalue>3750</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>blockaveragingcycles</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfampthreshold</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>0.1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>integrationtime</srrc:paraname><srrc:paravalue>0.1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>afc</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfattenuation</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfmode</srrc:paraname><srrc:paravalue>NORM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>mgc</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfmode</srrc:paraname><srrc:paravalue>CONT</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>horizontal</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>audiotype</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>spectrumswitch</srrc:paraname><srrc:paravalue>ON</srrc:paravalue></srrc:item></srrc:items></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"B_SglFreqDF\",\"taskType\":\"B_SglFreqDF\"}],\"param\":\"\",\"userAccount\":\"{\\\"user\\\":\\\"43000001\\\",\\\"username\\\":\\\"自动化\\\",\\\"userrmpno\\\":\\\"43000001\\\"}\"}"}
                    content_fixdf["userName"] = userID
                    param = '''{\"type\":\"%s\",\"priority\":1,\"deviceParam\":[{\"mfid\":\"%s\",\"equid\":\"%s\",\"bsCode\":\"1\",\"psCode\":\"1\",\"param\":\"<srrc:requestbody><srrc:appid>%s</srrc:appid><srrc:userid>%s</srrc:userid><srrc:priority>1</srrc:priority><srrc:executetime>0</srrc:executetime><srrc:mfid>%s</srrc:mfid><srrc:equid>%s</srrc:equid><srrc:feature>%s</srrc:feature><srrc:equpara><srrc:items><srrc:item><srrc:paraname>frequency</srrc:paraname><srrc:paravalue>101700000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>ifbw</srrc:paraname><srrc:paravalue>120000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>span</srrc:paraname><srrc:paravalue>20000000</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfbw</srrc:paraname><srrc:paravalue>3750</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>blockaveragingcycles</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfampthreshold</srrc:paraname><srrc:paravalue>0</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>demodmode</srrc:paraname><srrc:paravalue>FM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>measureTime</srrc:paraname><srrc:paravalue>0.1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>integrationtime</srrc:paraname><srrc:paravalue>0.1</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>afc</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfattenuation</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>rfmode</srrc:paraname><srrc:paravalue>NORM</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>mgc</srrc:paraname><srrc:paravalue>AUTO</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>dfmode</srrc:paraname><srrc:paravalue>CONT</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>polarization</srrc:paraname><srrc:paravalue>horizontal</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>audiotype</srrc:paraname><srrc:paravalue>OFF</srrc:paravalue></srrc:item><srrc:item><srrc:paraname>spectrumswitch</srrc:paraname><srrc:paravalue>ON</srrc:paravalue></srrc:item></srrc:items></srrc:equpara></srrc:requestbody>\",\"bizKey\":\"%s\",\"taskType\":\"%s\"}],\"param\":\"\",\"userAccount\":\"{\\\"user\\\":\\\"%s\\\",\\\"username\\\":\\\"%s\\\",\\\"userrmpno\\\":\\\"%s\\\"}\"}'''
                    paramNew = param % (
                    typei, mfid, equid, appid, userID, mfid, equid, feature, feature, feature, userID, userName, userID)
                    content_fixdf["param"] = paramNew
                    content = content_fixdf

                while 1:
                    ws = create_connection(url)  # 创建连接
                    ws.send(json.dumps(content))
                    while 1:
                        recv = ws.recv()
                        if "true" in recv:
                            # print('收到回复消息1:', recv)  # 打印服务器响应数据
                            #self.logs_Text.insert(1.0, '收到回复消息1:', recv, '\n')
                            content1 = {"cmdName": "CmdConfirm"}
                            recv1 = str(recv)
                            object = json.loads(recv1)

                            self.logs_Text.insert(1.0, '任务ID为:', object["data"]["object"])
                            ws.send(json.dumps(content1))
                            sendTime = int(round(time.time() * 1000))
                            a = 1
                            while True:
                                recv = ws.recv()
                                if a == 1:
                                    #self.logs_Text.insert(1.0, '收到回复消息1:',a,recv)
                                    # self.result_Text.insert(1.0, '收到回复消息1:', a, ws.recv())
                                    recvTime = int(round(time.time() * 1000))

                                    self.result_Text.insert(1.0, "收到监测数据，发送接收监测数据时差%s毫秒\n" % (recvTime - sendTime), a)
                                    a = a + 1
                                if a == 2:
                                    self.logs_Text.insert(1.0, '收到监测数据2:', a, ws.recv(), '\n')
                                    self.result_Text.insert(1.0, mfid, equid, feature, '接收到监测数据\n')

                                    content2 = {"userName": "43000001", "cmdName": "GmsStop", "param": "%s"}
                                    content2["userName"] = userName
                                    content2["param"] = object
                                    ws.send(json.dumps(content2))  # 发送停止请求
                                    self.result_Text.insert(1.0, '停止任务成功 \n')
                                    ws.close()  # 关闭连接
                                    break
                            break

                        else:
                            self.logs_Text.insert(1.0, '收到回复消息1:', recv, '\n')
                            continue

                    break
        _thread.start_new_thread(run1, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url1,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    ws.run_forever()
