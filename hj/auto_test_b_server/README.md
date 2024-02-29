* data ：源数据/结果文件存储
* main ：逻辑代码
* 打包命令临时：python -m PyInstaller  -p D:\work\python\tool\hj --add-data "D:\work\python\tool\hj\auto_test_b_server\data;."  -F .\app_start.py