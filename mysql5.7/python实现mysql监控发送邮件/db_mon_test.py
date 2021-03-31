#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@author: huanzhiqiang  
@file: db_mon_test.py  
@time: 2021/3/31 9:02
"""
import re,sys,time,pymysql,timeout_decorator
from pymongo import MongoClient
from sendEmail import send_mail

# sys.path.append('E:\\develop-dyin\\oracle-exp')
# print(sys.path)
host = []
user = []
passwd = []
port = []
auth_db = []

mysql_file='E:\\develop-dyin\\oracle-exp\\mysqldb_message.txt'
def get_message_mysqldb():
	print('读取mysql数据库详细信息文件中，请稍后....')
	with open(mysql_file,'r') as soure:
		lines=soure.read().splitlines()
		print(lines)
		i=0
		for char in lines:
			if char.strip() != '':
				char=re.split(' ',lines[i])
				new_dict={}
				for j in char:
					new_dict[re.split(':',j)[0]]=re.split(':',j)[1]
				host.append(new_dict['host'])
				user.append(new_dict['user'])
				passwd.append(new_dict['passwd'])
				port.append(new_dict['port'])
			i=i+1
		print("读取完成\n---------------------------")
		return host, user, passwd, port
def mysqldb_connect_and_test(ip,user,passwd,port):
	print("连接mysql数据库{0}中，请稍后....".format(ip))
	try:
		conn=pymysql.connect(host=ip,user=user,passwd=passwd,port=int(port),charset='utf8',connect_timeout=3)
		print("连接成功，执行测试语句中...")
		with conn.cursor() as cur:
			sql='select 1 from dual'
			a= str(cur.execute(sql))
			print("successful! 进一步确认数据库服务正常。执行结果-->a: {0}".format(a))
	except Exception:
		print("发生异常,数据库连接失败，服务器ip：{0}".format(ip), Exception)
		send_mail("XXXXX@163.com", ["XXXXXX@qq.com"], [], "警告：mysql数据库服务不可用！！！", "【邮件内容】：\n \t\tpython检测到mysql数据库异常，服务器为{0}，请紧急处理！！！".format(host), "")
	else:
		print("连接成功：{0}\n".format(ip))
		
def clear_list():
	host.clear()
	user.clear()
	passwd.clear()
	port.clear()
def main():
	print("检查mysql数据库")
	get_message_mysqldb()
	index=0
	for ip in host:
		print("--------------",ip,user[index], passwd[index], port[index])
		mysqldb_connect_and_test(ip, user[index], passwd[index], port[index])
		index=index+1
	clear_list()
if __name__ == '__main__':
	main()