#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@author: huanzhiqiang  
@file: sendEmail.py  
@time: 2021/3/31 9:46
"""
import smtplib  # 加载smtplib模块
import traceback
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

login_name = 'XXXXX@163.com'  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
login_pass = 'XXXXXXX'  # 邮箱密码，此处隐藏^_^

def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr((Header(name, 'utf-8').encode(),addr))


def send_mail(sender, recps, Ccs, subject, htmlmsg, fileAttachment):
	# 参数分别是：发送人邮箱、收件人邮箱、抄送人邮箱、主题、内容、附件，如果看不懂此处代码，知道如何使用即可
	smtpserver = 'smtp.163.com'
	receivers = recps + Ccs
	
	try:
		# msg = MIMEText(htmlmsg, 'html', 'utf-8')
		msg = MIMEMultipart()
		msg['Subject'] = Header(subject, 'utf-8').encode()
		msg['From'] = _format_addr(sender)
		Recp = []
		for recp in recps:
			Recp.append(_format_addr(recp))
		
		ccs = []
		for cc in Ccs:
			ccs.append(_format_addr(cc))
		
		msg['To'] = ','.join(Recp)
		msg['Cc'] = ','.join(ccs)
		
		# 附件
		for file in fileAttachment:
			part = MIMEApplication(open(file, 'rb').read())
			attFileName = file.split('/')[-1]
			part.add_header('Content-Disposition', 'attachment', filename=attFileName)
			msg.attach(part)
		#内容
		text_plain = MIMEText(htmlmsg, 'plain', 'utf-8')
		msg.attach(text_plain)
		
		smtp = smtplib.SMTP()
		smtp.connect(smtpserver)
		smtp.login(login_name, login_pass)
		#      smtp.login(username, password)
		smtp.sendmail(sender, receivers, msg.as_string())
		smtp.quit()
		print('SendEmail success')
	except:
		traceback.print_exc()
