#获取ftp服务器上monitor-web-1.0.jar更新，重启monitor服务

@echo off 
SET currenTime=%date% %time%
SET	idName=test.cit		#标识文件名（任意文件），每个机房使用不重复的标识文件名，该文件存放在ftp服务器的heading_code中，标识文件存在时，对应机房开始更新jar包，反之不执行更新
SET updateFile=monitor-web-new.jar	#更新的jar包，统一重命名为该文件名
SET currentFile=monitor-web-1.0.jar
SET backupFile=monitor-web-reback.jar
SET bat_path=D:\dgbc\windows\monitor-64.bat		#机房monitor服务启动脚本路径
SET process_name=monitor.exe	monitor进程名，monitor.bat文件里面要修改java.exe的名字

#检查ftp服务器中标识文件是否存在，存在时开始更新，不存在时结束探查
ftp -s:check.txt
if exist %idName% (
	echo %currenTime%:find idName! >>log.log
	
	#获取标识文件和更新包
	ftp -s:get.txt
	if exist %updateFile% (
		echo %currenTime%:download Newfile!>>log.log
		echo %currenTime%:update app start.....>>log.log
		
		wmic process where name=%process_name%  delete
		sleep 2
		
		move %currentFile% %backupFile%
		move %updateFile% %currentFile%
		echo %currenTime%:update complete!>>log.log
		
		#删除标识文件，避免重复更新
		ftp -s:del.txt
		del %idName%
		echo %currenTime%:delete idName >>log.log
		echo %currenTime%:update finished.....>>log.log
		
		start %bat_path%
		echo %currenTime%:restart monitor.exe......>>log.log
	) else (
		del %idName%
		echo %currenTime%:cannot find new File!>>log.log
	)
)


