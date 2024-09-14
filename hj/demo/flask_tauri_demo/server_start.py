import subprocess
import threading
import time

from werkzeug import *

from backend.app import *
from backend.get_relative_path import *


# 创建
stop_event = threading.Event()

def start_backend():
    try:
        # Flask 服务将运行在主线程
        server = run_simple('0.0.0.0', 5000, app)

        while not stop_event.is_set():
            time.sleep(1)
        server.shutdown()
    except Exception as e:
        print(f"后端启动失败: {e}")

def start_Frontend():
    try:
        print("启动前端")
        process = subprocess.Popen([get_path('./src/dgbc.exe')])

        # 等待前端进程消失
        while process.poll() is None:
            time.sleep(1)

        # 设置停止事件，通知后端线程退出
        stop_event.set()
    except Exception as e:
        print(f"前端启动失败: {e}")
        stop_event.set()


if __name__ == '__main__':

    # 创建停止事件
    stop_event = threading.Event()

    # 创建并启动线程
    thread_1 = threading.Thread(target=start_backend)
    thread_2 = threading.Thread(target=start_Frontend)

    thread_1.start()
    thread_2.start()

    # 等待前端线程结束
    thread_2.join()

    # 等待后端线程结束
    thread_1.join()




