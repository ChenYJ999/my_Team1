#!/usr/bin/env python  
#-*- coding: utf-8 -*- 
#	编写者：ChenYJ 
#	作者E-mail:1208882376@qq.com
#	时间: 2017-12-22
#	
import pymysql
import itchat
import re
import time


#数据库配置信息 Dict
config={'host':'localhost',
		'port':3306,
		'user':'OUTER',
		'password':'123456',
		'db':'cyfdata'
}

# 创建连接通道, 设置连接ip, port, 用户, 密码以及所要连接的数据库
mysql_db = pymysql.connect(**config)

# 创建游标, 操作数据库, 指定游标返回内容为字典类型
cursor = mysql_db.cursor()

#1.查询操作  
# 编写sql 查询语句  user 对应我的表名  
def query_mysql():
	sql="select * from FTank"
	Reply = '为您查询到的结果为：\n'
	try:
		cursor.execute(sql)
		#执行sql语句  	  
		results=cursor.fetchall()
#		遍历结果
		for row in results:
			Reply+='水箱ID：00'+str(row[0])+'\n'
			Reply+='水箱Name:'+str(row[1])+'\n'
			Reply+='设定水位：'+str(row[3])+'\n'
			Reply+='当前水位：'+str(row[2])+'\n'
			print(type(row[2]))
			Reply+='更新时间：'+str(row[4])+'\n'
			Reply+='Led状态：' +str(row[5])+'\n'
		return Reply
	

	except Exception as e:
#		raise e
		error = '查询发生错误'
		return error
#	finally:
#		mysql_db.close()
		#关闭连接  
def insert_mysql_targetH(Heigh):
	try:
		sql='update FTank set targetH='+str(Heigh)+' where id=\'001\''
		print(sql)
		cursor.execute(sql)

		sql='update FTank set UpTime='+ '\''+time.asctime() + '\'' + 'where id=\'001\''
		print(sql)
		cursor.execute(sql)

		#提交修改
		mysql_db.commit()
		#执行sql语句  	  
		return '状态更新成功'
	except Exception as e:
#		raise e
		error = '插入发生错误'
		return error
#	finally:
#		mysql_db.close()
		#关闭连接  

def insert_mysql_LedStatus(LedStatus):
	try:
		sql='update FTank set LedStatus='+str(LedStatus)+' where id=\'001\''
		print(sql)
		cursor.execute(sql)

		sql='update FTank set UpTime='+ '\''+time.asctime() + '\'' + 'where id=\'001\''
		print(sql)
		cursor.execute(sql)

		#提交修改
		mysql_db.commit()
		#执行sql语句  	  
		return '状态更新成功'
	except Exception as e:
#		raise e
		error = '插入发生错误'
		return error
#	finally:
#		mysql_db.close()
		#关闭连接  




@itchat.msg_register(itchat.content.TEXT)
def mysql_server(msg):
	if re.search(r'[帮助|help]',msg['Text'],re.L):
		results  = '请回复以下指令:\n'
		results += '1|查询当前状态\n'
		results += '2+Num 设置目标状态 如2+20 设置水位为20cm\n'
		print(results)
		return results

	if re.match(r'[查询|1]',msg['Text']):		
		#返回tuple数据类型
		results = query_mysql()
		print(results)
		#发送给作者的的微信号 ：后门
		itchat.send(results,toUserName='filehelper')		
		#return 给发信息的人
		return results

	if re.search('2\+',msg['Text']):	
		try:	
			target_H = re.search('\+(\d*)',msg['Text'])
			Heigh = (int)(target_H.group(1))
			reply = insert_mysql_targetH(Heigh)
			return reply

		except Exception as e:
#		raise e
			error = '设置发生错误'
			return error	

	
	if re.search('3\+',msg['Text']):	
		try:	
			LED_S = re.search('\+(\d*)',msg['Text'])
			LedStatus = (int)(LED_S.group(1))
			reply = insert_mysql_LedStatus(LedStatus)
			return reply

		except Exception as e:
#		raise e
			error = '设置发生错误'
			return error	



itchat.auto_login(enableCmdQR=2)

itchat.send("Hello,FileHelper",toUserName='filehelper')

itchat.run()
