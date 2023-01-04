
#创建定时任务，每5分钟执行一次:
SCHTASKS /Create /tn 'monitor_update_check' /sc minute /mo 5 /tr "D:\dgbc\windows\monitor_update.bat"
echo 创建成功，请检查...
pause

#删除:
#SCHTASKS /Delete /tn "biaoti"